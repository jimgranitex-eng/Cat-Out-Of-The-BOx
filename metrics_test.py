import time
import json
import os
import sys


class MetricsTester:
    """Run real-time metrics tests on the MCP/worker system."""
    
    def __init__(self):
        self.metrics = {
            "task_times": [],
            "memory_usage": [],
            "iterations": []
        }
    
    def test_task_execution(self, task_description, iterations=3):
        """Test task execution and measure metrics."""
        print(f"[TEST] Running: {task_description}")
        print(f"[STATUS] Iterations: {iterations}")
        print()
        
        for i in range(iterations):
            # Get baseline metrics
            start_time = time.time()
            memory_before = self._get_memory_mb()
            
            # Run the task
            import subprocess
            result = subprocess.run(
                ["python", "worker.py", task_description],
                capture_output=True,
                text=True,
                cwd="C:\\Users\\ssjin\\Desktop\\Cat-Out-Of-The-BOx",
                timeout=60
            )
            
            # Get post-task metrics
            elapsed = time.time() - start_time
            memory_after = self._get_memory_mb()
            
            # Record metrics
            self.metrics["task_times"].append(elapsed)
            self.metrics["memory_usage"].append({
                "before_mb": round(memory_before, 2),
                "after_mb": round(memory_after, 2),
                "delta_mb": round(memory_after - memory_before, 2)
            })
            self.metrics["iterations"].append(i + 1)
            
            print(f"[ITERATION {i+1}] Completed in {elapsed:.2f}s")
            print(f"[MEMORY] Before: {memory_before:.1f}MB, After: {memory_after:.1f}MB (Δ: {memory_after - memory_before:.1f}MB)")
            print(f"[EXIT CODE] {result.returncode}")
            print()
        
        # Print summary
        self.print_summary()
    
    def _get_memory_mb(self):
        """Get current memory usage in MB."""
        try:
            import psutil
            return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        except ImportError:
            # Fallback: just return 0 if psutil not available
            return 0.0
    
    def print_summary(self):
        """Print test summary with metrics."""
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        if self.metrics["task_times"]:
            avg_time = sum(self.metrics["task_times"]) / len(self.metrics["task_times"])
            print(f"✓ Average task time: {avg_time:.2f}s")
            print(f"✓ Min task time: {min(self.metrics['task_times']):.2f}s")
            print(f"✓ Max task time: {max(self.metrics['task_times']):.2f}s")
        
        if self.metrics["memory_usage"] and any(m["delta_mb"] for m in self.metrics["memory_usage"]):
            avg_mem_delta = sum(m["delta_mb"] for m in self.metrics["memory_usage"] if m["delta_mb"]) / len([m for m in self.metrics["memory_usage"] if m["delta_mb"]])
            print(f"✓ Average memory delta: {avg_mem_delta:.1f}MB")
        
        print(f"✓ Total tasks tested: {len(self.metrics['task_times'])}")
        print("=" * 60)


if __name__ == "__main__":
    tester = MetricsTester()
    
    print("MCP/Worker Metrics Test")
    print(f"Python: {sys.version.split()[0]}")
    print(f"psutil available: {__import__('psutil', fromlist=['']).__version__ if __import__('psutil', fromlist=['']) else 'No'}")
    print()
    
    # Run test with small task
    tester.test_task_execution("Test continuous AI worker with history", iterations=3)