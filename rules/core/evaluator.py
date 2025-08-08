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


class SafeValue:
    """A sentinel that safely absorbs attribute access, iteration, and comparisons."""
    def __getattr__(self, name: str) -> 'SafeValue':
        # Provide zero-like attributes often used in expressions
        if name in {'length', 'count'}:
            return 0
        return self

    def __iter__(self):
        return iter(())

    def __len__(self) -> int:
        return 0

    def __bool__(self) -> bool:
        return False

    # Comparisons always evaluate to False to avoid raising
    def _cmp(self, other) -> bool:
        return False

    __lt__ = __le__ = __gt__ = __ge__ = __ne__ = __eq__ = _cmp


class AttrDict(dict):
    """Dictionary that supports attribute-style access and recursive wrapping."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in list(self.items()):
            self[key] = self._wrap(value)

    def __getattr__(self, item):
        try:
            if item == 'length':
                return len(self)
            if item == 'count':
                return len(self)
            return self[item]
        except KeyError:
            return SafeValue()

    def __getitem__(self, key):
        if key in self.keys():
            return super().__getitem__(key)
        return SafeValue()

    def __setattr__(self, key, value):
        if key in {'_AttrDict__wrapped'}:
            return super().__setattr__(key, value)
        self[key] = self._wrap(value)

    @staticmethod
    def _wrap(value: Any) -> Any:
        if isinstance(value, dict):
            return AttrDict(value)
        if isinstance(value, list):
            return AttrList(value)
        return value


class AttrList(list):
    """List that provides attribute-style helpers and recursive wrapping."""
    def __init__(self, iterable=()):
        super().__init__(AttrDict._wrap(v) for v in iterable)

    @property
    def length(self) -> int:
        return len(self)

    @property
    def count(self) -> int:
        return len(self)


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
    
    def _wrap_data(self, data: Any) -> Any:
        """Recursively wrap dicts/lists for attribute-style access."""
        if isinstance(data, dict):
            return AttrDict(data)
        if isinstance(data, list):
            return AttrList(data)
        return data

    def _build_variables(self, context: ExecutionContext, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Build variables dictionary for expression evaluation."""
        wrapped_data = self._wrap_data(context.data or {})

        # Domain-friendly aliases inferred from data
        grant_alias = None
        report_alias = None
        if isinstance(wrapped_data, AttrDict):
            # If it looks like a grant application
            if 'grant_id' in wrapped_data or 'impact_metrics' in wrapped_data:
                grant_alias = wrapped_data
            # If it looks like an impact report
            if 'type' in wrapped_data and getattr(wrapped_data, 'type', None) == 'impact':
                report_alias = wrapped_data
            if 'outputs' in wrapped_data and 'outcomes' in wrapped_data:
                report_alias = wrapped_data

        project_alias = AttrDict({'id': context.data.get('project_id')}) if isinstance(context.data, dict) and 'project_id' in context.data else AttrDict({})
        agent_alias = self._wrap_data((context.data or {}).get('agent', {})) if isinstance(context.data, dict) else AttrDict({})
        user_alias = AttrDict({'request_type': ((context.data or {}).get('request', {}) or {}).get('type')}) if isinstance(context.data, dict) else AttrDict({})
        operation_alias = self._wrap_data((context.data or {}).get('operation', {})) if isinstance(context.data, dict) else AttrDict({})
        communication_alias = self._wrap_data((context.data or {}).get('communication', {})) if isinstance(context.data, dict) else AttrDict({})
        stakeholder_alias = self._wrap_data(((context.data or {}).get('stakeholder') or {})) if isinstance(context.data, dict) else AttrDict({})

        variables = {
            # Context data
            'context': context,
            'data': wrapped_data,
            'user_id': context.user_id,
            'session_id': context.session_id,
            'timestamp': context.timestamp,
            'metadata': context.metadata,
            'day_of_week': context.timestamp.strftime('%A') if isinstance(context.timestamp, datetime) else None,
            
            # Context type
            'context_type': context.context_type.value,
            
            # Domain aliases
            'grant': grant_alias or AttrDict({}),
            'report': report_alias or AttrDict({}),
            'project': project_alias,
            'agent': agent_alias,
            'user': user_alias,
            'operation': operation_alias,
            'communication': communication_alias,
            'stakeholder': stakeholder_alias,
            
            # Parameters
            **parameters,
            
            # Built-in functions
            **self.functions,
            
            # Built-in operators
            **self.operators
        }
        
        # Add data fields as top-level variables for convenience
        if isinstance(wrapped_data, (AttrDict, dict)):
            for key, value in (wrapped_data.items() if isinstance(wrapped_data, AttrDict) else wrapped_data.items()):
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
            ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq,
            ast.In, ast.NotIn,
            ast.BoolOp,
            ast.Attribute,
            ast.Call,
            ast.List,
            ast.Dict,
            ast.Tuple,
            ast.Subscript,
            ast.Index,
            ast.Slice,
            ast.Load
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
            'len', 'str', 'int', 'float', 'bool', 'length'
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