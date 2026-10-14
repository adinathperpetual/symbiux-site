#!/usr/bin/env python3
"""Build a GitHub Pages copy of public/ that works under a sub-path.

Usage:  python3 build-pages.py /symbiux-site/  [out_dir]
        python3 build-pages.py /               (user/org site or custom domain)
"""
import os, re, shutil, sys

base = sys.argv[1] if len(sys.argv) > 1 else "/"
if not base.startswith("/"): base = "/" + base
if not base.endswith("/"): base += "/"
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "public")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "dist")

shutil.rmtree(out, ignore_errors=True)
shutil.copytree(src, out)

def patch(rel, fn):
    p = os.path.join(out, rel)
    s = open(p, encoding="utf-8").read()
    n = fn(s)
    open(p, "w", encoding="utf-8").write(n)
    return s != n

if base != "/":
    pref = base  # e.g. /symbiux-site/
    # absolute root asset paths -> prefixed paths (HTML attributes, JS strings, CSS urls)
    rx = re.compile(r'(["\'(])/(assets/|logo\.jpg|favicon\.png)')
    targets = ["index.html", "assets/fonts.css"] + [
        "assets/" + f for f in os.listdir(os.path.join(out, "assets")) if f.endswith((".js", ".css"))]
    for t in targets:
        patch(t, lambda s: rx.sub(lambda m: m.group(1) + pref + m.group(2), s))
    # TanStack Start sets the router basepath (build-time value "") during client hydration
    js = [f for f in os.listdir(os.path.join(out, "assets")) if f.endswith(".js")]
    hit = 0
    for f in js:
        hit += patch("assets/" + f, lambda s: s.replace(
            'n.update({basepath:"",', 'n.update({basepath:"%s",' % base.rstrip("/")))
    if not hit:
        sys.exit("router basepath hook not found - bundle changed?")
    # in-page "/" home link
    patch("index.html", lambda s: s.replace('href="/"', 'href="%s"' % base))

# GitHub Pages: serve files as-is, and fall back to the app for unknown URLs
open(os.path.join(out, ".nojekyll"), "w").close()
shutil.copy(os.path.join(out, "index.html"), os.path.join(out, "404.html"))
print("built", out, "for base", base)
