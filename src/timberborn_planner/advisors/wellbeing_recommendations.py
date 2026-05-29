"""Wellbeing recommendation helpers."""

from dataclasses import dataclass
from typing import Any

from timberborn_planner.calculators.wellbeing import (
    calculate_service_building_count,
    get_service_rules,
    get_wellbeing_recommendation_rules,
    WellbeingRule,
)
from timberborn_planner.models.colony import ColonyInputs


@dataclass(frozen=True)
class WellbeingRecommendation:
    """One first-pass wellbeing recommendation."""

    category: str
    building_id: str | None
    building_name: str | None
    required_quantity: int | None
    message: str
    ratio_text: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, int | str | None]:
        return {
            "category": self.category,
            "building_id": self.building_id,
            "building_name": self.building_name,
            "required_quantity": self.required_quantity,
            "ratio_text": self.ratio_text,
            "message": self.message,
            "notes": self.notes,
        }


def suggest_service_buildings(
    colony: ColonyInputs,
    global_data: dict[str, Any],
    faction_data: dict[str, Any],
) -> list[WellbeingRecommendation]:
    """Suggest simple wellbeing service buildings from population ratios."""

    biological_population = colony.adults + colony.kits
    if biological_population == 0:
        return []

    recommendations: list[WellbeingRecommendation] = []
    service_rules = get_service_rules(global_data)

    for rule_id, rule_data in service_rules.items():
        if rule_data.get("applies_to", "biological_population") != (
            "biological_population"
        ):
            continue

        recommendations.append(
            _build_service_recommendation(
                rule_id=rule_id,
                rule_data=rule_data,
                biological_population=biological_population,
                faction_data=faction_data,
            )
        )

    return recommendations


def generate_wellbeing_recommendations(
    colony: ColonyInputs,
    global_data: dict[str, Any],
    faction_data: dict[str, Any],
) -> list[WellbeingRecommendation]:
    """Generate simple wellbeing recommendations from biological population."""

    rules = get_wellbeing_recommendation_rules(global_data)
    recommendations = [
        _build_general_recommendation(rule_id, rule_data)
        for rule_id, rule_data in rules.items()
    ]

    recommendations.extend(
        suggest_service_buildings(
            colony=colony,
            global_data=global_data,
            faction_data=faction_data,
        )
    )

    return recommendations


def _build_general_recommendation(
    rule_id: str,
    rule_data: WellbeingRule,
) -> WellbeingRecommendation:
    category = str(rule_data.get("category", "uncategorised"))
    message = str(rule_data.get("message", "Review wellbeing support."))
    notes = rule_data.get("notes")

    return WellbeingRecommendation(
        category=category,
        building_id=None,
        building_name=None,
        required_quantity=None,
        message=message,
        notes=_format_notes(notes),
    )


def _build_service_recommendation(
    rule_id: str,
    rule_data: WellbeingRule,
    biological_population: int,
    faction_data: dict[str, Any],
) -> WellbeingRecommendation:
    category = str(rule_data.get("category", "uncategorised"))
    message = str(rule_data.get("message", "Review wellbeing support."))
    notes = rule_data.get("notes")
    building_id = str(rule_data.get("building_id", rule_id))
    population_per_building = rule_data["population_per_building"]
    required_quantity = calculate_service_building_count(
        population=biological_population,
        population_per_building=population_per_building,
    )

    return WellbeingRecommendation(
        category=category,
        building_id=building_id,
        building_name=_get_building_name(building_id, faction_data),
        required_quantity=required_quantity,
        message=message,
        ratio_text=_format_ratio_text(population_per_building),
        notes=_format_notes(notes),
    )


def _get_building_name(building_id: str, faction_data: dict[str, Any]) -> str:
    building_data = faction_data.get("buildings", {}).get(building_id, {})

    return str(building_data.get("name", building_id))


def _format_ratio_text(population_per_building: int | float) -> str:
    ratio = _format_number(population_per_building)

    return f"1 per {ratio} biological population"


def _format_number(value: int | float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _format_notes(notes: object) -> str | None:
    if notes is None:
        return None

    if isinstance(notes, list):
        return " ".join(str(note) for note in notes)

    return str(notes)


# END OF FILE
