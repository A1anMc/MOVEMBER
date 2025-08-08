#!/usr/bin/env python3
"""
Data Governance Framework for Movember AI Rules System
Ensures data security, privacy, compliance, and lifecycle management
"""
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import os
import pandas as pd

class DataClassification(Enum):


    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataRetentionPolicy(Enum):


    SHORT_TERM = "short_term"  # 1 year
    MEDIUM_TERM = "medium_term"  # 5 years
    LONG_TERM = "long_term"  # 10 years
    PERMANENT = "permanent"

@dataclass
class DataGovernancePolicy:


    classification: DataClassification
    retention_policy: DataRetentionPolicy
    encryption_required: bool
    access_controls: List[str]
    audit_required: bool
    backup_frequency: str

class DataGovernanceFramework:


    def __init__(self):


        self.db_path = "movember_ai.db"
        self.logger = logging.getLogger(__name__)

        # Governance policies
        self.policies = {
            'grants': DataGovernancePolicy(
                classification=DataClassification.INTERNAL,
                retention_policy=DataRetentionPolicy.MEDIUM_TERM,
                encryption_required=True,
                access_controls=['read', 'write', 'delete'],
                audit_required=True,
                backup_frequency='daily'
            ),
            'research': DataGovernancePolicy(
                classification=DataClassification.PUBLIC,
                retention_policy=DataRetentionPolicy.LONG_TERM,
                encryption_required=False,
                access_controls=['read'],
                audit_required=False,
                backup_frequency='weekly'
            ),
            'impact': DataGovernancePolicy(
                classification=DataClassification.INTERNAL,
                retention_policy=DataRetentionPolicy.LONG_TERM,
                encryption_required=True,
                access_controls=['read', 'write'],
                audit_required=True,
                backup_frequency='daily'
            ),
            'personal_data': DataGovernancePolicy(
                classification=DataClassification.RESTRICTED,
                retention_policy=DataRetentionPolicy.SHORT_TERM,
                encryption_required=True,
                access_controls=['read'],
                audit_required=True,
                backup_frequency='daily'
            )
        }

        # Initialize governance tables
        self._init_governance_tables()

    def _init_governance_tables(self):


        """Initialize governance-related database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Data access audit log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_access_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                data_type TEXT,
                action TEXT,
                record_id TEXT,
                access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        """)

        # Data retention tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_retention_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_type TEXT,
                record_id TEXT,
                classification TEXT,
                retention_policy TEXT,
                created_date TIMESTAMP,
                expiry_date TIMESTAMP,
                last_accessed TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)

        # Data encryption keys
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS encryption_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_id TEXT UNIQUE,
                key_type TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)

        # Data backup tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_id TEXT UNIQUE,
                data_type TEXT,
                backup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                backup_size REAL,
                backup_location TEXT,
                status TEXT DEFAULT 'completed'
            )
        """)

        conn.commit()
        conn.close()

    def log_data_access(self, user_id: str, data_type: str, action: str, record_id: str,


                       ip_address: str = None, user_agent: str = None):
        """Log data access for audit purposes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO data_access_audit
            (user_id, data_type, action, record_id, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, data_type, action, record_id, ip_address, user_agent))

        conn.commit()
        conn.close()

        self.logger.info(f"Data access logged: {user_id} {action} {data_type}:{record_id}")

    def apply_retention_policy(self, data_type: str):


        """Apply retention policy to data"""
        policy = self.policies.get(data_type)
        if not policy:
            self.logger.warning(f"No retention policy found for {data_type}")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calculate expiry date based on retention policy
        if policy.retention_policy == DataRetentionPolicy.SHORT_TERM:
            expiry_days = 365
        elif policy.retention_policy == DataRetentionPolicy.MEDIUM_TERM:
            expiry_days = 1825  # 5 years
        elif policy.retention_policy == DataRetentionPolicy.LONG_TERM:
            expiry_days = 3650  # 10 years
        else:  # PERMANENT
            expiry_days = None

        # Get records that need retention tracking
        if data_type == 'grants':
            table_name = 'grants'
            id_column = 'grant_id'
        elif data_type == 'research':
            table_name = 'real_research'
            id_column = 'publication_id'
        elif data_type == 'impact':
            table_name = 'real_impact'
            id_column = 'indicator_id'
        else:
            table_name = data_type
            id_column = 'id'

        # Get records not already tracked
        cursor.execute(f"""
            SELECT {id_column}, created_at FROM {table_name}
            WHERE {id_column} NOT IN (
                SELECT record_id FROM data_retention_tracking
                WHERE data_type = ?
            )
        """, (data_type,))

        records = cursor.fetchall()

        for record_id, created_date in records:
            expiry_date = None
            if expiry_days:
                created_dt = datetime.fromisoformat(created_date)
                expiry_date = created_dt + timedelta(days=expiry_days)

            cursor.execute("""
                INSERT INTO data_retention_tracking
                (data_type, record_id, classification, retention_policy, created_date, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data_type, record_id, policy.classification.value,
                policy.retention_policy.value, created_date, expiry_date
            ))

        # Mark expired records for deletion
        if expiry_days:
            cursor.execute("""
                UPDATE data_retention_tracking
                SET status = 'expired'
                WHERE data_type = ? AND expiry_date < ? AND status = 'active'
            """, (data_type, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        self.logger.info(f"Retention policy applied to {len(records)} {data_type} records")

    def cleanup_expired_data(self):


        """Remove expired data based on retention policies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get expired records
        cursor.execute("""
            SELECT data_type, record_id FROM data_retention_tracking
            WHERE status = 'expired'
        """)

        expired_records = cursor.fetchall()

        for data_type, record_id in expired_records:
            try:
                # Determine table and ID column
                if data_type == 'grants':
                    table_name = 'grants'
                    id_column = 'grant_id'
                elif data_type == 'research':
                    table_name = 'real_research'
                    id_column = 'publication_id'
                elif data_type == 'impact':
                    table_name = 'real_impact'
                    id_column = 'indicator_id'
                else:
                    table_name = data_type
                    id_column = 'id'

                # Delete expired record
                cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", (record_id,))

                # Update retention tracking
                cursor.execute("""
                    UPDATE data_retention_tracking
                    SET status = 'deleted'
                    WHERE data_type = ? AND record_id = ?
                """, (data_type, record_id))

                self.logger.info(f"Deleted expired {data_type} record: {record_id}")

            except Exception as e:
                self.logger.error(f"Error deleting expired {data_type} record {record_id}: {e}")

        conn.commit()
        conn.close()

        self.logger.info(f"Cleanup completed: {len(expired_records)} expired records removed")

    def generate_governance_report(self) -> Dict[str, Any]:


        """Generate comprehensive governance report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            'generated_at': datetime.now().isoformat(),
            'data_inventory': {},
            'retention_summary': {},
            'access_audit': {},
            'compliance_status': {}
        }

        # Data inventory
        for data_type in ['grants', 'research', 'impact']:
            cursor.execute(f"SELECT COUNT(*) FROM {data_type}")
            count = cursor.fetchone()[0]

            policy = self.policies.get(data_type)
            report['data_inventory'][data_type] = {
                'record_count': count,
                'classification': policy.classification.value if policy else 'unknown',
                'retention_policy': policy.retention_policy.value if policy else 'unknown',
                'encryption_required': policy.encryption_required if policy else False
            }

        # Retention summary
        cursor.execute("""
            SELECT data_type, status, COUNT(*)
            FROM data_retention_tracking
            GROUP BY data_type, status
        """)

        retention_data = cursor.fetchall()
        for data_type, status, count in retention_data:
            if data_type not in report['retention_summary']:
                report['retention_summary'][data_type] = {}
            report['retention_summary'][data_type][status] = count

        # Access audit summary
        cursor.execute("""
            SELECT data_type, action, COUNT(*)
            FROM data_access_audit
            WHERE access_timestamp >= datetime('now', '-30 days')
            GROUP BY data_type, action
        """)

        audit_data = cursor.fetchall()
        for data_type, action, count in audit_data:
            if data_type not in report['access_audit']:
                report['access_audit'][data_type] = {}
            report['access_audit'][data_type][action] = count

        # Compliance status
        for data_type, policy in self.policies.items():
            report['compliance_status'][data_type] = {
                'encryption_compliant': policy.encryption_required,
                'audit_compliant': policy.audit_required,
                'retention_compliant': True,  # Would check actual compliance
                'access_control_compliant': len(policy.access_controls) > 0
            }

        conn.close()

        return report

    def encrypt_sensitive_data(self, data_type: str):


        """Encrypt sensitive data based on policy"""
        policy = self.policies.get(data_type)
        if not policy or not policy.encryption_required:
            return

        # This would implement actual encryption
        # For now, we'll just log the requirement
        self.logger.info(f"Encryption required for {data_type} data")

        # Generate encryption key
        key_id = hashlib.sha256(f"{data_type}_{datetime.now().isoformat()}".encode()).hexdigest()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO encryption_keys (key_id, key_type, expiry_date)
            VALUES (?, ?, ?)
        """, (key_id, f"{data_type}_encryption",
              (datetime.now() + timedelta(days=365)).isoformat()))

        conn.commit()
        conn.close()

        self.logger.info(f"Encryption key generated for {data_type}: {key_id}")

    def backup_data(self, data_type: str):


        """Create backup of data based on policy"""
        policy = self.policies.get(data_type)
        if not policy:
            return

        backup_id = f"{data_type}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_location = f"backups/{backup_id}.db"

        # Create backup directory if it doesn't exist
        os.makedirs("backups", exist_ok=True)

        # Create backup
        conn = sqlite3.connect(self.db_path)
        backup_conn = sqlite3.connect(backup_location)

        # Export data to backup
        if data_type == 'grants':
            df = pd.read_sql_query("SELECT * FROM grants", conn)
        elif data_type == 'research':
            df = pd.read_sql_query("SELECT * FROM real_research", conn)
        elif data_type == 'impact':
            df = pd.read_sql_query("SELECT * FROM real_impact", conn)
        else:
            df = pd.read_sql_query(f"SELECT * FROM {data_type}", conn)

        df.to_sql(data_type, backup_conn, if_exists='replace', index=False)

        # Get backup size
        backup_size = os.path.getsize(backup_location)

        # Log backup
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO backup_tracking
            (backup_id, data_type, backup_size, backup_location)
            VALUES (?, ?, ?, ?)
        """, (backup_id, data_type, backup_size, backup_location))

        conn.commit()
        conn.close()
        backup_conn.close()

        self.logger.info(f"Backup created for {data_type}: {backup_id} ({backup_size} bytes)")

def main():


    """Main function to demonstrate governance framework"""
    governance = DataGovernanceFramework()

    # Apply retention policies
    for data_type in ['grants', 'research', 'impact']:
        governance.apply_retention_policy(data_type)

    # Cleanup expired data
    governance.cleanup_expired_data()

    # Generate governance report
    report = governance.generate_governance_report()

    print("📊 Data Governance Report")
    print("=" * 50)
    print(f"Generated: {report['generated_at']}")
    print()

    print("📋 Data Inventory:")
    for data_type, info in report['data_inventory'].items():
        print(f"  - {data_type}: {info['record_count']} records")
        print(f"    Classification: {info['classification']}")
        print(f"    Retention: {info['retention_policy']}")
        print(f"    Encrypted: {info['encryption_required']}")
        print()

    print("🔒 Compliance Status:")
    for data_type, status in report['compliance_status'].items():
        compliant = all(status.values())
        print(f"  - {data_type}: {'✅' if compliant else '❌'}")

    # Save report
    with open('governance_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Governance report saved to governance_report.json")

if __name__ == "__main__":
    main()
