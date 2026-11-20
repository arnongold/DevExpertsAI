# DevExpertsAI — CRM Sales Research

A Claude Code skill that turns a company name into a CRM sales brief: company profile, key stakeholders mapped to buying roles, and evidence-backed opportunities to sell a new CRM system.

## Usage

Open this repository in Claude Code and run:

```
/sales-research Acme Corp
```

Add a website or country if the name is ambiguous, for example `/sales-research Mercury acme.com`. Asking in plain language ("research Acme Corp for a CRM pitch") also works.

Claude researches public web sources, writes the brief to `research/<company>-<date>.md`, and shows you the executive summary.

## Tailor it to your product

Fill in `.claude/skills/sales-research/offering.md` with your CRM's description, ideal customer profile, differentiators and the competitors you displace. Briefs then pitch your product specifically. Until then they're vendor-neutral.

## What's in a brief

- Executive summary with fit and timing ratings
- Company brief: what they do, size, ownership, go-to-market, recent news
- Current CRM and sales-tool landscape
- Stakeholder table (economic buyer, champion, technical evaluator, influencers, blockers) and a recommended first contact
- 3–5 sales opportunities, each tied to a cited signal
- Suggested approach: opening angle, discovery questions, objections, competitive notes
- Risks, unknowns and a numbered source list

Every name and number is sourced; anything inferred is marked. The skill collects only public business information about people.
