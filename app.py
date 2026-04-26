# TimberbornCalculator/app.py

import gradio as gr


TIMBERBORN_CSS = """
body {
    background: #1F4B45;
}

.gradio-container {
    background: #1F4B45;
    color: #E6E1D3;
}

#title-box {
    background: #12352F;
    border: 2px solid #A68A5E;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

button {
    background: #A68A5E !important;
    color: #F5F0DC !important;
    border: 1px solid #C2A97A !important;
}
"""


def placeholder_colony_summary(adults: int, kits: int, bots: int) -> str:

    total = adults + kits + bots

    return (
        f"## Colony Summary\n\n"
        f"- Adult beavers: **{adults}**\n"
        f"- Kits: **{kits}**\n"
        f"- Bots: **{bots}**\n"
        f"- Total population: **{total}**\n\n"
        f"Planner logic coming soon. The beavers are sharpening pencils."
    )


with gr.Blocks(css=TIMBERBORN_CSS, title="Timberlator (timberborn calculator)") as demo:
    gr.Markdown(
        """
            <div id="title-box">
                <h1>Timberborn Colony Planner</h1>
                <p>Folktails-first colony planning tool for food, water, power, science and chaos.</p>
            </div>
            """
    )

    with gr.Row():
        adults = gr.Number(label="Adult beavers", value=10, precision=0)
        kits = gr.Number(label="Kits", value=2, precision=0)
        bots = gr.Number(label="Bots", value=0, precision=0)

    button = gr.Button("Plan colony")
    output = gr.Markdown()

    button.click(
        fn=placeholder_colony_summary,
        inputs=[adults, kits, bots],
        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()
