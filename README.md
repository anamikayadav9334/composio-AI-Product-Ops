# Composio — 100 App API Research Agent

AI Product Ops Intern take-home assignment. Researches API/auth/access details for 100 apps across 10 categories, then generates a single self-explanatory HTML report.

## Live report

https://bespoke-taffy-ef8612.netlify.app
## What it does

1. `agent.py` — for each of the 100 apps: searches the web (Tavily), sends the results to Gemini to extract structured fields (auth method, self-serve status, API type, MCP availability, buildability verdict, blocker, docs URL), and saves everything to `results.json`. Crash-safe — re-running resumes from where it stopped.
2. `generate_html.py` — reads `results.json`, computes patterns (auth distribution, self-serve vs gated split, common blockers), and generates a single `index.html` report with the full table, headline patterns, and a manual verification section.

## How to run

```bash
pip install google-genai tavily-python python-dotenv

# Add to .env:
# TAVILY_API_KEY=your_key
# GEMINI_API_KEY=your_key

python3 agent.py           # researches all 100 apps → results.json
python3 generated_html.py  # builds the report → index.html
open index.html
```

## Where a human was needed

- Prompt tuning — first pass returned markdown-wrapped JSON, had to add fence-stripping logic
- Model/rate-limit troubleshooting — switched models twice due to free-tier quota limits
- Manual verification of ~12 apps against real docs pages (see report)
- Pattern analysis and headline writing
- HTML layout and design

## Accuracy / Verification

See the "Accuracy Verification" section in `index.html` — a sample of apps were manually cross-checked against real documentation, with hits and misses shown honestly.

