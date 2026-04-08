import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = int(os.environ["CHAT_ID"])
USERNAME  = os.environ["USERNAME"]
PASSWORD  = os.environ["PASSWORD"]
SCREENSHOT_PATH = "attendance.png"

def capture_attendance():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        # pretend to be a real browser
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        page.goto("https://ims.ritchennai.edu.in/login", wait_until="domcontentloaded")
        page.wait_for_selector("#email", timeout=60000)  # wait up to 60 seconds
        page.fill("#email", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("button[type=submit]")
        page.wait_for_load_state("networkidle")

        page.goto("https://ims.ritchennai.edu.in/admin/student-personal-attendance/report", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        browser.close()
        print("✅ Screenshot saved!")

def send_to_telegram():
    capture_attendance()

    with open(SCREENSHOT_PATH, "rb") as photo:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "📋 Daily Attendance"},
            files={"photo": photo}
        )
    print(r.json())

if __name__ == "__main__":
    send_to_telegram()
