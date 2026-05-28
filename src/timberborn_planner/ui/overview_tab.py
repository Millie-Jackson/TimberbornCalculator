"""Overview tab for the Gradio app."""

from html import escape
from typing import Any

import gradio as gr

from timberborn_planner.advisors.kit_guidance import calculate_kit_guidance
from timberborn_planner.calculators.bot_support import calculate_bot_support
from timberborn_planner.calculators.food_water import (
    calculate_food_per_day,
    calculate_water_per_day,
)
from timberborn_planner.calculators.housing import calculate_housing_need
from timberborn_planner.calculators.storage import calculate_storage_reserve
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.loaders import load_global_data

OverviewSections = tuple[str, str, str, str, str, str]


def build_overview_tab() -> None:
    with gr.Tab("Overview"):
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("## Population")
                    adults = gr.Number(
                        label="Adult Beavers",
                        value=10,
                        precision=0,
                        minimum=0,
                        step=1,
                        info="Adults are your main workforce.",
                    )
                    kits = gr.Number(
                        label="Kits",
                        value=2,
                        precision=0,
                        minimum=0,
                        step=1,
                        info="Kits increase future growth pressure.",
                    )
                    bots = gr.Number(
                        label="Bots",
                        value=0,
                        precision=0,
                        minimum=0,
                        step=1,
                        info="Bots do not consume food or water.",
                    )

                with gr.Group():
                    gr.Markdown("## Drought Planning")
                    drought_days = gr.Number(
                        label="Drought Days",
                        value=10,
                        precision=0,
                        minimum=0,
                        step=1,
                        info=(
                            "How many days the colony should survive without fresh "
                            "production."
                        ),
                    )
                    safety_buffer = gr.Number(
                        label="Safety Buffer %",
                        value=20,
                        precision=0,
                        minimum=0,
                        step=1,
                        info="Extra reserve added on top of the minimum need.",
                    )
                nerdy_mode = gr.Checkbox(
                    label="Nerdy Mode",
                    value=False,
                    info="Show detailed breakdowns and assumptions.",
                )
                plan_button = gr.Button("Update overview")

            with gr.Column(scale=2):
                population_output = gr.Markdown(elem_classes=["output-markdown"])
                daily_needs_output = gr.Markdown(elem_classes=["output-markdown"])
                drought_reserves_output = gr.Markdown(elem_classes=["output-markdown"])
                housing_output = gr.Markdown(elem_classes=["output-markdown"])
                bots_output = gr.Markdown(elem_classes=["output-markdown"])
                kit_growth_output = gr.Markdown(elem_classes=["output-markdown"])

        inputs = [adults, kits, bots, drought_days, safety_buffer, nerdy_mode]
        outputs = [
            population_output,
            daily_needs_output,
            drought_reserves_output,
            housing_output,
            bots_output,
            kit_growth_output,
        ]

        plan_button.click(
            fn=build_overview_sections,
            inputs=inputs,
            outputs=outputs,
        )

        for input_component in inputs:
            input_component.change(
                fn=build_overview_sections,
                inputs=inputs,
                outputs=outputs,
            )

        gr.on(
            triggers=[adults.submit, kits.submit, bots.submit],
            fn=build_overview_sections,
            inputs=inputs,
            outputs=outputs,
        )

        gr.on(
            triggers=None,
            fn=build_overview_sections,
            inputs=inputs,
            outputs=outputs,
        )


def build_overview_sections(
    adults: int | float | None,
    kits: int | float | None,
    bots: int | float | None,
    drought_days: int | float | None,
    safety_buffer: int | float | None,
    nerdy_mode: bool,
) -> OverviewSections:
    colony = ColonyInputs(
        adults=_whole_number(adults),
        kits=_whole_number(kits),
        bots=_whole_number(bots),
        drought_days=_whole_number(drought_days),
        safety_buffer=_number(safety_buffer),
    )
    global_data = load_global_data()

    food_per_day = calculate_food_per_day(colony, global_data)
    water_per_day = calculate_water_per_day(colony, global_data)
    food_reserve = calculate_storage_reserve(food_per_day, colony)
    water_reserve = calculate_storage_reserve(water_per_day, colony)
    housing_need = calculate_housing_need(colony)
    bot_support = calculate_bot_support(colony)
    kit_guidance = calculate_kit_guidance(colony)

    return (
        _population_section(colony, nerdy_mode),
        _daily_needs_section(food_per_day, water_per_day, colony, global_data, nerdy_mode),
        _drought_reserves_section(food_reserve, water_reserve, colony, nerdy_mode),
        _housing_section(housing_need, nerdy_mode),
        _bots_section(bot_support.bot_count, bot_support.status, nerdy_mode),
        _kit_growth_section(kit_guidance, nerdy_mode),
    )


def _population_section(colony: ColonyInputs, nerdy_mode: bool) -> str:
    rows = [
        ("Total population", str(colony.total_population)),
        ("Working population", str(colony.working_population)),
    ]

    details = []
    if nerdy_mode:
        details.extend(
            [
                f"Adults: {colony.adults}",
                f"Kits: {colony.kits}",
                f"Bots: {colony.bots}",
                f"Colony kit ratio: {_format_percent(colony.kit_ratio)}",
            ]
        )

    return _overview_card("Population", "Colony headcount at a glance.", rows, details)


def _daily_needs_section(
    food_per_day: float,
    water_per_day: float,
    colony: ColonyInputs,
    global_data: dict[str, Any],
    nerdy_mode: bool,
) -> str:
    rows = [
        ("Food / day", _format_number(food_per_day)),
        ("Water / day", _format_number(water_per_day)),
    ]

    details = []
    if nerdy_mode:
        details.extend(
            [
                _consumption_formula(colony, global_data, "food_per_day", "Food"),
                _consumption_formula(colony, global_data, "water_per_day", "Water"),
                "Adults and kits consume food and water; bots currently add 0 to both.",
            ]
        )

    return _overview_card("Daily Needs", "Baseline daily colony demand.", rows, details)


def _drought_reserves_section(
    food_reserve: float,
    water_reserve: float,
    colony: ColonyInputs,
    nerdy_mode: bool,
) -> str:
    rows = [
        ("Food reserve", _format_number(food_reserve)),
        ("Water reserve", _format_number(water_reserve)),
        ("Drought days", str(colony.drought_days)),
        ("Safety buffer", f"{_format_number(colony.safety_buffer)}%"),
    ]

    details = []
    if nerdy_mode:
        multiplier = 1 + colony.safety_buffer / 100
        details.extend(
            [
                f"Drought days: {colony.drought_days}",
                f"Safety buffer percentage: {_format_number(colony.safety_buffer)}%",
                f"Reserve multiplier: {_format_number(multiplier)}",
                "Reserve formula: daily need x drought days x reserve multiplier.",
            ]
        )

    return _overview_card(
        "Drought Reserves",
        "Targets for surviving dry spells.",
        rows,
        details,
    )


def _housing_section(housing_need: int, nerdy_mode: bool) -> str:
    rows = [("Needs housing", str(housing_need))]

    details = []
    if nerdy_mode:
        details.append(
            "Housing formula: adults + kits. Bots are excluded because bot housing is not "
            "modelled in this early slice."
        )

    return _overview_card(
        "Housing",
        "Current biological housing pressure.",
        rows,
        details,
    )


def _bots_section(bot_count: int, status: str, nerdy_mode: bool) -> str:
    rows = [
        ("Bot count", str(bot_count)),
        ("Status", status),
    ]

    details = []
    if nerdy_mode:
        details.append(
            "Bot support is an early placeholder; later planning will add bot-specific "
            "fuel, buildings, and failure warnings."
        )

    return _overview_card("Bots", "Automation population support.", rows, details)


def _kit_growth_section(kit_guidance: Any, nerdy_mode: bool) -> str:
    rows = [
        ("Kit ratio", _format_percent(kit_guidance.kit_ratio)),
        ("Recommended max kits", str(kit_guidance.recommended_max_kits)),
        ("Status", kit_guidance.status),
    ]
    details = [kit_guidance.message]

    if nerdy_mode:
        details.extend(
            [
                f"Current kits: {kit_guidance.current_kits}",
                f"Biological population: {kit_guidance.biological_population}",
                "Thresholds: 0-20% OK, over 20-30% caution, over 30% warning.",
            ]
        )

    return _overview_card("Kit Growth", "Growth pressure and early warnings.", rows, details)


def _consumption_formula(
    colony: ColonyInputs,
    global_data: dict[str, Any],
    rate_name: str,
    label: str,
) -> str:
    adult_rate = _population_rate(global_data, "adult", rate_name)
    kit_rate = _population_rate(global_data, "kit", rate_name)
    bot_rate = _population_rate(global_data, "bot", rate_name)

    return (
        f"{label} formula: adults {colony.adults} x {_format_number(adult_rate)} + "
        f"kits {colony.kits} x {_format_number(kit_rate)} + "
        f"bots {colony.bots} x {_format_number(bot_rate)}."
    )


def _population_rate(
    global_data: dict[str, Any],
    population_type: str,
    rate_name: str,
) -> float:
    return float(global_data["population"][population_type][rate_name])


def _overview_card(
    title: str,
    summary: str,
    rows: list[tuple[str, str]],
    details: list[str] | None = None,
) -> str:
    detail_items = details or []
    row_html = "\n".join(
        (
            '<div class="overview-card-row">'
            f"<span>{escape(label)}</span>"
            f"<strong>{escape(value)}</strong>"
            "</div>"
        )
        for label, value in rows
    )
    details_html = ""

    if detail_items:
        details_html = "\n".join(
            f'<p class="overview-card-detail">{escape(item)}</p>' for item in detail_items
        )

    return (
        '<section class="overview-card">'
        f"<h2>{escape(title)}</h2>"
        f"<p>{escape(summary)}</p>"
        f'<div class="overview-card-values">{row_html}</div>'
        f"{details_html}"
        "</section>"
    )


def _whole_number(value: int | float | None) -> int:
    if value is None:
        return 0

    return int(value)


def _number(value: int | float | None) -> float:
    if value is None:
        return 0

    return float(value)


def _format_number(value: float) -> str:
    if value == int(value):
        return str(int(value))

    return f"{value:.2f}"


def _format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


# END OF FILE
