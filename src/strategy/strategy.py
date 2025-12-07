from dataclasses import dataclass
from typing import Self, Literal
from coverage_strategy.branch_coverage import BranchCoverageTester
from coverage_strategy.coverage import CoverageTester
from coverage_strategy.line_coverage import LineCoverageTester
from dataset.functions_list import FunctionType
from abc import ABC, abstractmethod
import os

StrategyEnum = Literal["random", "input_bag", "novelty_search"]

@dataclass
class SettingsBaseClass():
    coverage_tester_class: type[CoverageTester] = BranchCoverageTester


class Strategy[TSettings: SettingsBaseClass](ABC):

    def __init__(self, function: FunctionType, settings: TSettings, log_dir: str):
        self.settings = settings
        self.log_dir = log_dir
        self.log_step = 0
        self.log_file = None
        self.function_def = function
        self.tester = settings.coverage_tester_class(function)
        self.function = self.tester.export_fn
        if os.path.exists(log_dir):
            self.log_file = open(f"{log_dir}/log.csv","w")
            self.log_file.write("time_step, score\n")

    def __del__(self):
        if self.log_file is not None:
            self.log_file.close()

    @classmethod
    def initialize(cls, function: FunctionType, settings: TSettings | None = None, log_dir: str = "") -> Self:
        if settings is None:
            settings = cls.default_settings()
        return cls(function, settings, log_dir)


    @classmethod
    @abstractmethod
    def default_settings(cls) -> TSettings:
        pass

    @abstractmethod
    def run(self) -> list[tuple]:
        pass

    def log(self, score: float):
        print(f"at iteration {self.log_step} coverage score is {score}")
        if self.log_file is not None:
            self.log_file.write(f"{self.log_step}, {score}\n")
        self.log_step += 1

    @classmethod
    def with_line_coverage(cls, function: FunctionType, settings: TSettings | None = None, log_dir: str = "") -> Self:
        """Create Strategy with line coverage tester."""
        if settings is None:
            settings = cls.default_settings()
        settings.coverage_tester_class = LineCoverageTester
        return cls.initialize(function, settings, log_dir)
    
    @classmethod 
    def with_branch_coverage(cls, function: FunctionType, settings: TSettings | None = None, log_dir: str = "") -> Self:
        """Create Strategy with branch coverage tester."""
        if settings is None:
            settings = cls.default_settings()
        settings.coverage_tester_class = BranchCoverageTester
        return cls.initialize(function, settings, log_dir)

    def set_coverage_type(self, coverage_type: str) -> None:
        """Switch between different coverage types."""
        if coverage_type == "line":
            self.settings.coverage_tester_class = LineCoverageTester
        elif coverage_type == "branch":
            self.settings.coverage_tester_class = BranchCoverageTester
        else:
            raise ValueError(f"Unknown coverage type: {coverage_type}. Use 'line' or 'branch'.")
        
        # Recreate the tester with the new coverage type
        self.tester = self.settings.coverage_tester_class(self.function_def)
        self.function = self.tester.export_fn
