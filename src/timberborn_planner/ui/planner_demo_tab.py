"""Planner Demo tab for the Gradio app."""

from html import escape
from typing import Any

import gradio as gr

from timberborn_planner.calculators.power import PowerSetupSuggestion
from timberborn_planner.services.loaders import load_faction_data, load_global_data
from timberborn_planner.services.planner import BuildingPlanResult, plan_building_addition
from timberborn_planner.services.summary_text import format_power_summary

PlannerDemoSections = tuple[str, str, str]


def build_planner_demo_tab() -> None:
    faction_data = load_faction_data("folktails")
    building_choices = build_building_choices(faction_data)
    default_building = default_building_id(faction_data)

    with gr.Tab("Planner Demo"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    building = gr.Dropdown(
                        label="Building",
                        choices=building_choices,
                        value=default_building,
                    )
                    quantity = gr.Number(
                        label="Quantity",
                        value=1,
                        precision=0,
                        minimum=0,
                        step=1,
                    )
                plan_button = gr.Button("Update planner")

            with gr.Column(scale=2):
                power_summary_output = gr.Markdown(elem_classes=["output-markdown"])
                suggested_setup_output = gr.Markdown(elem_classes=["output-markdown"])
                notes_output = gr.Markdown(elem_classes=["output-markdown"])

        inputs = [building, quantity]
        outputs = [
            power_summary_output,
            suggested_setup_output,
            notes_output,
        ]

        plan_button.click(
            fn=build_planner_demo_sections,
            inputs=inputs,
            outputs=outputs,
        )

        for input_component in inputs:
            input_component.change(
                fn=build_planner_demo_sections,
                inputs=inputs,
                outputs=outputs,
            )

        gr.on(
            triggers=[quantity.submit],
            fn=build_planner_demo_sections,
            inputs=inputs,
            outputs=outputs,
        )

        gr.on(
            triggers=None,
            fn=build_planner_demo_sections,
            inputs=inputs,
            outputs=outputs,
        )


def build_building_choices(
    faction_data: dict[str, Any],
) -> list[tuple[str, str]]:
    buildings = faction_data["buildings"]

    return [
        (str(building_data.get("name", building_id)), building_id)
        for building_id, building_data in buildings.items()
    ]


def default_building_id(faction_data: dict[str, Any]) -> str:
    buildings = faction_data["buildings"]

    if "gear_workshop" in buildings:
        return "gear_workshop"

    return next(iter(buildings))


def build_planner_demo_sections(
    building_id: str,
    quantity: int | float | None,
) -> PlannerDemoSections:
    faction_data = load_faction_data("folktails")
    global_data = load_global_data()
    clean_quantity = _whole_number(quantity)
    plan_result = plan_building_addition(
        faction_data=faction_data,
        global_data=global_data,
        building_id=building_id,
        quantity=clean_quantity,
    )
    building_data = faction_data["buildings"][building_id]

    return (
        _power_summary_section(plan_result),
        _suggested_setup_section(plan_result),
        _notes_section(building_data),
    )


def _power_summary_section(plan_result: BuildingPlanResult) -> str:
    selected_building = _format_building_quantity(
        plan_result.quantity,
        plan_result.building_name,
    )
    return _planner_card(
        "Power Summary",
        "Phase 5 power totals for the selected building.",
        [
            ("Selected building", selected_building),
            ("Total required power", _format_number(plan_result.power_required)),
            ("Total produced power", _format_number(plan_result.power_produced)),
            ("Power balance", _format_number(plan_result.power_balance)),
            ("Status", plan_result.power_status),
            ("Summary", format_power_summary(plan_result)),
        ],
    )


def _suggested_setup_section(plan_result: BuildingPlanResult) -> str:
    setup = plan_result.suggested_power_setup
    rows = [
        ("Power gap", _format_number(setup.power_gap)),
        ("Recommendation", setup.message),
    ]

    if setup.suggestions:
        suggestion_text = ", ".join(
            _format_power_suggestion(suggestion)
            for suggestion in setup.suggestions
        )
        rows.append(("Suggested buildings", suggestion_text))

    return _planner_card("Suggested Setup", "Simple Folktails power coverage.", rows)


def _format_power_suggestion(suggestion: PowerSetupSuggestion) -> str:
    return (
        f"{_format_building_quantity(suggestion.quantity, suggestion.building_name)} "
        f"({_format_number(suggestion.total_power_produced)} power)"
    )


def _notes_section(building_data: dict[str, Any]) -> str:
    note = str(building_data.get("notes", "Values are still being refined."))

    if "placeholder" not in note.lower():
        note = f"{note} Values are still being refined."

    return _planner_card("Notes", "Data confidence.", [("Current note", note)])


def _planner_card(
    title: str,
    summary: str,
    rows: list[tuple[str, str]],
) -> str:
    row_html = "\n".join(
        (
            '<div class="overview-card-row">'
            f"<span>{escape(label)}</span>"
            f"<strong>{escape(value)}</strong>"
            "</div>"
        )
        for label, value in rows
    )

    return (
        '<section class="overview-card">'
        f"<h2>{escape(title)}</h2>"
        f"<p>{escape(summary)}</p>"
        f'<div class="overview-card-values">{row_html}</div>'
        "</section>"
    )


def _whole_number(value: int | float | None) -> int:
    if value is None:
        return 0

    return int(value)


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _format_building_quantity(quantity: int, building_name: str) -> str:
    if quantity == 1:
        return f"1 {building_name}"

    return f"{quantity} {_pluralise_name(building_name)}"


def _pluralise_name(name: str) -> str:
    if name.endswith("s"):
        return name

    return f"{name}s"


# END OF FILE
