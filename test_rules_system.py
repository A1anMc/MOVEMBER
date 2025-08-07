#!/usr/bin/env python3
"""
Simple test for the rules system.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rules.core import RuleEngine
from rules.types import Rule, Condition, Action, RulePriority, ContextType, ExecutionContext


async def test_basic_rule():
    """Test a basic rule execution."""
    print("🧪 Testing basic rule execution...")
    
    # Create rule engine
    engine = RuleEngine()
    
    # Create a simple rule
    test_rule = Rule(
        name="test_rule",
        description="A simple test rule",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('value', 0) > 10", description="Value must be greater than 10")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'Test rule executed successfully',
                'level': 'INFO'
            }),
            Action("update_data", parameters={
                'updates': {'test_passed': True}
            })
        ]
    )
    
    engine.add_rule(test_rule)
    
    # Test with valid data
    context = ExecutionContext(
        context_type=ContextType.DATA_VALIDATION,
        context_id="test_1",
        data={'value': 15}
    )
    
    results = await engine.evaluate_async(context)
    
    assert len(results) == 1
    assert results[0].success
    assert results[0].conditions_met
    assert len(results[0].action_results) == 2
    
    print("✅ Basic rule test passed!")
    return True


async def test_rule_with_failed_condition():
    """Test a rule where conditions fail."""
    print("🧪 Testing rule with failed condition...")
    
    # Create rule engine
    engine = RuleEngine()
    
    # Create a simple rule
    test_rule = Rule(
        name="test_rule_fail",
        description="A test rule that should fail",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('value', 0) > 100", description="Value must be greater than 100")
        ],
        actions=[
            Action("log_message", parameters={
                'message': 'This should not execute',
                'level': 'INFO'
            })
        ]
    )
    
    engine.add_rule(test_rule)
    
    # Test with invalid data
    context = ExecutionContext(
        context_type=ContextType.DATA_VALIDATION,
        context_id="test_2",
        data={'value': 5}
    )
    
    results = await engine.evaluate_async(context)
    
    assert len(results) == 1
    assert results[0].success
    assert not results[0].conditions_met
    assert not results[0].action_results  # No actions should execute
    
    print("✅ Failed condition test passed!")
    return True


async def test_multiple_rules():
    """Test multiple rules execution."""
    print("🧪 Testing multiple rules execution...")
    
    # Create rule engine
    engine = RuleEngine()
    
    # Create multiple rules
    rule1 = Rule(
        name="rule_1",
        description="First rule",
        priority=RulePriority.HIGH,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('value', 0) > 0", description="Value must be positive")
        ],
        actions=[
            Action("update_data", parameters={
                'updates': {'rule1_executed': True}
            })
        ]
    )
    
    rule2 = Rule(
        name="rule_2",
        description="Second rule",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('value', 0) > 10", description="Value must be greater than 10")
        ],
        actions=[
            Action("update_data", parameters={
                'updates': {'rule2_executed': True}
            })
        ]
    )
    
    engine.add_rules([rule1, rule2])
    
    # Test with data that should trigger both rules
    context = ExecutionContext(
        context_type=ContextType.DATA_VALIDATION,
        context_id="test_3",
        data={'value': 15}
    )
    
    results = await engine.evaluate_async(context)
    
    assert len(results) == 2
    assert all(result.success for result in results)
    assert all(result.conditions_met for result in results)
    
    # Check that both rules updated the data
    assert context.data.get('rule1_executed')
    assert context.data.get('rule2_executed')
    
    print("✅ Multiple rules test passed!")
    return True


async def test_custom_action():
    """Test custom action execution."""
    print("🧪 Testing custom action...")
    
    # Create rule engine
    engine = RuleEngine()
    
    # Define custom action
    def custom_test_action(action, context):
        return f"Custom action executed with value: {context.data.get('value', 0)}"
    
    # Register custom action
    engine.executor.register_custom_action('custom_test', custom_test_action)
    
    # Create rule with custom action
    test_rule = Rule(
        name="custom_action_rule",
        description="Rule with custom action",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.get('value', 0) > 0", description="Value must be positive")
        ],
        actions=[
            Action("custom_test", parameters={})
        ]
    )
    
    engine.add_rule(test_rule)
    
    # Test custom action
    context = ExecutionContext(
        context_type=ContextType.DATA_VALIDATION,
        context_id="test_4",
        data={'value': 42}
    )
    
    results = await engine.evaluate_async(context)
    
    assert len(results) == 1
    assert results[0].success
    assert results[0].conditions_met
    assert len(results[0].action_results) == 1
    assert "Custom action executed with value: 42" in results[0].action_results[0].result
    
    print("✅ Custom action test passed!")
    return True


async def run_all_tests():
    """Run all tests."""
    print("🚀 Running Rules System Tests")
    print("=" * 40)
    
    tests = [
        test_basic_rule,
        test_rule_with_failed_condition,
        test_multiple_rules,
        test_custom_action
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The rules system is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1) 