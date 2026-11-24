from pathlib import Path

import os
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]

with sync_playwright() as p, TemporaryDirectory() as temp:
    browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH"))
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri())
    page.locator("#room").fill("Kitchen")
    page.locator("#contents").fill("Plates and bowls")
    page.locator("#fragile").check()
    page.get_by_role("button", name="Add label").click()
    assert "FRAGILE" in page.locator("article").inner_text()
    page.emulate_media(media="print")
    assert (
        page.locator("article").is_visible() and not page.locator("form").is_visible()
    )
    assert page.pdf().startswith(b"%PDF")
    assert not errors, errors
    browser.close()
