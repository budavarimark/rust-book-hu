## Hello, Cargo!

A Cargo a Rust build rendszere és csomagkezelője. A legtöbb rustacean ezzel az
eszközzel kezeli a Rust-projektjeit, mert a Cargo rengeteg feladatot elvégez
helyetted: lefordítja a kódodat, letölti azokat a könyvtárakat, amelyektől a
kódod függ, és lefordítja ezeket a könyvtárakat is. (A kódod által igényelt
könyvtárakat _függőségeknek_ nevezzük.)

A legegyszerűbb Rust-programoknak – amilyet eddig írtunk – nincsenek
függőségeik. Ha a „Hello, world!” projektet a Cargóval építettük volna fel,
akkor csak a Cargo azon részét használtuk volna, amely a kód fordításáért
felel. Ahogy egyre összetettebb Rust-programokat írsz, függőségeket adsz majd
hozzájuk, és ha a projektet a Cargóval kezded, a függőségek hozzáadása sokkal
könnyebb lesz.

Mivel a Rust-projektek túlnyomó többsége a Cargót használja, a könyv további
része feltételezi, hogy te is a Cargót használod. A Cargo a Rusttal együtt
települ, ha a [„Telepítés”][installation]<!-- ignore --> szakaszban tárgyalt
hivatalos telepítőket használtad. Ha valamilyen más módon telepítetted a
Rustot, a következő parancs terminálba írásával ellenőrizheted, hogy telepítve
van-e a Cargo:

```console
$ cargo --version
```

Ha verziószámot látsz, akkor megvan! Ha hibát látsz, például azt, hogy `command
not found`, nézd meg a telepítési módod dokumentációját, hogy kiderüljön,
hogyan telepítheted külön a Cargót.

### Projekt létrehozása a Cargóval

Hozzunk létre egy új projektet a Cargóval, és nézzük meg, miben tér el az
eredeti „Hello, world!” projektünktől. Navigálj vissza a _projects_
könyvtáradba (vagy oda, ahol a kódodat tárolni szoktad). Ezután bármelyik
operációs rendszeren futtasd a következőt:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Az első parancs létrehoz egy új, _hello_cargo_ nevű könyvtárat és projektet. A
projektünket _hello_cargo_-nak neveztük el, és a Cargo egy ugyanilyen nevű
könyvtárban hozza létre a fájljait.

Lépj be a _hello_cargo_ könyvtárba, és listázd ki a fájlokat. Látni fogod, hogy
a Cargo két fájlt és egy könyvtárat generált nekünk: egy _Cargo.toml_ fájlt és
egy _src_ könyvtárat, benne egy _main.rs_ fájllal.

Ezenkívül inicializált egy új Git-repót is egy _.gitignore_ fájllal együtt. A
Git-fájlok nem jönnek létre, ha a `cargo new` parancsot egy már meglévő
Git-repón belül futtatod; ezt a viselkedést a `cargo new --vcs=git` paranccsal
írhatod felül.

> Megjegyzés: A Git egy elterjedt verziókezelő rendszer. A `--vcs` kapcsolóval
> elérheted, hogy a `cargo new` másik verziókezelő rendszert vagy éppen
> semmilyet se használjon. Futtasd a `cargo new --help` parancsot az elérhető
> lehetőségek megtekintéséhez.

Nyisd meg a _Cargo.toml_ fájlt a választott szövegszerkesztődben. Nagyjából az
1-2. listában szereplő kódhoz hasonlóan kell kinéznie.

<Listing number="1-2" file-name="Cargo.toml" caption="A `cargo new` által generált *Cargo.toml* tartalma">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Ez a fájl [_TOML_][toml]<!-- ignore --> (_Tom's Obvious, Minimal Language_)
formátumú, ez a Cargo konfigurációs formátuma.

Az első sor, a `[package]`, szakaszcímsor, amely azt jelzi, hogy az utána
következő utasítások egy csomagot konfigurálnak. Ahogy több információt adunk
hozzá ehhez a fájlhoz, további szakaszokat is felveszünk majd.

A következő három sor azokat a konfigurációs adatokat állítja be, amelyekre a
Cargónak a programod lefordításához szüksége van: a nevet, a verziót és a
használandó Rust editiont. Az `edition` kulcsról az [E függelékben][appendix-e]<!-- ignore --> lesz szó.

Az utolsó sor, a `[dependencies]`, egy olyan szakasz kezdete, amelyben a
projekted függőségeit sorolhatod fel. A Rustban a kódcsomagokat _crate_-eknek
nevezzük. Ehhez a projekthez nem lesz szükségünk további crate-ekre, de a 2.
fejezet első projektjéhez igen, így ott majd használjuk ezt a függőségi
szakaszt.

Most nyisd meg a _src/main.rs_ fájlt, és nézd meg:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

A Cargo egy „Hello, world!” programot generált neked, pontosan olyat, amilyet
az 1-1. listában írtunk! Eddig annyi a különbség a mi projektünk és a Cargo
által generált projekt között, hogy a Cargo az _src_ könyvtárba tette a kódot,
és a legfelső szintű könyvtárban van egy _Cargo.toml_ konfigurációs fájlunk.

A Cargo azt várja, hogy a forrásfájljaid az _src_ könyvtárban legyenek. A
legfelső szintű projektkönyvtár csak a README fájloknak, a licencinformációknak,
a konfigurációs fájloknak és minden másnak való, ami nem kapcsolódik a kódodhoz.
A Cargo használata segít rendszerezni a projektjeidet. Mindennek megvan a helye,
és minden a helyén van.

Ha olyan projektet kezdtél el, amely nem használja a Cargót – ahogy a „Hello,
world!” projektnél tettük –, átalakíthatod olyanná, amely használja. Helyezd át
a projekt kódját az _src_ könyvtárba, és hozz létre egy megfelelő _Cargo.toml_
fájlt. A _Cargo.toml_ fájlhoz egyszerűen hozzájuthatsz a `cargo init` parancs
futtatásával, amely automatikusan létrehozza neked.

### Cargo-projekt fordítása és futtatása

Most nézzük meg, mi változik, ha a „Hello, world!” programot a Cargóval
fordítjuk le és futtatjuk! A _hello_cargo_ könyvtáradból a következő parancs
kiadásával fordíthatod le a projektedet:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Ez a parancs a jelenlegi könyvtárad helyett a _target/debug/hello_cargo_
(Windowson a _target\debug\hello_cargo.exe_) útvonalon hoz létre futtatható
állományt. Mivel az alapértelmezett build a debug build, a Cargo a bináris
állományt egy _debug_ nevű könyvtárba teszi. A futtatható állományt ezzel a
paranccsal futtathatod:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Ha minden jól megy, a `Hello, world!` szövegnek kell megjelennie a terminálban.
A `cargo build` első futtatásakor a Cargo egy új fájlt is létrehoz a legfelső
szinten: a _Cargo.lock_ fájlt. Ez a fájl tartja nyilván a projekted
függőségeinek pontos verzióit. Ennek a projektnek nincsenek függőségei, így a
fájl kicsit üresen tátong. Ezt a fájlt sosem kell kézzel módosítanod; a Cargo
kezeli helyetted a tartalmát.

Az imént lefordítottuk a projektet a `cargo build` paranccsal, és futtattuk a
`./target/debug/hello_cargo` paranccsal, de a `cargo run` paranccsal egyetlen
lépésben le is fordíthatjuk a kódot, és futtathatjuk is az elkészült futtatható
állományt:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

A `cargo run` kényelmesebb, mint megjegyezni, hogy le kell futtatni a `cargo
build` parancsot, majd beírni a bináris állomány teljes útvonalát, ezért a
legtöbb fejlesztő a `cargo run` parancsot használja.

Vedd észre, hogy ezúttal nem láttunk olyan kimenetet, amely azt jelezte volna,
hogy a Cargo lefordítja a `hello_cargo`-t. A Cargo rájött, hogy a fájlok nem
változtak, ezért nem fordított újra, csak lefuttatta a bináris állományt. Ha
módosítottad volna a forráskódodat, a Cargo futtatás előtt újrafordította volna
a projektet, és ezt a kimenetet láttad volna:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

A Cargo egy `cargo check` nevű parancsot is kínál. Ez a parancs gyorsan
ellenőrzi a kódodat, hogy meggyőződjön róla: lefordul, de nem állít elő
futtatható állományt:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Miért is ne szeretnél futtatható állományt? A `cargo check` gyakran sokkal
gyorsabb, mint a `cargo build`, mert kihagyja a futtatható állomány
előállításának lépését. Ha kódírás közben folyamatosan ellenőrzöd a munkádat, a
`cargo check` felgyorsítja azt a folyamatot, amelynek során megtudod, hogy a
projekted még mindig lefordul-e! Ezért sok rustacean rendszeresen futtatja a
`cargo check` parancsot programírás közben, hogy megbizonyosodjon róla: a
program lefordul. A `cargo build` parancsot pedig akkor futtatják, amikor már
használni akarják a futtatható állományt.

Foglaljuk össze, mit tanultunk eddig a Cargóról:

- A `cargo new` paranccsal projektet hozhatunk létre.
- A `cargo build` paranccsal lefordíthatunk egy projektet.
- A `cargo run` paranccsal egy lépésben lefordíthatunk és futtathatunk egy
  projektet.
- A `cargo check` paranccsal úgy fordíthatunk le egy projektet a hibák
  ellenőrzésére, hogy közben nem készül bináris állomány.
- A Cargo a build eredményét nem a kódunkkal azonos könyvtárba menti, hanem a
  _target/debug_ könyvtárban tárolja.

A Cargo használatának további előnye, hogy a parancsok ugyanazok, függetlenül
attól, melyik operációs rendszeren dolgozol. Ezért ettől a ponttól kezdve már
nem adunk külön utasításokat Linuxra és macOS-re, illetve Windowsra.

### Fordítás release-re

Amikor a projekted végre készen áll a kiadásra, a `cargo build --release`
paranccsal optimalizálásokkal fordíthatod le. Ez a parancs a _target/debug_
helyett a _target/release_ könyvtárban hoz létre futtatható állományt. Az
optimalizálásoktól a Rust-kódod gyorsabban fut, de a bekapcsolásuk
meghosszabbítja a program fordításának idejét. Ezért van két különböző profil:
az egyik a fejlesztéshez, amikor gyorsan és gyakran akarsz újrafordítani, a
másik pedig annak a végleges programnak az elkészítéséhez, amelyet a
felhasználónak adsz, amelyet nem fordítasz újra meg újra, és amelynek a lehető
leggyorsabban kell futnia. Ha a kódod futási idejét méred, mindenképpen a
`cargo build --release` parancsot futtasd, és a _target/release_ könyvtárban
lévő futtatható állománnyal mérj.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### A Cargo konvencióinak kihasználása

Egyszerű projekteknél a Cargo nem sokkal ad többet a puszta `rustc`
használatánál, de ahogy a programjaid összetettebbé válnak, bizonyítani fogja
az értékét. Amint egy program több fájlra nő, vagy függőségre van szüksége,
sokkal egyszerűbb a Cargóra bízni a build összehangolását.

Bár a `hello_cargo` projekt egyszerű, mostanra sok olyan valódi eszközt
használ, amelyet a Rust-pályafutásod további részében is használni fogsz.
Valójában bármely meglévő projekten a következő parancsokkal dolgozhatsz:
kicsekkolod a kódot Gittel, belépsz az adott projekt könyvtárába, és lefordítod:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

A Cargóról bővebben [a dokumentációjában][cargo] olvashatsz.

## Összefoglalás

Máris remekül elindultál a Rust-utadon! Ebben a fejezetben megtanultad, hogyan:

- Telepítsd a Rust legutóbbi stabil verzióját a `rustup` segítségével.
- Frissíts egy újabb Rust-verzióra.
- Nyisd meg a helyben telepített dokumentációt.
- Írj és futtass egy „Hello, world!” programot közvetlenül a `rustc`
  használatával.
- Hozz létre és futtass új projektet a Cargo konvencióival.

Ez remek alkalom arra, hogy egy tartalmasabb programot építs, és hozzászokj a
Rust-kód olvasásához és írásához. A 2. fejezetben ezért egy kitalálós játékot
készítünk. Ha inkább azzal kezdenéd, hogy megtanulod, hogyan működnek a gyakori
programozási fogalmak a Rustban, nézd meg a 3. fejezetet, és utána térj vissza
a 2. fejezethez.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
