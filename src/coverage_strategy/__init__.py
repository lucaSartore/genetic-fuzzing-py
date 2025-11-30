"""Coverage testing package with different coverage strategies."""

from .coverage import CoverageTester, ExecutionResult
from .branch_coverage import BranchCoverageTester, BranchExecutionResult
from .line_coverage import LineCoverageTester, LineExecutionResult

__all__ = [
    "CoverageTester",
    "ExecutionResult", 
    "BranchCoverageTester",
    "BranchExecutionResult",
    "LineCoverageTester", 
    "LineExecutionResult"
]