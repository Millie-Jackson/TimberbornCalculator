import pytest

from timberborn_planner.calculators.wellbeing import (
    calculate_required_wellbeing_buildings,
    generate_wellbeing_recommendations,
    get_wellbeing_categories,
    get_wellbeing_category,
    list_wellbeing_category_names,
    WellbeingRecommendation,
)
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.loaders import load_faction_data, load_global_data


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


def test_zero_population_returns_no_building_recommendations():
    recommendations = generate_wellbeing_recommendations(
        ColonyInputs(),
        load_global_data(),
        load_faction_data("folktails"),
    )

    building_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.building_id is not None
    ]

    assert building_recommendations == []


def test_ten_biological_population_recommends_one_campsite():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.required_quantity == 1


def test_eleven_biological_population_recommends_two_campsites():
    recommendation = _recommendation_for(
        ColonyInputs(adults=11),
        "campsite",
    )

    assert recommendation.required_quantity == 2


def test_bots_do_not_increase_basic_wellbeing_count():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10, bots=20),
        "campsite",
    )

    assert recommendation.required_quantity == 1


def test_kits_increase_basic_wellbeing_count():
    recommendation = _recommendation_for(
        ColonyInputs(adults=9, kits=2),
        "campsite",
    )

    assert recommendation.required_quantity == 2


def test_invalid_population_per_building_raises_value_error():
    with pytest.raises(ValueError, match="population_per_building must be above 0"):
        calculate_required_wellbeing_buildings(
            biological_population=10,
            population_per_building=0,
        )


def test_wellbeing_recommendations_include_category():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.category == "leisure"


def test_wellbeing_recommendations_include_readable_message():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.message == "Add campsites for basic leisure coverage."


def test_missing_building_id_is_handled_safely():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "rooftop_terrace",
    )

    assert recommendation.building_id == "rooftop_terrace"
    assert recommendation.building_name == "Rooftop Terrace"
    assert recommendation.required_quantity == 1


def test_nutrition_recommendation_returns_general_reminder():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        None,
        category="nutrition",
    )

    assert recommendation.required_quantity is None
    assert recommendation.message == (
        "Plan for more than one food type as the colony grows."
    )


def _recommendation_for(
    colony: ColonyInputs,
    building_id: str | None,
    category: str | None = None,
) -> WellbeingRecommendation:
    recommendations = generate_wellbeing_recommendations(
        colony,
        load_global_data(),
        load_faction_data("folktails"),
    )

    for recommendation in recommendations:
        if recommendation.building_id == building_id and (
            category is None or recommendation.category == category
        ):
            return recommendation

    raise AssertionError("Expected wellbeing recommendation was not generated")


# END OF FILE
