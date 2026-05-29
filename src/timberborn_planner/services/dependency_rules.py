"""Rules for turning building data into dependency summaries."""

from typing import Any

from timberborn_planner.models.building import (
    BuildingBuildRequirements,
    BuildingDependencySummary,
    BuildingRunRequirements,
    ResourceAmounts,
    WorkerSupportBurden,
)


def get_building_dependency_summary(
    building_id: str,
    faction_data: dict[str, Any],
    global_data: dict[str, Any] | None = None,
) -> BuildingDependencySummary:
    """Return build, run, and worker support requirements for one building."""

    buildings = faction_data.get("buildings", {})
    if building_id not in buildings:
        raise ValueError(f"Unknown building id: {building_id}")

    building_data = buildings[building_id]
    workers = int(building_data.get("workers", 0))

    return BuildingDependencySummary(
        building_id=building_id,
        name=str(building_data.get("name", building_id)),
        build=BuildingBuildRequirements(
            construction_cost=_resource_amounts(building_data, "construction_cost"),
            science_cost=_resource_amounts(building_data, "science_cost"),
        ),
        run=BuildingRunRequirements(
            workers=workers,
            inputs_per_day=_resource_amounts(building_data, "inputs_per_day"),
            outputs_per_day=_resource_amounts(building_data, "outputs_per_day"),
            power_required=building_data.get("power_required", 0),
            power_produced=building_data.get("power_produced", 0),
        ),
        support=_worker_support_burden(workers, global_data),
    )


def _resource_amounts(data: dict[str, Any], key: str) -> ResourceAmounts:
    values = data.get(key, {})
    if values is None:
        return {}

    return dict(values)


def _worker_support_burden(
    workers: int,
    global_data: dict[str, Any] | None,
) -> WorkerSupportBurden:
    if global_data is None:
        return WorkerSupportBurden(workers=workers, housing=workers)

    adult_rates = global_data["population"]["adult"]

    return WorkerSupportBurden(
        workers=workers,
        food_per_day=workers * float(adult_rates["food_per_day"]),
        water_per_day=workers * float(adult_rates["water_per_day"]),
        housing=workers,
    )


# END OF FILE
