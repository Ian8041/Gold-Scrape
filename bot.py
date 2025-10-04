import os
import requests
from playwright.sync_api import sync_playwright

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GRP_CHAT_IDS = ("GRP_CHAT_IDS")
URL = "https://www.kitco.com/charts/gold"
VALUE_SELECTOR = ".font-mulish.mb-\\[3px\\].text-4xl.font-bold.leading-normal.tracking-\\[1px\\]"

def send_telegram_message(text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": GRP_CHAT_IDS, "text": text}
    )

def send_telegram_photo(filepath):
    with open(filepath, "rb") as f:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": GRP_CHAT_IDS},
            files={"photo": f}
        )

# ---- Scraping and sending for bot ----
# def scrape_and_send():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(URL)

#         try:
#             page.wait_for_selector(VALUE_SELECTOR, timeout=10000)
#             value = page.text_content(VALUE_SELECTOR).strip()
#         except Exception as e:
#             value = f"Could not extract value! Error: {e}"

#         screenshot_path = "screenshot.png"
#         page.screenshot(path=screenshot_path, full_page=True)
#         browser.close()

#     send_telegram_message(f"Latest value: {value}")
#     send_telegram_photo(screenshot_path)

# ---- Scraping and sending to group chat ----
def scrape_and_send():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        try:
            page.wait_for_selector(VALUE_SELECTOR, timeout=10000)
            value = page.text_content(VALUE_SELECTOR).strip()
        except Exception as e:
            value = f"Could not extract value! Error: {e}"
            
        page.set_viewport_size({"width": 1200, "height": 1500})
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path)
        browser.close()

    # Send to Telegram group
    send_telegram_message(f"Latest value: {value}")
    send_telegram_photo(screenshot_path)


if __name__ == "__main__":
    scrape_and_send()
