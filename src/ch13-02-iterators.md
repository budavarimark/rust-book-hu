## Elemsorozatok feldolgozása iterátorokkal

Az iterátor minta lehetővé teszi, hogy egy elemsorozat minden elemén sorra
elvégezz valamilyen feladatot. Az iterátor felel az egyes elemeken való
végighaladás logikájáért és annak eldöntéséért, mikor ért véget a sorozat. Ha
iterátorokat használsz, ezt a logikát nem kell újra és újra magadnak
megírnod.

Rustban az iterátorok _lusták_ (lazy), vagyis addig nincs semmilyen hatásuk,
amíg meg nem hívsz olyan metódusokat, amelyek elfogyasztják az iterátort. A
13-10. lista kódja például létrehoz egy iterátort a `v1` vektor elemei fölött a
`Vec<T>` típuson definiált `iter` metódus meghívásával. Ez a kód önmagában nem
csinál semmi hasznosat.

<Listing number="13-10" file-name="src/main.rs" caption="Iterátor létrehozása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Az iterátort a `v1_iter` változó tárolja. Miután létrehoztunk egy iterátort,
sokféleképpen használhatjuk. A 3-5. listában egy tömbön haladtunk végig `for`
ciklussal, hogy minden elemén lefuttassunk valamilyen kódot. A motorháztető
alatt ez implicit módon létrehozott, majd elfogyasztott egy iterátort, de azt,
hogy ez pontosan hogyan működik, mostanáig elnagyoltuk.

A 13-11. lista példájában elválasztjuk az iterátor létrehozását az iterátor
`for` ciklusban való használatától. Amikor a `for` ciklust a `v1_iter`-ben lévő
iterátorral hívjuk meg, az iterátor minden eleme a ciklus egy-egy iterációjában
kerül felhasználásra, és a ciklus kiírja az egyes értékeket.

<Listing number="13-11" file-name="src/main.rs" caption="Iterátor használata `for` ciklusban">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Azokban a nyelvekben, amelyek standard könyvtára nem kínál iterátorokat,
ugyanezt a funkcionalitást valószínűleg úgy írnád meg, hogy egy változót 0-ról
indítasz, azzal a változóval indexeled a vektort, hogy megkapj egy értéket,
majd egy ciklusban növeled a változó értékét, amíg el nem éri a vektorban lévő
elemek számát.

Az iterátorok ezt az egész logikát elintézik helyetted, csökkentve az ismétlődő
kódot, amelyet esetleg elronthatnál. Az iterátorok nagyobb rugalmasságot adnak:
ugyanazt a logikát sokféle sorozattal használhatod, nem csak olyan
adatszerkezetekkel, amelyeket indexelni lehet, mint amilyenek a vektorok.
Nézzük meg, hogyan érik ezt el az iterátorok.

### Az `Iterator` trait és a `next` metódus {#the-iterator-trait-and-the-next-method}

Minden iterátor implementál egy `Iterator` nevű traitet, amelyet a standard
könyvtár definiál. A trait definíciója így néz ki:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Vedd észre, hogy ez a definíció néhány új szintaktikai elemet használ: a `type
Item` és a `Self::Item` egy asszociált típust definiál ehhez a traithez. Az
asszociált típusokról részletesen a 20. fejezetben lesz szó. Egyelőre csak
annyit kell tudnod, hogy ez a kód azt mondja: az `Iterator` trait
implementálásához definiálnod kell egy `Item` típust is, és ezt az `Item`
típust használja a `next` metódus visszatérési típusa. Más szóval az `Item`
típus lesz az a típus, amelyet az iterátor visszaad.

Az `Iterator` trait csak egyetlen metódus definiálását követeli meg az
implementálóktól: a `next` metódusét, amely egyszerre egy elemet ad vissza az
iterátorból, `Some`-ba csomagolva, az iteráció végén pedig `None`-t ad vissza.

A `next` metódust közvetlenül is meghívhatjuk az iterátorokon; a 13-12. lista
azt mutatja be, milyen értékeket ad vissza a vektorból létrehozott iterátoron
ismételten meghívott `next`.

<Listing number="13-12" file-name="src/lib.rs" caption="A `next` metódus meghívása egy iterátoron">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Figyeld meg, hogy a `v1_iter`-t módosíthatóvá kellett tennünk: a `next` metódus
meghívása egy iterátoron megváltoztatja azt a belső állapotot, amellyel az
iterátor nyilvántartja, hol tart a sorozatban. Más szóval ez a kód
_elfogyasztja_, azaz felhasználja az iterátort. A `next` minden hívása
felemészt egy elemet az iterátorból. A `for` ciklus használatakor nem kellett
módosíthatóvá tennünk a `v1_iter`-t, mert a ciklus átvette a `v1_iter`
ownershipjét, és a színfalak mögött módosíthatóvá tette.

Azt is vedd észre, hogy a `next` hívásaiból kapott értékek nem módosítható
referenciák a vektorban lévő értékekre. Az `iter` metódus nem módosítható
referenciákon végighaladó iterátort állít elő. Ha olyan iterátort szeretnénk
létrehozni, amely átveszi a `v1` ownershipjét, és birtokolt értékeket ad
vissza, akkor az `iter` helyett az `into_iter` metódust hívhatjuk. Hasonlóan,
ha módosítható referenciákon szeretnénk végighaladni, az `iter` helyett az
`iter_mut` metódust hívhatjuk.

### Az iterátort elfogyasztó metódusok

Az `Iterator` traitnek számos különböző metódusa van, amelyekhez a standard
könyvtár alapértelmezett implementációt ad; ezekről a metódusokról a standard
könyvtár API-dokumentációjában, az `Iterator` traitnél olvashatsz. Néhány ilyen
metódus a definíciójában meghívja a `next` metódust, és emiatt kell a `next`
metódust implementálnod az `Iterator` trait implementálásakor.

Azokat a metódusokat, amelyek meghívják a `next`-et, _fogyasztó adaptereknek_
nevezzük, mert a hívásuk felhasználja az iterátort. Egy példa erre a `sum`
metódus, amely átveszi az iterátor ownershipjét, és a `next` ismételt hívásával
végighalad az elemeken, ezzel elfogyasztva az iterátort. Miközben végighalad
rajtuk, minden elemet hozzáad egy futó összeghez, és az iteráció végén
visszaadja az összeget. A 13-13. listában egy teszt szemlélteti a `sum` metódus
használatát.

<Listing number="13-13" file-name="src/lib.rs" caption="A `sum` metódus meghívása az iterátor összes elemének összegzéséhez">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

A `sum` hívása után már nem használhatjuk a `v1_iter`-t, mert a `sum` átveszi
annak az iterátornak az ownershipjét, amelyen meghívjuk.

### Más iterátorokat előállító metódusok

Az _iterátor-adapterek_ az `Iterator` traiten definiált olyan metódusok,
amelyek nem fogyasztják el az iterátort. Ehelyett más iterátorokat állítanak
elő az eredeti iterátor valamely tulajdonságának megváltoztatásával.

A 13-14. lista példát mutat a `map` iterátor-adapter metódus meghívására, amely
egy closure-t vár, hogy azt minden elemen meghívja, ahogy végighalad rajtuk. A
`map` metódus egy új iterátort ad vissza, amely a módosított elemeket állítja
elő. Az itteni closure olyan új iterátort hoz létre, amelyben a vektor minden
eleme 1-gyel meg lesz növelve.

<Listing number="13-14" file-name="src/main.rs" caption="A `map` iterátor-adapter meghívása új iterátor létrehozásához">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Ez a kód azonban figyelmeztetést eredményez:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

A 13-14. lista kódja nem csinál semmit; az általunk megadott closure sosem
hívódik meg. A figyelmeztetés emlékeztet minket az okára: az
iterátor-adapterek lusták, és itt el kell fogyasztanunk az iterátort.

Hogy megszüntessük ezt a figyelmeztetést, és elfogyasszuk az iterátort, a
`collect` metódust fogjuk használni, amelyet a 12-1. listában az `env::args`
metódussal együtt már használtunk. Ez a metódus elfogyasztja az iterátort, és
az eredményül kapott értékeket összegyűjti egy kollekciótípusba.

A 13-15. listában a `map` hívásából visszakapott iterátoron való végighaladás
eredményeit gyűjtjük össze egy vektorba. Ez a vektor végül az eredeti vektor
minden elemét tartalmazni fogja 1-gyel megnövelve.

<Listing number="13-15" file-name="src/main.rs" caption="A `map` metódus meghívása új iterátor létrehozásához, majd a `collect` metódus meghívása az új iterátor elfogyasztásához és egy vektor létrehozásához">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Mivel a `map` closure-t vár, bármilyen műveletet megadhatunk, amelyet az egyes
elemeken el szeretnénk végezni. Ez remek példa arra, hogyan teszik lehetővé a
closure-ök valamilyen viselkedés testreszabását, miközben újrahasznosítod az
`Iterator` trait által nyújtott iterálási viselkedést.

Több iterátor-adapter-hívást is láncba fűzhetsz, hogy összetett műveleteket
végezz olvasható módon. De mivel minden iterátor lusta, meg kell hívnod
valamelyik fogyasztó adapter metódust, hogy eredményt kapj az
iterátor-adapterek hívásaiból.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### A környezetüket elkapó closure-ök

Sok iterátor-adapter closure-t vár argumentumként, és az
iterátor-adaptereknek argumentumként megadott closure-ök gyakran olyanok,
amelyek elkapják a környezetüket.

Ehhez a példához a `filter` metódust használjuk, amely egy closure-t vár. A
closure megkap egy elemet az iterátorból, és egy `bool` értéket ad vissza. Ha a
closure `true` értéket ad vissza, az érték bekerül a `filter` által előállított
iterátorba. Ha a closure `false` értéket ad vissza, az érték nem kerül bele.

A 13-16. listában a `filter`-t olyan closure-rel használjuk, amely elkapja a
`shoe_size` változót a környezetéből, hogy végighaladjunk `Shoe` struct
példányok egy kollekcióján. Csak a megadott méretű cipőket adja vissza.

<Listing number="13-16" file-name="src/lib.rs" caption="A `filter` metódus használata olyan closure-rel, amely elkapja a `shoe_size` változót">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

A `shoes_in_size` függvény paraméterként átveszi egy cipőket tartalmazó vektor
ownershipjét és egy cipőméretet. Olyan vektort ad vissza, amely csak a megadott
méretű cipőket tartalmazza.

A `shoes_in_size` törzsében meghívjuk az `into_iter` metódust, hogy
létrehozzunk egy olyan iterátort, amely átveszi a vektor ownershipjét. Ezután
meghívjuk a
`filter`-t, hogy azt az iterátort olyan új iterátorrá alakítsuk, amely csak
azokat az elemeket tartalmazza, amelyekre a closure `true` értéket ad vissza.

A closure elkapja a `shoe_size` paramétert a környezetből, és összehasonlítja
az értékét minden cipő méretével, csak a megadott méretű cipőket tartva meg.
Végül
a `collect` hívása az átalakított iterátor által visszaadott értékeket egy
vektorba gyűjti, amelyet a függvény visszaad.

A teszt megmutatja, hogy amikor meghívjuk a `shoes_in_size` függvényt, csak
olyan cipőket kapunk vissza, amelyek mérete megegyezik az általunk megadott
értékkel.
