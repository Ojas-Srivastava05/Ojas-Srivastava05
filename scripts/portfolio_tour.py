#!/usr/bin/env python3
"""Capture a section-by-section tour of the portfolio for the README preview."""
import io
import json
import pathlib
import sys

from PIL import Image, ImageEnhance
from playwright.sync_api import sync_playwright

URL = "https://ojas-srivastava.vercel.app/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data"
VIEW = (1440, 900)
FRAME = (1440, 900)
WANTED = ["top", "brief", "experience", "projects", "achievements", "contact"]

HIDE_FLOATING = """
() => {
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    const isTopNav = r.top < 60 && r.width > 600;
    if (!isTopNav) el.style.setProperty('visibility', 'hidden', 'important');
  }
  for (const c of document.querySelectorAll('canvas')) {
    const r = c.getBoundingClientRect();
    if (r.width >= innerWidth * 0.9 && r.height >= innerHeight * 0.9) c.style.setProperty('opacity', '0.35', 'important');
  }
}
"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": VIEW[0], "height": VIEW[1]}, device_scale_factor=2,
                                  reduced_motion="reduce", color_scheme="dark")
        page = ctx.new_page()
        page.goto(URL, wait_until="load", timeout=90000)
        page.wait_for_timeout(6000)

        height = page.evaluate("document.documentElement.scrollHeight")
        for y in range(0, height, 300):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(180)
        page.wait_for_timeout(1500)

        ids = set(page.evaluate("[...document.querySelectorAll('[id]')].map(e => e.id)"))
        frames = []
        for sid in WANTED:
            if sid == "top":
                page.evaluate("window.scrollTo(0, 0)")
            elif sid in ids:
                page.evaluate(f"window.scrollTo(0, document.getElementById('{sid}').getBoundingClientRect().top + scrollY - 24)")
            else:
                continue
            page.wait_for_timeout(4200)
            page.evaluate(HIDE_FLOATING)
            page.wait_for_timeout(300)
            png = page.screenshot(type="png")
            img = Image.open(io.BytesIO(png)).convert("RGB").resize(FRAME, Image.LANCZOS)
            img = ImageEnhance.Brightness(img).enhance(1.12)
            img = ImageEnhance.Contrast(img).enhance(1.06)
            img = ImageEnhance.Sharpness(img).enhance(1.25)
            name = f"tour-{len(frames)}.jpg"
            img.save(OUT / name, "JPEG", quality=84, optimize=True, progressive=True, subsampling=0)
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
