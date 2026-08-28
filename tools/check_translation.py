#!/usr/bin/env python3
"""Ellenőrzi, hogy a magyar fordítás megőrizte-e a forrás szerkezetét.

Használat:  python3 tools/check_translation.py [fajl.md ...]
Alapértelmezésben az összes src/*.md fájlt hasonlítja a megadott git
alapponthoz (BASE környezeti változó, alapértelmezés: angol-alap tag).
"""
import os, re, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE", "angol-alap")


def orig(path):
    rel = os.path.relpath(path, ROOT)
    return subprocess.run(["git", "-C", ROOT, "show", f"{BASE}:{rel}"],
                          capture_output=True, text=True).stdout


def strip_aquascope(text):
    """Kiveszi az Aquascope-blokkokat: ezek a fordításhoz képest kiegészítések."""
    out, keep, inb, fence = [], True, False, ""
    for line in text.split("\n"):
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m and not inb:
            inb, fence = True, m.group(1)
            keep = not line.strip().startswith(fence + "aquascope")
            if keep:
                out.append(line)
            continue
        if m and inb and line.strip().startswith(fence):
            inb = False
            if keep:
                out.append(line)
            keep = True
            continue
        if not inb or keep:
            out.append(line)
    return "\n".join(out)


def facts(text):
    f = {}
    f["fences"] = re.findall(r"^[ \t]*(`{3,}|~{3,})[ \t]*(.*)$", text, re.M)
    f["includes"] = re.findall(r"\{\{#\w+\s+([^}]*)\}\}", text)
    f["listing_num"] = re.findall(r'<Listing[^>]*?number="([^"]*)"', text)
    f["listing_file"] = re.findall(r'<Listing[^>]*?file-name="([^"]*)"', text)
    f["listing_count"] = [str(len(re.findall(r"<Listing", text))),
                          str(len(re.findall(r"</Listing>", text)))]
    f["linkdefs"] = re.findall(r"^\[([^\]]+)\]:\s*(\S+)", text, re.M)
    f["urls"] = re.findall(r"\]\((\S+?)\)", text)
    f["anchors"] = re.findall(r"\{#([A-Za-z0-9\-_]+)\}", text)
    f["headinglevels"] = re.findall(r"^(?:>\s*)?(#{1,6})\s", text, re.M)
    f["img"] = re.findall(r'src="([^"]*)"', text)
    # kódblokkok tartalma
    blocks, cur, inb, fence = [], [], False, ""
    for line in text.split("\n"):
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m and not inb:
            inb, fence, cur = True, m.group(1), []
        elif m and inb and line.strip().startswith(fence):
            inb = False
            blocks.append("\n".join(cur))
        elif inb:
            cur.append(line)
    f["code"] = blocks
    return f


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "src", "*.md")))
    problems = 0
    for path in files:
        path = os.path.abspath(path)
        o, n = orig(path), open(path, encoding="utf-8").read()
        if not o:
            print(f"?? {os.path.basename(path)}: nincs alapverzió")
            continue
        fo, fn = facts(o), facts(strip_aquascope(n))
        # Ezek soha nem változhatnak; a többinél a kiegészítés megengedett.
        STRICT = {"fences", "includes", "listing_num", "listing_file",
                  "listing_count", "code"}
        for key in fo:
            if key in STRICT:
                differs = fo[key] != fn[key]
            else:
                rest = list(fn[key])
                differs = False
                for item in fo[key]:
                    if item in rest:
                        rest.remove(item)
                    else:
                        differs = True
            if differs:
                problems += 1
                print(f"!! {os.path.basename(path)}: eltérés a(z) '{key}' elemben")
                so, sn = fo[key], fn[key]
                if isinstance(so, list) and len(so) == len(sn):
                    for a, b in zip(so, sn):
                        if a != b:
                            print(f"   - eredeti : {str(a)[:160]!r}")
                            print(f"   - fordítás: {str(b)[:160]!r}")
                else:
                    print(f"   - eredeti  darabszám: {len(so)}, fordítás: {len(sn)}")
                    for a in so:
                        if a not in sn:
                            print(f"   - hiányzik: {str(a)[:160]!r}")
                    for b in sn:
                        if b not in so:
                            print(f"   - többlet : {str(b)[:160]!r}")
    print(f"\n{len(files)} fájl ellenőrizve, {problems} eltérés.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
