## Cáfolhatóság: illeszkedhet-e egy minta sikertelenül

A minták két formában léteznek: cáfolhatók és cáfolhatatlanok. Azok a minták,
amelyek minden lehetséges átadott értékre illeszkednek, _cáfolhatatlanok_. Ilyen
például az `x` a `let x = 5;` utasításban, mert az `x` bármire illeszkedik, így
az illesztése nem hiúsulhat meg. Azok a minták, amelyek bizonyos lehetséges
értékekre nem illeszkednek, _cáfolhatók_. Ilyen például a `Some(x)` az `if let
Some(x) = a_value` kifejezésben, mert ha az `a_value` változóban lévő érték
`Some` helyett `None`, a `Some(x)` minta nem fog illeszkedni.

A függvényparaméterek, a `let` utasítások és a `for` ciklusok csak cáfolhatatlan
mintákat fogadnak el, mert a program nem tud semmi értelmeset kezdeni azzal, ha
az értékek nem illeszkednek. Az `if let` és a `while let` kifejezés, valamint a
`let...else` utasítás cáfolható és cáfolhatatlan mintákat is elfogad, de a
fordító figyelmeztet a cáfolhatatlan mintákra, hiszen ezek a szerkezetek
definíció szerint a lehetséges sikertelenség kezelésére valók: egy feltételes
szerkezet lényege éppen az, hogy sikertől vagy sikertelenségtől függően másképp
viselkedik.

Általánosságban nem kell sokat foglalkoznod a cáfolható és cáfolhatatlan minták
közötti különbséggel; a cáfolhatóság fogalmát azonban ismerned kell, hogy tudj
reagálni, ha egy hibaüzenetben találkozol vele. Ilyenkor a kód szándékolt
viselkedésétől függően vagy a mintát, vagy azt a szerkezetet kell
megváltoztatnod, amelyben a mintát használod.

Nézzünk meg egy példát arra, mi történik, amikor cáfolható mintát próbálunk
használni ott, ahol a Rust cáfolhatatlant vár, és fordítva. A 19-8. lista egy
`let` utasítást mutat be, amelyben mintaként a `Some(x)`-et adtuk meg, ami
cáfolható minta. Ahogy sejtheted, ez a kód nem fordul le.

<Listing number="19-8" caption="Cáfolható minta használatának kísérlete `let`-tel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Ha a `some_option_value` értéke `None` lenne, nem illeszkedne a `Some(x)`
mintára, vagyis a minta cáfolható. A `let` utasítás azonban csak cáfolhatatlan
mintát fogad el, mert a kód semmi érvényeset nem tud kezdeni egy `None`
értékkel. Fordítási időben a Rust panaszkodni fog, hogy cáfolható mintát
próbáltunk használni ott, ahol cáfolhatatlan szükséges:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Mivel a `Some(x)` mintával nem fedtünk le (és nem is fedhettünk le!) minden
érvényes értéket, a Rust joggal jelez fordítási hibát.

Ha cáfolható mintánk van ott, ahol cáfolhatatlanra van szükség, a hibát a mintát
használó kód megváltoztatásával orvosolhatjuk: `let` helyett használhatunk
`let...else`-t. Ekkor, ha a minta nem illeszkedik, a kapcsos zárójelek közötti
kód kezeli az értéket. A 19-9. lista bemutatja, hogyan javítható a 19-8.
listában szereplő kód.

<Listing number="19-9" caption="`let...else` és egy blokk használata cáfolható mintákkal a `let` helyett">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Adtunk a kódnak egy kiutat! Ez a kód teljesen érvényes, ugyanakkor azt is
jelenti, hogy cáfolhatatlan mintát nem használhatunk figyelmeztetés nélkül. Ha a
`let...else` szerkezetnek olyan mintát adunk, amely mindig illeszkedik – például
`x`-et, ahogy a 19-10. listában látható –, a fordító figyelmeztetést ad.

<Listing number="19-10" caption="Cáfolhatatlan minta használatának kísérlete `let...else`-szel">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

A Rust azt kifogásolja, hogy nincs értelme cáfolhatatlan mintával használni a
`let...else` szerkezetet, mert az `else` ág soha nem fut le:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Emiatt a `match`-ágaknak cáfolható mintákat kell használniuk, kivéve az utolsó
ágat, amelynek egy cáfolhatatlan mintával kell illeszkednie az összes megmaradt
értékre. A Rust megengedi, hogy egyetlen ágból álló `match`-ben cáfolhatatlan
mintát használjunk, de ez a szintaxis nem különösebben hasznos, és kiváltható
egy egyszerűbb `let` utasítással.

Most, hogy tudod, hol használhatsz mintákat, és mi a különbség a cáfolható és a
cáfolhatatlan minták között, vegyük sorra az összes szintaxist, amellyel
mintákat hozhatunk létre.
