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


def test_planner_demo_sections_include_summary_and_readable_outputs():
    sections = build_planner_demo_sections("gear_workshop", 1)
    joined_sections = "\n".join(sections)

    assert "Adding 1 Gear Workshop" in joined_sections
    assert "4" in joined_sections
    assert "30 planks" in joined_sections
    assert "10 planks/day" in joined_sections
    assert "Lumber Mill" in joined_sections
    assert "Total required power" in joined_sections
    assert "Total produced power" in joined_sections
    assert "Power deficit: 120" in joined_sections
    assert "Add 3 Power Wheels to cover a 120 power gap." in joined_sections
    assert "{'planks': 30}" not in joined_sections
    assert "'building_id': 'power_wheel'" not in joined_sections


# END OF FILE
