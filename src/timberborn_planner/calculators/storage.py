"""Storage reserve calculators."""

from timberborn_planner.models.colony import ColonyInputs


def calculate_storage_reserve(daily_need: float, colony: ColonyInputs) -> float:
    """Calculate reserve need for a drought with the colony safety buffer."""

    safety_multiplier = 1 + colony.safety_buffer / 100

    return daily_need * colony.drought_days * safety_multiplier


# END OF FILE
