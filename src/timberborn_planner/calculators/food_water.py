"""Food and water need calculators."""

from typing import Any

from timberborn_planner.models.colony import ColonyInputs


def calculate_food_per_day(
    colony: ColonyInputs,
    global_data: dict[str, Any],
) -> float:
    """Calculate daily food need from biological population."""

    return (
        colony.adults * _population_rate(global_data, "adult", "food_per_day")
        + colony.kits * _population_rate(global_data, "kit", "food_per_day")
        + colony.bots * _population_rate(global_data, "bot", "food_per_day")
    )


def calculate_water_per_day(
    colony: ColonyInputs,
    global_data: dict[str, Any],
) -> float:
    """Calculate daily water need from biological population."""

    return (
        colony.adults * _population_rate(global_data, "adult", "water_per_day")
        + colony.kits * _population_rate(global_data, "kit", "water_per_day")
        + colony.bots * _population_rate(global_data, "bot", "water_per_day")
    )


def _population_rate(
    global_data: dict[str, Any],
    population_type: str,
    rate_name: str,
) -> float:
    return float(global_data["population"][population_type][rate_name])


# END OF FILE
