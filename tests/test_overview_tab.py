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
    assert '<section class="overview-card">' in sections[0]
    assert "<h2>Population</h2>" in sections[0]
    assert "<span>Total population</span><strong>13</strong>" in sections[0]
    assert "<span>Food / day</span><strong>22</strong>" in sections[1]
    assert "<span>Food reserve</span><strong>132</strong>" in sections[2]
    assert "<span>Drought days</span><strong>5</strong>" in sections[2]
    assert "<span>Safety buffer</span><strong>20%</strong>" in sections[2]
    assert "<span>Needs housing</span><strong>12</strong>" in sections[3]
    assert "<span>Bot count</span><strong>1</strong>" in sections[4]
    assert "<span>Status</span><strong>OK</strong>" in sections[5]
    assert "Reserve multiplier" not in sections[2]
    assert "Food formula" not in sections[1]
    assert "Thresholds" not in sections[5]


def test_overview_sections_include_breakdown_when_nerdy_mode_is_on():
    sections = build_overview_sections(
        adults=10,
        kits=3,
        bots=2,
        drought_days=4,
        safety_buffer=50,
        nerdy_mode=True,
    )

    assert "Adults: 10" in sections[0]
    assert "Food formula: adults 10 x 2 + kits 3 x 1 + bots 2 x 0." in sections[1]
    assert "Water formula: adults 10 x 2 + kits 3 x 1 + bots 2 x 0." in sections[1]
    assert "Adults and kits consume food and water" in sections[1]
    assert "Reserve multiplier: 1.50" in sections[2]
    assert "Reserve formula: daily need x drought days x reserve multiplier." in sections[2]
    assert "Housing formula: adults + kits." in sections[3]
    assert "Bot support is an early placeholder" in sections[4]
    assert "<span>Recommended max kits</span><strong>2</strong>" in sections[5]
    assert "<span>Status</span><strong>caution</strong>" in sections[5]
    assert "Thresholds: 0-20% OK, over 20-30% caution, over 30% warning." in sections[5]


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
