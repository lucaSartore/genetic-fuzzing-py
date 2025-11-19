
from types import ModuleType
from typing import Callable
from dataset.functions_list import FUNCTIONS, FunctionType
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import coverage

def main():
    test_coverage(FUNCTIONS[0])

class ExecutionResult:
    total_lines: list[int]
    missing_lines: list[int]

    def __init__(self, total_lines: list[int], missing_lines: list[int]):
        self.total_lines = total_lines
        self.missing_lines = missing_lines
    
    def fraction_covered(self) -> float:
        covered_lines = len(self.total_lines) - len(self.missing_lines)
        return covered_lines / len(self.total_lines) if len(self.total_lines) > 0 else 0.0
    
    def similar_executed_or_ignored(self, other: "ExecutionResult")-> float:
        "it measures the inverse of the difference of the two executions, normalized by total lines"
        differences = set(self.missing_lines)^(set(other.missing_lines))
        total_len = len(self.total_lines)
        val = total_len-len(differences)
        return val/total_len if total_len>0 else 0.0
    
    def similar_executed(self, other: "ExecutionResult")-> float:
        "it measures the similarity of the two executions, normalized by total lines"
        both_executed = set(self.total_lines)-set(self.missing_lines)-set(other.missing_lines)
        val = len(both_executed)
        total_len = len(self.total_lines)
        return val/total_len if total_len>0 else 0.0
    
    def merge_one(self, other: "ExecutionResult")-> "ExecutionResult":
        if self.total_lines != other.total_lines:
            raise ValueError("cannot merge ExecutionResults with different total lines")
        self.missing_lines= list(set(self.missing_lines).intersection(set(other.missing_lines)))
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
        self.export_fn: Callable = getattr(self.module, "EXPORT_FUNCTION")
        assert callable(self.export_fn)
    
    
    def run_test(self, args: tuple):
        cov = coverage.Coverage(data_file=None)
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
        (_, total_lines, _, missing_lines, _) = cov.analysis2(self.module.__file__)
        return ExecutionResult(total_lines, missing_lines)

def test_coverage(function: FunctionType):
    tester = CoverageTester(function)
    vals=[]
    for sample in ("XV", "test", "MCMXCIV", "MCMXCIVV", "IL", "XXL", "IXI", ):
        result = tester.run_test((sample,))
        vals.append(result)
        print(f"Coverage for function {function['name']} with input {sample!r}: {result.fraction_covered()*100:.2f}%")

    # compute pairwise coverage similarity
    for x in vals:
        to_print=""
        for y in vals:
            sim = x.similar_executed(y)
            to_print+=f"{sim:.2f} "
        print(to_print)
    

if __name__ == "__main__":
    main()
