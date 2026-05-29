from timberborn_planner.ui.planner_demo_tab import build_planner_demo_sections


def test_planner_demo_sections_focus_on_phase_six_wellbeing_outputs():
    sections = build_planner_demo_sections(10, 0, 0)
    joined_sections = "\n".join(sections)

    assert len(sections) == 3
    assert "Wellbeing Categories" in joined_sections
    assert "Service Recommendations" in joined_sections
    assert "Notes" in joined_sections
    assert "Nutrition" in joined_sections
    assert "Leisure" in joined_sections
    assert "campsite" in joined_sections
    assert "quantity 1" in joined_sections
    assert "1 per 10 biological population" in joined_sections
    assert "Add campsites for basic leisure coverage." in joined_sections
    assert "Power Summary" not in joined_sections
    assert "Total required power" not in joined_sections
    assert "Power deficit" not in joined_sections
    assert "Suggested Setup" not in joined_sections
    assert "Build resources" not in joined_sections
    assert "Run resources" not in joined_sections
    assert "Upstream buildings" not in joined_sections


def test_planner_demo_kits_increase_service_recommendations():
    sections = build_planner_demo_sections(10, 1, 0)
    joined_sections = "\n".join(sections)

    assert "Biological population</span><strong>11</strong>" in joined_sections
    assert "<span>campsite</span><strong>leisure, quantity 2" in joined_sections
    assert "<span>rooftop_terrace</span><strong>comfort, quantity 2" in joined_sections


def test_planner_demo_bots_do_not_increase_service_recommendations():
    sections = build_planner_demo_sections(10, 0, 10)
    joined_sections = "\n".join(sections)

    assert "Biological population</span><strong>10</strong>" in joined_sections
    assert "Bots counted for service ratios</span><strong>no</strong>" in joined_sections
    assert "<span>campsite</span><strong>leisure, quantity 1" in joined_sections
    assert "<span>rooftop_terrace</span><strong>comfort, quantity 1" in joined_sections


def test_planner_demo_zero_biological_population_has_no_service_recommendations():
    sections = build_planner_demo_sections(0, 0, 10)
    joined_sections = "\n".join(sections)

    assert "none needed for 0 biological population" in joined_sections
    assert "Biological population</span><strong>0</strong>" in joined_sections


# END OF FILE
