#!/usr/bin/env python
"""
Cat-Out-Of-The-BOx v2.1.0 Wrapper

A universal wrapper that integrates with ANY program that uses AI models.
Provides task tracking, continuous execution, and diagram-fixing capabilities.

Usage:
    python wrapper.py "Your task description here"
    python wrapper.py --model ollama --model-name llama2 "Summarize this"
    python wrapper.py --diagram "path/to/diagram.png"
    python wrapper.py --task "Analyze data" --diagram "diagram.png"

Features:
- Works with any AI model backend (transformers, ollama, openai)
- Task tracking: input/goal/target/task/checklist/timeline persistence
- Continuous execution without "resume" prompts
- Diagram fixing skill with patent checklist compliance
- Offline-first with cloud fallback
- Chat history persistence across runs
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

# Cat-Out-Of-The-BOx version
VERSION = "2.1.0"
PROJECT = "Cat-Out-Of-The-BOx"

# Default paths
WORKER_DIR = Path(__file__).parent if "__file__" in dir() else Path(".")
CHAT_HISTORY = WORKER_DIR / ".chat_history.json"
TASK_STATE = WORKER_DIR / ".task_state.json"


def get_task_state():
    """Load task state from file if it exists."""
    if TASK_STATE.exists():
        try:
            with open(TASK_STATE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "input": "",
        "goal": "",
        "target": "",
        "current_task": "",
        "checklist": [],
        "timeline": [],
        "iteration": 0,
    }


def save_task_state(state):
    """Save task state to file."""
    try:
        with open(TASK_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def extract_task_info(task_description):
    """Extract input, goal, target from task description."""
    # Simple extraction - can be enhanced with NLP
    lines = []
    input_text = task_description
    goal = task_description
    target = f"Completed: {task_description[:60]}" + ("..." if len(task_description) > 60 else "")
    current_task = task_description

    # Build basic checklist based on task type
    checklist = [
        {"item": "Understand the task", "completed": False},
        {"item": "Execute the task", "completed": False},
        {"item": "Verify results", "completed": False},
        {"item": "Document outcome", "completed": False},
    ]

    # Task-type specific checklists
    task_lower = task_description.lower()
    if "analyze" in task_lower or "analysis" in task_lower:
        checklist = [
            {"item": "Understand the input data/task", "completed": False},
            {"item": "Identify key components", "completed": False},
            {"item": "Generate analysis", "completed": False},
            {"item": "Review and validate", "completed": False},
        ]
    elif "summarize" in task_lower or "summary" in task_lower:
        checklist = [
            {"item": "Identify main points", "completed": False},
            {"item": "Extract key information", "completed": False},
            {"item": "Create summary", "completed": False},
            {"item": "Review summary accuracy", "completed": False},
        ]
    elif "write" in task_lower or "code" in task_lower or "program" in task_lower:
        checklist = [
            {"item": "Understand requirements", "completed": False},
            {"item": "Generate code/solution", "completed": False},
            {"item": "Test and debug", "completed": False},
            {"item": "Document the solution", "completed": False},
        ]

    return {
        "input": input_text,
        "goal": goal,
        "target": target,
        "current_task": current_task,
        "checklist": checklist,
        "timeline": [
            {
                "iteration": 1,
                "input": input_text[:50] + ("..." if len(input_text) > 50 else input_text),
                "task": current_task,
                "goal": goal[:50] + ("..." if len(goal) > 50 else goal),
                "target": target[:50] + ("..." if len(target) > 50 else target),
            }
        ],
    }


def run_worker_with_tracking(task_description, model_backend="transformers", diagram=False, diagram_checklist=None):
    """Run the worker with full task tracking and optional diagram fixing."""
    import sys
    sys.path.insert(0, str(WORKER_DIR))

    from worker import EnhancedChatHistory, TaskState

    # Initialize task state
    state = get_task_state()
    task_info = extract_task_info(task_description)

    # Merge with existing state if continuing
    if state.get("input"):
        task_info["input"] = state["input"]
    if state.get("goal"):
        task_info["goal"] = state["goal"]
    if state.get("target"):
        task_info["target"] = state["target"]
    if state.get("current_task"):
        task_info["current_task"] = state["current_task"]
    if state.get("checklist"):
        task_info["checklist"] = state["checklist"]

    # Initialize enhanced chat history
    eh = EnhancedChatHistory()

    # Update task state with parsed info
    task_info["iteration"] = state.get("iteration", 0) + 1
    eh.task_state.update(
        task_info["input"],
        task_info["goal"],
        task_info["target"],
        task_info["current_task"],
        checklist_item=task_info["checklist"][0]["item"] if task_info["checklist"] else None,
    )

    # Add initial task message with task tracking info
    task_msg = f"Task: {task_description}\n\n"
    task_msg += f"Input: {task_info['input']}\n"
    task_msg += f"Goal: {task_info['goal']}\n"
    task_msg += f"Target: {task_info['target']}\n"
    task_msg += f"Current Task: {task_info['current_task']}\n"
    task_msg += f"\nChecklist:\n"
    for i, item in enumerate(task_info["checklist"], 1):
        task_msg += f"  {i}. [{'✓' if item.get('completed', False) else ' '}] {item['item']}\n"
    task_msg += f"\nTimeline iteration {task_info['iteration']}: Starting task"

    eh.add("user", task_msg)

    # Save updated state
    save_task_state(eh.task_state.to_dict())

    # Run the worker
    try:
        from worker import ContinuousWorker
        worker = ContinuousWorker(backend=model_backend)
        result = worker.run_task(task_description)

        # Update task state with completion
        eh.add("assistant", f"Task result: {str(result)[:500]}...")
        save_task_state(eh.task_state.to_dict())

        # Get updated task state
        final_state = eh.get_task_state()

        # Handle diagram fixing if requested
        if diagram and diagram_checklist:
            try:
                # Import diagram skill
                sys.path.insert(0, str(WORKER_DIR / "cat-out-the-box"))
                from diagram_skill import run_skill
                import json as _json

                # Run diagram fixing
                diagram_result = run_skill(
                    diagram_file=diagram_checklist.get("file", ""),
                    issues=diagram_checklist.get("checklist", {}),
                )

                # Add diagram results to task state
                if "result" in diagram_result:
                    eh.add("assistant", f"Diagram fixing complete: {diagram_result['result'][:300]}...")
                save_task_state(eh.task_state.to_dict())

            except ImportError:
                print("[WARN] Diagram skill not available, continuing without diagram fixing")
            except Exception as e:
                print(f"[WARN] Diagram fixing error: {e}")

        return {
            "task_result": result,
            "task_state": final_state,
            "version": VERSION,
            "project": PROJECT,
        }

    except ImportError as e:
        print(f"[ERROR] Worker import error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Worker execution error: {e}")
        return None


def main():
    """Main entry point for the wrapper."""
    parser = argparse.ArgumentParser(
        prog=f"python wrapper.py",
        description=f"Cat-Out-Of-The-BOx v{VERSION} - Universal AI Worker Wrapper",
    )

    parser.add_argument(
        "task",
        nargs="*",
        help="Task description to accomplish",
    )

    parser.add_argument(
        "--model",
        choices=["transformers", "ollama", "openai"],
        default="transformers",
        help="AI model backend (default: transformers for offline)",
    )

    parser.add_argument(
        "--model-name",
        default="gpt2",
        help="Model name/identifier (default: gpt2 for transformers)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=50,
        help=f"Max iterations before stop (default: 50)",
    )

    parser.add_argument(
        "--continue",
        dest="continue_task",
        action="store_true",
        help="Continue from previous task using saved history",
    )

    parser.add_argument(
        "--diagram",
        metavar="PATH",
        help="Path to diagram file to fix with checklist compliance",
    )

    parser.add_argument(
        "--checklist",
        metavar="JSON",
        help="JSON checklist for diagram fixing (e.g., '{\"f.3\": \"significant-improvements\"}')",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current task status and history",
    )

    parser.add_argument(
        "--new",
        action="store_true",
        help="Start new task (clears history and task state)",
    )

    args = parser.parse_args()

    # Handle /new command
    if args.new:
        # Clear history and task state files
        for f in [CHAT_HISTORY, TASK_STATE]:
            if f.exists():
                f.unlink()
        print("[INFO] New task started - chat history and task state cleared")
        return

    # Handle /status command
    if args.status:
        # Load and display task state
        state = get_task_state()
        chat_state = None
        if CHAT_HISTORY.exists():
            try:
                import json as _json
                with open(CHAT_HISTORY, "r", encoding="utf-8") as f:
                    chat_data = _json.load(f)
                chat_state = {
                    "messages_count": len(chat_data.get("messages", [])),
                    "iteration": chat_data.get("messages", [])[-1].get("content", "")[:100] if chat_data.get("messages") else "No messages yet",
                }
            except Exception:
                pass

        print(f"\n=== Cat-Out-Of-The-BOx v{VERSION} Status ===")
        print(f"Task: {args.task if args.task else 'None'}")
        print(f"Input: {state.get('input', 'Not set')[:100]}..." if state.get('input') else "Input: Not set")
        print(f"Goal: {state.get('goal', 'Not set')[:100]}..." if state.get('goal') else "Goal: Not set")
        print(f"Target: {state.get('target', 'Not set')[:100]}..." if state.get('target') else "Target: Not set")
        print(f"Current Task: {state.get('current_task', 'Not set')[:100]}..." if state.get('current_task') else "Current Task: Not set")
        print(f"Iteration: {state.get('iteration', 0)}")
        print(f"Checklist: {len(state.get('checklist', []))} items")
        print(f"Timeline entries: {len(state.get('timeline', []))}")
        if chat_state:
            last_msg = chat_state.get('last_message', 'No messages yet') if chat_state else 'No messages yet'
        print(f"Last message: {last_msg}")
        print(f"Chat history: {CHAT_HISTORY}")
        print(f"Task state: {TASK_STATE}")
        print(f"Model backend: {args.model}")
        print(f"\nUse 'python wrapper.py --continue' to continue the task")
        print(f"Use 'python wrapper.py --new' to start a new task")
        return

    # Parse task description
    if args.task:
        task_description = " ".join(args.task)
    elif args.diagram:
        # Diagram mode
        try:
            import json as _json
            diagram_checklist = _json.loads(args.checklist) if args.checklist else {"f.3": "significant-improvements", "f.5": "leave-as-is"}
            result = run_worker_with_tracking(
                task_description=f"Diagram fixing: {args.diagram}",
                model_backend=args.model,
                diagram=True,
                diagram_checklist=diagram_checklist,
            )
            if result:
                print(f"\n=== Task Complete ===")
                print(f"Version: {result.get('version', VERSION)}")
                print(f"Project: {result.get('project', PROJECT)}")
                ts = result.get("task_state", {})
                print(f"Iteration: {ts.get('iteration', 0)}")
                print(f"Checklist items: {len(ts.get('checklist', []))}")
                print(f"Timeline entries: {len(ts.get('timeline', []))}")
                print(f"Input: {ts.get('input', '')[:80]}...")
                print(f"Target: {ts.get('target', '')[:80]}...")
            return
        except Exception as e:
            print(f"[ERROR] Diagram mode error: {e}")
            return
    else:
        parser.print_help()
        return

    # Run task with tracking
    result = run_worker_with_tracking(
        task_description=task_description,
        model_backend=args.model,
    )

    if result:
        print(f"\n=== Task Complete ===")
        print(f"Version: {result.get('version', VERSION)}")
        print(f"Project: {result.get('project', PROJECT)}")

        ts = result.get("task_state", {})
        print(f"\n--- Task State ---")
        print(f"Iteration: {ts.get('iteration', 0)}")
        print(f"Input: {ts.get('input', '')[:100]}..." if ts.get('input') else "Input: None")
        print(f"Goal: {ts.get('goal', '')[:100]}..." if ts.get('goal') else "Goal: None")
        print(f"Target: {ts.get('target', '')[:100]}..." if ts.get('target') else "Target: None")
        print(f"Current Task: {ts.get('current_task', '')[:100]}..." if ts.get('current_task') else "Current Task: None")
        print(f"Checklist: {len(ts.get('checklist', []))} items")
        print(f"  Completed: {sum(1 for c in ts.get('checklist', []) if c.get('completed', False))}/{len(ts.get('checklist', []))}")
        print(f"Timeline entries: {len(ts.get('timeline', []))}")

        print(f"\n--- Chat History ---")
        print(f"Saved to: {CHAT_HISTORY}")

        print(f"\n--- Result Summary ---")
        tr = result.get("task_result", {})
        if tr:
            print(f"Task completed: {str(tr)[:200]}...")
    else:
        print("\n[ERROR] Task did not complete successfully")


if __name__ == "__main__":
    main()