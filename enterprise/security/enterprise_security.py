#!/usr/bin/env python3
"""
Enterprise Security Module
Core security features for the Movember AI Rules System.
"""

import asyncio
import logging
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityEvent:
    """Security event log entry."""
    event_id: str
    timestamp: datetime
    event_type: str
    severity: SecurityLevel
    user_id: str
    ip_address: str
    details: Dict[str, Any]
    resolved: bool = False

class EnterpriseSecurity:
    """Enterprise security system."""
    
    def __init__(self):
        self.security_events: List[SecurityEvent] = []
        self.blocked_ips: List[str] = []
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.max_requests_per_minute = 100
        self.max_failed_logins = 5
        self.session_timeout_minutes = 30
    
    def log_security_event(self, event_type: str, severity: SecurityLevel, 
                          user_id: str, ip_address: str, details: Dict[str, Any] = None):
        """Log a security event."""
        if details is None:
            details = {}
        
        event = SecurityEvent(
            event_id=f"sec_{secrets.token_urlsafe(8)}",
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            ip_address=ip_address,
            details=details
        )
        
        self.security_events.append(event)
        
        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]
        
        logger.warning(f"Security event: {event_type} - {severity.value} - {user_id} - {ip_address}")
    
    def check_rate_limit(self, ip_address: str) -> bool:
        """Check if IP address is within rate limits."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        if ip_address not in self.rate_limits:
            self.rate_limits[ip_address] = []
        
        # Remove old requests
        self.rate_limits[ip_address] = [
            req_time for req_time in self.rate_limits[ip_address] 
            if req_time > minute_ago
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[ip_address]) >= self.max_requests_per_minute:
            self.log_security_event(
                "rate_limit_exceeded",
                SecurityLevel.MEDIUM,
                "unknown",
                ip_address,
                {"requests": len(self.rate_limits[ip_address])}
            )
            return False
        
        # Add current request
        self.rate_limits[ip_address].append(now)
        return True
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is blocked."""
        return ip_address in self.blocked_ips
    
    def block_ip(self, ip_address: str, reason: str = "security_violation"):
        """Block an IP address."""
        if ip_address not in self.blocked_ips:
            self.blocked_ips.append(ip_address)
            self.log_security_event(
                "ip_blocked",
                SecurityLevel.HIGH,
                "system",
                ip_address,
                {"reason": reason}
            )
            logger.warning(f"IP address blocked: {ip_address} - {reason}")
    
    def unblock_ip(self, ip_address: str):
        """Unblock an IP address."""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            self.log_security_event(
                "ip_unblocked",
                SecurityLevel.LOW,
                "system",
                ip_address,
                {"action": "manual_unblock"}
            )
            logger.info(f"IP address unblocked: {ip_address}")
    
    def get_security_events(self, severity: Optional[SecurityLevel] = None, 
                          limit: int = 100) -> List[SecurityEvent]:
        """Get security events."""
        events = self.security_events
        
        if severity:
            events = [e for e in events if e.severity == severity]
        
        return events[-limit:]
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security summary."""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        
        recent_events = [e for e in self.security_events if e.timestamp > last_24h]
        
        return {
            "total_events": len(self.security_events),
            "events_last_24h": len(recent_events),
            "blocked_ips": len(self.blocked_ips),
            "rate_limited_ips": len([ip for ip, times in self.rate_limits.items() 
                                   if len([t for t in times if t > last_24h]) > 0]),
            "events_by_severity": {
                level.value: len([e for e in recent_events if e.severity == level])
                for level in SecurityLevel
            },
            "unresolved_events": len([e for e in self.security_events if not e.resolve])
        }

# Global instance
security_system = EnterpriseSecurity()

# Convenience functions
def log_security_event(event_type: str, severity: SecurityLevel, user_id: str, 
                      ip_address: str, details: Dict[str, Any] = None):
    """Log a security event."""
    security_system.log_security_event(event_type, severity, user_id, ip_address, details)

def check_rate_limit(ip_address: str) -> bool:
    """Check if IP address is within rate limits."""
    return security_system.check_rate_limit(ip_address)

def is_ip_blocked(ip_address: str) -> bool:
    """Check if IP address is blocked."""
    return security_system.is_ip_blocked(ip_address)

def get_security_summary() -> Dict[str, Any]:
    """Get security summary."""
    return security_system.get_security_summary()
