## Haladó trait-ek {#advanced-traits}

A trait-ekkel először a 10. fejezet [„Osztott viselkedés definiálása
trait-ekkel”][traits]<!-- ignore --> című szakaszában foglalkoztunk, de a
haladóbb részleteket nem tárgyaltuk. Most, hogy már többet tudsz a Rustról,
belemerülhetünk a részletekbe.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Trait-ek definiálása asszociált típusokkal

Az _asszociált típusok_ úgy kötnek össze egy típushelyettesítőt egy trait-tel,
hogy a trait metódusdefiníciói használhatják ezeket a helyettesítő típusokat a
szignatúrájukban. A trait implementálója adja meg azt a konkrét típust, amelyet
az adott implementációban a helyettesítő típus helyett használunk. Így olyan
trait-et definiálhatunk, amely bizonyos típusokat használ anélkül, hogy pontosan
tudnunk kellene, mik ezek a típusok, egészen a trait implementálásáig.

Az ebben a fejezetben tárgyalt haladó képességek nagy részét úgy jellemeztük,
mint amelyekre ritkán van szükség. Az asszociált típusok valahol középen
helyezkednek el: ritkábban használjuk őket, mint a könyv többi részében
bemutatott képességeket, de gyakrabban, mint az ebben a fejezetben tárgyalt
többi elemet.

Az asszociált típussal rendelkező trait-ek egyik példája a standard könyvtár
`Iterator` trait-je. Az asszociált típus neve `Item`, és azoknak az értékeknek a
típusát helyettesíti, amelyeken az `Iterator` trait-et implementáló típus
iterál. Az `Iterator` trait definíciója a 20-13. listában látható.

<Listing number="20-13" caption="Az `Iterator` trait definíciója, amelynek van egy `Item` asszociált típusa">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Az `Item` típus egy helyettesítő, és a `next` metódus definíciója azt mutatja,
hogy az `Option<Self::Item>` típusú értékeket ad vissza. Az `Iterator` trait
implementálói megadják az `Item` konkrét típusát, a `next` metódus pedig egy
`Option`-t ad vissza, amely ilyen konkrét típusú értéket tartalmaz.

Az asszociált típusok elsőre a generikusokhoz hasonló fogalomnak tűnhetnek,
hiszen az utóbbiak is lehetővé teszik, hogy úgy definiáljunk egy függvényt,
hogy nem adjuk meg, milyen típusokat tud kezelni. Hogy megvizsgáljuk a két
fogalom közötti különbséget, nézzük meg az `Iterator` trait egy implementációját
egy `Counter` nevű típuson, amely az `Item` típust `u32`-ként adja meg:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Ez a szintaxis a generikusokéhoz hasonlónak tűnik. Miért ne definiálhatnánk
tehát az `Iterator` trait-et egyszerűen generikusokkal, ahogy a 20-14. listában
látható?

<Listing number="20-14" caption="Az `Iterator` trait feltételezett definíciója generikusokkal">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

A különbség az, hogy generikusok használatakor, ahogy a 20-14. listában,
minden implementációban annotálnunk kell a típusokat; mivel az `Iterator<String>
for Counter`-t vagy bármely más típust is implementálhatnánk, több `Iterator`
implementációnk is lehetne a `Counter`-hez. Más szóval, ha egy trait-nek van
generikus paramétere, akkor egy típusra többször is implementálható úgy, hogy a
generikus típusparaméterek konkrét típusait minden alkalommal megváltoztatjuk.
Amikor a `Counter`-en a `next` metódust használnánk, típusannotációkkal kellene
jeleznünk, melyik `Iterator` implementációt akarjuk használni.

Asszociált típusokkal nem kell típusokat annotálnunk, mert egy trait-et nem
implementálhatunk többször ugyanarra a típusra. A 20-13. listában, ahol a
definíció asszociált típusokat használ, csak egyszer választhatjuk meg az `Item`
típusát, mert csak egyetlen `impl Iterator for Counter` lehet. Nem kell
mindenhol megadnunk, hogy `u32` értékek iterátorát szeretnénk, ahol a
`Counter`-en meghívjuk a `next`-et.

Az asszociált típusok a trait szerződésének is részévé válnak: a trait
implementálóinak típust kell adniuk az asszociált típushelyettesítő helyére. Az
asszociált típusok neve gyakran leírja, hogyan használjuk majd a típust, és jó
gyakorlat az asszociált típust dokumentálni az API-dokumentációban.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Alapértelmezett generikus paraméterek és operátor-túlterhelés

Amikor generikus típusparamétereket használunk, megadhatunk a generikus
típushoz egy alapértelmezett konkrét típust. Ezzel feleslegessé válik, hogy a
trait implementálói konkrét típust adjanak meg, ha az alapértelmezett típus
megfelel. Alapértelmezett típust a generikus típus deklarálásakor a
`<PlaceholderType=ConcreteType>` szintaxissal adhatsz meg.

Kiváló példa arra a helyzetre, ahol ez a technika hasznos, az
_operátor-túlterhelés_, amellyel egy operátor (például a `+`) viselkedését
szabhatod testre bizonyos helyzetekben.

A Rust nem engedi, hogy saját operátorokat hozz létre, vagy hogy tetszőleges
operátorokat terhelj túl. A `std::ops`-ban felsorolt műveleteket és a hozzájuk
tartozó trait-eket viszont túlterhelheted úgy, hogy implementálod az
operátorhoz tartozó trait-et. Például a 20-15. listában a `+` operátort
terheljük túl, hogy két `Point` példányt össze tudjunk adni. Ezt úgy tesszük,
hogy implementáljuk az `Add` trait-et egy `Point` structon.

<Listing number="20-15" file-name="src/main.rs" caption="Az `Add` trait implementálása a `+` operátor túlterhelésére `Point` példányokhoz">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Az `add` metódus összeadja két `Point` példány `x` értékeit és két `Point`
példány `y` értékeit, így hozva létre egy új `Point`-ot. Az `Add` trait-nek van
egy `Output` nevű asszociált típusa, amely meghatározza az `add` metódus
visszatérési típusát.

Az alapértelmezett generikus típus ebben a kódban az `Add` trait-ben van. Íme a
definíciója:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Ennek a kódnak nagyjából ismerősnek kell lennie: egy trait egy metódussal és
egy asszociált típussal. Az új rész a `Rhs=Self`: ezt a szintaxist hívjuk
_alapértelmezett típusparamétereknek_. Az `Rhs` generikus típusparaméter (a
„right-hand side”, azaz jobb oldal rövidítése) az `add` metódus `rhs`
paraméterének típusát adja meg. Ha az `Add` trait implementálásakor nem adunk
meg konkrét típust az `Rhs`-hez, akkor az `Rhs` típusa alapértelmezés szerint
`Self` lesz, vagyis az a típus, amelyre az `Add`-et implementáljuk.

Amikor az `Add`-et a `Point`-ra implementáltuk, az `Rhs` alapértelmezését
használtuk, mert két `Point` példányt akartunk összeadni. Nézzünk most egy
példát az `Add` trait olyan implementálására, ahol az alapértelmezett érték
helyett testre akarjuk szabni az `Rhs` típust.

Van két structunk, a `Millimeters` és a `Meters`, amelyek különböző
mértékegységekben tárolnak értékeket. Egy meglévő típusnak ez a vékony
becsomagolása egy másik structba a _newtype minta_ néven ismert, amelyet
részletesebben a [„Külső trait-ek implementálása a newtype
mintával”][newtype]<!-- ignore --> című szakaszban írunk le. Milliméterben
megadott értékeket szeretnénk méterben megadott értékekhez adni úgy, hogy az
`Add` implementációja helyesen végezze el az átváltást. Az `Add`-et a
`Millimeters`-re implementálhatjuk úgy, hogy az `Rhs` a `Meters` legyen, ahogy
a 20-16. listában látható.

<Listing number="20-16" file-name="src/lib.rs" caption="Az `Add` trait implementálása a `Millimeters`-en, hogy össze lehessen adni a `Millimeters`-t és a `Meters`-t">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Ahhoz, hogy a `Millimeters`-t és a `Meters`-t összeadhassuk, `impl
Add<Meters>`-t adunk meg, ezzel állítva be az `Rhs` típusparaméter értékét a
`Self` alapértelmezés helyett.

Az alapértelmezett típusparamétereket főként két módon fogod használni:

1. Egy típus kiterjesztésére a meglévő kód megtörése nélkül
2. Olyan testreszabás engedélyezésére, amelyre a legtöbb felhasználónak nem lesz
   szüksége konkrét esetekben

A standard könyvtár `Add` trait-je a második célra példa: általában két azonos
típust adsz össze, de az `Add` trait lehetőséget ad az ezen túlmutató
testreszabásra. Az `Add` trait definíciójában az alapértelmezett típusparaméter
használata azt jelenti, hogy legtöbbször nem kell megadnod az extra
paramétert. Más szóval nincs szükség némi implementációs sablonkódra, ami
megkönnyíti a trait használatát.

Az első cél hasonlít a másodikra, csak fordítva: ha egy meglévő trait-hez
típusparamétert akarsz adni, adhatsz neki alapértelmezett értéket, hogy a trait
funkcionalitása a meglévő implementációs kód megtörése nélkül bővíthető legyen.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Azonos nevű metódusok megkülönböztetése

A Rustban semmi nem akadályozza meg, hogy egy trait-nek olyan metódusa legyen,
amelynek a neve megegyezik egy másik trait metódusának nevével, és azt sem
akadályozza meg a Rust, hogy mindkét trait-et ugyanarra a típusra implementáld.
Az is lehetséges, hogy közvetlenül a típuson definiálj olyan metódust, amelynek
a neve megegyezik a trait-ek metódusaiéval.

Amikor azonos nevű metódusokat hívsz, meg kell mondanod a Rustnak, melyiket
akarod használni. Nézd meg a 20-17. listában lévő kódot, ahol két trait-et
definiáltunk, a `Pilot`-ot és a `Wizard`-ot, és mindkettőnek van egy `fly` nevű
metódusa. Ezután mindkét trait-et implementáljuk egy `Human` típusra, amelynek
már van rajta implementálva egy `fly` nevű metódusa. Mindegyik `fly` metódus
mást csinál.

<Listing number="20-17" file-name="src/main.rs" caption="Két trait-et úgy definiálunk, hogy legyen `fly` metódusuk, és implementáljuk őket a `Human` típuson, amelyre közvetlenül is implementálunk egy `fly` metódust.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Amikor egy `Human` példányon meghívjuk a `fly`-t, a fordító alapértelmezés
szerint azt a metódust hívja meg, amely közvetlenül a típusra van
implementálva, ahogy a 20-18. listában látható.

<Listing number="20-18" file-name="src/main.rs" caption="A `fly` hívása egy `Human` példányon">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Ezt a kódot futtatva a `*waving arms furiously*` szöveg jelenik meg, ami azt
mutatja, hogy a Rust a közvetlenül a `Human`-ra implementált `fly` metódust
hívta meg.

Ahhoz, hogy a `Pilot` vagy a `Wizard` trait `fly` metódusát hívjuk meg,
kifejezettebb szintaxist kell használnunk annak megadására, melyik `fly`
metódusra gondolunk. A 20-19. lista mutatja be ezt a szintaxist.

<Listing number="20-19" file-name="src/main.rs" caption="Annak megadása, melyik trait `fly` metódusát akarjuk hívni">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Ha a metódusnév elé kiírjuk a trait nevét, azzal egyértelművé tesszük a Rust
számára, melyik `fly` implementációt akarjuk hívni. Írhatnánk azt is, hogy
`Human::fly(&person)`, ami egyenértékű a 20-19. listában használt
`person.fly()`-jal, de ezt kicsit hosszabb leírni, ha nincs szükség
egyértelműsítésre.

Ezt a kódot futtatva a következőt kapjuk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Mivel a `fly` metódusnak van `self` paramétere, ha két olyan _típusunk_ lenne,
amely ugyanazt az egy _trait-et_ implementálja, a Rust a `self` típusa alapján ki
tudná találni, a trait melyik implementációját használja.

Azoknak az asszociált függvényeknek viszont, amelyek nem metódusok, nincs
`self` paraméterük. Ha több olyan típus vagy trait van, amely azonos nevű, nem
metódus függvényeket definiál, a Rust nem mindig tudja, melyikre gondolsz,
hacsak nem használsz teljesen minősített szintaxist. Például a 20-20. listában
egy állatmenhelyhez készítünk trait-et, ahol minden kutyakölyköt Spotnak akarnak
elnevezni. Készítünk egy `Animal` trait-et egy `baby_name` nevű, nem metódus
asszociált függvénnyel. Az `Animal` trait-et a `Dog` structra implementáljuk,
amelyre közvetlenül is megadunk egy `baby_name` nevű, nem metódus asszociált
függvényt.

<Listing number="20-20" file-name="src/main.rs" caption="Egy trait asszociált függvénnyel és egy típus azonos nevű asszociált függvénnyel, amely a trait-et is implementálja">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Azt a kódot, amely minden kutyakölyköt Spotnak nevez el, a `Dog`-on definiált
`baby_name` asszociált függvényben implementáljuk. A `Dog` típus az `Animal`
trait-et is implementálja, amely az összes állat jellemzőit írja le. A
kutyakölyköket angolul „puppy”-nak hívják, és ez az `Animal` trait `Dog`-ra
vonatkozó implementációjában, az `Animal` trait-hez tartozó `baby_name`
függvényben jelenik meg.

A `main`-ben a `Dog::baby_name` függvényt hívjuk meg, amely a közvetlenül a
`Dog`-on definiált asszociált függvényt hívja. Ez a kód a következőt írja ki:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Ez a kimenet nem az, amit szerettünk volna. Azt a `baby_name` függvényt akarjuk
meghívni, amely a `Dog`-ra implementált `Animal` trait része, hogy a kód az `A
baby dog is called a puppy` szöveget írja ki. Az a technika, amellyel a 20-19.
listában megadtuk a trait nevét, itt nem segít; ha a `main`-t a 20-21. listában
lévő kódra cseréljük, fordítási hibát kapunk.

<Listing number="20-21" file-name="src/main.rs" caption="Kísérlet az `Animal` trait `baby_name` függvényének hívására, de a Rust nem tudja, melyik implementációt használja">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Mivel az `Animal::baby_name`-nek nincs `self` paramétere, és lehetnének más
típusok is, amelyek implementálják az `Animal` trait-et, a Rust nem tudja
kitalálni, az `Animal::baby_name` melyik implementációját akarjuk. Ezt a
fordítói hibát kapjuk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Ahhoz, hogy egyértelműsítsük, és megmondjuk a Rustnak, hogy az `Animal`
`Dog`-ra vonatkozó implementációját akarjuk használni, nem pedig az `Animal`
valamely más típusra vonatkozó implementációját, teljesen minősített
szintaxisra van szükségünk. A 20-22. lista mutatja be, hogyan használjuk a
teljesen minősített szintaxist.

<Listing number="20-22" file-name="src/main.rs" caption="Teljesen minősített szintaxis használata annak megadására, hogy az `Animal` trait `baby_name` függvényét akarjuk hívni a `Dog`-ra implementált változatban">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

A csúcsos zárójelek között típusannotációt adunk a Rustnak, amely jelzi, hogy
az `Animal` trait `baby_name` metódusát akarjuk hívni a `Dog`-ra implementált
változatban, vagyis azt mondjuk, hogy ehhez a függvényhíváshoz a `Dog` típust
`Animal`-ként akarjuk kezelni. Ez a kód most már azt írja ki, amit szeretnénk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Általánosan a teljesen minősített szintaxist a következőképpen definiáljuk:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Azoknál az asszociált függvényeknél, amelyek nem metódusok, nem lenne
`receiver`: csak a többi argumentum listája szerepelne. Teljesen minősített
szintaxist bárhol használhatnál, ahol függvényeket vagy metódusokat hívsz.
Ugyanakkor elhagyhatod ennek a szintaxisnak minden olyan részét, amelyet a Rust
a program más információiból ki tud következtetni. Erre a bőbeszédűbb
szintaxisra csak azokban az esetekben van szükséged, amikor több azonos nevű
implementáció van, és a Rustnak segítségre van szüksége annak azonosításához,
melyiket akarod hívni.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Supertrait-ek használata

Néha olyan trait-definíciót írhatsz, amely egy másik traittől függ: ahhoz, hogy
egy típus implementálja az első trait-et, meg akarod követelni, hogy az adott
típus a második trait-et is implementálja. Ezt azért teszed, hogy a
trait-definíciód használhassa a második trait asszociált elemeit. Azt a trait-et,
amelyre a trait-definíciód támaszkodik, a trait-ed _supertraitjének_ nevezzük.

Tegyük fel például, hogy szeretnénk készíteni egy `OutlinePrint` trait-et egy
`outline_print` metódussal, amely egy adott értéket úgy formázva ír ki, hogy az
csillagokkal legyen keretezve. Vagyis egy olyan `Point` struct esetén, amely
implementálja a standard könyvtár `Display` trait-jét úgy, hogy az `(x, y)`
alakot eredményezi, amikor az `outline_print`-et meghívjuk egy olyan `Point`
példányon, ahol az `x` értéke `1`, az `y` értéke pedig `3`, a következőnek kell
megjelennie:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Az `outline_print` metódus implementációjában a `Display` trait
funkcionalitását akarjuk használni. Ezért meg kell adnunk, hogy az
`OutlinePrint` trait csak olyan típusokra működjön, amelyek a `Display`-t is
implementálják, és így biztosítják azt a funkcionalitást, amelyre az
`OutlinePrint`-nek szüksége van. Ezt a trait-definícióban tehetjük meg az
`OutlinePrint: Display` megadásával. Ez a technika hasonlít ahhoz, mintha trait
boundot adnánk a trait-hez. A 20-23. lista az `OutlinePrint` trait egy
implementációját mutatja.

<Listing number="20-23" file-name="src/main.rs" caption="Az `OutlinePrint` trait implementálása, amely megköveteli a `Display` funkcionalitását">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Mivel megadtuk, hogy az `OutlinePrint`-hez szükség van a `Display` trait-re,
használhatjuk a `to_string` függvényt, amely automatikusan implementálva van
minden `Display`-t implementáló típusra. Ha úgy próbálnánk használni a
`to_string`-et, hogy nem tennénk ki a kettőspontot, és nem adnánk meg a
`Display` trait-et a trait neve után, olyan hibát kapnánk, amely szerint a
`&Self` típushoz nem található `to_string` nevű metódus az aktuális hatókörben.

Nézzük meg, mi történik, ha az `OutlinePrint`-et olyan típusra próbáljuk
implementálni, amely nem implementálja a `Display`-t, például a `Point`
structra:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Olyan hibát kapunk, amely szerint a `Display` szükséges, de nincs
implementálva:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Ennek javításához implementáljuk a `Display`-t a `Point`-ra, és így teljesítjük
az `OutlinePrint` által megkövetelt megkötést, így:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Ezután az `OutlinePrint` trait `Point`-ra való implementálása sikeresen
lefordul, és meghívhatjuk az `outline_print`-et egy `Point` példányon, hogy
csillagokból álló keretben jelenítsük meg.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Külső trait-ek implementálása a newtype mintával {#implementing-external-traits-with-the-newtype-pattern}

A 10. fejezet [„Trait implementálása egy
típuson”][implementing-a-trait-on-a-type]<!-- ignore --> című szakaszában
megemlítettük az orphan szabályt, amely szerint egy trait-et csak akkor
implementálhatunk egy típusra, ha vagy a trait, vagy a típus, vagy mindkettő
lokális a crate-ünkben. Ezt a korlátozást megkerülhetjük a newtype mintával,
amelynek lényege, hogy egy tuple structban új típust hozunk létre. (A tuple
structokról az 5. fejezet [„Különböző típusok létrehozása tuple
structokkal”][tuple-structs]<!-- ignore --> című szakaszában volt szó.) A tuple
structnak egyetlen mezője lesz, és vékony burkolóként veszi körül azt a
típust, amelyre trait-et szeretnénk implementálni. Ekkor a burkolótípus lokális
a crate-ünkben, így implementálhatjuk rá a trait-et. A _newtype_ olyan kifejezés,
amely a Haskell programozási nyelvből származik. Ennek a mintának a
használatáért nem kell futásidejű teljesítménybüntetést fizetni, a burkolótípus
pedig fordítási időben eltűnik.

Példaként tegyük fel, hogy a `Display`-t szeretnénk implementálni a `Vec<T>`-re,
amit az orphan szabály közvetlenül nem enged meg, mert a `Display` trait és a
`Vec<T>` típus is a crate-ünkön kívül van definiálva. Készíthetünk egy `Wrapper`
structot, amely egy `Vec<T>` példányt tárol; ezután a `Display`-t
implementálhatjuk a `Wrapper`-re, és használhatjuk a `Vec<T>` értéket, ahogy a
20-24. listában látható.

<Listing number="20-24" file-name="src/main.rs" caption="Egy `Wrapper` típus létrehozása a `Vec<String>` köré, hogy implementálhassuk a `Display`-t">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

A `Display` implementációja a `self.0`-t használja a belső `Vec<T>` elérésére,
mert a `Wrapper` tuple struct, és a `Vec<T>` a tuple 0. indexű eleme. Ezután a
`Display` trait funkcionalitását használhatjuk a `Wrapper`-en.

Ennek a technikának a hátránya, hogy a `Wrapper` új típus, így nincsenek meg
rajta annak az értéknek a metódusai, amelyet tárol. A `Vec<T>` összes metódusát
közvetlenül a `Wrapper`-re kellene implementálnunk úgy, hogy a metódusok a
`self.0`-nak delegálják a feladatot; ez tenné lehetővé, hogy a `Wrapper`-t
pontosan úgy kezeljük, mint egy `Vec<T>`-t. Ha azt szeretnénk, hogy az új
típusnak megvan minden metódusa, amivel a belső típus rendelkezik, megoldás
lehet a `Deref` trait implementálása a `Wrapper`-en úgy, hogy az a belső típust
adja vissza (a `Deref` trait implementálásáról a 15. fejezet [„Smart pointerek
kezelése közönséges referenciaként”][smart-pointer-deref]<!-- ignore --> című
szakaszában beszéltünk). Ha nem akarnánk, hogy a `Wrapper` típusnak megvan a
belső típus összes metódusa – például azért, hogy korlátozzuk a `Wrapper` típus
viselkedését –, akkor csak azokat a metódusokat kellene kézzel implementálnunk,
amelyeket valóban szeretnénk.

Ez a newtype minta akkor is hasznos, ha nincsenek trait-ek a képben. Váltsunk
témát, és nézzünk meg néhány haladó módot a Rust típusrendszerével való
munkára.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
