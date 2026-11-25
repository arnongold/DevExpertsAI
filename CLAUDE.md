# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A prompt-only solution with no application code, build, lint or tests. The product is the Claude Code skill `sales-research`, which researches a company on the web and writes a CRM sales brief.

- `.claude/skills/sales-research/SKILL.md`: the research workflow (steps 0–5) and the report template. Change the brief's structure here.
- `.claude/skills/sales-research/offering.md`: the seller's CRM product, ICP and competitors. The skill reads it at run time to tailor pitches; while it holds `TODO` placeholders, briefs stay vendor-neutral and say so in one line at the top.
- `research/`: generated briefs, named `<company-slug>-<YYYY-MM-DD>.md`. `research/matrix-it-2026-11-20.md` is the reference example of a finished brief.

## Running and checking the skill

There is nothing to build. To exercise a change, run the skill and read the brief it writes:

```
/sales-research <company> [website or country to disambiguate]
```

The company argument arrives as `$ARGUMENTS` in `SKILL.md`.

## Editing the skill

- The `allowed-tools` frontmatter in `SKILL.md` (WebSearch, WebFetch, Read, Write, Glob) limits what the skill can do. Add a tool there if a workflow change needs one.
- `README.md` lists the brief's sections under "What's in a brief". Keep it in sync when you change the report template.

## Rules for generated briefs

- Never invent stakeholders or figures. Cite every name and number as `[n]` against the numbered Sources list, mark inferences *(inferred)*, and flag role data older than 12 months as *verify*.
- Public business information only: no personal contact details or private-life data about individuals.
- Confirm which company is meant before researching in depth when the name is ambiguous.
