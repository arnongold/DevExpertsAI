---
name: sales-research
description: Research a target company for a CRM sale. Given a company name, produce a sales brief covering the company profile, key stakeholders and buying roles, and concrete opportunities to sell a new CRM system. Use when the user says "research <company>", "sales brief for <company>", "account research", "who should I talk to at <company>", or invokes /sales-research.
argument-hint: <company name> [website or country to disambiguate]
allowed-tools: WebSearch, WebFetch, Read, Write, Glob
---

# Sales research: CRM account brief

Target company: **$ARGUMENTS**

If no company name was given, ask for one and stop.

## 0. Load the seller's context

Read `.claude/skills/sales-research/offering.md`. It describes the CRM being sold (product, ideal customer profile, differentiators, competitors it displaces). Shape the opportunities and talking points around it. If it still holds only the template placeholders, write a vendor-neutral brief and say so in one line at the top of the report.

## 1. Identify the right company

Company names collide. Before researching in depth, confirm the entity: official website, HQ country, industry. If two or more plausible companies match and the user gave nothing to tell them apart, list them briefly and ask which one. Otherwise state the one you picked in the report header.

## 2. Research (public sources only)

Run searches in parallel where possible. Prefer primary and recent sources (last 18 months). Cover:

| Area | What to find | Good sources |
|---|---|---|
| Profile | What they sell, to whom, business model (B2B/B2C, direct/channel), HQ, locations, founding year | Company site (About, Products), LinkedIn company page, Wikipedia |
| Scale | Employee count, revenue or funding, growth trend, public/private, owners/investors | Annual reports, 10-K, Crunchbase, press releases |
| Momentum | Funding rounds, M&A, new markets, product launches, layoffs, restructuring, leadership changes | News, press releases, earnings calls |
| Go-to-market | Size and shape of sales, marketing, customer success and support teams; regions; partner channels | Careers page, job postings, LinkedIn |
| Current stack | CRM and adjacent tools in use (Salesforce, HubSpot, Dynamics, Zoho, homegrown, spreadsheets), marketing automation, ERP, support desk | Job postings that name tools, vendor case studies, tech-stack sites, engineering blogs |
| Stakeholders | People in the roles listed in section 3 | Company leadership page, LinkedIn, press releases, conference talks, interviews |
| Pain signals | Statements or evidence of problems a CRM solves | Job postings ("build our RevOps function", "migrate CRM"), employee reviews, earnings-call remarks, customer complaints |

Rules:
- **Never invent facts or people.** Every stakeholder name and every number needs a source. If you can't find it, write "Not found" — don't guess.
- Mark anything inferred (not stated by a source) as *(inferred)* and say what it's inferred from.
- Note the date of time-sensitive facts (headcount, revenue, who holds a role). People change jobs; flag any role whose source is older than 12 months as *verify*.
- Business information only: names, titles, public professional background, public statements. Do not collect personal phone numbers, personal emails, home addresses, or family details.

## 3. Map stakeholders to buying roles

Look for people in these functions and assign each a buying role:

- **Economic buyer**: CEO (small companies), CRO, CFO, COO
- **Champion / primary user owner**: VP or Head of Sales, Revenue Operations, Sales Operations
- **Technical evaluator**: CIO, CTO, Head of IT / Business Systems, Salesforce or CRM admin, enterprise architect
- **Influencers**: CMO / VP Marketing (lead flow, attribution), VP Customer Success / Support, Head of Partnerships
- **Procurement / blockers**: Procurement, Legal, Security / CISO, anyone who sponsored the current CRM

For small companies (under ~50 people) the founder or CEO often holds several roles. Say so rather than padding the list.

## 4. Build the opportunity analysis

Connect evidence to need. Each opportunity must cite the signal it comes from. Typical patterns:

- Rapid headcount growth in sales or CS → the current tool or process won't scale
- M&A → multiple CRMs to consolidate
- New CRO / VP Sales (hired in the last 12 months) → new leaders re-evaluate tools in their first year
- Expansion into new regions or segments → multi-currency, territories, partner management
- Job posts for RevOps, "CRM migration", or a specific competitor's admin → active project or pain with the incumbent
- Spreadsheets or a homegrown system → greenfield CRM opportunity
- Contract renewal timing for the incumbent, if publicly known

Then rate fit (High / Medium / Low) and timing (Now / 6–12 months / Not now) with a one-line justification each.

## 5. Write the report

Save to `research/<company-slug>-<YYYY-MM-DD>.md` (lowercase, hyphens), then show the user the executive summary and the file path. Use this structure:

```markdown
# <Company> — CRM Sales Brief
*Prepared <date> · Entity: <legal name>, <HQ>, <website>*

## Executive summary
3–5 bullets: who they are, why they might buy a CRM now, who to approach first, fit/timing rating.

## Company brief
- **What they do:**
- **Industry / segment:**
- **HQ & footprint:**
- **Size:** employees (date, source); revenue or funding (date, source)
- **Ownership:**
- **Business model & go-to-market:**
- **Recent developments:** dated bullets, newest first

## Current sales & CRM landscape
Known or likely CRM and adjacent tools, with evidence. Sales/CS team size and structure.

## Key stakeholders
| Name | Title | Buying role | Why they matter | Source (date) |
|---|---|---|---|---|

Recommended entry point: who to contact first and why.

## Sales opportunities
For each (3–5): **Opportunity** — evidence → what our CRM solves → suggested pitch angle.

**Fit:** High/Medium/Low — reason
**Timing:** Now / 6–12 months / Not now — reason

## Suggested approach
- Opening message angle for the entry-point contact (2–3 sentences)
- 5–7 discovery questions
- Likely objections and responses
- Competitive notes vs. the incumbent

## Risks & unknowns
What we couldn't verify and what to confirm on the first call.

## Sources
Numbered list of URLs with titles and access date. Reference them as [n] in the text above.
```

Keep the brief scannable: around 1–2 pages, short bullets, no filler.
