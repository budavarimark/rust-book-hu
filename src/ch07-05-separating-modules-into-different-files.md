## Modulok szétválasztása külön fájlokba

Eddig a fejezet összes példája több modult definiált egyetlen fájlban. Ha a
modulok nagyra nőnek, érdemes lehet a definícióikat külön fájlba mozgatni, hogy
a kódban könnyebb legyen eligazodni.

Induljunk ki például a 7-17. listában szereplő kódból, amely több étteremmodult
tartalmazott. A modulokat fájlokba emeljük ki ahelyett, hogy mindet a crate
gyökérfájljában definiálnánk. Ebben az esetben a crate gyökérfájlja a
_src/lib.rs_, de ez az eljárás olyan binary crate-ekkel is működik, amelyek
gyökérfájlja a _src/main.rs_.

Először a `front_of_house` modult emeljük ki a saját fájljába. Töröld a
`front_of_house` modul kapcsos zárójelei közötti kódot, és hagyd meg csak a
`mod front_of_house;` deklarációt, hogy a _src/lib.rs_ a 7-21. listában látható
kódot tartalmazza. Vedd figyelembe, hogy ez addig nem fordul le, amíg létre nem
hozzuk a 7-22. listában szereplő _src/front_of_house.rs_ fájlt.

<Listing number="7-21" file-name="src/lib.rs" caption="A `front_of_house` modul deklarálása, amelynek törzse a *src/front_of_house.rs* fájlban lesz">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Ezután helyezd a kapcsos zárójelek között álló kódot egy új,
_src/front_of_house.rs_ nevű fájlba, ahogy a 7-22. lista mutatja. A fordító
tudja, hogy ebben a fájlban kell keresnie, mert a crate gyökerében találkozott a
`front_of_house` nevű modul deklarációjával.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="A `front_of_house` modulon belüli definíciók a *src/front_of_house.rs* fájlban">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Vedd figyelembe, hogy egy fájlt `mod` deklarációval csak _egyszer_ kell
betöltened a modulfádban. Miután a fordító tudja, hogy a fájl a projekt része
(és azt is tudja, hol helyezkedik el a kód a modulfában, mert oda tetted a `mod`
utasítást), a projekt többi fájljának a betöltött fájl kódjára a deklarálás
helyéhez vezető útvonallal kell hivatkoznia, ahogy azt a
[„Útvonalak a modulfa elemeire való hivatkozáshoz”][paths]<!-- ignore --> című
szakaszban tárgyaltuk. Más szóval a `mod` _nem_ olyan „include” művelet, amelyet
más programozási nyelvekben láthattál.

Ezután a `hosting` modult emeljük ki a saját fájljába. A folyamat kissé
másképp néz ki, mert a `hosting` a `front_of_house` gyermekmodulja, nem pedig a
gyökérmodulé. A `hosting` fájlját egy új könyvtárba tesszük, amelyet a
modulfában lévő őseiről nevezünk el; ebben az esetben ez a _src/front_of_house_.

A `hosting` áthelyezésének elkezdéséhez a _src/front_of_house.rs_ fájlt úgy
módosítjuk, hogy csak a `hosting` modul deklarációját tartalmazza:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Ezután létrehozunk egy _src/front_of_house_ könyvtárat és egy _hosting.rs_
fájlt, amely a `hosting` modulban szereplő definíciókat tartalmazza:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Ha ehelyett a _hosting.rs_ fájlt a _src_ könyvtárba tennénk, a fordító azt
várná, hogy a _hosting.rs_ kódja a crate gyökerében deklarált `hosting` modulhoz
tartozik, nem pedig a `front_of_house` modul gyermekeként deklarált modulhoz. A
fordítónak azok a szabályai, amelyek megmondják, melyik modul kódját melyik
fájlban kell keresnie, azt eredményezik, hogy a könyvtárak és a fájlok szorosan
követik a modulfa szerkezetét.

> ### Alternatív fájlútvonalak {#alternate-file-paths}
>
> Eddig azokat a fájlútvonalakat vettük végig, amelyeket a Rust fordító
> leginkább idiomatikusnak tekint, a Rust azonban egy régebbi stílusú
> fájlútvonalat is támogat. A crate gyökerében deklarált `front_of_house` nevű
> modul kódját a fordító ezeken a helyeken keresi:
>
> - _src/front_of_house.rs_ (amit tárgyaltunk)
> - _src/front_of_house/mod.rs_ (régebbi stílusú, továbbra is támogatott
>   útvonal)
>
> A `front_of_house` almoduljaként létező `hosting` nevű modul kódját a fordító
> ezeken a helyeken keresi:
>
> - _src/front_of_house/hosting.rs_ (amit tárgyaltunk)
> - _src/front_of_house/hosting/mod.rs_ (régebbi stílusú, továbbra is
>   támogatott útvonal)
>
> Ha ugyanahhoz a modulhoz mindkét stílust használod, fordítási hibát kapsz.
> Az, hogy ugyanabban a projektben különböző modulokhoz keverve használod a két
> stílust, megengedett, de zavaró lehet azok számára, akik a projektedben
> próbálnak eligazodni.
>
> A _mod.rs_ nevű fájlokat használó stílus fő hátránya, hogy a projektedben sok
> _mod.rs_ nevű fájl keletkezhet, ami zavaró lehet, amikor egyszerre több is
> nyitva van a szerkesztődben.

Minden modul kódját külön fájlba mozgattuk, a modulfa pedig ugyanaz maradt. Az
`eat_at_restaurant` függvényben lévő függvényhívások bármilyen módosítás nélkül
működni fognak, noha a definíciók más fájlokban élnek. Ezzel a technikával a
modulokat új fájlokba mozgathatod, ahogy egyre nagyobbra nőnek.

Vedd figyelembe, hogy a `pub use crate::front_of_house::hosting` utasítás a
_src/lib.rs_ fájlban szintén nem változott, és a `use` semmilyen hatással sincs
arra, mely fájlok fordulnak le a crate részeként. A `mod` kulcsszó modulokat
deklarál, a Rust pedig a modullal azonos nevű fájlban keresi azt a kódot, amely
az adott modulba tartozik.

## Összefoglalás

A Rust lehetővé teszi, hogy egy csomagot több crate-re, egy crate-et pedig
modulokra bonts, így az egyik modulban definiált elemekre egy másik modulból is
hivatkozhatsz. Ezt abszolút vagy relatív útvonalak megadásával teheted meg.
Ezeket az útvonalakat egy `use` utasítással hatókörbe hozhatod, hogy rövidebb
útvonalat használhass, ha az adott hatókörben többször hivatkozol az elemre. A
modulok kódja alapértelmezés szerint privát, de a definíciókat a `pub` kulcsszó
hozzáadásával nyilvánossá teheted.

A következő fejezetben a standard könyvtár néhány kollekciós adatszerkezetét
nézzük meg, amelyeket a szépen rendszerezett kódodban használhatsz.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
