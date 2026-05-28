"""Kit growth guidance."""

from dataclasses import dataclass

from timberborn_planner.models.colony import ColonyInputs

RECOMMENDED_KIT_RATIO = 0.2
CAUTION_KIT_RATIO = 0.3

OK_MESSAGE = "Kit growth looks manageable."
CAUTION_MESSAGE = (
    "Kit count is a little high; make sure food, water, and housing can keep up."
)
WARNING_MESSAGE = (
    "Kit count is high; growth may overload food, water, housing, and labour planning."
)


@dataclass(frozen=True)
class KitGuidance:
    current_kits: int
    biological_population: int
    recommended_max_kits: int
    kit_ratio: float
    status: str
    message: str


def calculate_kit_guidance(colony: ColonyInputs) -> KitGuidance:
    biological_population = calculate_biological_population(colony)
    kit_ratio = calculate_kit_ratio(colony)
    status = choose_kit_status(kit_ratio)

    return KitGuidance(
        current_kits=colony.kits,
        biological_population=biological_population,
        recommended_max_kits=calculate_recommended_max_kits(biological_population),
        kit_ratio=kit_ratio,
        status=status,
        message=message_for_status(status),
    )


def calculate_biological_population(colony: ColonyInputs) -> int:
    return colony.adults + colony.kits


def calculate_recommended_max_kits(biological_population: int) -> int:
    return int(biological_population * RECOMMENDED_KIT_RATIO)


def calculate_kit_ratio(colony: ColonyInputs) -> float:
    biological_population = calculate_biological_population(colony)

    if biological_population == 0:
        return 0

    return colony.kits / biological_population


def choose_kit_status(kit_ratio: float) -> str:
    if kit_ratio <= RECOMMENDED_KIT_RATIO:
        return "OK"

    if kit_ratio <= CAUTION_KIT_RATIO:
        return "caution"

    return "warning"


def message_for_status(status: str) -> str:
    messages = {
        "OK": OK_MESSAGE,
        "caution": CAUTION_MESSAGE,
        "warning": WARNING_MESSAGE,
    }

    return messages[status]


# END OF FILE
