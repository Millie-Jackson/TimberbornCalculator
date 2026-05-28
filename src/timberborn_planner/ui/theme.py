"""Timberborn-inspired Gradio theme styling."""

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
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}

#title-box h1 {
    color: #F5F0DC;
    margin-bottom: 8px;
}

#title-box p {
    color: #E6E1D3;
    margin: 0;
}

.output-markdown {
    margin-bottom: 10px;
}

.overview-card {
    background: #12352F;
    border: 1px solid #A68A5E;
    border-radius: 8px;
    padding: 14px;
}

.overview-card h2 {
    color: #F5F0DC;
    font-size: 1.1rem;
    margin: 0 0 4px;
}

.overview-card p {
    color: #D8CBAA;
    margin: 0 0 10px;
}

.overview-card-values {
    display: grid;
    gap: 8px;
}

.overview-card-row {
    align-items: center;
    border-top: 1px solid rgba(166, 138, 94, 0.35);
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding-top: 8px;
}

.overview-card-row span {
    color: #E6E1D3;
}

.overview-card-row strong {
    color: #F5F0DC;
    text-align: right;
}

.overview-card-detail {
    border-top: 1px solid rgba(166, 138, 94, 0.35);
    color: #D8CBAA !important;
    margin-top: 10px !important;
    padding-top: 8px;
}

button {
    background: #A68A5E !important;
    color: #F5F0DC !important;
    border: 1px solid #C2A97A !important;
}
"""

# END OF FILE
