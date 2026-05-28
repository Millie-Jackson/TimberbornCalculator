"""Bot support calculators."""

from dataclasses import dataclass

from timberborn_planner.models.colony import ColonyInputs


@dataclass(frozen=True)
class BotSupportSummary:
    bot_count: int
    status: str


def calculate_bot_support(colony: ColonyInputs) -> BotSupportSummary:
    if colony.bots == 0:
        return BotSupportSummary(
            bot_count=0,
            status="No bots to support yet.",
        )

    return BotSupportSummary(
        bot_count=colony.bots,
        status="Bot support details are not modelled yet.",
    )


# END OF FILE
