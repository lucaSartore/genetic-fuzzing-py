from types import ModuleType
from typing import Callable
import coverage

from .coverage import ExecutionResult, CoverageTester
from .hashable_result_container import HashableResultContainer
from dataset.functions_list import FunctionType


class BranchExecutionResult(ExecutionResult):
    """Execution result implementation for branch coverage."""

    def __init__(
        self,
        taken_branches: list[tuple[int, int]],
        total_branches: list[tuple[int, int]],
        path_hashes: set[HashableResultContainer[tuple[int, int]]] | None = None 
    ):
        self.taken_branches = taken_branches
        self.total_branches = total_branches
        self.total_branches_count = sum([count for (_, count) in total_branches])
        if path_hashes != None:
            self.path_hashes = path_hashes
        else:
            self.path_hashes = set([HashableResultContainer(taken_branches, total_branches)])

        
    def fraction_covered(self) -> float:
        """Return the fraction of branches covered."""
        covered_branches = len(self.taken_branches)
        return covered_branches / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def novelty(self, baseline: "BranchExecutionResult") -> float:
        """Calculate novelty compared to baseline execution result."""
        for path in self.path_hashes:
            if path not in baseline.path_hashes:
                return 1
        return 0
    
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
        path_hashes = self.path_hashes.union(other.path_hashes)
        merged_branches = list(set(self.taken_branches).union(set(other.taken_branches)))
        return BranchExecutionResult(merged_branches, self.total_branches, path_hashes)
        
    
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
    
    def __init__(self, function: FunctionType):
        super().__init__(function)
        # Cache the total branches since they don't change
        self._total_branches_cache = None
        # Reuse coverage object to avoid recreation overhead
        self._cov = coverage.Coverage(data_file=None, branch=True)
    
    def _get_total_branches(self) -> list[tuple[int, int]]:
        """Get total branches, using cache if available."""
        if self._total_branches_cache is None:
            # Run once to get branch stats
            self._cov.start()
            try:
                self.export_fn()
            except:
                pass
            self._cov.stop()
            
            branch_stats = self._cov.branch_stats(self.module.__file__)
            self._total_branches_cache = [(key, value[0]) for key, value in branch_stats.items()]
            self._cov.erase()
        
        return self._total_branches_cache
    
    def run_test(self, args: tuple | list[tuple]) -> BranchExecutionResult:
        """Run test with given arguments and return branch execution result."""
        if isinstance(args, tuple):
            args = [args]

        # Erase previous data and start fresh
        self._cov.erase()
        self._cov.start()
        try:
            for a in args:
                try:
                    self.export_fn(*a)
                except Exception:
                    # swallow exceptions from the tested function
                    pass
        finally:
            pass
            self._cov.stop()
        
        # Use cached total branches
        total_branches = self._get_total_branches()
        
        # Get taken branches from arc data - optimize this loop
        arcs = self._cov.get_data().arcs(self.module.__file__)
        if arcs is None:
            branches_taken = []
        else:
            # Use set comprehension for faster filtering
            total_branches_set = {fr for fr, _ in total_branches}
            branches_taken = [
                (fr, to) for fr, to in arcs
                if fr is not None and to is not None and fr != to 
                and fr >= 0 and to >= 0 and fr in total_branches_set
            ]
        
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
