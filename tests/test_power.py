import pytest

from timberborn_planner.calculators.power import (
    calculate_building_power_demand,
    calculate_building_power_generation,
    calculate_power_balance,
    calculate_power_summary,
    calculate_total_power_demand,
    calculate_total_power_generation,
    suggest_power_setup,
)
from timberborn_planner.services.loaders import load_faction_data


def test_one_powered_building_returns_correct_demand():
    building_data = load_faction_data("folktails")["buildings"]["gear_workshop"]

    assert calculate_building_power_demand(building_data, quantity=1) == 120


def test_quantity_multiplies_power_demand():
    building_data = load_faction_data("folktails")["buildings"]["gear_workshop"]

    assert calculate_building_power_demand(building_data, quantity=2) == 240


def test_missing_power_required_defaults_to_zero():
    building_data = {"name": "Plain Building"}

    assert calculate_building_power_demand(building_data, quantity=3) == 0


def test_total_power_demand_sums_multiple_buildings():
    faction_data = load_faction_data("folktails")
    building_quantities = {
        "gear_workshop": 2,
        "lumber_mill": 1,
        "farmhouse": 3,
    }

    assert calculate_total_power_demand(building_quantities, faction_data) == 290


def test_quantity_zero_returns_zero_demand():
    building_data = load_faction_data("folktails")["buildings"]["gear_workshop"]

    assert calculate_building_power_demand(building_data, quantity=0) == 0


def test_negative_quantity_raises_value_error():
    building_data = load_faction_data("folktails")["buildings"]["gear_workshop"]

    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        calculate_building_power_demand(building_data, quantity=-1)


def test_total_power_demand_rejects_negative_quantity():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        calculate_total_power_demand({"gear_workshop": -1}, faction_data)


def test_invalid_building_id_raises_value_error():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="Unknown building id: missing_building"):
        calculate_total_power_demand({"missing_building": 1}, faction_data)


def test_one_power_wheel_produces_power():
    building_data = load_faction_data("folktails")["buildings"]["power_wheel"]

    assert calculate_building_power_generation(building_data, quantity=1) == 50


def test_quantity_multiplies_power_generation():
    building_data = load_faction_data("folktails")["buildings"]["power_wheel"]

    assert calculate_building_power_generation(building_data, quantity=3) == 150


def test_missing_power_produced_defaults_to_zero():
    building_data = {"name": "Plain Building"}

    assert calculate_building_power_generation(building_data, quantity=3) == 0


def test_total_power_generation_sums_multiple_buildings():
    faction_data = load_faction_data("folktails")
    building_quantities = {
        "power_wheel": 2,
        "gear_workshop": 1,
        "small_warehouse": 3,
    }

    assert calculate_total_power_generation(building_quantities, faction_data) == 100


def test_power_balance_is_generation_minus_demand():
    faction_data = load_faction_data("folktails")
    building_quantities = {
        "power_wheel": 3,
        "gear_workshop": 1,
        "lumber_mill": 1,
    }

    assert calculate_power_balance(building_quantities, faction_data) == -20


def test_power_balance_rejects_negative_quantity():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        calculate_power_balance({"power_wheel": -1}, faction_data)


def test_power_balance_rejects_invalid_building_id():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="Unknown building id: missing_building"):
        calculate_power_balance({"missing_building": 1}, faction_data)


def test_power_summary_reports_deficit_when_required_exceeds_produced():
    faction_data = load_faction_data("folktails")

    summary = calculate_power_summary({"gear_workshop": 1}, faction_data)

    assert summary.total_required_power == 120
    assert summary.total_produced_power == 0
    assert summary.power_balance == -120
    assert summary.status == "deficit"
    assert summary.message == "Power deficit: 120"
    assert summary.suggested_setup.message == (
        "Add 3 Power Wheels to cover a 120 power gap."
    )


def test_power_summary_reports_surplus_when_produced_exceeds_required():
    faction_data = load_faction_data("folktails")

    summary = calculate_power_summary({"power_wheel": 2}, faction_data)

    assert summary.total_required_power == 0
    assert summary.total_produced_power == 100
    assert summary.power_balance == 100
    assert summary.status == "surplus"
    assert summary.message == "Power surplus: 100"
    assert summary.suggested_setup.message == "No extra power setup needed."


def test_power_summary_reports_balanced_when_required_matches_produced():
    faction_data = load_faction_data("folktails")

    summary = calculate_power_summary(
        {
            "power_wheel": 1,
            "lumber_mill": 1,
        },
        faction_data,
    )

    assert summary.total_required_power == 50
    assert summary.total_produced_power == 50
    assert summary.power_balance == 0
    assert summary.status == "balanced"
    assert summary.message == "Power is balanced."
    assert summary.suggested_setup.message == "No extra power setup needed."


def test_power_setup_has_no_suggestion_when_power_gap_is_zero():
    faction_data = load_faction_data("folktails")

    setup = suggest_power_setup(0, faction_data)

    assert setup.power_gap == 0
    assert setup.suggestions == []
    assert setup.message == "No extra power setup needed."


def test_power_setup_has_no_suggestion_when_power_gap_is_negative():
    faction_data = load_faction_data("folktails")

    setup = suggest_power_setup(-10, faction_data)

    assert setup.power_gap == 0
    assert setup.suggestions == []
    assert setup.message == "No extra power setup needed."


def test_power_setup_suggests_enough_power_wheels_for_deficit():
    faction_data = load_faction_data("folktails")

    setup = suggest_power_setup(120, faction_data)

    assert setup.power_gap == 120
    assert setup.message == "Add 3 Power Wheels to cover a 120 power gap."
    assert len(setup.suggestions) == 1
    assert setup.suggestions[0].building_id == "power_wheel"
    assert setup.suggestions[0].building_name == "Power Wheel"
    assert setup.suggestions[0].quantity == 3
    assert setup.suggestions[0].power_per_building == 50
    assert setup.suggestions[0].total_power_produced == 150


def test_power_setup_prefers_power_wheel_when_multiple_generators_exist():
    faction_data = {
        "buildings": {
            "windmill": {"name": "Windmill", "power_produced": 100},
            "power_wheel": {"name": "Power Wheel", "power_produced": 50},
        }
    }

    setup = suggest_power_setup(75, faction_data)

    assert setup.suggestions[0].building_id == "power_wheel"
    assert setup.suggestions[0].quantity == 2


def test_power_setup_rounds_up_to_whole_buildings():
    faction_data = load_faction_data("folktails")

    setup = suggest_power_setup(51, faction_data)

    assert setup.suggestions[0].quantity == 2
    assert setup.suggestions[0].total_power_produced == 100


def test_power_setup_ignores_buildings_with_no_power_production():
    faction_data = {
        "buildings": {
            "plain_building": {"name": "Plain Building"},
            "drain": {"name": "Drain", "power_required": 10},
            "tiny_wheel": {"name": "Tiny Wheel", "power_produced": 25},
        }
    }

    setup = suggest_power_setup(50, faction_data)

    assert setup.suggestions[0].building_id == "tiny_wheel"
    assert setup.suggestions[0].quantity == 2


def test_power_setup_handles_no_available_power_producers():
    faction_data = {
        "buildings": {
            "gear_workshop": {"name": "Gear Workshop", "power_required": 120},
            "storage": {"name": "Storage"},
        }
    }

    setup = suggest_power_setup(120, faction_data)

    assert setup.power_gap == 120
    assert setup.suggestions == []
    assert setup.message == (
        "No power-producing buildings are available to cover a 120 power gap."
    )


def test_quantity_zero_returns_zero_generation():
    building_data = load_faction_data("folktails")["buildings"]["power_wheel"]

    assert calculate_building_power_generation(building_data, quantity=0) == 0


def test_power_generation_rejects_negative_quantity():
    building_data = load_faction_data("folktails")["buildings"]["power_wheel"]

    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        calculate_building_power_generation(building_data, quantity=-1)


def test_total_power_generation_rejects_negative_quantity():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="quantity must be 0 or above"):
        calculate_total_power_generation({"power_wheel": -1}, faction_data)


def test_total_power_generation_rejects_invalid_building_id():
    faction_data = load_faction_data("folktails")

    with pytest.raises(ValueError, match="Unknown building id: missing_building"):
        calculate_total_power_generation({"missing_building": 1}, faction_data)


# END OF FILE
