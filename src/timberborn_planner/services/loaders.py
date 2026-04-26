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


def _require_keys(
    data: dict[str, Any],
    required_keys: list[str],
    section_name: str,
) -> None:

    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        raise ValueError(f"{section_name} is missing required keys: {missing_keys}")


# .========================================================================
# BLOCK 2 — Validation helpers
# .========================================================================


def validate_global_data(data: dict[str, Any]) -> None:

    _require_keys(
        data=data, required_keys=["resources", "population"], section_name="global.json"
    )


def validate_faction_data(data: dict[str, Any]) -> None:

    _require_keys(data=data, required_keys=["buildings"], section_name="faction data")


def validate_patch_meta(data: dict[str, Any]) -> None:

    _require_keys(
        data=data,
        required_keys=["game", "version", "faction", "notes"],
        section_name="patch_meta.json",
    )


# .========================================================================
# BLOCK 3 — Public loaders
# .========================================================================


def load_global_data() -> dict[str, Any]:

    data = _load_json_file(DATA_DIR / "global.json")
    validate_global_data(data)

    return data


def load_patch_meta() -> dict[str, Any]:

    data = _load_json_file(DATA_DIR / "patch_meta.json")
    validate_patch_meta(data)

    return data


def load_faction_data(faction: str = "folktails") -> dict[str, Any]:

    filename = f"{faction.lower()}.json"
    data = _load_json_file(DATA_DIR / filename)
    validate_faction_data(data)

    return data


# .========================================================================
# BLOCK 4 — Combined loader
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
