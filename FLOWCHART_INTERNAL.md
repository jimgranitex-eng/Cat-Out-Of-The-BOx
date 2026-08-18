# Cat-Out-Of-The-BOx v2 - Internal Working Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                  CAT-OUT-OF-THE-BOX v2 ENGINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  USER INPUT  ──►  PARSE ARGUMENTS  ──►  INITIALIZE BACKEND       │
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────────┐ │
│  │  task       │──►│  --model     │──►│  backend = "       │ │
│  │  description│    │  --tier      │    │  transformers"    │ │
│  └─────────────┘    └──────────────┘    │  ollama / openai" │ │
│                        └──────┬──────┘                     │ │
│                              │                              │ │
│                              ▼                              │ │
│                      ┌─────────────────────┐                │ │
│                      │  LOAD CHAT HISTORY   │                │ │
│                      │  .chat_history.json │                │ │
│                      └─────────────────────┘                │ │
│                              │                              │ │
│                              ▼                              │ │
│                      ┌─────────────────────┐                │ │
│                      │  SETUP SIGNALS       │                │ │
│                      │  Ctrl+C, SIGTERM    │                │ │
│                      └─────────────────────┘                │ │
│                              │                              │ │
│                              ▼                              │ │
│                      ┌─────────────────────┐                │ │
│                      │  TASK EXECUTION LOOP │                │ │
│                      │  (continuous, no    │                │ │
│                      │   prompt pauses)    │                │ │
│                      └─────────────────────┘                │ │
│                              │                              │ │
│                      ▼                              │ │
│              ┌───────────────────────┐                │ │
│              │  ITERATION STEP      │                │ │
│              │  1. Get AI response  │                │ │
│              │     using model       │                │ │
│              │  2. Add to history   │                │ │
│              │  3. Check conditions │                │ │
│              │     (disk, limits)   │                │ │
│              │  4. Check control    │                │ │
│              │     commands         │                │ │
│              │  5. Determine done?  │                │ │
│              └───────────────────────┘                │ │
│                              │                              │ │
│                      ▼                              │ │
│              ┌───────────────────────┐                │ │
│              │  CONDITION CHECK     │                │ │
│              │  • Disk space < 1GB? │                │ │
│              │  • Iterations > max? │                │ │
│              │  • Time exceeded?    │                │ │
│              │  • Ctrl+C interrupted?│              │ │
│              └───────────────────────┘                │ │
│                              │                              │ │
│                      ▼                              │ │
│              ┌───────────────────────┐                │ │
│              │  CONTROL HANDLING    │                │ │
│              │  • /new  → Clear hist│                │ │
│              │  • /stop → Stop wkr   │                │ │
│              │  • /status→ Show stat │                │ │
│              │  • /continue→ Contiue│                │ │
│              └───────────────────────┘                │ │
│                              │                              │ │
│                      ▼                              │ │
│              ┌───────────────────────┐                │ │
│              │  TASK COMPLETE?      │                │ │
│              │  Yes → ✓ Success     │                │ │
│              │  No  → Loop back     │                │ │
│              └───────────────────────┘                │ │
│                              │                              │ │
│                      ▼                              │ │
│              ┌───────────────────────┐                │ │
│              │  SAVE & EXIT         │                │ │
│              │  • Save .chat_history│                │ │
│              │  • Graceful shutdown │                │ │
│              └───────────────────────┘                │ │
│                                                                 │
│  ┌───────────────────────┐    ┌───────────────────────┐    │ │
│  │  MCP BLUEPRINT          │────►│  Generated script     │    │ │
│  │  (mcp.py)               │    │  worker.run_task()    │    │ │
│  │  • Decompose task       │    │  • Sequential steps   │    │ │
│  │  • Route to tiers       │    │  • Auto-complete      │    │ │
│  │  • Generate blueprint  │    └───────────────────────┘    │ │
│  └───────────────────────┘                          │ │
└─────────────────────────────────────────────────────────────────┘
```

---

### Model Backend Flow

```
┌───────────────────┐     ┌───────────────────────┐     ┌─────────────────────┐
│  transformers      │     │  ollama               │     │  openai             │
│  (default)         │     │  (local, requires)    │     │  (API, requires)    │
│✓ No API key       │     │✓ Runs locally        │     │✓ Needs OPENAI_API_KEY│
│✓ Offline          │     │✓ Models: llama2, etc │     │✗ Internet required  │
│⚠️ PIL compatibility│     │⚠️ Ollama must be run │     │✓ Best for: cloud   │
│   issues possible  │     │   as service         │     │   deployments      │
│✓ Best compat: gpt2│     └───────────────────────┘     └─────────────────────┘
└───────────────────┘
```

---

### MCP (Mini Continuous Planner) Flow

```
┌────────────────────────────────────────────────────┐
│                  MCP v2.0.0 FLOW                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  USER TASK  ──► DECOMPOSE  ──► ROUTE TIERS  ──► BLUEPRINT │
│                                                    │
│  "Analyze data"     ──► 3 subtasks           │           │
│                     │ 1. analysis        │           │
│                     │ 2. summarization   │           │
│                     │ 3. generation      │           │
│                     ▼                         │           │
│  Tiers:             │  mid, mid, mid-high  │           │
│  Model ranges:      │  8b-13b, 8b-13b, 13b-70b│       │
│  Blueprint:         │  Generated Python   │           │
│                    │  script with worker.│           │
│                    │  run_task() calls   │           │
│                                                    │
│  OUTPUT:            │  Ready-to-run      │           │
│                    │  script saved as   │           │
│                    │  mcp_blueprint_*.py │           │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

### Resource Usage Monitor

```
┌───────────────────┐     ┌───────────────────────┐
│  TASK TIMING       │     │  MEMORY USAGE         │
├───────────────────┼────►├───────────────────────┤
│  Avg: 7.11s        │     │  Delta: 0.0MB per task│
│  Min: 7.08s        │     │  Stable across runs   │
│  Max: 7.13s        │     │  Predictable          │
│  Consistent!     │     └───────────────────────┘
└───────────────────┘
```