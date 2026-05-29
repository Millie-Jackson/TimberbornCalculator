# TimberbornCalculator/tests/test_loaders.py

import pytest
from timberborn_planner.services.loaders import (
    load_faction_data,
    load_game_data,
    load_global_data,
    load_patch_meta,
    validate_faction_data,
    validate_global_data,
    validate_patch_meta,
)


# .========================================================================
# BLOCK 1 — Loader tests
# .========================================================================


def test_load_global_data_returns_resources_and_population():

    data = load_global_data()

    assert "resources" in data
    assert "population" in data


def test_load_faction_data_returns_buildings():

    data = load_faction_data("folktails")

    assert "buildings" in data


def test_folktails_starter_buildings_exist():

    data = load_faction_data("folktails")

    expected_buildings = {
        "lumber_mill",
        "gear_workshop",
        "farmhouse",
        "water_pump",
        "small_warehouse",
        "small_water_tank",
        "inventor",
        "power_wheel",
    }

    assert expected_buildings <= data["buildings"].keys()


def test_folktails_starter_buildings_have_names_and_categories():

    data = load_faction_data("folktails")

    for building in data["buildings"].values():
        assert building["name"]
        assert building["category"]


def test_folktails_power_wheel_produces_power():

    data = load_faction_data("folktails")
    power_wheel = data["buildings"]["power_wheel"]

    assert power_wheel["power_required"] == 0
    assert power_wheel["power_produced"] > 0


def test_folktails_gear_workshop_requires_power():

    data = load_faction_data("folktails")
    gear_workshop = data["buildings"]["gear_workshop"]

    assert gear_workshop["power_required"] > 0
    assert gear_workshop["power_produced"] == 0


def test_folktails_inventor_outputs_science():

    data = load_faction_data("folktails")
    inventor = data["buildings"]["inventor"]

    assert inventor["outputs_per_day"]["science"] > 0


def test_folktails_water_pump_outputs_water():

    data = load_faction_data("folktails")
    water_pump = data["buildings"]["water_pump"]

    assert water_pump["outputs_per_day"]["water"] > 0


def test_folktails_storage_buildings_are_marked_as_storage_support():

    data = load_faction_data("folktails")

    for building_id in ["small_warehouse", "small_water_tank"]:
        building = data["buildings"][building_id]

        assert building["category"] == "storage"
        assert "storage" in building["notes"].lower()


def test_load_patch_meta_returns_game_version():

    data = load_patch_meta()

    assert data["game"] == "Timberborn"
    assert data["version"] == "1.0"


def test_load_game_data_returns_combined_sections():

    data = load_game_data("folktails")

    assert "global" in data
    assert "faction" in data
    assert "patch_meta" in data


# .========================================================================
# BLOCK 2 — Validation tests
# .========================================================================


def test_validate_global_data_rejects_missing_population():

    broken_data = {"resources": {}}

    with pytest.raises(ValueError, match="population"):
        validate_global_data(broken_data)


def test_validate_faction_data_rejects_missing_buildings():

    broken_data = {}

    with pytest.raises(ValueError, match="buildings"):
        validate_faction_data(broken_data)


def test_validate_patch_meta_rejects_missing_version():

    broken_data = {
        "game": "Timberborn",
        "faction": "Folktails",
        "notes": "Missing version",
    }

    with pytest.raises(ValueError, match="version"):
        validate_patch_meta(broken_data)


# END OF FILE
