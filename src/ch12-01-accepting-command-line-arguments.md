## Parancssori argumentumok fogadása

Hozzunk létre egy új projektet, szokás szerint a `cargo new` paranccsal. A
projektünket `minigrep`-nek nevezzük el, hogy megkülönböztessük a `grep`
eszköztől, amely talán már megtalálható a rendszereden:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Az első feladat az, hogy a `minigrep` fogadja a két parancssori argumentumát: a
fájlútvonalat és a keresendő karakterláncot. Vagyis azt szeretnénk, hogy a
programunkat a `cargo run` paranccsal futtathassuk, utána két kötőjellel
jelezve, hogy az azt követő argumentumok a mi programunknak szólnak, nem a
`cargo`-nak, majd megadhassuk a keresendő karakterláncot és a fájl útvonalát,
amelyben keresni akarunk, így:

```console
$ cargo run -- searchstring example-filename.txt
```

Jelenleg a `cargo new` által generált program nem tudja feldolgozni a neki
átadott argumentumokat. Néhány létező könyvtár a [crates.io](https://crates.io/)
oldalon segítséget nyújt parancssori argumentumokat fogadó programok írásához,
de mivel épp most ismerkedsz ezzel a fogalommal, valósítsuk meg magunk ezt a
képességet.

### Az argumentumértékek beolvasása

Ahhoz, hogy a `minigrep` be tudja olvasni a neki átadott parancssori
argumentumok értékeit, a Rust standard könyvtárában található `std::env::args`
függvényre lesz szükségünk. Ez a függvény a `minigrep`-nek átadott parancssori
argumentumok iterátorát adja vissza. Az iterátorokat teljes körűen a [13.
fejezetben][ch13]<!-- ignore --> tárgyaljuk. Egyelőre csak két dolgot kell
tudnod az iterátorokról: az iterátorok értékek sorozatát állítják elő, és
meghívhatjuk egy iterátoron a `collect` metódust, hogy kollekcióvá – például
vektorrá – alakítsuk, amely az iterátor által előállított összes elemet
tartalmazza.

A 12-1. listában szereplő kód lehetővé teszi, hogy a `minigrep` programod
beolvassa a neki átadott parancssori argumentumokat, majd az értékeket egy
vektorba gyűjtse.

<Listing number="12-1" file-name="src/main.rs" caption="A parancssori argumentumok vektorba gyűjtése és kiírása">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Először egy `use` utasítással hatókörbe hozzuk a `std::env` modult, hogy
használhassuk az `args` függvényét. Figyeld meg, hogy a `std::env::args`
függvény két modulszint mélyén található. Ahogy a [7.
fejezetben][ch7-idiomatic-use]<!-- ignore --> tárgyaltuk, olyan esetekben,
amikor a kívánt függvény egynél több modulba van beágyazva, inkább a szülő
modult hozzuk hatókörbe, mint magát a függvényt. Így könnyen használhatjuk a
`std::env` többi függvényét is. Ez egyben kevésbé félreérthető, mint a `use
std::env::args` írása, majd a függvény meghívása pusztán az `args` névvel, mert
az `args`-ot könnyen összetéveszthetnénk egy olyan függvénnyel, amelyet a
jelenlegi modulban definiáltak.

> ### Az `args` függvény és az érvénytelen Unicode
>
> Vedd figyelembe, hogy a `std::env::args` panicot vált ki, ha bármelyik
> argumentum érvénytelen Unicode-ot tartalmaz. Ha a programodnak érvénytelen
> Unicode-ot tartalmazó argumentumokat is fogadnia kell, használd helyette a
> `std::env::args_os` függvényt. Az a függvény olyan iterátort ad vissza, amely
> `String` értékek helyett `OsString` értékeket állít elő. Az egyszerűség
> kedvéért itt a `std::env::args` használata mellett döntöttünk, mert az
> `OsString` értékek platformonként eltérnek, és bonyolultabb velük dolgozni,
> mint a `String` értékekkel.

A `main` első sorában meghívjuk az `env::args` függvényt, és azonnal a `collect`
segítségével vektorrá alakítjuk az iterátort, amely az iterátor által
előállított összes értéket tartalmazza. A `collect` függvénnyel sokféle
kollekciót létrehozhatunk, ezért kifejezetten megadjuk az `args` típusát, hogy
jelezzük: karakterláncok vektorát akarjuk. Bár a Rustban nagyon ritkán kell
típusokat megadni, a `collect` az egyik olyan függvény, amelynél gyakran
szükséges, mert a Rust nem tudja kikövetkeztetni, milyen kollekciót szeretnél.

Végül a debug makróval kiírjuk a vektort. Próbáljuk meg lefuttatni a kódot
először argumentumok nélkül, majd két argumentummal:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Figyeld meg, hogy a vektor első értéke a `"target/debug/minigrep"`, ami a
binárisunk neve. Ez megegyezik a C-ben megszokott argumentumlista
viselkedésével, és lehetővé teszi a programoknak, hogy futás közben használják
azt a nevet, amellyel meghívták őket. Gyakran kényelmes, ha hozzáférünk a
program nevéhez, például ha ki akarjuk írni üzenetekben, vagy a program
viselkedését attól akarjuk függővé tenni, milyen parancssori aliasszal hívták
meg. Ebben a fejezetben azonban figyelmen kívül hagyjuk, és csak azt a két
argumentumot mentjük el, amelyre szükségünk van.

### Az argumentumértékek elmentése változókba

A program jelenleg hozzá tud férni a parancssori argumentumként megadott
értékekhez. Most el kell mentenünk a két argumentum értékét változókba, hogy a
program további részében is használhassuk őket. Ezt tesszük a 12-2. listában.

<Listing number="12-2" file-name="src/main.rs" caption="Változók létrehozása a keresési kifejezés és a fájlútvonal argumentumának tárolására">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Ahogy a vektor kiírásakor láttuk, a program neve foglalja el a vektor első
értékét az `args[0]` helyen, ezért az argumentumokat az 1-es indextől kezdjük. A
`minigrep` első argumentuma a keresett karakterlánc, ezért az első argumentumra
mutató referenciát a `query` változóba tesszük. A második argumentum a
fájlútvonal lesz, így a második argumentumra mutató referenciát a `file_path`
változóba tesszük.

Átmenetileg kiírjuk ezeknek a változóknak az értékét, hogy bizonyítsuk: a kód a
szándékaink szerint működik. Futtassuk le újra ezt a programot a `test` és a
`sample.txt` argumentumokkal:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Nagyszerű, a program működik! A szükséges argumentumok értékei a megfelelő
változókba kerülnek. Később hozzáadunk némi hibakezelést, hogy kezeljük az
esetleges hibás helyzeteket, például amikor a felhasználó egyáltalán nem ad meg
argumentumokat; egyelőre figyelmen kívül hagyjuk ezt a helyzetet, és inkább a
fájlbeolvasási képesség hozzáadásán dolgozunk.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths
