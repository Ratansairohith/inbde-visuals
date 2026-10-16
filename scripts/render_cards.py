"""Render every element with class "card" in an HTML file to its own PNG.

Usage: python3 scripts/render_cards.py <html_file> <out_dir>
Each card needs a data-name attribute; output is <out_dir>/<data-name>.png
(rendered at 2x for crisp text on phones).
"""
import sys
import pathlib
from playwright.sync_api import sync_playwright

html_path = pathlib.Path(sys.argv[1]).resolve()
out_dir = pathlib.Path(sys.argv[2]).resolve()
out_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
    page.goto(html_path.as_uri())
    page.wait_for_load_state("networkidle")
    cards = page.query_selector_all(".card")
    for c in cards:
        name = c.get_attribute("data-name")
        out = out_dir / f"{name}.png"
        c.screenshot(path=str(out))
        print(out)
    browser.close()
