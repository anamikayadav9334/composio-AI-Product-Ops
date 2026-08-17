import os
import json
import time
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


APPS = [
    # CRM and Sales
    {"id": 1,  "name": "Salesforce",                 "url": "salesforce.com",                                  "category": "CRM and Sales"},
    {"id": 2,  "name": "HubSpot",                    "url": "hubspot.com",                                     "category": "CRM and Sales"},
    {"id": 3,  "name": "Pipedrive",                  "url": "pipedrive.com",                                   "category": "CRM and Sales"},
    {"id": 4,  "name": "Attio",                      "url": "attio.com",                                       "category": "CRM and Sales"},
    {"id": 5,  "name": "Twenty",                     "url": "twenty.com",                                      "category": "CRM and Sales"},
    {"id": 6,  "name": "Podio",                      "url": "podio.com",                                       "category": "CRM and Sales"},
    {"id": 7,  "name": "Zoho CRM",                   "url": "zoho.com/crm",                                    "category": "CRM and Sales"},
    {"id": 8,  "name": "Close",                      "url": "close.com",                                       "category": "CRM and Sales"},
    {"id": 9,  "name": "Copper",                     "url": "copper.com",                                      "category": "CRM and Sales"},
    {"id": 10, "name": "DealCloud",                  "url": "api.docs.dealcloud.com",                          "category": "CRM and Sales"},
    # Support and Helpdesk
    {"id": 11, "name": "Zendesk",                    "url": "zendesk.com",                                     "category": "Support and Helpdesk"},
    {"id": 12, "name": "Intercom",                   "url": "intercom.com",                                    "category": "Support and Helpdesk"},
    {"id": 13, "name": "Freshdesk",                  "url": "freshdesk.com",                                   "category": "Support and Helpdesk"},
    {"id": 14, "name": "Front",                      "url": "front.com",                                       "category": "Support and Helpdesk"},
    {"id": 15, "name": "Pylon",                      "url": "usepylon.com",                                    "category": "Support and Helpdesk"},
    {"id": 16, "name": "LiveAgent",                  "url": "liveagent.com",                                   "category": "Support and Helpdesk"},
    {"id": 17, "name": "Plain",                      "url": "plain.com",                                       "category": "Support and Helpdesk"},
    {"id": 18, "name": "Help Scout",                 "url": "helpscout.com",                                   "category": "Support and Helpdesk"},
    {"id": 19, "name": "Gorgias",                    "url": "gorgias.com",                                     "category": "Support and Helpdesk"},
    {"id": 20, "name": "Gladly",                     "url": "gladly.com",                                      "category": "Support and Helpdesk"},
    # Communications and Messaging
    {"id": 21, "name": "Slack",                      "url": "slack.com",                                       "category": "Communications and Messaging"},
    {"id": 22, "name": "Twilio",                     "url": "twilio.com",                                      "category": "Communications and Messaging"},
    {"id": 23, "name": "Zoho Cliq",                  "url": "zoho.com/cliq",                                   "category": "Communications and Messaging"},
    {"id": 24, "name": "Lark",                       "url": "open.larksuite.com",                              "category": "Communications and Messaging"},
    {"id": 25, "name": "Pumble",                     "url": "pumble.com",                                      "category": "Communications and Messaging"},
    {"id": 26, "name": "Discord",                    "url": "discord.com",                                     "category": "Communications and Messaging"},
    {"id": 27, "name": "Telegram",                   "url": "core.telegram.org",                               "category": "Communications and Messaging"},
    {"id": 28, "name": "WhatsApp Business",          "url": "developers.facebook.com/docs/whatsapp",           "category": "Communications and Messaging"},
    {"id": 29, "name": "Aircall",                    "url": "aircall.io",                                      "category": "Communications and Messaging"},
    {"id": 30, "name": "Vonage",                     "url": "developer.vonage.com",                            "category": "Communications and Messaging"},
    # Marketing, Ads, Email and Social
    {"id": 31, "name": "Google Ads",                 "url": "developers.google.com/google-ads",                "category": "Marketing, Ads, Email and Social"},
    {"id": 32, "name": "Meta Ads",                   "url": "developers.facebook.com/docs/marketing-apis",     "category": "Marketing, Ads, Email and Social"},
    {"id": 33, "name": "LinkedIn Ads",               "url": "learn.microsoft.com/linkedin/marketing",          "category": "Marketing, Ads, Email and Social"},
    {"id": 34, "name": "GoHighLevel",                "url": "highlevel.stoplight.io",                          "category": "Marketing, Ads, Email and Social"},
    {"id": 35, "name": "Mailchimp",                  "url": "mailchimp.com/developer",                         "category": "Marketing, Ads, Email and Social"},
    {"id": 36, "name": "Klaviyo",                    "url": "developers.klaviyo.com",                          "category": "Marketing, Ads, Email and Social"},
    {"id": 37, "name": "Systeme.io",                 "url": "systeme.io",                                      "category": "Marketing, Ads, Email and Social"},
    {"id": 38, "name": "Pinterest",                  "url": "developers.pinterest.com",                        "category": "Marketing, Ads, Email and Social"},
    {"id": 39, "name": "Threads",                    "url": "developers.facebook.com/docs/threads",            "category": "Marketing, Ads, Email and Social"},
    {"id": 40, "name": "SendGrid",                   "url": "sendgrid.com",                                    "category": "Marketing, Ads, Email and Social"},
    # Ecommerce
    {"id": 41, "name": "Shopify",                    "url": "shopify.dev",                                     "category": "Ecommerce"},
    {"id": 42, "name": "WooCommerce",                "url": "woocommerce.com/document/woocommerce-rest-api",   "category": "Ecommerce"},
    {"id": 43, "name": "BigCommerce",                "url": "developer.bigcommerce.com",                       "category": "Ecommerce"},
    {"id": 44, "name": "Salesforce Commerce Cloud",  "url": "developer.salesforce.com/docs/commerce",          "category": "Ecommerce"},
    {"id": 45, "name": "Magento",                    "url": "developer.adobe.com/commerce",                    "category": "Ecommerce"},
    {"id": 46, "name": "Squarespace",                "url": "developers.squarespace.com",                      "category": "Ecommerce"},
    {"id": 47, "name": "Ecwid",                      "url": "api-docs.ecwid.com",                              "category": "Ecommerce"},
    {"id": 48, "name": "Gumroad",                    "url": "gumroad.com/api",                                 "category": "Ecommerce"},
    {"id": 49, "name": "Amazon Selling Partner",     "url": "developer-docs.amazon.com/sp-api",                "category": "Ecommerce"},
    {"id": 50, "name": "Fanbasis",                   "url": "fanbasis.com",                                    "category": "Ecommerce"},
    # Data, SEO and Scraping
    {"id": 51, "name": "DataForSEO",                 "url": "docs.dataforseo.com",                             "category": "Data, SEO and Scraping"},
    {"id": 52, "name": "SE Ranking",                 "url": "seranking.com/api",                               "category": "Data, SEO and Scraping"},
    {"id": 53, "name": "Ahrefs",                     "url": "ahrefs.com/api",                                  "category": "Data, SEO and Scraping"},
    {"id": 54, "name": "MrScraper",                  "url": "docs.mrscraper.com",                              "category": "Data, SEO and Scraping"},
    {"id": 55, "name": "Apify",                      "url": "docs.apify.com",                                  "category": "Data, SEO and Scraping"},
    {"id": 56, "name": "Firecrawl",                  "url": "firecrawl.dev",                                   "category": "Data, SEO and Scraping"},
    {"id": 57, "name": "Bright Data",                "url": "brightdata.com",                                  "category": "Data, SEO and Scraping"},
    {"id": 58, "name": "Sherlock",                   "url": "github.com/sherlock-project/sherlock",            "category": "Data, SEO and Scraping"},
    {"id": 59, "name": "Waterfall.io",               "url": "waterfall.io",                                    "category": "Data, SEO and Scraping"},
    {"id": 60, "name": "Clay",                       "url": "clay.com",                                        "category": "Data, SEO and Scraping"},
    # Developer, Infra and Data platforms
    {"id": 61, "name": "GitHub",                     "url": "docs.github.com/rest",                            "category": "Developer, Infra and Data"},
    {"id": 62, "name": "Vercel",                     "url": "vercel.com/docs/rest-api",                        "category": "Developer, Infra and Data"},
    {"id": 63, "name": "Netlify",                    "url": "docs.netlify.com/api",                            "category": "Developer, Infra and Data"},
    {"id": 64, "name": "Cloudflare",                 "url": "developers.cloudflare.com/api",                   "category": "Developer, Infra and Data"},
    {"id": 65, "name": "Supabase",                   "url": "supabase.com/docs",                               "category": "Developer, Infra and Data"},
    {"id": 66, "name": "Neo4j",                      "url": "neo4j.com/docs/api",                              "category": "Developer, Infra and Data"},
    {"id": 67, "name": "Snowflake",                  "url": "docs.snowflake.com",                              "category": "Developer, Infra and Data"},
    {"id": 68, "name": "MongoDB Atlas",              "url": "mongodb.com/docs/atlas/api",                      "category": "Developer, Infra and Data"},
    {"id": 69, "name": "Datadog",                    "url": "docs.datadoghq.com/api",                          "category": "Developer, Infra and Data"},
    {"id": 70, "name": "Sentry",                     "url": "docs.sentry.io/api",                              "category": "Developer, Infra and Data"},
    # Productivity and Project Management
    {"id": 71, "name": "Notion",                     "url": "developers.notion.com",                           "category": "Productivity and Project Management"},
    {"id": 72, "name": "Airtable",                   "url": "airtable.com/developers",                         "category": "Productivity and Project Management"},
    {"id": 73, "name": "Linear",                     "url": "developers.linear.app",                           "category": "Productivity and Project Management"},
    {"id": 74, "name": "Jira",                       "url": "developer.atlassian.com",                         "category": "Productivity and Project Management"},
    {"id": 75, "name": "Asana",                      "url": "developers.asana.com",                            "category": "Productivity and Project Management"},
    {"id": 76, "name": "Monday.com",                 "url": "developer.monday.com",                            "category": "Productivity and Project Management"},
    {"id": 77, "name": "ClickUp",                    "url": "clickup.com/api",                                 "category": "Productivity and Project Management"},
    {"id": 78, "name": "Coda",                       "url": "coda.io/developers",                              "category": "Productivity and Project Management"},
    {"id": 79, "name": "Smartsheet",                 "url": "smartsheet.com/developers",                       "category": "Productivity and Project Management"},
    {"id": 80, "name": "Harvest",                    "url": "help.getharvest.com/api-v2",                      "category": "Productivity and Project Management"},
    # Finance and Fintech
    {"id": 81, "name": "Stripe",                     "url": "stripe.com/docs/api",                             "category": "Finance and Fintech"},
    {"id": 82, "name": "Plaid",                      "url": "plaid.com/docs",                                  "category": "Finance and Fintech"},
    {"id": 83, "name": "Binance",                    "url": "binance-docs.github.io",                          "category": "Finance and Fintech"},
    {"id": 84, "name": "Paygent Connect",            "url": "paygent.com",                                     "category": "Finance and Fintech"},
    {"id": 85, "name": "iPayX",                      "url": "ipayx.ai/docs",                                   "category": "Finance and Fintech"},
    {"id": 86, "name": "QuickBooks",                 "url": "developer.intuit.com",                            "category": "Finance and Fintech"},
    {"id": 87, "name": "Xero",                       "url": "developer.xero.com",                              "category": "Finance and Fintech"},
    {"id": 88, "name": "Brex",                       "url": "developer.brex.com",                              "category": "Finance and Fintech"},
    {"id": 89, "name": "Ramp",                       "url": "docs.ramp.com",                                   "category": "Finance and Fintech"},
    {"id": 90, "name": "PitchBook",                  "url": "pitchbook.com",                                   "category": "Finance and Fintech"},
    # AI, Research and Media
    {"id": 91, "name": "NotebookLM",                 "url": "cloud.google.com/gemini",                         "category": "AI, Research and Media"},
    {"id": 92, "name": "Otter AI",                   "url": "help.otter.ai",                                   "category": "AI, Research and Media"},
    {"id": 93, "name": "Fathom",                     "url": "fathom.video",                                    "category": "AI, Research and Media"},
    {"id": 94, "name": "Consensus",                  "url": "consensus.app",                                   "category": "AI, Research and Media"},
    {"id": 95, "name": "Reducto",                    "url": "reducto.ai",                                      "category": "AI, Research and Media"},
    {"id": 96, "name": "Devin",                      "url": "docs.devin.ai",                                   "category": "AI, Research and Media"},
    {"id": 97, "name": "Higgsfield",                 "url": "higgsfield.ai",                                   "category": "AI, Research and Media"},
    {"id": 98, "name": "Mermaid CLI",                "url": "github.com/mermaid-js/mermaid-cli",               "category": "AI, Research and Media"},
    {"id": 99, "name": "YouTube Transcript",         "url": "transcriptapi.com",                               "category": "AI, Research and Media"},
    {"id": 100,"name": "Grain",                      "url": "grain.com",                                       "category": "AI, Research and Media"},
]


def research_app(app):
    query = f"{app['name']} API authentication method developer docs self-serve access"
    try:
        results = tavily.search(query=query, max_results=5)
        search_content = "\n\n".join([
            f"URL: {r.get('url','')}\n{r.get('content','')}"
            for r in results.get('results', [])
        ])
        docs_urls = [r.get('url', '') for r in results.get('results', [])]

        prompt = f"""You are researching APIs for an AI agent toolkit company called Composio.
Research this app and return ONLY a valid JSON object, no markdown, no explanation.

App: {app['name']}
Website: {app['url']}
Category: {app['category']}

Search results:
{search_content[:3000]}

Return ONLY this JSON (no other text):
{{
  "what_it_does": "one line description of the app",
  "auth_methods": ["list OAuth2 / API Key / Basic / Token / other"],
  "self_serve": "yes / no / partial",
  "self_serve_notes": "brief: free trial, paid only, partner approval needed, etc.",
  "api_type": "REST / GraphQL / both / none",
  "api_breadth": "broad / moderate / narrow / none",
  "has_mcp": "yes / no / unknown",
  "buildability": "high / medium / low",
  "main_blocker": "none / or brief description of main blocker",
  "docs_url": "best docs URL from search results"
}}"""

        message = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
        raw = message.text.strip()
        # strip markdown fences if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        data = json.loads(raw)
        data.update({"id": app["id"], "name": app["name"],
                     "category": app["category"], "website": app["url"]})
        return data

    except Exception as e:
        print(f"  ⚠ Error on {app['name']}: {e}")
        return {
            "id": app["id"], "name": app["name"],
            "category": app["category"], "website": app["url"],
            "what_it_does": "Research failed",
            "auth_methods": ["unknown"], "self_serve": "unknown",
            "self_serve_notes": str(e), "api_type": "unknown",
            "api_breadth": "unknown", "has_mcp": "unknown",
            "buildability": "unknown", "main_blocker": "error",
            "docs_url": app["url"]
        }


def main():
    results = []

    # Resume support — if results.json exists, skip already done
    if os.path.exists("results.json"):
        with open("results.json", "r") as f:
            results = json.load(f)
        done_ids = {r["id"] for r in results}
        print(f"▶ Resuming — {len(results)} apps already done\n")
    else:
        done_ids = set()

    for app in APPS:
        if app["id"] in done_ids:
            continue
        print(f"[{app['id']:>3}/100] {app['name']} ...", end=" ", flush=True)
        result = research_app(app)
        results.append(result)
        print(f"✓ buildability={result.get('buildability','?')} | auth={result.get('auth_methods','?')}")

        # Save after every app (crash-safe)
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)

        time.sleep(1)  # polite rate limit

    print(f"\n✅ Done! {len(results)} apps saved to results.json")


if __name__ == "__main__":
    main()