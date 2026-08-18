import sys
import time
import json
import argparse
import os
import signal
from datetime import datetime
from pathlib import Path


# ─── MCP (Mini Continuous Planner) Configuration ─────────────────────────

MCP_VERSION = "2.0.0"
DEFAULT_MODEL_TIER = "mid"  # mid, mid-high, high, ultra
MAX_SUBTASKS = 5
HISTORY_FILE = ".mcp_history.json"


# ─── Task Decomposition Engine ────────────────────────────────────────────

class TaskDecomposer:
    """Breaks down complex user tasks into manageable subtasks."""

    @staticmethod
    def decompose(task_description, complexity="medium"):
        """Decompose a task into subtasks based on complexity and size."""

        task = task_description.lower().strip()

        # Simple pattern-based decomposition
        subtasks = []

        # Check for common task types
        if any(kw in task for kw in ["analyze", "analysis", "data", "file"]):
            subtasks.append({
                "id": 1,
                "type": "analysis",
                "description": f"Analyze: {task_description}",
                "model_tier": "mid",
                "estimated_time": "short"
            })

        if any(kw in task for kw in ["summarize", "summary", "text", "document"]):
            subtasks.append({
                "id": 2,
                "type": "summarization",
                "description": f"Summarize: {task_description}",
                "model_tier": "mid",
                "estimated_time": "short"
            })

        if any(kw in task for kw in ["process", "transform", "convert", "format"]):
            subtasks.append({
                "id": 3,
                "type": "processing",
                "description": f"Process/transform: {task_description}",
                "model_tier": "mid-high",
                "estimated_time": "medium"
            })

        if any(kw in task for kw in ["create", "generate", "write", "code", "script"]):
            subtasks.append({
                "id": 4,
                "type": "generation",
                "description": f"Generate/create: {task_description}",
                "model_tier": "mid-high",
                "estimated_time": "medium"
            })

        if any(kw in task for kw in ["search", "find", "look up", "research"]):
            subtasks.append({
                "id": 5,
                "type": "research",
                "description": f"Research: {task_description}",
                "model_tier": "mid",
                "estimated_time": "medium"
            })

        # If no specific pattern matched, create a general task
        if not subtasks:
            subtasks.append({
                "id": 1,
                "type": "general",
                "description": task_description,
                "model_tier": DEFAULT_MODEL_TIER,
                "estimated_time": "medium"
            })

        # Limit to max subtasks
        subtasks = subtasks[:MAX_SUBTASKS]

        # If only one subtask was found but user task is long, split further
        if len(subtasks) == 1 and len(task) > 100:
            subtasks.append({
                "id": 2,
                "type": "general",
                "description": f"Process main request: {task_description}",
                "model_tier": DEFAULT_MODEL_TIER,
                "estimated_time": "medium"
            })

        return subtasks


# ─── Model Router ────────────────────────────────────────────────────────

class ModelRouter:
    """Routes subtasks to appropriate model tiers based on complexity."""

    TIER_CONFIGS = {
        "low": {"model_range": "2b-8b", "capability": "simple queries, classification"},
        "mid": {"model_range": "8b-13b", "capability": "analysis, summarization, reasoning"},
        "mid-high": {"model_range": "13b-70b", "capability": "complex analysis, coding, generation"},
        "high": {"model_range": "70b-150b", "capability": "expert reasoning, complex coding"},
        "ultra": {"model_range": "150b+", "capability": "frontier models, research"}
    }

    @staticmethod
    def get_tier_config(tier):
        return ModelRouter.TIER_CONFIGS.get(tier, ModelRouter.TIER_CONFIGS["mid"])

    @staticmethod
    def route_subtask(subtask):
        """Determine the appropriate model tier for a subtask."""
        task_type = subtask["type"].lower()
        description = subtask["description"].lower()

        if task_type in ["generation", "coding"]:
            return "mid-high" if "simple" not in description else "mid"
        elif task_type in ["analysis", "research"]:
            return "mid-high"
        elif task_type in ["summarization"]:
            return "mid"
        else:
            return DEFAULT_MODEL_TIER


# ─── MCP Engine ──────────────────────────────────────────────────────────

class MCP_Engine:
    """Main MCP (Mini Continuous Planner) engine."""

    def __init__(self):
        self.running = True
        self.task_history = []
        self.setup_signals()

    def setup_signals(self):
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        self.running = False
        print("\n[INTERRUPT] Received signal to stop...")

    def run(self, user_task, model_tier=DEFAULT_MODEL_TIER, use_history=False):
        """Run the MCP planner on a user task."""

        print("=" * 60)
        print(f"MCP {MCP_VERSION} - Mini Continuous Planner")
        print("=" * 60)
        print()
        print(f"[TASK] User request: {user_task}")
        print(f"[MODEL] Tier: {model_tier}")
        print()

        # Step 1: Decompose the task
        print("[PLAN] Decomposing task into subtasks...")
        subtasks = TaskDecomposer.decompose(user_task, model_tier)

        print(f"[PLAN] Decomposed into {len(subtasks)} subtask(s):")
        for i, subtask in enumerate(subtasks, 1):
            tier_config = ModelRouter.get_tier_config(subtask["model_tier"])
            print(f"  {i}. [{subtask['type']}] {subtask['description'][:60]}...")
            print(f"     Model tier: {subtask['model_tier']} ({tier_config['model_range']})")
            print(f"     Estimated: {subtask['estimated_time']}")
        print()

        # Step 2: Generate the execution blueprint/script
        print("[BUILD] Generating mini-script/blueprint...")
        blueprint = self._generate_blueprint(subtasks, model_tier)

        print("[BUILD] Blueprint generated:")
        print("-" * 60)
        print(blueprint)
        print("-" * 60)
        print()

        # Step 3: Provide options
        print("[OPTIONS]")
        print("  1. Run script now with Cat-Out-Of-The-BOx worker")
        print("  2. Save script to file for later execution")
        print("  3. Modify subtasks manually")
        print("  4. Run with different model tier")
        print("  5. Exit")

        return blueprint, subtasks

    def _generate_blueprint(self, subtasks, model_tier):
        """Generate a mini-script/blueprint from the subtasks."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blueprint_name = f"mcp_blueprint_{timestamp}.py"

        # Start the script
        lines = []
        lines.append("# ")
        lines.append(f"# MCP Generated Blueprint")
        lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Original task: {' '.join(subtasks[0]['description'].split()[:20])}...")
        lines.append(f"# Subtasks: {len(subtasks)}")
        lines.append(f"# Model tier: {model_tier}")
        lines.append("# ")
        lines.append("# This script was generated by MCP v2")
        lines.append("# Run with: python worker.py \"<task>\" or execute directly")
        lines.append("# ")
        lines.append("# Auto-generated subtasks:")
        lines.append("# ")

        # Add each subtask as a comment/task
        for i, subtask in enumerate(subtasks, 1):
            lines.append(f"#   {i}. {subtask['type']}: {subtask['description'][:80]}")
        lines.append("# ")

        # Add main execution logic
        lines.append("#")
        lines.append("# EXECUTION LOGIC")
        lines.append("#")
        lines.append("import sys")
        lines.append("import time")
        lines.append("from worker import ContinuousWorker")
        lines.append("# ")
        lines.append("worker = ContinuousWorker()")
        lines.append("# ")
        lines.append("# Run each subtask sequentially")
        lines.append("#")

        for i, subtask in enumerate(subtasks, 1):
            lines.append(f"# Subtask {i}: {subtask['type']}")
            lines.append(f"# Description: {subtask['description'][:100]}")
            lines.append(f"# Model: {subtask['model_tier']}")
            lines.append("worker.run_task(")
            lines.append(f'    """{subtask["description"]}"""')
            lines.append(")")
            lines.append("")

        # Add completion notice
        lines.append("#")
        lines.append("# When complete, the worker will have processed all subtasks")
        lines.append("# Review .chat_history.json for results")
        lines.append("#")
        lines.append("# To execute this blueprint:")
        lines.append("#   python worker.py \"<task description>\"")
        lines.append("#   # Or run this generated script directly")
        lines.append("# ")

        # Join all lines
        blueprint = "\n".join(lines)

        # Also save to file
        try:
            with open(blueprint_name, "w", encoding="utf-8") as f:
                f.write(blueprint)
            print(f"  [SAVE] Blueprint saved to: {blueprint_name}")
        except Exception as e:
            print(f"  [WARN] Could not save blueprint file: {e}")

        return blueprint

    def start_interactive(self):
        """Start MCP in interactive mode."""
        if len(sys.argv) < 2:
            print("=" * 60)
            print("MCP v2 - Interactive Mode")
            print("=" * 60)
            print()
            print("Usage: python mcp.py \"Your task description\" [options]")
            print()
            print("Options:")
            print("  --tier MID/MED-HIGH/HIGH    Model tier to use")
            print("  --history                   Use saved chat history")
            print("  --list-tiers                Show available model tiers")
            print()
            print("Model Tiers:")
            print("  mid       - 8b-13b models (good for analysis, summarization)")
            print("  mid-high  - 13b-70b models (good for coding, complex generation)")
            print("  high      - 70b-150b models (expert reasoning)")
            print()
            print("Examples:")
            print('  python mcp.py "Analyze this data and generate a summary"')
            print('  python mcp.py --tier high "Write a Python script to process CSV"')
            print()
            sys.exit(1)

        # Parse arguments
        task_parts = []
        model_tier = DEFAULT_MODEL_TIER
        use_history = False

        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--tier" and i + 1 < len(sys.argv):
                model_tier = sys.argv[i + 1]
                i += 2
            elif arg == "--history":
                use_history = True
                i += 1
            elif arg == "--list-tiers":
                self._list_tiers()
                sys.exit(0)
            else:
                task_parts.append(arg)
                i += 1

        user_task = " ".join(task_parts)

        if not user_task:
            print("[ERROR] No task provided")
            sys.exit(1)

        # Run MCP
        blueprint, subtasks = self.run(user_task, model_tier, use_history)

        # Ask what to do next
        print()
        print("=" * 60)
        print("Next steps:")
        print("=" * 60)
        print()
        print("The generated blueprint above can be:")
        print("  1. Run directly with: python worker.py \"<task>\"")
        print("  2. Save and execute later")
        print("  3. Modify the subtasks and regenerate")
        print()
        print("The MCP will now monitor completion or wait for your command.")

    def _list_tiers(self):
        """List available model tiers."""
        print("Available Model Tiers:")
        print("=" * 40)
        for tier, config in ModelRouter.TIER_CONFIGS.items():
            print(f"  {tier:10} - {config['model_range']:15} - {config['capability']}")


# ─── Entry Point ────────────────────────────────────────────────────────

def main():
    mcp = MCP_Engine()
    mcp.start_interactive()


if __name__ == "__main__":
    main()