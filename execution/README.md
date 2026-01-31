# Execution Scripts

This directory contains **deterministic Python scripts** that perform the actual work.

## Purpose

Execution scripts handle:
- API calls
- Data processing
- File operations
- Cloud storage interactions
- Any repeatable task

## Principles

1. **Deterministic**: Same inputs → Same outputs
2. **Fast**: Optimized for performance
3. **Testable**: Can be run independently
4. **Repeatable**: Designed to run multiple times safely

## Design Guidelines

- Use clear function names and docstrings
- Handle errors gracefully with informative messages
- Log important steps for debugging
- Accept inputs via command-line arguments or environment variables
- Return clear exit codes (0 = success, non-zero = failure)

## Environment Variables

Scripts should read secrets and API keys from `.env` file.
Never hardcode credentials.

## Example Script Structure

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main execution function."""
    # Your logic here
    pass

if __name__ == "__main__":
    main()
```

## Testing

Before committing a script:
1. Test with valid inputs
2. Test with edge cases
3. Verify error handling
4. Update the corresponding directive with learnings
