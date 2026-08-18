import sys
import json
import os
import argparse
from datetime import datetime
from pathlib import Path


# ─── Bridge Connector Configuration ───────────────────────────────────────

BRIDGE_VERSION = "1.0.0"

# Task type mapping: user input patterns -> task category
# The KEY is what the user might type, the VALUE is the internal task category
TASK_TYPE_MAPPING = {
    # Art & Visual Tasks
    "draw": "artist",
    "drawing": "artist",
    "sketch": "artist",
    "art": "artist",
    "create art": "artist",
    "create image": "artist",
    "paint": "artist",
    "painting": "artist",

    # Text & Writing Tasks
    "write": "writer",
    "writing": "writer",
    "summarize": "writer",
    "summary": "writer",
    "analyze": "analyst",
    "analysis": "analyst",
    "describe": "analyst",
    "description": "analyst",

    # Code & Programming Tasks
    "code": "coder",
    "coding": "coder",
    "program": "coder",
    "programming": "coder",
    "script": "coder",
    "website": "coder",

    # Data & Analysis Tasks
    "data": "analyst",
    "analyze data": "analyst",
    "csv": "analyst",
    "excel": "analyst",
    "statistics": "analyst",

    # File & Document Tasks
    "file": "handler",
    "document": "handler",
    "pdf": "handler",
    "text file": "handler",

    # General/AI Tasks
    "chat": "conversation",
    "talk": "conversation",
    "help": "conversation",
    "answer": "conversation",
    "explain": "conversation",
    "learn": "conversation",
}

# Bridge mappings: task type -> (worker tool, mcp subtask, description)
BRIDGE_TARGETS = {
    "artist": {
        "worker_tool": "worker",
        "mcp_subtask": "generation",
        "description": "Uses worker.py's continuous generation capability with transformers backend to create images/descriptions",
        "requires_model": True,
    },
    "writer": {
        "worker_tool": "worker",
        "mcp_subtask": "generation",
        "description": "Uses worker.py's text generation with chat history to create written content",
        "requires_model": True,
    },
    "analyst": {
        "worker_tool": "worker",
        "mcp_subtask": "analysis",
        "description": "Uses worker.py's analysis capability with chat history to process data, text, or information",
        "requires_model": True,
    },
    "coder": {
        "worker_tool": "worker",
        "mcp_subtask": "generation",
        "description": "Uses worker.py's code generation with appropriate model tier (mid-high for coding tasks)",
        "requires_model": True,
    },
    "handler": {
        "worker_tool": "worker",
        "mcp_subtask": "processing",
        "description": "Uses worker.py's file processing and transformation capabilities",
        "requires_model": True,
    },
    "conversation": {
        "worker_tool": "worker",
        "mcp_subtask": "general",
        "description": "Uses worker.py's conversational AI with chat history maintenance",
        "requires_model": True,
    },
    "general": {
        "worker_tool": "worker",
        "mcp_subtask": "general",
        "description": "Uses worker.py's general AI capability",
        "requires_model": True,
    },
}


# ─── Task Analyzer ────────────────────────────────────────────────────────

class TaskAnalyzer:
    """Analyzes user input to determine task type and requirements."""

    def __init__(self):
        self.task_type = None
        self.confidence = 0
        self.extracted_elements = []

    def analyze(self, user_input):
        """Analyze user input and determine the best task type match."""
        user_lower = user_input.lower().strip()

        # Check for exact matches and partial matches
        scores = {}
        for task_type, category in TASK_TYPE_MAPPING.items():
            score = 0
            # Check if the task type KEY is in the user input
            if task_type in user_lower:
                score = 10  # High score for direct keyword match
            # Also check if any word in the input matches the category
            # (for cases like "draw a dog" -> "draw" keyword matches)
            for word in user_lower.split():
                if word == task_type:
                    score = max(score, 5)
            # Check if user input starts with or contains key phrases
            if user_lower.startswith(task_type) or user_lower.endswith(task_type):
                score = max(score, 8)
            scores[task_type] = score

        # Find best match (highest score)
        if scores:
            best_type = max(scores, key=scores.get)
            self.confidence = scores[best_type]
            self.task_type = best_type

            # Extract elements - remove the task type keyword and common words
            elements = user_lower
            # Remove the detected task type
            if self.task_type in elements:
                elements = elements.replace(self.task_type, "").strip()
            # Remove common task-starting words
            for word in ["draw", "me", "a", "an", "the", "of", "with", "to", "for"]:
                elements = elements.replace(word, " ").strip()
            self.extracted_elements = [e.strip() for e in elements.split() if e.strip()]
        else:
            self.task_type = "general"
            self.confidence = 1
            self.extracted_elements = [user_lower]

        return self.task_type, self.confidence, self.extracted_elements

    def get_bridge_info(self):
        """Get the bridge configuration for the detected task type."""
        if self.task_type in BRIDGE_TARGETS:
            return BRIDGE_TARGETS[self.task_type]
        return BRIDGE_TARGETS.get("general", {
            "worker_tool": "worker",
            "mcp_subtask": "general",
            "description": "Uses worker.py's general AI capability",
            "requires_model": True,
        })


# ─── Bridge Executor ─────────────────────────────────────────────────────

class BridgeExecutor:
    """Executes tasks using the bridge pattern - direct connection to exact tool needed."""

    def __init__(self):
        self.history = []

    def execute_with_bridge(self, user_task, use_history=False, model_tier="mid"):
        """Execute task using bridge pattern - direct tool connection."""

        # Step 1: Analyze the task
        analyzer = TaskAnalyzer()
        task_type, confidence, elements = analyzer.analyze(user_task)

        # Step 2: Get bridge configuration
        bridge_config = analyzer.get_bridge_info()

        # Step 3: Build execution command
        worker_tool = bridge_config["worker_tool"]
        mcp_subtask = bridge_config["mcp_subtask"]
        description = bridge_config["description"]

        # Step 4: Construct the task description for worker.py
        # Combine user task with the detected type for better AI understanding
        enhanced_task = f"[Task Type: {task_type}] {user_task}"
        if elements:
            enhanced_task += f" [Elements: {', '.join(elements[:3])}]"

        # Step 5: Run the worker with appropriate parameters
        import subprocess
        cmd = [
            "python", "worker.py",
            "--model", "transformers",
            "--max-iterations", "10",
            enhanced_task
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="C:\\Users\\ssjin\\Desktop\\Cat-Out-Of-The-BOx",
                timeout=60
            )

            # Record the bridge usage
            bridge_record = {
                "timestamp": datetime.now().isoformat(),
                "original_task": user_task,
                "detected_type": task_type,
                "confidence": confidence,
                "bridge_used": worker_tool,
                "mcp_subtask": mcp_subtask,
                "execution_success": result.returncode == 0,
                "output": result.stdout[-500:] if result.stdout else "",
                "error": result.stderr[-200:] if result.stderr else "",
            }
            self.history.append(bridge_record)

            return {
                "success": result.returncode == 0,
                "task_type": task_type,
                "confidence": confidence,
                "bridge_used": worker_tool,
                "mcp_subtask": mcp_subtask,
                "description": description,
                "output": result.stdout,
                "error": result.stderr,
                "enhanced_task": enhanced_task,
            }

        except Exception as e:
            return {
                "success": False,
                "task_type": task_type,
                "confidence": confidence,
                "bridge_used": "worker",
                "mcp_subtask": "general",
                "description": "Uses worker.py's general AI capability",
                "output": "",
                "error": str(e),
            }

    def get_execution_summary(self):
        """Get summary of all bridge executions."""
        if not self.history:
            return "No executions recorded."

        summary = f"Bridge Execution Summary ({len(self.history)} executions):\n"
        summary += "=" * 60 + "\n"

        for record in self.history[-10:]:  # Last 10 executions
            summary += f"\n📋 Task: {record['original_task'][:60]}..."
            summary += f"\n  Type: {record['detected_type']} (confidence: {record['confidence']})"
            summary += f"\n  Bridge: {record['bridge_used']}"
            summary += f"\n  Subtask: {record['mcp_subtask']}"
            summary += f"\n  Success: {record['execution_success']}"
            summary += f"\n  Output: {record['output'][:100]}..."
            summary += "\n" + "-" * 60 + "\n"

        return summary


# ─── Bridge Console ──────────────────────────────────────────────────────

class BridgeConsole:
    """Console interface for the bridge connector system."""

    def __init__(self):
        self.executor = BridgeExecutor()

    def run(self):
        """Run the bridge console interface."""
        print("=" * 60)
        print(f"Bridge Connector v{BRIDGE_VERSION}")
        print("Intelligent task routing using bridge pattern")
        print("=" * 60)
        print()
        print("The bridge connector analyzes your request and")
        print("directly connects to the exact tool needed (no permanent")
        print("integrations - just-in-time tool selection).")
        print()
        print("Examples:")
        print('  "build me a drawing of a dog with labels"')
        print('  "write a python script to process csv"')
        print('  "analyze this data and summarize"')
        print('  "create a summary report"')
        print()
        print("Type 'quit' or 'exit' to stop.")
        print()

        while True:
            try:
                user_input = input("\n🔗 What would you like to build/create/analyze? ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Goodbye! The bridge connector will remember your")
                    print("   execution history for future optimization.")
                    break

                if not user_input:
                    continue

                # Execute via bridge
                print("\n" + "─" * 60)
                result = self.executor.execute_with_bridge(user_input)

                print(f"\n📊 Analysis:")
                print(f"   Detected type: {result['task_type']}")
                print(f"   Confidence: {result['confidence']}")
                print(f"\n🌉 Bridge Used: {result['bridge_used']}")
                print(f"   MCP Subtask: {result['mcp_subtask']}")
                print(f"   Description: {result['description']}")

                print(f"\n📤 Output ({len(result['output'])} chars):")
                if result['output']:
                    # Display first part of output, trimmed
                    display_output = result['output'][:500]
                    if len(result['output']) > 500:
                        display_output += "... [truncated]"
                    print(display_output)
                else:
                    print("(no output generated)")

                if result['error']:
                    print(f"\n⚠️ Errors ({len(result['error'])} chars):")
                    print(result['error'][:300] + ("..." if len(result['error']) > 300 else ""))

                print(f"\n📄 Enhanced Task: {result['enhanced_task']}")
                print("─" * 60)

            except KeyboardInterrupt:
                print("\n\n👋 Bridge connector interrupted. History saved.")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")


# ─── Entry Point ────────────────────────────────────────────────────────

def main():
    console = BridgeConsole()

    # Check for command-line argument
    if len(sys.argv) > 1:
        user_task = " ".join(sys.argv[1:])
        print("=" * 60)
        print("Bridge Connector v1.0.0")
        print("=" * 60)
        print(f"\nRequest: {user_task}")
        print()

        result = console.executor.execute_with_bridge(user_task)

        print(f"\n📊 Analysis:")
        print(f"   Detected type: {result['task_type']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"\n🌉 Bridge Used: {result['bridge_used']}")
        print(f"   MCP Subtask: {result['mcp_subtask']}")
        print(f"   Description: {result['description']}")

        print(f"\n📤 Output:")
        if result['output']:
            print(result['output'][:1000])
        else:
            print("(no output)")

        if result['error']:
            print(f"\n⚠️ Error: {result['error'][:500]}")

        print("\n" + "=" * 60)
    else:
        # Run console interface
        console.run()


if __name__ == "__main__":
    main()