from timberborn_planner.services.loaders import load_faction_data, load_global_data
from timberborn_planner.services.planner import plan_building_addition
from timberborn_planner.services.summary_text import (
    format_building_plan_summary,
    format_power_summary,
    format_resource_amounts,
)


def test_empty_resources_return_none():
    assert format_resource_amounts({}) == "none"


def test_resource_amounts_format_readably():
    assert format_resource_amounts({"logs": 20, "planks": 5}) == "20 logs and 5 planks"


def test_gear_workshop_summary_includes_workers():
    summary = _gear_workshop_summary()

    assert "4 extra workers" in summary


def test_gear_workshop_summary_includes_build_cost():
    summary = _gear_workshop_summary()

    assert "30 planks to build" in summary


def test_gear_workshop_summary_includes_run_inputs():
    summary = _gear_workshop_summary()

    assert "10 planks/day to run" in summary


def test_gear_workshop_summary_includes_food_and_water_support():
    summary = _gear_workshop_summary()

    assert "8 food/day" in summary
    assert "8 water/day" in summary


def test_gear_workshop_summary_includes_power_requirement():
    summary = _gear_workshop_summary()

    assert "Power required: 120." in summary


def test_upstream_dependencies_are_included():
    summary = _gear_workshop_summary()

    assert "It also depends on: Lumber Mill." in summary


def test_power_gap_is_included_when_power_balance_is_negative():
    plan_result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    assert "Power gap: 120." in format_power_summary(plan_result)


def test_quantity_greater_than_one_reads_sensibly():
    plan_result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
        quantity=2,
    )

    summary = format_building_plan_summary(plan_result)

    assert "Adding 2 Gear Workshops" in summary
    assert "8 extra workers" in summary
    assert "60 planks to build" in summary


def _gear_workshop_summary() -> str:
    plan_result = plan_building_addition(
        load_faction_data("folktails"),
        load_global_data(),
        "gear_workshop",
    )

    return format_building_plan_summary(plan_result)


# END OF FILE
