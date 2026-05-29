import pytest

from timberborn_planner.services.dependency_rules import (
    get_building_dependency_summary,
)
from timberborn_planner.services.loaders import load_faction_data, load_global_data


def test_existing_building_returns_expected_summary():
    faction_data = load_faction_data("folktails")
    global_data = load_global_data()

    result = get_building_dependency_summary(
        "gear_workshop",
        faction_data,
        global_data,
    ).to_dict()

    assert result == {
        "building_id": "gear_workshop",
        "name": "Gear Workshop",
        "build": {
            "construction_cost": {"planks": 30},
            "science_cost": {"science": 30},
        },
        "run": {
            "workers": 4,
            "inputs_per_day": {"planks": 10},
            "outputs_per_day": {"gears": 5},
            "power_required": 120,
            "power_produced": 0,
        },
        "support": {
            "workers": 4,
            "food_per_day": 8,
            "water_per_day": 8,
            "housing": 4,
        },
    }


def test_missing_building_raises_value_error():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="Unknown building id: missing_building"):
        get_building_dependency_summary("missing_building", faction_data)


def test_missing_optional_fields_default_safely():
    faction_data = {
        "buildings": {
            "plain_building": {
                "name": "Plain Building",
            }
        }
    }

    result = get_building_dependency_summary("plain_building", faction_data).to_dict()

    assert result["build"]["construction_cost"] == {}
    assert result["build"]["science_cost"] == {}
    assert result["run"]["inputs_per_day"] == {}
    assert result["run"]["outputs_per_day"] == {}
    assert result["run"]["workers"] == 0
    assert result["run"]["power_required"] == 0
    assert result["run"]["power_produced"] == 0
    assert result["support"] == {
        "workers": 0,
        "food_per_day": 0,
        "water_per_day": 0,
        "housing": 0,
    }


def test_construction_cost_is_included():
    faction_data = load_faction_data("folktails")

    result = get_building_dependency_summary("lumber_mill", faction_data)

    assert result.build.construction_cost == {"logs": 20}


def test_science_cost_is_included():
    faction_data = load_faction_data("folktails")

    result = get_building_dependency_summary("lumber_mill", faction_data)

    assert result.build.science_cost == {"science": 20}


def test_workers_are_included():
    faction_data = load_faction_data("folktails")

    result = get_building_dependency_summary("lumber_mill", faction_data)

    assert result.run.workers == 2


def test_power_values_are_included():
    faction_data = load_faction_data("folktails")

    result = get_building_dependency_summary("lumber_mill", faction_data)

    assert result.run.power_required == 50
    assert result.run.power_produced == 0


def test_power_produced_defaults_to_zero_when_missing():
    faction_data = {
        "buildings": {
            "plain_building": {
                "name": "Plain Building",
                "power_required": 5,
            }
        }
    }

    result = get_building_dependency_summary("plain_building", faction_data)

    assert result.run.power_required == 5
    assert result.run.power_produced == 0


def test_inputs_and_outputs_are_included():
    faction_data = load_faction_data("folktails")

    result = get_building_dependency_summary("lumber_mill", faction_data)

    assert result.run.inputs_per_day == {"logs": 10}
    assert result.run.outputs_per_day == {"planks": 5}


def test_worker_support_uses_global_population_rates():
    faction_data = load_faction_data("folktails")
    global_data = {
        "population": {
            "adult": {
                "food_per_day": 3,
                "water_per_day": 4,
            }
        }
    }

    result = get_building_dependency_summary(
        "lumber_mill",
        faction_data,
        global_data,
    )

    assert result.support.food_per_day == 6
    assert result.support.water_per_day == 8
    assert result.support.housing == 2


# END OF FILE
