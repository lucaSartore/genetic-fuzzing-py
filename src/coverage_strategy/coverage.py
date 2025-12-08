from abc import ABC, abstractmethod
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Callable, TypeVar, Self


import coverage
from dataset.functions_list import FunctionType


class ExecutionResult(ABC):
    @abstractmethod
    def fraction_covered(self) -> float:
        """Return the fraction of code covered by this execution result."""
        pass
    
    @abstractmethod
    def novelty(self, baseline: Self) -> float:
        """Calculate novelty compared to baseline execution result."""
        pass

    @abstractmethod
    def merge_one(self, other: Self) -> Self:
        """Merge this execution result with another one."""
        pass
    
    @classmethod
    def merge_list(cls, results: list[Self]) -> Self:
        """Merge a list of execution results into one."""
        assert len(results) != 0, "can't merge empty list"
        first = results[0]
        for result in results[1:]:
            first = first.merge_one(result)
        return first

    def merge_all(self, others: list[Self]) -> Self:
        """Merge this execution result with multiple others."""
        result = self
        for other in others:
            result = result.merge_one(other)
        return result


# Type variable for ExecutionResult subclasses
CovResult = TypeVar('CovResult', bound=ExecutionResult)


class CoverageTester(ABC):
    """Abstract base class for coverage testing implementations."""
    
    def __init__(self, function: FunctionType):
        self.function = function
        base_dir = Path(__file__).parent.parent / "dataset" / "output"
        module_path = base_dir / f"{function['name']}.py"
        if not module_path.exists():
            raise FileNotFoundError(f"module file not found: {module_path}")

        spec = spec_from_file_location(f"{function['name']}", module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not create import spec for {module_path}")
        self.module = module_from_spec(spec)
        try:
            spec.loader.exec_module(self.module)
        except Exception as e:
            raise ImportError(f"failed to import module {module_path}: {e}") from e

        if not hasattr(self.module, "EXPORT_FUNCTION"):
            raise AttributeError(f"module {function['name']} has no EXPORT_FUNCTION")
        self.export_fn: Callable = getattr(self.module, "EXPORT_FUNCTION")
        assert callable(self.export_fn)

    @abstractmethod
    def run_test(self, args: tuple | list[tuple]) -> ExecutionResult:
        """Run test with given arguments and return execution result."""
        pass
