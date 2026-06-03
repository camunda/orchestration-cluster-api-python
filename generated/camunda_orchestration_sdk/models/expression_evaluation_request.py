from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ScopeKey, lift_scope_key

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.expression_evaluation_request_variables import (
        ExpressionEvaluationRequestVariables,
    )


T = TypeVar("T", bound="ExpressionEvaluationRequest")


@_attrs_define
class ExpressionEvaluationRequest:
    """
    Attributes:
        expression (str): The expression to evaluate (e.g., "=x + y") Example: =x + y.
        tenant_id (str | Unset): Required when the expression references tenant-scoped cluster variables Example:
            tenant_123.
        scope_key (str | Unset): Key of the process instance or element instance whose variables should be made visible
            to the expression. Use a process instance key to evaluate against the process instance
            scope, or an element instance key to evaluate against that element instance scope. If
            omitted, the expression is evaluated unscoped, using only cluster variables
            and request-body variables.
        variables (ExpressionEvaluationRequestVariables | None | Unset): Optional variables for expression evaluation.
            These variables are only used for the current evaluation and do not persist beyond it. Example: {'x': 10, 'y':
            20}.
    """

    expression: str
    tenant_id: str | Unset = UNSET
    scope_key: ScopeKey | Unset = UNSET
    variables: ExpressionEvaluationRequestVariables | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        from ..models.expression_evaluation_request_variables import (
            ExpressionEvaluationRequestVariables,
        )

        expression = self.expression

        tenant_id = self.tenant_id

        scope_key: ScopeKey | Unset
        if isinstance(self.scope_key, Unset):
            scope_key = UNSET
        else:
            scope_key = self.scope_key

        variables: dict[str, Any] | None | Unset
        if isinstance(self.variables, Unset):
            variables = UNSET
        elif isinstance(self.variables, ExpressionEvaluationRequestVariables):
            variables = self.variables.to_dict()
        else:
            variables = self.variables

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expression": expression,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if scope_key is not UNSET:
            field_dict["scopeKey"] = scope_key
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.expression_evaluation_request_variables import (
            ExpressionEvaluationRequestVariables,
        )

        d = dict(src_dict)
        expression = d.pop("expression")

        tenant_id = d.pop("tenantId", UNSET)

        def _parse_scope_key(data: object) -> str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(str | Unset, data)

        _raw_scope_key = _parse_scope_key(d.pop("scopeKey", UNSET))


        scope_key = lift_scope_key(_raw_scope_key)

        def _parse_variables(
            data: object,
        ) -> ExpressionEvaluationRequestVariables | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_expression_evaluation_request_variables_type_0 = (
                    ExpressionEvaluationRequestVariables.from_dict(data)
                )

                return componentsschemas_expression_evaluation_request_variables_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExpressionEvaluationRequestVariables | None | Unset, data)

        variables = _parse_variables(d.pop("variables", UNSET))

        expression_evaluation_request = cls(
            expression=expression,
            tenant_id=tenant_id,
            scope_key=scope_key,
            variables=variables,
        )

        expression_evaluation_request.additional_properties = d
        return expression_evaluation_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
