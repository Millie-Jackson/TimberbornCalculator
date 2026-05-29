from timberborn_planner.advisors.wellbeing_recommendations import (
    generate_wellbeing_recommendations,
    suggest_service_buildings,
    WellbeingRecommendation,
)
from timberborn_planner.models.colony import ColonyInputs
from timberborn_planner.services.loaders import load_faction_data, load_global_data


def test_zero_biological_population_returns_no_service_recommendations():
    recommendations = suggest_service_buildings(
        ColonyInputs(),
        load_global_data(),
        load_faction_data("folktails"),
    )

    assert recommendations == []


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


def test_twenty_biological_population_recommends_one_shrine():
    recommendation = _recommendation_for(
        ColonyInputs(adults=20),
        "shrine",
    )

    assert recommendation.required_quantity == 1


def test_bots_do_not_increase_service_recommendations():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10, bots=20),
        "campsite",
    )

    assert recommendation.required_quantity == 1


def test_kits_increase_service_recommendations():
    recommendation = _recommendation_for(
        ColonyInputs(adults=9, kits=2),
        "campsite",
    )

    assert recommendation.required_quantity == 2


def test_service_recommendations_include_category():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.category == "leisure"


def test_service_recommendations_include_readable_message():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.message == "Add campsites for basic leisure coverage."


def test_missing_building_name_falls_back_to_building_id():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "rooftop_terrace",
    )

    assert recommendation.building_id == "rooftop_terrace"
    assert recommendation.building_name == "rooftop_terrace"
    assert recommendation.required_quantity == 1


def test_service_recommendation_ratio_text_is_readable():
    recommendation = _recommendation_for(
        ColonyInputs(adults=10),
        "campsite",
    )

    assert recommendation.ratio_text == "1 per 10 biological population"


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


def test_generate_wellbeing_recommendations_includes_service_recommendations():
    recommendations = generate_wellbeing_recommendations(
        ColonyInputs(adults=10),
        load_global_data(),
        load_faction_data("folktails"),
    )

    assert any(
        recommendation.building_id == "campsite"
        for recommendation in recommendations
    )


def _recommendation_for(
    colony: ColonyInputs,
    building_id: str | None,
    category: str | None = None,
) -> WellbeingRecommendation:
    recommendations = suggest_service_buildings(
        colony,
        load_global_data(),
        load_faction_data("folktails"),
    )

    if building_id is None:
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
