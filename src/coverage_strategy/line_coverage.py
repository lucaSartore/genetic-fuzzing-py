from typing import Callable
import coverage

from .coverage import ExecutionResult, CoverageTester
from dataset.functions_list import FunctionType


class LineExecutionResult(ExecutionResult):
    """Execution result implementation for line coverage."""

    def __init__(self, total_lines: list[int], missing_lines: list[int]):
        self.total_lines = total_lines
        self.missing_lines = missing_lines

    @property
    def executed_lines(self) -> set[int]:
        """Return the set of executed lines."""
        return set(self.total_lines) - set(self.missing_lines)
    
    def fraction_covered(self) -> float:
        """Return the fraction of lines covered."""
        covered_lines = len(self.total_lines) - len(self.missing_lines)
        return covered_lines / len(self.total_lines) if len(self.total_lines) > 0 else 0.0
    
    def novelty(self, baseline: "LineExecutionResult") -> float:
        """Calculate novelty compared to baseline execution result."""
        novel_lines = self.executed_lines - baseline.executed_lines
        total_len = len(self.total_lines)
        val = len(novel_lines)
        return val / total_len if total_len > 0 else 0.0
    
    def similar_executed_or_ignored(self, other: "LineExecutionResult") -> float:
        """Measure the inverse of the difference of the two executions, normalized by total lines."""
        differences = set(self.missing_lines) ^ set(other.missing_lines)
        total_len = len(self.total_lines)
        val = total_len - len(differences)
        return val / total_len if total_len > 0 else 0.0
    
    def similar_executed(self, other: "LineExecutionResult") -> float:
        """Measure the similarity of the two executions, normalized by total lines."""
        both_executed = set(self.total_lines) - set(self.missing_lines) - set(other.missing_lines)
        val = len(both_executed)
        total_len = len(self.total_lines)
        return val / total_len if total_len > 0 else 0.0

    def merge_one(self, other: LineExecutionResult) -> LineExecutionResult:
        """Merge this execution result with another one."""
        if self.total_lines != other.total_lines:
            raise ValueError("cannot merge ExecutionResults with different total lines")
        merged_missing = list(set(self.missing_lines).intersection(set(other.missing_lines)))
        return LineExecutionResult(self.total_lines, merged_missing)
        
    
    def __repr__(self) -> str:
        return f"<LineExecutionResult covered={self.fraction_covered():.2%} total={len(self.total_lines)} missing={len(self.missing_lines)}>"

    def __lt__(self, other: "LineExecutionResult") -> bool:
        return self.fraction_covered() < other.fraction_covered()
        
    def __gt__(self, other: "LineExecutionResult") -> bool:
        return self.fraction_covered() > other.fraction_covered()
        
    def __le__(self, other: "LineExecutionResult") -> bool:
        return self.fraction_covered() <= other.fraction_covered()
        
    def __ge__(self, other: "LineExecutionResult") -> bool:
        return self.fraction_covered() >= other.fraction_covered()


class LineCoverageTester(CoverageTester):
    """Coverage tester implementation using line coverage."""
    
    def run_test(self, args: tuple | list[tuple]) -> LineExecutionResult:
        """Run test with given arguments and return line execution result."""
        if isinstance(args, tuple):
            args = [args]

        cov = coverage.Coverage(data_file=None)
        try:
            cov.erase()
            cov.start()
            for a in args:
                try:
                    self.export_fn(*a)
                except Exception:
                    # swallow exceptions from the tested function
                    pass
        finally:
            cov.stop()
        
        (_, total_lines, _, missing_lines, _) = cov.analysis2(self.module.__file__)
        return LineExecutionResult(total_lines, missing_lines)


def test_coverage(function: FunctionType):
    """Test function for line coverage."""
    tester = LineCoverageTester(function)
    vals = []
    for sample in ("XV", "test", "MCMXCIV", "MCMXCIVV", "IL", "XXL", "IXI"):
        result = tester.run_test((sample,))
        vals.append(result)
        print(f"Line coverage for function {function['name']} with input {sample!r}: {result.fraction_covered()*100:.2f}%")

    # compute pairwise coverage similarity
    for x in vals:
        to_print = ""
        for y in vals:
            sim = x.similar_executed(y)
            to_print += f"{sim:.2f} "
        print(to_print)


def main():
    from dataset.functions_list import FUNCTIONS
    test_coverage(FUNCTIONS[0])


if __name__ == "__main__":
    main()
