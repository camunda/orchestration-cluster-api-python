"""Deprecated compatibility shim module.

``ProcessInstanceCreationInstructionByIdVariables`` was renamed to ``ProcessInstanceCreationInstructionBaseVariables`` by an upstream spec backport
within the 10.x line. This module is preserved so existing imports of
``camunda_orchestration_sdk.models.process_instance_creation_instruction_by_id_variables`` keep working. Importing it
emits a ``DeprecationWarning``; the exported name is the same class object as
``ProcessInstanceCreationInstructionBaseVariables``. It will be removed in the next major version.
"""

from __future__ import annotations

import warnings as _warnings

from .process_instance_creation_instruction_base_variables import (
    ProcessInstanceCreationInstructionBaseVariables as ProcessInstanceCreationInstructionByIdVariables,
)

_warnings.warn(
    "camunda_orchestration_sdk.models.process_instance_creation_instruction_by_id_variables is deprecated, use "
    "camunda_orchestration_sdk.models.process_instance_creation_instruction_base_variables (ProcessInstanceCreationInstructionBaseVariables) instead. "
    "Will be removed in the next major version.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ProcessInstanceCreationInstructionByIdVariables"]
