import pytest

from timberborn_planner.models.colony import ColonyInputs


def test_total_population_includes_adults_kits_and_bots():
    colony = ColonyInputs(adults=10, kits=3, bots=2)

    assert colony.total_population == 15


def test_working_population_includes_adults_and_bots_only():
    colony = ColonyInputs(adults=10, kits=3, bots=2)

    assert colony.working_population == 12


def test_kit_ratio_uses_total_population():
    colony = ColonyInputs(adults=7, kits=3, bots=0)

    assert colony.kit_ratio == 0.3


def test_default_values_describe_an_empty_colony():
    colony = ColonyInputs()

    assert colony.adults == 0
    assert colony.kits == 0
    assert colony.bots == 0
    assert colony.drought_days == 0
    assert colony.safety_buffer == 0
    assert colony.total_population == 0
    assert colony.working_population == 0
    assert colony.kit_ratio == 0


def test_validation_rejects_negative_adults():
    with pytest.raises(ValueError, match="adults"):
        ColonyInputs(adults=-1)


def test_validation_rejects_negative_kits():
    with pytest.raises(ValueError, match="kits"):
        ColonyInputs(kits=-1)


def test_validation_rejects_negative_bots():
    with pytest.raises(ValueError, match="bots"):
        ColonyInputs(bots=-1)


def test_validation_rejects_negative_drought_days():
    with pytest.raises(ValueError, match="drought_days"):
        ColonyInputs(drought_days=-1)


def test_validation_rejects_negative_safety_buffer():
    with pytest.raises(ValueError, match="safety_buffer"):
        ColonyInputs(safety_buffer=-1)


# END OF FILE
