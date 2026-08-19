# Cat-Out-Of-The-BOx v2.1.0

[![GitHub Stars](https://img.shields.io/github/stars/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx/stargazers)
[![GitHub License](https://img.shields.io/github/license/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx/blob/main/LICENSE)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx/commits/main)

## AI that works from start to end without stopping to prompt.

**Version 2.1.0: Continuous AI Worker with Task Tracking and Offline Support**

A tool to help AI models work continuously toward goals without constant prompting/resuming,
with full chat history tracking, task state persistence, and offline model support.

**Key v2.1.0 Enhancements:**
- 🆕 **Task tracking**: Input/goal/target/task/checklist/timeline persistence
- 🆕 **No resume cycle**: Runs start-to-end in one continuous session
- 🆕 **Diagram skill**: Automatic diagram fixing with checklist compliance
- 🆕 **Offline-first**: Works without API keys, transformers backend

---

## 📦 Features

### Core Features (Version 1)
- **Continuous task execution**: Runs tasks in a loop without stopping to ask "continue?"
- **Auto-detection of stop conditions**: Checks for practical limits (disk space, iteration limits, etc.)
- **Watchdog/alarm clock monitor**: Detects if worker stops and can attempt restart
- **Keyboard interrupt handling**: Graceful Ctrl+C handling
- **Configurable iteration limits**: Safety limit to prevent runaway processes (default: 50)

### New Version 2 Features
- **Chat history tracking**: Full conversation history saved to `.chat_history.json`
  - History persists between runs - AI remembers previous context
  - Automatic saving and loading of conversation state
  - History file can be inspected/edited manually
- **Offline AI model support**: Works with local transformers models
  - No API key needed for offline mode
  - Falls back to `gpt2` for maximum compatibility
  - Supports Ollama and OpenAI API backends
- **Control commands during task**: Respond to special commands
  - `/new` - Start new task (clears history)
  - `/stop` - Stop the worker
  - `/status` - Show worker status and history count
  - `/continue` - Continue current task
- **Model backend flexibility**: Choose between
  - `transformers` - Offline local models (default, recommended)
  - `ollama` - Ollama local models (requires Ollama running)
  - `openai` - OpenAI API (requires OPENAI_API_KEY)
- **Task continuity**: AI uses chat history to guide work toward goal
  - Maintains context across iterations
  - Remembers previous task progress
  - Can resume from where it left off
- **v2.1.0 Task Tracking**: Input/goal/target/task/checklist/timeline persistence
- **Diagram skill**: Automatic diagram fixing with checklist compliance

### v2.1.0 New: Task Tracking System
- **Input**: Raw user input/request tracking
- **Goal**: What user ultimately wants to accomplish
- **Target**: Specific measurable deliverable
- **Current task**: What being worked on right now
- **Checklist**: Items to complete, with completion status
- **Timeline**: Iteration-by-iteration progress record
- **Persistent storage**: Saves to `.task_state.json` and `.chat_history.json`

### v2.1.0 New: Diagram Fixing Skill
- **Continuous execution**: Runs from start to end without stopping to prompt "continue?"
- **Checklist-driven**: Applies spacing, margins, flow correction per patent requirements
- **f.3**: Significant improvements (spacing, margins, flow correction)
- **f.5**: Left as-is per user specification
- **Other files**: Reviewed and corrected for consistency
- **Output**: Fixed diagrams saved back to tester folder

---

## 🚀 Usage

### Basic Usage (Offline Transformers - No API Key Needed)
```bash
python worker.py "Your task description here"
```

### With Model Selection
```bash
python worker.py --model ollama --model-name llama2 "Summarize this text"
python worker.py --model openai "Analyze this data"  # Needs OPENAI_API_KEY
python worker.py --model transformers --model-name gpt2 "Your task"
```

### With Options
```bash
python worker.py --max-iterations 20 "Process this file"
python worker.py --continue "Continue previous task"
python worker.py --tier mid "Analysis task"
```

### Control Commands (During Task)
Type `/new`, `/stop`, `/status`, or `/continue` in response to AI prompts

### Diagram Fixing Skill
```bash
diagram-skill "path/to/diagram.png" '{"f.3": "significant-improvements", "f.5": "leave-as-is"}'
```

### Task Tracking Integration
The worker automatically tracks and persists:
- Input, goal, target, current task
- Checklist items with completion status
- Timeline of iteration progress
- Saved to `.task_state.json` for future runs

---

## 📦 Repository Structure

```
Cat-Out-Of-The-BOx/
├── worker.py              # Main continuous AI worker (v2.1.0)
├── mcp.py                 # Mini Continuous Planner v2.0.0
├── bridge_connector.py    # Bridge connector utility
├── upload.py              # File upload utility (paste.rs)
├── metrics_test.py        # Performance testing script
├── CHECKLIST.md           # Complete feature inventory & next version plans
├── FLOWCHART_INTERNAL.md  # Internal engine working diagram
├── FLOWCHART_USAGE.md     # Step-by-step usage flow diagram
├── GRADE.md               # Formal a++ rating document
├── LOGO.txt               # ASCII text logo
├── README.md              # This file
├── .chat_history.json     # Auto-generated chat history (gitignored)
└── .task_state.json       # Task state persistence (gitignored)
```

### Generated Output
- `.chat_history.json` - Auto-generated chat history
- `mcp_blueprint_*.py` - Generated execution blueprints

### Integration Tools
- `integration/opencode/` - opencode CLI integration
- `diagram-skill.py` - Diagram fixing skill for opencode
- `diagram-skill.cmd` - Windows command wrapper

---

## 🛠️ Installing and Using Offline Models

### Option 1: Offline Transformers (Recommended - No API Key)
```bash
# Install dependencies
pip install transformers huggingface-hub tokenizers

# Run with offline model
python worker.py "Your task here"
# Uses microsoft/DialoGPT-small by default, falls back to gpt2

# Use a specific model
python worker.py --model transformers --model-name gpt2 "Your task"
```

### Option 2: Ollama (Local Models)
```bash
# Install Ollama from https://ollama.ai
# Start Ollama service

python worker.py --model ollama --model-name llama2 "Your task"
```

### Option 3: OpenAI API
```bash
# Set your API key
set OPENAI_API_KEY=sk-your-key-here  # Windows PowerShell
# Or: export OPENAI_API_KEY=sk-your-key-here  # Linux/macOS

python worker.py --model openai "Your task here"
```

---

## 📋 Version History

### Version 1
- Continuous task execution without prompting
- Basic stop condition checks
- Watchdog mechanism
- Simple file upload

### Version 2 (Current - v2.1.0)
- **Chat history tracking and persistence**
- **Offline model support** (transformers, ollama, openai)
- **Control commands** during task execution
- **Backend flexibility** - switch between models
- **Task continuity** - resume from where you left off
- **Task tracking** - input/goal/target/task/checklist/timeline persistence
- **Diagram skill** - automatic diagram fixing with checklist compliance

### Version 2.1.0 (Patch)
- **Task state persistence** - full input/goal/target tracking
- **Diagram skill integration** - automatic diagram fixing
- **opencode CLI integration** - `diagram-skill` command
- **Wrapper support** - works with any AI-model program

---

## 🎯 Philosophy

Cat-Out-Of-The-BOx addresses the common AI model problem of stopping 
and asking "continue?" every few steps. Version 2.1.0 enables:

- **Hands-free operation**: Task runs from start to end without interruption
- **Memory**: AI remembers context via chat history + task state
- **Flexibility**: Choose your AI backend (offline or API)
- **Reliability**: Graceful handling of environment issues
- **Control**: User can interrupt or start new anytime via commands
- **Persistent state**: No more repetitive resume cycles
- **Task visibility**: Always see input, goal, target, progress checklist

---

## 🔗 Quick Access

- 🌐 **View on GitHub**: https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx
- 📜 **Raw Logo**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/LOGO.txt
- 📜 **Usage Flowchart**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/FLOWCHART_USAGE.md
- 📜 **Internal Diagram**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/FLOWCHART_INTERNAL.md
- 📜 **Grade Document**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/GRADE.md
- 📜 **Checklist**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/CHECKLIST.md
- 🐍 **Python API**: https://pypi.org/project/cat-out-the-box/

---

## 💡 Example Tasks

```bash
# Analyze data and generate report
python worker.py "Analyze this CSV sales data and generate a summary report with charts"

# Summarize a document
python worker.py --model transformers "Summarize this 10-page document in 3 key points"

# Continue previous task
python worker.py --continue "Continue from where we left off"

# New task, clearing history
python worker.py /new "Start fresh with new task context"

# Diagram fixing with checklist
diagram-skill "diagrams/flowchart.png" '{"f.3": "significant-improvements", "f.5": "leave-as-is"}'
```

---

## 📄 License

MIT License - See the [LICENSE](LICENSE) file for details.