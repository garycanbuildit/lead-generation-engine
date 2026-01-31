# Quick Start Guide

Welcome to the DOE Agent System! This guide will help you get started.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r execution/requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env and add your API keys
   ```

## Testing the System

Run the example script to verify everything works:

```bash
python3 execution/hello_world.py --name "Your Name" --style casual
```

You should see a greeting message and a file created at `.tmp/greeting.txt`.

## Creating Your First Workflow

### Step 1: Write a Directive

Create a new file in `directives/` (e.g., `directives/my_task.md`):

```markdown
# My Task

## Goal
What this task accomplishes

## Inputs
- Input 1: Description
- Input 2: Description

## Execution
Which scripts to run

## Outputs
What deliverables are produced

## Edge Cases
Known limitations and error scenarios
```

### Step 2: Create an Execution Script

Create a new Python script in `execution/` (e.g., `execution/my_task.py`):

```python
#!/usr/bin/env python3
"""
Description of what this script does.
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="My task")
    parser.add_argument("--input", required=True, help="Input parameter")
    args = parser.parse_args()
    
    # Your logic here
    print(f"Processing: {args.input}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Make it executable:
```bash
chmod +x execution/my_task.py
```

### Step 3: Test and Iterate

1. Run your script
2. Observe results
3. Fix any issues
4. Update the directive with learnings
5. Repeat

## The DOE Loop in Action

When you encounter an error:

1. **Observe**: Read the error message carefully
2. **Experiment**: Fix the issue in the script
3. **Test**: Run again to verify the fix
4. **Update Directive**: Document what you learned
5. **Continue**: The system is now stronger

## Directory Structure

```
.
├── AGENT.md                    # Operating rules (READ THIS FIRST)
├── README.md                   # System overview
├── QUICKSTART.md              # This file
├── directives/                # Task definitions (Markdown)
│   ├── README.md
│   └── example_hello_world.md
├── execution/                 # Deterministic scripts (Python)
│   ├── README.md
│   ├── requirements.txt
│   └── hello_world.py
├── .tmp/                      # Temporary files (disposable)
│   └── README.md
├── .env.template              # Environment variables template
└── .gitignore                 # Git ignore rules
```

## Key Principles to Remember

1. **Check before creating**: Review `execution/` before writing new scripts
2. **Self-anneal on failure**: Fix → Improve → Test → Update directive
3. **Directives are living documents**: Update them as you learn
4. **Deliverables in cloud, intermediates in .tmp**: Local files are temporary
5. **Be deterministic**: Same inputs should produce same outputs

## Next Steps

1. Read `AGENT.md` thoroughly
2. Explore the example directive and script
3. Create your first real directive
4. Build your first execution script
5. Start the DOE loop!

---

**Questions?** Review the README files in each directory for more details.
