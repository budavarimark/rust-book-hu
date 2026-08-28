## A build testreszabása release profilokkal

Rustban a _release profilok_ előre definiált, testreszabható profilok
különböző konfigurációkkal, amelyek nagyobb kontrollt adnak a programozónak a
kód fordításának különféle beállításai fölött. Minden profil a többitől
függetlenül konfigurálható.

A Cargónak két fő profilja van: a `dev` profil, amelyet a `cargo build`
futtatásakor használ, és a `release` profil, amelyet a `cargo build --release`
futtatásakor. A `dev` profil a fejlesztéshez való jó alapértelmezésekkel van
definiálva, a `release` profilnak pedig a release buildekhez való jó
alapértelmezései vannak.

Ezek a profilnevek ismerősek lehetnek a buildjeid kimenetéből:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

A `dev` és a `release` ezek a különböző profilok, amelyeket a fordító használ.

A Cargónak minden profilhoz vannak alapértelmezett beállításai, amelyek akkor
érvényesülnek, ha nem adtál hozzá kifejezetten `[profile.*]` szakaszokat a
projekt _Cargo.toml_ fájljához. Ha bármelyik testreszabni kívánt profilhoz
hozzáadsz egy `[profile.*]` szakaszt, felülírhatod az alapértelmezett
beállítások tetszőleges részhalmazát. Például itt vannak az `opt-level`
beállítás alapértelmezett értékei a `dev` és a `release` profilhoz:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Az `opt-level` beállítás azt szabályozza, hány optimalizációt alkalmaz a Rust a
kódodra; az értéke 0-tól 3-ig terjedhet. A több optimalizáció alkalmazása
megnyújtja a fordítási időt, ezért ha fejlesztés közben gyakran fordítod a
kódodat, kevesebb optimalizációt szeretnél, hogy gyorsabban forduljon, még ha
az eredményül kapott kód lassabban fut is. A `dev` profil alapértelmezett
`opt-level` értéke ezért `0`. Amikor készen állsz a kódod kiadására, jobban
megéri több időt tölteni a fordítással. Release módban csak egyszer fordítasz,
a lefordított programot viszont sokszor futtatod, így a release mód a hosszabb
fordítási időt cseréli el gyorsabban futó kódra. Ezért a `release` profil
alapértelmezett `opt-level` értéke `3`.

Egy alapértelmezett beállítást úgy írhatsz felül, hogy másik értéket adsz meg
hozzá a _Cargo.toml_ fájlban. Ha például az 1-es optimalizációs szintet
szeretnénk használni a fejlesztői profilban, ezt a két sort adhatjuk hozzá a
projektünk _Cargo.toml_ fájljához:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Ez a kód felülírja a `0` alapértelmezett beállítást. Mostantól, amikor
lefuttatjuk a `cargo build` parancsot, a Cargo a `dev` profil alapértelmezéseit
használja, kiegészítve az `opt-level` testreszabásunkkal. Mivel az `opt-level`
értékét `1`-re állítottuk, a Cargo több optimalizációt alkalmaz az
alapértelmezettnél, de nem annyit, mint egy release buildben.

A konfigurációs beállítások és az egyes profilok alapértelmezéseinek teljes
listájáért lásd
[a Cargo dokumentációját](https://doc.rust-lang.org/cargo/reference/profiles.html).
