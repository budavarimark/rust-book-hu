## A tesztek futtatásának szabályozása {#controlling-how-tests-are-run}

Ahogy a `cargo run` lefordítja a kódodat, majd lefuttatja a kapott binárist, a
`cargo test` teszt módban fordítja le a kódodat, és lefuttatja a kapott
tesztbinárist. A `cargo test` által előállított bináris alapértelmezett
viselkedése az, hogy az összes tesztet párhuzamosan futtatja, és elkapja a
tesztek futása során keletkező kimenetet, megakadályozva annak megjelenítését,
így könnyebben olvashatóvá téve a teszteredményekhez tartozó kimenetet.
Parancssori opciókkal azonban megváltoztathatod ezt az alapértelmezett
viselkedést.

Egyes parancssori opciók a `cargo test` parancsnak szólnak, mások a kapott
tesztbinárisnak. A kétféle argumentum elválasztásához először a `cargo test`
parancsnak szóló argumentumokat sorolod fel, ezt követi a `--` elválasztó, majd
azok, amelyek a tesztbinárisnak szólnak. A `cargo test --help` futtatása
megjeleníti a `cargo test` parancshoz használható opciókat, a
`cargo test -- --help` futtatása pedig az elválasztó után használható opciókat.
Ezek az opciók dokumentálva vannak [a _The `rustc` Book_ „Tests”
szakaszában][tests] is.

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Tesztek futtatása párhuzamosan vagy egymás után

Amikor több tesztet futtatsz, azok alapértelmezés szerint párhuzamosan,
szálakat használva futnak, ami azt jelenti, hogy hamarabb végeznek, és
gyorsabban kapsz visszajelzést. Mivel a tesztek egyszerre futnak, meg kell
bizonyosodnod arról, hogy a tesztjeid nem függenek egymástól vagy bármilyen
osztott állapottól, beleértve az osztott környezetet is, például az aktuális
munkakönyvtárat vagy a környezeti változókat.

Tegyük fel például, hogy minden tesztedben fut egy kódrészlet, amely létrehoz
egy _test-output.txt_ nevű fájlt a lemezen, és adatokat ír bele. Ezután minden
teszt beolvassa a fájlban lévő adatokat, és azt állítja, hogy a fájl egy adott,
tesztenként eltérő értéket tartalmaz. Mivel a tesztek egyszerre futnak, az
egyik teszt felülírhatja a fájlt abban az időablakban, amikor egy másik teszt
írja, majd olvassa a fájlt. A második teszt ekkor megbukik, nem azért, mert a
kód hibás, hanem azért, mert a tesztek zavarták egymást a párhuzamos futás
közben. Az egyik megoldás az, hogy gondoskodunk róla, hogy minden teszt más
fájlba írjon; egy másik megoldás, hogy a teszteket egyesével futtatjuk.

Ha nem akarod párhuzamosan futtatni a teszteket, vagy finomabb kontrollt
szeretnél a használt szálak száma felett, elküldheted a `--test-threads`
kapcsolót és a használni kívánt szálak számát a tesztbinárisnak. Nézd meg a
következő példát:

```console
$ cargo test -- --test-threads=1
```

A tesztszálak számát `1`-re állítjuk, ezzel megmondva a programnak, hogy ne
használjon párhuzamosságot. A tesztek egy szálon való futtatása tovább tart,
mint a párhuzamos futtatás, de a tesztek nem zavarják egymást, ha osztoznak
valamilyen állapoton.

### A függvények kimenetének megjelenítése

Alapértelmezés szerint, ha egy teszt sikeres, a Rust tesztkönyvtára elkapja
mindazt, amit a standard kimenetre írtak. Ha például meghívjuk a `println!`
makrót egy tesztben, és a teszt sikeres, nem fogjuk látni a `println!` kimenetét
a terminálban; csak azt a sort látjuk, amely jelzi, hogy a teszt sikeres volt.
Ha egy teszt megbukik, látni fogjuk mindazt, amit a standard kimenetre írtak, a
bukási üzenet többi részével együtt.

Példaként a 11-10. listán egy együgyű függvény szerepel, amely kiírja a
paraméterének értékét, és 10-et ad vissza, valamint egy sikeres és egy
megbukó teszt.

<Listing number="11-10" file-name="src/lib.rs" caption="Tesztek egy olyan függvényhez, amely meghívja a `println!` makrót">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Amikor ezeket a teszteket a `cargo test` paranccsal futtatjuk, a következő
kimenetet látjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Figyeld meg, hogy ebben a kimenetben sehol nem látjuk az `I got the value 4`
szöveget, amely a sikeres teszt futtatásakor íródik ki. Azt a kimenetet a
rendszer elkapta. A megbukott teszt kimenete, az `I got the value 8`, megjelenik
a teszt összegző kimenetének abban a szakaszában, amely a tesztbukás okát is
mutatja.

Ha a sikeres tesztek kiírt értékeit is látni akarjuk, a `--show-output`
kapcsolóval megmondhatjuk a Rustnak, hogy a sikeres tesztek kimenetét is
jelenítse meg:

```console
$ cargo test -- --show-output
```

Amikor a 11-10. lista tesztjeit újra lefuttatjuk a `--show-output` kapcsolóval,
a következő kimenetet látjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Tesztek egy részhalmazának futtatása név alapján {#running-a-subset-of-tests-by-name}

Egy teljes tesztkészlet lefuttatása néha sokáig tarthat. Ha egy adott terület
kódján dolgozol, előfordulhat, hogy csak az ahhoz a kódhoz tartozó teszteket
akarod lefuttatni. Kiválaszthatod, mely tesztek fussanak, ha argumentumként
átadod a `cargo test` parancsnak a futtatni kívánt teszt vagy tesztek nevét.

Hogy bemutassuk, hogyan futtathatók a tesztek egy részhalmaza, először három
tesztet hozunk létre az `add_two` függvényünkhöz, ahogy a 11-11. listán
látható, majd kiválasztjuk, melyik fusson.

<Listing number="11-11" file-name="src/lib.rs" caption="Három teszt három különböző névvel">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Ha argumentumok átadása nélkül futtatjuk a teszteket, ahogy korábban láttuk, az
összes teszt párhuzamosan fut:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Egyetlen teszt futtatása

Bármely tesztfüggvény nevét átadhatjuk a `cargo test` parancsnak, hogy csak azt
a tesztet futtassuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Csak az `one_hundred` nevű teszt futott le; a másik két teszt neve nem
illeszkedett erre a névre. A teszt kimenete tudatja velünk, hogy voltak további
tesztek, amelyek nem futottak le, azzal, hogy a végén megjeleníti a
`2 filtered out` szöveget.

Több teszt nevét nem adhatjuk meg ilyen módon; a `cargo test` parancsnak csak
az első megadott értéket használja. De van mód több teszt futtatására is.

#### Szűrés több teszt futtatásához

Megadhatjuk egy tesztnév egy részét, és minden teszt lefut, amelynek a neve
illeszkedik erre az értékre. Mivel például két tesztünk neve tartalmazza az
`add` szót, ezt a kettőt a `cargo test add` parancs futtatásával futtathatjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Ez a parancs minden olyan tesztet lefuttatott, amelynek a nevében szerepel az
`add`, és kiszűrte az `one_hundred` nevű tesztet. Vedd figyelembe azt is, hogy
az a modul, amelyben egy teszt szerepel, a teszt nevének részévé válik, így egy
modul összes tesztjét lefuttathatjuk a modul nevére való szűréssel.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Tesztek kihagyása, hacsak nem kérjük őket kifejezetten {#ignoring-tests-unless-specifically-requested}

Néha néhány konkrét teszt végrehajtása nagyon időigényes lehet, ezért érdemes
lehet kihagyni őket a `cargo test` futtatásainak nagy részében. Ahelyett, hogy
argumentumként felsorolnád az összes tesztet, amelyet futtatni akarsz, az
időigényes teszteket megjelölheted az `ignore` attribútummal, hogy kimaradjanak,
ahogy itt látható:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

A `#[test]` után hozzáadjuk a `#[ignore]` sort ahhoz a teszthez, amelyet ki
akarunk hagyni. Most, amikor lefuttatjuk a tesztjeinket, az `it_works` lefut, az
`expensive_test` viszont nem:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Az `expensive_test` függvény `ignored` jelöléssel szerepel a listában. Ha csak a
figyelmen kívül hagyott teszteket akarjuk futtatni, használhatjuk a
`cargo test -- --ignored` parancsot:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Azzal, hogy szabályozod, mely tesztek fussanak, gondoskodhatsz róla, hogy a
`cargo test` eredményei gyorsan megérkezzenek. Amikor eljutsz oda, hogy érdemes
ellenőrizni az `ignored` tesztek eredményeit, és van időd megvárni azokat,
helyette a `cargo test -- --ignored` parancsot futtathatod. Ha az összes
tesztet futtatni akarod, akár figyelmen kívül vannak hagyva, akár nem, a
`cargo test -- --include-ignored` parancsot futtathatod.
