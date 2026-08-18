# Cat-Out-Of-The-BOx

<a href="https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx">
  <img src="https://img.shields.io/github/stars/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge"/>
  <img src="https://img.shields.io/github/license/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge"/>
</a>

**AI that works from start to end without stopping to prompt.**

Version 2: Continuous AI Worker with Chat History and Offline Support

A tool to help AI models work continuously toward goals without constant prompting/resuming,
with full chat history tracking and offline model support.

[![GitHub](https://img.shields.io/github/actions/workflow/status/jimgranitex-eng/Cat-Out-Of-The-BOx/main.yml?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx/actions)
[![GitHub repo size](https://img.shields.io/github/repo-size/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx)
[![GitHub last commit](https://img.shields.io/github/last-commit/jimgranitex-eng/Cat-Out-Of-The-BOx?style=for-the-badge)](https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx)

## Features (Version 2)

### Core Features (Carried from Version 1)
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
  - `transformers` - Offline local models (default)
  - `ollama` - Ollama local models (requires Ollama running)
  - `openai` - OpenAI API (requires OPENAI_API_KEY)
- **Task continuity**: AI uses chat history to guide work toward goal
  - Maintains context across iterations
  - Remembers previous task progress
  - Can resume from where it left off

## Usage

```bash
# Basic usage (offline transformers model - no API needed)
python worker.py "Your task description here"

# With model selection
python worker.py --model ollama --model-name llama2 "Summarize this text"
python worker.py --model openai "Analyze this data"  # Needs OPENAI_API_KEY

# With options
python worker.py --max-iterations 20 "Process this file"
python worker.py --continue "Continue previous task"

# Control commands (during task):
# Type /new, /stop, /status, or /continue in response to AI prompts
```

## Examples

```bash
python worker.py "Analyze sales data and generate a summary report"
python worker.py --model transformers "Translate this document to French"
python worker.py --model ollama "Creative writing story about cats"
python worker.py /new "Start fresh with new task context"
```

## How It Works

### Version 2 Flow
1. Worker starts and parses command-line arguments
2. AI model is initialized (offline transformers by default)
3. Task description is added to chat history
4. Worker enters continuous loop:
   - AI gets response using recent chat history for context
   - Response is displayed and added to history
   - Check for stop conditions (disk space, iteration limits)
   - Respond to control commands if present
5. Task completes when AI marks it done OR user interrupts with Ctrl+C
6. Chat history is saved to `.chat_history.json` for next run

### Chat History Persistence
- Saved to `.chat_history.json` in project directory
- Contains full conversation: system prompt, user messages, assistant responses
- On next run, history is loaded and AI continues from where it left off
- Use `/new` to clear history and start fresh
- History can be manually edited to modify context

### Stop Conditions
- **Disk space**: Checks if less than 1GB free
- **Iteration limit**: Max 50 iterations (configurable with `--max-iterations`)
- **Ctrl+C**: Graceful interruption at any time
- **AI completion**: AI determines task is done and marks it complete

## 📂 Repository Files

All tools and assets are stored in the repository and can be viewed via GitHub:

### Core Tools
- `worker.py` - Version 2 continuous AI worker (~600 lines)
- `upload.py` - File upload utility (paste.rs)
- `mcp.py` - Mini Continuous Planner v2.0.0
- `metrics_test.py` - Performance testing script

### Visual Assets & Documentation
- `FLOWCHART_USAGE.md` - Step-by-step usage flow diagram
- `FLOWCHART_INTERNAL.md` - Internal engine working diagram
- `LOGO.txt` - ASCII text logo
- `GRADE.md` - Formal a++ rating document
- `CHECKLIST.md` - Complete feature inventory & next version plans
- `README.md` - This file (you are here)

### Generated Output
- `.chat_history.json` - Auto-generated chat history (gitignored)
- `mcp_blueprint_*.py` - Generated execution blueprints

### Quick Access
- 🌐 **View on GitHub**: https://github.com/jimgranitex-eng/Cat-Out-Of-The-BOx
- 📜 **Raw Logo**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/LOGO.txt
- 📜 **Usage Flowchart**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/FLOWCHART_USAGE.md
- 📜 **Internal Diagram**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/FLOWCHART_INTERNAL.md
- 📜 **Grade Document**: https://raw.githubusercontent.com/jimgranitex-eng/Cat-Out-Of-The-BOx/main/GRADE.md

## Installing and Using Offline Models

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

## Version History

### Version 1
- Continuous task execution without prompting
- Basic stop condition checks
- Watchdog mechanism
- Simple file upload

### Version 2 (Current)
- **Chat history tracking and persistence**
- **Offline model support** (transformers, ollama, openai)
- **Control commands** during task execution
- **Backend flexibility** - switch between models
- **Task continuity** - resume from where you left off

## Philosophy

Cat-Out-Of-The-BOx addresses the common AI model problem of stopping 
and asking "continue?" every few steps. Version 2 enables:

- **Hands-free operation**: Task runs from start to end without interruption
- **Memory**: AI remembers context via chat history
- **Flexibility**: Choose your AI backend (offline or API)
- **Reliability**: Graceful handling of environment issues
- **Control**: User can interrupt or start new anytime via commands