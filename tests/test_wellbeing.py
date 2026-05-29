import pytest

from timberborn_planner.calculators.wellbeing import (
    get_wellbeing_categories,
    get_wellbeing_category,
    list_wellbeing_category_names,
)
from timberborn_planner.services.loaders import load_global_data


EXPECTED_WELLBEING_CATEGORY_IDS = {
    "nutrition",
    "comfort",
    "leisure",
    "spirituality",
    "aesthetics",
    "social",
    "health",
    "safety",
}


def test_wellbeing_categories_can_be_loaded():
    categories = get_wellbeing_categories(load_global_data())

    assert categories
    assert isinstance(categories, dict)


def test_expected_wellbeing_category_ids_exist():
    categories = get_wellbeing_categories(load_global_data())

    assert EXPECTED_WELLBEING_CATEGORY_IDS <= categories.keys()


def test_wellbeing_category_returns_structured_category_data():
    category = get_wellbeing_category(load_global_data(), "leisure")

    assert category["name"] == "Leisure"
    assert category["description"] == "Recreation and free-time activities."
    assert "internal planner grouping" in category["notes"].lower()


def test_wellbeing_category_names_can_be_listed():
    names = list_wellbeing_category_names(load_global_data())

    assert names == [
        "Nutrition",
        "Comfort",
        "Leisure",
        "Spirituality",
        "Aesthetics",
        "Social",
        "Health",
        "Safety",
    ]


def test_missing_wellbeing_category_raises_clear_value_error():
    with pytest.raises(ValueError, match="Unknown wellbeing category: missing"):
        get_wellbeing_category(load_global_data(), "missing")


def test_missing_wellbeing_data_returns_empty_categories():
    assert get_wellbeing_categories({}) == {}


def test_missing_wellbeing_data_returns_empty_category_names():
    assert list_wellbeing_category_names({}) == []


def test_malformed_wellbeing_data_raises_clear_value_error():
    with pytest.raises(ValueError, match="wellbeing must be a JSON object"):
        get_wellbeing_categories({"wellbeing": []})


def test_malformed_wellbeing_categories_raise_clear_value_error():
    with pytest.raises(ValueError, match="wellbeing categories must be a JSON object"):
        get_wellbeing_categories({"wellbeing": {"categories": []}})


# END OF FILE
