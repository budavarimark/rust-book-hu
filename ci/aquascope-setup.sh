#!/bin/bash

# Telepíti az Aquascope-ábrákhoz szükséges eszközöket:
#  - az aquascope release binárisait (mdbook-aquascope, cargo-aquascope,
#    aquascope-driver) a $BIN_DIR könyvtárba,
#  - azt a nightly Rust toolchaint, amellyel az aquascope-driver készült.
#
# Használat:
#
#   ./ci/aquascope-setup.sh
#   export PATH="$PWD/bin:$PATH"
#   export LD_LIBRARY_PATH="$(rustc +nightly-2026-05-01 --print target-libdir)"
#   mdbook build
#
# A szkript a végén kiírja a beállítandó környezeti változókat.

set -eu

AQUASCOPE_VERSION="${AQUASCOPE_VERSION:-0.4.0}"
AQUASCOPE_TOOLCHAIN="${AQUASCOPE_TOOLCHAIN:-nightly-2026-05-01}"
BIN_DIR="${BIN_DIR:-$PWD/bin}"

mkdir -p "$BIN_DIR"

if [ ! -x "$BIN_DIR/mdbook-aquascope" ]; then
    echo "Aquascope $AQUASCOPE_VERSION letöltése ide: $BIN_DIR"
    curl -sSL "https://github.com/cognitive-engineering-lab/aquascope/releases/download/v${AQUASCOPE_VERSION}/aquascope-x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz --directory="$BIN_DIR"
fi

if ! rustup toolchain list | grep -q "^${AQUASCOPE_TOOLCHAIN}"; then
    echo "A(z) $AQUASCOPE_TOOLCHAIN toolchain telepítése"
    rustup toolchain install "$AQUASCOPE_TOOLCHAIN" \
        -c rust-src,rustc-dev,llvm-tools-preview,miri --profile minimal
    cargo "+$AQUASCOPE_TOOLCHAIN" miri setup
fi

target_libdir="$(rustc "+$AQUASCOPE_TOOLCHAIN" --print target-libdir)"

echo
echo "Kész. Állítsd be a következőket a könyv fordítása előtt:"
echo "  export PATH=\"$BIN_DIR:\$PATH\""
echo "  export LD_LIBRARY_PATH=\"$target_libdir\""
