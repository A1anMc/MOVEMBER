#!/usr/bin/env python3
"""
Rules System Demo

A comprehensive demonstration of the brilliant rules system.
"""

import asyncio
import time

from rules.core import RuleEngine, RuleEngineConfig
from rules.types import ExecutionContext, ContextType
from rules.examples.user_validation_rules import (
    create_user_validation_rules,
    create_login_rules,
    create_security_rules
)


def print_separator(title: str):
    """Print a formatted separator."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_rule_results(results):
    """Print rule execution results in a formatted way."""
    for result in results:
        status = "✅ PASSED" if result.success else "❌ FAILED"
        print(f"\n{status} - {result.rule_name}")
        print(f"  Execution Time: {result.execution_time:.3f}s")

        if result.conditions_met is not None:
            print(f"  Conditions Met: {'Yes' if result.conditions_met else 'No'}")

        if result.action_results:
            print("  Actions Executed:")
            for action_result in result.action_results:
                action_status = "✅" if action_result.success else "❌"
                print(f"    {action_status} {action_result.action_name}: {action_result.result}")

        if result.error:
            print(f"  Error: {result.error}")


async def demo_user_registration():
    """Demonstrate user registration rules."""
    print_separator("USER REGISTRATION DEMO")

    # Create rule engine
    engine = RuleEngine()

    # Add user validation rules
    user_rules = create_user_validation_rules()
    engine.add_rules(user_rules)

    print(f"Loaded {len(user_rules)} user validation rules")

    # Test case 1: Valid user registration
    print("\n🧪 Test Case 1: Valid User Registration")
    valid_user_data = {
        'email': 'john.doe@example.com',
        'password': 'StrongPass123!',
        'age': 25,
        'name': 'John Doe'
    }

    context = ExecutionContext(
        context_type=ContextType.USER_REGISTRATION,
        context_id=f"reg_{int(time.time())}",
        data=valid_user_data,
        user_id="user_123"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    # Test case 2: Invalid user registration (weak password)
    print("\n🧪 Test Case 2: Invalid User Registration (Weak Password)")
    invalid_user_data = {
        'email': 'jane@example.com',
        'password': 'weak',
        'age': 20,
        'name': 'Jane Smith'
    }

    context = ExecutionContext(
        context_type=ContextType.USER_REGISTRATION,
        context_id=f"reg_{int(time.time())}",
        data=invalid_user_data,
        user_id="user_124"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    # Test case 3: Underage user
    print("\n🧪 Test Case 3: Underage User Registration")
    underage_user_data = {
        'email': 'kid@example.com',
        'password': 'StrongPass123!',
        'age': 12,
        'name': 'Kid User'
    }

    context = ExecutionContext(
        context_type=ContextType.USER_REGISTRATION,
        context_id=f"reg_{int(time.time())}",
        data=underage_user_data,
        user_id="user_125"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    return engine


async def demo_login_validation():
    """Demonstrate login validation rules."""
    print_separator("LOGIN VALIDATION DEMO")

    # Create rule engine
    engine = RuleEngine()

    # Add login and security rules
    login_rules = create_login_rules()
    security_rules = create_security_rules()
    engine.add_rules(login_rules + security_rules)

    print(f"Loaded {len(login_rules)} login rules and {len(security_rules)} security rules")

    # Test case 1: Valid login
    print("\n🧪 Test Case 1: Valid Login")
    valid_login_data = {
        'email': 'user@example.com',
        'password': 'correct_password',
        'login_attempts': 1,
        'ip_address': '192.168.1.1'
    }

    context = ExecutionContext(
        context_type=ContextType.USER_LOGIN,
        context_id=f"login_{int(time.time())}",
        data=valid_login_data,
        user_id="user_123"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    # Test case 2: Failed login
    print("\n🧪 Test Case 2: Failed Login")
    failed_login_data = {
        'email': 'user@example.com',
        'password': 'wrong_password',
        'login_attempts': 1,
        'ip_address': '192.168.1.1'
    }

    context = ExecutionContext(
        context_type=ContextType.USER_LOGIN,
        context_id=f"login_{int(time.time())}",
        data=failed_login_data,
        user_id="user_123"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    # Test case 3: Suspicious activity
    print("\n🧪 Test Case 3: Suspicious Login Activity")
    suspicious_login_data = {
        'email': 'user@example.com',
        'password': 'wrong_password',
        'login_attempts': 5,
        'ip_address': '203.0.113.1'  # Unusual IP
    }

    context = ExecutionContext(
        context_type=ContextType.USER_LOGIN,
        context_id=f"login_{int(time.time())}",
        data=suspicious_login_data,
        user_id="user_123"
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    return engine


async def demo_metrics_and_monitoring():
    """Demonstrate metrics and monitoring capabilities."""
    print_separator("METRICS AND MONITORING DEMO")

    # Create rule engine with metrics enabled
    config = RuleEngineConfig(enable_metrics=True, enable_audit_trail=True)
    engine = RuleEngine(config)

    # Add some rules
    user_rules = create_user_validation_rules()
    engine.add_rules(user_rules)

    # Run multiple test scenarios
    test_scenarios = [
        {
            'name': 'Valid Registration',
            'data': {
                'email': 'test1@example.com',
                'password': 'StrongPass123!',
                'age': 25
            }
        },
        {
            'name': 'Invalid Registration',
            'data': {
                'email': 'test2@example.com',
                'password': 'weak',
                'age': 25
            }
        },
        {
            'name': 'Another Valid Registration',
            'data': {
                'email': 'test3@example.com',
                'password': 'AnotherStrong123!',
                'age': 30
            }
        }
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Running scenario {i}: {scenario['name']}")

        context = ExecutionContext(
            context_type=ContextType.USER_REGISTRATION,
            context_id=f"demo_{int(time.time())}_{i}",
            data=scenario['data']
        )

        results = await engine.evaluate_async(context)
        print(f"  Executed {len(results)} rules")

    # Show metrics
    print("\n📊 METRICS SUMMARY")
    metrics = engine.get_metrics()

    if metrics:
        system_metrics = metrics['system']
        print(f"Total Rules Executed: {system_metrics['total_rules_executed']}")
        print(f"Total Batch Executions: {system_metrics['total_batch_executions']}")
        print(f"Average Batch Time: {system_metrics['average_batch_time']:.3f}s")
        print(f"System Uptime: {system_metrics['uptime_seconds']:.1f}s")

        print("\n📈 RULE-SPECIFIC METRICS")
        for rule_name, rule_metrics in metrics['rules'].items():
            print(f"\n{rule_name}:")
            print(f"  Total Executions: {rule_metrics['total_executions']}")
            print(f"  Success Rate: {rule_metrics['success_rate']:.1%}")
            print(f"  Average Time: {rule_metrics['average_execution_time']:.3f}s")

    # Show execution history
    print("\n📋 RECENT EXECUTION HISTORY")
    history = engine.get_execution_history(limit=3)
    for entry in history:
        print(f"\nExecution at {entry['timestamp']}:")
        print(f"  Context: {entry['context_type']} (ID: {entry['context_id']})")
        print(f"  Rules Executed: {entry['total_rules']}")
        print(f"  Successful Rules: {entry['successful_rules']}")
        print(f"  Total Time: {entry['total_execution_time']:.3f}s")

    return engine


async def demo_custom_actions():
    """Demonstrate custom action capabilities."""
    print_separator("CUSTOM ACTIONS DEMO")

    # Create rule engine
    engine = RuleEngine()

    # Define a custom action
    def custom_greeting_action(action, context):


        """Custom action that generates a personalized greeting."""
        name = context.data.get('name', 'User')
        greeting = f"Hello {name}! Welcome to our brilliant rules system!"
        return greeting

    # Register the custom action
    engine.executor.register_custom_action('custom_greeting', custom_greeting_action)

    # Create a rule that uses the custom action
    from rules.types import Rule, Condition, Action, RulePriority, ContextType

    greeting_rule = Rule(
        name="personalized_greeting",
        description="Generate personalized greeting for users",
        priority=RulePriority.LOW,
        context_types=[ContextType.USER_REGISTRATION],
        conditions=[
            Condition("data.get('name') is not None", description="User has a name")
        ],
        actions=[
            Action("custom_greeting", parameters={}),
            Action("log_message", parameters={
                'message': 'Custom greeting generated',
                'level': 'INFO'
            })
        ],
        tags=['custom', 'greeting', 'personalization']
    )

    engine.add_rule(greeting_rule)

    # Test the custom action
    print("\n🧪 Test Case: Custom Greeting Action")
    user_data = {
        'name': 'Alice Johnson',
        'email': 'alice@example.com',
        'age': 28
    }

    context = ExecutionContext(
        context_type=ContextType.USER_REGISTRATION,
        context_id=f"custom_{int(time.time())}",
        data=user_data
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    return engine


async def demo_rule_chaining():
    """Demonstrate rule chaining capabilities."""
    print_separator("RULE CHAINING DEMO")

    # Create rule engine
    engine = RuleEngine()

    from rules.types import Rule, Condition, Action, RulePriority, ContextType

    # Rule 1: Initial validation
    initial_rule = Rule(
        name="initial_validation",
        description="Perform initial data validation",
        priority=RulePriority.HIGH,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("len(data.get('input_text', '')) > 0", description="Input text is provided")
        ],
        actions=[
            Action("update_data", parameters={
                'updates': {'initial_validation_passed': True, 'text_length': 'len(data.get("input_text", ""))'}
            }),
            Action("log_message", parameters={
                'message': 'Initial validation passed',
                'level': 'INFO'
            })
        ],
        tags=['validation', 'initial']
    )

    # Rule 2: Text processing (depends on initial validation)
    processing_rule = Rule(
        name="text_processing",
        description="Process the validated text",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('initial_validation_passed') == True", description="Initial validation passed"),
            Condition("data.get('text_length', 0) > 10", description="Text is long enough for processing")
        ],
        actions=[
            Action("update_data", parameters={
                'updates': {
                    'processed_text': 'data.get("input_text", "").upper()',
                    'processing_complete': True
                }
            }),
            Action("log_message", parameters={
                'message': 'Text processing completed',
                'level': 'INFO'
            })
        ],
        tags=['processing', 'text']
    )

    # Rule 3: Final output (depends on processing)
    output_rule = Rule(
        name="final_output",
        description="Generate final output",
        priority=RulePriority.LOW,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('processing_complete') == True", description="Processing is complete")
        ],
        actions=[
            Action("log_message", parameters={
                'message': f'Final output: {data.get("processed_text", "")}',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'final_output_ready': True}
            })
        ],
        tags=['output', 'final']
    )

    engine.add_rules([initial_rule, processing_rule, output_rule])

    # Test rule chaining
    print("\n🧪 Test Case: Rule Chaining with Text Processing")
    test_data = {
        'input_text': 'This is a test message for rule chaining demonstration'
    }

    context = ExecutionContext(
        context_type=ContextType.DATA_VALIDATION,
        context_id=f"chain_{int(time.time())}",
        data=test_data
    )

    results = await engine.evaluate_async(context)
    print_rule_results(results)

    # Show the final data state
    print(f"\n📋 Final Data State:")
    for key, value in context.data.items():
        print(f"  {key}: {value}")

    return engine


async def main():
    """Run all demos."""
    print("🚀 BRILLIANT RULES SYSTEM DEMO")
    print("=" * 60)
    print("This demo showcases the powerful features of our rules system:")
    print("• Declarative rule definition")
    print("• Complex condition evaluation")
    print("• Action execution and chaining")
    print("• Metrics and monitoring")
    print("• Custom actions and extensibility")
    print("• Performance optimization")
    print("• Comprehensive audit trail")

    # Run all demos
    engines = []

    try:
        engines.append(await demo_user_registration())
        engines.append(await demo_login_validation())
        engines.append(await demo_metrics_and_monitoring())
        engines.append(await demo_custom_actions())
        engines.append(await demo_rule_chaining())

        print_separator("DEMO COMPLETE")
        print("✅ All demos completed successfully!")
        print("\n🎉 The rules system is working brilliantly!")
        print("\nKey features demonstrated:")
        print("• Multi-rule evaluation with complex conditions")
        print("• Action execution with built-in and custom actions")
        print("• Comprehensive metrics and performance monitoring")
        print("• Rule chaining and dependency management")
        print("• Error handling and retry logic")
        print("• Audit trail and execution history")

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        raise

    finally:
        # Cleanup
        for engine in engines:
            engine.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
