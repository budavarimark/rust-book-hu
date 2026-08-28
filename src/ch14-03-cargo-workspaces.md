## Cargo workspace-ek

A 12. fejezetben olyan csomagot építettünk, amely egy binary crate-et és egy
library crate-et is tartalmazott. Ahogy a projekted fejlődik, előfordulhat, hogy
a library crate egyre nagyobbra nő, és a csomagot tovább szeretnéd bontani több
library crate-re. A Cargo _workspace_ néven kínál olyan képességet, amely segít
az együtt fejlesztett, egymáshoz kapcsolódó csomagok kezelésében.

### Workspace létrehozása

A _workspace_ olyan csomagok halmaza, amelyek ugyanazon a _Cargo.lock_ fájlon és
kimeneti könyvtáron osztoznak. Hozzunk létre egy projektet workspace
használatával – szándékosan egyszerű kódot írunk, hogy a workspace szerkezetére
tudjunk koncentrálni. Egy workspace-t többféleképpen is fel lehet építeni, ezért
csak egy elterjedt megoldást mutatunk be. A workspace-ünk egy binárist és két
könyvtárat fog tartalmazni. A bináris, amely a fő funkcionalitást nyújtja majd,
a két könyvtártól fog függeni. Az egyik könyvtár egy `add_one` függvényt, a
másik egy `add_two` függvényt biztosít. Ez a három crate ugyanannak a
workspace-nek lesz a része. Kezdjük azzal, hogy létrehozunk egy új könyvtárat a
workspace-nek:

```console
$ mkdir add
$ cd add
```

Ezután az _add_ könyvtárban létrehozzuk azt a _Cargo.toml_ fájlt, amely az egész
workspace-t konfigurálja. Ebben a fájlban nem lesz `[package]` szakasz. Helyette
egy `[workspace]` szakasszal kezdődik, amelyben tagokat adhatunk a
workspace-hez. Arra is ügyelünk, hogy a Cargo resolver algoritmusának legújabb,
legjobb változatát használjuk a workspace-ünkben, ezért a `resolver` értékét
`"3"`-ra állítjuk:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Ezután létrehozzuk az `adder` binary crate-et: futtassuk a `cargo new` parancsot
az _add_ könyvtárban:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Ha a `cargo new` parancsot egy workspace-en belül futtatod, az automatikusan
hozzáadja az újonnan létrehozott csomagot a workspace _Cargo.toml_ fájljában
lévő `[workspace]` definíció `members` kulcsához, így:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Ezen a ponton a `cargo build` futtatásával fel tudjuk építeni a workspace-t. Az
_add_ könyvtárban lévő fájloknak így kell kinézniük:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

A workspace-nek egyetlen _target_ könyvtára van a legfelső szinten, amelybe a
lefordított artifactok kerülnek; az `adder` csomagnak nincs saját _target_
könyvtára. Még ha az _adder_ könyvtárból futtatnánk is a `cargo build`
parancsot, a lefordított artifactok akkor is az _add/target_ könyvtárba
kerülnének, nem pedig az _add/adder/target_ könyvtárba. A Cargo azért így
alakítja ki a _target_ könyvtárat egy workspace-ben, mert a workspace crate-jei
szándékoltan egymástól függenek. Ha minden crate-nek saját _target_ könyvtára
volna, mindegyik crate-nek újra kellene fordítania a workspace összes többi
crate-jét, hogy az artifactok a saját _target_ könyvtárába kerüljenek. Egyetlen
_target_ könyvtáron osztozva a crate-ek elkerülhetik a fölösleges újraépítést.

### A workspace második csomagjának létrehozása

Ezután hozzunk létre egy másik tagcsomagot a workspace-ben, és nevezzük el
`add_one`-nak. Generáljunk egy `add_one` nevű új library crate-et:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

A legfelső szintű _Cargo.toml_ mostantól tartalmazza az _add_one_ útvonalat a
`members` listában:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Az _add_ könyvtáradban most már ezeknek a könyvtáraknak és fájloknak kell
lenniük:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Az _add_one/src/lib.rs_ fájlban vegyünk fel egy `add_one` függvényt:

<span class="filename">Fájlnév: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Most már elérhetjük, hogy a binárisunkat tartalmazó `adder` csomag függjön a
könyvtárunkat tartalmazó `add_one` csomagtól. Először fel kell vennünk egy
útvonal szerinti függőséget az `add_one`-ra az _adder/Cargo.toml_ fájlba.

<span class="filename">Fájlnév: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

A Cargo nem feltételezi, hogy egy workspace crate-jei függenek egymástól, ezért
nekünk kell kifejezetten megadnunk a függőségi viszonyokat.

Ezután használjuk az `add_one` függvényt (az `add_one` crate-ből) az `adder`
crate-ben. Nyisd meg az _adder/src/main.rs_ fájlt, és módosítsd a `main`
függvényt úgy, hogy meghívja az `add_one` függvényt, ahogy a 14-7. listában
látható.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Az `add_one` library crate használata az `adder` crate-ből">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Építsük fel a workspace-t: futtassuk a `cargo build` parancsot a legfelső szintű
_add_ könyvtárban!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Ahhoz, hogy a binary crate-et az _add_ könyvtárból futtassuk, a `cargo run`
parancsnál a `-p` argumentummal és a csomag nevével adhatjuk meg, a workspace
melyik csomagját szeretnénk futtatni:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Ez az _adder/src/main.rs_ fájlban lévő kódot futtatja, amely az `add_one`
crate-től függ.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Függés külső csomagtól

Figyeld meg, hogy a workspace-nek csak egyetlen _Cargo.lock_ fájlja van a
legfelső szinten, nem pedig minden crate könyvtárában külön-külön. Ez
biztosítja, hogy minden crate ugyanazt a verziót használja az összes
függőségből. Ha felvesszük a `rand` csomagot az _adder/Cargo.toml_ és az
_add_one/Cargo.toml_ fájlokba, a Cargo mindkettőt a `rand` egyetlen verziójára
oldja fel, és ezt rögzíti az egyetlen _Cargo.lock_ fájlban. Ha a workspace
minden crate-je ugyanazokat a függőségeket használja, akkor a crate-ek mindig
kompatibilisek lesznek egymással. Vegyük fel a `rand` crate-et az
_add_one/Cargo.toml_ fájl `[dependencies]` szakaszába, hogy használni tudjuk a
`rand` crate-et az `add_one` crate-ben:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Fájlnév: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Most már hozzáadhatjuk a `use rand;` sort az _add_one/src/lib.rs_ fájlhoz, és ha
az _add_ könyvtárban a `cargo build` futtatásával felépítjük az egész
workspace-t, az behúzza és lefordítja a `rand` crate-et. Kapni fogunk egy
figyelmeztetést, mert nem hivatkozunk arra a `rand`-ra, amelyet behoztunk a
hatókörbe:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

A legfelső szintű _Cargo.lock_ mostantól tartalmazza az `add_one` `rand`-tól
való függésének adatait. Ugyanakkor hiába használjuk a `rand`-ot valahol a
workspace-ben, a workspace többi crate-jében nem használhatjuk mindaddig, amíg a
`rand`-ot fel nem vesszük az ő _Cargo.toml_ fájljaikba is. Ha például az `adder`
csomag _adder/src/main.rs_ fájljához hozzáadjuk a `use rand;` sort, hibát
kapunk:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Ennek javításához szerkeszd az `adder` csomag _Cargo.toml_ fájlját, és jelezd,
hogy a `rand` az ő függősége is. Az `adder` csomag felépítése felveszi a
`rand`-ot az `adder` függőségeinek listájára a _Cargo.lock_ fájlban, de a `rand`
további másolatait nem tölti le. A Cargo gondoskodik arról, hogy a workspace
minden csomagjának minden olyan crate-je, amely a `rand` csomagot használja,
ugyanazt a verziót használja – amennyiben kompatibilis `rand`-verziókat adnak
meg –, így helyet takarít meg, és biztosítja, hogy a workspace crate-jei
kompatibilisek legyenek egymással.

Ha a workspace crate-jei ugyanannak a függőségnek nem kompatibilis verzióit
adják meg, a Cargo mindegyiket feloldja, de akkor is igyekszik a lehető
legkevesebb verziót feloldani.

### Teszt hozzáadása egy workspace-hez

További fejlesztésként vegyünk fel egy tesztet az `add_one::add_one` függvényhez
az `add_one` crate-en belül:

<span class="filename">Fájlnév: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Most futtasd a `cargo test` parancsot a legfelső szintű _add_ könyvtárban. Ha
egy ilyen felépítésű workspace-ben futtatod a `cargo test` parancsot, az a
workspace összes crate-jének tesztjeit lefuttatja:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

A kimenet első szakasza azt mutatja, hogy az `add_one` crate-ben lévő `it_works`
teszt sikeres volt. A következő szakasz azt mutatja, hogy az `adder` crate-ben
nulla tesztet találtunk, az utolsó szakasz pedig azt, hogy az `add_one`
crate-ben nulla dokumentációs tesztet találtunk.

Egy workspace-ben lévő adott crate tesztjeit is futtathatjuk a legfelső szintű
könyvtárból, ha használjuk a `-p` kapcsolót, és megadjuk annak a crate-nek a
nevét, amelyet tesztelni szeretnénk:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Ez a kimenet azt mutatja, hogy a `cargo test` csak az `add_one` crate tesztjeit
futtatta le, az `adder` crate tesztjeit nem.

Ha a workspace crate-jeit publikálod a [crates.io](https://crates.io/)<!--
ignore --> oldalra, a workspace minden crate-jét külön kell publikálni. A `cargo
test`-hez hasonlóan a workspace egy adott crate-jét a `-p` kapcsolóval és a
publikálni kívánt crate nevének megadásával publikálhatjuk.

További gyakorlásként vegyél fel egy `add_two` crate-et is ebbe a workspace-be,
hasonlóan az `add_one` crate-hez!

Ahogy a projekted nő, érdemes workspace-t használni: így egyetlen nagy kódmassza
helyett kisebb, könnyebben érthető komponensekkel dolgozhatsz. Emellett ha a
crate-eket egy workspace-ben tartod, az megkönnyítheti a crate-ek közötti
összehangolást, amennyiben gyakran egyszerre változnak.
