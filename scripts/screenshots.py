"""Take the full-page screenshots in resources/screenshots/ and check the page while doing it.

For each width (375, 768, 1024, 1440) and theme (dark, light) it saves <theme>-<width>.png, plus the
1440x900 hero-<theme>.png images used by the README. It also reports console errors and horizontal
page scroll (spec §11, items 1 and 3), and exits 1 if it finds any.

Setup, once per environment:
    pip3 install -r requirements-dev.txt
    python3 -m playwright install chromium   # skip if Chromium is already installed for Playwright

Usage:
    python3 scripts/screenshots.py                  # all widths, both themes
    python3 scripts/screenshots.py --widths 375 1440 --out /tmp/shots

The script serves the repo itself on a free port, so server.py doesn't need to be running.
Set PLAYWRIGHT_CHROMIUM_EXECUTABLE to use a specific Chromium binary. If cdn.jsdelivr.net is blocked,
the CDN files are taken from the npm registry instead (same package, same version).
"""

import argparse
import functools
import io
import json
import mimetypes
import os
import re
import sys
import tarfile
import threading
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright isn't installed. Run `pip3 install -r requirements-dev.txt` and "
          "`python3 -m playwright install chromium`, then try again.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
WIDTHS = [375, 768, 1024, 1440]
THEMES = ["dark", "light"]
HERO_SIZE = {"width": 1440, "height": 900}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve_repo():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}/"


# Some networks block cdn.jsdelivr.net but allow the npm registry, which serves the same files.
JSDELIVR_NPM = re.compile(r"https://cdn\.jsdelivr\.net/npm/((?:@[^/]+/)?[^@/]+)@([^/]+)/?(.*)")
_tarballs = {}


def from_npm(package, version, path):
    """Return (file name, bytes) for a jsdelivr /npm/ URL, read from the package's npm tarball."""
    key = (package, version)
    if key not in _tarballs:
        name = package.split("/")[-1]
        url = f"https://registry.npmjs.org/{package}/-/{name}-{version}.tgz"
        with urllib.request.urlopen(url, timeout=60) as response:
            _tarballs[key] = tarfile.open(fileobj=io.BytesIO(response.read()), mode="r:gz")
    tar = _tarballs[key]
    if not path:  # a bare package URL serves the package's default file, as jsdelivr does
        manifest = json.load(tar.extractfile("package/package.json"))
        path = manifest.get("jsdelivr") or manifest.get("browser") or manifest.get("main") or "index.js"
    path = path.removeprefix("./")
    return path, tar.extractfile(f"package/{path}").read()


def cdn_route(route):
    try:
        response = route.fetch()
        if response.ok:
            route.fulfill(response=response)
            return
    except Exception:
        pass
    match = JSDELIVR_NPM.match(route.request.url)
    if not match:
        route.abort()
        return
    path, body = from_npm(*match.groups())
    route.fulfill(status=200, body=body, content_type=mimetypes.guess_type(path)[0] or "text/plain")


def open_page(browser, url, theme, viewport, errors):
    context = browser.new_context(viewport=viewport)
    # The page reads the saved theme before first paint (spec §9).
    context.add_init_script(f"try {{ localStorage.setItem('theme', '{theme}') }} catch (e) {{}}")
    page = context.new_page()
    page.route("**/favicon.ico", lambda route: route.fulfill(status=204))  # the page has no favicon
    page.route("https://cdn.jsdelivr.net/**", cdn_route)
    page.on("console", lambda msg: msg.type == "error" and errors.append(msg.text))
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(url, wait_until="networkidle")
    return context, page


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--widths", type=int, nargs="+", default=WIDTHS)
    parser.add_argument("--out", type=Path, default=ROOT / "resources" / "screenshots")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    server, url = serve_repo()
    problems = []
    with sync_playwright() as p:
        # Chromium ignores the proxy environment variables, so pass the proxy on (the CDN needs it).
        proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        proxy = {"server": proxy_url, "bypass": "127.0.0.1,localhost"} if proxy_url else None
        try:
            browser = p.chromium.launch(executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"), proxy=proxy)
        except Exception as exc:
            print(f"Couldn't start Chromium: {str(exc).splitlines()[0]}\n"
                  "Run `python3 -m playwright install chromium`, or set PLAYWRIGHT_CHROMIUM_EXECUTABLE.")
            return 1
        for theme in THEMES:
            for width in args.widths:
                errors = []
                context, page = open_page(browser, url, theme, {"width": width, "height": 900}, errors)
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                page.screenshot(path=args.out / f"{theme}-{width}.png", full_page=True)
                context.close()
                status = "ok"
                if errors:
                    problems.append(f"{theme} {width}px: console errors: {errors}")
                    status = "console errors"
                if overflow > 0:
                    problems.append(f"{theme} {width}px: horizontal scroll ({overflow}px too wide)")
                    status = "horizontal scroll"
                print(f"{theme:5} {width:>4}px  {status}")
            context, page = open_page(browser, url, theme, HERO_SIZE, [])
            page.screenshot(path=args.out / f"hero-{theme}.png")
            context.close()
        browser.close()
    server.shutdown()

    for problem in problems:
        print(f"FAIL  {problem}")
    print(f"Saved to {args.out}" + ("" if not problems else f"; {len(problems)} problem(s)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
