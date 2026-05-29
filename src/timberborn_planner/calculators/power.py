"""Power demand calculators."""

from typing import Any


def calculate_building_power_demand(
    building_data: dict[str, Any],
    quantity: int,
) -> float | int:
    """Calculate direct power demand for one building type."""

    if quantity < 0:
        raise ValueError("quantity must be 0 or above")

    return building_data.get("power_required", 0) * quantity


def calculate_total_power_demand(
    building_quantities: dict[str, int],
    faction_data: dict[str, Any],
) -> float | int:
    """Calculate total power demand from selected building quantities."""

    buildings = faction_data.get("buildings", {})
    total_demand: float | int = 0

    for building_id, quantity in building_quantities.items():
        if building_id not in buildings:
            raise ValueError(f"Unknown building id: {building_id}")

        total_demand += calculate_building_power_demand(
            buildings[building_id],
            quantity,
        )

    return total_demand


# END OF FILE
