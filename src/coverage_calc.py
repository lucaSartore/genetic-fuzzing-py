
from types import ModuleType
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
    
    def __repr__(self) -> str:
        return f"<ExecutionResult covered={self.fraction_covered():.2%} total={len(self.total_lines)} missing={len(self.missing_lines)}>"


class CoverageTester:
    function: FunctionType
    module: ModuleType
    export_fn: callable
    
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
        cov = coverage.Coverage(data_file=None)
        try:
            cov.erase()
            cov.start()
            try:
                self.export_fn(*args)
            except Exception:
                # swallow exceptions from the tested function, but ensure coverage is stopped
                pass
        finally:
            cov.stop()
        (_, total_lines, _, missing_lines, _) = cov.analysis2(self.module.__file__)
        return ExecutionResult(total_lines, missing_lines)

def test_coverage(function: FunctionType):
    tester = CoverageTester(function)
    for sample in ("XV", "test", "MCMXCIV", "IL", "XXL", "IXI"):
        result = tester.run_test((sample,))
        print(f"Coverage for function {function['name']} with input {sample!r}: {result.fraction_covered()*100:.2f}%")


if __name__ == "__main__":
    main()