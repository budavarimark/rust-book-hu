#!/usr/bin/env python3
"""Megkeresi a maradék angol prózasorokat a lefordított könyvben.

A kódblokkokat, include-okat, link-definíciókat és HTML-kommenteket kihagyja,
majd angol funkciószavak alapján jelzi a gyanús sorokat.
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = r"\b(the|and|of|to|that|with|this|you|your|we|our|for|from|which|when|there|their|have|has|will|would|can|because|about|into|these|those|what|how|it's|don't)\b"


def prose_lines(text):
    out, inb, fence, incomment = [], False, "", False
    for i, line in enumerate(text.split("\n"), 1):
        if incomment:
            if "-->" in line:
                incomment = False
            continue
        if "<!--" in line and "-->" not in line:
            incomment = True
            continue
        m = re.match(r"^[ \t]*(`{3,}|~{3,})", line)
        if m:
            if not inb:
                inb, fence = True, m.group(1)
            elif line.strip().startswith(fence):
                inb = False
            continue
        if inb:
            continue
        s = line.strip()
        if not s or s.startswith("<!--") or s.startswith("{{#"):
            continue
        if re.match(r"^\[[^\]]+\]:\s*\S+$", s):
            continue
        if re.match(r"^</?(Listing|figure|figcaption|img|a|span|Output)", s):
            continue
        out.append((i, line))
    return out


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "src", "*.md")))
    total = 0
    for f in files:
        text = open(f, encoding="utf-8").read()
        hits = []
        for ln, line in prose_lines(text):
            stripped = re.sub(r"`[^`]*`", "", line)
            stripped = re.sub(r"\[[^\]]*\]\([^)]*\)", "", stripped)
            stripped = re.sub(r"\{#[A-Za-z0-9\-_]+\}", "", stripped)
            stripped = re.sub(r"\]\[[A-Za-z0-9\-_]+\]", "]", stripped)
            stripped = re.sub(r"https?://\S+", "", stripped)
            stripped = re.sub(r"[\w./-]+\.(md|rs|toml|txt|html)\b", "", stripped)
            if len(re.findall(STOP, stripped, re.I)) >= 2:
                hits.append((ln, line.strip()[:110]))
        if hits:
            total += len(hits)
            print(f"\n== {os.path.basename(f)}: {len(hits)} gyanús sor")
            for ln, s in hits[:6]:
                print(f"   {ln}: {s}")
            if len(hits) > 6:
                print(f"   … még {len(hits)-6} sor")
    print(f"\nÖsszesen {total} gyanús angol prózasor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
