from dataclasses import dataclass

from .v10_action_plan import InventoryActionPlan
from .v10_decision_contract import InventoryDecisionInput


@dataclass(frozen=True)
class DecisionValidationResult:
    valid: bool
    errors: tuple[str, ...]


class InventoryDecisionValidator:

    def validate(
        self,
        decision_input: InventoryDecisionInput,
        action_plan: InventoryActionPlan,
    ) -> DecisionValidationResult:

        errors: list[str] = []

        if decision_input.forecast_demand < 0:
            errors.append("forecast_demand cannot be negative")

        if action_plan.purchase_required:
            if action_plan.purchase_line is None:
                errors.append("missing purchase line")

            if (
                action_plan.purchase_line is not None
                and action_plan.purchase_line.quantity <= 0
            ):
                errors.append(
                    "purchase quantity must be positive"
                )

        if not action_plan.purchase_required:
            if action_plan.purchase_line is not None:
                errors.append(
                    "purchase line exists without purchase requirement"
                )

        return DecisionValidationResult(
            valid=len(errors) == 0,
            errors=tuple(errors),
        )
