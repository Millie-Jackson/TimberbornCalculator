import pytest

from timberborn_planner.calculators.wellbeing import (
    calculate_required_wellbeing_buildings,
    calculate_service_building_count,
    get_service_rules,
    get_wellbeing_categories,
    get_wellbeing_category,
    get_wellbeing_recommendation_rules,
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


def test_empty_wellbeing_data_returns_empty_categories():
    assert get_wellbeing_categories({"wellbeing": {}}) == {}


def test_missing_wellbeing_data_returns_empty_category_names():
    assert list_wellbeing_category_names({}) == []


def test_malformed_wellbeing_data_raises_clear_value_error():
    with pytest.raises(ValueError, match="wellbeing must be a JSON object"):
        get_wellbeing_categories({"wellbeing": []})


def test_malformed_wellbeing_categories_raise_clear_value_error():
    with pytest.raises(ValueError, match="wellbeing categories must be a JSON object"):
        get_wellbeing_categories({"wellbeing": {"categories": []}})


def test_service_rules_can_be_loaded():
    service_rules = get_service_rules(load_global_data())

    assert {"campsite", "rooftop_terrace", "shrine"} <= service_rules.keys()


def test_missing_wellbeing_data_returns_empty_service_rules():
    assert get_service_rules({}) == {}


def test_empty_wellbeing_data_returns_empty_recommendation_rules():
    assert get_wellbeing_recommendation_rules({"wellbeing": {}}) == {}


def test_ten_population_requires_one_service_building():
    assert calculate_service_building_count(
        population=10,
        population_per_building=10,
    ) == 1


def test_required_building_count_rounds_up():
    assert calculate_required_wellbeing_buildings(
        biological_population=21,
        population_per_building=10,
    ) == 3


def test_eleven_population_requires_two_service_buildings():
    assert calculate_service_building_count(
        population=11,
        population_per_building=10,
    ) == 2


def test_zero_population_requires_zero_service_buildings():
    assert calculate_service_building_count(
        population=0,
        population_per_building=10,
    ) == 0


def test_invalid_population_per_building_raises_value_error():
    with pytest.raises(ValueError, match="population_per_building must be above 0"):
        calculate_required_wellbeing_buildings(
            biological_population=10,
            population_per_building=0,
        )


def test_invalid_service_ratio_raises_value_error():
    with pytest.raises(ValueError, match="population_per_building must be above 0"):
        calculate_service_building_count(
            population=10,
            population_per_building=0,
        )


def test_negative_population_raises_value_error():
    with pytest.raises(ValueError, match="biological_population must be 0 or above"):
        calculate_required_wellbeing_buildings(
            biological_population=-1,
            population_per_building=10,
        )


# END OF FILE
