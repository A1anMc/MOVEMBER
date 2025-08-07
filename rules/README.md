# Rules System

A brilliant, flexible, and extensible rules engine for your system.

## Overview

The rules system provides a powerful way to define, manage, and execute business logic, validation rules, and automated workflows. It's designed to be:

- **Declarative**: Rules are defined in a clear, readable format
- **Composable**: Rules can be combined and nested
- **Extensible**: Easy to add new rule types and conditions
- **Performant**: Optimized for fast rule evaluation
- **Testable**: Comprehensive testing framework included

## Architecture

```
rules/
├── core/           # Core rule engine
├── types/          # Rule type definitions
├── conditions/     # Condition evaluators
├── actions/        # Action executors
├── validators/     # Rule validation
└── examples/       # Example rules and usage
```

## Key Features

- **Rule Chaining**: Rules can trigger other rules
- **Conditional Logic**: Complex if/then/else scenarios
- **Data Validation**: Input/output validation
- **Event-Driven**: Rules can respond to system events
- **Audit Trail**: Complete logging of rule executions
- **Performance Monitoring**: Built-in metrics and profiling

## Quick Start

```python
from rules.core import RuleEngine
from rules.types import Rule, Condition, Action

# Define a simple rule
rule = Rule(
    name="user_validation",
    conditions=[
        Condition("user.age >= 18"),
        Condition("user.email is not None")
    ],
    actions=[
        Action("approve_user"),
        Action("send_welcome_email")
    ]
)

# Create and run the engine
engine = RuleEngine()
engine.add_rule(rule)
result = engine.evaluate(user_data)
```

## Rule Types

1. **Validation Rules**: Data validation and integrity checks
2. **Business Rules**: Domain-specific logic and workflows
3. **Security Rules**: Access control and permission checks
4. **Transformation Rules**: Data transformation and mapping
5. **Notification Rules**: Event-driven notifications and alerts

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `python -m pytest tests/`
3. Start the rule engine: `python -m rules.core`

## Documentation

- [Rule Definition Guide](docs/rule-definition.md)
- [Condition Reference](docs/conditions.md)
- [Action Reference](docs/actions.md)
- [Performance Tuning](docs/performance.md)
- [API Reference](docs/api.md) 