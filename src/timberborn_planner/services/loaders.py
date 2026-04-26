# TimberbornCalculator/src/timberborn_planner/services/loaders.py

import json
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_ROOT / "data"


# .========================================================================
# BLOCK 1 — JSON helpers
# .========================================================================


def _load_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Data fie not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Data file must contain a JSON object: {path}")

    return data


def load_global_data() -> dict[str, Any]:
    return _load_json_file(DATA_DIR / "global.json")


def load_patch_meta() -> dict[str, Any]:
    return _load_json_file(DATA_DIR / "patch_meta.json")


def load_faction_data(faction: str = "folktails") -> dict[str, Any]:

    filename = f"{faction.lower()}.json"

    return _load_json_file(DATA_DIR / filename)


# .========================================================================
# BLOCK 2 — Combined loader
# .========================================================================


def load_game_data(faction: str = "folktails") -> dict[str, Any]:

    global_data = load_global_data()
    faction_data = load_faction_data()
    patch_meta = load_patch_meta()

    return {
        "global": global_data,
        "faction": faction_data,
        "patch_meta": patch_meta,
    }


# END OF FILE
