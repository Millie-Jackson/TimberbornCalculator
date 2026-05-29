import pytest

from timberborn_planner.calculators.power import (
    calculate_building_power_demand,
    calculate_total_power_demand,
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


# END OF FILE
