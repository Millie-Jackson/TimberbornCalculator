"""Wellbeing category helpers."""

from typing import Any

WellbeingCategory = dict[str, Any]
WellbeingCategories = dict[str, WellbeingCategory]


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


# END OF FILE
