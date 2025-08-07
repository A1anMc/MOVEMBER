"""
Rule Evaluator

Handles evaluation of rule conditions with support for complex expressions
and custom evaluators.
"""

from typing import List, Dict, Any, Optional, Callable
import logging
import re
import ast
import operator
from datetime import datetime
import asyncio

from ..types import Condition, ExecutionContext

logger = logging.getLogger(__name__)


class ConditionEvaluator:
    """Evaluates individual conditions."""
    
    def __init__(self):
        # Built-in operators
        self.operators = {
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge,
            'in': operator.contains,
            'not in': lambda x, y: not operator.contains(x, y),
            'is': operator.is_,
            'is not': operator.is_not,
            'and': operator.and_,
            'or': operator.or_,
            'not': operator.not_
        }
        
        # Built-in functions
        self.functions = {
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'isinstance': isinstance,
            'hasattr': hasattr,
            'getattr': getattr,
            'datetime': datetime,
            'now': datetime.now
        }
    
    def evaluate(self, condition: Condition, context: ExecutionContext) -> bool:
        """Evaluate a single condition."""
        try:
            if condition.custom_evaluator:
                return condition.custom_evaluator(context)
            
            # Parse and evaluate the expression
            expression = condition.expression
            variables = self._build_variables(context, condition.parameters)
            
            return self._evaluate_expression(expression, variables)
            
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition.expression}': {e}")
            return False
    
    async def evaluate_async(self, condition: Condition, context: ExecutionContext) -> bool:
        """Evaluate a single condition asynchronously."""
        if asyncio.iscoroutinefunction(condition.custom_evaluator):
            return await condition.custom_evaluator(context)
        
        # For synchronous evaluators, run in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.evaluate, condition, context
        )
    
    def _build_variables(self, context: ExecutionContext, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Build variables dictionary for expression evaluation."""
        variables = {
            # Context data
            'context': context,
            'data': context.data,
            'user_id': context.user_id,
            'session_id': context.session_id,
            'timestamp': context.timestamp,
            'metadata': context.metadata,
            
            # Context type
            'context_type': context.context_type.value,
            
            # Parameters
            **parameters,
            
            # Built-in functions
            **self.functions,
            
            # Built-in operators
            **self.operators
        }
        
        # Add data fields as top-level variables for convenience
        for key, value in context.data.items():
            if key not in variables:  # Don't override built-ins
                variables[key] = value
        
        return variables
    
    def _evaluate_expression(self, expression: str, variables: Dict[str, Any]) -> bool:
        """Evaluate a Python expression safely."""
        try:
            # Parse the expression
            tree = ast.parse(expression, mode='eval')
            
            # Validate the expression (only allow safe operations)
            self._validate_ast(tree)
            
            # Compile and evaluate
            code = compile(tree, '<string>', 'eval')
            result = eval(code, {"__builtins__": {}}, variables)
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error evaluating expression '{expression}': {e}")
            return False
    
    def _validate_ast(self, tree: ast.Expression) -> None:
        """Validate AST to ensure only safe operations are allowed."""
        allowed_nodes = {
            ast.Expression,
            ast.Name,
            ast.Constant,
            ast.BinOp,
            ast.UnaryOp,
            ast.Compare,
            ast.BoolOp,
            ast.Attribute,
            ast.Call,
            ast.List,
            ast.Dict,
            ast.Tuple,
            ast.Subscript,
            ast.Index,
            ast.Slice
        }
        
        for node in ast.walk(tree):
            if type(node) not in allowed_nodes:
                raise ValueError(f"Unsafe operation: {type(node).__name__}")
            
            # Additional safety checks
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name not in self.functions:
                        raise ValueError(f"Function '{func_name}' not allowed")
                elif isinstance(node.func, ast.Attribute):
                    # Allow method calls on safe objects
                    if not self._is_safe_attribute(node.func):
                        raise ValueError(f"Attribute access not allowed: {ast.unparse(node.func)}")
    
    def _is_safe_attribute(self, node: ast.Attribute) -> bool:
        """Check if attribute access is safe."""
        # Allow common safe attributes
        safe_attributes = {
            'lower', 'upper', 'strip', 'split', 'join', 'replace',
            'startswith', 'endswith', 'find', 'count', 'isdigit',
            'isalpha', 'isalnum', 'isspace', 'format', 'keys',
            'values', 'items', 'get', 'append', 'extend', 'pop',
            'len', 'str', 'int', 'float', 'bool'
        }
        
        if isinstance(node.attr, str) and node.attr in safe_attributes:
            return True
        
        return False


class RuleEvaluator:
    """Evaluates multiple conditions for a rule."""
    
    def __init__(self):
        self.condition_evaluator = ConditionEvaluator()
    
    def evaluate_conditions(self, conditions: List[Condition], context: ExecutionContext) -> bool:
        """Evaluate all conditions for a rule."""
        if not conditions:
            return True
        
        for condition in conditions:
            if not self.condition_evaluator.evaluate(condition, context):
                return False
        
        return True
    
    async def evaluate_conditions_async(self, conditions: List[Condition], context: ExecutionContext) -> bool:
        """Evaluate all conditions for a rule asynchronously."""
        if not conditions:
            return True
        
        for condition in conditions:
            if not await self.condition_evaluator.evaluate_async(condition, context):
                return False
        
        return True
    
    def evaluate_conditions_with_details(self, conditions: List[Condition], context: ExecutionContext) -> Dict[str, Any]:
        """Evaluate conditions and return detailed results."""
        results = {
            'all_passed': True,
            'conditions': [],
            'total_conditions': len(conditions)
        }
        
        for i, condition in enumerate(conditions):
            start_time = datetime.now()
            passed = self.condition_evaluator.evaluate(condition, context)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            condition_result = {
                'index': i,
                'expression': condition.expression,
                'description': condition.description,
                'passed': passed,
                'execution_time': execution_time
            }
            
            results['conditions'].append(condition_result)
            
            if not passed:
                results['all_passed'] = False
        
        return results 