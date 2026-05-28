import pytest

from timberborn_planner.ui.overview_tab import build_overview_sections


def test_overview_sections_return_short_summary_when_nerdy_mode_is_off():
    sections = build_overview_sections(
        adults=10,
        kits=2,
        bots=1,
        drought_days=5,
        safety_buffer=20,
        nerdy_mode=False,
    )

    assert len(sections) == 6
    assert "Total population: **13**" in sections[0]
    assert "Food per day: **22**" in sections[1]
    assert "Food reserve: **132**" in sections[2]
    assert "Biological population needing housing: **12**" in sections[3]
    assert "Bot count: **1**" in sections[4]
    assert "Status: **OK**" in sections[5]
    assert "Reserve multiplier" not in sections[2]


def test_overview_sections_include_breakdown_when_nerdy_mode_is_on():
    sections = build_overview_sections(
        adults=10,
        kits=3,
        bots=2,
        drought_days=4,
        safety_buffer=50,
        nerdy_mode=True,
    )

    assert "Adults: **10**" in sections[0]
    assert "Adults and kits consume food and water; bots do not." in sections[1]
    assert "Reserve multiplier: **1.50**" in sections[2]
    assert "Recommended max kits: **2**" in sections[5]
    assert "Status: **caution**" in sections[5]


def test_overview_sections_reject_negative_inputs():
    with pytest.raises(ValueError, match="adults"):
        build_overview_sections(
            adults=-1,
            kits=0,
            bots=0,
            drought_days=0,
            safety_buffer=0,
            nerdy_mode=False,
        )


# END OF FILE
