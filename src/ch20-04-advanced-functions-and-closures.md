## Haladó függvények és closure-ök

Ez a szakasz néhány haladó, függvényekhez és closure-ökhöz kapcsolódó képességet
mutat be, köztük a függvénypointereket és a closure-ök visszaadását.

### Függvénypointerek

Már beszéltünk arról, hogyan adhatunk át closure-öket függvényeknek; hasonlóan
átadhatsz közönséges függvényeket is függvényeknek! Ez a technika akkor
hasznos, ha egy már definiált függvényt szeretnél átadni, ahelyett hogy új
closure-t írnál. A függvények az `fn` típussá kényszerülnek (kisbetűs _f_-fel),
amit nem szabad összekeverni az `Fn` closure trait-tel. Az `fn` típus neve
_függvénypointer_. Ha függvénypointerekkel adsz át függvényeket, azzal más
függvények argumentumaként használhatod a függvényeket.

Annak jelölése, hogy egy paraméter függvénypointer, a closure-ökéhez hasonló
szintaxissal történik, ahogy azt a 20-28. lista mutatja: itt definiáltunk egy
`add_one` függvényt, amely 1-et ad a paraméteréhez. A `do_twice` függvény két
paramétert vár: egy függvénypointert bármely olyan függvényre, amely `i32`
paramétert kap és `i32` értéket ad vissza, valamint egy `i32` értéket. A
`do_twice` függvény kétszer meghívja az `f` függvényt az `arg` értékkel, majd
összeadja a két függvényhívás eredményét. A `main` függvény az `add_one` és az
`5` argumentumokkal hívja meg a `do_twice`-t.

<Listing number="20-28" file-name="src/main.rs" caption="Az `fn` típus használata függvénypointer argumentumként való fogadásához">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Ez a kód a `The answer is: 12` szöveget írja ki. Megadjuk, hogy a `do_twice`
`f` paramétere olyan `fn`, amely egy `i32` típusú paramétert vár és `i32`
értéket ad vissza. Ezután a `do_twice` törzsében meghívhatjuk az `f`-et. A
`main`-ben az `add_one` függvénynevet adhatjuk át a `do_twice` első
argumentumaként.

A closure-ökkel ellentétben az `fn` típus, nem trait, ezért közvetlenül az
`fn`-t adjuk meg paramétertípusként, ahelyett hogy generikus típusparamétert
deklarálnánk valamelyik `Fn` trait-tel mint trait bound-dal.

A függvénypointerek mindhárom closure trait-et implementálják (`Fn`, `FnMut` és
`FnOnce`), ami azt jelenti, hogy mindig átadhatsz függvénypointert
argumentumként egy closure-t váró függvénynek. A legjobb, ha a függvényeidet
generikus típussal és valamelyik closure trait-tel írod meg, hogy függvényeket
és closure-öket egyaránt fogadhassanak.

Ennek ellenére van olyan eset, amikor kizárólag `fn`-t akarsz elfogadni,
closure-t nem: amikor olyan külső kóddal érintkezel, amely nem ismeri a
closure-öket. A C függvények képesek függvényeket fogadni argumentumként, de a
C-ben nincsenek closure-ök.

Példaként arra, hogy hol használhatnál akár helyben definiált closure-t, akár
elnevezett függvényt, nézzük meg a standard könyvtár `Iterator` trait-je által
biztosított `map` metódus egy alkalmazását. Ha a `map` metódussal számok
vektorát akarjuk sztringek vektorává alakítani, használhatunk closure-t, ahogy
a 20-29. listában látható.

<Listing number="20-29" caption="Closure használata a `map` metódussal számok sztringgé alakítására">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

De a closure helyett meg is nevezhetünk egy függvényt a `map` argumentumaként.
A 20-30. lista mutatja, hogy ez hogyan nézne ki.

<Listing number="20-30" caption="A `String::to_string` függvény használata a `map` metódussal számok sztringgé alakítására">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Vedd észre, hogy a [„Haladó trait-ek”][advanced-traits]<!-- ignore --> című
szakaszban tárgyalt teljesen minősített szintaxist kell használnunk, mert több
`to_string` nevű függvény is elérhető.

Itt a `ToString` trait-ben definiált `to_string` függvényt használjuk, amelyet
a standard könyvtár minden olyan típusra implementált, amely implementálja a
`Display` trait-et.

A 6. fejezet [„Enum-értékek”][enum-values]<!-- ignore --> című szakaszából
emlékezhetsz rá, hogy minden általunk definiált enum-változat neve
inicializáló függvénnyé is válik. Ezeket az inicializáló függvényeket
használhatjuk olyan függvénypointerekként, amelyek implementálják a closure
trait-eket, ami azt jelenti, hogy megadhatjuk őket argumentumként closure-t
váró metódusoknak, ahogy a 20-31. listában látható.

<Listing number="20-31" caption="Enum-inicializáló használata a `map` metódussal `Status` példányok létrehozására számokból">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Itt `Status::Value` példányokat hozunk létre annak a tartománynak minden `u32`
értékéből, amelyen a `map`-et meghívjuk, mégpedig a `Status::Value`
inicializáló függvényével. Egyesek ezt a stílust kedvelik, mások a closure-öket
használják szívesebben. Ugyanarra a kódra fordulnak, úgyhogy azt a stílust
válaszd, amelyik számodra érthetőbb.

### Closure-ök visszaadása

A closure-öket trait-ek reprezentálják, ami azt jelenti, hogy közvetlenül nem
adhatsz vissza closure-t. A legtöbb olyan esetben, amikor trait-et adnál
vissza, helyette a trait-et implementáló konkrét típust használhatod a függvény
visszatérési értékeként. A closure-öknél viszont ezt általában nem teheted meg,
mert nincs visszaadható konkrét típusuk; például az `fn` függvénypointert sem
használhatod visszatérési típusként, ha a closure bármilyen értéket befog a
hatóköréből.

Helyette rendszerint a 10. fejezetben megismert `impl Trait` szintaxist fogod
használni. Bármilyen függvénytípust visszaadhatsz az `Fn`, `FnOnce` és `FnMut`
trait-ekkel. Például a 20-32. lista kódja gond nélkül lefordul.

<Listing number="20-32" caption="Closure visszaadása függvényből az `impl Trait` szintaxissal">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Ahogy azonban a 13. fejezet [„Closure-típusok kikövetkeztetése és
annotálása”][closure-types]<!-- ignore --> című szakaszában megjegyeztük,
minden closure önálló, saját típus is egyben. Ha több olyan függvénnyel kell
dolgoznod, amelyeknek azonos a szignatúrájuk, de eltérő az implementációjuk,
trait objectet kell használnod hozzájuk. Nézzük meg, mi történik, ha a 20-33.
listában látható kódot írod.

<Listing file-name="src/main.rs" number="20-33" caption="Closure-ök `Vec<T>` gyűjteményének létrehozása `impl Fn` típust visszaadó függvényekkel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Itt két függvényünk van, a `returns_closure` és a
`returns_initialized_closure`, amelyek mindketten `impl Fn(i32) -> i32` értéket
adnak vissza. Vedd észre, hogy az általuk visszaadott closure-ök különbözőek,
noha ugyanazt a típust implementálják. Ha megpróbáljuk lefordítani, a Rust
tudatja velünk, hogy ez nem fog működni:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

A hibaüzenet elárulja, hogy valahányszor `impl Trait` értéket adunk vissza, a
Rust egyedi _átlátszatlan típust_ (opaque type) hoz létre: olyan típust,
amelynek nem látunk bele a részleteibe — sem abba, amit a Rust felépít
nekünk, sem abba, hogy milyen típust fog generálni, hogy azt magunk írhassuk
le. Így hiába adnak vissza ezek a függvények ugyanazt a trait-et, az
`Fn(i32) -> i32`-t implementáló closure-öket, a Rust által mindegyikhez
generált átlátszatlan típus más és más. (Ez hasonlít ahhoz, ahogyan a Rust
különböző konkrét típusokat állít elő a különböző async blokkokhoz még akkor
is, ha azonos a kimeneti típusuk, ahogy azt a 17. fejezet [„A `Pin` típus és az
`Unpin` trait”][future-types]<!-- ignore --> című szakaszában láttuk.) A
megoldást erre a problémára már többször láttuk: használhatunk trait objectet,
ahogy a 20-34. listában.

<Listing number="20-34" caption="Closure-ök `Vec<T>` gyűjteményének létrehozása `Box<dyn Fn>` értéket visszaadó függvényekkel, hogy azonos típusúak legyenek">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Ez a kód gond nélkül lefordul. A trait objectekről bővebben a 18. fejezet
[„Trait objectek használata a közös viselkedés
absztrahálására”][trait-objects]<!-- ignore --> című szakaszában olvashatsz.

Következőnek nézzük meg a makrókat!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
