<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Trait objectek használata a közös viselkedés absztrahálására {#using-trait-objects-to-abstract-over-shared-behavior}

A 8. fejezetben említettük, hogy a vektorok egyik korlátja, hogy csak egyetlen
típusú elemeket tudnak tárolni. A 8-9. listában készítettünk erre egy
megkerülő megoldást: definiáltunk egy `SpreadsheetCell` enumot, amelynek
voltak egész számokat, lebegőpontos számokat és szöveget tároló variánsai. Így
minden cellában más-más típusú adatot tárolhattunk, és mégis olyan vektorunk
volt, amely egy cellákból álló sort ábrázolt. Ez tökéletesen jó megoldás
akkor, ha a felcserélhető elemeink a típusok olyan rögzített halmazát alkotják,
amelyet már a kód fordításakor ismerünk.

Néha azonban azt szeretnénk, hogy a könyvtárunk használója bővíthesse az adott
helyzetben érvényes típusok halmazát. Hogy megmutassuk, ezt hogyan érhetjük
el, készítünk egy példaként szolgáló grafikus felhasználói felület (GUI)
eszközt, amely végigmegy egy elemlistán, és mindegyik elemen meghívja a `draw`
metódust, hogy kirajzolja a képernyőre – ez a GUI-eszközök egyik bevett
technikája. Létrehozunk egy `gui` nevű library crate-et, amely egy
GUI-könyvtár vázát tartalmazza. Ebben a crate-ben lehet néhány típus, amelyet
az emberek használhatnak, például `Button` vagy `TextField`. Ezenfelül a `gui`
felhasználói szeretnének majd saját, kirajzolható típusokat is létrehozni:
lehet, hogy az egyik programozó hozzáad egy `Image` típust, egy másik pedig egy
`SelectBox` típust.

A könyvtár megírásakor nem tudhatjuk és nem definiálhatjuk előre az összes
típust, amelyet más programozók létre akarnak majd hozni. Azt viszont tudjuk,
hogy a `gui`-nak sok különböző típusú értéket kell nyilvántartania, és
mindegyik ilyen eltérő típusú értéken meg kell hívnia egy `draw` metódust. Azt
nem kell tudnia, pontosan mi történik, amikor meghívjuk a `draw` metódust,
csak azt, hogy az adott értéken ez a metódus meghívható lesz.

Egy öröklődéssel rendelkező nyelvben ezt úgy oldanánk meg, hogy definiálnánk
egy `Component` nevű osztályt, amelyen van egy `draw` nevű metódus. A többi
osztály, például a `Button`, az `Image` és a `SelectBox`, a `Component`-től
örökölne, és így megörökölné a `draw` metódust is. Mindegyikük felülírhatná a
`draw` metódust, hogy a saját viselkedését adja meg, a keretrendszer viszont az
összes típust úgy kezelhetné, mintha `Component` példányok lennének, és
meghívhatná rajtuk a `draw`-t. Mivel azonban a Rustban nincs öröklődés, más
módot kell találnunk a `gui` könyvtár felépítésére, hogy a felhasználók a
könyvtárral kompatibilis új típusokat hozhassanak létre.

### Trait definiálása a közös viselkedéshez

Ahhoz, hogy megvalósítsuk a `gui`-tól elvárt viselkedést, definiálunk egy
`Draw` nevű traitet, amelynek egyetlen `draw` nevű metódusa lesz. Ezután
definiálhatunk egy olyan vektort, amely trait objectet vesz fel. Egy _trait
object_ egyszerre mutat az általunk megadott traitet implementáló típus egyik
példányára, és egy táblázatra, amelynek segítségével futásidőben megkereshetők
az adott típus trait-metódusai. Trait objectet úgy hozunk létre, hogy megadunk
valamiféle pointert – például egy referenciát vagy egy `Box<T>` smart pointert
–, majd a `dyn` kulcsszót, végül pedig a megfelelő traitet. (Arról, hogy a
trait objecteknek miért kell pointert használniuk, a 20. fejezet [„Dinamikusan
méretezett típusok és a `Sized` trait”][dynamically-sized]<!-- ignore -->
részében lesz szó.) A trait objecteket generikus vagy konkrét típus helyén
használhatjuk. Bárhol is használunk trait objectet, a Rust típusrendszere
fordítási időben biztosítja, hogy az adott környezetben használt minden érték
implementálja a trait object traitjét. Ennek következtében nem kell fordítási
időben ismernünk az összes lehetséges típust.

Említettük már, hogy a Rustban tartózkodunk attól, hogy a structokat és az
enumokat „objektumnak” nevezzük, hogy megkülönböztessük őket más nyelvek
objektumaitól. Egy structban vagy enumban a struct mezőiben lévő adatok és az
`impl` blokkokban lévő viselkedés elkülönül, míg más nyelvekben az egyetlen
fogalommá összevont adatot és viselkedést gyakran objektumnak nevezik. A trait
objectek abban különböznek más nyelvek objektumaitól, hogy egy trait objecthez
nem tudunk adatot hozzáadni. A trait objectek általánosságban nem olyan
hasznosak, mint más nyelvek objektumai: kifejezetten az a céljuk, hogy közös
viselkedésre lehessen absztrahálni.

A 18-3. lista bemutatja, hogyan definiálhatunk egy `Draw` nevű traitet egyetlen
`draw` nevű metódussal.

<Listing number="18-3" file-name="src/lib.rs" caption="A `Draw` trait definíciója">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Ez a szintaxis ismerősnek tűnhet abból, amit a 10. fejezetben a traitek
definiálásáról beszéltünk. Ezután jön némi új szintaxis: a 18-4. lista
definiál egy `Screen` nevű structot, amely egy `components` nevű vektort
tartalmaz. Ez a vektor `Box<dyn Draw>` típusú, ami egy trait object;
helyettesítője bármely olyan típusnak egy `Box`-on belül, amely implementálja a
`Draw` traitet.

<Listing number="18-4" file-name="src/lib.rs" caption="A `Screen` struct definíciója egy `components` mezővel, amely a `Draw` traitet implementáló trait objectek vektorát tartalmazza">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

A `Screen` structon definiálunk egy `run` nevű metódust, amely meghívja a
`draw` metódust minden egyes elemén a `components` vektorban, ahogy a 18-5.
listában látható.

<Listing number="18-5" file-name="src/lib.rs" caption="A `Screen` `run` metódusa, amely minden komponensen meghívja a `draw` metódust">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Ez másképp működik, mint amikor olyan structot definiálunk, amely trait
boundokkal ellátott generikus típusparamétert használ. Egy generikus
típusparaméter egyszerre csak egyetlen konkrét típussal helyettesíthető, a
trait objectek viszont lehetővé teszik, hogy futásidőben több konkrét típus is
betöltse a trait object helyét. Definiálhattuk volna például a `Screen`
structot generikus típussal és trait bounddal is, ahogy a 18-6. listában
látható.

<Listing number="18-6" file-name="src/lib.rs" caption="A `Screen` struct és `run` metódusának alternatív implementációja generikusokkal és trait boundokkal">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Ez arra korlátoz minket, hogy a `Screen` példány komponenslistájában minden
elem `Button` típusú legyen, vagy minden elem `TextField` típusú. Ha úgyis
mindig homogén kollekcióid lesznek, a generikusok és a trait boundok
használata az előnyösebb, mert a definíciók fordítási időben monomorfizálódnak
a konkrét típusokra.

A trait objecteket használó megoldásnál viszont egyetlen `Screen` példány
tarthat olyan `Vec<T>` vektort, amely egy `Box<Button>` és egy `Box<TextField>`
értéket is tartalmaz. Nézzük meg, hogyan működik ez, aztán beszélünk a
futásidejű teljesítménybeli következményekről.

### A trait implementálása

Most hozzáadunk néhány olyan típust, amely implementálja a `Draw` traitet.
Elkészítjük a `Button` típust. Egy GUI-könyvtár tényleges megvalósítása
ismételten túlmutat e könyv keretein, ezért a `draw` metódus törzsében nem lesz
használható implementáció. Hogy elképzelhessük, hogyan nézhetne ki az
implementáció, a `Button` structnak lehetnének `width`, `height` és `label`
mezői, ahogy a 18-7. listában látható.

<Listing number="18-7" file-name="src/lib.rs" caption="Egy `Button` struct, amely implementálja a `Draw` traitet">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

A `Button` `width`, `height` és `label` mezői eltérnek majd a többi komponens
mezőitől; egy `TextField` típusnak például lehetnek ugyanezek a mezői, plusz
egy `placeholder` mező. Minden olyan típus, amelyet a képernyőre akarunk
rajzolni, implementálja majd a `Draw` traitet, de a `draw` metódusban más-más
kódot használ annak megadására, hogyan kell az adott típust kirajzolni, ahogy
itt a `Button` teszi (az említett módon a tényleges GUI-kód nélkül). A `Button`
típusnak például lehet egy további `impl` blokkja, amely azzal kapcsolatos
metódusokat tartalmaz, hogy mi történik, amikor a felhasználó rákattint a
gombra. Az ilyesféle metódusoknak nincs értelmük olyan típusoknál, mint a
`TextField`.

Ha a könyvtárunk valamelyik használója úgy dönt, hogy implementál egy
`SelectBox` structot `width`, `height` és `options` mezőkkel, akkor a
`SelectBox` típusra is implementálná a `Draw` traitet, ahogy a 18-8. listában
látható.

<Listing number="18-8" file-name="src/main.rs" caption="Egy másik crate, amely a `gui`-t használja, és implementálja a `Draw` traitet egy `SelectBox` structra">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

A könyvtárunk használója most már megírhatja a `main` függvényét, hogy
létrehozzon egy `Screen` példányt. A `Screen` példányhoz hozzáadhat egy
`SelectBox`-ot és egy `Button`-t úgy, hogy mindegyiket egy `Box<T>`-ba teszi,
és így trait objectté válnak. Ezután meghívhatja a `Screen` példány `run`
metódusát, amely minden komponensen meghívja a `draw` metódust. A 18-9. lista
mutatja ezt az implementációt.

<Listing number="18-9" file-name="src/main.rs" caption="Trait objectek használata ugyanazt a traitet implementáló, különböző típusú értékek tárolására">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Amikor megírtuk a könyvtárat, nem tudtuk, hogy valaki hozzáadhat egy
`SelectBox` típust, a `Screen` implementációnk mégis képes volt kezelni és
kirajzolni az új típust, mert a `SelectBox` implementálja a `Draw` traitet,
vagyis implementálja a `draw` metódust.

Ez az elgondolás – hogy csak az számít, milyen üzenetekre válaszol egy érték,
nem pedig az, hogy mi az érték konkrét típusa – hasonlít a dinamikusan típusos
nyelvekben ismert _duck typing_ fogalmához: ha úgy jár, mint egy kacsa, és úgy
hápog, mint egy kacsa, akkor biztosan kacsa! A `Screen` `run` metódusának
18-5. listabeli implementációjában a `run`-nak nem kell tudnia, mi az egyes
komponensek konkrét típusa. Nem ellenőrzi, hogy egy komponens `Button` vagy
`SelectBox` példány-e, egyszerűen meghívja rajta a `draw` metódust. Azzal,
hogy a `components` vektorban lévő értékek típusaként `Box<dyn Draw>`-t adtunk
meg, a `Screen`-t úgy definiáltuk, hogy olyan értékekre van szüksége,
amelyeken meghívható a `draw` metódus.

A trait objectek és a Rust típusrendszerének használatával a duck typinghoz
hasonló kódot írhatunk, azzal az előnnyel, hogy soha nem kell futásidőben
ellenőriznünk, egy érték implementál-e egy adott metódust, és nem kell attól
tartanunk, hogy hibát kapunk, mert egy érték nem implementál egy metódust, mi
mégis meghívjuk. A Rust le sem fordítja a kódunkat, ha az értékek nem
implementálják azokat a traiteket, amelyekre a trait objecteknek szükségük van.

A 18-10. lista például azt mutatja meg, mi történik, ha megpróbálunk olyan
`Screen`-t létrehozni, amelynek egyik komponense egy `String`.

<Listing number="18-10" file-name="src/main.rs" caption="Kísérlet olyan típus használatára, amely nem implementálja a trait object traitjét">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Ezt a hibát fogjuk kapni, mert a `String` nem implementálja a `Draw` traitet:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Ez a hiba azt jelzi, hogy vagy olyasmit adunk át a `Screen`-nek, amit nem
akartunk, és így más típust kellene átadnunk, vagy implementálnunk kellene a
`Draw`-t a `String`-re, hogy a `Screen` meg tudja hívni rajta a `draw`-t.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dinamikus dispatch végrehajtása

Emlékezz vissza a 10. fejezet [„A generikusokat használó kód
teljesítménye”][performance-of-code-using-generics]<!-- ignore --> részére, ahol
arról a monomorfizációs folyamatról volt szó, amelyet a fordító a generikusokon
végez: a fordító minden olyan konkrét típusra, amelyet egy generikus
típusparaméter helyén használunk, nem generikus implementációt állít elő a
függvényekből és metódusokból. A monomorfizációból származó kód _statikus
dispatchet_ végez, vagyis olyat, amikor a fordító már fordítási időben tudja,
melyik metódust hívod. Ennek ellentéte a _dinamikus dispatch_, amikor a fordító
fordítási időben nem tudja megállapítani, melyik metódust hívod. Dinamikus
dispatch esetén a fordító olyan kódot állít elő, amely futásidőben fogja
tudni, melyik metódust kell meghívni.

Amikor trait objecteket használunk, a Rustnak dinamikus dispatchet kell
alkalmaznia. A fordító nem ismeri az összes olyan típust, amelyet a trait
objecteket használó kóddal használhatnak, így nem tudja, melyik típuson
implementált melyik metódust kell meghívni. Ehelyett a Rust futásidőben a trait
objecten belüli pointerek alapján tudja meg, melyik metódust kell meghívni. Ez a
keresés olyan futásidejű költséggel jár, amely a statikus dispatchnél nem
jelentkezik. A dinamikus dispatch emellett megakadályozza, hogy a fordító
beinline-olja egy metódus kódját, ami viszont bizonyos optimalizációkat is
kizár, és a Rustnak vannak szabályai arra, hol használhatsz dinamikus
dispatchet és hol nem; ezeket _dyn kompatibilitásnak_ nevezik. Ezek a szabályok
túlmutatnak e tárgyalás keretein, de többet olvashatsz róluk [a
referenciában][dyn-compatibility]<!-- ignore -->. Cserébe viszont többletbeli
rugalmasságot kaptunk abban a kódban, amelyet a 18-5. listában írtunk, és
amelyet a 18-9. listában sikerült támogatnunk, szóval ez egy mérlegelendő
kompromisszum.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
