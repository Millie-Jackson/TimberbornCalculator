# MVP Scope

## Project
Timberborn Calculator / Colony Planner

A Python + Gradio web app for Timberborn 1.0, hosted on Hugging Face Spaces.

## MVP goal
Release a public, genuinely useful Folktails-first colony planner that helps players estimate:
- population support
- food and water needs
- drought reserves
- building dependencies
- power demand and suggested power setup
- basic wellbeing support
- automation and problem-solving suggestions

This is not just a raw calculator.
The MVP should already feel like a colony planning tool.

## Target users
Two main user types:

1. Casual players
   - want simple answers quickly
   - need help spotting likely problems
   - may not know the exact production chain

2. Nerdy players
   - want detailed assumptions
   - want dependency breakdowns
   - want upstream requirements and ratios
   - want patch-aware numbers

## In scope for MVP

### 1. Platform and deployment
- Python project
- Gradio UI from the start
- Hugging Face Spaces deployment working from the beginning
- GitHub repo using the standard project template

### 2. Game scope
- Target Timberborn 1.0
- Folktails only for MVP
- Mixed population support:
  - adult beavers
  - kits
  - bots

### 3. Colony inputs
The MVP should support input fields for:
- faction
- adult beavers
- kits
- bots
- drought length
- safety buffer percentage
- selected buildings or planned additions
- simple mode / Nerdy Mode toggle

### 4. Core calculations
The MVP should calculate:
- daily food needs
- daily water needs
- drought reserve targets
- basic housing needs
- kit growth warnings or guidance
- bot-related support needs where relevant

### 5. Building dependency planning
The MVP should support dependency expansion for a limited but useful set of Folktails buildings.

When the user adds a building, the app should estimate:
- workers required
- upstream resources required
- upstream buildings required
- extra food and water needed for the extra workers
- power demand
- useful summary text

Example style:
> Adding 1 Gear Workshop requires X workers, Y planks, Z extra support, and N power.

### 6. Farm tile planning
The MVP should estimate farm tile requirements for relevant food chains.

This can begin with approximate but patch-driven values rather than trying to simulate every edge case.

### 7. Power planning
The MVP should include:
- total power demand
- total power production
- surplus or deficit
- suggested power setup

Power should not be ignored or treated as a later bolt-on.

### 8. Wellbeing planning
The MVP should include a first-pass wellbeing recommendation layer.

This should cover:
- simple population-to-building suggestions
- basic leisure or service recommendations
- food variety guidance where practical

Wellbeing should be helpful without becoming a giant optimisation monster.

### 9. Automation helper
The MVP should include a simple rule-based automation helper.

This should provide threshold suggestions or simple setup advice for common problems.

Examples:
- weak water reserve
- food production barely covering demand
- not enough power
- too many kits at once
- bots not being supported properly

### 10. Problem -> solution helper
The MVP should include a rule-based troubleshooting section.

This should map common colony problems to likely causes and fixes.

Examples:
- "My colony keeps running out of water"
- "My power is unstable"
- "My bots keep stopping"
- "My food chain is falling behind"

### 11. UI expectations
The MVP UI should:
- use Timberborn-inspired colours from the start
- be easy to skim
- use tabs or accordions to reduce clutter
- support a simple default view
- support a detailed "Nerdy Mode"

## Out of scope for MVP

The following are explicitly excluded from MVP:

- Iron Teeth support
- full game-wide building coverage
- perfect simulation of every colony edge case
- map layout planning
- district pathing simulation
- export/import colony saves
- account system or user login
- multiplayer or shared planning
- advanced visual graphs unless they become clearly necessary
- fully dynamic optimisation of every wellbeing path
- modelling every possible automation setup in exhaustive detail

## Data and accuracy rules
- Use Timberborn 1.0 as the target patch
- Keep values data-driven
- Store game values in editable project data files
- Avoid hardcoding values into app logic where possible
- If a value is uncertain, flag it clearly instead of inventing one

## Definition of done for MVP
The MVP is done when all of the following are true:

1. The app is live on Hugging Face Spaces
2. The app supports Folktails
3. The app supports adults, kits, and bots in one colony model
4. The app calculates food, water, and reserve needs
5. The app can expand at least a small useful set of building dependencies
6. The app includes power estimation and suggested power setup
7. The app includes first-pass wellbeing suggestions
8. The app includes basic automation advice
9. The app includes problem -> solution guidance
10. The UI is usable and readable
11. Core planner logic has tests

## Non-goals
This project is not trying to:
- replace the entire Timberborn wiki
- become a full colony simulator in version one
- model every last tile and travel-time detail from day one
- solve every faction at once
- be perfectly complete before release

## Release philosophy
Ship a useful Folktails-first planner first.
Then expand coverage.
Do not wait for perfection before releasing something players can actually use.