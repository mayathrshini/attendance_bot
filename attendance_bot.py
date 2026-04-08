import os
import requests
import time
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

SCREENSHOT_PATH = "attendance.png"
SCREENSHOT_PATH = r"D:\attendance\attendance.png"

def capture_attendance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ims.ritchennai.edu.in/login")
        page.fill("#email", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("button[type=submit]")
        page.wait_for_load_state("networkidle")

        # Navigate to attendance page
        page.goto("https://ims.ritchennai.edu.in/admin/student-personal-attendance/report")
        page.wait_for_load_state("networkidle")

        page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        browser.close()
        print("✅ Screenshot saved!")

def send_to_telegram():
    capture_attendance()

    if not os.path.exists(SCREENSHOT_PATH):
        print("❌ Screenshot was NOT created!")
        return

    print(f"✅ File size: {os.path.getsize(SCREENSHOT_PATH)} bytes")

    with open(SCREENSHOT_PATH, "rb") as photo:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "📋 Daily Attendance"},
            files={"photo": photo}
        )
    print(r.json())



if __name__ == "__main__":
    send_to_telegram()   # run once immediately to test
   
