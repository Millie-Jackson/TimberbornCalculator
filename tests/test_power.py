import pytest

from timberborn_planner.calculators.power import (
    calculate_building_power_demand,
    calculate_building_power_generation,
    calculate_power_balance,
    calculate_power_summary,
    calculate_total_power_demand,
    calculate_total_power_generation,
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


def test_power_summary_reports_deficit_when_required_exceeds_produced():
    faction_data = load_faction_data("folktails")

    summary = calculate_power_summary({"gear_workshop": 1}, faction_data)

    assert summary.total_required_power == 120
    assert summary.total_produced_power == 0
    assert summary.power_balance == -120
    assert summary.status == "deficit"
    assert summary.message == "Power deficit: 120"


def test_power_summary_reports_surplus_when_produced_exceeds_required():
    faction_data = load_faction_data("folktails")

    summary = calculate_power_summary({"power_wheel": 2}, faction_data)

    assert summary.total_required_power == 0
    assert summary.total_produced_power == 100
    assert summary.power_balance == 100
    assert summary.status == "surplus"
    assert summary.message == "Power surplus: 100"


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
