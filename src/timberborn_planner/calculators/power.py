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


def calculate_building_power_generation(
    building_data: dict[str, Any],
    quantity: int,
) -> float | int:
    """Calculate direct power generation for one building type."""

    if quantity < 0:
        raise ValueError("quantity must be 0 or above")

    return building_data.get("power_produced", 0) * quantity


def calculate_total_power_generation(
    building_quantities: dict[str, int],
    faction_data: dict[str, Any],
) -> float | int:
    """Calculate total power generation from selected building quantities."""

    buildings = faction_data.get("buildings", {})
    total_generation: float | int = 0

    for building_id, quantity in building_quantities.items():
        if building_id not in buildings:
            raise ValueError(f"Unknown building id: {building_id}")

        total_generation += calculate_building_power_generation(
            buildings[building_id],
            quantity,
        )

    return total_generation


def calculate_power_balance(
    building_quantities: dict[str, int],
    faction_data: dict[str, Any],
) -> float | int:
    """Calculate net power balance from generation minus demand."""

    return calculate_total_power_generation(
        building_quantities,
        faction_data,
    ) - calculate_total_power_demand(
        building_quantities,
        faction_data,
    )


# END OF FILE
