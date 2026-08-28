## Az I/O-projektünk továbbfejlesztése

Az iterátorokról szerzett új tudásunkkal továbbfejleszthetjük a 12. fejezet
I/O-projektjét: az iterátorok segítségével a kód több pontja világosabbá és
tömörebbé válik. Nézzük meg, hogyan javíthatnak az iterátorok a
`Config::build` függvény és a `search` függvény implementációján.

### Egy `clone` hívás megszüntetése iterátorral

A 12-6. listában olyan kódot adtunk hozzá, amely `String` értékek egy slice-át
vette át, és a slice indexelésével, majd az értékek klónozásával létrehozta a
`Config` struct egy példányát, lehetővé téve, hogy a `Config` struct birtokolja
ezeket az értékeket. A 13-17. listában újra közöljük a `Config::build` függvény
implementációját úgy, ahogyan a 12-23. listában szerepelt.

<Listing number="13-17" file-name="src/main.rs" caption="A `Config::build` függvény újraközlése a 12-23. listából">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Akkor azt mondtuk, hogy ne aggódj a nem hatékony `clone` hívások miatt, mert a
jövőben megszüntetjük őket. Nos, elérkezett ez az idő!

Azért volt szükségünk itt a `clone`-ra, mert az `args` paraméterben `String`
elemeket tartalmazó slice van, a `build` függvény viszont nem birtokolja az
`args`-ot. Ahhoz, hogy visszaadhassuk egy `Config` példány ownershipjét,
klónoznunk kellett a `Config` `query` és `file_path` mezőinek értékeit, hogy a
`Config` példány birtokolhassa a saját értékeit.

Az iterátorokról szerzett új tudásunkkal megváltoztathatjuk a `build`
függvényt úgy, hogy egy slice kölcsönvétele helyett egy iterátor ownershipjét
vegye át argumentumként. Az iterátorok képességeit fogjuk használni annak a
kódnak a helyett, amely ellenőrzi a slice hosszát, és konkrét helyeken
indexeli. Ez világosabbá teszi, mit csinál a `Config::build` függvény, mert az
értékekhez az iterátor fog hozzáférni.

Miután a `Config::build` átveszi az iterátor ownershipjét, és nem használ többé
kölcsönvevő indexelő műveleteket, a `String` értékeket az iterátorból a
`Config`-ba mozgathatjuk ahelyett, hogy `clone`-t hívnánk, és új memóriát
foglalnánk.

#### A visszaadott iterátor közvetlen használata

Nyisd meg az I/O-projekted _src/main.rs_ fájlját, amely így néz ki:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Először a `main` függvény elejét, amely a 12-24. listában szerepelt, a 13-18.
lista kódjára cseréljük, amely ezúttal iterátort használ. Ez addig nem fordul
le, amíg a `Config::build` függvényt is nem frissítjük.

<Listing number="13-18" file-name="src/main.rs" caption="Az `env::args` visszatérési értékének átadása a `Config::build` függvénynek">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Az `env::args` függvény egy iterátort ad vissza! Ahelyett, hogy az iterátor
értékeit egy vektorba gyűjtenénk, majd egy slice-ot adnánk át a
`Config::build` függvénynek, most közvetlenül az `env::args` által visszaadott
iterátor ownershipjét adjuk át a `Config::build` függvénynek.

Ezután frissítenünk kell a `Config::build` definícióját. Változtassuk meg a
`Config::build` szignatúráját úgy, hogy a 13-19. listához hasonlóan nézzen ki.
Ez még mindig nem fog lefordulni, mert a függvény törzsét is frissítenünk kell.

<Listing number="13-19" file-name="src/main.rs" caption="A `Config::build` szignatúrájának frissítése, hogy iterátort várjon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Az `env::args` függvény standard könyvtári dokumentációja szerint az általa
visszaadott iterátor típusa `std::env::Args`, és ez a típus implementálja az
`Iterator` trait-et, valamint `String` értékeket ad vissza.

Frissítettük a `Config::build` függvény szignatúráját úgy, hogy az `args`
paraméter `&[String]` helyett `impl Iterator<Item = String>` trait bounddal
rendelkező generikus típusú legyen. Az `impl Trait` szintaxisnak ez a
használata, amelyről a 10. fejezet
[„Trait-ek használata paraméterként”][impl-trait]<!-- ignore --> című
alfejezetében volt szó, azt jelenti, hogy az `args` bármilyen olyan típus
lehet, amely implementálja az `Iterator` trait-et, és `String` elemeket ad
vissza.

Mivel átvesszük az `args` ownershipjét, és módosítani fogjuk az `args`-ot
azzal, hogy végighaladunk rajta, az `args` paraméter megadásához hozzáadhatjuk
a `mut` kulcsszót, hogy módosíthatóvá tegyük.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Az `Iterator` trait metódusainak használata

Ezután megjavítjuk a `Config::build` törzsét. Mivel az `args` implementálja az
`Iterator` trait-et, tudjuk, hogy meghívhatjuk rajta a `next` metódust! A 13-20.
lista a 12-23. lista kódját frissíti úgy, hogy a `next` metódust használja.

<Listing number="13-20" file-name="src/main.rs" caption="A `Config::build` törzsének átalakítása iterátormetódusok használatára">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Ne feledd, hogy az `env::args` visszatérési értékének első eleme a program
neve. Ezt figyelmen kívül szeretnénk hagyni, és a következő értékhez akarunk
jutni, ezért először meghívjuk a `next`-et, és nem kezdünk semmit a
visszatérési értékkel. Ezután meghívjuk a `next`-et, hogy megkapjuk azt az
értéket, amelyet a `Config` `query` mezőjébe akarunk tenni. Ha a `next`
`Some`-ot ad vissza, egy `match` segítségével kinyerjük az értéket. Ha `None`-t
ad vissza, az azt jelenti, hogy nem adtak meg elég argumentumot, és korán
visszatérünk egy `Err` értékkel. Ugyanezt tesszük a `file_path` értékkel is.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### A kód áttekinthetőbbé tétele iterátor-adapterekkel

Az I/O-projektünk `search` függvényében is kihasználhatjuk az iterátorokat; ezt
a függvényt itt, a 13-21. listában közöljük újra úgy, ahogyan a 12-19. listában
szerepelt.

<Listing number="13-21" file-name="src/lib.rs" caption="A `search` függvény implementációja a 12-19. listából">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Ezt a kódot tömörebben is megírhatjuk iterátor-adapter metódusokkal. Így azt is
elkerülhetjük, hogy szükségünk legyen egy módosítható, köztes `results`
vektorra. A funkcionális programozási stílus arra törekszik, hogy minimalizálja
a módosítható állapot mennyiségét, ezzel téve világosabbá a kódot. A
módosítható állapot megszüntetése egy jövőbeli továbbfejlesztést is lehetővé
tehet, amelyben a keresés párhuzamosan zajlik, mert nem kellene kezelnünk a
`results` vektorhoz való konkurens hozzáférést. A 13-22. lista mutatja ezt a
változtatást.

<Listing number="13-22" file-name="src/lib.rs" caption="Iterátor-adapter metódusok használata a `search` függvény implementációjában">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Emlékezz vissza, hogy a `search` függvény célja az, hogy visszaadja a
`contents` összes olyan sorát, amely tartalmazza a `query`-t. A 13-16. lista
`filter`-példájához hasonlóan ez a kód a `filter` adaptert használja, hogy csak
azokat a sorokat tartsa meg, amelyekre a `line.contains(query)` `true` értéket
ad vissza. Ezután a `collect` segítségével egy másik vektorba gyűjtjük az
illeszkedő sorokat. Sokkal egyszerűbb! Nyugodtan végezd el ugyanezt a
változtatást a `search_case_insensitive` függvényben is, hogy az is
iterátormetódusokat használjon.

További javításként add vissza a `search` függvényből magát az iterátort: hagyd
el a `collect` hívását, és változtasd a visszatérési típust `impl
Iterator<Item = &'a str>`-re, hogy a függvényből iterátor-adapter legyen. Ne
feledd, hogy a teszteket is frissítened kell! A változtatás előtt és után is
keress egy nagy fájlban a `minigrep` eszközöddel, hogy megfigyeld a viselkedés
különbségét. A változtatás előtt a program addig nem ír ki semmilyen
eredményt, amíg össze nem gyűjtötte az összeset, a változtatás után viszont az
eredmények akkor íródnak ki, amikor az egyes illeszkedő sorok megtalálódnak,
mert a `run` függvényben lévő `for` ciklus ki tudja használni az iterátor
lustaságát.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Választás ciklusok és iterátorok között

A következő kézenfekvő kérdés az, hogy melyik stílust válaszd a saját kódodban,
és miért: a 13-21. lista eredeti implementációját, vagy a 13-22. lista
iterátorokat használó változatát (feltéve, hogy az összes eredményt
összegyűjtjük, mielőtt visszaadnánk őket, nem pedig magát az iterátort adjuk
vissza). A legtöbb Rust-programozó az iterátoros stílust részesíti előnyben.
Elsőre kicsit nehezebb ráérezni, de ha egyszer megérzed a különféle
iterátor-adapterek működését, az iterátorokat könnyebb lehet megérteni.
Ahelyett, hogy a ciklusszervezés és az új vektorok építésének apró
részleteivel bajlódnál, a kód a ciklus magas szintű céljára összpontosít. Ez
elrejti a megszokott, sablonos kód egy részét, így könnyebb meglátni az ebben
a kódban egyedi fogalmakat, például azt a szűrési feltételt, amelynek az
iterátor minden elemének meg kell felelnie.

De vajon tényleg egyenértékű a két implementáció? Az intuitív feltételezés az
lehet, hogy az alacsonyabb szintű ciklus gyorsabb. Beszéljünk a
teljesítményről.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
