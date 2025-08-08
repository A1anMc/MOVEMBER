"""
User Validation Rules

Example rules for user registration and validation.
"""

from rules.types import Rule, Condition, Action, RulePriority, ContextType


def create_user_validation_rules():
    """Create a set of user validation rules."""

    # Rule 1: Basic user data validation
    basic_validation_rule = Rule(
        name="basic_user_validation",
        description="Validate basic user registration data",
        priority=RulePriority.HIGH,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("len(data.get('email', '')) > 0", description="Email is required"),
            Condition("len(data.get('password', '')) >= 8", description="Password must be at least 8 characters"),
            Condition("'@' in data.get('email', '')", description="Email must contain @ symbol"),
            Condition("data.get('age', 0) >= 13", description="User must be at least 13 years old")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Basic user validation passed',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'validation_status': 'basic_passed'}
            })
        ],
        tags=['validation', 'user', 'registration']
    )

    # Rule 2: Email format validation
    email_validation_rule = Rule(
        name="email_format_validation",
        description="Validate email format using regex",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$', data.get('email', ''))",
                     description="Email must match standard format")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Email format validation passed',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'email_valid': True}
            })
        ],
        tags=['validation', 'email']
    )

    # Rule 3: Password strength validation
    password_strength_rule = Rule(
        name="password_strength_validation",
        description="Validate password strength requirements",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("any(c.isupper() for c in data.get('password', ''))", description="Password must contain uppercase letter"),
            Condition("any(c.islower() for c in data.get('password', ''))", description="Password must contain lowercase letter"),
            Condition("any(c.isdigit() for c in data.get('password', ''))", description="Password must contain digit"),
            Condition("any(c in '!@#$%^&*()' for c in data.get('password', ''))", description="Password must contain special character")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Password strength validation passed',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'password_strength': 'strong'}
            })
        ],
        tags=['validation', 'password', 'security']
    )

    # Rule 4: Age-based restrictions
    age_restriction_rule = Rule(
        name="age_restriction_validation",
        description="Apply age-based restrictions and requirements",
        priority=RulePriority.LOW,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("data.get('age', 0) >= 18", description="User is 18 or older")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Adult user registration',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'user_type': 'adult', 'requires_parental_consent': False}
            })
        ],
        tags=['validation', 'age', 'restrictions']
    )

    # Rule 5: Duplicate email check (simulated)
    duplicate_email_rule = Rule(
        name="duplicate_email_check",
        description="Check for duplicate email addresses",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("data.get('email') not in ['existing@example.com', 'admin@example.com']",
                     description="Email is not already registered")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Email is available for registration',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'email_available': True}
            })
        ],
        tags=['validation', 'email', 'duplicate']
    )

    # Rule 6: Welcome email for successful registration
    welcome_email_rule = Rule(
        name="welcome_email_rule",
        description="Send welcome email for successful registration",
        priority=RulePriority.LOW,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("data.get('validation_status') == 'basic_passed'", description="Basic validation passed"),
            Condition("data.get('email_valid') == True", description="Email is valid"),
            Condition("data.get('password_strength') == 'strong'", description="Password is strong"),
            Condition("data.get('email_available') == True", description="Email is available")
        ],
        actions=[
            Action("send_email", parameters={
                'to_email': 'data.get("email")',
                'subject': 'Welcome to Our Platform!',
                'body': 'Thank you for registering with us. Your account has been successfully created.'
            }),
            Action("log_message", parameters={
                'message': 'Welcome email sent to new user',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'registration_complete': True, 'welcome_email_sent': True}
            })
        ],
        tags=['email', 'welcome', 'registration']
    )

    # Rule 7: Failed validation handling
    failed_validation_rule = Rule(
        name="failed_validation_handling",
        description="Handle failed validation scenarios",
        priority=RulePriority.HIGH,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("data.get('validation_status') != 'basic_passed' or data.get('email_valid') != True",
                     description="Validation failed")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'User registration validation failed',
                'level': 'WARNING'
            }),
            Action("update_data", parameters={
                'updates': {'registration_status': 'failed', 'error_message': 'Validation failed'}
            }),
            Action("raise_alert", parameters={
                'type': 'validation_failure',
                'message': 'User registration validation failed',
                'severity': 'medium'
            })
        ],
        tags=['error', 'validation', 'handling']
    )

    return [
        basic_validation_rule,
        email_validation_rule,
        password_strength_rule,
        age_restriction_rule,
        duplicate_email_rule,
        welcome_email_rule,
        failed_validation_rule
    ]


def create_login_rules():
    """Create rules for user login validation."""

    # Rule 1: Login attempt validation
    login_validation_rule = Rule(
        name="login_validation",
        description="Validate login attempt",
        priority=RulePriority.HIGH,
        context_types=[ContextType.USER_LOGIN],
        conditions=[
            Condition("len(data.get('email', '')) > 0", description="Email is required"),
            Condition("len(data.get('password', '')) > 0", description="Password is required"),
            Condition("data.get('email') in ['user@example.com', 'admin@example.com']",
                     description="User exists in system")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Login validation passed',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'login_valid': True, 'user_authenticated': True}
            })
        ],
        tags=['login', 'authentication']
    )

    # Rule 2: Failed login handling
    failed_login_rule = Rule(
        name="failed_login_handling",
        description="Handle failed login attempts",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.USER_LOGIN],
        conditions=[
            Condition("data.get('email') not in ['user@example.com', 'admin@example.com'] or data.get('password') != 'correct_password'",
                     description="Invalid credentials")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Failed login attempt',
                'level': 'WARNING'
            }),
            Action("update_data", parameters={
                'updates': {'login_failed': True, 'error_message': 'Invalid credentials'}
            }),
            Action("raise_alert", parameters={
                'type': 'security',
                'message': 'Failed login attempt detected',
                'severity': 'low'
            })
        ],
        tags=['login', 'security', 'error']
    )

    return [login_validation_rule, failed_login_rule]


def create_security_rules():
    """Create security-related rules."""

    # Rule 1: Rate limiting for login attempts
    rate_limit_rule = Rule(
        name="login_rate_limiting",
        description="Implement rate limiting for login attempts",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.USER_LOGIN],
        conditions=[
            Condition("data.get('login_attempts', 0) < 5", description="Login attempts under limit")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Login attempt within rate limit',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'rate_limit_exceeded': False}
            })
        ],
        tags=['security', 'rate_limiting', 'login']
    )

    # Rule 2: Suspicious activity detection
    suspicious_activity_rule = Rule(
        name="suspicious_activity_detection",
        description="Detect suspicious login activity",
        priority=RulePriority.HIGH,
        context_types=[ContextType.USER_LOGIN],
        conditions=[
            Condition("data.get('login_attempts', 0) >= 3", description="Multiple login attempts"),
            Condition("data.get('ip_address') not in ['192.168.1.1', '10.0.0.1']", description="Unusual IP address")
        ],
        actions=[
            Action("raise_alert", parameters={
                'type': 'security',
                'message': 'Suspicious login activity detected',
                'severity': 'high'
            }),
            Action("send_email", parameters={
                'to_email': 'admin@example.com',
                'subject': 'Security Alert - Suspicious Activity',
                'body': 'Multiple login attempts detected from unusual IP address.'
            }),
            Action("update_data", parameters={
                'updates': {'suspicious_activity': True, 'account_locked': True}
            })
        ],
        tags=['security', 'monitoring', 'alert']
    )

    return [rate_limit_rule, suspicious_activity_rule]
