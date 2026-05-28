from timberborn_planner.advisors.kit_guidance import calculate_kit_guidance
from timberborn_planner.models.colony import ColonyInputs


def test_zero_population_returns_zero_recommendation():
    guidance = calculate_kit_guidance(ColonyInputs())

    assert guidance.current_kits == 0
    assert guidance.biological_population == 0
    assert guidance.recommended_max_kits == 0
    assert guidance.kit_ratio == 0
    assert guidance.status == "OK"


def test_ten_adults_and_no_kits_returns_ok():
    guidance = calculate_kit_guidance(ColonyInputs(adults=10, kits=0))

    assert guidance.status == "OK"
    assert guidance.message == "Kit growth looks manageable."


def test_ten_adults_and_two_kits_returns_ok():
    guidance = calculate_kit_guidance(ColonyInputs(adults=10, kits=2))

    assert guidance.kit_ratio == 2 / 12
    assert guidance.status == "OK"


def test_ratio_above_twenty_percent_returns_caution():
    guidance = calculate_kit_guidance(ColonyInputs(adults=10, kits=3))

    assert guidance.kit_ratio == 3 / 13
    assert guidance.status == "caution"
    assert guidance.message == (
        "Kit count is a little high; make sure food, water, and housing can keep up."
    )


def test_ratio_at_twenty_percent_returns_ok():
    guidance = calculate_kit_guidance(ColonyInputs(adults=8, kits=2))

    assert guidance.kit_ratio == 0.2
    assert guidance.status == "OK"


def test_ratio_at_thirty_percent_returns_caution():
    guidance = calculate_kit_guidance(ColonyInputs(adults=7, kits=3))

    assert guidance.kit_ratio == 0.3
    assert guidance.status == "caution"


def test_ratio_above_thirty_percent_returns_warning():
    guidance = calculate_kit_guidance(ColonyInputs(adults=10, kits=5))

    assert guidance.kit_ratio == 5 / 15
    assert guidance.status == "warning"
    assert guidance.message == (
        "Kit count is high; growth may overload food, water, housing, and labour planning."
    )


def test_recommended_max_kits_uses_biological_population():
    guidance = calculate_kit_guidance(ColonyInputs(adults=17, kits=8))

    assert guidance.biological_population == 25
    assert guidance.recommended_max_kits == 5


def test_recommended_max_kits_rounds_down():
    guidance = calculate_kit_guidance(ColonyInputs(adults=12, kits=6))

    assert guidance.biological_population == 18
    assert guidance.recommended_max_kits == 3


def test_bots_do_not_affect_kit_ratio():
    without_bots = calculate_kit_guidance(ColonyInputs(adults=10, kits=3, bots=0))
    with_bots = calculate_kit_guidance(ColonyInputs(adults=10, kits=3, bots=20))

    assert with_bots.biological_population == without_bots.biological_population
    assert with_bots.kit_ratio == without_bots.kit_ratio
    assert with_bots.recommended_max_kits == without_bots.recommended_max_kits


# END OF FILE
