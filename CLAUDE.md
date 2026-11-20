# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A prompt-only solution with no application code, build or tests. The product is the Claude Code skill `sales-research`, which researches a company on the web and writes a CRM sales brief.

- `.claude/skills/sales-research/SKILL.md`: the research workflow and the report template. Change the brief's structure here.
- `.claude/skills/sales-research/offering.md`: the seller's CRM product, ICP and competitors. The skill reads it at run time to tailor pitches; while it holds `TODO` placeholders, briefs stay vendor-neutral.
- `research/`: generated briefs, named `<company-slug>-<YYYY-MM-DD>.md`.

## Rules for generated briefs

- Never invent stakeholders or figures. Cite every name and number, mark inferences *(inferred)*, and flag role data older than 12 months as *verify*.
- Public business information only: no personal contact details or private-life data about individuals.
- Confirm which company is meant before researching in depth when the name is ambiguous.
