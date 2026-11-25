# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A set of Claude Code agents that analyze customer service data: support tickets, chat transcripts, CSAT/NPS surveys and call logs. Like the `sales-research` skill in the repo root, the agents are prompt-first: each is a skill or subagent definition, plus small Python scripts where numbers must be computed.

## Layout

- `.claude/skills/<agent-name>/SKILL.md`: one skill per analysis, for example `ticket-trends`, `csat-drivers`, `agent-performance`, `topic-clustering` or `sla-breaches`. Each SKILL.md states its inputs, steps and report template.
- `.claude/agents/<name>.md`: subagents for work that should run in its own context, for example a classifier that tags thousands of tickets.
- `scripts/`: Python helpers the skills call to load, clean and aggregate data. Keep calculations here, not in prompts.
- `data/`: input exports (CSV, JSON, XLSX). Git-ignored because they contain customer PII. Never commit raw data.
- `reports/`: generated analyses, named `<analysis>-<YYYY-MM-DD>.md`.

## Building a new agent

1. Create `.claude/skills/<agent-name>/SKILL.md` with frontmatter `name`, `description` (include the phrases a user would say to trigger it), `argument-hint` and `allowed-tools`. Grant only the tools the agent needs: usually Read, Write, Glob and Bash for running scripts.
2. Start the skill with a data-check step: list the files and columns found, the date range and the row count, and map the columns to the standard fields below. Stop and ask if a required field is missing.
3. Put calculations in `scripts/` and have the skill run them. Don't let the model estimate counts, averages or percentages by reading rows.
4. End the skill with a fixed report template, saved to `reports/`, and show the user the summary.
5. Test the agent on a small sample file before a full export.

## Standard fields

Exports from Zendesk, Intercom, Freshdesk, Salesforce Service Cloud and similar tools name columns differently. Map them to these fields before analyzing: `ticket_id`, `created_at`, `first_response_at`, `resolved_at`, `status`, `channel`, `priority`, `category`/`tags`, `agent`, `team`, `customer_id`, `csat_score`, `reopened`, `body`/`transcript`.

## Metric definitions

Use these unless the user defines a metric differently, and state the definition used in every report:

- **First response time (FRT):** `first_response_at - created_at`. Report the median and the 90th percentile, not just the mean.
- **Resolution time:** `resolved_at - created_at`, for resolved tickets only.
- **CSAT:** share of responses scoring 4–5 on a 5-point scale. Always report the response count.
- **Reopen rate:** reopened tickets ÷ resolved tickets.
- **Backlog:** tickets open at the end of the period.
- Say whether times are in calendar or business hours, and which time zone.

## Analysis rules

- Every number comes from the data or a script output. Never invent or extrapolate figures.
- State the date range, the row count and any filters for each result. Flag segments with fewer than 30 tickets or responses as low-sample.
- Separate findings (measured) from hypotheses (inferred). Mark the latter *(inferred)*.
- Report what was excluded (duplicates, test tickets, missing timestamps) and how many rows.
- Theme or topic labels from LLM classification: report the method, show 2–3 example tickets per theme, and spot-check a sample.

## Privacy

- Treat ticket text as customer PII. Reports quote ticket IDs and short anonymized snippets, never names, emails, phone numbers, addresses or payment details.
- Report individual agent performance only when the user asks for it, and give team-level context with it.
