# Example Directive: Hello World

## Goal
Demonstrate the DOE system with a simple "Hello World" example that shows how directives connect to execution scripts.

## Inputs
- `name` (string): The name to greet
- `greeting_style` (string, optional): Style of greeting ("formal" or "casual", defaults to "casual")

## Execution
Run the script: `execution/hello_world.py`

```bash
python execution/hello_world.py --name "John" --style casual
```

## Outputs
- Console output: A greeting message
- File output: `.tmp/greeting.txt` containing the greeting

## Edge Cases
- **Empty name**: Script should handle gracefully with error message
- **Invalid style**: Should default to "casual"
- **Missing arguments**: Should show usage help

## Learnings
- (This section will be updated as we discover constraints or improvements)
