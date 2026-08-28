## Tömör vezérlés az `if let` és a `let...else` szerkezettel

Az `if let` szintaxis lehetővé teszi, hogy az `if`-et és a `let`-et
összevonva kevésbé bőbeszédű módon kezeld az egyetlen mintára illeszkedő
értékeket, a többit pedig figyelmen kívül hagyd. Nézd meg a 6-6. listában
látható programot, amely a `config_max` változóban lévő `Option<u8>` értékre
illeszt, de csak akkor akar kódot futtatni, ha az érték a `Some` variáns.

<Listing number="6-6" caption="Egy `match`, amelyet csak az érdekel, hogy kódot futtasson, ha az érték `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Ha az érték `Some`, kiírjuk a `Some` variánsban lévő értéket úgy, hogy a
mintában hozzákötjük az értéket a `max` változóhoz. A `None` értékkel nem
akarunk semmit sem kezdeni. Hogy a `match` kifejezésnek eleget tegyünk, egyetlen
variáns feldolgozása után hozzá kell adnunk a `_ => ()` ágat, ami bosszantó,
felesleges sablonkód.

Ehelyett rövidebben is megírhatjuk ezt `if let` segítségével. A következő kód
ugyanúgy viselkedik, mint a 6-6. listában lévő `match`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Az `if let` szintaxis egy mintát és egy kifejezést vár, egyenlőségjellel
elválasztva. Ugyanúgy működik, mint egy `match`, ahol a kifejezést a `match`
kapja meg, a minta pedig az első ága. Ebben az esetben a minta a `Some(max)`, a
`max` pedig a `Some`-ban lévő értékhez kötődik. Ezután az `if let` blokk
törzsében ugyanúgy használhatjuk a `max` változót, ahogyan a neki megfelelő
`match`-ágban használtuk. Az `if let` blokkban lévő kód csak akkor fut le, ha az
érték illeszkedik a mintára.

Az `if let` használatával kevesebbet kell gépelni, kevesebb a behúzás és
kevesebb a sablonkód. Cserébe viszont elveszíted azt a kimerítő ellenőrzést,
amelyet a `match` kényszerít ki, és amely biztosítja, hogy egyetlen esetet se
felejts el kezelni. A `match` és az `if let` közötti választás attól függ, mit
csinálsz az adott helyzetben, és hogy a tömörség megéri-e a kimerítő ellenőrzés
elvesztését.

Más szóval úgy gondolhatsz az `if let`-re, mint egy olyan `match` szintaktikai
cukorkájára, amely akkor futtat kódot, ha az érték egy adott mintára
illeszkedik, majd minden más értéket figyelmen kívül hagy.

Az `if let` mellé `else` ágat is tehetünk. Az `else`-hez tartozó kódblokk
ugyanaz, mint az a kódblokk, amely az `if let`-tel és `else`-szel egyenértékű
`match` kifejezés `_` ágához tartozna. Emlékezz vissza a `Coin` enum 6-4.
listában lévő definíciójára, ahol a `Quarter` variáns egy `UsState` értéket is
tárolt. Ha meg akarnánk számolni az összes látott, nem negyeddolláros érmét, és
közben be is akarnánk mondani a negyeddollárosok államát, ezt megtehetnénk egy
`match` kifejezéssel, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Vagy használhatnánk egy `if let` és `else` kifejezést, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Maradjunk a „boldog úton” a `let...else` szerkezettel

Gyakori minta, hogy elvégzünk valamilyen számítást, ha van érték, egyébként
pedig egy alapértelmezett értéket adunk vissza. Folytatva a `UsState` értéket
tartalmazó érmés példánkat: ha valami vicceset szeretnénk mondani annak
függvényében, hogy milyen régi a negyeddollároson szereplő állam, bevezethetünk
egy metódust az `UsState`-en, amely megnézi egy állam korát, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Ezután `if let`-tel illeszthetünk az érme típusára, és bevezethetünk egy `state`
változót a feltétel törzsében, ahogy a 6-7. listában látható.

<Listing number="6-7" caption="Annak ellenőrzése, hogy egy állam létezett-e 1900-ban, egy `if let`-be ágyazott feltételekkel">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Ez megoldja a feladatot, de a munkát az `if let` utasítás törzsébe tolta, és ha
az elvégzendő munka bonyolultabb, nehéz lehet pontosan követni, hogyan
viszonyulnak egymáshoz a legfelső szintű ágak. Kihasználhatnánk azt is, hogy a
kifejezéseknek van értékük, és vagy előállítjuk a `state`-et az `if let`-ből,
vagy korán visszatérünk, ahogy a 6-8. listában. (Valami hasonlót `match`-csel
is csinálhatnál.)

<Listing number="6-8" caption="Az `if let` használata érték előállítására vagy korai visszatérésre">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Ezt viszont a maga módján kicsit bosszantó követni! Az `if let` egyik ága
értéket állít elő, a másik pedig teljesen kilép a függvényből.

Hogy ezt a gyakori mintát szebben lehessen kifejezni, a Rustban van
`let...else`. A `let...else` szintaxis a bal oldalon egy mintát, a jobb oldalon
egy kifejezést vár, nagyon hasonlóan az `if let`-hez, de nincs `if` ága, csak
`else` ága. Ha a minta illeszkedik, a mintából származó értéket a külső
hatókörben köti hozzá. Ha a minta _nem_ illeszkedik, a program az `else` ágra
kerül, amelynek vissza kell térnie a függvényből.

A 6-9. listában láthatod, hogyan néz ki a 6-8. lista, ha az `if let` helyett
`let...else` szerkezetet használunk.

<Listing number="6-9" caption="A `let...else` használata a függvényen belüli folyamat áttekinthetőbbé tételére">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Vedd észre, hogy így a függvény fő törzsében végig a „boldog úton” maradunk,
anélkül hogy két ág között jelentősen eltérő vezérlési folyam alakulna ki, ahogy
az `if let` esetében történt.

Ha olyan helyzetbe kerülsz, amelyben a programod logikája túl bőbeszédű ahhoz,
hogy `match`-csel fejezd ki, ne feledd, hogy az `if let` és a `let...else` is a
Rust-eszköztáradban van.

## Összefoglalás

Áttekintettük, hogyan használhatók az enumok arra, hogy olyan egyéni típusokat
hozzunk létre, amelyek egy felsorolt értékkészlet valamelyik elemét vehetik fel.
Megmutattuk, hogyan segít a standard könyvtár `Option<T>` típusa abban, hogy a
típusrendszert hibák megelőzésére használd. Amikor az enum értékei adatot is
tartalmaznak, a `match` vagy az `if let` segítségével nyerheted ki és
használhatod ezeket az értékeket, attól függően, hány esetet kell kezelned.

A Rust-programjaid mostantól struct-ok és enumok segítségével tudják kifejezni a
szakterületed fogalmait. Ha egyéni típusokat hozol létre az API-dhoz, azzal
típusbiztonságot biztosítasz: a fordító gondoskodik arról, hogy a függvényeid
csak olyan típusú értékeket kapjanak, amilyet az adott függvény elvár.

Ahhoz, hogy jól szervezett, egyszerűen használható API-t adhass a
felhasználóidnak, amely pontosan csak azt teszi közzé, amire szükségük lesz,
most forduljunk a Rust moduljai felé.
