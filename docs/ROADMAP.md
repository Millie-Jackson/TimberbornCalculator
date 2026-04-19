# Roadmap

## Project goal
Build a Timberborn colony planner for Timberborn 1.0 using Python and Gradio, hosted on Hugging Face Spaces.

The planner should help players estimate:
- food
- water
- storage
- drought reserves
- housing
- power
- wellbeing support
- automation suggestions
- building dependency chains

The first supported faction is Folktails.

---

## Phase 0 — Setup
Goal: get the project running locally and on Hugging Face from day one.

Tasks:
1. Create the repo and publish it
2. Create the Hugging Face Space
3. Add minimal Gradio app
4. Add `requirements.txt`
5. Confirm local run works
6. Confirm Hugging Face deploy works
7. Add root docs:
   - `README.md`
   - `AGENTS.md`
8. Add docs folder and starter planning docs
9. Pick Timberborn-inspired colours now

Milestone:
- Gradio app is live locally and on Hugging Face

---

## Phase 1 — Data spine
Goal: create the data structure that drives the planner.

Tasks:
1. Create project package structure
2. Add Timberborn data files:
   - `global.json`
   - `folktails.json`
   - `patch_meta.json`
3. Define schema for:
   - population
   - resources
   - buildings
   - jobs
   - power
   - food and water consumption
   - kits
   - bots
   - wellbeing
   - automation hints
4. Build data loaders
5. Add basic validation
6. Add tests for loading and validation

Milestone:
- Data files load successfully and validation catches broken values

---

## Phase 2 — Core colony maths
Goal: calculate the basic needs of a colony.

Tasks:
1. Model colony inputs:
   - adults
   - kits
   - bots
   - drought days
   - safety buffer
2. Build calculators for:
   - food per day
   - water per day
   - storage reserve
   - housing
   - bot support
3. Add kit guidance:
   - recommended max kits
   - kit ratio warnings
4. Add tests for all core maths

Milestone:
- Basic colony needs can be calculated correctly

---

## Phase 3 — First real UI slice
Goal: connect the maths to a usable Gradio interface.

Tasks:
1. Build Overview tab
2. Add population inputs
3. Add drought and safety settings
4. Display basic output cards
5. Add simple mode and Nerdy Mode structure
6. Keep Hugging Face deploy working with each step

Milestone:
- A user can enter colony inputs and get useful outputs in the app

---

## Phase 4 — Dependency planner
Goal: turn the calculator into a planner.

Tasks:
1. Define building dependency rules
2. Start with a small set of Folktails buildings
3. Build planner logic so adding a building returns:
   - extra workers needed
   - upstream resources needed
   - upstream buildings needed
   - food and water needed for those workers
   - power needed
4. Add farm tile estimation
5. Add summary text outputs
6. Add dependency tests

Milestone:
- The planner can explain what a new building requires

---

## Phase 5 — Power
Goal: include power demand and suggested setups.

Tasks:
1. Add power demand calculations
2. Add power generation options for Folktails
3. Show:
   - total required power
   - total produced power
   - deficit or surplus
4. Add suggested power setup output
5. Add tests for power calculations

Milestone:
- The app can estimate required power and suggest a setup

---

## Phase 6 — Wellbeing
Goal: add wellbeing support without overcomplicating the planner.

Tasks:
1. Split wellbeing into categories
2. Add simple recommendation rules
3. Suggest service buildings and ratios
4. Keep recommendation logic separate from core calculator logic
5. Add tests

Milestone:
- The app gives useful wellbeing recommendations

---

## Phase 7 — Automation and problem solver
Goal: help casual players fix common colony issues.

Tasks:
1. Add Automation tab
2. Add threshold suggestions
3. Add problem -> likely fix logic
4. Start with common issues:
   - too little water
   - too little food
   - weak drought prep
   - power deficit
   - too many kits
   - bots failing
5. Add tests for advice outputs

Milestone:
- The app can suggest useful fixes for common colony problems

---

## Phase 8 — Expand Folktails coverage
Goal: make the planner useful enough for real players.

Tasks:
1. Add more buildings
2. Add more food chains
3. Add more power options
4. Improve storage and drought modelling
5. Improve warnings and summaries
6. Add more tests

Milestone:
- Folktails MVP feature set is broadly useful

---

## Phase 9 — Polish
Goal: make the tool feel public-ready.

Tasks:
1. Improve Timberborn-inspired theme
2. Improve layout and spacing
3. Add help text and assumptions
4. Improve readability in Nerdy Mode
5. Improve output presentation

Milestone:
- The app looks and feels like a proper public tool

---

## Phase 10 — MVP release
Goal: release the first public version.

MVP includes:
- Folktails support
- mixed populations
- colony needs calculations
- dependency planning
- power estimation and suggestions
- wellbeing recommendations
- automation and problem advice
- Gradio UI
- Hugging Face deployment
- tests for core planner logic

Milestone:
- Public Folktails MVP

---

## Post-MVP
Later ideas:
- Iron Teeth
- presets by colony stage
- export and import configs
- compare colony setups
- richer automation logic
- patch update workflow