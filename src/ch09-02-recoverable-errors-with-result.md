## Helyrehozható hibák a `Result` típussal

A legtöbb hiba nem elég súlyos ahhoz, hogy a program teljes leállítását
követelje. Néha, amikor egy függvény hibázik, annak olyan oka van, amelyet
könnyen értelmezni tudsz, és reagálni tudsz rá. Ha például megpróbálsz megnyitni
egy fájlt, és a művelet azért nem sikerül, mert a fájl nem létezik, akkor lehet,
hogy a folyamat leállítása helyett inkább létre akarod hozni a fájlt.

Emlékezz vissza a 2. fejezet [„Lehetséges hibák kezelése a `Result`
segítségével”][handle_failure]<!-- ignore --> szakaszára: a `Result` enum két
varianssal van definiálva, ezek az `Ok` és az `Err`, az alábbi módon:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

A `T` és az `E` generikus típusparaméterek: a generikusokat a 10. fejezetben
tárgyaljuk részletesebben. Most annyit kell tudnod, hogy a `T` annak az értéknek
a típusát képviseli, amelyet siker esetén az `Ok` variánsban kapunk vissza, az
`E` pedig annak a hibának a típusát, amelyet hiba esetén az `Err` variánsban
kapunk vissza. Mivel a `Result` rendelkezik ezekkel a generikus
típusparaméterekkel, a `Result` típust és a rajta definiált függvényeket sokféle
különböző helyzetben használhatjuk, ahol a visszaadni kívánt siker- és hibaérték
eltérő lehet.

Hívjunk meg egy olyan függvényt, amely `Result` értéket ad vissza, mert a
függvény hibázhat. A 9-3. listában megpróbálunk megnyitni egy fájlt.

<Listing number="9-3" file-name="src/main.rs" caption="Fájl megnyitása">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

A `File::open` visszatérési típusa egy `Result<T, E>`. A `T` generikus
paramétert a `File::open` implementációja a sikeres érték típusával töltötte ki,
ez a `std::fs::File`, ami egy fájlleíró. A hibaértékben használt `E` típusa a
`std::io::Error`. Ez a visszatérési típus azt jelenti, hogy a `File::open`
hívása sikerülhet, és visszaadhat egy fájlleírót, amelyből olvashatunk vagy
amelybe írhatunk. A függvényhívás azonban hibázhat is: előfordulhat például,
hogy a fájl nem létezik, vagy nincs jogosultságunk hozzáférni a fájlhoz. A
`File::open` függvénynek valamiképp tudatnia kell velünk, hogy sikerrel járt-e
vagy sem, és ezzel egyidejűleg át kell adnia nekünk vagy a fájlleírót, vagy a
hiba adatait. Pontosan ezt az információt közvetíti a `Result` enum.

Abban az esetben, ha a `File::open` sikerrel jár, a `greeting_file_result`
változóban lévő érték egy `Ok` példány lesz, amely egy fájlleírót tartalmaz.
Abban az esetben, ha hibázik, a `greeting_file_result` értéke egy `Err` példány
lesz, amely bővebb információt tartalmaz a bekövetkezett hiba fajtájáról.

Ki kell egészítenünk a 9-3. lista kódját, hogy különböző műveleteket hajtson
végre attól függően, milyen értéket ad vissza a `File::open`. A 9-4. lista
egyféle módot mutat a `Result` kezelésére egy alapvető eszközzel, a 6.
fejezetben tárgyalt `match` kifejezéssel.

<Listing number="9-4" file-name="src/main.rs" caption="`match` kifejezés használata a visszaadható `Result`-variánsok kezelésére">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Vedd észre, hogy az `Option` enumhoz hasonlóan a `Result` enumot és variánsait
is behozza a hatókörbe a prelude, így nem kell kiírnunk a `Result::` előtagot az
`Ok` és `Err` variánsok elé a `match`-ágakban.

Ha az eredmény `Ok`, ez a kód visszaadja az `Ok` variánsban lévő `file` értéket,
amelyet aztán hozzárendelünk a `greeting_file` változóhoz. A `match` után
használhatjuk a fájlleírót olvasásra vagy írásra.

A `match` másik ága azt az esetet kezeli, amikor `Err` értéket kapunk a
`File::open`-től. Ebben a példában úgy döntöttünk, hogy meghívjuk a `panic!`
makrót. Ha nincs _hello.txt_ nevű fájl az aktuális könyvtárunkban, és
lefuttatjuk ezt a kódot, a `panic!` makrótól a következő kimenetet fogjuk látni:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Szokás szerint ez a kimenet pontosan megmondja, mi ment félre.

### Illesztés különböző hibákra

A 9-4. lista kódja `panic!` hívást vált ki, bármi is legyen a `File::open`
hibájának oka. Mi azonban különböző hibaokok esetén különböző műveleteket
szeretnénk végrehajtani. Ha a `File::open` azért hibázott, mert a fájl nem
létezik, létre akarjuk hozni a fájlt, és visszaadni az új fájl leíróját. Ha a
`File::open` bármilyen más okból hibázott – például mert nem volt jogosultságunk
megnyitni a fájlt –, akkor továbbra is azt szeretnénk, hogy a kód ugyanúgy
`panic!` hívást váltson ki, mint a 9-4. listában. Ehhez egy belső `match`
kifejezést adunk hozzá, ahogy a 9-5. lista mutatja.

<Listing number="9-5" file-name="src/main.rs" caption="Különböző hibafajták különböző módon való kezelése">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Annak az értéknek a típusa, amelyet a `File::open` az `Err` variánsban ad
vissza, az `io::Error`, ami a standard könyvtár által biztosított struct. Ennek
a structnak van egy `kind` metódusa, amelyet meghívva egy `io::ErrorKind`
értéket kapunk. Az `io::ErrorKind` enumot a standard könyvtár biztosítja, és
olyan variánsai vannak, amelyek az `io`-műveletekből származó különféle
hibafajtákat képviselik. Az a variáns, amelyet használni szeretnénk, az
`ErrorKind::NotFound`, amely azt jelzi, hogy a megnyitni kívánt fájl még nem
létezik. Tehát illesztünk a `greeting_file_result`-ra, de van egy belső
illesztésünk is az `error.kind()`-ra.

A belső illesztésben azt a feltételt akarjuk ellenőrizni, hogy az `error.kind()`
által visszaadott érték az `ErrorKind` enum `NotFound` variánsa-e. Ha igen,
megpróbáljuk létrehozni a fájlt a `File::create` hívással. Mivel azonban a
`File::create` is hibázhat, szükségünk van egy második ágra a belső `match`
kifejezésben. Ha a fájlt nem lehet létrehozni, egy másik hibaüzenetet írunk ki.
A külső `match` második ága változatlan marad, így a program a hiányzó fájl
hibáján kívül minden hiba esetén panicot vált ki.

> #### A `match` alternatívái a `Result<T, E>` kezelésére
>
> Ez rengeteg `match`! A `match` kifejezés nagyon hasznos, ugyanakkor eléggé
> alacsony szintű eszköz. A 13. fejezetben megismerkedsz a closure-ökkel,
> amelyeket a `Result<T, E>` típuson definiált metódusok közül sokkal együtt
> használunk. Ezek a metódusok tömörebbek lehetnek, mint a `match`, amikor a
> kódodban `Result<T, E>` értékeket kezelsz.
>
> Íme például egy másik mód a 9-5. listában látható logika megírására, ezúttal
> closure-ökkel és az `unwrap_or_else` metódussal:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Bár ennek a kódnak ugyanaz a viselkedése, mint a 9-5. listának, egyetlen
> `match` kifejezést sem tartalmaz, és letisztultabban olvasható. Térj vissza
> ehhez a példához, miután elolvastad a 13. fejezetet, és nézd meg az
> `unwrap_or_else` metódust a standard könyvtár dokumentációjában. Sok további
> ilyen metódus képes megtisztítani a hatalmas, egymásba ágyazott `match`
> kifejezéseket, amikor hibákkal dolgozol.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Rövidítések a hiba esetén kiváltott panichoz

A `match` használata elég jól működik, de kissé bőbeszédű lehet, és nem mindig
fejezi ki jól a szándékot. A `Result<T, E>` típuson sok segédmetódus van
definiálva különféle, konkrétabb feladatok elvégzésére. Az `unwrap` metódus egy
olyan rövidítő metódus, amelyet pontosan úgy implementáltak, mint azt a `match`
kifejezést, amelyet a 9-4. listában írtunk. Ha a `Result` érték az `Ok` variáns,
az `unwrap` visszaadja az `Ok`-ban lévő értéket. Ha a `Result` az `Err` variáns,
az `unwrap` meghívja helyettünk a `panic!` makrót. Íme egy példa az `unwrap`
működésére:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Ha ezt a kódot _hello.txt_ fájl nélkül futtatjuk, az `unwrap` metódus által
kezdeményezett `panic!` hívás hibaüzenetét fogjuk látni:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Hasonlóképpen az `expect` metódus lehetővé teszi, hogy mi válasszuk meg a
`panic!` hibaüzenetét is. Ha az `unwrap` helyett az `expect` metódust használod,
és jó hibaüzeneteket adsz meg, azzal kifejezheted a szándékodat, és
megkönnyítheted a panic forrásának felderítését. Az `expect` szintaxisa így néz
ki:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Az `expect` metódust ugyanúgy használjuk, mint az `unwrap`-et: a fájlleíró
visszaadására vagy a `panic!` makró meghívására. Az `expect` által a `panic!`
hívásában használt hibaüzenet az a paraméter lesz, amelyet átadunk az
`expect`-nek, nem pedig az az alapértelmezett `panic!` üzenet, amelyet az
`unwrap` használ. Így néz ki:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Éles minőségű kódban a legtöbb rustacean az `unwrap` helyett az `expect`
metódust választja, és több kontextust ad meg arról, miért várható, hogy a
művelet mindig sikerrel jár. Így, ha a feltételezéseid mégis tévesnek
bizonyulnak, több információd lesz a hibakereséshez.

### Hibák továbbadása

Amikor egy függvény implementációja olyasmit hív meg, ami hibázhat, ahelyett,
hogy magában a függvényben kezelnéd a hibát, visszaadhatod a hibát a hívó
kódnak, hogy az döntse el, mit tegyen. Ezt a hiba _továbbadásának_ (propagating)
nevezzük, és több irányítást ad a hívó kódnak, ahol több információ vagy logika
állhat rendelkezésre a hiba kezelésének módjáról, mint amennyi a te kódod
kontextusában elérhető.

A 9-6. lista például egy olyan függvényt mutat, amely egy fájlból olvas be egy
felhasználónevet. Ha a fájl nem létezik, vagy nem olvasható, ez a függvény
visszaadja ezeket a hibákat annak a kódnak, amely meghívta a függvényt.

<Listing number="9-6" file-name="src/main.rs" caption="Függvény, amely `match` segítségével adja vissza a hibákat a hívó kódnak">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Ez a függvény sokkal rövidebben is megírható, de azzal kezdjük, hogy sok
mindent kézzel csinálunk meg a hibakezelés megismerése érdekében; a végén
megmutatjuk a rövidebb módot. Nézzük először a függvény visszatérési típusát:
`Result<String, io::Error>`. Ez azt jelenti, hogy a függvény egy
`Result<T, E>` típusú értéket ad vissza, ahol a `T` generikus paraméter a
konkrét `String` típussal, az `E` generikus típus pedig a konkrét `io::Error`
típussal lett kitöltve.

Ha ez a függvény bármilyen probléma nélkül sikerrel jár, az őt meghívó kód egy
`Ok` értéket kap, amely egy `String`-et tartalmaz – azt a `username`-et, amelyet
ez a függvény kiolvasott a fájlból. Ha ez a függvény bármilyen problémába
ütközik, a hívó kód egy `Err` értéket kap, amely egy `io::Error` példányt
tartalmaz, benne bővebb információval a problémákról. Azért az `io::Error`
típust választottuk a függvény visszatérési hibatípusának, mert történetesen ez
annak a hibaértéknek a típusa, amelyet mindkét olyan művelet visszaad, amelyet
ennek a függvénynek a törzsében hívunk, és amely hibázhat: a `File::open`
függvény és a `read_to_string` metódus.

A függvény törzse a `File::open` függvény hívásával kezdődik. Ezután a `Result`
értéket egy `match` kifejezéssel kezeljük, hasonlóan a 9-4. listában lévő
`match`-hez. Ha a `File::open` sikerrel jár, a `file` mintaváltozóban lévő
fájlleíró lesz a módosítható `username_file` változó értéke, és a függvény
folytatódik. Az `Err` esetben a `panic!` hívása helyett a `return` kulcsszót
használjuk, hogy korán, teljesen kilépjünk a függvényből, és a `File::open`
hibaértékét – amely most az `e` mintaváltozóban van – visszaadjuk a hívó kódnak
mint ennek a függvénynek a hibaértékét.

Így, ha van egy fájlleírónk a `username_file`-ban, a függvény ezután létrehoz
egy új `String`-et a `username` változóban, és meghívja a `read_to_string`
metódust a `username_file`-ban lévő fájlleírón, hogy beolvassa a fájl tartalmát
a `username`-be. A `read_to_string` metódus szintén `Result`-ot ad vissza, mert
hibázhat, még akkor is, ha a `File::open` sikerrel járt. Ezért szükségünk van
egy újabb `match`-re ennek a `Result`-nak a kezelésére: ha a `read_to_string`
sikerrel jár, akkor a függvényünk is sikerrel járt, és `Ok`-ba csomagolva
visszaadjuk a fájlból származó, most már a `username`-ben lévő
felhasználónevet. Ha a `read_to_string` hibázik, ugyanúgy adjuk vissza a
hibaértéket, ahogy abban a `match`-ben tettük, amely a `File::open` visszatérési
értékét kezelte. Itt azonban nem kell kiírnunk a `return` kulcsszót, mert ez a
függvény utolsó kifejezése.

Az ezt a kódot meghívó kód ezután vagy egy felhasználónevet tartalmazó `Ok`
értéket, vagy egy `io::Error`-t tartalmazó `Err` értéket fog kezelni. A hívó kód
dolga eldönteni, mit kezd ezekkel az értékekkel. Ha a hívó kód `Err` értéket
kap, meghívhatja például a `panic!` makrót és összeomlaszthatja a programot,
használhat egy alapértelmezett felhasználónevet, vagy kikeresheti a
felhasználónevet valahonnan máshonnan, nem fájlból. Nincs elég információnk
arról, hogy a hívó kód valójában mit próbál elérni, ezért minden siker- és
hibainformációt felfelé továbbadunk, hogy ő kezelje megfelelően.

A hibatovábbadásnak ez a mintája annyira gyakori a Rustban, hogy a Rust a
kérdőjel operátort, a `?`-et biztosítja ennek megkönnyítésére.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### A `?` operátor mint rövidítés

A 9-7. lista a `read_username_from_file` olyan implementációját mutatja, amely
ugyanazt tudja, mint a 9-6. listában lévő, de ez az implementáció a `?`
operátort használja.

<Listing number="9-7" file-name="src/main.rs" caption="Függvény, amely a `?` operátor segítségével adja vissza a hibákat a hívó kódnak">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

Egy `Result` érték után elhelyezett `?` definíció szerint majdnem ugyanúgy
működik, mint azok a `match` kifejezések, amelyeket a 9-6. listában a `Result`
értékek kezelésére definiáltunk. Ha a `Result` értéke `Ok`, az `Ok`-ban lévő
érték lesz a kifejezés visszatérési értéke, és a program folytatódik. Ha az
érték `Err`, az `Err` lesz az egész függvény visszatérési értéke, mintha a
`return` kulcsszót használtuk volna, így a hibaérték továbbadódik a hívó kódnak.

Van egy különbség aközött, amit a 9-6. lista `match` kifejezése tesz, és amit a
`?` operátor: azok a hibaértékek, amelyeken a `?` operátort hívjuk, átmennek a
`from` függvényen, amely a standard könyvtár `From` traitjében van definiálva,
és amelyet értékek egyik típusból másikba való átalakítására használunk. Amikor
a `?` operátor meghívja a `from` függvényt, a kapott hibatípus átalakul azzá a
hibatípussá, amely az aktuális függvény visszatérési típusában van definiálva.
Ez akkor hasznos, ha egy függvény egyetlen hibatípust ad vissza mindazon módok
megjelenítésére, ahogyan a függvény hibázhat, még akkor is, ha egyes részek
sokféle különböző okból hibázhatnak.

Például megváltoztathatnánk a 9-7. lista `read_username_from_file` függvényét
úgy, hogy egy általunk definiált, `OurError` nevű egyedi hibatípust adjon
vissza. Ha emellett definiáljuk az `impl From<io::Error> for OurError`
implementációt, hogy `OurError`-példányt hozzunk létre egy `io::Error`-ból,
akkor a `read_username_from_file` törzsében lévő `?` operátorhívások meghívják a
`from` függvényt, és átalakítják a hibatípusokat anélkül, hogy bármilyen további
kódot hozzá kellene adnunk a függvényhez.

A 9-7. lista kontextusában a `File::open` hívás végén álló `?` az `Ok`-ban lévő
értéket adja vissza a `username_file` változóba. Ha hiba történik, a `?`
operátor korán kilép az egész függvényből, és bármilyen `Err` értéket átad a
hívó kódnak. Ugyanez érvényes a `read_to_string` hívás végén álló `?`-re is.

A `?` operátor rengeteg sablonkódot kiküszöböl, és egyszerűbbé teszi ennek a
függvénynek az implementációját. Ezt a kódot még tovább is rövidíthetnénk azzal,
hogy közvetlenül a `?` után metódushívásokat fűzünk láncba, ahogy a 9-8. lista
mutatja.

<Listing number="9-8" file-name="src/main.rs" caption="Metódushívások láncba fűzése a `?` operátor után">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Az új `String` létrehozását a `username` változóban a függvény elejére
helyeztük át; ez a rész nem változott. Ahelyett, hogy létrehoznánk egy
`username_file` változót, a `read_to_string` hívását közvetlenül a
`File::open("hello.txt")?` eredményéhez fűztük. Továbbra is van egy `?` a
`read_to_string` hívás végén, és továbbra is egy `username`-et tartalmazó `Ok`
értéket adunk vissza hibák helyett, amikor mind a `File::open`, mind a
`read_to_string` sikerrel jár. A működés ismét ugyanaz, mint a 9-6. és a 9-7.
listában; ez csak egy másik, ergonomikusabb módja a megírásának.

A 9-9. lista egy módot mutat arra, hogy ezt még rövidebbé tegyük a
`fs::read_to_string` segítségével.

<Listing number="9-9" file-name="src/main.rs" caption="A `fs::read_to_string` használata a fájl megnyitása és beolvasása helyett">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Egy fájl beolvasása egy stringbe elég gyakori művelet, ezért a standard könyvtár
biztosítja a kényelmes `fs::read_to_string` függvényt, amely megnyitja a fájlt,
létrehoz egy új `String`-et, beolvassa a fájl tartalmát, beleteszi a tartalmat
abba a `String`-be, és visszaadja azt. A `fs::read_to_string` használata
természetesen nem adna alkalmat arra, hogy elmagyarázzuk az összes hibakezelést,
ezért előbb a hosszabb úton jártunk.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Hol használható a `?` operátor

A `?` operátor csak olyan függvényekben használható, amelyek visszatérési típusa
kompatibilis azzal az értékkel, amelyen a `?`-et használjuk. Ez azért van, mert
a `?` operátor definíció szerint korai visszatérést hajt végre egy értékkel a
függvényből, ugyanúgy, ahogy a 9-6. listában definiált `match` kifejezés. A 9-6.
listában a `match` egy `Result` értéket használt, és a korai visszatérést végző
ág egy `Err(e)` értéket adott vissza. A függvény visszatérési típusának
`Result`-nak kell lennie, hogy kompatibilis legyen ezzel a `return`-nel.

A 9-10. listában nézzük meg, milyen hibát kapunk, ha a `?` operátort egy olyan
`main` függvényben használjuk, amelynek a visszatérési típusa nem kompatibilis
annak az értéknek a típusával, amelyen a `?`-et használjuk.

<Listing number="9-10" file-name="src/main.rs" caption="A `?` használatának kísérlete a `()`-t visszaadó `main` függvényben nem fordul le.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Ez a kód megnyit egy fájlt, ami hibázhat. A `?` operátor a `File::open` által
visszaadott `Result` értéket követi, de ennek a `main` függvénynek a
visszatérési típusa `()`, nem `Result`. Amikor lefordítjuk ezt a kódot, a
következő hibaüzenetet kapjuk:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Ez a hiba rámutat, hogy a `?` operátort csak olyan függvényben használhatjuk,
amely `Result`-ot, `Option`-t vagy egy másik olyan típust ad vissza, amely
implementálja a `FromResidual` traitet.

A hiba javítására két lehetőséged van. Az egyik, hogy megváltoztatod a
függvényed visszatérési típusát úgy, hogy kompatibilis legyen azzal az értékkel,
amelyen a `?` operátort használod – feltéve, hogy semmilyen megkötés nem
akadályoz ebben. A másik, hogy egy `match`-et vagy a `Result<T, E>` valamelyik
metódusát használod a `Result<T, E>` kezelésére az adott helyzetben megfelelő
módon.

A hibaüzenet azt is megemlítette, hogy a `?` `Option<T>` értékekkel is
használható. Ahogy a `Result`-on való `?`-használatnál, az `Option`-on is csak
olyan függvényben használhatod a `?`-et, amely `Option`-t ad vissza. A `?`
operátor viselkedése egy `Option<T>`-n meghívva hasonló ahhoz, ahogy egy
`Result<T, E>`-n viselkedik: ha az érték `None`, a `None` korán visszaadódik a
függvényből azon a ponton. Ha az érték `Some`, a `Some`-ban lévő érték lesz a
kifejezés eredménye, és a függvény folytatódik. A 9-11. listában egy olyan
függvény példája szerepel, amely megkeresi az adott szöveg első sorának utolsó
karakterét.

<Listing number="9-11" caption="A `?` operátor használata egy `Option<T>` értéken">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Ez a függvény `Option<char>`-t ad vissza, mert lehetséges, hogy van ott
karakter, de az is lehetséges, hogy nincs. Ez a kód veszi a `text` string slice
argumentumot, és meghívja rajta a `lines` metódust, amely egy iterátort ad
vissza a stringben lévő sorokon. Mivel ez a függvény az első sort akarja
megvizsgálni, meghívja az iterátoron a `next`-et, hogy megkapja az iterátor első
értékét. Ha a `text` az üres string, ez a `next`-hívás `None`-t ad vissza, ez
esetben a `?`-et használjuk, hogy megálljunk, és `None`-t adjunk vissza a
`last_char_of_first_line`-ból. Ha a `text` nem az üres string, a `next` egy
`Some` értéket ad vissza, amely a `text` első sorának string slice-át
tartalmazza.

A `?` kinyeri a string slice-ot, és meghívhatjuk azon a string slice-on a
`chars`-t, hogy egy iterátort kapjunk a karaktereiről. Minket ennek az első
sornak az utolsó karaktere érdekel, ezért meghívjuk a `last`-ot, hogy visszaadja
az iterátor utolsó elemét. Ez egy `Option`, mert lehetséges, hogy az első sor
üres string; például ha a `text` üres sorral kezdődik, de más sorokban vannak
karakterek, mint a `"\nhi"` esetében. Ha viszont van utolsó karakter az első
sorban, azt a `Some` variánsban kapjuk vissza. A középen álló `?` operátor
tömör módot ad ennek a logikának a kifejezésére, így egyetlen sorban
implementálhatjuk a függvényt. Ha nem használhatnánk a `?` operátort az
`Option`-on, ezt a logikát több metódushívással vagy egy `match` kifejezéssel
kellene implementálnunk.

Vedd észre, hogy a `?` operátort használhatod egy `Result`-on egy `Result`-ot
visszaadó függvényben, és használhatod a `?` operátort egy `Option`-on egy
`Option`-t visszaadó függvényben, de a kettőt nem keverheted. A `?` operátor nem
alakít át automatikusan `Result`-ot `Option`-né vagy fordítva; ilyen esetekben
olyan metódusokat használhatsz, mint a `Result` `ok` metódusa vagy az `Option`
`ok_or` metódusa, hogy kifejezetten elvégezd az átalakítást.

Eddig minden `main` függvényünk `()`-t adott vissza. A `main` függvény
különleges, mert ez egy futtatható program belépési és kilépési pontja, és
megkötések vonatkoznak arra, mi lehet a visszatérési típusa, hogy a program a
várt módon viselkedjen.

Szerencsére a `main` `Result<(), E>`-t is visszaadhat. A 9-12. listában a 9-10.
lista kódja szerepel, de a `main` visszatérési típusát
`Result<(), Box<dyn Error>>`-ra változtattuk, és a végére hozzáadtunk egy
`Ok(())` visszatérési értéket. Ez a kód már le fog fordulni.

<Listing number="9-12" file-name="src/main.rs" caption="Ha a `main`-t úgy módosítjuk, hogy `Result<(), E>`-t adjon vissza, akkor használható a `?` operátor a `Result` értékeken.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

A `Box<dyn Error>` típus egy trait object, amelyről a 18. fejezet [„Trait
objectek használata az osztott viselkedés absztrahálására”][trait-objects]<!--
ignore --> szakaszában lesz szó. Egyelőre a `Box<dyn Error>`-t olvashatod
„bármilyen fajta hiba” értelemben. A `?` használata egy `Result` értéken egy
olyan `main` függvényben, amelynek hibatípusa `Box<dyn Error>`, megengedett,
mert lehetővé teszi bármilyen `Err` érték korai visszaadását. Bár ennek a `main`
függvénynek a törzse csak `std::io::Error` típusú hibákat fog valaha
visszaadni, a `Box<dyn Error>` megadásával ez a szignatúra akkor is helyes
marad, ha a `main` törzséhez további, más hibákat visszaadó kódot adunk hozzá.

Ha egy `main` függvény `Result<(), E>`-t ad vissza, a futtatható program `0`
értékkel lép ki, amennyiben a `main` `Ok(())`-t ad vissza, és nem nulla értékkel
lép ki, ha a `main` `Err` értéket ad vissza. A C-ben írt futtatható programok
egész számokat adnak vissza kilépéskor: a sikeresen kilépő programok a `0` egész
számot adják vissza, a hibával kilépők pedig valamilyen `0`-tól különböző egész
számot. A Rust szintén egész számokat ad vissza a futtatható programokból, hogy
kompatibilis legyen ezzel a konvencióval.

A `main` függvény bármilyen olyan típust visszaadhat, amely implementálja [a
`std::process::Termination` traitet][termination]<!-- ignore -->, amely
tartalmaz egy `report` függvényt, ami `ExitCode`-ot ad vissza. A standard
könyvtár dokumentációjában találsz további információt arról, hogyan
implementáld a `Termination` traitet a saját típusaidra.

Most, hogy megbeszéltük a `panic!` hívásának és a `Result` visszaadásának
részleteit, térjünk vissza ahhoz a témához, hogyan döntsük el, melyiket
érdemes használni az egyes esetekben.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html
