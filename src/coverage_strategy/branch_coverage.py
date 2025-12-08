from types import ModuleType
from typing import Callable
import coverage

from .coverage import ExecutionResult, CoverageTester
from dataset.functions_list import FunctionType


class BranchExecutionResult(ExecutionResult):
    """Execution result implementation for branch coverage."""

    def __init__(self, taken_branches: list[tuple[int, int]], total_branches: list[tuple[int, int]]):
        self.taken_branches = taken_branches
        self.total_branches = total_branches
        self.total_branches_count = sum([count for (_, count) in total_branches])
        
    def fraction_covered(self) -> float:
        """Return the fraction of branches covered."""
        covered_branches = len(self.taken_branches)
        return covered_branches / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def novelty(self, baseline: "BranchExecutionResult") -> float:
        """Calculate novelty compared to baseline execution result."""
        novel_branches = set(self.taken_branches) - set(baseline.taken_branches)
        return len(novel_branches) / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def similar_executed_or_ignored(self, other: "BranchExecutionResult") -> float:
        """Measure the inverse of the difference of the two executions, normalized by total branches."""
        differences = set(self.taken_branches) ^ set(other.taken_branches)
        val = self.total_branches_count - len(differences)
        return val / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def similar_executed(self, other: "BranchExecutionResult") -> float:
        """Measure the similarity of the two executions, normalized by total branches."""
        both_executed = set(self.taken_branches).intersection(set(other.taken_branches))
        val = len(both_executed)
        return val / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def merge_one(self, other: "BranchExecutionResult") -> "BranchExecutionResult":
        """Merge this execution result with another one."""
        if self.total_branches != other.total_branches:
            raise ValueError("cannot merge ExecutionResults with different total branches")
        merged_branches = list(set(self.taken_branches).union(set(other.taken_branches)))
        return BranchExecutionResult(merged_branches, self.total_branches)
        
    
    def __repr__(self) -> str:
        return f"<BranchExecutionResult covered={self.fraction_covered():.2%} total_branches={self.total_branches_count} taken={len(self.taken_branches)}>"

    def __lt__(self, other: "BranchExecutionResult") -> bool:
        return self.fraction_covered() < other.fraction_covered()
        
    def __gt__(self, other: "BranchExecutionResult") -> bool:
        return self.fraction_covered() > other.fraction_covered()
        
    def __le__(self, other: "BranchExecutionResult") -> bool:
        return self.fraction_covered() <= other.fraction_covered()
        
    def __ge__(self, other: "BranchExecutionResult") -> bool:
        return self.fraction_covered() >= other.fraction_covered()


class BranchCoverageTester(CoverageTester):
    """Coverage tester implementation using branch coverage."""
    
    def run_test(self, args: tuple | list[tuple]) -> BranchExecutionResult:
        """Run test with given arguments and return branch execution result."""
        if isinstance(args, tuple):
            args = [args]

        cov = coverage.Coverage(data_file=None, branch=True)
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
        
        branch_stats = cov.branch_stats(self.module.__file__)
        total_branches = []
        for key, value in branch_stats.items():
            total_branches.append((key, value[0]))
        
        # Get taken branches from arc data
        arcs = cov.get_data().arcs(self.module.__file__)
        branches_taken = []
        for fr, to in arcs:
            if fr is None or to is None:
                continue
            if fr == to:
                continue
            if fr < 0 or to < 0:
                continue
            branches_taken.append((fr, to))
        
        return BranchExecutionResult(branches_taken, total_branches)


def test_coverage(function: FunctionType):
    """Test function for branch coverage."""
    tester = BranchCoverageTester(function)
    vals = []
    for sample in ("XV", "test", "MCMXCIV", "MCMXCIVV", "IL", "XXL", "IXI"):
        result = tester.run_test((sample,))
        vals.append(result)
        print(f"Branch coverage for function {function['name']} with input {sample!r}: {result.fraction_covered()*100:.2f}%")

    # compute pairwise coverage similarity
    for x in vals:
        to_print = ""
        for y in vals:
            sim = x.similar_executed_or_ignored(y)
            to_print += f"{sim:.2f} "
        print(to_print)


def main():
    from dataset.functions_list import FUNCTIONS
    test_coverage(FUNCTIONS[0])


if __name__ == "__main__":
    main()
