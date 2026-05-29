from timberborn_planner.services.loaders import load_faction_data
from timberborn_planner.ui.planner_demo_tab import (
    build_building_choices,
    build_planner_demo_sections,
    default_building_id,
)


def test_building_choices_use_names_as_labels_and_ids_as_values():
    faction_data = load_faction_data("folktails")

    choices = build_building_choices(faction_data)

    assert ("Gear Workshop", "gear_workshop") in choices


def test_default_building_is_gear_workshop_when_available():
    faction_data = load_faction_data("folktails")

    assert default_building_id(faction_data) == "gear_workshop"


def test_planner_demo_sections_focus_on_phase_five_power_outputs():
    sections = build_planner_demo_sections("gear_workshop", 1)
    joined_sections = "\n".join(sections)

    assert len(sections) == 3
    assert "Power Summary" in joined_sections
    assert "Selected building" in joined_sections
    assert "1 Gear Workshop" in joined_sections
    assert "Total required power" in joined_sections
    assert "Total produced power" in joined_sections
    assert "Power balance" in joined_sections
    assert "Status" in joined_sections
    assert "Power deficit: 120" in joined_sections
    assert "Suggested Setup" in joined_sections
    assert "Add 3 Power Wheels to cover a 120 power gap." in joined_sections
    assert "3 Power Wheels (150 power)" in joined_sections
    assert "Notes" in joined_sections
    assert "Build resources" not in joined_sections
    assert "Run resources" not in joined_sections
    assert "Upstream buildings" not in joined_sections
    assert "Extra workers" not in joined_sections
    assert "Food / day for workers" not in joined_sections
    assert "30 planks" not in joined_sections
    assert "10 planks/day" not in joined_sections
    assert "{'planks': 30}" not in joined_sections
    assert "'building_id': 'power_wheel'" not in joined_sections


def test_planner_demo_sections_show_power_generation_surplus():
    sections = build_planner_demo_sections("power_wheel", 2)
    joined_sections = "\n".join(sections)

    assert "2 Power Wheels" in joined_sections
    assert "<span>Total required power</span><strong>0</strong>" in joined_sections
    assert "<span>Total produced power</span><strong>100</strong>" in joined_sections
    assert "<span>Power balance</span><strong>100</strong>" in joined_sections
    assert "Power surplus: 100" in joined_sections
    assert "No extra power setup needed." in joined_sections


# END OF FILE
