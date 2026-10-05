from playwright.sync_api import sync_playwright
import time
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import *

def wait_seconds():
    print(f"      ⏳ Waiting {WAIT_SECONDS} seconds...")
    for i in range(WAIT_SECONDS, 0, -1):
        print(f"\r      ⏳ {i:2d} seconds remaining...", end="", flush=True)
        time.sleep(1)
    print("\r      ⏳ Ready to click.                 ")

def highlight_element(page, selector: str):
    try:
        page.evaluate("""
            (selector) => {
                const els = document.querySelectorAll(selector);
                els.forEach(el => {
                    el.style.outline = '5px solid red';
                    el.style.outlineOffset = '4px';
                    el.style.backgroundColor = 'rgba(255, 255, 0, 0.4)';
                    el.scrollIntoView({behavior: 'smooth', block: 'center'});
                });
            }
        """, selector)
        print("      🔴 Highlighted")
        time.sleep(1.5)
    except:
        pass

def parse_resolution(res: str):
    w, h = res.split("x")
    return {"width": int(w), "height": int(h)}

def get_user_agent(device: str):
    if device == "mobile":
        return "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    elif device == "tablet":
        return "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
    else:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def parse_proxy(proxy_str: str):
    """Convert http://user:pass@ip:port → dict"""
    if not proxy_str:
        return None
    try:
        # Remove http://
        clean = proxy_str.replace("http://", "").replace("https://", "")
        if "@" in clean:
            auth, server = clean.split("@")
            username, password = auth.split(":")
            return {
                "server": f"http://{server}",
                "username": username,
                "password": password
            }
        else:
            return {"server": f"http://{clean}"}
    except:
        return None

def run_one_bot(bot: dict, proxy_str: str | None = None):
    print(f"\n{'='*60}")
    print(f"🚀 {bot['bot']} | {bot['country']} | {bot['device']}")
    
    proxy_config = parse_proxy(proxy_str) if proxy_str else None
    if proxy_config:
        print(f"   🌐 Using proxy: {proxy_config['server']}")
    else:
        print("   ⚠️ No proxy")

    viewport = parse_resolution(bot["resolution"])
    user_agent = get_user_agent(bot["device"])

    with sync_playwright() as p:
        launch_options = {
            "headless": HEADLESS,
            "slow_mo": SLOW_MO,
            "args": [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        }

        if proxy_config:
            launch_options["proxy"] = proxy_config

        browser = None
        try:
            browser = p.chromium.launch(**launch_options)
            context = browser.new_context(
                user_agent=user_agent,
                viewport=viewport,
                locale="en-US",
                ignore_https_errors=True,
            )
            page = context.new_page()

            print("   🌐 Loading website...")
            page.goto(WEBSITE_URL, wait_until="domcontentloaded", timeout=90000)

            for i, target in enumerate(CLICK_TARGETS, 1):
                print(f"   → Click {i}/8 : {target['name']}")
                wait_seconds()
                highlight_element(page, target["selector"])

                try:
                    page.click(target["selector"], timeout=12000, force=True)
                    print("      ✅ Click successful")
                except:
                    try:
                        page.locator(target["selector"]).first.click(timeout=8000, force=True)
                        print("      ✅ Clicked first match")
                    except Exception as e:
                        print(f"      ❌ Failed: {str(e)[:80]}")

                time.sleep(1.5)

            print(f"✅ {bot['bot']} finished all 8 clicks")

        except Exception as e:
            print(f"❌ {bot['bot']} error: {str(e)[:120]}")
        finally:
            if browser:
                browser.close()
            print(f"🔒 {bot['bot']} closed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual", action="store_true")
    parser.add_argument("--bots", type=int, default=10)
    args = parser.parse_args()

    if args.manual:
        print("\n🟡 MANUAL MODE - Press ENTER to start...")
        input()

    print(f"\nStarting {args.bots} bots in PARALLEL (headless={HEADLESS})")
    print(f"Wait time: {WAIT_SECONDS} seconds per click\n")

    proxy_list = []
    for i in range(args.bots):
        if PROXIES:
            proxy_list.append(PROXIES[i % len(PROXIES)])
        else:
            proxy_list.append(None)

    with ThreadPoolExecutor(max_workers=min(args.bots, 5)) as executor:
        futures = [
            executor.submit(run_one_bot, BOTS[i], proxy_list[i])
            for i in range(args.bots)
        ]
        for f in as_completed(futures):
            f.result()

    print("\n🎉 All bots completed!")

if __name__ == "__main__":
    main()
