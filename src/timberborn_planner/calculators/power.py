"""Power demand calculators."""

import math
from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(frozen=True)
class PowerSetupSuggestion:
    """One suggested power-producing building option."""

    building_id: str
    building_name: str
    quantity: int
    power_per_building: float | int
    total_power_produced: float | int

    def to_dict(self) -> dict[str, float | int | str]:
        return {
            "building_id": self.building_id,
            "building_name": self.building_name,
            "quantity": self.quantity,
            "power_per_building": self.power_per_building,
            "total_power_produced": self.total_power_produced,
        }


@dataclass(frozen=True)
class PowerSetupPlan:
    """Suggested setup for covering a power gap."""

    power_gap: float | int
    suggestions: list[PowerSetupSuggestion] = field(default_factory=list)
    message: str = "No extra power setup needed."

    def to_dict(self) -> dict[str, object]:
        return {
            "power_gap": self.power_gap,
            "suggestions": [suggestion.to_dict() for suggestion in self.suggestions],
            "message": self.message,
        }


@dataclass(frozen=True)
class PowerSummary:
    """Power totals and status for selected buildings."""

    total_required_power: float | int
    total_produced_power: float | int
    power_balance: float | int
    status: str
    message: str
    suggested_setup: PowerSetupPlan = field(default_factory=PowerSetupPlan)


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
        suggested_setup=suggest_power_setup(abs(power_balance), faction_data)
        if status == "deficit"
        else suggest_power_setup(0, faction_data),
    )


def suggest_power_setup(
    power_gap: float | int,
    faction_data: dict[str, Any],
) -> PowerSetupPlan:
    """Suggest a simple power setup to cover a positive power gap."""

    if power_gap <= 0:
        return PowerSetupPlan(
            power_gap=0,
            suggestions=[],
            message="No extra power setup needed.",
        )

    producer = _preferred_power_producer(faction_data)
    if producer is None:
        return PowerSetupPlan(
            power_gap=power_gap,
            suggestions=[],
            message=(
                "No power-producing buildings are available to cover "
                f"a {_format_number(power_gap)} power gap."
            ),
        )

    building_id, building_data = producer
    power_per_building = building_data["power_produced"]
    quantity = math.ceil(power_gap / power_per_building)
    total_power_produced = power_per_building * quantity
    building_name = str(building_data.get("name", building_id))
    suggestion = PowerSetupSuggestion(
        building_id=building_id,
        building_name=building_name,
        quantity=quantity,
        power_per_building=power_per_building,
        total_power_produced=total_power_produced,
    )

    return PowerSetupPlan(
        power_gap=power_gap,
        suggestions=[suggestion],
        message=(
            f"Add {_pluralise(quantity, building_name)} to cover "
            f"a {_format_number(power_gap)} power gap."
        ),
    )


def _preferred_power_producer(
    faction_data: dict[str, Any],
) -> tuple[str, dict[str, Any]] | None:
    producers = [
        (building_id, building_data)
        for building_id, building_data in faction_data.get("buildings", {}).items()
        if building_data.get("power_produced", 0) > 0
    ]

    if not producers:
        return None

    for building_id, building_data in producers:
        if building_id == "power_wheel":
            return building_id, building_data

    return producers[0]


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


def _pluralise(quantity: int, name: str) -> str:
    if quantity == 1:
        return f"1 {name}"

    if name.endswith("s"):
        return f"{quantity} {name}"

    return f"{quantity} {name}s"


# END OF FILE
