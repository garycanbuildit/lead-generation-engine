#!/usr/bin/env python3
"""
Example execution script: Hello World

This demonstrates the structure of a deterministic execution script.
It accepts inputs, performs a simple task, and produces outputs.
"""

import argparse
import os
import sys
from pathlib import Path


def create_greeting(name: str, style: str = "casual") -> str:
    """
    Create a greeting message based on name and style.
    
    Args:
        name: The name to greet
        style: The greeting style ("formal" or "casual")
    
    Returns:
        A formatted greeting string
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    
    if style == "formal":
        return f"Good day, {name}. It is a pleasure to make your acquaintance."
    else:
        return f"Hey {name}! Great to meet you!"


def save_greeting(greeting: str, output_path: Path) -> None:
    """
    Save the greeting to a file.
    
    Args:
        greeting: The greeting message to save
        output_path: Path where the greeting should be saved
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(greeting)
    print(f"✓ Greeting saved to: {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Generate a greeting message (DOE example script)"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name to greet"
    )
    parser.add_argument(
        "--style",
        choices=["formal", "casual"],
        default="casual",
        help="Greeting style (default: casual)"
    )
    parser.add_argument(
        "--output",
        default=".tmp/greeting.txt",
        help="Output file path (default: .tmp/greeting.txt)"
    )
    
    args = parser.parse_args()
    
    try:
        # Generate greeting
        greeting = create_greeting(args.name, args.style)
        print(f"\n{greeting}\n")
        
        # Save to file
        output_path = Path(args.output)
        save_greeting(greeting, output_path)
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
