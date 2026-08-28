## Fájl beolvasása

Most hozzáadjuk azt a képességet, hogy beolvassuk a `file_path` argumentumban
megadott fájlt. Először szükségünk van egy mintafájlra, amellyel kipróbálhatjuk:
olyan fájlt használunk, amely több soron át kevés szöveget tartalmaz, benne
néhány ismétlődő szóval. A 12-3. listában egy Emily Dickinson-vers szerepel,
amely tökéletesen megfelel erre! Hozz létre egy _poem.txt_ nevű fájlt a
projekted gyökerében, és írd bele az „I’m Nobody! Who are you?” című verset.

<Listing number="12-3" file-name="poem.txt" caption="Egy Emily Dickinson-vers jó tesztesetnek bizonyul.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Ha a szöveg a helyén van, szerkeszd az _src/main.rs_ fájlt, és add hozzá a fájl
beolvasásához szükséges kódot, ahogy a 12-4. listában látható.

<Listing number="12-4" file-name="src/main.rs" caption="A második argumentumban megadott fájl tartalmának beolvasása">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Először egy `use` utasítással behozzuk a standard könyvtár egy fontos részét: a
fájlok kezeléséhez a `std::fs` modulra van szükségünk.

A `main` függvényben az új `fs::read_to_string` utasítás fogadja a `file_path`
értéket, megnyitja az adott fájlt, és egy `std::io::Result<String>` típusú
értéket ad vissza, amely a fájl tartalmát hordozza.

Ezután ismét hozzáadunk egy ideiglenes `println!` utasítást, amely a fájl
beolvasása után kiírja a `contents` értékét, hogy ellenőrizhessük: a program
eddig működik.

Futtassuk le ezt a kódot tetszőleges karakterlánccal első parancssori
argumentumként (mert a keresést végző részt még nem valósítottuk meg), és a
_poem.txt_ fájllal második argumentumként:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Nagyszerű! A kód beolvasta, majd kiírta a fájl tartalmát. A kódnak azonban van
néhány gyengéje. Pillanatnyilag a `main` függvénynek több felelőssége is van:
általánosságban a függvények világosabbak és könnyebben karbantarthatók, ha
mindegyik függvény csak egyetlen dologért felel. A másik gond az, hogy nem
kezeljük olyan jól a hibákat, ahogyan lehetne. A program még kicsi, így ezek a
gyengék nem jelentenek nagy problémát, de ahogy a program növekszik, egyre
nehezebb lesz tisztán kijavítani őket. Jó gyakorlat, ha egy program
fejlesztésekor korán elkezdjük a refaktorálást, mert kisebb mennyiségű kódot
sokkal könnyebb refaktorálni. A következőkben ezt tesszük.
