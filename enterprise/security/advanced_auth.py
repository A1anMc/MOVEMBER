#!/usr/bin/env python3
"""
Advanced Authentication & Authorization System
Enterprise-grade security for the Movember AI Rules System.
"""

import asyncio
import logging
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import jwt
from passlib.context import CryptContext
import bcrypt

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles with different permission levels."""
    VIEWER = "viewer"
    ANALYST = "analyst"
    MANAGER = "manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class Permission(Enum):
    """System permissions."""
    # Data permissions
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    DELETE_DATA = "delete_data"
    EXPORT_DATA = "export_data"
    
    # Analytics permissions
    VIEW_ANALYTICS = "view_analytics"
    RUN_PREDICTIONS = "run_predictions"
    ACCESS_ML_MODELS = "access_ml_models"
    
    # System permissions
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    SYSTEM_CONFIG = "system_config"
    VIEW_LOGS = "view_logs"
    
    # Grant permissions
    VIEW_GRANTS = "view_grants"
    CREATE_GRANTS = "create_grants"
    APPROVE_GRANTS = "approve_grants"
    MANAGE_GRANTS = "manage_grants"
    
    # Impact permissions
    VIEW_IMPACT = "view_impact"
    CREATE_IMPACT_REPORTS = "create_impact_reports"
    APPROVE_IMPACT_REPORTS = "approve_impact_reports"
    
    # Health data permissions
    VIEW_HEALTH_DATA = "view_health_data"
    ACCESS_SENSITIVE_DATA = "access_sensitive_data"
    EXPORT_HEALTH_DATA = "export_health_data"

@dataclass
class User:
    """User entity with authentication and authorization data."""
    user_id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    permissions: List[Permission]
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = None
    last_login: datetime = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_hash: str = ""
    two_factor_enabled: bool = False
    two_factor_secret: str = ""
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Session:
    """User session data."""
    session_id: str
    user_id: str
    token: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    last_activity: datetime = None
    
    def __post_init__(self):
        if self.last_activity is None:
            self.last_activity = datetime.now()

@dataclass
class AuditLog:
    """Security audit log entry."""
    log_id: str
    user_id: str
    action: str
    resource: str
    timestamp: datetime
    ip_address: str
    user_agent: str
    success: bool
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}

class AdvancedAuthSystem:
    """Advanced authentication and authorization system."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = self._generate_secret_key()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 30
        
        # In-memory storage (would be replaced with database in production)
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.audit_logs: List[AuditLog] = []
        
        # Role-based permissions mapping
        self.role_permissions = {
            UserRole.VIEWER: [
                Permission.READ_DATA,
                Permission.VIEW_ANALYTICS,
                Permission.VIEW_GRANTS,
                Permission.VIEW_IMPACT,
                Permission.VIEW_HEALTH_DATA
            ],
            UserRole.ANALYST: [
                Permission.READ_DATA,
                Permission.WRITE_DATA,
                Permission.EXPORT_DATA,
                Permission.VIEW_ANALYTICS,
                Permission.RUN_PREDICTIONS,
                Permission.ACCESS_ML_MODELS,
                Permission.VIEW_GRANTS,
                Permission.CREATE_GRANTS,
                Permission.VIEW_IMPACT,
                Permission.CREATE_IMPACT_REPORTS,
                Permission.VIEW_HEALTH_DATA
            ],
            UserRole.MANAGER: [
                Permission.READ_DATA,
                Permission.WRITE_DATA,
                Permission.DELETE_DATA,
                Permission.EXPORT_DATA,
                Permission.VIEW_ANALYTICS,
                Permission.RUN_PREDICTIONS,
                Permission.ACCESS_ML_MODELS,
                Permission.MANAGE_USERS,
                Permission.VIEW_LOGS,
                Permission.VIEW_GRANTS,
                Permission.CREATE_GRANTS,
                Permission.APPROVE_GRANTS,
                Permission.VIEW_IMPACT,
                Permission.CREATE_IMPACT_REPORTS,
                Permission.APPROVE_IMPACT_REPORTS,
                Permission.VIEW_HEALTH_DATA,
                Permission.ACCESS_SENSITIVE_DATA
            ],
            UserRole.ADMIN: [
                Permission.READ_DATA,
                Permission.WRITE_DATA,
                Permission.DELETE_DATA,
                Permission.EXPORT_DATA,
                Permission.VIEW_ANALYTICS,
                Permission.RUN_PREDICTIONS,
                Permission.ACCESS_ML_MODELS,
                Permission.MANAGE_USERS,
                Permission.MANAGE_ROLES,
                Permission.SYSTEM_CONFIG,
                Permission.VIEW_LOGS,
                Permission.VIEW_GRANTS,
                Permission.CREATE_GRANTS,
                Permission.APPROVE_GRANTS,
                Permission.MANAGE_GRANTS,
                Permission.VIEW_IMPACT,
                Permission.CREATE_IMPACT_REPORTS,
                Permission.APPROVE_IMPACT_REPORTS,
                Permission.VIEW_HEALTH_DATA,
                Permission.ACCESS_SENSITIVE_DATA,
                Permission.EXPORT_HEALTH_DATA
            ],
            UserRole.SUPER_ADMIN: [
                Permission.READ_DATA,
                Permission.WRITE_DATA,
                Permission.DELETE_DATA,
                Permission.EXPORT_DATA,
                Permission.VIEW_ANALYTICS,
                Permission.RUN_PREDICTIONS,
                Permission.ACCESS_ML_MODELS,
                Permission.MANAGE_USERS,
                Permission.MANAGE_ROLES,
                Permission.SYSTEM_CONFIG,
                Permission.VIEW_LOGS,
                Permission.VIEW_GRANTS,
                Permission.CREATE_GRANTS,
                Permission.APPROVE_GRANTS,
                Permission.MANAGE_GRANTS,
                Permission.VIEW_IMPACT,
                Permission.CREATE_IMPACT_REPORTS,
                Permission.APPROVE_IMPACT_REPORTS,
                Permission.VIEW_HEALTH_DATA,
                Permission.ACCESS_SENSITIVE_DATA,
                Permission.EXPORT_HEALTH_DATA
            ]
        }
        
        # Initialize default admin user
        self._create_default_admin()
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key."""
        return secrets.token_urlsafe(32)
    
    def _create_default_admin(self):
        """Create default super admin user."""
        admin_user = User(
            user_id="admin_001",
            username="admin",
            email="admin@movember.com",
            full_name="System Administrator",
            role=UserRole.SUPER_ADMIN,
            permissions=self.role_permissions[UserRole.SUPER_ADMIN],
            is_verified=True
        )
        admin_user.password_hash = self.pwd_context.hash("Movember2025!")
        self.users[admin_user.user_id] = admin_user
        logger.info("Default admin user created")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            return None
    
    async def authenticate_user(self, username: str, password: str, ip_address: str, user_agent: str) -> Optional[User]:
        """Authenticate user with username and password."""
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            self._log_audit_event("login_failed", "user", ip_address, user_agent, False, {"username": username, "reason": "user_not_found"})
            return None
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.now():
            self._log_audit_event("login_failed", "user", ip_address, user_agent, False, {"username": username, "reason": "account_locked"})
            return None
        
        # Check if account is active
        if not user.is_active:
            self._log_audit_event("login_failed", "user", ip_address, user_agent, False, {"username": username, "reason": "account_inactive"})
            return None
        
        # Verify password
        if not self.verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            
            # Lock account if too many failed attempts
            if user.failed_login_attempts >= self.max_failed_attempts:
                user.locked_until = datetime.now() + timedelta(minutes=self.lockout_duration_minutes)
                logger.warning(f"Account locked for user {username}")
            
            self._log_audit_event("login_failed", "user", ip_address, user_agent, False, {"username": username, "reason": "invalid_password"})
            return None
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now()
        
        self._log_audit_event("login_success", "user", ip_address, user_agent, True, {"username": username})
        return user
    
    async def create_session(self, user: User, ip_address: str, user_agent: str) -> Session:
        """Create a new user session."""
        session_id = secrets.token_urlsafe(32)
        access_token = self.create_access_token({"sub": user.user_id, "role": user.role.value})
        refresh_token = self.create_refresh_token({"sub": user.user_id})
        
        session = Session(
            session_id=session_id,
            user_id=user.user_id,
            token=access_token,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=self.access_token_expire_minutes),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        logger.info(f"Session created for user {user.username}")
        return session
    
    async def validate_session(self, session_id: str, ip_address: str) -> Optional[Session]:
        """Validate an existing session."""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session is active and not expired
        if not session.is_active or session.expires_at < datetime.now():
            return None
        
        # Update last activity
        session.last_activity = datetime.now()
        
        # Optional: Check IP address for security
        if session.ip_address != ip_address:
            logger.warning(f"IP address mismatch for session {session_id}")
            # Could implement additional security measures here
        
        return session
    
    async def revoke_session(self, session_id: str) -> bool:
        """Revoke a user session."""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            logger.info(f"Session {session_id} revoked")
            return True
        return False
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        return permission in user.permissions
    
    def has_role(self, user: User, role: UserRole) -> bool:
        """Check if user has a specific role."""
        return user.role == role
    
    def has_role_or_higher(self, user: User, required_role: UserRole) -> bool:
        """Check if user has required role or higher."""
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.ANALYST: 2,
            UserRole.MANAGER: 3,
            UserRole.ADMIN: 4,
            UserRole.SUPER_ADMIN: 5
        }
        
        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    async def create_user(self, username: str, email: str, full_name: str, role: UserRole, 
                         password: str, created_by: User) -> Optional[User]:
        """Create a new user (admin only)."""
        if not self.has_permission(created_by, Permission.MANAGE_USERS):
            self._log_audit_event("create_user_denied", "user", "", "", False, {"target_username": username})
            return None
        
        # Check if username already exists
        for user in self.users.values():
            if user.username == username:
                return None
        
        user_id = f"user_{secrets.token_urlsafe(8)}"
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            permissions=self.role_permissions[role]
        )
        user.password_hash = self.get_password_hash(password)
        
        self.users[user_id] = user
        
        self._log_audit_event("create_user", "user", "", "", True, {
            "created_by": created_by.username,
            "target_username": username,
            "role": role.value
        })
        
        logger.info(f"User {username} created by {created_by.username}")
        return user
    
    async def update_user_role(self, target_user: User, new_role: UserRole, updated_by: User) -> bool:
        """Update user role (admin only)."""
        if not self.has_permission(updated_by, Permission.MANAGE_ROLES):
            self._log_audit_event("update_role_denied", "user", "", "", False, {
                "target_username": target_user.username,
                "new_role": new_role.value
            })
            return False
        
        old_role = target_user.role
        target_user.role = new_role
        target_user.permissions = self.role_permissions[new_role]
        
        self._log_audit_event("update_role", "user", "", "", True, {
            "updated_by": updated_by.username,
            "target_username": target_user.username,
            "old_role": old_role.value,
            "new_role": new_role.value
        })
        
        logger.info(f"User {target_user.username} role updated from {old_role.value} to {new_role.value}")
        return True
    
    async def deactivate_user(self, target_user: User, deactivated_by: User) -> bool:
        """Deactivate a user account (admin only)."""
        if not self.has_permission(deactivated_by, Permission.MANAGE_USERS):
            self._log_audit_event("deactivate_user_denied", "user", "", "", False, {
                "target_username": target_user.username
            })
            return False
        
        target_user.is_active = False
        
        # Revoke all active sessions
        for session in self.sessions.values():
            if session.user_id == target_user.user_id:
                session.is_active = False
        
        self._log_audit_event("deactivate_user", "user", "", "", True, {
            "deactivated_by": deactivated_by.username,
            "target_username": target_user.username
        })
        
        logger.info(f"User {target_user.username} deactivated by {deactivated_by.username}")
        return True
    
    def _log_audit_event(self, action: str, resource: str, ip_address: str, user_agent: str, 
                        success: bool, details: Dict[str, Any] = None):
        """Log security audit event."""
        if details is None:
            details = {}
        
        log_entry = AuditLog(
            log_id=f"log_{secrets.token_urlsafe(8)}",
            user_id="system",  # Would be actual user ID in real implementation
            action=action,
            resource=resource,
            timestamp=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            details=details
        )
        
        self.audit_logs.append(log_entry)
        
        # Keep only last 1000 audit logs
        if len(self.audit_logs) > 1000:
            self.audit_logs = self.audit_logs[-1000:]
    
    async def get_audit_logs(self, user: User, limit: int = 100) -> List[AuditLog]:
        """Get audit logs (admin only)."""
        if not self.has_permission(user, Permission.VIEW_LOGS):
            return []
        
        return self.audit_logs[-limit:]
    
    async def get_user_sessions(self, user: User) -> List[Session]:
        """Get all active sessions for a user."""
        return [session for session in self.sessions.values() 
                if session.user_id == user.user_id and session.is_active]
    
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.expires_at < current_time:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

# Global instance
auth_system = AdvancedAuthSystem()

# Convenience functions
async def authenticate_user(username: str, password: str, ip_address: str, user_agent: str) -> Optional[User]:
    """Authenticate user with username and password."""
    return await auth_system.authenticate_user(username, password, ip_address, user_agent)

async def create_session(user: User, ip_address: str, user_agent: str) -> Session:
    """Create a new user session."""
    return await auth_system.create_session(user, ip_address, user_agent)

def has_permission(user: User, permission: Permission) -> bool:
    """Check if user has a specific permission."""
    return auth_system.has_permission(user, permission)

def has_role_or_higher(user: User, required_role: UserRole) -> bool:
    """Check if user has required role or higher."""
    return auth_system.has_role_or_higher(user, required_role)

if __name__ == "__main__":
    # Test the authentication system
    async def test_auth():
        print("Testing Advanced Authentication System...")
        
        # Test user creation
        admin_user = auth_system.users["admin_001"]
        test_user = await auth_system.create_user(
            "testuser", "test@movember.com", "Test User", 
            UserRole.ANALYST, "password123", admin_user
        )
        
        if test_user:
            print(f"Created test user: {test_user.username}")
            
            # Test authentication
            authenticated_user = await auth_system.authenticate_user(
                "testuser", "password123", "127.0.0.1", "test-agent"
            )
            
            if authenticated_user:
                print(f"Authentication successful for: {authenticated_user.username}")
                
                # Test session creation
                session = await auth_system.create_session(
                    authenticated_user, "127.0.0.1", "test-agent"
                )
                print(f"Session created: {session.session_id}")
                
                # Test permissions
                can_view_data = auth_system.has_permission(authenticated_user, Permission.READ_DATA)
                print(f"Can view data: {can_view_data}")
                
                # Test role hierarchy
                is_manager_or_higher = auth_system.has_role_or_higher(authenticated_user, UserRole.MANAGER)
                print(f"Is manager or higher: {is_manager_or_higher}")
        
        print("Advanced Authentication System test completed!")
    
    asyncio.run(test_auth())
