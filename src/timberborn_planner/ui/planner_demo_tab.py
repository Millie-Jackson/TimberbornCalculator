"""Planner Demo tab for the Gradio app."""

from html import escape
from typing import Any

import gradio as gr

from timberborn_planner.models.building import ResourceAmounts
from timberborn_planner.services.loaders import load_faction_data, load_global_data
from timberborn_planner.services.planner import BuildingPlanResult, plan_building_addition
from timberborn_planner.services.summary_text import (
    format_building_plan_summary,
    format_resource_amounts,
)

PlannerDemoSections = tuple[str, str, str, str, str]


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
                summary_output = gr.Markdown(elem_classes=["output-markdown"])
                resources_output = gr.Markdown(elem_classes=["output-markdown"])
                support_output = gr.Markdown(elem_classes=["output-markdown"])
                power_output = gr.Markdown(elem_classes=["output-markdown"])
                notes_output = gr.Markdown(elem_classes=["output-markdown"])

        inputs = [building, quantity]
        outputs = [
            summary_output,
            resources_output,
            support_output,
            power_output,
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
        _summary_section(plan_result),
        _resources_section(plan_result),
        _support_section(plan_result),
        _power_section(plan_result),
        _notes_section(building_data),
    )


def _summary_section(plan_result: BuildingPlanResult) -> str:
    return _planner_card(
        "Summary",
        "Readable planner result.",
        [("Plan", format_building_plan_summary(plan_result))],
    )


def _resources_section(plan_result: BuildingPlanResult) -> str:
    upstream_buildings = "none"
    if plan_result.upstream_buildings:
        upstream_buildings = ", ".join(
            _format_building_id(building_id)
            for building_id in plan_result.upstream_buildings
        )

    rows = [
        (
            "Build resources",
            format_resource_amounts(
                plan_result.upstream_resources.get("construction_cost", {}),
            ),
        ),
        (
            "Science cost",
            format_resource_amounts(
                plan_result.upstream_resources.get("science_cost", {}),
            ),
        ),
        (
            "Run resources",
            format_resource_amounts(
                plan_result.upstream_resources.get("inputs_per_day", {}),
                per_day=True,
            ),
        ),
        ("Upstream buildings", upstream_buildings),
    ]

    return _planner_card("Resources", "Build and operating inputs.", rows)


def _support_section(plan_result: BuildingPlanResult) -> str:
    rows = [
        ("Extra workers", _format_number(plan_result.extra_workers)),
        ("Food / day for workers", _format_number(plan_result.food_per_day_for_workers)),
        ("Water / day for workers", _format_number(plan_result.water_per_day_for_workers)),
    ]

    return _planner_card("Worker Support", "Added colony support burden.", rows)


def _power_section(plan_result: BuildingPlanResult) -> str:
    rows = [
        ("Power required", _format_number(plan_result.power_required)),
        ("Power produced", _format_number(plan_result.power_produced)),
        ("Power balance", _format_number(plan_result.power_balance)),
    ]

    return _planner_card("Power", "Direct power effect.", rows)


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


def _format_building_id(building_id: str) -> str:
    return building_id.replace("_", " ").title()


# END OF FILE
