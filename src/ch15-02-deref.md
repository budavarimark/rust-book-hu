<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Smart pointerek kezelése közönséges referenciaként {#treating-smart-pointers-like-regular-references}

A `Deref` trait implementálásával testre szabhatod a _dereferáló operátor_, `*`
viselkedését (nem tévesztendő össze a szorzás- vagy a glob operátorral). Ha úgy
implementálod a `Deref` trait-et, hogy egy smart pointert közönséges
referenciaként lehessen kezelni, akkor írhatsz olyan kódot, amely referenciákkal
dolgozik, és ezt a kódot smart pointerekkel is használhatod.

Először nézzük meg, hogyan működik a dereferáló operátor közönséges
referenciákkal. Ezután megpróbálunk definiálni egy saját típust, amely a
`Box<T>`-hez hasonlóan viselkedik, és megnézzük, miért nem működik a dereferáló
operátor referenciaként az újonnan definiált típusunkon. Feltárjuk, hogyan teszi
lehetővé a `Deref` trait implementálása, hogy a smart pointerek a referenciákhoz
hasonlóan működjenek. Végül megnézzük a Rust deref coercion képességét, és azt,
hogyan teszi lehetővé, hogy referenciákkal és smart pointerekkel egyaránt
dolgozzunk.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### A referencia követése az értékig

A közönséges referencia is pointertípus, és a pointerre úgy is gondolhatunk, mint
egy nyílra, amely egy máshol tárolt értékre mutat. A 15-6. listában létrehozunk
egy referenciát egy `i32` értékre, majd a dereferáló operátorral követjük a
referenciát az értékig.

<Listing number="15-6" file-name="src/main.rs" caption="A dereferáló operátor használata egy `i32` értékre mutató referencia követéséhez">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Az `x` változó az `5` `i32` értéket tartalmazza. Az `y`-t egy `x`-re mutató
referenciával tesszük egyenlővé. Állíthatjuk, hogy `x` egyenlő `5`-tel. Ha
azonban az `y`-ban lévő értékről akarunk állítást tenni, akkor a `*y` alakot kell
használnunk, hogy kövessük a referenciát addig az értékig, amelyre mutat (innen
a _dereferálás_ elnevezés), így a fordító a tényleges értéket tudja
összehasonlítani. Miután dereferáltuk az `y`-t, hozzáférünk ahhoz az egész
értékhez, amelyre az `y` mutat, és amelyet összehasonlíthatunk `5`-tel.

Ha ehelyett az `assert_eq!(5, y);` sort próbálnánk megírni, ezt a fordítási hibát
kapnánk:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Egy szám és egy számra mutató referencia összehasonlítása nem megengedett, mert
különböző típusúak. A dereferáló operátort kell használnunk, hogy kövessük a
referenciát addig az értékig, amelyre mutat.

### A `Box<T>` használata referenciaként

A 15-6. lista kódját átírhatjuk úgy, hogy referencia helyett `Box<T>`-t
használjon; a 15-7. listában a `Box<T>`-n alkalmazott dereferáló operátor
ugyanúgy működik, mint a 15-6. listában a referencián alkalmazott dereferáló
operátor.

<Listing number="15-7" file-name="src/main.rs" caption="A dereferáló operátor használata egy `Box<i32>` értéken">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

A fő különbség a 15-7. és a 15-6. lista között az, hogy itt az `y`-t egy box
példányává tesszük, amely az `x` egy másolt értékére mutat, nem pedig egy
referenciává, amely az `x` értékére mutat. Az utolsó állításban ugyanúgy
használhatjuk a dereferáló operátort a box pointerének követésére, ahogy akkor
tettük, amikor az `y` referencia volt. Ezután egy saját box típus definiálásával
feltárjuk, mi az a különleges tulajdonsága a `Box<T>`-nek, amely lehetővé teszi
számunkra a dereferáló operátor használatát.

### Saját smart pointer definiálása

Építsünk egy burkolótípust, amely hasonló a standard könyvtár által biztosított
`Box<T>` típushoz, hogy megtapasztaljuk, miben viselkednek a smart pointer
típusok alapértelmezés szerint másképp, mint a referenciák. Ezután megnézzük,
hogyan adhatjuk hozzá a dereferáló operátor használatának képességét.

> Megjegyzés: egy nagy különbség van a `MyBox<T>` típus, amelyet mindjárt
> megépítünk, és a valódi `Box<T>` között: a mi változatunk nem a heapen fogja
> tárolni az adatait. Ebben a példában a `Deref` trait-re összpontosítunk, ezért
> kevésbé fontos, hol tárolódik ténylegesen az adat, mint a pointerszerű
> viselkedés.

A `Box<T>` típus végső soron egyelemű tuple structként van definiálva, ezért a
15-8. lista ugyanígy definiálja a `MyBox<T>` típust. Definiálunk egy `new`
függvényt is, hogy megfeleljen a `Box<T>`-n definiált `new` függvénynek.

<Listing number="15-8" file-name="src/main.rs" caption="A `MyBox<T>` típus definiálása">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Definiálunk egy `MyBox` nevű structot, és deklarálunk egy `T` generikus
paramétert, mert azt szeretnénk, hogy a típusunk bármilyen típusú értéket
tárolhasson. A `MyBox` típus egy egyelemű tuple struct, amelynek eleme `T`
típusú. A `MyBox::new` függvény egyetlen `T` típusú paramétert vesz át, és egy
olyan `MyBox` példánnyal tér vissza, amely a kapott értéket tárolja.

Próbáljuk meg hozzáadni a 15-7. listában lévő `main` függvényt a 15-8. listához,
és módosítsuk úgy, hogy a `Box<T>` helyett az általunk definiált `MyBox<T>`
típust használja. A 15-9. lista kódja nem fog lefordulni, mert a Rust nem tudja,
hogyan kell dereferálni a `MyBox`-ot.

<Listing number="15-9" file-name="src/main.rs" caption="Kísérlet a `MyBox<T>` ugyanolyan használatára, ahogy a referenciákat és a `Box<T>`-t használtuk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Íme a keletkező fordítási hiba:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

A `MyBox<T>` típusunkat nem lehet dereferálni, mert nem implementáltuk ezt a
képességet a típusunkon. Ahhoz, hogy a `*` operátorral dereferálni lehessen,
implementáljuk a `Deref` trait-et.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### A `Deref` trait implementálása

Ahogy a 10. fejezet [„Trait implementálása egy típuson”][impl-trait]<!-- ignore
--> című szakaszában tárgyaltuk, egy trait implementálásához a trait által
megkövetelt metódusok implementációját kell megadnunk. A standard könyvtár által
biztosított `Deref` trait egyetlen, `deref` nevű metódus implementálását követeli
meg, amely borrowolja a `self`-et, és a belső adatra mutató referenciával tér
vissza. A 15-10. lista a `Deref` egy implementációját tartalmazza, amelyet a
`MyBox<T>` definíciójához adhatunk hozzá.

<Listing number="15-10" file-name="src/main.rs" caption="A `Deref` implementálása a `MyBox<T>`-n">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

A `type Target = T;` szintaxis egy asszociált típust definiál a `Deref` trait
számára. Az asszociált típusok egy kissé más módját jelentik a generikus
paraméterek deklarálásának, de egyelőre nem kell velük foglalkoznod; a 20.
fejezetben részletesebben is szó lesz róluk.

A `deref` metódus törzsét a `&self.0` kifejezéssel töltjük ki, hogy a `deref` egy
referenciát adjon vissza arra az értékre, amelyhez a `*` operátorral szeretnénk
hozzáférni; emlékezz vissza az 5. fejezet [„Különböző típusok létrehozása tuple
structokkal”][tuple-structs]<!-- ignore --> című szakaszára, ahol arról volt szó,
hogy a `.0` egy tuple struct első értékéhez fér hozzá. A 15-9. listában szereplő
`main` függvény, amely a `*` operátort hívja meg a `MyBox<T>` értéken, immár
lefordul, és az állítások teljesülnek!

A `Deref` trait nélkül a fordító csak a `&` referenciákat tudja dereferálni. A
`deref` metódus adja meg a fordítónak azt a képességet, hogy fogjon egy
tetszőleges, `Deref`-et implementáló típusú értéket, és meghívja rajta a `deref`
metódust, hogy olyan referenciát kapjon, amelyet már tud dereferálni.

Amikor a 15-9. listában beírtuk a `*y`-t, a Rust a színfalak mögött valójában ezt
a kódot futtatta:

```rust,ignore
*(y.deref())
```

A Rust a `*` operátort a `deref` metódus hívására, majd egy egyszerű
dereferálásra cseréli, hogy ne kelljen azon gondolkodnunk, meg kell-e hívnunk a
`deref` metódust. A Rustnak ez a képessége lehetővé teszi, hogy olyan kódot
írjunk, amely azonosan működik akár közönséges referenciánk van, akár egy
`Deref`-et implementáló típusunk.

Annak, hogy a `deref` metódus egy értékre mutató referenciával tér vissza, és
hogy a `*(y.deref())` kifejezésben a zárójelen kívüli egyszerű dereferálás
továbbra is szükséges, az ownership rendszerhez van köze. Ha a `deref` metódus az
értékre mutató referencia helyett közvetlenül az értéket adná vissza, akkor az
érték kimozdulna (move) a `self`-ből. Ebben az esetben – és a legtöbb esetben,
amikor a dereferáló operátort használjuk – nem szeretnénk átvenni a `MyBox<T>`
belsejében lévő érték ownershipjét.

Vedd észre, hogy a `*` operátort minden alkalommal, amikor egy `*`-ot használunk
a kódunkban, csak egyszer cseréli le a `deref` metódus hívása, majd a `*`
operátor hívása. Mivel a `*` operátor helyettesítése nem rekurzálódik a
végtelenségig, végül `i32` típusú adatot kapunk, ami megfelel a 15-9. listában az
`assert_eq!`-ben szereplő `5`-nek.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Deref coercion használata függvényekben és metódusokban

A _deref coercion_ egy `Deref` trait-et implementáló típusra mutató referenciát
alakít át egy másik típusra mutató referenciává. Például a deref coercion a
`&String`-et `&str`-ré tudja alakítani, mert a `String` úgy implementálja a
`Deref` trait-et, hogy az `&str`-t ad vissza. A deref coercion egy kényelmi
szolgáltatás, amelyet a Rust a függvények és metódusok argumentumain végez, és
csak olyan típusokon működik, amelyek implementálják a `Deref` trait-et.
Automatikusan megtörténik, amikor egy adott típusú értékre mutató referenciát
adunk át argumentumként egy olyan függvénynek vagy metódusnak, amelynek
definíciójában a paraméter típusa nem egyezik meg vele. A `deref` metódus
hívásainak sorozata alakítja át az általunk megadott típust azzá a típussá,
amelyre a paraméternek szüksége van.

A deref coercion azért került bele a Rustba, hogy a függvény- és
metódushívásokat író programozóknak ne kelljen annyi explicit referenciát és
dereferálást kiírniuk a `&` és a `*` jelekkel. A deref coercion képességének
köszönhetően több olyan kódot is írhatunk, amely referenciákkal és smart
pointerekkel egyaránt működik.

Hogy a deref coercion működés közben is lássuk, használjuk a 15-8. listában
definiált `MyBox<T>` típust, valamint a `Deref` implementációját, amelyet a
15-10. listában adtunk hozzá. A 15-11. lista egy olyan függvény definícióját
mutatja, amelynek string slice paramétere van.

<Listing number="15-11" file-name="src/main.rs" caption="Egy `hello` függvény, amelynek `name` paramétere `&str` típusú">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

A `hello` függvényt meghívhatjuk egy string slice-szal argumentumként, például
így: `hello("Rust");`. A deref coercion teszi lehetővé, hogy a `hello`-t egy
`MyBox<String>` típusú értékre mutató referenciával hívjuk meg, ahogy azt a
15-12. lista mutatja.

<Listing number="15-12" file-name="src/main.rs" caption="A `hello` meghívása egy `MyBox<String>` értékre mutató referenciával, ami a deref coercion miatt működik">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Itt a `hello` függvényt a `&m` argumentummal hívjuk meg, amely egy
`MyBox<String>` értékre mutató referencia. Mivel a 15-10. listában
implementáltuk a `Deref` trait-et a `MyBox<T>`-n, a Rust a `deref` hívásával a
`&MyBox<String>`-et `&String`-gé tudja alakítani. A standard könyvtár biztosítja
a `Deref` egy implementációját a `String`-en, amely egy string slice-t ad vissza;
ez megtalálható a `Deref` API-dokumentációjában. A Rust ismét meghívja a
`deref`-et, hogy a `&String`-ből `&str` legyen, ami megfelel a `hello` függvény
definíciójának.

Ha a Rust nem implementálná a deref coercion képességét, a 15-12. lista kódja
helyett a 15-13. lista kódját kellene megírnunk ahhoz, hogy a `hello`-t egy
`&MyBox<String>` típusú értékkel hívjuk meg.

<Listing number="15-13" file-name="src/main.rs" caption="A kód, amelyet meg kellene írnunk, ha a Rustban nem volna deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

A `(*m)` a `MyBox<String>`-et `String`-gé dereferálja. Ezután a `&` és a `[..]`
egy olyan string slice-t vesz a `String`-ből, amely az egész sztringgel egyenlő,
hogy megfeleljen a `hello` szignatúrájának. Ezt a deref coercion nélküli kódot a
sok jel miatt nehezebb olvasni, megírni és megérteni. A deref coercion lehetővé
teszi, hogy a Rust automatikusan elintézze helyettünk ezeket az átalakításokat.

Ha az érintett típusokra definiálva van a `Deref` trait, a Rust elemzi a
típusokat, és annyiszor használja a `Deref::deref`-et, ahányszor szükséges, hogy
olyan referenciát kapjon, amely megfelel a paraméter típusának. Fordítási időben
dől el, hányszor kell beszúrni a `Deref::deref`-et, így a deref coercion
kihasználásának nincs futásidejű költsége!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Deref coercion kezelése módosítható referenciákkal

Ahogyan a `Deref` trait-tel felülírhatod a `*` operátort a nem módosítható
referenciákon, úgy a `DerefMut` trait-tel felülírhatod a `*` operátort a
módosítható referenciákon.

A Rust három esetben végez deref coerciont, amikor megfelelő típusokat és
trait-implementációkat talál:

1. `&T`-ből `&U`-ba, ha `T: Deref<Target=U>`
2. `&mut T`-ből `&mut U`-ba, ha `T: DerefMut<Target=U>`
3. `&mut T`-ből `&U`-ba, ha `T: Deref<Target=U>`

Az első két eset azonos, azzal a különbséggel, hogy a második a módosíthatóságot
implementálja. Az első eset azt mondja ki, hogy ha van egy `&T`-d, és a `T`
implementálja a `Deref`-et valamilyen `U` típusra, akkor transzparens módon
kaphatsz egy `&U`-t. A második eset azt mondja ki, hogy ugyanez a deref coercion
megtörténik a módosítható referenciákra is.

A harmadik eset trükkösebb: a Rust egy módosítható referenciát nem módosíthatóvá
is átalakít. Fordítva viszont _nem_ lehetséges: a nem módosítható referenciákból
soha nem lesz módosítható referencia. A borrowing szabályai miatt, ha van egy
módosítható referenciád, akkor annak a módosítható referenciának az egyetlen
referenciának kell lennie az adott adatra (különben a program nem fordulna le).
Egy módosítható referencia egyetlen nem módosítható referenciává alakítása soha
nem sérti a borrowing szabályait. Egy nem módosítható referencia módosítható
referenciává alakítása viszont megkövetelné, hogy az eredeti nem módosítható
referencia legyen az egyetlen nem módosítható referencia arra az adatra, a
borrowing szabályai azonban ezt nem garantálják. Ezért a Rust nem élhet azzal a
feltételezéssel, hogy egy nem módosítható referencia módosítható referenciává
alakítása lehetséges.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
