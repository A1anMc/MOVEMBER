# 🚀 Brilliant Rules System

A powerful, flexible, and extensible rules engine designed for complex business logic, validation, and automated workflows.

## ✨ Features

- **Declarative Rule Definition**: Define rules in a clear, readable format
- **Complex Condition Evaluation**: Support for sophisticated boolean logic and expressions
- **Action Execution**: Built-in actions plus custom action support
- **Rule Chaining**: Rules can trigger other rules and workflows
- **Performance Monitoring**: Comprehensive metrics and performance tracking
- **Audit Trail**: Complete logging of all rule executions
- **Async Support**: Full async/await support for high-performance applications
- **Extensible**: Easy to add new rule types, conditions, and actions
- **Thread-Safe**: Designed for concurrent execution
- **Error Handling**: Robust error handling with retry logic

## 🏗️ Architecture

```
rules/
├── core/           # Core rule engine components
│   ├── engine.py   # Main rule engine orchestrator
│   ├── evaluator.py # Condition evaluation logic
│   ├── executor.py  # Action execution logic
│   └── metrics.py   # Performance metrics collection
├── types/          # Core data structures
│   └── __init__.py # Rule, Condition, Action definitions
├── examples/       # Example rules and usage
│   └── user_validation_rules.py
└── README.md       # This file
```

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rules-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the demo:
```bash
python demo.py
```

4. Run tests:
```bash
python test_rules_system.py
```

### Basic Usage

```python
from rules.core import RuleEngine
from rules.types import Rule, Condition, Action, RulePriority, ContextType, ExecutionContext

# Create a rule engine
engine = RuleEngine()

# Define a simple rule
rule = Rule(
    name="user_validation",
    description="Validate user registration data",
    priority=RulePriority.HIGH,
    context_types=[ContextType.USER_REGISTRATION],
    conditions=[
        Condition("len(data.get('email', '')) > 0", description="Email is required"),
        Condition("len(data.get('password', '')) >= 8", description="Password must be at least 8 characters")
    ],
    actions=[
        Action("log_message", parameters={
            'message': 'User validation passed',
            'level': 'INFO'
        }),
        Action("update_data", parameters={
            'updates': {'validation_status': 'passed'}
        })
    ]
)

# Add the rule to the engine
engine.add_rule(rule)

# Create execution context
context = ExecutionContext(
    context_type=ContextType.USER_REGISTRATION,
    context_id="user_123",
    data={
        'email': 'user@example.com',
        'password': 'securepassword123'
    }
)

# Evaluate rules
results = await engine.evaluate_async(context)

# Check results
for result in results:
    if result.success and result.conditions_met:
        print(f"✅ Rule '{result.rule_name}' executed successfully")
    else:
        print(f"❌ Rule '{result.rule_name}' failed: {result.error}")
```

## 📋 Rule Components

### Rule Definition

A rule consists of:
- **Name**: Unique identifier for the rule
- **Description**: Human-readable description
- **Priority**: Execution priority (CRITICAL, HIGH, MEDIUM, LOW, MINIMAL)
- **Context Types**: When this rule should be evaluated
- **Conditions**: Boolean expressions that must be true
- **Actions**: Operations to perform when conditions are met
- **Tags**: Optional categorization

### Conditions

Conditions are boolean expressions that can reference:
- Context data (`data.get('field')`)
- Built-in functions (`len()`, `str()`, `int()`, etc.)
- Comparison operators (`==`, `!=`, `<`, `>`, etc.)
- Logical operators (`and`, `or`, `not`)
- Custom evaluators

### Actions

Built-in actions include:
- `log_message`: Log messages with different levels
- `send_email`: Send email notifications
- `send_webhook`: Send HTTP requests
- `update_data`: Update context data
- `validate_data`: Validate data fields
- `notify_user`: Send user notifications
- `trigger_workflow`: Trigger external workflows
- `store_result`: Store results
- `raise_alert`: Raise alerts
- `approve_request`: Approve requests
- `reject_request`: Reject requests
- `schedule_task`: Schedule tasks
- `update_status`: Update status

## 🔧 Advanced Features

### Custom Actions

```python
def custom_action(action, context):
    """Custom action implementation."""
    return f"Custom action executed with data: {context.data}"

# Register custom action
engine.executor.register_custom_action('custom_action', custom_action)

# Use in rule
rule = Rule(
    name="custom_rule",
    conditions=[Condition("data.get('value') > 0")],
    actions=[Action("custom_action", parameters={})]
)
```

### Rule Chaining

Rules can modify data that affects subsequent rules:

```python
# Rule 1: Initial validation
rule1 = Rule(
    name="initial_validation",
    conditions=[Condition("data.get('input') is not None")],
    actions=[Action("update_data", parameters={
        'updates': {'validation_passed': True}
    })]
)

# Rule 2: Processing (depends on rule 1)
rule2 = Rule(
    name="processing",
    conditions=[Condition("data.get('validation_passed') == True")],
    actions=[Action("update_data", parameters={
        'updates': {'processing_complete': True}
    })]
)
```

### Metrics and Monitoring

```python
# Get system metrics
metrics = engine.get_metrics()
print(f"Total rules executed: {metrics['system']['total_rules_executed']}")

# Get performance summary
summary = engine.metrics.get_performance_summary()
print(f"Overall success rate: {summary['overall_success_rate']:.1%}")

# Get execution history
history = engine.get_execution_history(limit=10)
for entry in history:
    print(f"Execution at {entry['timestamp']}: {entry['total_rules']} rules")
```

### Async Support

```python
# Async rule evaluation
results = await engine.evaluate_async(context)

# Async custom actions
async def async_custom_action(action, context):
    await asyncio.sleep(0.1)  # Simulate async work
    return "Async action completed"

engine.executor.register_custom_action('async_action', async_custom_action)
```

## 📊 Performance Features

- **Concurrent Execution**: Rules execute in parallel when possible
- **Performance Monitoring**: Track execution times and success rates
- **Alerting**: Automatic alerts for slow rules or high error rates
- **Caching**: Built-in caching for frequently accessed data
- **Optimization**: Smart rule selection based on context and priority

## 🔒 Security Features

- **Expression Validation**: Safe expression evaluation with AST validation
- **Input Sanitization**: Automatic input validation and sanitization
- **Access Control**: Rule-based access control and permissions
- **Audit Logging**: Complete audit trail for compliance

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_rules_system.py
```

The test suite covers:
- Basic rule execution
- Condition evaluation
- Action execution
- Custom actions
- Multiple rule scenarios
- Error handling

## 📈 Monitoring and Observability

### Metrics Dashboard

The system provides comprehensive metrics:
- Rule execution counts and success rates
- Average execution times
- System uptime and performance
- Error rates and alerting
- Custom metrics and KPIs

### Audit Trail

Every rule execution is logged with:
- Timestamp and context information
- Rule name and parameters
- Execution time and results
- Error details if applicable
- Data changes and updates

## 🚀 Production Deployment

### Configuration

```python
from rules.core import RuleEngine, RuleEngineConfig

config = RuleEngineConfig(
    max_concurrent_rules=20,
    enable_metrics=True,
    enable_audit_trail=True,
    timeout_seconds=30,
    retry_attempts=3
)

engine = RuleEngine(config)
```

### Scaling

The rules system is designed to scale:
- **Horizontal Scaling**: Run multiple engine instances
- **Vertical Scaling**: Increase concurrent rule limits
- **Caching**: Add Redis or similar for caching
- **Persistence**: Add database storage for rules and results

### Integration

Easy integration with:
- **Web Frameworks**: FastAPI, Django, Flask
- **Message Queues**: Redis, RabbitMQ, Kafka
- **Databases**: PostgreSQL, MongoDB, Redis
- **Monitoring**: Prometheus, Grafana, ELK Stack

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

- [ ] Web-based rule editor
- [ ] Rule versioning and rollback
- [ ] Advanced rule templates
- [ ] Machine learning rule optimization
- [ ] Distributed rule execution
- [ ] Real-time rule updates
- [ ] Advanced analytics dashboard
- [ ] Integration with popular frameworks

## 🆘 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation
- Run the demo and test files
- Review the example rules

---

**Built with ❤️ for brilliant systems that scale.** 