# Directives

This directory contains **SOP-style instructions** written in Markdown.

## Purpose

Directives define:
- **Goals**: What needs to be accomplished
- **Inputs**: What data/parameters are required
- **Tools/Scripts**: Which execution scripts to use
- **Outputs**: What the result should look like
- **Edge Cases**: Known constraints, limitations, and error scenarios

## Format

Each directive should be written in plain language, as if briefing a competent teammate.

## Example Structure

```markdown
# [Task Name]

## Goal
What this directive accomplishes

## Inputs
- Input 1: Description
- Input 2: Description

## Execution
Which scripts in `execution/` to run and in what order

## Outputs
What deliverables are produced

## Edge Cases
- Known limitations
- API constraints
- Error scenarios
```

## Living Documents

Directives are continuously improved based on learnings from execution.
When errors occur or better approaches are discovered, update the relevant directive.

**Do not create, overwrite, or delete directives unless explicitly instructed.**
