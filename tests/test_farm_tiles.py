import pytest

from timberborn_planner.calculators.farm_tiles import (
    calculate_daily_yield_per_tile,
    calculate_farm_tiles_needed,
)
from timberborn_planner.services.loaders import load_faction_data


def test_daily_yield_per_tile_calculation():
    crop_data = load_faction_data("folktails")["crops"]["carrots"]

    assert calculate_daily_yield_per_tile(crop_data) == 0.75


def test_required_tiles_rounds_up():
    crop_data = {"yield_per_tile": 3, "growth_days": 4}

    assert calculate_farm_tiles_needed(2, crop_data) == 3


def test_safety_buffer_increases_required_tiles():
    crop_data = {"yield_per_tile": 3, "growth_days": 4}

    assert calculate_farm_tiles_needed(3, crop_data, safety_buffer=25) == 5


def test_zero_food_need_returns_zero_tiles():
    crop_data = {"yield_per_tile": 3, "growth_days": 4}

    assert calculate_farm_tiles_needed(0, crop_data) == 0


def test_negative_food_need_raises_value_error():
    crop_data = {"yield_per_tile": 3, "growth_days": 4}

    with pytest.raises(ValueError, match="required_food_per_day"):
        calculate_farm_tiles_needed(-1, crop_data)


def test_negative_safety_buffer_raises_value_error():
    crop_data = {"yield_per_tile": 3, "growth_days": 4}

    with pytest.raises(ValueError, match="safety_buffer"):
        calculate_farm_tiles_needed(1, crop_data, safety_buffer=-1)


def test_zero_yield_raises_value_error():
    crop_data = {"yield_per_tile": 0, "growth_days": 4}

    with pytest.raises(ValueError, match="yield_per_tile"):
        calculate_daily_yield_per_tile(crop_data)


def test_zero_growth_days_raises_value_error():
    crop_data = {"yield_per_tile": 3, "growth_days": 0}

    with pytest.raises(ValueError, match="growth_days"):
        calculate_daily_yield_per_tile(crop_data)


# END OF FILE
