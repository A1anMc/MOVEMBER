import builtins
import logging

# Provide a global `logger` name accessible in tests
builtins.logger = logging.getLogger("tests")
