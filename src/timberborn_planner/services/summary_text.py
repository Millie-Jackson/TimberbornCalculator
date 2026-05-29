"""Human-readable summary text for planner results."""

from timberborn_planner.models.building import ResourceAmounts
from timberborn_planner.services.planner import BuildingPlanResult


def format_resource_amounts(
    resources: ResourceAmounts,
    per_day: bool = False,
) -> str:
    """Format resource amounts without exposing raw Python data structures."""

    if not resources:
        return "none"

    suffix = "/day" if per_day else ""
    formatted_resources = [
        f"{_format_number(amount)} {_format_resource_name(resource_id)}{suffix}"
        for resource_id, amount in resources.items()
    ]

    return _join_readable_list(formatted_resources)


def format_worker_support_summary(plan_result: BuildingPlanResult) -> str:
    worker_text = _pluralise(plan_result.extra_workers, "extra worker")
    food = _format_number(plan_result.food_per_day_for_workers)
    water = _format_number(plan_result.water_per_day_for_workers)

    return f"{worker_text}, {food} food/day, {water} water/day"


def format_power_summary(plan_result: BuildingPlanResult) -> str:
    return (
        f"Power required: {_format_number(plan_result.power_required)}. "
        f"Power produced: {_format_number(plan_result.power_produced)}. "
        f"{plan_result.power_message}"
    )


def format_building_plan_summary(plan_result: BuildingPlanResult) -> str:
    """Format a short player-facing summary for a building plan result."""

    building_label = _format_building_quantity(
        plan_result.quantity,
        plan_result.building_name,
    )
    construction_cost = format_resource_amounts(
        plan_result.upstream_resources.get("construction_cost", {}),
    )
    run_inputs = format_resource_amounts(
        plan_result.upstream_resources.get("inputs_per_day", {}),
        per_day=True,
    )

    summary = (
        f"Adding {building_label} needs "
        f"{format_worker_support_summary(plan_result)}, "
        f"{construction_cost} to build, and {run_inputs} to run. "
        f"{format_power_summary(plan_result)}"
    )

    if plan_result.upstream_buildings:
        dependencies = [
            _format_building_id(building_id)
            for building_id in plan_result.upstream_buildings
        ]
        summary += f" It also depends on: {_join_readable_list(dependencies)}."

    return summary


def _format_building_quantity(quantity: int, building_name: str) -> str:
    if quantity == 1:
        return f"1 {building_name}"

    return f"{quantity} {_pluralise_name(building_name)}"


def _format_building_id(building_id: str) -> str:
    return building_id.replace("_", " ").title()


def _format_resource_name(resource_id: str) -> str:
    return resource_id.replace("_", " ")


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _join_readable_list(values: list[str]) -> str:
    if len(values) <= 1:
        return "".join(values)

    if len(values) == 2:
        return f"{values[0]} and {values[1]}"

    return f"{', '.join(values[:-1])}, and {values[-1]}"


def _pluralise(amount: float | int, singular: str) -> str:
    if amount == 1:
        return f"{_format_number(amount)} {singular}"

    return f"{_format_number(amount)} {singular}s"


def _pluralise_name(name: str) -> str:
    if name.endswith("s"):
        return name

    return f"{name}s"


# END OF FILE
