## Haladó típusok

A Rust típusrendszerének van néhány olyan képessége, amelyet eddig már
említettünk, de még nem tárgyaltunk. Először általánosságban a newtype-okról
lesz szó, és megvizsgáljuk, miért hasznosak típusként. Utána rátérünk a
típusaliasokra, amelyek a newtype-okhoz hasonló, de kissé eltérő szemantikájú
nyelvi elemek. Szó lesz még a `!` típusról és a dinamikusan méretezett
típusokról is.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Típusbiztonság és absztrakció a newtype mintával

Ez a szakasz feltételezi, hogy elolvastad a korábbi [„Külső trait-ek
implementálása a newtype mintával”][newtype]<!-- ignore --> szakaszt. A newtype
minta az eddig tárgyaltakon túl további feladatokra is hasznos, például arra,
hogy statikusan kikényszerítsük az értékek össze nem keverhetőségét, vagy hogy
jelezzük egy érték mértékegységét. A 20-16. listában láttál példát arra, hogy
newtype-okkal jelezzük a mértékegységet: emlékezz rá, hogy a `Millimeters` és a
`Meters` struct `u32` értékeket csomagolt be egy newtype-ba. Ha írnánk egy
`Millimeters` típusú paraméterrel rendelkező függvényt, nem tudnánk lefordítani
egy olyan programot, amely véletlenül `Meters` típusú vagy sima `u32` értékkel
próbálná meghívni ezt a függvényt.

A newtype mintát arra is használhatjuk, hogy elrejtsük egy típus bizonyos
implementációs részleteit: az új típus a privát belső típus API-jától eltérő,
publikus API-t tehet elérhetővé.

A newtype-ok a belső implementációt is elrejthetik. Például készíthetnénk egy
`People` típust, amely egy `HashMap<i32, String>` értéket csomagol be, és egy
személy azonosítóját tárolja a nevéhez rendelve. A `People` típust használó kód
csak az általunk biztosított publikus API-val érintkezne — például egy olyan
metódussal, amely egy névsztringet ad hozzá a `People` kollekcióhoz —, és ennek
a kódnak nem kellene tudnia, hogy belül `i32` azonosítót rendelünk a nevekhez.
A newtype minta könnyűsúlyú módja annak az egységbezárásnak, amellyel
elrejthetjük az implementációs részleteket; erről a 18. fejezet [„Egységbezárás,
amely elrejti az implementációs
részleteket”][encapsulation-that-hides-implementation-details]<!-- ignore -->
című szakaszában volt szó.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Típusszinonimák és típusaliasok {#type-synonyms-and-type-aliases}

A Rust lehetőséget ad arra, hogy _típusaliast_ deklarálj, amellyel egy létező
típusnak másik nevet adsz. Ehhez a `type` kulcsszót használjuk. Például így
hozhatjuk létre a `Kilometers` aliast az `i32` típushoz:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Mostantól a `Kilometers` alias az `i32` _szinonimája_; a 20-16. listában
létrehozott `Millimeters` és `Meters` típusokkal ellentétben a `Kilometers` nem
külön, új típus. A `Kilometers` típusú értékeket ugyanúgy kezeli a fordító,
mint az `i32` típusúakat:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Mivel a `Kilometers` és az `i32` ugyanaz a típus, összeadhatjuk a kétféle
típusú értékeket, és `Kilometers` értékeket adhatunk át olyan függvényeknek,
amelyek `i32` paramétert várnak. Ezzel a módszerrel viszont nem kapjuk meg azt
a típusellenőrzési előnyt, amelyet a korábban tárgyalt newtype minta nyújt.
Más szóval, ha valahol összekeverjük a `Kilometers` és az `i32` értékeket, a
fordító nem jelez hibát.

A típusszinonimák fő haszna az ismétlődés csökkentése. Például lehet egy ilyen
hosszú típusunk:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Fárasztó és hibalehetőségekkel teli dolog ezt a hosszú típust a
függvényszignatúrákban és típusannotációkként újra meg újra leírni a kód
minden pontján. Képzelj el egy olyan projektet, amely tele van a 20-25.
listához hasonló kóddal.

<Listing number="20-25" caption="Hosszú típus használata sok helyen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

A típusalias kezelhetőbbé teszi ezt a kódot azzal, hogy csökkenti az
ismétlődést. A 20-26. listában bevezettünk egy `Thunk` nevű aliast a bőbeszédű
típushoz, így a típus minden előfordulását lecserélhetjük a rövidebb `Thunk`
aliasra.

<Listing number="20-26" caption="A `Thunk` típusalias bevezetése az ismétlődés csökkentésére">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Ezt a kódot sokkal könnyebb olvasni és írni! Ha értelmes nevet választasz a
típusaliasnak, azzal a szándékodat is jól kifejezheted (a _thunk_ olyan kódot
jelent, amelyet később kell kiértékelni, így találó név egy eltárolt
closure-nek).

A típusaliasokat gyakran használják a `Result<T, E>` típussal is az ismétlődés
csökkentésére. Nézzük a standard könyvtár `std::io` modulját. Az I/O-műveletek
gyakran `Result<T, E>` értéket adnak vissza, hogy kezelni lehessen a
sikertelen műveleteket. Ebben a könyvtárban van egy `std::io::Error` struct,
amely az összes lehetséges I/O-hibát reprezentálja. Az `std::io` sok függvénye
olyan `Result<T, E>` értéket ad vissza, amelyben az `E` az `std::io::Error` —
ilyenek például a `Write` trait alábbi függvényei:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

A `Result<..., Error>` sokszor ismétlődik. Emiatt az `std::io` tartalmazza ezt
a típusalias-deklarációt:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Mivel ez a deklaráció az `std::io` modulban van, használhatjuk a teljesen
minősített `std::io::Result<T>` aliast; vagyis egy olyan `Result<T, E>`
típust, amelyben az `E` helyére az `std::io::Error` kerül. A `Write` trait
függvényszignatúrái így végül így néznek ki:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

A típusalias két dologban segít: könnyebbé teszi a kód írását, _és_ egységes
felületet ad az egész `std::io` modulban. Mivel ez csak alias, valójában egy
közönséges `Result<T, E>`, ami azt jelenti, hogy minden olyan metódust
használhatunk vele, amely `Result<T, E>` értékeken működik, és a speciális
szintaxist is, például a `?` operátort.

### A never típus, amely sosem tér vissza

A Rustban van egy `!` nevű speciális típus, amelyet a típuselmélet szóhasználata
_üres típusnak_ nevez, mert nincs egyetlen értéke sem. Mi szívesebben hívjuk
_never típusnak_, mert a visszatérési típus helyén áll, ha egy függvény sosem
tér vissza. Íme egy példa:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Ezt a kódot így olvassuk: „a `bar` függvény sosem tér vissza”. A sosem
visszatérő függvényeket _divergáló függvényeknek_ nevezzük. A `!` típusnak nem
tudunk értékeit létrehozni, így a `bar` semmiképpen nem tud visszatérni.

De mire jó egy olyan típus, amelynek sosem hozhatunk létre értékét? Emlékezz
vissza a 2-5. lista kódjára, a számkitalálós játék részletére; egy darabkáját
újra megmutatjuk a 20-27. listában.

<Listing number="20-27" caption="`match`, amelynek egyik ága `continue`-val végződik">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Akkoriban átugrottunk néhány részletet ebben a kódban. A 6. fejezet [„A `match`
vezérlési szerkezet”][the-match-control-flow-construct]<!-- ignore --> című
szakaszában szó volt arról, hogy a `match`-ágaknak mind ugyanazt a típust kell
visszaadniuk. Így például az alábbi kód nem működik:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Ebben a kódban a `guess` típusának egyszerre kellene egész számnak _és_
sztringnek lennie, a Rust viszont megköveteli, hogy a `guess`-nek csak egy
típusa legyen. Mit ad hát vissza a `continue`? Hogyan lehetséges, hogy a 20-27.
listában az egyik ágból `u32` értéket adhattunk vissza, miközben egy másik ág
`continue`-val végződik?

Ahogy sejtheted, a `continue` értéke `!` típusú. Vagyis amikor a Rust
kiszámítja a `guess` típusát, mindkét match-ágat megnézi: az elsőben `u32`
értékű, a másodikban `!` értékű kifejezés áll. Mivel a `!` sosem vehet fel
értéket, a Rust úgy dönt, hogy a `guess` típusa `u32`.

E viselkedés formális leírása úgy hangzik, hogy a `!` típusú kifejezések
bármely más típussá kényszeríthetők. Azért zárhatjuk le ezt a `match`-ágat
`continue`-val, mert a `continue` nem ad vissza értéket; ehelyett visszaadja a
vezérlést a ciklus elejére, így az `Err` esetben sosem rendelünk értéket a
`guess`-hez.

A never típus a `panic!` makróval is hasznos. Emlékezz vissza az `unwrap`
függvényre, amelyet `Option<T>` értékeken hívunk meg, hogy értéket kapjunk
vagy panicot váltsunk ki; a definíciója ez:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Ebben a kódban ugyanaz történik, mint a 20-27. lista `match`-ében: a Rust
látja, hogy a `val` típusa `T`, a `panic!` típusa pedig `!`, így a teljes
`match` kifejezés eredménye `T` típusú. Ez a kód azért működik, mert a `panic!`
nem állít elő értéket; véget vet a programnak. A `None` esetben nem adunk
vissza értéket az `unwrap`-ből, így ez a kód érvényes.

Még egy kifejezés van, amelynek `!` a típusa: a `loop` ciklus.

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Itt a ciklus sosem ér véget, így a kifejezés értéke `!`. Ez azonban nem lenne
igaz, ha `break`-et is beleírnánk, mert akkor a ciklus a `break`-hez érve
befejeződne.

### Dinamikusan méretezett típusok és a `Sized` trait {#dynamically-sized-types-and-the-sized-trait}

A Rustnak bizonyos részleteket tudnia kell a típusairól, például azt, hogy egy
adott típus értéke számára mennyi helyet foglaljon le. Emiatt a
típusrendszerének egyik sarka elsőre kissé zavarba ejtő: ez a _dinamikusan
méretezett típusok_ fogalma. Ezeket a típusokat néha _DST_-knek vagy
_méret nélküli típusoknak_ is nevezik, és lehetővé teszik, hogy olyan
értékekkel írjunk kódot, amelyek méretét csak futásidőben ismerhetjük meg.

Nézzük meg közelebbről egy dinamikusan méretezett típus, a `str` részleteit,
amelyet a könyv során végig használtunk. Jól olvasod: nem a `&str`, hanem
önmagában a `str` a DST. Sok esetben — például ha a felhasználó által beírt
szöveget tároljuk — csak futásidőben derül ki, milyen hosszú a sztring. Ez azt
jelenti, hogy nem hozhatunk létre `str` típusú változót, és `str` típusú
argumentumot sem fogadhatunk. Nézd meg az alábbi kódot, amely nem működik:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

A Rustnak tudnia kell, mennyi memóriát foglaljon le egy adott típus bármely
értékének, és egy típus minden értékének ugyanannyi memóriát kell használnia.
Ha a Rust megengedné ezt a kódot, ennek a két `str` értéknek ugyanannyi helyet
kellene elfoglalnia. A hosszuk viszont különböző: az `s1` 12 bájtnyi tárhelyet
igényel, az `s2` pedig 15-öt. Ezért nem lehet dinamikusan méretezett típusú
értéket tartalmazó változót létrehozni.

Mit tegyünk hát? Ebben az esetben már ismered a választ: a `s1` és az `s2`
típusa ne `str`, hanem string slice (`&str`) legyen. A 4. fejezet [„String
slice-ok”][string-slices]<!-- ignore --> című szakaszából emlékezhetsz rá, hogy
a slice adatszerkezet csak a slice kezdőpozícióját és hosszát tárolja. Így míg
a `&T` egyetlen érték, amely azt a memóriacímet tárolja, ahol a `T`
elhelyezkedik, addig a string slice _két_ érték: a `str` címe és a hossza.
Ennek megfelelően egy string slice értékének méretét fordítási időben
ismerjük: egy `usize` hosszának kétszerese. Vagyis mindig tudjuk, mekkora egy
string slice, függetlenül attól, milyen hosszú sztringre hivatkozik.
Általánosságban így használjuk a dinamikusan méretezett típusokat a Rustban:
van egy kis extra metaadatuk, amely a dinamikus információ méretét tárolja. A
dinamikusan méretezett típusok aranyszabálya, hogy az ilyen típusú értékeket
mindig valamilyen pointer mögé kell tennünk.

A `str` mindenféle pointerrel kombinálható: például `Box<str>` vagy `Rc<str>`
alakban. Valójában ezt már láttad korábban is, csak egy másik dinamikusan
méretezett típusnál: a trait-eknél. Minden trait dinamikusan méretezett típus,
amelyre a trait nevével hivatkozhatunk. A 18. fejezet [„Trait objectek
használata a közös viselkedés
absztrahálására”][using-trait-objects-to-abstract-over-shared-behavior]<!--
ignore --> című szakaszában említettük, hogy ha a trait-eket trait objectként
akarjuk használni, pointer mögé kell tennünk őket, például `&dyn Trait` vagy
`Box<dyn Trait>` alakban (az `Rc<dyn Trait>` is működne).

A DST-kkel való munkához a Rust a `Sized` trait-et biztosítja, amellyel
eldönthető, hogy egy típus mérete ismert-e fordítási időben. Ez a trait
automatikusan implementálva van mindenre, aminek a mérete fordítási időben
ismert. Ezenfelül a Rust minden generikus függvényhez implicit módon hozzáad
egy `Sized` trait bound-ot. Vagyis egy ilyen generikus függvénydefiníció:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

valójában úgy viselkedik, mintha ezt írtuk volna:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Alapértelmezés szerint a generikus függvények csak olyan típusokkal működnek,
amelyek mérete fordítási időben ismert. Az alábbi speciális szintaxissal
azonban lazíthatsz ezen a megkötésen:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

A `?Sized` trait bound jelentése: „a `T` lehet `Sized`, de nem feltétlenül az”,
és ez a jelölés felülírja azt az alapértelmezést, hogy a generikus típusok
méretének fordítási időben ismertnek kell lennie. A `?Trait` szintaxis ebben az
értelemben csak a `Sized` esetén használható, más trait-ekkel nem.

Vedd észre azt is, hogy a `t` paraméter típusát `T`-ről `&T`-re cseréltük.
Mivel a típus lehet, hogy nem `Sized`, valamilyen pointer mögött kell
használnunk. Ebben az esetben referenciát választottunk.

A következőkben a függvényekről és a closure-ökről lesz szó!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
