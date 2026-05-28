"""Overview tab for the Gradio app."""

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
                adults = gr.Number(label="Adult beavers", value=10, precision=0)
                kits = gr.Number(label="Kits", value=2, precision=0)
                bots = gr.Number(label="Bots", value=0, precision=0)
                drought_days = gr.Number(label="Drought days", value=5, precision=0)
                safety_buffer = gr.Number(
                    label="Safety buffer percentage",
                    value=20,
                    precision=0,
                )
                nerdy_mode = gr.Checkbox(label="Nerdy Mode", value=False)
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
        _daily_needs_section(food_per_day, water_per_day, nerdy_mode),
        _drought_reserves_section(food_reserve, water_reserve, colony, nerdy_mode),
        _housing_section(housing_need, nerdy_mode),
        _bots_section(bot_support.bot_count, bot_support.status, nerdy_mode),
        _kit_growth_section(kit_guidance, nerdy_mode),
    )


def _population_section(colony: ColonyInputs, nerdy_mode: bool) -> str:
    lines = [
        "## Population",
        f"Total population: **{colony.total_population}**",
        f"Working population: **{colony.working_population}**",
    ]

    if nerdy_mode:
        lines.extend(
            [
                "",
                f"Adults: **{colony.adults}**",
                f"Kits: **{colony.kits}**",
                f"Bots: **{colony.bots}**",
                f"Colony kit ratio: **{_format_percent(colony.kit_ratio)}**",
            ]
        )

    return "\n\n".join(lines)


def _daily_needs_section(
    food_per_day: float,
    water_per_day: float,
    nerdy_mode: bool,
) -> str:
    lines = [
        "## Daily Needs",
        f"Food per day: **{_format_number(food_per_day)}**",
        f"Water per day: **{_format_number(water_per_day)}**",
    ]

    if nerdy_mode:
        lines.append("")
        lines.append("Adults and kits consume food and water; bots do not.")

    return "\n\n".join(lines)


def _drought_reserves_section(
    food_reserve: float,
    water_reserve: float,
    colony: ColonyInputs,
    nerdy_mode: bool,
) -> str:
    lines = [
        "## Drought Reserves",
        f"Food reserve: **{_format_number(food_reserve)}**",
        f"Water reserve: **{_format_number(water_reserve)}**",
    ]

    if nerdy_mode:
        multiplier = 1 + colony.safety_buffer / 100
        lines.extend(
            [
                "",
                f"Drought days: **{colony.drought_days}**",
                f"Safety buffer: **{_format_number(colony.safety_buffer)}%**",
                f"Reserve multiplier: **{_format_number(multiplier)}**",
            ]
        )

    return "\n\n".join(lines)


def _housing_section(housing_need: int, nerdy_mode: bool) -> str:
    lines = [
        "## Housing",
        f"Biological population needing housing: **{housing_need}**",
    ]

    if nerdy_mode:
        lines.append("")
        lines.append("Housing currently counts adults and kits, excluding bots.")

    return "\n\n".join(lines)


def _bots_section(bot_count: int, status: str, nerdy_mode: bool) -> str:
    lines = [
        "## Bots",
        f"Bot count: **{bot_count}**",
        status,
    ]

    if nerdy_mode:
        lines.append("")
        lines.append("Bot-specific support will be expanded in a later planning step.")

    return "\n\n".join(lines)


def _kit_growth_section(kit_guidance: Any, nerdy_mode: bool) -> str:
    lines = [
        "## Kit Growth",
        f"Status: **{kit_guidance.status}**",
        kit_guidance.message,
    ]

    if nerdy_mode:
        lines.extend(
            [
                "",
                f"Current kits: **{kit_guidance.current_kits}**",
                f"Biological population: **{kit_guidance.biological_population}**",
                f"Recommended max kits: **{kit_guidance.recommended_max_kits}**",
                f"Kit ratio: **{_format_percent(kit_guidance.kit_ratio)}**",
            ]
        )

    return "\n\n".join(lines)


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
