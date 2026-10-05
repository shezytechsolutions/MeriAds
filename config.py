import os
from dotenv import load_dotenv

load_dotenv()

WEBSITE_URL = os.getenv("WEBSITE_URL", "https://tech-news-modern-digital-magazine-reviews.ai.studio/")

CLICK_TARGETS = [
    {"name": "1. Header Desktop 728×90", "selector": 'header .hidden.md\\:flex iframe[title^="ad-"]'},
    {"name": "2. Header Mobile 320×50", "selector": 'header .flex.md\\:hidden iframe[title^="ad-"]'},
    {"name": "3. Main content mid-page 468×60", "selector": 'main .lg\\:col-span-8 iframe[title^="ad-"]'},
    {"name": "4. Main content mobile 320×50", "selector": 'main .lg\\:col-span-8 iframe[title^="ad-"]'},
    {"name": "5. Sidebar 300×250", "selector": 'aside iframe[title^="ad-"][width="300"]'},
    {"name": "6. Sidebar 160×300", "selector": 'aside iframe[title^="ad-"][height="300"]'},
    {"name": "7. Sidebar 160×600", "selector": 'aside iframe[title^="ad-"][height="600"]'},
    {"name": "8. Footer 728×90", "selector": 'main .mt-12 iframe[title^="ad-"]'},
]

BOTS = [
    {"bot": "Bot 1",  "country": "US", "device": "desktop", "resolution": "1920x1080"},
    {"bot": "Bot 2",  "country": "GB", "device": "mobile",  "resolution": "390x844"},
    {"bot": "Bot 3",  "country": "DE", "device": "laptop",  "resolution": "1366x768"},
    {"bot": "Bot 4",  "country": "FR", "device": "tablet",  "resolution": "820x1180"},
    {"bot": "Bot 5",  "country": "CA", "device": "desktop", "resolution": "1920x1080"},
    {"bot": "Bot 6",  "country": "AU", "device": "mobile",  "resolution": "412x915"},
    {"bot": "Bot 7",  "country": "IN", "device": "laptop",  "resolution": "1440x900"},
    {"bot": "Bot 8",  "country": "JP", "device": "tablet",  "resolution": "768x1024"},
    {"bot": "Bot 9",  "country": "BR", "device": "desktop", "resolution": "2560x1440"},
    {"bot": "Bot 10", "country": "AE", "device": "mobile",  "resolution": "360x800"},
]

# Headless is forced True on GitHub / servers
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "50"))
WAIT_SECONDS = int(os.getenv("WAIT_SECONDS", "10"))

# Proxies from environment (recommended for GitHub)
# Format in .env or GitHub Secrets: 
# PROXY_1=http://user:pass@ip:port
# or leave empty
PROXIES = []
for i in range(1, 11):
    p = os.getenv(f"PROXY_{i}")
    if p:
        PROXIES.append(p)
