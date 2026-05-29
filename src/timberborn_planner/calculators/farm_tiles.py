"""Farm tile estimation calculators."""

import math
from typing import Any


def calculate_daily_yield_per_tile(crop_data: dict[str, Any]) -> float:
    """Calculate average daily food output from one farm tile."""

    yield_per_tile = float(crop_data["yield_per_tile"])
    growth_days = float(crop_data["growth_days"])

    if yield_per_tile <= 0:
        raise ValueError("yield_per_tile must be above 0")

    if growth_days <= 0:
        raise ValueError("growth_days must be above 0")

    return yield_per_tile / growth_days


def calculate_farm_tiles_needed(
    required_food_per_day: float,
    crop_data: dict[str, Any],
    safety_buffer: float = 0,
) -> int:
    """Estimate whole farm tiles needed for a daily food target."""

    if required_food_per_day < 0:
        raise ValueError("required_food_per_day must be 0 or above")

    if safety_buffer < 0:
        raise ValueError("safety_buffer must be 0 or above")

    if required_food_per_day == 0:
        return 0

    daily_yield_per_tile = calculate_daily_yield_per_tile(crop_data)
    buffered_food_need = required_food_per_day * (1 + safety_buffer / 100)

    return math.ceil(buffered_food_need / daily_yield_per_tile)


# END OF FILE
