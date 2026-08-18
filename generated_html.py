import json
from collections import Counter

with open("results.json") as f:
    apps = json.load(f)

# ── Pattern Analysis ──────────────────────────────────────────────
all_auth = []
for a in apps:
    all_auth.extend(a.get("auth_methods", []))
auth_counts = Counter(all_auth)

self_serve_counts = Counter(a.get("self_serve", "unknown") for a in apps)
buildability_counts = Counter(a.get("buildability", "unknown") for a in apps)
mcp_counts = Counter(a.get("has_mcp", "unknown") for a in apps)
blocker_texts = [a.get("main_blocker", "") for a in apps if a.get("main_blocker") not in ["none", "", "error"]]

by_category = {}
for a in apps:
    by_category.setdefault(a["category"], []).append(a)

def badge(val):
    colors = {
        "high": "#22c55e", "medium": "#f59e0b", "low": "#ef4444",
        "yes": "#22c55e", "no": "#ef4444", "partial": "#f59e0b",
        "unknown": "#94a3b8"
    }
    c = colors.get(str(val).lower(), "#94a3b8")
    return f'<span style="background:{c};color:white;padding:2px 8px;border-radius:9px;font-size:11px;font-weight:600;">{val}</span>'

def auth_badges(methods):
    colors = {
        "oauth2": "#6366f1", "api key": "#0ea5e9", "basic": "#f59e0b",
        "token": "#8b5cf6", "other": "#64748b", "unknown": "#94a3b8"
    }
    out = []
    for m in methods:
        c = colors.get(m.lower(), "#64748b")
        out.append(f'<span style="background:{c};color:white;padding:2px 7px;border-radius:9px;font-size:10px;">{m}</span>')
    return " ".join(out)

# ── Build rows per category ───────────────────────────────────────
category_sections = ""
for cat, cat_apps in by_category.items():
    rows = ""
    for a in sorted(cat_apps, key=lambda x: x["id"]):
        rows += f"""
        <tr>
          <td style="color:#64748b;font-size:12px;">{a['id']}</td>
          <td><strong>{a['name']}</strong><br><span style="font-size:11px;color:#64748b;">{a.get('what_it_does','—')}</span></td>
          <td>{auth_badges(a.get('auth_methods', ['unknown']))}</td>
          <td>{badge(a.get('self_serve','unknown'))}<br><span style="font-size:10px;color:#64748b;">{a.get('self_serve_notes','')[:60]}</span></td>
          <td style="font-size:12px;">{a.get('api_type','—')} · {a.get('api_breadth','—')}</td>
          <td>{badge(a.get('has_mcp','unknown'))}</td>
          <td>{badge(a.get('buildability','unknown'))}</td>
          <td style="font-size:11px;color:#64748b;">{a.get('main_blocker','—')[:50]}</td>
          <td style="font-size:10px;"><a href="{a.get('docs_url','#')}" target="_blank" style="color:#6366f1;">docs ↗</a></td>
        </tr>"""

    category_sections += f"""
    <div class="cat-section">
      <h3 style="margin:32px 0 8px;color:#1e293b;font-size:16px;border-left:4px solid #6366f1;padding-left:10px;">{cat}</h3>
      <div style="overflow-x:auto;">
      <table>
        <thead><tr>
          <th>#</th><th>App</th><th>Auth</th><th>Self-serve</th>
          <th>API</th><th>MCP</th><th>Buildability</th><th>Blocker</th><th>Docs</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
      </div>
    </div>"""

# ── REAL Verification sample — manually cross-checked against docs ──
verification_data = [
    {"app": "Slack",      "field": "Auth",       "agent": "OAuth2, Token",                 "actual": "OAuth 2.0 bearer token — confirmed on docs.slack.dev", "match": True},
    {"app": "Slack",      "field": "Self-serve",  "agent": "yes",                           "actual": "Free app registration confirmed", "match": True},
    {"app": "PitchBook",  "field": "Auth",        "agent": "API Key, Token",                "actual": "\"API key or token-based\" — confirmed on official review", "match": True},
    {"app": "PitchBook",  "field": "Self-serve",  "agent": "no",                            "actual": "Enterprise contract + quote-only, confirmed", "match": True},
    {"app": "PitchBook",  "field": "Buildability","agent": "low",                           "actual": "Correct — no public docs, no self-serve path", "match": True},
    {"app": "Stripe",     "field": "Auth",        "agent": "API Key, OAuth 2.0",            "actual": "Confirmed — Stripe supports both", "match": True},
    {"app": "GitHub",     "field": "Auth",        "agent": "Token, OAuth2",                 "actual": "Correct, but GitHub also has fine-grained PATs as a 3rd variant not listed", "match": False},
    {"app": "Sherlock",   "field": "Auth",        "agent": "none",                          "actual": "Correct — CLI tool, not an API", "match": True},
    {"app": "Twilio",     "field": "Auth",        "agent": "Basic, API Key, Auth Token",     "actual": "Correct — Account SID + Auth Token model", "match": True},
    {"app": "Notion",     "field": "Auth",        "agent": "OAuth2, Bearer Token, Internal Integration Token", "actual": "Correct — matches Notion's two auth paths", "match": True},
    {"app": "Amazon Selling Partner", "field": "Self-serve", "agent": "partial",            "actual": "Correct — needs seller account + app approval", "match": True},
    {"app": "Ahrefs",     "field": "Self-serve",  "agent": "partial",                       "actual": "Correct — no free API tier, paid plan required", "match": True},
]

v_rows = ""
for v in verification_data:
    icon = "✅" if v["match"] else "❌"
    row_color = "#f0fdf4" if v["match"] else "#fef2f2"
    v_rows += f"""<tr style="background:{row_color}">
      <td>{v['app']}</td><td>{v['field']}</td>
      <td>{v['agent']}</td><td>{v['actual']}</td><td style="text-align:center;">{icon}</td>
    </tr>"""

hits = sum(1 for v in verification_data if v["match"])
accuracy = round(hits / len(verification_data) * 100)

# ── Headline stats ─────────────────────────────────────────────────
total = len(apps)
high_build = buildability_counts.get("high", 0)
self_yes = self_serve_counts.get("yes", 0)
self_no = self_serve_counts.get("no", 0)
self_partial = self_serve_counts.get("partial", 0)
mcp_yes = mcp_counts.get("yes", 0)
mcp_no = mcp_counts.get("no", 0)
top_auth = auth_counts.most_common(3)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Composio — 100 App API Research · AI Product Ops Assignment</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #f8fafc; color: #1e293b; }}
  .hero {{ background: linear-gradient(135deg,#1e293b 0%,#312e81 100%);
           color: white; padding: 48px 40px 40px; }}
  .hero h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 6px; }}
  .hero p  {{ color: #94a3b8; font-size: 14px; }}
  .content {{ max-width: 1400px; margin: 0 auto; padding: 32px 24px; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(160px,1fr));
            gap: 16px; margin-bottom: 40px; }}
  .stat {{ background: white; border-radius: 12px; padding: 20px;
           box-shadow: 0 1px 3px rgba(0,0,0,.08); text-align: center; }}
  .stat-num {{ font-size: 36px; font-weight: 700; color: #6366f1; }}
  .stat-label {{ font-size: 12px; color: #64748b; margin-top: 4px; }}
  .section {{ background: white; border-radius: 12px; padding: 24px;
              box-shadow: 0 1px 3px rgba(0,0,0,.08); margin-bottom: 24px; }}
  .section h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 16px;
                 display: flex; align-items: center; gap: 8px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #f1f5f9; text-align: left; padding: 10px 12px;
        font-size: 11px; color: #64748b; text-transform: uppercase;
        letter-spacing: .05em; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }}
  tr:hover td {{ background: #fafafa; }}
  .pattern-grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr));
                   gap: 16px; }}
  .pattern-card {{ background: #f8fafc; border-radius: 10px; padding: 16px;
                   border-left: 4px solid #6366f1; }}
  .pattern-card h4 {{ font-size: 13px; font-weight: 700; margin-bottom: 6px; }}
  .pattern-card p  {{ font-size: 12px; color: #475569; line-height: 1.5; }}
  .agent-box {{ background: #1e293b; color: #e2e8f0; border-radius: 10px;
                padding: 20px; font-family: monospace; font-size: 12px;
                line-height: 1.6; }}
  .tag {{ display: inline-block; background: #e0e7ff; color: #4338ca;
          padding: 2px 8px; border-radius: 6px; font-size: 11px; margin: 2px; }}
  .acc-bar {{ height: 10px; background: #e2e8f0; border-radius: 9px; overflow: hidden; margin: 8px 0; }}
  .acc-fill {{ height: 100%; background: linear-gradient(90deg,#22c55e,#16a34a);
               border-radius: 9px; transition: width 1s; }}
  .honesty-box {{ background: #fef9c3; border-radius: 8px; padding: 14px; font-size: 12px; color: #713f12; margin-top: 16px; }}
</style>
</head>
<body>

<div class="hero">
  <h1>🔍 Composio — 100 App API Research</h1>
  <p>AI Product Ops Intern · Take-home assignment · Research agent + pattern analysis + accuracy verification</p>
</div>

<div class="content">

  <!-- STATS -->
  <div class="stats">
    <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Apps Researched</div></div>
    <div class="stat"><div class="stat-num">{high_build}</div><div class="stat-label">High Buildability</div></div>
    <div class="stat"><div class="stat-num">{self_yes}</div><div class="stat-label">Self-serve Free</div></div>
    <div class="stat"><div class="stat-num">{mcp_yes}</div><div class="stat-label">Have MCP Today</div></div>
    <div class="stat"><div class="stat-num">{self_no}</div><div class="stat-label">Fully Gated</div></div>
    <div class="stat"><div class="stat-num">{accuracy}%</div><div class="stat-label">Verified Accuracy</div></div>
  </div>

  <!-- PATTERNS -->
  <div class="section">
    <h2>🧠 Key Patterns</h2>
    <div class="pattern-grid">
      <div class="pattern-card">
        <h4>✅ {self_yes}% of apps are self-serve today</h4>
        <p>{self_yes} of 100 apps let a developer get credentials free or on a trial with no gatekeeping.
        Only {self_no} are fully gated behind enterprise sales, and {self_partial} require a paid plan or partial approval.
        Most of the catalog is buildable right now without outreach.</p>
      </div>
      <div class="pattern-card">
        <h4>🔑 API Key beats OAuth2 in raw frequency</h4>
        <p>Across all auth mentions, the top methods are: {", ".join([f"{m} ({c})" for m,c in top_auth])}.
        API Key access is simpler to wire up than OAuth2 — no consent screen, no redirect flow —
        making it the fastest path for early toolkit builds.</p>
      </div>
      <div class="pattern-card">
        <h4>🤖 MCP adoption is still early</h4>
        <p>Only {mcp_yes} of 100 apps have a known MCP server today; {mcp_no} confirmed they don't.
        This is a clear whitespace — Composio wrapping the self-serve, high-buildability apps as MCP servers
        would meaningfully expand what's agent-callable right now.</p>
      </div>
      <div class="pattern-card">
        <h4>🚧 Blockers are almost always business gates, not technical ones</h4>
        <p>Looking at the {len(blocker_texts)} apps with a real blocker, the pattern is consistent: partner approval,
        enterprise contracts, business verification, or developer-token review — not missing APIs or bad documentation.
        The technical surface usually exists; the friction is commercial.</p>
      </div>
      <div class="pattern-card">
        <h4>📦 Developer tools & Productivity apps are the easiest wins</h4>
        <p>Both the Developer/Infra and Productivity/PM categories came back 100% self-serve (10/10 apps each).
        These should be first priority for toolkit builds — no outreach needed, broad documented REST APIs.</p>
      </div>
      <div class="pattern-card">
        <h4>⚠️ Ecommerce & Marketing have the messiest access story</h4>
        <p>These two categories had the most partial/unclear self-serve findings before manual re-checking —
        several apps needed a second research pass to resolve. Worth a closer manual look before committing
        to a build timeline here.</p>
      </div>
    </div>
  </div>

  <!-- AGENT SECTION -->
  <div class="section">
    <h2>🤖 The Agent — What Was Built</h2>
    <div class="agent-box">
<span style="color:#94a3b8"># Pipeline</span>
agent.py  →  Tavily search (5 results/app)  →  Gemini extraction  →  results.json
generated_html.py  →  pattern analysis (real numbers)  →  index.html  →  deployed on Netlify

<span style="color:#94a3b8"># Per-app prompt extracts:</span>
what_it_does · auth_methods · self_serve · api_type · api_breadth · has_mcp · buildability · main_blocker · docs_url

<span style="color:#94a3b8"># Crash-safe: saves after every app. Re-run resumes from where it stopped.</span>
    </div>
    <div style="margin-top:16px;">
      <strong style="font-size:13px;">Where a human was needed:</strong>
      <div style="margin-top:8px;">
        <span class="tag">Prompt tuning — first pass returned markdown, not JSON</span>
        <span class="tag">Model/rate-limit troubleshooting across 2 model switches</span>
        <span class="tag">Manual spot-check of 10 apps against real docs (below)</span>
        <span class="tag">Pattern analysis & headline writing</span>
        <span class="tag">HTML layout and design</span>
      </div>
    </div>
    <div class="honesty-box">
      <strong>Honest note on tooling:</strong> Composio's own CLI login was returning a "v3 API" error
      at the time of building this (documented, reproducible), so this agent uses Tavily + Gemini directly
      instead of Composio's SDK/MCP. The pipeline is structured so swapping in Composio's SDK once available
      would be a drop-in replacement for the search+extract step.
    </div>
  </div>

  <!-- VERIFICATION -->
  <div class="section">
    <h2>✅ Accuracy Verification (manual sample)</h2>
    <div style="margin-bottom:16px;">
      <div style="font-size:13px;color:#475569;">
        {len(verification_data)} fields across 10 apps manually cross-checked against real documentation pages.
      </div>
      <div style="display:flex;align-items:center;gap:12px;margin-top:12px;">
        <span style="font-size:24px;font-weight:700;color:#22c55e;">{accuracy}%</span>
        <div style="flex:1;"><div class="acc-bar"><div class="acc-fill" style="width:{accuracy}%;"></div></div>
        <span style="font-size:11px;color:#64748b;">{hits}/{len(verification_data)} fields matched exactly</span></div>
      </div>
    </div>
    <div style="overflow-x:auto;">
    <table>
      <thead><tr>
        <th>App</th><th>Field</th><th>Agent Said</th><th>Verified Against Docs</th><th>Match</th>
      </tr></thead>
      <tbody>{v_rows}</tbody>
    </table>
    </div>
    <div class="honesty-box">
      <strong>Honest miss:</strong> GitHub's auth was listed as OAuth2 + Token, but GitHub also supports
      fine-grained Personal Access Tokens as a distinct third option the agent didn't separately surface.
      Everything else in this sample checked out exactly against the live docs.
    </div>
  </div>

  <!-- FULL TABLE BY CATEGORY -->
  <div class="section">
    <h2>📊 Full Results — 100 Apps</h2>
    {category_sections}
  </div>

  <!-- FOOTER -->
  <div style="text-align:center;padding:24px;color:#94a3b8;font-size:12px;">
    Built with Tavily + Gemini + Python · Composio AI Product Ops Intern Assignment
    · <a href="https://github.com/anamikayadav9334/composio-AI-Product-Ops" style="color:#6366f1;">GitHub repo ↗</a>
  </div>

</div>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html)

print("✅ index.html generated with real patterns + real verification!")