from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId, lift_tenant_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.expression_evaluation_request_context import (
        ExpressionEvaluationRequestContext,
    )


T = TypeVar("T", bound="ExpressionEvaluationRequest")


@_attrs_define
class ExpressionEvaluationRequest:
    """
    Attributes:
        expression (str): The expression to evaluate (e.g., "=x + y") Example: =x + y.
        tenant_id (str | Unset): Required when the expression references tenant-scoped cluster variables Example:
            tenant_123.
        context (ExpressionEvaluationRequestContext | None | Unset): Optional context variables for expression
            evaluation. These variables are only used for the current evaluation and do not persist beyond it. Example:
            {'x': 10, 'y': 20}.
    """

    expression: str
    tenant_id: TenantId | Unset = UNSET
    context: ExpressionEvaluationRequestContext | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.expression_evaluation_request_context import (
            ExpressionEvaluationRequestContext,
        )

        expression = self.expression

        tenant_id = self.tenant_id

        context: dict[str, Any] | None | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        elif isinstance(self.context, ExpressionEvaluationRequestContext):
            context = self.context.to_dict()
        else:
            context = self.context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expression": expression,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.expression_evaluation_request_context import (
            ExpressionEvaluationRequestContext,
        )

        d = dict(src_dict)
        expression = d.pop("expression")

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        def _parse_context(
            data: object,
        ) -> ExpressionEvaluationRequestContext | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_expression_evaluation_request_context_type_0 = (
                    ExpressionEvaluationRequestContext.from_dict(data)
                )

                return componentsschemas_expression_evaluation_request_context_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExpressionEvaluationRequestContext | None | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        expression_evaluation_request = cls(
            expression=expression,
            tenant_id=tenant_id,
            context=context,
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
