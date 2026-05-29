"""Power demand calculators."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PowerSummary:
    """Power totals and status for selected buildings."""

    total_required_power: float | int
    total_produced_power: float | int
    power_balance: float | int
    status: str
    message: str


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


def calculate_power_summary(
    building_quantities: dict[str, int],
    faction_data: dict[str, Any],
) -> PowerSummary:
    """Calculate power totals with a player-readable status message."""

    total_required_power = calculate_total_power_demand(
        building_quantities,
        faction_data,
    )
    total_produced_power = calculate_total_power_generation(
        building_quantities,
        faction_data,
    )
    power_balance = total_produced_power - total_required_power
    status = _power_status(power_balance)

    return PowerSummary(
        total_required_power=total_required_power,
        total_produced_power=total_produced_power,
        power_balance=power_balance,
        status=status,
        message=_power_message(status, power_balance),
    )


def _power_status(power_balance: float | int) -> str:
    if power_balance < 0:
        return "deficit"

    if power_balance > 0:
        return "surplus"

    return "balanced"


def _power_message(status: str, power_balance: float | int) -> str:
    if status == "deficit":
        return f"Power deficit: {_format_number(abs(power_balance))}"

    if status == "surplus":
        return f"Power surplus: {_format_number(power_balance)}"

    return "Power is balanced."


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


# END OF FILE
