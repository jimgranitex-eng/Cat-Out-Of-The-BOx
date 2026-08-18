# Cat-Out-Of-The-BOx v2 - Usage Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAT-OUT-OF-THE-BOX v2                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  1. START          │────▶│  Set Task Description        │       │
│  │  python worker.py  │     │  "Your task here"           │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  2. PARSE ARGS     │────▶│  Initialize Backend          │       │
│  │  --model, --tier   │     │  (transformers/ollama/openai)│      │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  3. INITIALIZE     │────▶│  Load Chat History           │       │
│  │  .chat_history.json│────▶│  (persists between runs)    │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  4. TASK LOOP      │────▶│  Run Continuous Task         │       │
│  │  (no prompts!)     │────▶│  AI works until:             │       │
│  │                    │     │  • Task complete            │       │
│  │                    │     │ • Stop condition met      │       │
│  │                    │     │ • Ctrl+C interrupted     │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  5. CHECK CONDITIONS│────▶│  Auto-Check:                │       │
│  │  • Disk space      │────▶│  • Free GB < 1.0           │       │
│  │  • Iteration limit │────▶│  • Iterations > max        │       │
│  │  • Time limits     │────▶│  • Time exceeded           │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  6. CONTROL CMD?   │────▶│  Respond to:               │       │
│  │  (during task)     │────▶│  • /new  → New task        │       │
│  │  Type in console:  │────▶│  • /stop → Stop worker      │       │
│  │  /status, /continue│────▶│  • /status→ Show status     │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  7. COMPLETE?      │────▶│  Task Finished?             │       │
│  │  Yes → ✓ Success   │────▶│  Show result, save history  │       │
│  │  No  → Loop back   │────▶│  Continue task              │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────┐     ┌─────────────────────────────┐       │
│  │  8. SAVE & EXIT    │────▶│  Save .chat_history.json    │       │
│  │  (auto & graceful) │────▶│  Exit cleanly               │       │
│  └─────────────────────┘     └─────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Usage Reference

```
Command                      | Action
-----------------------------|----------------------
python worker.py "Task"      | Run task (offline, no API)
python worker.py --model ollama --model-name llama2 "Task" | Run with Ollama
python worker.py --tier mid-high "Task" | Specify model tier
/stop                        | During task: Stop worker
/new                         | During task: New task (clear history)
/status                      | During task: Show status
/continue                    | During task: Continue
```

---

### Version 2 Features in Flow

```
┌───────────────────┐     ┌─────────────────────────────┐
│   CHAT HISTORY       │────▶│ Persists in .chat_history.json│
│   (system memory)    │     │   Auto-saves on each step   │
│↓                    │     ↓                           │
│⟵ Remember context   │────▶│   AI recalls past steps     │
│   across iterations │     │   to maintain goal awareness  │
│↓                    │     ↓                           │
│   ✓ Task continuity │     │   ✓ Resume from where left  │
└───────────────────┘     └─────────────────────────────┘
```

---

### Model Tier Selection Flow

```
┌───────────────────┐
│  Choose Model Tier    │
├─────────────────────┤
│  mid     (8b-13b)   │✓ Good for: analysis, summarization
│  mid-high (13b-70b) │✓ Good for: coding, complex generation
│  high    (70b-150b) │⚠️ Needs: powerful GPU/operator
│  ultra   (150b+)   │❌ Needs: frontier hardware
└─────────────────────┘
```

***

**Usage Examples:**

```bash
# Basic - offline, no API key needed
python worker.py "Analyze this data and generate a summary"

# With model specification
python worker.py --model ollama --model-name llama2 "Write a Python script"

# With tier specification
python worker.py --tier mid-high "Process this CSV file"

# Control during task (type in console)
/stop   → Stop worker
/new    → Start new task (clears history)
/status → Show worker status
/continue → Continue current task
```