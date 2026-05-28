"""Colony input models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColonyInputs:
    """Basic colony population and planning assumptions."""

    adults: int = 0
    kits: int = 0
    bots: int = 0
    drought_days: int = 0
    safety_buffer: float = 0

    def __post_init__(self) -> None:
        self._validate_non_negative("adults", self.adults)
        self._validate_non_negative("kits", self.kits)
        self._validate_non_negative("bots", self.bots)
        self._validate_non_negative("drought_days", self.drought_days)
        self._validate_non_negative("safety_buffer", self.safety_buffer)

    @property
    def total_population(self) -> int:
        return self.adults + self.kits + self.bots

    @property
    def working_population(self) -> int:
        return self.adults + self.bots

    @property
    def kit_ratio(self) -> float:
        if self.total_population == 0:
            return 0

        return self.kits / self.total_population

    @staticmethod
    def _validate_non_negative(name: str, value: int | float) -> None:
        if value < 0:
            raise ValueError(f"{name} must be 0 or above")


# END OF FILE
