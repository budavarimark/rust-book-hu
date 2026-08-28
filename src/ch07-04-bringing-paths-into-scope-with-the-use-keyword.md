## Útvonalak hatókörbe hozása a `use` kulcsszóval

Kényelmetlennek és ismétlődőnek tűnhet, hogy a függvények hívásához ki kell
írnunk az útvonalakat. A 7-7. listában, akár az abszolút, akár a relatív
útvonalat választottuk az `add_to_waitlist` függvényhez, minden alkalommal, ha
meg akartuk hívni az `add_to_waitlist`-et, a `front_of_house`-t és a
`hosting`-ot is meg kellett adnunk. Szerencsére van mód a folyamat
egyszerűsítésére: a `use` kulcsszóval egyszer létrehozhatunk egy rövidítést egy
útvonalhoz, majd a hatókör összes többi pontján a rövidebb nevet használhatjuk.

A 7-11. listában a `crate::front_of_house::hosting` modult hozzuk be az
`eat_at_restaurant` függvény hatókörébe, így az `add_to_waitlist` függvény
`eat_at_restaurant`-beli hívásához már csak a `hosting::add_to_waitlist`-et kell
megadnunk.

<Listing number="7-11" file-name="src/lib.rs" caption="Modul hatókörbe hozása a `use` segítségével">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Egy `use` és egy útvonal hozzáadása egy hatókörben hasonlít ahhoz, mint amikor
szimbolikus linket hozunk létre a fájlrendszerben. Azzal, hogy a crate
gyökerében hozzáadjuk a `use crate::front_of_house::hosting` sort, a `hosting`
mostantól érvényes név abban a hatókörben, épp úgy, mintha a `hosting` modul a
crate gyökerében lett volna definiálva. A `use`-zal hatókörbe hozott útvonalakra
is vonatkozik a privátság ellenőrzése, ahogy minden más útvonalra.

Vedd figyelembe, hogy a `use` csak abban a bizonyos hatókörben hozza létre a
rövidítést, amelyben szerepel. A 7-12. listában az `eat_at_restaurant` függvényt
egy új, `customer` nevű gyermekmodulba mozgatjuk, ami így már más hatókör, mint
a `use` utasításé, ezért a függvény törzse nem fordul le.

<Listing number="7-12" file-name="src/lib.rs" caption="A `use` utasítás csak abban a hatókörben érvényes, amelyben van.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

A fordítási hiba mutatja, hogy a rövidítés a `customer` modulon belül már nem
érvényes:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Vedd észre, hogy egy figyelmeztetés is szerepel arról, hogy a `use` a saját
hatókörében már nincs használatban! A probléma megoldásához vagy mozgasd a
`use`-t is a `customer` modulba, vagy a gyermek `customer` modulon belül
hivatkozz a szülőmodulban lévő rövidítésre a `super::hosting` alakkal.

### Idiomatikus `use`-útvonalak írása {#creating-idiomatic-use-paths}

A 7-11. listánál talán felmerült benned, miért a
`use crate::front_of_house::hosting` sort adtuk meg, majd miért a
`hosting::add_to_waitlist`-et hívtuk az `eat_at_restaurant`-ban ahelyett, hogy
ugyanennek az eredménynek az eléréséhez a `use` útvonalát egészen az
`add_to_waitlist` függvényig írtuk volna ki, ahogy a 7-13. listában látható.

<Listing number="7-13" file-name="src/lib.rs" caption="Az `add_to_waitlist` függvény hatókörbe hozása a `use` segítségével, ami nem idiomatikus">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Bár a 7-11. és a 7-13. lista ugyanazt a feladatot végzi el, a 7-11. lista az
idiomatikus módja annak, hogy egy függvényt a `use`-zal hatókörbe hozzunk. Ha a
függvény szülőmodulját hozzuk hatókörbe a `use`-zal, akkor a függvény hívásakor
meg kell adnunk a szülőmodult. A szülőmodul megadása a függvény hívásakor
világossá teszi, hogy a függvény nem helyben van definiálva, miközben a teljes
útvonal ismétlését is minimálisra csökkenti. A 7-13. listában lévő kódból nem
derül ki egyértelműen, hol van az `add_to_waitlist` definiálva.

Ezzel szemben structok, enumok és egyéb elemek `use`-zal való behozatalakor az
idiomatikus megoldás a teljes útvonal megadása. A 7-14. lista azt az
idiomatikus módot mutatja be, ahogyan a standard könyvtár `HashMap` structját
egy binary crate hatókörébe hozzuk.

<Listing number="7-14" file-name="src/main.rs" caption="A `HashMap` hatókörbe hozása idiomatikus módon">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Nincs erős indok e mögött az idióma mögött: egyszerűen ez a konvenció alakult
ki, és az emberek megszokták, hogy így olvassák és írják a Rust-kódot.

Az idióma alóli kivétel az, ha két azonos nevű elemet hozunk hatókörbe `use`
utasításokkal, mert azt a Rust nem engedi meg. A 7-15. lista azt mutatja be,
hogyan hozhatunk hatókörbe két olyan `Result` típust, amelyek neve azonos, de
szülőmoduljuk eltérő, és hogyan hivatkozhatunk rájuk.

<Listing number="7-15" file-name="src/lib.rs" caption="Ha két azonos nevű típust hozunk ugyanabba a hatókörbe, használnunk kell a szülőmoduljaikat.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Ahogy látod, a szülőmodulok használata megkülönbözteti a két `Result` típust. Ha
ehelyett a `use std::fmt::Result` és a `use std::io::Result` sorokat adnánk meg,
két `Result` típusunk lenne ugyanabban a hatókörben, és a Rust nem tudná, melyik
`Result`-ra gondolunk, amikor a `Result`-ot használjuk.

### Új nevek megadása az `as` kulcsszóval

Van egy másik megoldás is arra a problémára, hogy két azonos nevű típust hozunk
`use`-zal ugyanabba a hatókörbe: az útvonal után megadhatjuk az `as` kulcsszót
és a típus új, helyi nevét, azaz egy _aliast_. A 7-16. lista a 7-15. listában
szereplő kód megírásának egy másik módját mutatja be: a két `Result` típus közül
az egyiket az `as` segítségével átnevezi.

<Listing number="7-16" file-name="src/lib.rs" caption="Típus átnevezése az `as` kulcsszóval, amikor hatókörbe hozzuk">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

A második `use` utasításban az `IoResult` új nevet választottuk a
`std::io::Result` típusnak, ami így nem ütközik a `std::fmt`-ből származó
`Result`-tal, amelyet szintén hatókörbe hoztunk. A 7-15. és a 7-16. lista
egyaránt idiomatikusnak számít, így rajtad áll a választás!

### Nevek újraexportálása a `pub use` segítségével

Amikor egy nevet a `use` kulcsszóval hatókörbe hozunk, a név privát abban a
hatókörben, amelybe importáltuk. Ahhoz, hogy az adott hatókörön kívüli kód is
úgy hivatkozhasson erre a névre, mintha abban a hatókörben lett volna
definiálva, kombinálhatjuk a `pub`-ot és a `use`-t. Ezt a technikát
_újraexportálásnak_ nevezzük, mert nemcsak hatókörbe hozunk egy elemet, hanem
elérhetővé is tesszük, hogy mások a saját hatókörükbe hozhassák.

A 7-17. lista a 7-11. listában szereplő kódot mutatja, azzal a különbséggel,
hogy a gyökérmodulban a `use`-t `pub use`-ra cseréltük.

<Listing number="7-17" file-name="src/lib.rs" caption="Név elérhetővé tétele bármilyen kód számára egy új hatókörből a `pub use` segítségével">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

E változtatás előtt a külső kódnak a
`restaurant::front_of_house::hosting::add_to_waitlist()` útvonalon kellett volna
meghívnia az `add_to_waitlist` függvényt, ami ráadásul azt is megkövetelte
volna, hogy a `front_of_house` modul `pub`-ként legyen megjelölve. Most, hogy ez
a `pub use` újraexportálta a `hosting` modult a gyökérmodulból, a külső kód
helyette a `restaurant::hosting::add_to_waitlist()` útvonalat használhatja.

Az újraexportálás akkor hasznos, ha a kódod belső szerkezete eltér attól,
ahogyan a kódodat hívó programozók a témakörről gondolkodnak. Ebben az
éttermes hasonlatban például az éttermet üzemeltető emberek „front of house” és
„back of house” fogalmakban gondolkodnak. Az étterembe betérő vendégek viszont
valószínűleg nem ilyen kifejezésekben gondolkodnak az étterem részeiről. A
`pub use` segítségével a kódunkat az egyik szerkezet szerint írhatjuk meg, de
egy másik szerkezetet tehetünk közzé. Így a könyvtárunk jól szervezett lesz
azoknak a programozóknak, akik a könyvtáron dolgoznak, és azoknak is, akik a
könyvtárat hívják. A 14. fejezetben, a [„Kényelmes nyilvános API
exportálása”][ch14-pub-use]<!-- ignore --> szakaszban megnézünk egy másik `pub
use`-példát, és azt is, hogyan hat ez a crate-ed dokumentációjára.

### Külső csomagok használata

A 2. fejezetben egy kitalálós játék projektet programoztunk, amely egy `rand`
nevű külső csomagot használt véletlen számok előállítására. Ahhoz, hogy a
`rand`-ot használhassuk a projektünkben, ezt a sort adtuk a _Cargo.toml_
fájlhoz:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Ha a `rand`-ot függőségként adjuk hozzá a _Cargo.toml_ fájlhoz, azzal azt
mondjuk a Cargónak, hogy töltse le a `rand` csomagot és annak összes függőségét
a [crates.io](https://crates.io/) oldalról, és tegye elérhetővé a `rand`-ot a
projektünk számára.

Ezután ahhoz, hogy a `rand` definícióit a csomagunk hatókörébe hozzuk, egy
`use` sort adtunk hozzá, amely a crate nevével, a `rand`-dal kezdődött, és
felsorolta azokat az elemeket, amelyeket hatókörbe akartunk hozni. Emlékezz
vissza: a 2. fejezetben a [„Véletlen szám előállítása”][rand]<!-- ignore -->
szakaszban a `rand::prelude` modulban lévő elemeket hoztuk hatókörbe, és a
`rand::rng` függvényt hívtuk meg:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

A Rust közösségének tagjai rengeteg csomagot tettek elérhetővé a
[crates.io](https://crates.io/) oldalon, és bármelyikük behúzása a csomagodba
ugyanezekből a lépésekből áll: felveszed őket a csomagod _Cargo.toml_ fájljába,
és a `use`-zal hatókörbe hozod a crate-jeikből az elemeket.

Vedd figyelembe, hogy a standard `std` könyvtár szintén olyan crate, amely a
csomagunkon kívül van. Mivel a standard könyvtár a Rust nyelvvel együtt
érkezik, nem kell módosítanunk a _Cargo.toml_ fájlt ahhoz, hogy az `std`-t
felvegyük. Arra viszont szükség van, hogy `use`-zal hivatkozzunk rá, hogy az
onnan származó elemeket a csomagunk hatókörébe hozzuk. A `HashMap` esetében
például ezt a sort használnánk:

```rust
use std::collections::HashMap;
```

Ez egy abszolút útvonal, amely az `std`-vel, a standard könyvtár crate nevével
kezdődik.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Egymásba ágyazott útvonalak a `use`-listák rendbetételéhez

Ha ugyanabban a crate-ben vagy ugyanabban a modulban definiált több elemet is
használunk, sok függőleges helyet foglalhat el a fájljainkban, ha minden elemet
külön sorban sorolunk fel. Például ez a két `use` utasítás, amely a 2-4.
listában szereplő kitalálós játékban volt, elemeket hoz hatókörbe az `std`-ből:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Ehelyett egymásba ágyazott útvonalakkal egyetlen sorban is hatókörbe hozhatjuk
ugyanezeket az elemeket. Ehhez megadjuk az útvonal közös részét, majd két
kettőspontot, végül kapcsos zárójelek közé tesszük az útvonalak eltérő
részeinek listáját, ahogy azt a 7-18. lista mutatja.

<Listing number="7-18" file-name="src/main.rs" caption="Egymásba ágyazott útvonal megadása több, azonos előtagú elem hatókörbe hozásához">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Nagyobb programokban, ha egyazon crate-ből vagy modulból sok elemet hozunk
hatókörbe egymásba ágyazott útvonalakkal, azzal rengeteg különálló `use`
utasítást takaríthatunk meg!

Egymásba ágyazott útvonalat egy útvonal bármely szintjén használhatunk, ami
hasznos két olyan `use` utasítás összevonásakor, amelyek osztoznak egy
részútvonalon. A 7-19. lista például két `use` utasítást mutat: az egyik az
`std::io`-t, a másik az `std::io::Write`-ot hozza hatókörbe.

<Listing number="7-19" file-name="src/lib.rs" caption="Két `use` utasítás, amelyek közül az egyik a másik részútvonala">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

E két útvonal közös része az `std::io`, ami egyben a teljes első útvonal is.
Ahhoz, hogy ezt a két útvonalat egyetlen `use` utasításba olvasszuk, a `self`-et
használhatjuk az egymásba ágyazott útvonalban, ahogy azt a 7-20. lista mutatja.

<Listing number="7-20" file-name="src/lib.rs" caption="A 7-19. listában szereplő útvonalak összevonása egyetlen `use` utasításba">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Ez a sor az `std::io`-t és az `std::io::Write`-ot is hatókörbe hozza.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Elemek importálása a glob operátorral

Ha egy útvonalban definiált _összes_ nyilvános elemet hatókörbe akarjuk hozni,
megadhatjuk az útvonalat, majd utána a `*` glob operátort:

```rust
use std::collections::*;
```

Ez a `use` utasítás az `std::collections`-ben definiált összes nyilvános elemet
az aktuális hatókörbe hozza. Légy óvatos a glob operátor használatakor! A glob
megnehezítheti annak megállapítását, hogy mely nevek vannak hatókörben, és hol
lett definiálva egy, a programodban használt név. Ezen felül, ha a függőség
megváltoztatja a definícióit, akkor az is megváltozik, amit importáltál, ami
fordítási hibákhoz vezethet a függőség frissítésekor, például akkor, ha a
függőség olyan definíciót vesz fel, amelynek a neve megegyezik egy saját,
ugyanabban a hatókörben lévő definícióddal.

A glob operátort gyakran használják teszteléskor, hogy a teszt alatt álló
mindent behozzák a `tests` modulba; erről a 11. fejezetben, a [„Hogyan írjunk
teszteket”][writing-tests]<!-- ignore --> szakaszban lesz szó. A glob operátort
néha a prelude minta részeként is használják: erről a mintáról lásd
[a standard könyvtár
dokumentációját](../std/prelude/index.html#other-preludes)<!-- ignore -->.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
