## Generikus adattípusok

A generikusokat arra használjuk, hogy definíciókat készítsünk olyan elemekhez,
mint a függvényszignatúrák vagy a structok, amelyeket aztán sokféle konkrét
adattípussal használhatunk. Nézzük meg először, hogyan definiálhatunk
függvényeket, structokat, enumokat és metódusokat generikusokkal. Utána szó lesz
arról, hogyan hatnak a generikusok a kód teljesítményére.

### Függvénydefiníciókban

Ha generikusokat használó függvényt definiálunk, a generikusokat a függvény
szignatúrájában oda tesszük, ahol egyébként a paraméterek és a visszatérési
érték adattípusát adnánk meg. Ettől a kódunk rugalmasabb lesz, és több
funkcionalitást nyújt a függvényünk hívóinak, miközben megelőzi a kódismétlést.

Maradva a `largest` függvényünknél, a 10-4. listázás két olyan függvényt mutat,
amelyek mindegyike a legnagyobb értéket keresi meg egy slice-ban. Ezeket
egyetlen, generikusokat használó függvénnyé fogjuk összevonni.

<Listing number="10-4" file-name="src/main.rs" caption="Két függvény, amelyek csak a nevükben és a szignatúrájukban szereplő típusokban különböznek">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

A `largest_i32` függvény az, amelyet a 10-3. listázásban emeltünk ki; ez keresi
meg a legnagyobb `i32`-t egy slice-ban. A `largest_char` függvény a legnagyobb
`char`-t keresi meg egy slice-ban. A függvénytörzsekben ugyanaz a kód szerepel,
szüntessük hát meg az ismétlődést azzal, hogy egyetlen függvényben bevezetünk
egy generikus típusparamétert.

Ahhoz, hogy egy új, egységes függvényben paraméterezhessük a típusokat, el kell
neveznünk a típusparamétert, ugyanúgy, ahogy a függvény értékparamétereit is
elnevezzük. Bármilyen azonosítót használhatsz típusparaméter-névként. Mi
azonban a `T`-t használjuk, mert a konvenció szerint a típusparaméterek nevei a
Rustban rövidek, gyakran mindössze egyetlen betűből állnak, a Rust
típuselnevezési konvenciója pedig az UpperCamelCase. A `T` a _type_ rövidítése,
és a legtöbb Rust-programozó alapértelmezett választása.

Amikor egy paramétert használunk a függvény törzsében, a paraméter nevét
deklarálnunk kell a szignatúrában, hogy a fordító tudja, mit jelent az a név.
Hasonlóképpen,
amikor egy típusparaméter-nevet használunk egy függvényszignatúrában, a
típusparaméter nevét deklarálnunk kell, mielőtt használnánk. A generikus
`largest` függvény definiálásához a típusnév-deklarációkat csúcsos zárójelek,
`<>` közé tesszük, a függvény neve és a paraméterlista közé, így:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Ezt a definíciót így olvassuk: „A `largest` függvény generikus valamilyen `T`
típusra nézve.” Ennek a függvénynek egyetlen `list` nevű paramétere van, amely
`T` típusú értékek slice-a. A `largest` függvény ugyanilyen `T` típusú értékre
mutató referenciát ad vissza.

A 10-5. listázás a `largest` függvény összevont definícióját mutatja, amely a
generikus adattípust használja a szignatúrájában. A listázás azt is bemutatja,
hogyan hívhatjuk meg a függvényt akár `i32`, akár `char` értékekből álló
slice-szal. Vedd figyelembe, hogy ez a kód még nem fordul le.

<Listing number="10-5" file-name="src/main.rs" caption="A `largest` függvény generikus típusparaméterekkel; ez még nem fordul le">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Ha most rögtön lefordítjuk ezt a kódot, ezt a hibát kapjuk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

A súgószöveg megemlíti a `std::cmp::PartialOrd`-ot, ami egy trait; a trait-ekről
a következő szakaszban lesz szó. Egyelőre elég annyit tudni, hogy ez a hiba azt
állítja: a `largest` törzse nem működik minden lehetséges típusra, ami a `T`
lehet. Mivel a törzsben `T` típusú értékeket akarunk összehasonlítani, csak
olyan típusokat használhatunk, amelyek értékei rendezhetők. Az összehasonlítások
lehetővé tételére a standard könyvtárban ott van a `std::cmp::PartialOrd` trait,
amelyet implementálhatsz a típusaidon (erről a traitről bővebben a C.
függelékben). A 10-5. listázás javításához követhetjük a súgószöveg javaslatát,
és a `T`-hez érvényes típusokat leszűkíthetjük azokra, amelyek implementálják a
`PartialOrd`-ot. A listázás ezután le fog fordulni, mert a standard könyvtár
implementálja a `PartialOrd`-ot az `i32`-re és a `char`-ra is.

### Structdefiníciókban

A structokat is definiálhatjuk úgy, hogy egy vagy több mezőjükben generikus
típusparamétert használjanak, a `<>` szintaxissal. A 10-6. listázás egy
`Point<T>` structot definiál, amely tetszőleges típusú `x` és `y`
koordinátaértékeket tárol.

<Listing number="10-6" file-name="src/main.rs" caption="Egy `Point<T>` struct, amely `T` típusú `x` és `y` értékeket tárol">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

A generikusok structdefiníciókban való használatának szintaxisa hasonlít arra,
amit a függvénydefinícióknál használunk. Először deklaráljuk a típusparaméter
nevét csúcsos zárójelek között, közvetlenül a struct neve után. Ezután a
generikus típust ott használjuk a structdefinícióban, ahol egyébként konkrét
adattípusokat adnánk meg.

Vedd figyelembe, hogy mivel a `Point<T>` definiálásához csak egyetlen generikus
típust használtunk, ez a definíció azt mondja ki, hogy a `Point<T>` struct
generikus valamilyen `T` típusra nézve, és az `x`, illetve `y` mező _mindkettő_
ugyanaz a típus, bármi legyen is az. Ha olyan `Point<T>` példányt hozunk létre,
amelyben különböző típusú értékek szerepelnek, mint a 10-7. listázásban, a
kódunk nem fordul le.

<Listing number="10-7" file-name="src/main.rs" caption="Az `x` és `y` mezőnek azonos típusúnak kell lennie, mert mindkettőnek ugyanaz a `T` generikus adattípusa.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Ebben a példában, amikor az `5` egész értéket rendeljük az `x`-hez, tudatjuk a
fordítóval, hogy a `T` generikus típus egész szám lesz a `Point<T>` ezen
példánya esetében. Ezután, amikor `4.0`-t adunk meg az `y`-nak, amelyet
ugyanolyan típusúnak definiáltunk, mint az `x`-et, ilyen típuseltérési hibát
kapunk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Ha olyan `Point` structot szeretnénk definiálni, amelyben az `x` és az `y` is
generikus, de eltérő típusú lehet, több generikus típusparamétert használhatunk.
A 10-8. listázásban például úgy változtatjuk meg a `Point` definícióját, hogy
`T` és `U` típusokra nézve legyen generikus, ahol az `x` `T` típusú, az `y`
pedig `U` típusú.

<Listing number="10-8" file-name="src/main.rs" caption="Egy `Point<T, U>`, amely két típusra nézve generikus, így az `x` és az `y` különböző típusú érték lehet">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Most már a `Point` minden bemutatott példánya megengedett! Egy definícióban
annyi generikus típusparamétert használhatsz, amennyit csak akarsz, de ha
néhánynál többet használsz, a kódod nehezen olvashatóvá válik. Ha azt veszed
észre, hogy sok generikus típusra van szükséged a kódodban, az arra utalhat,
hogy a kódodat kisebb darabokra kellene bontani.

### Enumdefiníciókban

Ahogy a structoknál tettük, az enumokat is definiálhatjuk úgy, hogy generikus
adattípusokat tároljanak a variánsaikban. Nézzük meg újra az `Option<T>` enumot,
amelyet a standard könyvtár biztosít, és amelyet a 6. fejezetben használtunk:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Ennek a definíciónak most már több értelme kell hogy legyen a számodra. Amint
látod, az `Option<T>` enum a `T` típusra nézve generikus, és két variánsa van: a
`Some`, amely egy `T` típusú értéket tárol, valamint a `None` variáns, amely
semmilyen értéket nem tárol. Az `Option<T>` enum használatával kifejezhetjük az
opcionális érték absztrakt fogalmát, és mivel az `Option<T>` generikus, ezt az
absztrakciót attól függetlenül használhatjuk, hogy milyen típusú az opcionális
érték.

Az enumok több generikus típust is használhatnak. Erre példa a `Result` enum
definíciója, amelyet a 9. fejezetben használtunk:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

A `Result` enum két típusra, a `T`-re és az `E`-re nézve generikus, és két
variánsa van: az `Ok`, amely `T` típusú értéket tárol, és az `Err`, amely `E`
típusú értéket tárol. Ez a definíció kényelmessé teszi a `Result` enum
használatát mindenütt, ahol olyan műveletünk van, amely sikerülhet (valamilyen
`T` típusú értéket ad vissza) vagy elbukhat (valamilyen `E` típusú hibát ad
vissza). Valójában éppen ezt használtuk fájl megnyitására a 9-3. listázásban,
ahol a `T` helyére a `std::fs::File` típus került, amikor a fájl megnyitása
sikerült, az `E` helyére pedig a `std::io::Error` típus, amikor gondok voltak a
fájl megnyitásával.

Ha olyan helyzeteket ismersz fel a kódodban, ahol több struct- vagy
enumdefiníció csak az általuk tárolt értékek típusaiban különbözik,
elkerülheted az ismétlődést azzal, hogy helyettük generikus típusokat használsz.

### Metódusdefiníciókban

Implementálhatunk metódusokat structokon és enumokon (ahogy az 5. fejezetben
tettük), és a definícióikban generikus típusokat is használhatunk. A 10-9.
listázás a 10-6. listázásban definiált `Point<T>` structot mutatja, egy rajta
implementált `x` nevű metódussal.

<Listing number="10-9" file-name="src/main.rs" caption="Egy `x` nevű metódus implementálása a `Point<T>` structon, amely a `T` típusú `x` mezőre mutató referenciát ad vissza">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Itt egy `x` nevű metódust definiáltunk a `Point<T>`-n, amely az `x` mezőben
lévő adatra mutató referenciát ad vissza.

Vedd figyelembe, hogy a `T`-t közvetlenül az `impl` után deklarálnunk kell,
hogy a `T`-vel jelezhessük: a `Point<T>` típuson implementálunk metódusokat.
Azzal, hogy a `T`-t generikus típusként deklaráljuk az `impl` után, a Rust
felismeri, hogy a `Point` csúcsos zárójeleiben álló típus generikus, nem pedig
konkrét típus. Választhattunk volna ennek a generikus paraméternek a
structdefinícióban deklarált generikus paraméterétől eltérő nevet is, de
konvenció szerint ugyanazt a nevet használjuk. Ha olyan `impl` blokkba írsz
metódust, amely generikus típust deklarál, az a metódus a típus minden
példányán definiálva lesz, függetlenül attól, hogy végül milyen konkrét típus
lép a generikus típus helyébe.

Megszorításokat is megadhatunk a generikus típusokra, amikor metódusokat
definiálunk a típuson. Például implementálhatnánk metódusokat csak `Point<f32>`
példányokra ahelyett, hogy bármilyen generikus típusú `Point<T>` példányokra
tennénk. A 10-10. listázásban az `f32` konkrét típust használjuk, ami azt
jelenti, hogy nem deklarálunk semmilyen típust az `impl` után.

<Listing number="10-10" file-name="src/main.rs" caption="Egy `impl` blokk, amely csak olyan structra vonatkozik, amelyben a `T` generikus típusparaméter helyén egy adott konkrét típus áll">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Ez a kód azt jelenti, hogy a `Point<f32>` típusnak lesz egy
`distance_from_origin` metódusa; a `Point<T>` azon példányainak, ahol a `T` nem
`f32` típusú, nem lesz definiálva ez a metódus. A metódus azt méri meg, milyen
messze van a pontunk a (0.0, 0.0) koordinátájú ponttól, és olyan matematikai
műveleteket használ, amelyek csak lebegőpontos típusokra érhetők el.

Egy structdefinícióban szereplő generikus típusparaméterek nem mindig azonosak
azokkal, amelyeket ugyanannak a structnak a metódusszignatúráiban használsz. A
10-11. listázás az `X1` és `Y1` generikus típusokat használja a `Point`
structhoz, az `X2`-t és `Y2`-t pedig a `mixup` metódus szignatúrájához, hogy a
példa világosabb legyen. A metódus új `Point` példányt hoz létre, amelyben az
`x` érték a `self` `Point`-ból (`X1` típusú), az `y` érték pedig az átadott
`Point`-ból (`Y2` típusú) származik.

<Listing number="10-11" file-name="src/main.rs" caption="Egy metódus, amely a structja definíciójától eltérő generikus típusokat használ">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

A `main`-ben olyan `Point`-ot definiáltunk, amelynek az `x`-e `i32` (`5`
értékkel), az `y`-ja pedig `f64` (`10.4` értékkel). A `p2` változó olyan `Point`
struct, amelynek az `x`-e egy string slice (`"Hello"` értékkel), az `y`-ja pedig
egy `char` (`c` értékkel). Ha meghívjuk a `mixup`-ot a `p1`-en a `p2`
argumentummal, megkapjuk a `p3`-at, amelynek az `x`-e `i32` lesz, mert az `x` a
`p1`-ből jött. A `p3` változó `y`-ja `char` lesz, mert az `y` a `p2`-ből jött. A
`println!` makró hívása a `p3.x = 5, p3.y = c` szöveget fogja kiírni.

Ennek a példának az a célja, hogy bemutasson egy olyan helyzetet, amelyben
bizonyos generikus paramétereket az `impl`-lel, másokat pedig a
metódusdefinícióval deklarálunk. Itt az `X1` és `Y1` generikus paramétereket az
`impl` után deklaráljuk, mert a structdefinícióhoz tartoznak. Az `X2` és `Y2`
generikus paramétereket az `fn mixup` után deklaráljuk, mert csak a metódus
szempontjából relevánsak.

### A generikusokat használó kód teljesítménye {#performance-of-code-using-generics}

Talán azon töprengsz, hogy jár-e futásidejű költséggel a generikus
típusparaméterek használata. A jó hír az, hogy a generikus típusok használatától
a programod nem fut lassabban, mint konkrét típusokkal futna.

Ezt a Rust úgy éri el, hogy fordítási időben elvégzi a generikusokat használó
kód monomorfizációját. A _monomorfizáció_ az a folyamat, amelynek során a
generikus kódból specifikus kód lesz azáltal, hogy behelyettesíti a fordításkor
használt konkrét típusokat. Ebben a folyamatban a fordító azoknak a lépéseknek
az ellenkezőjét végzi el, amelyekkel a 10-5. listázásban a generikus függvényt
létrehoztuk: a fordító megnézi az összes olyan helyet, ahol generikus kódot
hívnak meg, és kódot generál azokra a konkrét típusokra, amelyekkel a generikus
kódot meghívják.

Nézzük meg, hogyan működik ez, a standard könyvtár generikus `Option<T>`
enumjának példáján:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Amikor a Rust lefordítja ezt a kódot, elvégzi a monomorfizációt. Ennek során a
fordító beolvassa az `Option<T>` példányokban használt értékeket, és az
`Option<T>` két fajtáját azonosítja: az egyik `i32`, a másik `f64`. Ezért az
`Option<T>` generikus definícióját két, `i32`-re és `f64`-re specializált
definícióvá bontja ki, és így a generikus definíciót a specifikusakra cseréli.

A kód monomorfizált változata a következőhöz hasonlóan néz ki (a fordító más
neveket használ, mint amiket mi itt a szemléltetés kedvéért):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

A generikus `Option<T>` helyére a fordító által létrehozott specifikus
definíciók kerülnek. Mivel a Rust a generikus kódot olyan kóddá fordítja, amely
minden példányban megadja a típust, semmilyen futásidejű költséget nem fizetünk
a generikusok használatáért. Amikor a kód lefut, ugyanúgy teljesít, mintha
minden definíciót kézzel másoltunk volna le. A monomorfizáció folyamata
rendkívül hatékonnyá teszi a Rust generikusait futásidőben.
