from pathlib import Path
import sys

import gradio as gr

REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"

# Hugging Face Spaces runs app.py from the repo root, so make src imports safe.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from timberborn_planner.ui.overview_tab import build_overview_tab
from timberborn_planner.ui.planner_demo_tab import build_planner_demo_tab
from timberborn_planner.ui.theme import TIMBERBORN_CSS


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Timber Planner") as app:
        gr.Markdown(
            """
            <div id="title-box">
                <h1>Timber Planner</h1>
                <p>Folktails-first colony planning for food, water, droughts, housing, bots and kit growth.</p>
            </div>
            """
        )

        build_overview_tab()
        build_planner_demo_tab()

    return app


demo = build_app()


if __name__ == "__main__":
    demo.launch(css=TIMBERBORN_CSS)


# END OF FILE
