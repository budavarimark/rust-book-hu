## A tesztek szervezése

Ahogy a fejezet elején említettük, a tesztelés összetett szakterület, és
különböző emberek különböző terminológiát és szervezési módot használnak. A Rust
közössége két fő kategóriában gondolkodik a tesztekről: egységtesztek és
integrációs tesztek. Az _egységtesztek_ kicsik és fókuszáltabbak, egyszerre egy
modult tesztelnek elszigetelten, és a privát interfészeket is tesztelhetik. Az
_integrációs tesztek_ teljesen kívül esnek a könyvtáradon, és ugyanúgy
használják a kódodat, ahogy bármely más külső kód tenné: csak a publikus
interfészt veszik igénybe, és tesztenként több modult is mozgásba hozhatnak.

Mindkét tesztfajta megírása fontos ahhoz, hogy megbizonyosodj róla: a könyvtárad
darabjai külön-külön és együtt is azt teszik, amit elvársz tőlük.

### Egységtesztek

Az egységtesztek célja az, hogy a kód minden egyes egységét a kód többi részétől
elszigetelten teszteljék, így gyorsan kideríthető, hol működik a kód az elvárt
módon, és hol nem. Az egységteszteket az _src_ könyvtárban, abban a fájlban
helyezed el, amelyben a tesztelt kód is van. A bevett szokás az, hogy minden
fájlban létrehozol egy `tests` nevű modult a tesztfüggvények számára, és a
modult a `cfg(test)` attribútummal jelölöd meg.

#### A `tests` modul és a `#[cfg(test)]`

A `tests` modulon szereplő `#[cfg(test)]` annotáció azt mondja meg a Rustnak,
hogy a tesztkódot csak akkor fordítsa le és futtassa, amikor a `cargo test`
parancsot adod ki, a `cargo build` esetén viszont ne. Ez fordítási időt takarít
meg, amikor csak a könyvtárat akarod lefordítani, és helyet spórol az így
keletkező lefordított artifactban, mert a tesztek nem kerülnek bele. Látni
fogod, hogy az integrációs teszteknek nincs szükségük a `#[cfg(test)]`
annotációra, mivel külön könyvtárba kerülnek. Az egységtesztek viszont
ugyanabban a fájlban vannak, mint a kód, ezért a `#[cfg(test)]` segítségével
jelzed, hogy ne kerüljenek bele a lefordított eredménybe.

Emlékezz vissza: amikor a fejezet első szakaszában létrehoztuk az új `adder`
projektet, a Cargo ezt a kódot generálta nekünk:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Az automatikusan generált `tests` modulon a `cfg` attribútum a _configuration_
(konfiguráció) rövidítése, és azt közli a Rusttal, hogy az utána következő elem
csak egy adott konfigurációs beállítás mellett kerüljön bele a fordításba. Ebben
az esetben a konfigurációs beállítás a `test`, amelyet a Rust biztosít a tesztek
fordításához és futtatásához. A `cfg` attribútum használatával a Cargo csak
akkor fordítja le a tesztkódunkat, ha ténylegesen futtatjuk a teszteket a `cargo
test` paranccsal. Ez a `#[test]` annotációval ellátott függvényeken túl minden
olyan segédfüggvényre is vonatkozik, amely ebben a modulban lehet.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Privát függvények tesztelése

A tesztelői közösségen belül vita folyik arról, hogy a privát függvényeket
kell-e közvetlenül tesztelni, más nyelvek pedig megnehezítik vagy egyenesen
lehetetlenné teszik a privát függvények tesztelését. Bármelyik tesztelési
szemléletet is követed, a Rust láthatósági szabályai lehetővé teszik a privát
függvények tesztelését. Nézzük meg a 11-12. listában szereplő kódot az
`internal_adder` privát függvénnyel.

<Listing number="11-12" file-name="src/lib.rs" caption="Egy privát függvény tesztelése">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Figyeld meg, hogy az `internal_adder` függvény nincs `pub`-ként megjelölve. A
tesztek is csak Rust-kódok, a `tests` modul pedig csak egy modul a többi közül.
Ahogy az [„Útvonalak a modulfában lévő elemekre való
hivatkozáshoz”][paths]<!-- ignore --> részben tárgyaltuk, a gyermekmodulokban
lévő elemek használhatják az őseik moduljaiban lévő elemeket. Ebben a tesztben a
`use super::*` segítségével hatókörbe hozzuk a `tests` modul szülőjéhez tartozó
összes elemet, így a teszt meg tudja hívni az `internal_adder` függvényt. Ha
szerinted a privát függvényeket nem kellene tesztelni, a Rustban semmi nem
kényszerít erre.

### Integrációs tesztek

A Rustban az integrációs tesztek teljesen kívül esnek a könyvtáradon. Ugyanúgy
használják a könyvtáradat, ahogy bármely más kód tenné, ami azt jelenti, hogy
csak olyan függvényeket hívhatnak meg, amelyek a könyvtárad publikus API-jának
részei. A céljuk annak tesztelése, hogy a könyvtárad számos része helyesen
működik-e együtt. A kód önmagukban helyesen működő egységei az integráció után
hibásan viselkedhetnek, ezért az integrált kód tesztlefedettsége is fontos. Az
integrációs tesztek létrehozásához először egy _tests_ könyvtárra van szükséged.

#### A _tests_ könyvtár

Hozzunk létre egy _tests_ könyvtárat a projektkönyvtárunk legfelső szintjén, az
_src_ mellett. A Cargo tudja, hogy ebben a könyvtárban kell keresnie az
integrációs tesztek fájljait. Ezután annyi tesztfájlt hozhatunk létre, amennyit
csak akarunk, és a Cargo mindegyik fájlt önálló crate-ként fordítja le.

Készítsünk egy integrációs tesztet. Hagyd a 11-12. lista kódját az _src/lib.rs_
fájlban, hozz létre egy _tests_ könyvtárat, és benne egy
_tests/integration_test.rs_ nevű új fájlt. A könyvtárszerkezetednek így kell
kinéznie:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Írd be a 11-13. listában szereplő kódot a _tests/integration_test.rs_ fájlba.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Az `adder` crate egyik függvényének integrációs tesztje">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

A _tests_ könyvtár minden fájlja külön crate, ezért minden egyes tesztcrate
hatókörébe be kell hoznunk a könyvtárunkat. Emiatt írjuk a kód elejére a `use
adder::add_two;` sort, amire az egységteszteknél nem volt szükségünk.

A _tests/integration_test.rs_ fájlban semmilyen kódot nem kell a `#[cfg(test)]`
annotációval ellátnunk. A Cargo külön kezeli a _tests_ könyvtárat, és az ebben a
könyvtárban lévő fájlokat csak akkor fordítja le, amikor a `cargo test`
parancsot futtatjuk. Futtassuk most a `cargo test` parancsot:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

A kimenet három szakasza az egységteszteket, az integrációs tesztet és a
dokumentációs teszteket tartalmazza. Vedd figyelembe, hogy ha egy szakaszban
bármelyik teszt elbukik, a következő szakaszok nem futnak le. Ha például egy
egységteszt bukik el, semmilyen kimenet nem lesz az integrációs és a
dokumentációs tesztekhez, mert azok csak akkor futnak le, ha minden egységteszt
sikeres.

Az egységtesztekhez tartozó első szakasz ugyanaz, mint amit eddig is láttunk:
egy sor minden egységteszthez (egy `internal` nevű, amelyet a 11-12. listában
adtunk hozzá), majd egy összegző sor az egységtesztekről.

Az integrációs tesztek szakasza a `Running tests/integration_test.rs` sorral
kezdődik. Ezután egy-egy sor következik az integrációs teszt minden
tesztfüggvényéhez, majd egy összegző sor az integrációs teszt eredményéről,
közvetlenül a `Doc-tests adder` szakasz kezdete előtt.

Minden integrációs tesztfájlnak megvan a maga szakasza, tehát ha több fájlt
adunk hozzá a _tests_ könyvtárhoz, több integrációs teszt szakasz lesz.

Egy adott integrációs tesztfüggvényt továbbra is futtathatunk úgy, hogy a
tesztfüggvény nevét argumentumként megadjuk a `cargo test` parancsnak. Ha egy
adott integrációs tesztfájl összes tesztjét akarod futtatni, használd a `cargo
test` `--test` argumentumát, amelyet a fájl neve követ:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Ez a parancs csak a _tests/integration_test.rs_ fájlban lévő teszteket futtatja
le.

#### Almodulok az integrációs tesztekben

Ahogy egyre több integrációs tesztet adsz hozzá, elképzelhető, hogy több fájlt
akarsz létrehozni a _tests_ könyvtárban, hogy jobban rendszerezhesd őket;
csoportosíthatod például a tesztfüggvényeket az általuk tesztelt funkcionalitás
szerint. Ahogy korábban említettük, a _tests_ könyvtár minden fájlja önálló
crate-ként fordul le, ami hasznos külön hatókörök létrehozásához, hogy jobban
utánozzuk azt, ahogyan a végfelhasználók használni fogják a crate-edet. Ez
viszont azt is jelenti, hogy a _tests_ könyvtárban lévő fájlok nem ugyanúgy
viselkednek, mint az _src_ fájljai, ahogy azt a 7. fejezetben a kód modulokra és
fájlokra bontásáról tanultad.

A _tests_ könyvtár fájljainak eltérő viselkedése akkor a legszembetűnőbb, amikor
van egy sor segédfüggvényed, amelyet több integrációs tesztfájlban is használni
szeretnél, és megpróbálod követni a 7. fejezet [„Modulok szétválasztása külön
fájlokba”][separating-modules-into-files]<!-- ignore --> című szakaszának
lépéseit, hogy ezeket egy közös modulba emeld ki. Ha például létrehozzuk a
_tests/common.rs_ fájlt, és elhelyezünk benne egy `setup` nevű függvényt,
írhatunk a `setup` függvénybe olyan kódot, amelyet több tesztfájl több
tesztfüggvényéből is meg akarunk hívni:

<span class="filename">Fájlnév: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Amikor újra lefuttatjuk a teszteket, egy új szakaszt látunk a tesztek
kimenetében a _common.rs_ fájlhoz, pedig ez a fájl egyetlen tesztfüggvényt sem
tartalmaz, és a `setup` függvényt sem hívtuk meg sehonnan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Nem ezt akartuk, hogy a `common` megjelenjen a tesztek eredményei között a
`running 0 tests` felirattal. Csak meg akartunk osztani némi kódot a többi
integrációs tesztfájllal. Ahhoz, hogy a `common` ne jelenjen meg a tesztek
kimenetében, a _tests/common.rs_ helyett a _tests/common/mod.rs_ fájlt hozzuk
létre. A projektkönyvtár most így néz ki:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Ez az a régebbi elnevezési konvenció, amelyet a Rust szintén megért, és amelyet
a 7. fejezet [„Alternatív fájlútvonalak”][alt-paths]<!-- ignore --> szakaszában
említettünk. Ha így nevezed el a fájlt, azzal azt mondod a Rustnak, hogy ne
kezelje a `common` modult integrációs tesztfájlként. Amikor a `setup` függvény
kódját átmozgatjuk a _tests/common/mod.rs_ fájlba, és töröljük a
_tests/common.rs_ fájlt, a tesztek kimenetében lévő szakasz többé nem jelenik
meg. A _tests_ könyvtár alkönyvtáraiban lévő fájlok nem fordulnak le külön
crate-ként, és nem kapnak szakaszt a tesztek kimenetében.

Miután létrehoztuk a _tests/common/mod.rs_ fájlt, bármelyik integrációs
tesztfájlból modulként használhatjuk. Íme egy példa arra, hogyan hívjuk meg a
`setup` függvényt az `it_adds_two` tesztből a _tests/integration_test.rs_
fájlban:

<span class="filename">Fájlnév: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Figyeld meg, hogy a `mod common;` deklaráció ugyanaz, mint az a
modul-deklaráció, amelyet a 7-21. listában mutattunk be. Ezután a
tesztfüggvényben meghívhatjuk a `common::setup()` függvényt.

#### Binary crate-ek integrációs tesztjei

Ha a projektünk olyan binary crate, amely csak egy _src/main.rs_ fájlt
tartalmaz, és nincs benne _src/lib.rs_ fájl, akkor nem hozhatunk létre
integrációs teszteket a _tests_ könyvtárban, és nem hozhatjuk hatókörbe egy
`use` utasítással az _src/main.rs_ fájlban definiált függvényeket. Csak a
library crate-ek tesznek elérhetővé olyan függvényeket, amelyeket más crate-ek
használhatnak; a binary crate-eket önálló futtatásra szánták.

Ez az egyik oka annak, hogy azok a Rust-projektek, amelyek binárist
biztosítanak, egyszerű _src/main.rs_ fájlt tartalmaznak, amely az _src/lib.rs_
fájlban lévő logikát hívja meg. Ezzel a szerkezettel az integrációs tesztek
_tudják_ tesztelni a library crate-et a `use` segítségével, elérhetővé téve a
fontos funkcionalitást. Ha a fontos funkcionalitás működik, akkor az
_src/main.rs_ fájlban lévő kevés kód is működni fog, és azt a kevés kódot nem
kell tesztelni.

## Összefoglalás

A Rust tesztelési képességei módot adnak arra, hogy megadd, hogyan kellene
működnie a kódnak, így biztosítva, hogy az továbbra is az elvárásaid szerint
működjön, még akkor is, ha változtatásokat végzel rajta. Az egységtesztek
külön-külön mozgatják meg egy könyvtár különböző részeit, és a privát
implementációs részleteket is tesztelhetik. Az integrációs tesztek azt
ellenőrzik, hogy a könyvtár számos része helyesen működik-e együtt, és a
könyvtár publikus API-ját használják a kód tesztelésére, ugyanúgy, ahogy a külső
kód is használni fogja. Bár a Rust típusrendszere és ownership-szabályai
segítenek megelőzni bizonyos fajta hibákat, a tesztek továbbra is fontosak azon
logikai hibák csökkentéséhez, amelyek a kódod elvárt viselkedéséhez
kapcsolódnak.

Kapcsoljuk össze az ebben a fejezetben és a korábbi fejezetekben tanultakat, és
dolgozzunk egy projekten!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
