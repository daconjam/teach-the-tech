import time
import statistics
from typing import Dict, Any, Callable, List

from radon.complexity import cc_visit, cc_rank


class CodeTelemetryEngine:
    """
    Production-grade telemetry engine providing static complexity analysis
    and isolated runtime execution profiling.
    """

    @staticmethod
    def calculate_cyclomatic_complexity(source_code: str) -> List[Dict[str, Any]]:
        """
        Calculates cyclomatic complexity using Radon's underlying AST visitor.
        Returns explicit structural evaluations or precise error payloads.
        """
        results: List[Dict[str, Any]] = []

        # Defensive Gate: Reject blank blocks before invoking parsing layers
        if not source_code.strip():
            return [{"error": "Empty or whitespace-only code block provided."}]

        try:
            blocks = cc_visit(source_code)
            for block in blocks:
                results.append(
                    {
                        "type": str(type(block).__name__),
                        "name": str(block.name),
                        "complexity": int(block.complexity),
                        "rank": str(cc_rank(block.complexity)),
                    }
                )
        except SyntaxError as e:
            results.append(
                {"error": f"Static analysis failed due to SyntaxError: {str(e)}"}
            )
        except Exception as e:
            results.append(
                {"error": f"Unexpected structural parsing failure: {str(e)}"}
            )

        return results

    @staticmethod
    def profile_execution(
        func: Callable[..., Any], *args: Any, iterations: int = 5, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Profiles runtime execution velocity across isolated iterations.
        Defensively manages internal loop failures to preserve tracking integrity.
        """
        if iterations <= 0:
            raise ValueError("Profiling iterations must be a positive integer.")

        execution_times: List[float] = []
        failure_count: int = 0
        error_logs: List[str] = []

        for _ in range(iterations):
            start_time = time.perf_counter()
            try:
                func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_times.append(end_time - start_time)
            except Exception as e:
                failure_count += 1
                error_logs.append(str(type(e).__name__))
                # Continue the loop to allow other profiling iterations to complete
                continue

        # Handle the edge case where every iteration failed
        if not execution_times:
            return {
                "success": False,
                "status": "FAILED_ALL_TRIALS",
                "total_trials": iterations,
                "failures": failure_count,
                "error_types": list(set(error_logs)),
            }

        return {
            "success": True,
            "status": "SUCCESS" if failure_count == 0 else "PARTIAL_SUCCESS",
            "total_trials": iterations,
            "successful_trials": len(execution_times),
            "failed_trials": failure_count,
            "metrics": {
                "mean_execution_seconds": float(statistics.mean(execution_times)),
                "median_execution_seconds": float(statistics.median(execution_times)),
                "stdev_seconds": (
                    float(statistics.stdev(execution_times))
                    if len(execution_times) > 1
                    else 0.0
                ),
            },
        }
