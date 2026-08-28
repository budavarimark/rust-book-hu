## D függelék: Hasznos fejlesztői eszközök

Ebben a függelékben néhány hasznos fejlesztői eszközről beszélünk, amelyeket a
Rust projekt biztosít. Szó lesz az automatikus formázásról, a figyelmeztetések
javításának gyors módjairól, egy linterről és az IDE-kkel való integrációról.

### Automatikus formázás a `rustfmt` segítségével

A `rustfmt` eszköz a közösségi kódstílusnak megfelelően formázza újra a kódodat.
Sok együttműködésen alapuló projekt használja a `rustfmt`-et, hogy elkerülje a
vitákat arról, milyen stílust használjanak Rust írásakor: mindenki ezzel az
eszközzel formázza a kódját.

A Rust telepítései alapértelmezetten tartalmazzák a `rustfmt`-et, így a
`rustfmt` és a `cargo-fmt` program valószínűleg már megvan a rendszereden. Ez a
két parancs úgy viszonyul egymáshoz, mint a `rustc` és a `cargo`: a `rustfmt`
finomabb vezérlést tesz lehetővé, a `cargo-fmt` pedig ismeri egy Cargót használó
projekt konvencióit. Bármely Cargo-projekt formázásához írd be a következőt:

```console
$ cargo fmt
```

Ennek a parancsnak a futtatása újraformázza az aktuális crate összes Rust
kódját. Ez csak a kód stílusát változtathatja meg, a kód szemantikáját nem. A
`rustfmt`-ről bővebben [a dokumentációjában][rustfmt] olvashatsz.

### Javítsd a kódodat a `rustfix` segítségével

A `rustfix` eszköz a Rust telepítéseinek része, és automatikusan ki tudja
javítani azokat a fordítói figyelmeztetéseket, amelyeknél egyértelmű módja van a
probléma orvoslásának, és az valószínűleg meg is felel a szándékodnak.
Valószínűleg találkoztál már fordítói figyelmeztetésekkel. Vegyük például ezt a
kódot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Itt az `x` változót módosíthatóként definiáljuk, de valójában soha nem
módosítjuk. A Rust figyelmeztet erre:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

A figyelmeztetés azt javasolja, hogy távolítsuk el a `mut` kulcsszót. Ezt a
javaslatot automatikusan alkalmazhatjuk a `rustfix` eszközzel, ha lefuttatjuk a
`cargo fix` parancsot:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Ha újra megnézzük a _src/main.rs_ fájlt, látni fogjuk, hogy a `cargo fix`
megváltoztatta a kódot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Az `x` változó immár nem módosítható, és a figyelmeztetés sem jelenik meg többé.

A `cargo fix` paranccsal a kódodat különböző Rust editionök között is
átültetheted. Az editionökről az [E függelékben][editions]<!-- ignore --> esik
szó.

### További lintek a Clippyvel

A Clippy eszköz lintek gyűjteménye, amely elemzi a kódodat, hogy elkaphasd a
gyakori hibákat, és javíthasd a Rust kódodat. A Clippy a szokásos Rust
telepítések része.

A Clippy lintjeinek futtatásához bármely Cargo-projekten írd be a következőt:

```console
$ cargo clippy
```

Tegyük fel például, hogy olyan programot írsz, amely egy matematikai konstans,
mondjuk a pi közelítését használja, mint ez a program:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

A `cargo clippy` futtatása ezen a projekten a következő hibát eredményezi:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Ez a hiba tudatja veled, hogy a Rustban már van egy pontosabb `PI` konstans
definiálva, és a programod helyesebb lenne, ha inkább azt a konstanst
használnád. Ezután módosítanád a kódodat, hogy a `PI` konstanst használja.

Az alábbi kód nem eredményez semmilyen hibát vagy figyelmeztetést a Clippytől:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

A Clippyről bővebben [a dokumentációjában][clippy] olvashatsz.

### IDE-integráció a `rust-analyzer` használatával

Az IDE-integrációhoz a Rust közösség a
[`rust-analyzer`][rust-analyzer]<!-- ignore --> használatát ajánlja. Ez az
eszköz fordítóközpontú segédprogramok együttese, amelyek a [Language Server
Protocol][lsp]<!-- ignore --> nyelvet beszélik; ez egy specifikáció arra, hogy
az IDE-k és a programozási nyelvek hogyan kommunikáljanak egymással. Különféle
kliensek használhatják a `rust-analyzer`-t, például [a Visual Studio Code Rust
analyzer bővítménye][vscode].

A telepítési útmutatóért látogass el a `rust-analyzer` projekt
[kezdőlapjára][rust-analyzer]<!-- ignore -->, majd telepítsd a nyelvi szerver
támogatását a saját IDE-dben. Az IDE-d így olyan képességekkel bővül, mint az
automatikus kiegészítés, a definícióra ugrás és a beágyazott hibajelzések.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
