from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://unstop.com/internships?term=Frontend")
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        page.screenshot(path="unstop_screenshot.png")
        browser.close()

if __name__ == "__main__":
    run()
