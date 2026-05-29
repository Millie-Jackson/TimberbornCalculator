"""Wellbeing category helpers."""

import math
from typing import Any

WellbeingCategory = dict[str, Any]
WellbeingCategories = dict[str, WellbeingCategory]
WellbeingRule = dict[str, Any]
WellbeingRules = dict[str, WellbeingRule]


def get_wellbeing_categories(global_data: dict[str, Any]) -> WellbeingCategories:
    """Return wellbeing categories from global data.

    Missing wellbeing data is treated as an empty category set so older or
    partial data files can still be inspected clearly.
    """

    wellbeing_data = global_data.get("wellbeing", {})
    if not isinstance(wellbeing_data, dict):
        raise ValueError("wellbeing must be a JSON object")

    categories = wellbeing_data.get("categories", {})
    if not isinstance(categories, dict):
        raise ValueError("wellbeing categories must be a JSON object")

    return categories


def get_wellbeing_category(
    global_data: dict[str, Any],
    category_id: str,
) -> WellbeingCategory:
    """Return one wellbeing category by id."""

    categories = get_wellbeing_categories(global_data)

    if category_id not in categories:
        raise ValueError(f"Unknown wellbeing category: {category_id}")

    return categories[category_id]


def list_wellbeing_category_names(global_data: dict[str, Any]) -> list[str]:
    """Return readable wellbeing category names in data order."""

    categories = get_wellbeing_categories(global_data)

    return [
        str(category_data.get("name", category_id))
        for category_id, category_data in categories.items()
    ]


def get_wellbeing_recommendation_rules(global_data: dict[str, Any]) -> WellbeingRules:
    """Return wellbeing recommendation rules from global data."""

    wellbeing_data = global_data.get("wellbeing", {})
    if not isinstance(wellbeing_data, dict):
        raise ValueError("wellbeing must be a JSON object")

    rules = wellbeing_data.get("recommendation_rules", {})
    if not isinstance(rules, dict):
        raise ValueError("wellbeing recommendation rules must be a JSON object")

    return rules


def get_service_rules(global_data: dict[str, Any]) -> WellbeingRules:
    """Return wellbeing service ratio rules from global data."""

    wellbeing_data = global_data.get("wellbeing", {})
    if not isinstance(wellbeing_data, dict):
        raise ValueError("wellbeing must be a JSON object")

    rules = wellbeing_data.get("service_rules", {})
    if not isinstance(rules, dict):
        raise ValueError("wellbeing service rules must be a JSON object")

    return rules


def calculate_required_wellbeing_buildings(
    biological_population: int,
    population_per_building: int | float,
) -> int:
    """Calculate whole wellbeing buildings needed for a population ratio."""

    if biological_population < 0:
        raise ValueError("biological_population must be 0 or above")

    if population_per_building <= 0:
        raise ValueError("population_per_building must be above 0")

    if biological_population == 0:
        return 0

    return math.ceil(biological_population / population_per_building)


def calculate_service_building_count(
    population: int,
    population_per_building: int | float,
) -> int:
    """Calculate whole service buildings needed for a population ratio."""

    return calculate_required_wellbeing_buildings(
        biological_population=population,
        population_per_building=population_per_building,
    )


# END OF FILE
