import pytest

from timberborn_planner.services.loaders import load_faction_data, load_global_data
from timberborn_planner.services.planner import plan_building_addition


def test_adding_one_gear_workshop_returns_extra_worker_count():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert result.extra_workers == 4


def test_quantity_two_multiplies_workers_and_power():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
        quantity=2,
    )

    assert result.extra_workers == 8
    assert result.power_required == 240
    assert result.power_produced == 0


def test_construction_costs_are_included():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert result.upstream_resources["construction_cost"] == {"planks": 30}
    assert result.upstream_resources["science_cost"] == {"science": 30}


def test_operating_inputs_are_included():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert result.upstream_resources["inputs_per_day"] == {"planks": 10}


def test_upstream_dependencies_are_returned_if_present():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert result.upstream_buildings == ["lumber_mill"]


def test_food_and_water_for_workers_use_adult_consumption():
    faction_data = load_faction_data("folktails")
    global_data = {
        "population": {
            "adult": {"food_per_day": 3, "water_per_day": 4},
            "kit": {"food_per_day": 1, "water_per_day": 1},
            "bot": {"food_per_day": 0, "water_per_day": 0},
        }
    }

    result = plan_building_addition(
        faction_data,
        global_data,
        "gear_workshop",
    )

    assert result.food_per_day_for_workers == 12
    assert result.water_per_day_for_workers == 16


def test_power_required_is_returned():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert result.power_required == 120


def test_power_produced_defaults_to_zero_when_missing():
    faction_data = {
        "buildings": {
            "plain_building": {
                "name": "Plain Building",
                "workers": 1,
                "power_required": 5,
            }
        }
    }

    result = plan_building_addition(
        faction_data,
        load_global_data(),
        "plain_building",
    )

    assert result.power_produced == 0


def test_power_balance_is_calculated():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "power_wheel",
        quantity=2,
    )

    assert result.power_required == 0
    assert result.power_produced == 100
    assert result.power_balance == 100


def test_invalid_building_id_raises_clear_value_error():
    with pytest.raises(ValueError, match="Unknown building id: missing_building"):
        plan_building_addition(
            load_faction_data("folktails"),
            load_global_data(),
            "missing_building",
        )


def test_negative_quantity_raises_clear_value_error():
    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        plan_building_addition(
            load_faction_data("folktails"),
            load_global_data(),
            "gear_workshop",
            quantity=-1,
        )


def test_quantity_zero_returns_zero_requirements():
    result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
        quantity=0,
    )

    assert result.extra_workers == 0
    assert result.upstream_resources["construction_cost"] == {"planks": 0}
    assert result.upstream_resources["science_cost"] == {"science": 0}
    assert result.upstream_resources["inputs_per_day"] == {"planks": 0}
    assert result.food_per_day_for_workers == 0
    assert result.water_per_day_for_workers == 0
    assert result.power_required == 0
    assert result.power_produced == 0
    assert result.power_balance == 0


# END OF FILE
