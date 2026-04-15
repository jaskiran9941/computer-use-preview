# Agent Skills — Figma Design Review

Claude-powered skills for reviewing Figma designs. Each skill is a structured prompt that accepts a Figma screenshot and produces actionable PM/design feedback.

## Skills

| Skill | File | Purpose |
|---|---|---|
| `/copy-review` | `copy-review.md` | Review UI copy for tone, clarity, consistency, and truncation risks |
| `/missing-states` | `missing-states.md` | Enumerate UI states missing from the design (loading, empty, error, edge cases) |
| `/a11y-check` | `a11y-check.md` | Accessibility audit against WCAG 2.1 AA |

## How to Use

Each skill file contains:
1. **How to Use** — the prompt format and example
2. **System Prompt** — the full prompt to configure Claude

To use a skill, configure Claude with the system prompt from the skill file, then paste your Figma screenshot with the context described in the "How to Use" section.

## Inputs

All skills accept:
- **Figma screenshot** — export your frame as PNG or take a screenshot
- **Context** — brief description of screen purpose, platform, audience

## Tips

- Run all three skills on the same design before handing off to engineering
- `/missing-states` pairs well with your feasibility estimator — missing states directly inflate effort estimates
- `/copy-review` + `/a11y-check` together catch most pre-launch copy and compliance issues
