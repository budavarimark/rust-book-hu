## Példaprogram struct-okkal

Hogy megértsük, mikor érdemes struct-okat használnunk, írjunk egy programot,
amely kiszámítja egy téglalap területét. Először külön változókkal kezdjük,
majd addig alakítjuk át a programot, amíg struct-okat nem használunk helyettük.

Hozzunk létre a Cargóval egy új binary projektet _rectangles_ néven, amely
pixelben megadott szélességet és magasságot vesz át, és kiszámítja a téglalap
területét. Az 5-8. listában egy rövid program látható, amely pontosan ezt
teszi a projektünk _src/main.rs_ fájljában.

<Listing number="5-8" file-name="src/main.rs" caption="Téglalap területének kiszámítása külön szélesség- és magasságváltozókkal">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Most futtasd a programot a `cargo run` paranccsal:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Ez a kód sikeresen kiszámítja a téglalap területét úgy, hogy az `area`
függvényt hívja meg mindkét mérettel, de sokat tehetünk még azért, hogy a kód
világosabb és olvashatóbb legyen.

A kód problémája az `area` szignatúrájából derül ki:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Az `area` függvénynek egyetlen téglalap területét kellene kiszámítania, de a
megírt függvénynek két paramétere van, és a programunkban sehol nem derül ki,
hogy a paraméterek összetartoznak. Olvashatóbb és kezelhetőbb lenne a
szélességet és a magasságot egybefogni. Az egyik lehetséges módszert már
tárgyaltuk a 3. fejezet [„A tuple típus”][the-tuple-type]<!-- ignore -->
szakaszában: a tuple-ök használatát.

### Átalakítás tuple-ökkel

Az 5-9. listában a programunk egy másik változata látható, amely tuple-öket
használ.

<Listing number="5-9" file-name="src/main.rs" caption="A téglalap szélességének és magasságának megadása tuple-lel">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Egyfelől ez a program jobb. A tuple-ök segítségével kapunk némi szerkezetet, és
most már csak egyetlen argumentumot adunk át. Másfelől viszont ez a változat
kevésbé világos: a tuple-ök nem nevezik meg az elemeiket, ezért indexeléssel
kell elérnünk a tuple részeit, ami kevésbé teszi nyilvánvalóvá a számításunkat.

A szélesség és a magasság felcserélése a területszámításnál nem számítana, de
ha ki akarnánk rajzolni a téglalapot a képernyőre, már számítana! Fejben kellene
tartanunk, hogy a `width` a `0`-s, a `height` pedig az `1`-es tuple-index. Ezt
másvalakinek még nehezebb lenne kitalálnia és fejben tartania, ha használni
akarná a kódunkat. Mivel a kódunkban nem fejeztük ki az adataink jelentését,
mostantól könnyebben csúszik be hiba.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Átalakítás struct-okkal

A struct-okkal úgy adunk jelentést, hogy címkékkel látjuk el az adatokat. A
használt tuple-t átalakíthatjuk struct-tá, amelynek neve van, és a részei is
nevet kapnak, ahogy az 5-10. listában látható.

<Listing number="5-10" file-name="src/main.rs" caption="A `Rectangle` struct definiálása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Itt definiáltunk egy struct-ot, és a `Rectangle` nevet adtuk neki. A kapcsos
zárójeleken belül a `width` és a `height` mezőket definiáltuk, mindkettő `u32`
típusú. Ezután a `main`-ben létrehoztuk a `Rectangle` egy konkrét példányát,
amelynek szélessége `30`, magassága `50`.

Az `area` függvényünk most már egyetlen paraméterrel van definiálva, amelyet
`rectangle`-nek neveztünk el, és amelynek típusa egy `Rectangle` struct-példány
nem módosítható borrow-ja. Ahogy a 4. fejezetben említettük, a struct-ot
inkább borrow-olni akarjuk, mintsem átvenni az ownership-jét. Így a `main`
megtartja az ownership-et, és továbbra is használhatja a `rect1`-et; ezért
szerepel a `&` a függvény szignatúrájában és a függvényhívás helyén is.

Az `area` függvény a `Rectangle` példány `width` és `height` mezőit éri el
(vedd észre, hogy egy borrow-olt struct-példány mezőinek elérése nem move-olja
a mezők értékeit, ezért látsz gyakran struct-okra vonatkozó borrow-okat). Az
`area` szignatúrája most pontosan azt mondja ki, amit gondolunk: számítsd ki a
`Rectangle` területét a `width` és a `height` mezője alapján. Ez kifejezi, hogy
a szélesség és a magasság összetartozik, és beszédes neveket ad az értékeknek a
`0` és `1` tuple-indexek helyett. Ez egyértelmű nyereség az érthetőség
szempontjából.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Funkcionalitás hozzáadása derive-olt trait-ekkel

Hasznos lenne, ha a program hibakeresése közben ki tudnánk írni egy `Rectangle`
példányt, és látnánk az összes mezőjének értékét. Az 5-11. lista a
[`println!` makróval][println]<!-- ignore --> próbálkozik, ahogyan azt a
korábbi fejezetekben is tettük. Ez azonban nem fog működni.

<Listing number="5-11" file-name="src/main.rs" caption="Kísérlet egy `Rectangle` példány kiírására">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Amikor lefordítjuk ezt a kódot, a következő lényegi üzenetet tartalmazó hibát
kapjuk:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

A `println!` makró sokféle formázásra képes, és alapértelmezés szerint a kapcsos
zárójelek azt mondják a `println!`-nek, hogy a `Display` néven ismert formázást
használja: ez a közvetlenül a végfelhasználónak szánt kimenet. Az eddig látott
primitív típusok alapból implementálják a `Display`-t, mert egy `1`-est vagy
bármely más primitív típust csak egyféleképpen szeretnél megmutatni a
felhasználónak. A struct-oknál viszont kevésbé egyértelmű, hogyan formázza a
`println!` a kimenetet, mert több megjelenítési lehetőség is van: kellenek
vesszők vagy sem? Ki akarod íratni a kapcsos zárójeleket? Minden mező
látszódjon? E kétértelműség miatt a Rust nem próbálja kitalálni, mit akarunk,
és a struct-okhoz nincs kész `Display` implementáció, amit a `println!`-lel és
a `{}` helyőrzővel használhatnánk.

Ha tovább olvassuk a hibaüzeneteket, ezt a hasznos megjegyzést találjuk:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Próbáljuk ki! A `println!` makróhívás most így fog kinézni: `println!("rect1 is
{rect1:?}");`. A kapcsos zárójeleken belülre tett `:?` specifikátor azt mondja
a `println!`-nek, hogy a `Debug` nevű kimeneti formátumot szeretnénk használni.
A `Debug` trait lehetővé teszi, hogy a struct-unkat a fejlesztők számára
hasznos módon írjuk ki, így a kód hibakeresése közben láthatjuk az értékét.

Fordítsd le a kódot ezzel a változtatással. A csudába! Még mindig hibát kapunk:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

De a fordító megint hasznos megjegyzést ad:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

A Rust _tartalmaz_ olyan képességet, amellyel hibakeresési információt lehet
kiírni, de kifejezetten kérnünk kell, hogy ez a képesség elérhető legyen a
struct-unk számára. Ehhez a `#[derive(Debug)]` külső attribútumot tesszük
közvetlenül a struct definíciója elé, ahogy az 5-12. listában látható.

<Listing number="5-12" file-name="src/main.rs" caption="A `Debug` trait derive-olását kérő attribútum hozzáadása és a `Rectangle` példány kiírása debug formázással">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Ha most futtatjuk a programot, nem kapunk hibát, és a következő kimenetet
látjuk:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Remek! Nem ez a legszebb kimenet, de megmutatja a példány összes mezőjének
értékét, ami hibakeresés közben mindenképpen segít. Nagyobb struct-oknál
hasznos, ha a kimenet kicsit könnyebben olvasható; ilyenkor a `println!`
sztringben a `{:?}` helyett a `{:#?}` alakot használhatjuk. Ebben a példában a
`{:#?}` stílus a következőt írja ki:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Egy érték `Debug` formátumú kiírásának másik módja a [`dbg!`
makró][dbg]<!-- ignore -->, amely átveszi egy kifejezés ownership-jét (szemben
a `println!`-lel, amely referenciát vesz át), kiírja annak a fájlnak a nevét és
sorszámát, ahol az a `dbg!` makróhívás a kódodban szerepel, a kifejezés
eredményével együtt, majd visszaadja az érték ownership-jét.

> Megjegyzés: a `dbg!` makró hívása a standard hibakimenetre (`stderr`) ír,
> szemben a `println!`-lel, amely a standard kimenetre (`stdout`) ír. A
> `stderr`-ről és a `stdout`-ról bővebben a 12. fejezet [„Hibák átirányítása a
> standard hibakimenetre”][err]<!-- ignore --> szakaszában lesz szó.

Íme egy példa, amelyben a `width` mezőhöz rendelt érték, valamint a `rect1`-ben
lévő teljes struct értéke érdekel minket:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

A `dbg!`-t rátehetjük a `30 * scale` kifejezésre, és mivel a `dbg!` visszaadja
a kifejezés értékének ownership-jét, a `width` mező ugyanazt az értéket kapja,
mintha nem lenne ott a `dbg!` hívás. Azt nem szeretnénk, hogy a `dbg!` átvegye
a `rect1` ownership-jét, ezért a következő hívásban a `rect1` egy referenciáját
használjuk. Így néz ki ennek a példának a kimenete:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Látható, hogy a kimenet első része a _src/main.rs_ 10. sorából származik, ahol
a `30 * scale` kifejezést vizsgáljuk, és az eredménye `60` (az egészekre
implementált `Debug` formázás csak az értéküket írja ki). A _src/main.rs_ 14.
sorában lévő `dbg!` hívás a `&rect1` értékét írja ki, ami a `Rectangle` struct.
Ez a kimenet a `Rectangle` típus szép `Debug` formázását használja. A `dbg!`
makró nagyon hasznos tud lenni, amikor azt próbálod kideríteni, mit is csinál
a kódod!

A `Debug` trait mellett a Rust számos további trait-et biztosít, amelyeket a
`derive` attribútummal használhatunk, és amelyek hasznos viselkedést adnak a
saját típusainkhoz. Ezeket a trait-eket és a viselkedésüket a [C
függelék][app-c]<!-- ignore --> sorolja fel. A 10. fejezetben lesz szó arról,
hogyan implementálhatod ezeket a trait-eket saját viselkedéssel, és hogyan
hozhatsz létre saját trait-eket. A `derive`-on kívül sok más attribútum is van;
további információért lásd a Rust Reference [„Attributes”
szakaszát][attributes].

Az `area` függvényünk nagyon speciális: kizárólag téglalapok területét számítja
ki. Hasznos lenne, ha ezt a viselkedést szorosabban a `Rectangle` struct-unkhoz
kötnénk, mivel semmilyen más típussal nem működik. Nézzük meg, hogyan
alakíthatjuk tovább ezt a kódot úgy, hogy az `area` függvényből a `Rectangle`
típusunkon definiált `area` metódus legyen.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
