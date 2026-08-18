import sys
import time
import signal
import os
import json
import requests
from datetime import datetime


class ContinuousWorker:
    """Version 1: Continuous AI worker that runs tasks without stopping to prompt."""

    def __init__(self):
        self.running = True
        self.task_completed = False
        self.setup_signals()

    def setup_signals(self):
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        self.running = False
        print("\n[INTERRUPT] Received signal to stop...")

    def check_conditions(self):
        """Check practical reasons to stop - limits, space, etc."""
        reasons = []

        # Check disk space
        try:
            stat = os.statvfs('.')
            free_gb = stat.f_bavail * stat.f_frsize / (1024 ** 3)
            if free_gb < 1.0:
                reasons.append(f"Low disk space: {free_gb:.1f}GB free")
        except Exception:
            pass

        # Check estimated time (max 24 hours continuous)
        # Would be customized per task

        # Check API rate limits if using external AI
        # Would be customized per integration

        return reasons

    def run_task(self, task_description, max_iterations=100):
        """Run a task continuously until completion or stop condition."""
        print(f"[TASK] Starting: {task_description}")
        print(f"[STATUS] Worker active - will run until complete or stop condition met")
        print(f"[STATUS] Press Ctrl+C to interrupt early\n")

        iteration = 0
        start_time = time.time()

        while self.running and iteration < max_iterations:
            iteration += 1
            current_time = time.time()
            elapsed = current_time - start_time

            # Check stop conditions
            conditions = self.check_conditions()
            if conditions:
                for cond in conditions:
                    print(f"[WARNING] {cond}")

            # Execute task step - this is where AI model would be called
            step_result = self._execute_step(task_description, iteration)

            if step_result.get('completed', False):
                self.task_completed = True
                print(f"\n[TASK] Completed in {iteration} iterations ({elapsed:.1f}s)")
                print(f"[RESULT] {step_result.get('result', 'Task completed')}")
                return True

            # Brief pause to prevent CPU spinning and allow signal checking
            # In real implementation, this is where AI model call happens
            time.sleep(0.1)

        if iteration >= max_iterations:
            print(f"\n[LIMIT] Reached max iterations: {max_iterations}")

        return False

    def _execute_step(self, task_description, iteration):
        """Execute one step of the task.

        Override this method in subclasses or customize for your AI integration.
        The base implementation simulates progress for Version 1.
        """
        # Display progress
        print(f"[STEP {iteration}] Working on: {task_description[:60]}...")

        # Demo: mark complete after a few iterations
        # Remove this logic and replace with actual AI model call
        if iteration >= 3:
            return {
                'completed': True,
                'result': f'Task completed: Analyzed "{task_description[:50]}..."'
            }

        # Simulate work
        # time.sleep(0.5)  # Uncomment for real timing

        return {'completed': False}

    def watchdog(self, check_interval=5, max_wait=300):
        """Alarm clock watchdog - monitors and alerts if worker stops unexpectedly."""
        print(f"[WATCHDOG] Starting monitor (check every {check_interval}s, max {max_wait}s wait)")

        wait_time = 0
        while wait_time < max_wait:
            if not self.running:
                print(f"[WATCHDOG] Worker stopped at {wait_time}s - would attempt restart")
                print("[WATCHDOG] To auto-restart, integrate with your task scheduler")
                return False
            time.sleep(check_interval)
            wait_time += check_interval

        print("[WATCHDOG] Max wait time reached - keeping current state")
        return True

    def start(self):
        """Main entry point for the continuous worker."""
        if len(sys.argv) < 2:
            print("=" * 60)
            print("Cat-Out-Of-The-BOx Version 1")
            print("=" * 60)
            print()
            print("A tool to help AI models work continuously toward goals")
            print("without constant prompting or resuming.")
            print()
            print("Usage:")
            print("  python worker.py \"Your task description here\"")
            print()
            print("Examples:")
            print('  python worker.py "Analyze sales data and generate report"')
            print('  python worker.py "Process all CSV files in this directory"')
            print('  python worker.py "Summarize this document and extract key points"')
            print()
            print("How it works:")
            print("  - Task runs in a continuous loop without stopping to prompt")
            print("  - Checks practical stop conditions (disk space, limits)")
            print("  - Watchdog monitors for unexpected stops")
            print("  - Ctrl+C handles graceful interruption")
            print("  - Max iterations configurable (default: 100)")
            sys.exit(1)

        task_description = ' '.join(sys.argv[1:])

        try:
            print(f"[START] {datetime.now().strftime('%H:%M:%S')}")
            print()

            # Run the task
            completed = self.run_task(task_description)

            print()
            if completed:
                print("✓ Task completed successfully!")
                print(f"[END] {datetime.now().strftime('%H:%M:%S')}")
            else:
                print("✗ Task did not complete (interrupted or limit reached)")
                print(f"[END] {datetime.now().strftime('%H:%M:%S')}")

        except KeyboardInterrupt:
            print("\n[INTERRUPT] User interrupted the task")
        finally:
            self.running = False


def upload_file(file_path, url="https://paste.rs"):
    """Upload a file to paste.rs and return the URL."""
    try:
        with open(file_path, "rb") as f:
            resp = requests.put(url, data=f)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return f"Upload failed: {resp.status_code}"
    except Exception as e:
        return f"Upload error: {e}"


if __name__ == "__main__":
    worker = ContinuousWorker()
    worker.start()