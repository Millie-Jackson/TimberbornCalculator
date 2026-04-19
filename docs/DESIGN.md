# Design

## Project
Timberborn Calculator / Colony Planner

A Python + Gradio web app for Timberborn 1.0.

The tool is intended to be more than a basic calculator.
It should behave as a colony planner that helps users understand:

- what a colony currently needs
- what happens when they add new buildings
- what support chains are required
- where likely bottlenecks are
- how to prepare for droughts, growth, and power needs

## Core design principles

### 1. Data-driven values
Game values must be stored in project data files, not buried in calculator logic.

Reason:
- Timberborn updates happen
- values may need patch corrections
- faction data differs
- hardcoding values makes maintenance miserable

Examples of values that belong in data:
- consumption rates
- building construction costs
- building operating costs
- workers per building
- input/output resources
- power use or power generation
- storage capacities
- wellbeing building ratios
- automation hints

### 2. Separate build cost from run cost
Every building should distinguish between:

- construction cost
- operating requirements
- colony support requirements

This matters because a player may want to know:
- what resources they need to place a building now
- what they will need to keep it functioning afterwards
- what new demands this adds to the wider colony

Example:

Adding 1 Gear Workshop may require:
- Build: logs and planks
- Run: workers, planks, power
- Support: food, water, housing, wellbeing support for the workers

### 3. Mixed population model
The app should support one colony containing:
- adult beavers
- kits
- bots

Bots are not a faction.
They are a population type within the colony.

The faction changes the available buildings, foods, and production chains.
The population mix changes the colony's needs.

### 4. Planner, not just calculator
The app should answer:
- how much food and water do I need?
- what do I need to support this building?
- how much power do I need?
- what upstream buildings or tiles do I need?
- what common problems am I likely to hit?

This means the system must support dependency expansion, not just isolated formulas.

### 5. Friendly by default
The app should work for:
- casual players
- detail-focused players

Default mode should be simple and readable.
Advanced mode should be labelled "Nerdy Mode".

## Architecture overview

The project should be split into a few clear layers.

### 1. Data layer
Stores Timberborn patch values in editable structured files.

Suggested files:
- `global.json`
- `folktails.json`
- later `ironteeth.json`
- `patch_meta.json`

Responsibilities:
- define resources
- define buildings
- define consumption rates
- define wellbeing rules
- define power values
- define automation hints

### 2. Loader and validation layer
Loads structured data into Python.
Checks that required keys and values exist.

Responsibilities:
- load JSON data
- validate schema basics
- raise useful errors when data is broken

### 3. Calculator layer
Performs focused calculations.

Examples:
- food and water needs
- drought storage reserves
- housing estimates
- power demand and supply
- wellbeing recommendations
- farm tile estimates

These calculators should stay small and testable.

### 4. Dependency engine
This is the planner core.

The dependency engine expands user actions into upstream requirements.

Example:
User adds 1 Gear Workshop.

The engine should determine:
- construction cost
- workers needed
- operating inputs
- power demand
- upstream producers needed
- support burden added to the colony

This is what makes the tool a planner rather than a plain calculator.

### 5. Advice layer
Provides rule-based recommendations.

Examples:
- weak water reserve
- too many kits at once
- insufficient power margin
- too little food buffer
- bots not properly supported
- likely labour bottlenecks

This layer should stay separate from the raw maths.

### 6. UI layer
Gradio interface for player inputs and planner outputs.

The UI should:
- use Timberborn-inspired colours from the start
- keep simple mode clean
- hide advanced controls in accordions or Nerdy Mode sections
- show outputs in clear grouped blocks

## Proposed project structure

```text
src/timberborn_planner/
├── __init__.py
├── config.py
├── data/
│   ├── global.json
│   ├── folktails.json
│   └── patch_meta.json
├── models/
│   ├── colony.py
│   ├── buildings.py
│   └── resources.py
├── calculators/
│   ├── food_water.py
│   ├── housing.py
│   ├── drought.py
│   ├── power.py
│   ├── wellbeing.py
│   └── farm_tiles.py
├── advisors/
│   ├── automation.py
│   └── problems.py
├── services/
│   ├── loaders.py
│   ├── planner.py
│   └── dependency_engine.py
└── ui/
    ├── theme.py
    ├── overview_tab.py
    ├── planner_tab.py
    ├── wellbeing_tab.py
    └── automation_tab.py


## Colony model

The colony model should represent the current state and planning assumptions.

### Inputs
- faction
- adult beavers
- kits
- bots
- drought days
- safety buffer percentage
- target population
- selected buildings
- selected power setup
- selected science progression or target unlock
- simple mode or Nerdy Mode

### Outputs
- food per day
- water per day
- storage targets
- housing targets
- kit growth warnings
- build costs
- operating costs
- support requirements
- science requirements
- power surplus or deficit
- wellbeing suggestions
- problem warnings

---

## Building model

Each building should include:

- id
- display name
- faction
- category
- construction cost
- science cost or unlock requirement
- worker count
- operating inputs (per day)
- operating outputs (per day)
- power required or produced
- optional wellbeing contribution
- notes
- automation hints

### Example

```json
{
  "gear_workshop": {
    "name": "Gear Workshop",
    "category": "industry",
    "construction_cost": {
      "logs": 0,
      "planks": 0
    },
    "science_cost": {
      "science": 0
    },
    "workers": 4,
    "inputs_per_day": {
      "planks": 10
    },
    "outputs_per_day": {
      "gears": 5
    },
    "power_required": 120
  }
}

## Resource coverage

The MVP should support a limited but meaningful set of resources.

### Core resources
- logs
- planks
- gears
- water
- science

### Food (initial set)
- carrots
- grilled potatoes (or equivalent early food)

The goal is not full coverage, but enough to support early-to-mid colony planning.

---

## Build vs Run vs Support

All outputs must be clearly grouped into:

### Build
Resources required to construct buildings:
- logs
- planks
- gears
- metal blocks (later if needed)
- science (unlock cost)

### Run
Resources required to operate buildings:
- workers
- input materials per day
- power

### Support
Colony impact of running buildings:
- food required for workers
- water required
- housing
- wellbeing support
- additional upstream production

This separation is required for clarity.

---

## Dependency planning scope

The MVP should support dependency expansion for a small set of buildings.

### Initial building set (example)
- Lumber Mill
- Gear Workshop
- Farmhouse
- basic food processor (e.g. grill)
- water pump
- storage building

### Behaviour
When a building is added, the planner should:
- calculate build cost
- calculate run requirements
- calculate support requirements
- identify upstream buildings required

The system does not need to support every building yet.

---

## Science scope

Science must be included in MVP.

### The planner should:
- show science required to unlock selected buildings
- warn if science is a bottleneck
- include science in planning summaries

### Not required for MVP:
- full tech tree navigation
- optimal science pathing

---

## Power scope

Power must be included in MVP.

### The planner should:
- calculate total power demand
- estimate power production
- show surplus or deficit
- suggest a basic power setup

Power should not be ignored or simplified away.

---

## Wellbeing scope

Wellbeing should be included as a simple recommendation layer.

### Include:
- basic building ratios (e.g. campsites)
- simple service suggestions
- basic food variety prompts

### Exclude:
- full wellbeing optimisation
- detailed happiness simulation

---

## Kits and growth scope

Kits must be included in MVP.

### The planner should:
- include kits in population totals
- estimate their impact on housing and resources
- provide simple growth guidance

### Example outputs:
- recommended max kits
- kits as % of total population
- warning if growth is too aggressive

---

## Automation and advice scope

The MVP should include a rule-based advice system.

### Include:
- water shortage warnings
- food shortage warnings
- power deficit warnings
- kit overgrowth warnings
- science bottleneck warnings
- basic production imbalance warnings

### Advice should:
- be short
- be actionable
- avoid jargon where possible

---

## UI scope

The MVP UI should:

- use Timberborn-inspired colours from the start
- support tabs or grouped sections
- support a simple default mode
- support "Nerdy Mode"
- clearly group outputs into:
  - Build
  - Run
  - Support
  - Science
  - Warnings
  - Suggestions

---

## Definition of done

The MVP is complete when:

1. The app is live on Hugging Face
2. Folktails is supported
3. Mixed population works (adults, kits, bots)
4. Food and water calculations work
5. Building dependency expansion works (limited set)
6. Build vs run vs support is clearly shown
7. Power is included with suggested setup
8. Science requirements are included
9. Wellbeing suggestions are present
10. Advice system produces useful warnings
11. The UI is usable and readable
12. Core logic has tests

---

## Release rule

Ship when it is:
- useful
- understandable
- correct enough

Do not wait for:
- full game coverage
- perfect accuracy
- every edge case

Release early, improve continuously.