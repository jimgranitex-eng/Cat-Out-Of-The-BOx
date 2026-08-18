import sys
import time
import signal
import os
from datetime import datetime

class ContinuousWorker:
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
        
        # Check if out of space (simple check)
        try:
            stat = os.statvfs('.')
            free_gb = stat.f_bavail * stat.f_frsize / (1024**3)
            if free_gb < 1.0:
                reasons.append(f"Low disk space: {free_gb:.1f}GB free")
        except:
            pass
        
        # Check time limit (24 hours max)
        # This would be customized per task
        
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
            
            # Execute task step
            step_result = self._execute_step(task_description, iteration)
            
            if step_result.get('completed', False):
                self.task_completed = True
                print(f"\n[TASK] Completed in {iteration} iterations ({elapsed:.1f}s)")
                return True
            
            # Brief pause to prevent CPU spinning and allow signal checking
            time.sleep(0.1)
        
        if iteration >= max_iterations:
            print(f"\n[LIMIT] Reached max iterations: {max_iterations}")
        
        return False
    
    def _execute_step(self, task_description, iteration):
        """Execute one step of the task. Override or customize this."""
        # Placeholder - in version 1, we just simulate progress
        # In real use, this would call the AI model
        print(f"[STEP {iteration}] Working on: {task_description[:50]}...")
        
        # Simulate work - remove this in real implementation
        # time.sleep(0.5)
        
        # For demo: mark complete after a few iterations
        if iteration >= 3:
            return {'completed': True, 'result': 'Demo task complete'}
        
        return {'completed': False}
    
    def watchdog(self, check_interval=5, max_wait=300):
        """Alarm clock watchdog - monitors and restarts if stopped unexpectedly."""
        print(f"[WATCHDOG] Starting monitor (check every {check_interval}s, max {max_wait}s wait)")
        
        wait_time = 0
        while wait_time < max_wait:
            if not self.running:
                print(f"[WATCHDOG] Worker stopped at {wait_time}s - attempting restart...")
                # In a real implementation, this would restart the worker
                # For now, just alert
                return False
            time.sleep(check_interval)
            wait_time += check_interval
        
        print("[WATCHDOG] Max wait time reached")
        return True
    
    def start(self):
        """Main entry point."""
        if len(sys.argv) < 2:
            print("Usage: python worker.py <task_description>")
            print("Example: python worker.py 'Analyze this data file and generate report'")
            sys.exit(1)
        
        task_description = ' '.join(sys.argv[1:])
        
        try:
            # Run the task
            completed = self.run_task(task_description)
            
            if completed:
                print("\n✓ Task completed successfully!")
            else:
                print("\n✗ Task did not complete (interrupted or limit reached)")
                
        except KeyboardInterrupt:
            print("\n[INTERRUPT] User interrupted the task")
        finally:
            self.running = False


if __name__ == "__main__":
    worker = ContinuousWorker()
    worker.start()