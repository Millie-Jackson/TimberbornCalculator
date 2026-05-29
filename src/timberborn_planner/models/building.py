"""Building dependency summary models."""

from dataclasses import dataclass, field


ResourceAmounts = dict[str, float | int]


@dataclass(frozen=True)
class BuildingBuildRequirements:
    """Resources and unlock costs needed before a building can be built."""

    construction_cost: ResourceAmounts = field(default_factory=dict)
    science_cost: ResourceAmounts = field(default_factory=dict)

    def to_dict(self) -> dict[str, ResourceAmounts]:
        return {
            "construction_cost": dict(self.construction_cost),
            "science_cost": dict(self.science_cost),
        }


@dataclass(frozen=True)
class BuildingRunRequirements:
    """Daily operating needs and outputs for one building."""

    workers: int = 0
    inputs_per_day: ResourceAmounts = field(default_factory=dict)
    outputs_per_day: ResourceAmounts = field(default_factory=dict)
    power_required: float | int = 0
    power_produced: float | int = 0

    def to_dict(self) -> dict[str, ResourceAmounts | float | int]:
        return {
            "workers": self.workers,
            "inputs_per_day": dict(self.inputs_per_day),
            "outputs_per_day": dict(self.outputs_per_day),
            "power_required": self.power_required,
            "power_produced": self.power_produced,
        }


@dataclass(frozen=True)
class WorkerSupportBurden:
    """Food, water, and housing burden added by staffed buildings."""

    workers: int = 0
    food_per_day: float = 0
    water_per_day: float = 0
    housing: int = 0

    def to_dict(self) -> dict[str, float | int]:
        return {
            "workers": self.workers,
            "food_per_day": self.food_per_day,
            "water_per_day": self.water_per_day,
            "housing": self.housing,
        }


@dataclass(frozen=True)
class BuildingDependencySummary:
    """Build, run, and support requirements for one building."""

    building_id: str
    name: str
    build: BuildingBuildRequirements
    run: BuildingRunRequirements
    support: WorkerSupportBurden

    def to_dict(self) -> dict[str, object]:
        return {
            "building_id": self.building_id,
            "name": self.name,
            "build": self.build.to_dict(),
            "run": self.run.to_dict(),
            "support": self.support.to_dict(),
        }


# END OF FILE
