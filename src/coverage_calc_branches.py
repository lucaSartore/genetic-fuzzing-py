
from types import ModuleType
from dataset.functions_list import FUNCTIONS, FunctionType
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import coverage

def main():
    test_coverage(FUNCTIONS[0])

class ExecutionResult:

    def __init__(self, taken_branches: list[tuple[int, int]], total_branches: list[tuple[int, int]]):
        self.taken_branches = taken_branches
        self.total_branches = total_branches
        self.total_branches_count = sum([count for (_, count) in total_branches])
        
    def fraction_covered(self) -> float:
        covered_lines = len(self.taken_branches)
        return covered_lines / self.total_branches_count if self.total_branches_count > 0 else 0.0
    
    def similar_executed_or_ignored(self, other: "ExecutionResult")-> float:
        "it measures the inverse of the difference of the two executions, normalized by total lines"
        differences = set(self.taken_branches)^(set(other.taken_branches))
        val = self.total_branches_count-len(differences)
        return val/self.total_branches_count if self.total_branches_count>0 else 0.0
    
    def similar_executed(self, other: "ExecutionResult")-> float:
        "it measures the similarity of the two executions, normalized by total lines"
        both_executed = set(self.taken_branches).intersection(set(other.taken_branches))
        val = len(both_executed)
        return val/self.total_branches_count if self.total_branches_count>0 else 0.0
    
    def merge_one(self, other: "ExecutionResult")-> "ExecutionResult":
        if self.total_branches != other.total_branches:
            raise ValueError("cannot merge ExecutionResults with different total lines")
        self.taken_branches= list(set(self.taken_branches).union(set(other.taken_branches)))
        return self
        
    def merge_all(self, others: list["ExecutionResult"])-> "ExecutionResult":
        #result = ExecutionResult(self.total_lines, self.missing_lines)
        for other in others:
            self.merge_one(other)
        return self
    
    def __repr__(self) -> str:
        return f"<ExecutionResult covered={self.fraction_covered():.2%} total={len(self.total_lines)} missing={len(self.missing_lines)}>"


class CoverageTester:
    
    def __init__(self, function: FunctionType):
        self.function = function
        base_dir = Path(__file__).parent / "dataset" / "output"
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
        self.export_fn = getattr(self.module, "EXPORT_FUNCTION")
    
    
    def run_test(self, args: tuple):
        cov = coverage.Coverage(data_file=None, branch=True)
        try:
            cov.erase()
            cov.start()
            try:
                self.export_fn(*args)
            except Exception:
                # swallow exceptions from the tested function
                pass
        finally:
            cov.stop()
        branch = cov.branch_stats(self.module.__file__)
        total_branches = []
        for key, value in branch.items():
            total_branches.append((key, value[0]))
        
        
        # extended for readability
        arcs = cov.get_data().arcs(self.module.__file__)
        branches_taken = []
        for fr, to in arcs:
            if fr is None or to is None:
                continue
            if fr==to:
                continue
            if fr<0 or to<0:
                continue
            branches_taken.append((fr, to))
        return ExecutionResult(branches_taken, total_branches)

def test_coverage(function: FunctionType):
    tester = CoverageTester(function)
    vals=[]
    for sample in ("XV", "test", "MCMXCIV", "MCMXCIVV", "IL", "XXL", "IXI", ):
        result = tester.run_test((sample,))
        vals.append(result)
        #print(f"{result.total_lines}")
        print(f"Coverage for function {function['name']} with input {sample!r}: {result.fraction_covered()*100:.2f}%")

    # compute pairwise coverage similarity
    for x in vals:
        to_print=""
        for y in vals:
            sim = x.similar_executed_or_ignored(y)
            to_print+=f"{sim:.2f} "
        print(to_print)
    

if __name__ == "__main__":
    main()
