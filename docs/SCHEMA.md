# Data Schema

## Population schema

Population supports:
- adult beavers
- kits
- bots

```json
{
  "population": {
    "adult": {
      "food_per_day": 2,
      "water_per_day": 2,
      "can_work": true
    },
    "kit": {
      "food_per_day": 1,
      "water_per_day": 1,
      "can_work": false
    },
    "bot": {
      "food_per_day": 0,
      "water_per_day": 0,
      "can_work": true
    }
  }
}
```

## Resource schema

```json
{
  "logs": {
    "name": "Logs",
    "emoji": "🪵",
    "type": "raw_material"
  }
}
```

Allowed resource types:
- raw_material
- processed_material
- food
- liquid
- science
- power
- wellbeing

## Building schema

```json
{
  "gear_workshop": {
    "name": "Gear Workshop",
    "category": "industry",
    "construction_cost": {
      "planks": 30
    },
    "science_cost": {
      "science": 30
    },
    "workers": 4,
    "job_type": "industry_worker",
    "inputs_per_day": {
      "planks": 10
    },
    "outputs_per_day": {
      "gears": 5
    },
    "power_required": 120,
    "power_produced": 0,
    "wellbeing": {},
    "automation_hints": []
  }
}
```

## Jobs schema

```json
{
  "jobs": {
    "industry_worker": {
      "name": "Industry Worker",
      "counts_as_worker": true
    },
    "farmer": {
      "name": "Farmer",
      "counts_as_worker": true
    }
  }
}
```

## Power schema

Buildings can require or produce power.

```json
{
  "power_required": 120,
  "power_produced": 0
}
```

Power outputs should calculate:
- total required
- total produced
- surplus or deficit
- suggested setup

## Food and water schema

Consumption lives in `global.json`.

```json
{
  "food_per_day": 2,
  "water_per_day": 2
}
```

Food production lives on buildings.

```json
{
  "outputs_per_day": {
    "carrots": 20
  }
}
```

## Kits schema

Kits are population members but not workers.

Kit guidance should calculate:
- kit count
- kits as percentage of total population
- warning if kit ratio is too high

## Bots schema

Bots are population members, not a faction.

Bots:
- do not need food
- do not need water
- can work
- may need bot-specific support later

## Wellbeing schema

Wellbeing is recommendation-based at MVP stage.

```json
{
  "wellbeing": {
    "category": "leisure",
    "supports_population": 10
  }
}
```

Wellbeing outputs should suggest:
- buildings needed
- food variety prompts
- service gaps

## Automation hints schema

Automation hints are simple rule-based suggestions.

```json
{
  "automation_hints": [
    {
      "problem": "low_water_storage",
      "suggestion": "Add more water storage before long droughts."
    }
  ]
}
```

## Schema rule

All Timberborn numbers should live in JSON data files.

Python code should load and calculate from data.
Do not hardcode game values into calculator logic unless unavoidable.
