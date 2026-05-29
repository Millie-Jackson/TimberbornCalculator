"""Planner Demo tab for the Gradio app."""

from html import escape
from typing import Any

import gradio as gr

from timberborn_planner.advisors.wellbeing_recommendations import (
    WellbeingRecommendation,
    generate_wellbeing_recommendations,
    suggest_service_buildings,
)
from timberborn_planner.calculators.wellbeing import get_wellbeing_categories
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.loaders import load_faction_data, load_global_data

PlannerDemoSections = tuple[str, str, str]


def build_planner_demo_tab() -> None:
    with gr.Tab("Planner Demo"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    adults = gr.Number(
                        label="Adults",
                        value=10,
                        precision=0,
                        minimum=0,
                        step=1,
                    )
                    kits = gr.Number(
                        label="Kits",
                        value=0,
                        precision=0,
                        minimum=0,
                        step=1,
                    )
                    bots = gr.Number(
                        label="Bots",
                        value=0,
                        precision=0,
                        minimum=0,
                        step=1,
                    )
                plan_button = gr.Button("Update planner")

            with gr.Column(scale=2):
                categories_output = gr.Markdown(elem_classes=["output-markdown"])
                service_output = gr.Markdown(elem_classes=["output-markdown"])
                notes_output = gr.Markdown(elem_classes=["output-markdown"])

        inputs = [adults, kits, bots]
        outputs = [
            categories_output,
            service_output,
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
            triggers=[adults.submit, kits.submit, bots.submit],
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


def build_planner_demo_sections(
    adults: int | float | None,
    kits: int | float | None,
    bots: int | float | None,
) -> PlannerDemoSections:
    global_data = load_global_data()
    faction_data = load_faction_data("folktails")
    colony = ColonyInputs(
        adults=_whole_number(adults),
        kits=_whole_number(kits),
        bots=_whole_number(bots),
    )

    return (
        _wellbeing_categories_section(global_data),
        _service_recommendations_section(colony, global_data, faction_data),
        _notes_section(colony, global_data, faction_data),
    )


def _wellbeing_categories_section(global_data: dict[str, Any]) -> str:
    categories = get_wellbeing_categories(global_data)
    rows = [
        (
            str(category_data.get("name", category_id)),
            str(category_data.get("description", "No description yet.")),
        )
        for category_id, category_data in categories.items()
    ]

    return _planner_card(
        "Wellbeing Categories",
        "Internal planner groups for Phase 6 recommendations.",
        rows,
    )


def _service_recommendations_section(
    colony: ColonyInputs,
    global_data: dict[str, Any],
    faction_data: dict[str, Any],
) -> str:
    recommendations = suggest_service_buildings(
        colony=colony,
        global_data=global_data,
        faction_data=faction_data,
    )

    if not recommendations:
        rows = [("Service buildings", "none needed for 0 biological population")]
    else:
        rows = [
            (
                recommendation.building_name or recommendation.building_id or "Service",
                _format_service_recommendation(recommendation),
            )
            for recommendation in recommendations
        ]

    return _planner_card(
        "Service Recommendations",
        "Adults and kits count; bots do not affect these ratios yet.",
        rows,
    )


def _notes_section(
    colony: ColonyInputs,
    global_data: dict[str, Any],
    faction_data: dict[str, Any],
) -> str:
    biological_population = colony.adults + colony.kits
    reminders = [
        recommendation.message
        for recommendation in generate_wellbeing_recommendations(
            colony=colony,
            global_data=global_data,
            faction_data=faction_data,
        )
        if recommendation.building_id is None
    ]
    reminder_text = " ".join(reminders) if reminders else "none"
    rows = [
        ("Biological population", _format_number(biological_population)),
        ("Bots counted for service ratios", "no"),
        ("General reminder", reminder_text),
        ("Data status", "Planning ratios are placeholders until values are verified."),
    ]

    return _planner_card("Notes", "Phase 6 wellbeing demo assumptions.", rows)


def _format_service_recommendation(
    recommendation: WellbeingRecommendation,
) -> str:
    quantity = _format_number(recommendation.required_quantity or 0)
    ratio_text = recommendation.ratio_text or "no ratio"

    return (
        f"{recommendation.category}, quantity {quantity}, "
        f"{ratio_text}. {recommendation.message}"
    )


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


# END OF FILE
