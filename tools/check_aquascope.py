#!/usr/bin/env python3
"""Ellenőrzi a megadott markdown fájlok ```aquascope blokkjait.

Minden blokkot egy eldobható mdbook-projektbe másol, lefordítja, és jelzi, ha
az Aquascope nem tudta elemezni. Így egy fejezeten dolgozva sem kell az egész
könyvet újrafordítani.

Használat:
    python3 tools/check_aquascope.py src/ch04-02-references-and-borrowing.md
    python3 tools/check_aquascope.py            # az összes src/*.md

Környezet: a szkript magától megkeresi a bin/ könyvtárat és a nightly
toolchaint (lásd ci/aquascope-setup.sh).
"""
import html, json, os, re, sys, glob, shutil, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLCHAIN = os.environ.get("AQUASCOPE_TOOLCHAIN", "nightly-2026-05-01")


def env():
    e = dict(os.environ)
    bins = [os.path.join(ROOT, "bin")]
    extra = os.environ.get("AQUASCOPE_BIN_DIR")
    if extra:
        bins.insert(0, extra)
    e["PATH"] = os.pathsep.join(bins + [e.get("PATH", "")])
    if "LD_LIBRARY_PATH" not in e:
        out = subprocess.run(["rustc", f"+{TOOLCHAIN}", "--print", "target-libdir"],
                             capture_output=True, text=True)
        if out.returncode == 0:
            e["LD_LIBRARY_PATH"] = out.stdout.strip()
    return e


def blocks(path):
    """(kezdősor, teljes blokkszöveg) párok."""
    lines = open(path, encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("```aquascope"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append((i + 1, "\n".join(lines[i:j + 1])))
            i = j + 1
        else:
            i += 1
    return out


def build(chapters, workdir):
    src = os.path.join(workdir, "src")
    os.makedirs(src, exist_ok=True)
    with open(os.path.join(workdir, "book.toml"), "w") as f:
        f.write('[book]\ntitle = "ellenorzes"\n\n[preprocessor.aquascope]\n')
    summary = ["# Summary\n"]
    for n, (_, text) in enumerate(chapters):
        name = f"b{n}.md"
        open(os.path.join(src, name), "w", encoding="utf-8").write(f"# {n}\n\n{text}\n")
        summary.append(f"- [{n}]({name})")
    open(os.path.join(src, "SUMMARY.md"), "w", encoding="utf-8").write("\n".join(summary) + "\n")
    r = subprocess.run(["mdbook", "build"], cwd=workdir, env=env(),
                       capture_output=True, text=True)
    log = (r.stderr or "") + (r.stdout or "")
    if r.returncode != 0 or "ERROR" in r.stderr:
        return False, log
    # Az Aquascope némán üres elemzést is adhat (pl. rosszul escape-elt
    # `#[derive(...)]` esetén); ilyenkor az ábra üresen jelenne meg.
    for n in range(len(chapters)):
        page = os.path.join(workdir, "book", f"b{n}.html")
        if not os.path.exists(page):
            return False, log + f"\nHiányzó kimenet: b{n}.html"
        text = open(page, encoding="utf-8").read()
        found = re.findall(r'data-responses="([^"]*)"', text)
        if not found:
            return False, log + f"\nA(z) {n}. blokkhoz nem készült ábra."
        for raw in found:
            try:
                data = json.loads(html.unescape(raw))
            except ValueError:
                return False, log + f"\nA(z) {n}. blokk elemzése olvashatatlan."
            if not data or any(not v for v in data.values()):
                return False, log + (
                    f"\nA(z) {n}. blokk elemzése üres: {json.dumps(data)[:120]}. "
                    "Gyakori ok: a `#[derive(...)]` sort `##[derive(...)]` "
                    "alakban kell írni, különben rejtett sorként csonkul.")
    return True, log


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "src", "*.md")))
    if not shutil.which("mdbook", path=env()["PATH"]):
        print("Nem találom az mdbook binárist. Futtasd: ./ci/aquascope-setup.sh")
        return 2
    problems = 0
    for path in files:
        bs = blocks(path)
        if not bs:
            continue
        with tempfile.TemporaryDirectory() as d:
            ok, log = build(bs, d)
        if ok:
            print(f"ok  {os.path.basename(path)}: {len(bs)} blokk rendben")
            continue
        # hibás blokk megkeresése egyenként
        print(f"!!  {os.path.basename(path)}: hibás blokk(ok)")
        for line, text in bs:
            with tempfile.TemporaryDirectory() as d:
                ok1, log1 = build([(line, text)], d)
            if not ok1:
                problems += 1
                print(f"    {os.path.basename(path)}:{line} nem elemezhető")
                for l in [x for x in log1.split("\n") if "error" in x.lower()][:4]:
                    print("      " + l.strip()[:160])
    print(f"\n{problems} hibás blokk.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
