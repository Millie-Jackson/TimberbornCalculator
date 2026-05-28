"""Housing need calculators."""

from timberborn_planner.models.colony import ColonyInputs


def calculate_housing_need(colony: ColonyInputs) -> int:
    return colony.adults + colony.kits


# END OF FILE
