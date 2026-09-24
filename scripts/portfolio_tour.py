#!/usr/bin/env python3
"""Capture a section-by-section tour of the portfolio for the README preview."""
import io
import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

URL = "https://ojas-srivastava.vercel.app/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data"
FRAME = (1120, 700)
WANTED = ["top", "brief", "experience", "projects", "coding-stats", "achievements", "contact"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.goto(URL, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(2500)

        height = page.evaluate("document.documentElement.scrollHeight")
        for y in range(0, height, 400):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(120)

        ids = page.evaluate("[...document.querySelectorAll('section[id], [id]')].map(e => e.id)")
        frames = []
        for sid in WANTED:
            if sid == "top":
                page.evaluate("window.scrollTo(0, 0)")
            elif sid in ids:
                page.evaluate(f"document.getElementById('{sid}').scrollIntoView({{block: 'start'}})")
            else:
                continue
            page.wait_for_timeout(1800)
            png = page.screenshot(type="png")
            img = Image.open(io.BytesIO(png)).convert("RGB").resize(FRAME, Image.LANCZOS)
            name = f"tour-{len(frames)}.jpg"
            img.save(OUT / name, "JPEG", quality=64, optimize=True, progressive=True)
            frames.append({"file": name, "hash": "" if sid == "top" else f"#{sid}"})
        browser.close()

    if len(frames) < 3:
        sys.exit("tour capture failed: too few frames")
    for stale in OUT.glob("tour-*.jpg"):
        if stale.name not in {f["file"] for f in frames}:
            stale.unlink()
    (OUT / "tour.json").write_text(json.dumps(frames, indent=2) + "\n")
    print("captured", [f["hash"] or "/" for f in frames])


if __name__ == "__main__":
    main()
