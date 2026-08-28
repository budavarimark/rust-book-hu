## Kód futtatása takarításkor a `Drop` trait-tel

A smart pointer mintában a második fontos trait a `Drop`, amellyel testre
szabhatod, mi történjen akkor, amikor egy érték épp kilép a hatóköréből. A
`Drop` trait-et bármilyen típusra implementálhatod, és az így megadott kód
alkalmas erőforrások – például fájlok vagy hálózati kapcsolatok –
felszabadítására.

Azért a smart pointerek kapcsán mutatjuk be a `Drop` trait-et, mert a
funkcionalitására szinte mindig szükség van, amikor smart pointert
implementálunk. Amikor például egy `Box<T>` megsemmisül, felszabadítja azt a
heapen lévő területet, amelyre a box mutat.

Néhány nyelvben bizonyos típusoknál a programozónak minden alkalommal meg kell
hívnia a memóriát vagy az erőforrásokat felszabadító kódot, amikor befejezte az
adott típus egy példányának használatát. Ilyen például a fájlkezelő (file
handle), a socket és a lock. Ha a programozó elfelejti ezt megtenni, a rendszer
túlterhelődhet és összeomolhat. Rustban megadhatod, hogy egy adott kódrészlet
lefusson, valahányszor egy érték kilép a hatóköréből, és a fordító automatikusan
beszúrja ezt a kódot. Ennek eredményeként nem kell gondosan ügyelned arra, hogy
a program minden olyan pontján elhelyezd a takarítókódot, ahol egy adott típus
példányával végeztél – mégsem szivárogtatsz el erőforrásokat!

Azt, hogy milyen kód fusson le, amikor egy érték kilép a hatóköréből, a `Drop`
trait implementálásával adod meg. A `Drop` trait egyetlen, `drop` nevű metódus
implementálását követeli meg, amely egy módosítható referenciát vesz át a
`self`-re. Hogy lássuk, mikor hívja meg a Rust a `drop`-ot, egyelőre `println!`
utasításokkal implementáljuk.

A 15-14. listában egy `CustomSmartPointer` struct látható, amelynek egyetlen
egyedi funkciója az, hogy kiírja a `Dropping CustomSmartPointer!` szöveget,
amikor a példány kilép a hatóköréből – így megmutatja, mikor futtatja a Rust a
`drop` metódust.

<Listing number="15-14" file-name="src/main.rs" caption="Egy `CustomSmartPointer` struct, amely implementálja a `Drop` trait-et, ahová a takarítókódunk kerülne">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

A `Drop` trait benne van a preludeban, ezért nem kell külön behoznunk a
hatókörbe. A `Drop` trait-et a `CustomSmartPointer`-re implementáljuk, és a
`drop` metódushoz olyan implementációt adunk, amely meghívja a `println!`-t. A
`drop` metódus törzsébe kerül minden olyan logika, amelyet akkor szeretnél
futtatni, amikor a típusod egy példánya kilép a hatóköréből. Itt most szöveget
írunk ki, hogy szemléletesen bemutassuk, mikor hívja meg a Rust a `drop`-ot.

A `main`-ben létrehozzuk a `CustomSmartPointer` két példányát, majd kiírjuk a
`CustomSmartPointers created` szöveget. A `main` végén a `CustomSmartPointer`
példányaink kilépnek a hatókörükből, és a Rust meghívja a `drop` metódusba tett
kódunkat, kiírva a záró üzenetünket. Vedd észre, hogy nem kellett explicit
módon meghívnunk a `drop` metódust.

Ha lefuttatjuk ezt a programot, a következő kimenetet látjuk:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

A Rust automatikusan meghívta helyettünk a `drop`-ot, amikor a példányaink
kiléptek a hatókörükből, így lefuttatta az általunk megadott kódot. A változók a
létrehozásukkal ellentétes sorrendben semmisülnek meg, ezért `d` előbb
semmisült meg, mint `c`. Ennek a példának az a célja, hogy szemléletes képet
adjon a `drop` metódus működéséről; a valóságban általában a típusod számára
szükséges takarítókódot adnád meg egy kiírt üzenet helyett.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Sajnos az automatikus `drop` funkcionalitást nem lehet egyszerűen kikapcsolni.
A `drop` letiltására általában nincs is szükség; a `Drop` trait lényege épp az,
hogy mindez automatikusan történik. Időnként azonban előfordulhat, hogy egy
értéket korábban szeretnél megtisztítani. Erre példa a lockokat kezelő smart
pointerek használata: elképzelhető, hogy ki akarod kényszeríteni a lockot
felszabadító `drop` metódus futását, hogy ugyanabban a hatókörben lévő másik
kód megszerezhesse a lockot. A Rust nem engedi, hogy kézzel meghívd a `Drop`
trait `drop` metódusát; helyette a standard könyvtár által biztosított
`std::mem::drop` függvényt kell meghívnod, ha egy értéket a hatóköre vége előtt
akarsz megsemmisíteni.

Ha úgy próbáljuk kézzel meghívni a `Drop` trait `drop` metódusát, hogy
módosítjuk a 15-14. lista `main` függvényét, az nem fog működni – ezt mutatja a
15-15. lista.

<Listing number="15-15" file-name="src/main.rs" caption="Kísérlet a `Drop` trait `drop` metódusának kézi meghívására a korai takarítás érdekében">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Amikor megpróbáljuk lefordítani ezt a kódot, a következő hibát kapjuk:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Ez a hibaüzenet azt mondja, hogy nem hívhatjuk meg explicit módon a `drop`-ot.
A hibaüzenet a _destructor_ kifejezést használja, ami az általános programozási
elnevezése annak a függvénynek, amely megtisztít egy példányt. A _destructor_ a
_constructor_ megfelelője, amely létrehoz egy példányt. A Rustban a `drop`
függvény egy konkrét destructor.

A Rust azért nem engedi, hogy explicit módon meghívjuk a `drop`-ot, mert a
`main` végén akkor is automatikusan meghívná a `drop`-ot az értékre. Ez kettős
felszabadítási (double free) hibát okozna, mert a Rust ugyanazt az értéket
kétszer próbálná megtisztítani.

Nem tudjuk kikapcsolni a `drop` automatikus beszúrását, amikor egy érték kilép
a hatóköréből, és nem hívhatjuk meg explicit módon a `drop` metódust sem. Ha
tehát ki kell kényszerítenünk egy érték korai megtisztítását, a
`std::mem::drop` függvényt használjuk.

A `std::mem::drop` függvény különbözik a `Drop` trait `drop` metódusától. Úgy
hívjuk meg, hogy argumentumként átadjuk neki azt az értéket, amelynek a
megsemmisítését ki akarjuk kényszeríteni. A függvény benne van a preludeban,
így a 15-15. lista `main`-jét módosíthatjuk úgy, hogy meghívja a `drop`
függvényt, ahogy azt a 15-16. lista mutatja.

<Listing number="15-16" file-name="src/main.rs" caption="A `std::mem::drop` meghívása egy érték explicit megsemmisítésére, mielőtt kilépne a hatóköréből">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Ennek a kódnak a futtatása a következőt írja ki:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

A ``Dropping CustomSmartPointer with data `some data`!`` szöveg a
`CustomSmartPointer created` és a `CustomSmartPointer dropped before the end of
main` szövegek között jelenik meg, ami azt mutatja, hogy a `drop` metódus kódja
ezen a ponton fut le `c` megsemmisítéséhez.

A `Drop` trait implementációjában megadott kódot sokféleképpen használhatod
arra, hogy a takarítás kényelmes és biztonságos legyen: például akár saját
memóriafoglalót is készíthetsz vele! A `Drop` trait-tel és a Rust
ownership-rendszerével nem kell emlékezned a takarításra, mert a Rust
automatikusan elvégzi.

Amiatt sem kell aggódnod, hogy a még használatban lévő értékek véletlen
megtisztításából problémák adódnának: ugyanaz az ownership-rendszer, amely
gondoskodik a referenciák érvényességéről, azt is biztosítja, hogy a `drop`
csak egyszer hívódjon meg, akkor, amikor az értéket már nem használjuk.

Most, hogy megvizsgáltuk a `Box<T>`-t és a smart pointerek néhány jellemzőjét,
nézzünk meg néhány további smart pointert a standard könyvtárból.
