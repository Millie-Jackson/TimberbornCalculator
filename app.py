import gradio as gr

from timberborn_planner.ui.overview_tab import build_overview_tab
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

    return app


demo = build_app()


if __name__ == "__main__":
    demo.launch(css=TIMBERBORN_CSS)


# END OF FILE
