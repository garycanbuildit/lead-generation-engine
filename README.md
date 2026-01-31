# DOE Agent System

A **Directive → Observation → Experiment** agent system for converting human intent into reliable, repeatable outputs.

## Architecture

This system uses a 3-layer architecture:

### Layer 1: Directive (What needs to be done)
- SOP-style instructions in `directives/`
- Define goals, inputs, tools, outputs, and edge cases
- Written in plain language

### Layer 2: Orchestration (Decision-making)
- AI agent interprets directives
- Routes execution intelligently
- Handles errors and ambiguity
- Updates directives with learnings

### Layer 3: Execution (Doing the work)
- Deterministic Python scripts in `execution/`
- Handle APIs, data processing, file operations
- Fast, testable, and repeatable

## Directory Structure

```
.
├── AGENT.md              # Operating rules and principles
├── directives/           # Markdown SOPs
├── execution/            # Python scripts
├── .tmp/                 # Temporary files (disposable)
├── .env                  # Environment variables (not in version control)
└── credentials.json      # OAuth credentials (not in version control)
```

## Getting Started

1. **Copy environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Add your API keys to `.env`**

3. **Read the operating rules:**
   ```bash
   cat AGENT.md
   ```

4. **Create your first directive** in `directives/`

5. **Build execution scripts** in `execution/`

## Operating Principles

1. **Check for existing tools** before creating new ones
2. **Self-anneal on failure** - fix, improve, test, update
3. **Improve directives continuously** - they are living documents

## Self-Annealing Loop

When something breaks:
1. Fix it
2. Improve the tool
3. Test again
4. Update the directive
5. Continue with a stronger system

## Key Principles

- **AI is probabilistic. Business logic must be deterministic.**
- **Deliverables live in the cloud. Intermediates are disposable.**
- **Errors compound. Deterministic scripts increase reliability.**
- **Be pragmatic. Be reliable. Self-anneal.**

---

For detailed operating rules, see [AGENT.md](./AGENT.md)
