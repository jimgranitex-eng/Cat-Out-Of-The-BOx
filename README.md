# Cat-Out-Of-The-BOx

Version 2: Continuous AI Worker with Chat History and Offline Support

A tool to help AI models work continuously toward goals without constant prompting/resuming,
with full chat history tracking and offline model support.

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

## Files

- `worker.py` - Main continuous worker tool (Version 2)
- `upload.py` - File upload utility (upload to paste.rs)
- `README.md` - This file
- `.chat_history.json` - Chat history (auto-generated, .gitignored)

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