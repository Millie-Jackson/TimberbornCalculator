from timberborn_planner.calculators.bot_support import calculate_bot_support
from timberborn_planner.calculators.food_water import (
    calculate_food_per_day,
    calculate_water_per_day,
)
from timberborn_planner.calculators.housing import calculate_housing_need
from timberborn_planner.calculators.storage import calculate_storage_reserve
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.loaders import load_global_data


def test_adults_and_kits_need_food():
    colony = ColonyInputs(adults=3, kits=2)
    global_data = load_global_data()

    assert calculate_food_per_day(colony, global_data) == 8


def test_food_per_day_uses_loaded_population_rates():
    colony = ColonyInputs(adults=1, kits=1, bots=1)
    global_data = {
        "population": {
            "adult": {"food_per_day": 10},
            "kit": {"food_per_day": 4},
            "bot": {"food_per_day": 0},
        }
    }

    assert calculate_food_per_day(colony, global_data) == 14


def test_bots_do_not_need_food():
    colony = ColonyInputs(adults=0, kits=0, bots=5)
    global_data = load_global_data()

    assert calculate_food_per_day(colony, global_data) == 0


def test_adults_and_kits_need_water():
    colony = ColonyInputs(adults=3, kits=2)
    global_data = load_global_data()

    assert calculate_water_per_day(colony, global_data) == 8


def test_water_per_day_uses_loaded_population_rates():
    colony = ColonyInputs(adults=1, kits=1, bots=1)
    global_data = {
        "population": {
            "adult": {"water_per_day": 12},
            "kit": {"water_per_day": 5},
            "bot": {"water_per_day": 0},
        }
    }

    assert calculate_water_per_day(colony, global_data) == 17


def test_bots_do_not_need_water():
    colony = ColonyInputs(adults=0, kits=0, bots=5)
    global_data = load_global_data()

    assert calculate_water_per_day(colony, global_data) == 0


def test_drought_reserve_includes_safety_buffer():
    colony = ColonyInputs(drought_days=10, safety_buffer=20)

    assert calculate_storage_reserve(daily_need=5, colony=colony) == 60


def test_safety_buffer_multiplier_treats_buffer_as_percentage():
    colony = ColonyInputs(drought_days=4, safety_buffer=50)

    assert calculate_storage_reserve(daily_need=10, colony=colony) == 60


def test_storage_reserve_is_zero_when_drought_days_are_zero():
    colony = ColonyInputs(drought_days=0, safety_buffer=50)

    assert calculate_storage_reserve(daily_need=10, colony=colony) == 0


def test_housing_excludes_bots():
    colony = ColonyInputs(adults=6, kits=3, bots=4)

    assert calculate_housing_need(colony) == 9


def test_bot_support_returns_bot_count():
    colony = ColonyInputs(bots=4)

    result = calculate_bot_support(colony)

    assert result.bot_count == 4


def test_bot_support_returns_placeholder_status_for_bots():
    colony = ColonyInputs(bots=4)

    result = calculate_bot_support(colony)

    assert result.status == "Bot support details are not modelled yet."


def test_bot_support_returns_no_bot_status_for_zero_bots():
    colony = ColonyInputs()

    result = calculate_bot_support(colony)

    assert result.status == "No bots to support yet."


def test_zero_population_returns_zero_needs():
    colony = ColonyInputs()
    global_data = load_global_data()

    assert calculate_food_per_day(colony, global_data) == 0
    assert calculate_water_per_day(colony, global_data) == 0
    assert calculate_storage_reserve(daily_need=0, colony=colony) == 0
    assert calculate_housing_need(colony) == 0
    assert calculate_bot_support(colony).bot_count == 0


# END OF FILE
