# Cat-Out-Of-The-BOx

Version 1: Continuous AI Worker Tool

A tool to help AI models work continuously toward goals without constant prompting/resuming.

## Features (Version 1)
- **Continuous task execution**: Runs tasks in a loop without stopping to ask "continue?"
- **Auto-detection of stop conditions**: Checks for practical limits (disk space, iteration limits, etc.)
- **Watchdog/alarm clock monitor**: Detects if worker stops and can attempt restart
- **Keyboard interrupt handling**: Graceful Ctrl+C handling
- **Configurable iteration limits**: Safety limit to prevent runaway processes (default: 100)
- **File upload utility**: Built-in upload.py for sharing results

## Usage

```bash
python worker.py "Your task description here"
```

### Examples

```bash
python worker.py "Analyze the data trends in sales_data.csv and generate a summary"
python worker.py "Process all files in this directory and upload results"
python worker.py "Summarize this document and extract key points"
```

### How it works

1. The worker starts and immediately begins executing the task in a continuous loop
2. It runs steps without prompting the user between iterations
3. The task continues until:
   - The task marks itself as complete
   - A stop condition is met (low disk space, time limits, etc.)
   - The user presses Ctrl+C to interrupt
4. The watchdog monitor runs in parallel, checking if the worker is still active

### Stop Conditions (Version 1)
- **Disk space**: Checks if less than 1GB free
- **Iteration limit**: Default max 100 iterations (configurable)
- **Time**: Will respect Ctrl+C interrupt

### Watchdog (Version 1)
- Monitors worker status every 5 seconds
- Max wait time: 300 seconds (5 minutes)
- Can be extended for continuous monitoring

## Files

- `worker.py` - Main continuous worker tool (Version 1)
- `upload.py` - File upload utility (upload to paste.rs)
- `README.md` - This file