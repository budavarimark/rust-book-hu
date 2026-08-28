<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Binárisok telepítése a `cargo install` paranccsal

A `cargo install` paranccsal binary crate-eket telepíthetsz és használhatsz
helyben. Ez nem a rendszer csomagkezelőjét hivatott kiváltani; kényelmes módot
ad a Rust-fejlesztőknek arra, hogy telepítsék azokat az eszközöket, amelyeket
mások megosztottak a [crates.io](https://crates.io/)<!-- ignore --> oldalon. Ne
feledd, hogy csak olyan csomagokat tudsz telepíteni, amelyeknek van bináris
targetjük. A _bináris target_ az a futtatható program, amely akkor jön létre, ha
a crate rendelkezik _src/main.rs_ fájllal vagy egy másik, binárisként megadott
fájllal – szemben a library targettel, amely önmagában nem futtatható, viszont
alkalmas arra, hogy más programokba beépítsd. A crate-ek README fájlja általában
tartalmaz információt arról, hogy az adott crate könyvtár-e, van-e bináris
targetje, vagy mindkettő igaz rá.

A `cargo install` paranccsal telepített összes bináris a telepítési gyökér _bin_
mappájába kerül. Ha a Rustot a _rustup.rs_ segítségével telepítetted, és nincs
egyedi beállításod, akkor ez a könyvtár a *$HOME/.cargo/bin* lesz. Gondoskodj
róla, hogy ez a könyvtár szerepeljen a `$PATH` változóban, hogy futtatni tudd a
`cargo install` paranccsal telepített programokat.

Például a 12. fejezetben említettük, hogy létezik a `grep` eszköznek egy Rust
implementációja, a `ripgrep`, fájlokban való kereséshez. A `ripgrep`
telepítéséhez a következőt futtathatjuk:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

A kimenet utolsó előtti sora mutatja a telepített bináris helyét és nevét, ami a
`ripgrep` esetében `rg`. Amíg a telepítési könyvtár szerepel a `$PATH`
változóban – ahogy korábban említettük –, addig futtathatod az `rg --help`
parancsot, és elkezdheted használni ezt a gyorsabb, rustosabb eszközt fájlok
kereséséhez!
