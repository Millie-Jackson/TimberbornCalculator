# TimberbornCalculator/tests/test_loaders.py

from timberborn_planner.services.loaders import (
    load_faction_data,
    load_game_data,
    load_global_data,
    load_patch_meta,
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


def test_load_patch_meta_returns_game_version():

    data = load_patch_meta()

    assert data["game"] == "Timberborn"
    assert data["version"] == "1.0"


def test_load_game_data_returns_combined_sections():

    data = load_game_data("folktails")

    assert "global" in data
    assert "faction" in data
    assert "patch_meta" in data


# END OF FILE
