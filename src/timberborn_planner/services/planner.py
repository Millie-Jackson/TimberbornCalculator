"""First-pass non-recursive building planning logic."""

from dataclasses import dataclass, field
from typing import Any

from timberborn_planner.calculators.food_water import (
    calculate_food_per_day,
    calculate_water_per_day,
)
from timberborn_planner.models.building import ResourceAmounts
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.dependency_rules import (
    get_building_dependency_summary,
)


@dataclass(frozen=True)
class BuildingPlanResult:
    """Support breakdown for adding one kind of building."""

    building_id: str
    building_name: str
    quantity: int = 1
    extra_workers: int = 0
    upstream_resources: dict[str, ResourceAmounts] = field(default_factory=dict)
    upstream_buildings: list[str] = field(default_factory=list)
    food_per_day_for_workers: float = 0
    water_per_day_for_workers: float = 0
    power_required: float | int = 0
    power_produced: float | int = 0
    power_balance: float | int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "building_id": self.building_id,
            "building_name": self.building_name,
            "quantity": self.quantity,
            "extra_workers": self.extra_workers,
            "upstream_resources": {
                key: dict(value) for key, value in self.upstream_resources.items()
            },
            "upstream_buildings": list(self.upstream_buildings),
            "food_per_day_for_workers": self.food_per_day_for_workers,
            "water_per_day_for_workers": self.water_per_day_for_workers,
            "power_required": self.power_required,
            "power_produced": self.power_produced,
            "power_balance": self.power_balance,
        }


def plan_building_addition(
    faction_data: dict[str, Any],
    global_data: dict[str, Any],
    building_id: str,
    quantity: int = 1,
) -> BuildingPlanResult:
    """Plan the direct support needs for adding buildings.

    This first version does not recursively expand upstream building chains.
    """

    if quantity < 0:
        raise ValueError("quantity must be 0 or above")

    dependency_summary = get_building_dependency_summary(
        building_id=building_id,
        faction_data=faction_data,
        global_data=global_data,
    )
    building_data = faction_data["buildings"][building_id]

    extra_workers = dependency_summary.run.workers * quantity
    worker_colony = ColonyInputs(adults=extra_workers)
    power_required = dependency_summary.run.power_required * quantity
    power_produced = dependency_summary.run.power_produced * quantity

    return BuildingPlanResult(
        building_id=dependency_summary.building_id,
        building_name=dependency_summary.name,
        quantity=quantity,
        extra_workers=extra_workers,
        upstream_resources={
            "construction_cost": _multiply_resource_amounts(
                dependency_summary.build.construction_cost,
                quantity,
            ),
            "science_cost": _multiply_resource_amounts(
                dependency_summary.build.science_cost,
                quantity,
            ),
            "inputs_per_day": _multiply_resource_amounts(
                dependency_summary.run.inputs_per_day,
                quantity,
            ),
        },
        upstream_buildings=list(building_data.get("upstream_dependencies", [])),
        food_per_day_for_workers=calculate_food_per_day(worker_colony, global_data),
        water_per_day_for_workers=calculate_water_per_day(worker_colony, global_data),
        power_required=power_required,
        power_produced=power_produced,
        power_balance=power_produced - power_required,
    )


def _multiply_resource_amounts(
    resource_amounts: ResourceAmounts,
    quantity: int,
) -> ResourceAmounts:
    return {
        resource_id: amount * quantity
        for resource_id, amount in resource_amounts.items()
    }


# END OF FILE
