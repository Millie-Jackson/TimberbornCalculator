# AGENTS.md

## Project
Timberborn Calculator / Colony Planner

A Python + Gradio web app for Timberborn 1.0 planning.
This project is a colony planner, not just a simple calculator.

The app should support:
- Folktails first
- mixed populations: adult beavers, kits, and bots
- food, water, storage, and drought planning
- dependency expansion for buildings
- power estimation and suggested setups
- wellbeing recommendations
- automation and problem-solving suggestions
- simple mode and "Nerdy Mode"

## Developer preferences
- Use British English spelling.
- Keep explanations clear and practical.
- Do not use the word "alongside".
- Prefer simple, readable code over clever code.
- Keep functions focused and easy to test.
- Add docstrings to non-trivial functions.
- Do not add new dependencies unless explicitly asked.
- Keep the UI in Gradio from the start.
- Use Timberborn-inspired colours from the start.
- Advanced mode should be labelled "Nerdy Mode".

## Architecture rules
- Keep formulas and patch values data-driven.
- Do not hardcode Timberborn values into app logic when they belong in data files.
- Treat repo data files as the source of truth for game values.
- Folktails is the first supported faction.
- Bots are not a faction; they are a population type within the colony.
- Keep planner logic separate from UI code.
- Keep advice and recommendation logic separate from raw calculator logic.
- Prefer modular files over one huge file.

## Data rules
- Target Timberborn 1.0 patch data.
- Store updateable values in structured data files.
- Validate loaded data where practical.
- If a value is uncertain, flag it clearly rather than inventing one.

## Coding workflow
- For anything non-trivial, explain the plan before making edits.
- Keep tasks small and incremental.
- When making changes, say which files will be touched.
- After edits, summarise what changed and any risks.
- Where relevant, suggest tests to run.
- Write or update tests for planner logic.
- Do not make large speculative refactors unless explicitly asked.

## Testing
Prioritise tests for:
- data loading
- food and water maths
- power calculations
- wellbeing recommendations
- dependency expansion
- planner and advice logic

## UI and UX rules
- Make the default experience friendly for casual players.
- Keep Nerdy Mode available for detailed controls and assumptions.
- Use clear labels and outputs.
- Prefer tabs and accordions to reduce clutter.
- Outputs should be easy to skim.

## Current project direction
- Hugging Face deployment should work from the beginning.
- Build a working vertical slice early, then expand coverage.
- Focus on one faction first, then broaden later.