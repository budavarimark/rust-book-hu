## Mintaszintaxis

Ebben a szakaszban összegyűjtjük a mintákban érvényes összes szintaxist, és
megbeszéljük, miért és mikor érdemes mindegyiket használni.

### Illesztés literálokra

Ahogy a 6. fejezetben láttad, a mintákat közvetlenül literálokra is
illesztheted. Az alábbi kód néhány példát mutat erre:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Ez a kód a `one` szöveget írja ki, mert az `x` értéke `1`. Ez a szintaxis akkor
hasznos, ha azt szeretnéd, hogy a kódod egy adott konkrét érték esetén
végrehajtson valamilyen műveletet.

### Illesztés elnevezett változókra

Az elnevezett változók cáfolhatatlan minták, amelyek bármilyen értékre
illeszkednek; ebben a könyvben már sokszor használtuk őket. Van azonban egy
bonyodalom, ha elnevezett változókat használsz `match`, `if let` vagy `while
let` kifejezésekben. Mivel ezek a kifejezésfajták mind új hatókört nyitnak, az
ezeken belül a minta részeként deklarált változók shadowingolják az azonos nevű,
a szerkezeten kívüli változókat – ahogy az minden változónál történik. A 19-11.
listában deklarálunk egy `x` nevű változót `Some(5)` értékkel, valamint egy `y`
változót `10` értékkel. Ezután létrehozunk egy `match` kifejezést az `x`
értékre. Nézd meg a `match`-ágakban lévő mintákat és a végén álló `println!`
hívást, és próbáld meg kitalálni, mit fog kiírni a kód, mielőtt lefuttatnád vagy
tovább olvasnál.

<Listing number="19-11" file-name="src/main.rs" caption="Egy `match` kifejezés, amelynek egyik ága új változót vezet be, és ezzel shadowingolja a meglévő `y` változót">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Nézzük végig, mi történik a `match` kifejezés futásakor. Az első `match`-ág
mintája nem illeszkedik az `x` megadott értékére, így a kód továbbhalad.

A második `match`-ág mintája egy új, `y` nevű változót vezet be, amely a `Some`
értéken belüli bármilyen értékre illeszkedik. Mivel a `match` kifejezésen belül
új hatókörben vagyunk, ez egy új `y` változó, nem az az `y`, amelyet az elején
`10` értékkel deklaráltunk. Ez az új `y` kötés a `Some`-on belüli bármilyen
értékre illeszkedik, és pontosan ilyen érték van az `x`-ben. Ezért ez az új `y`
az `x`-ben lévő `Some` belső értékéhez kötődik. Ez az érték `5`, így az ághoz
tartozó kifejezés fut le, és a `Matched, y = 5` szöveget írja ki.

Ha az `x` `Some(5)` helyett `None` érték lett volna, az első két ág mintái nem
illeszkedtek volna, így az érték az aláhúzásra illeszkedett volna. Az aláhúzásos
ág mintájában nem vezettünk be `x` változót, így a kifejezésben szereplő `x`
továbbra is a külső, nem shadowingolt `x`. Ebben az elképzelt esetben a `match`
a `Default case, x = None` szöveget írta volna ki.

Amikor a `match` kifejezés befejeződik, a hatóköre véget ér, és vele együtt a
belső `y` hatóköre is. Az utolsó `println!` az `at the end: x = Some(5), y = 10`
szöveget adja.

Ahhoz, hogy olyan `match` kifejezést hozzunk létre, amely a külső `x` és `y`
értékét hasonlítja össze ahelyett, hogy a meglévő `y` változót shadowingoló új
változót vezetne be, egy match guard feltételt kellene használnunk helyette. A
match guardokról a [„Feltételek hozzáadása match
guardokkal”](#adding-conditionals-with-match-guards)<!-- ignore --> szakaszban
lesz szó később.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Illesztés több mintára

A `match` kifejezésekben a `|` szintaxissal több mintára is illeszthetsz; ez a
minták _vagy_ operátora. Az alábbi kódban például az `x` értékét illesztjük a
`match`-ágakra, amelyek közül az elsőben egy _vagy_ lehetőség szerepel, vagyis
ha az `x` értéke az adott ágban szereplő értékek bármelyikére illeszkedik, akkor
az ághoz tartozó kód fut le:


```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Ez a kód a `one or two` szöveget írja ki.

### Értéktartományokra illesztés a `..=` szintaxissal

A `..=` szintaxis lehetővé teszi, hogy zárt értéktartományra illesszünk. Az
alábbi kódban, ha egy minta a megadott tartományon belüli bármelyik értékre
illeszkedik, az adott ág fut le:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Ha az `x` értéke `1`, `2`, `3`, `4` vagy `5`, az első ág illeszkedik. Ez a
szintaxis több illesztendő érték esetén kényelmesebb, mint ugyanennek a
gondolatnak a `|` operátorral való kifejezése; ha `|`-t használnánk, az `1 | 2 |
3 | 4 | 5` alakot kellene leírnunk. Egy tartomány megadása sokkal rövidebb,
különösen ha mondjuk az 1 és 1000 közötti bármelyik számra szeretnénk
illeszteni!

A fordító fordítási időben ellenőrzi, hogy a tartomány nem üres-e, és mivel a
Rust csak a `char` és a numerikus értékek esetében tudja megállapítani, hogy egy
tartomány üres-e, a tartományok csak numerikus vagy `char` értékekkel
használhatók.

Íme egy példa `char` értékek tartományaival:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

A Rust meg tudja állapítani, hogy a `'c'` az első minta tartományába esik, ezért
az `early ASCII letter` szöveget írja ki.

### Destrukturálás értékek szétbontására

Mintákkal structokat, enumokat és tuple-öket is destrukturálhatunk, hogy ezen
értékek különböző részeit használjuk. Vegyük sorra az egyes értékfajtákat.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Structok

A 19-12. lista egy `Point` structot mutat két mezővel, `x`-szel és `y`-nal,
amelyet egy `let` utasításban használt mintával bonthatunk szét.

<Listing number="19-12" file-name="src/main.rs" caption="Egy struct mezőinek destrukturálása különálló változókba">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Ez a kód létrehozza az `a` és `b` változókat, amelyek a `p` struct `x` és `y`
mezőinek értékére illeszkednek. A példa azt mutatja, hogy a mintában szereplő
változónevek nem feltétlenül egyeznek meg a struct mezőneveivel. Bevett szokás
azonban a változóneveket a mezőnevekhez igazítani, hogy könnyebb legyen
megjegyezni, melyik változó melyik mezőből származik. E gyakori használat miatt,
és mivel a `let Point { x: x, y: y } = p;` írásmód sok ismétlést tartalmaz, a
Rustban van egy rövidítés a struct mezőire illeszkedő mintákhoz: elég csak a
struct mezőjének nevét felsorolni, és a mintából létrejövő változók ugyanezt a
nevet kapják. A 19-13. lista ugyanúgy viselkedik, mint a 19-12. listában
szereplő kód, de a `let` mintában létrehozott változók `a` és `b` helyett `x` és
`y` lesznek.

<Listing number="19-13" file-name="src/main.rs" caption="Struct mezőinek destrukturálása a struct-mezőrövidítéssel">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Ez a kód létrehozza az `x` és `y` változókat, amelyek a `p` változó `x` és `y`
mezőire illeszkednek. Az eredmény az, hogy az `x` és `y` változók a `p` struct
értékeit tartalmazzák.

A struct-mintában a mezők egy részéhez literál értékeket is megadhatunk
ahelyett, hogy minden mezőhöz változót hoznánk létre. Így néhány mezőt adott
értékre vizsgálhatunk, miközben a többi mező destrukturálásához változókat
hozunk létre.

A 19-14. listában egy `match` kifejezés a `Point` értékeket három esetre bontja:
az `x` tengelyen fekvő pontok (ez akkor igaz, ha `y = 0`), az `y` tengelyen
fekvők (`x = 0`), illetve azok, amelyek egyik tengelyen sincsenek.

<Listing number="19-14" file-name="src/main.rs" caption="Destrukturálás és literál értékekre illesztés egyetlen mintában">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Az első ág minden olyan pontra illeszkedik, amely az `x` tengelyen fekszik: ezt
úgy adjuk meg, hogy az `y` mező akkor illeszkedik, ha értéke a `0` literálra
illeszkedik. A minta ettől még létrehoz egy `x` változót, amelyet az ághoz
tartozó kódban használhatunk.

Hasonlóan, a második ág minden `y` tengelyen lévő pontra illeszkedik: megadjuk,
hogy az `x` mező akkor illeszkedik, ha értéke `0`, és létrehozunk egy `y`
változót az `y` mező értékének. A harmadik ág nem ad meg literálokat, így minden
más `Point` értékre illeszkedik, és mind az `x`, mind az `y` mezőhöz létrehoz
egy változót.

Ebben a példában a `p` érték a második ágra illeszkedik, mivel az `x` értéke
`0`, így ez a kód az `On the y axis at 7` szöveget írja ki.

Ne feledd, hogy a `match` kifejezés abbahagyja az ágak vizsgálatát, amint
megtalálta az első illeszkedő mintát, így hiába van a `Point { x: 0, y: 0 }` az
`x` és az `y` tengelyen is, ez a kód csak az `On the x axis at 0` szöveget írná
ki.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enumok

Ebben a könyvben már destrukturáltunk enumokat (például a 6. fejezet 6-5.
listájában), de még nem beszéltünk kifejezetten arról, hogy az enum
destrukturálására szolgáló minta annak felel meg, ahogyan az enumban tárolt
adatokat definiáltuk. Példaként a 19-15. listában a 6-2. listából származó
`Message` enumot használjuk, és olyan mintákkal írunk `match`-et, amelyek minden
belső értéket destrukturálnak.

<Listing number="19-15" file-name="src/main.rs" caption="Különböző fajta értékeket tároló enum-variánsok destrukturálása">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Ez a kód a `Change color to red 0, green 160, and blue 255` szöveget írja ki.
Próbáld meg megváltoztatni a `msg` értékét, hogy lásd a többi ág kódjának
futását is.

Az adatot nem tartalmazó enum-variánsoknál, mint a `Message::Quit`, az értéket
nem tudjuk tovább destrukturálni. Csak magára a `Message::Quit` literál értékre
illeszthetünk, és abban a mintában nincs változó.

A struct-szerű enum-variánsoknál, mint a `Message::Move`, ahhoz hasonló mintát
használhatunk, amilyet a structokra illesztéskor adunk meg. A variáns neve után
kapcsos zárójeleket teszünk, majd felsoroljuk a mezőket a változókkal, hogy
szétbontsuk a részeket, és felhasználhassuk őket az ághoz tartozó kódban. Itt a
rövidített alakot használjuk, ahogy a 19-13. listában is.

A tuple-szerű enum-variánsoknál – mint a `Message::Write`, amely egyelemű
tuple-t tárol, és a `Message::ChangeColor`, amely háromelemű tuple-t – a minta
hasonló ahhoz, amilyet a tuple-ökre illesztéskor adunk meg. A mintában lévő
változók számának meg kell egyeznie annak a variánsnak az elemszámával, amelyre
illesztünk.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Egymásba ágyazott structok és enumok

Eddigi példáinkban mindig egy szinttel mélyen illesztettünk structokra vagy
enumokra, de az illesztés egymásba ágyazott elemekkel is működik! Például
átalakíthatjuk a 19-15. listában szereplő kódot úgy, hogy a `ChangeColor`
üzenetben RGB és HSV színeket is támogasson, ahogy a 19-16. listában látható.

<Listing number="19-16" caption="Illesztés egymásba ágyazott enumokra">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

A `match` kifejezés első ágának mintája egy olyan `Message::ChangeColor`
enum-variánsra illeszkedik, amely `Color::Rgb` variánst tartalmaz; a minta
ezután a három belső `i32` értékhez kötődik. A második ág mintája szintén egy
`Message::ChangeColor` enum-variánsra illeszkedik, de a belső enum ezúttal a
`Color::Hsv` variánsra illeszkedik. Ezeket az összetett feltételeket egyetlen
`match` kifejezésben adhatjuk meg, noha két enum is szerepel bennük.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Structok és tuple-ök

A destrukturáló mintákat még ennél is összetettebb módon vegyíthetjük,
kombinálhatjuk és ágyazhatjuk egymásba. Az alábbi példa egy bonyolult
destrukturálást mutat be, amelyben structokat és tuple-öket ágyazunk egy
tuple-be, és az összes primitív értéket kibontjuk belőle:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Ez a kód lehetővé teszi, hogy összetett típusokat az alkotórészeikre bontsunk,
és külön-külön használjuk a minket érdeklő értékeket.

A mintákkal való destrukturálás kényelmes módja annak, hogy egy érték részeit –
például egy struct egyes mezőinek értékeit – egymástól függetlenül használjuk.

### Értékek figyelmen kívül hagyása egy mintában {#ignoring-values-in-a-pattern}

Láttad már, hogy néha hasznos figyelmen kívül hagyni értékeket egy mintában,
például egy `match` utolsó ágában, hogy olyan mindent elkapó ágat kapjunk, amely
valójában semmit sem csinál, de az összes megmaradt lehetséges értéket lefedi.
Több módja is van annak, hogy egy mintában teljes értékeket vagy értékek részeit
figyelmen kívül hagyjuk: használhatjuk a `_` mintát (ezt már láttad), a `_`
mintát egy másik mintán belül, aláhúzással kezdődő nevet, vagy a `..` szintaxist
egy érték megmaradt részeinek figyelmen kívül hagyására. Nézzük meg, hogyan és
miért érdemes ezeket a mintákat használni.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Teljes érték a `_` mintával

Az aláhúzást eddig helyettesítő mintaként használtuk, amely bármilyen értékre
illeszkedik, de nem kötődik hozzá. Ez különösen egy `match` kifejezés utolsó
ágaként hasznos, de bármilyen mintában használhatjuk, például
függvényparaméterekben is, ahogy a 19-17. listában látható.

<Listing number="19-17" file-name="src/main.rs" caption="A `_` használata egy függvényszignatúrában">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Ez a kód teljesen figyelmen kívül hagyja az első argumentumként átadott `3`
értéket, és a `This code only uses the y parameter: 4` szöveget írja ki.

A legtöbb esetben, amikor már nincs szükséged egy adott függvényparaméterre,
megváltoztatnád a szignatúrát úgy, hogy ne tartalmazza a nem használt
paramétert. Egy függvényparaméter figyelmen kívül hagyása különösen olyankor
hasznos, amikor például egy trait-et implementálsz, ahol adott típusszignatúrára
van szükség, de az implementációdban a függvény törzsének nincs szüksége az
egyik paraméterre. Így elkerülöd a nem használt függvényparaméterekről szóló
fordítói figyelmeztetést, amelyet név használata esetén kapnál.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Egy érték részei beágyazott `_` mintával

A `_` mintát egy másik mintán belül is használhatjuk, hogy egy értéknek csak egy
részét hagyjuk figyelmen kívül – például amikor egy értéknek csak egy részét
akarjuk vizsgálni, de a többi részre nincs szükségünk a hozzá tartozó,
lefuttatandó kódban. A 19-18. lista olyan kódot mutat be, amely egy beállítás
értékének kezeléséért felel. Az üzleti követelmény az, hogy a felhasználó ne
írhassa felül egy beállítás meglévő testreszabását, de törölhesse a beállítást,
és értéket adhasson neki, ha az jelenleg nincs beállítva.

<Listing number="19-18" caption="Aláhúzás használata `Some` variánsokra illeszkedő mintákban, amikor nincs szükségünk a `Some`-on belüli értékre">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Ez a kód a `Can't overwrite an existing customized value`, majd a `setting is
Some(5)` szöveget írja ki. Az első `match`-ágban nem kell illesztenünk a `Some`
variánsokon belüli értékekre, és nem is használjuk őket, de vizsgálnunk kell azt
az esetet, amikor a `setting_value` és a `new_setting_value` is `Some` variáns.
Ebben az esetben kiírjuk, miért nem változtatjuk meg a `setting_value` értékét,
és az valóban változatlan marad.

Minden más esetben (ha a `setting_value` vagy a `new_setting_value` `None`),
amelyet a második ág `_` mintája fejez ki, azt szeretnénk, hogy a
`new_setting_value` legyen a `setting_value` új értéke.

Egyetlen mintán belül több helyen is használhatunk aláhúzást, hogy bizonyos
értékeket figyelmen kívül hagyjunk. A 19-19. lista arra mutat példát, hogyan
hagyjuk figyelmen kívül egy ötelemű tuple második és negyedik értékét.

<Listing number="19-19" caption="Egy tuple több részének figyelmen kívül hagyása">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Ez a kód a `Some numbers: 2, 8, 32` szöveget írja ki, a `4` és a `16` értéket
pedig figyelmen kívül hagyja.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Nem használt változó a nevének `_` jellel kezdésével

Ha létrehozol egy változót, de sehol nem használod, a Rust általában
figyelmeztetést ad, mert egy nem használt változó hiba jele lehet. Néha azonban
hasznos létrehozni olyan változót, amelyet még nem használsz – például
prototípus készítésekor vagy egy projekt kezdetén. Ilyenkor úgy mondhatod meg a
Rustnak, hogy ne figyelmeztessen a nem használt változóra, hogy a változó nevét
aláhúzással kezded. A 19-20. listában két nem használt változót hozunk létre, de
a kód lefordításakor csak az egyikről kell figyelmeztetést kapnunk.

<Listing number="19-20" file-name="src/main.rs" caption="Változónév kezdése aláhúzással a nem használt változóról szóló figyelmeztetés elkerülésére">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Itt figyelmeztetést kapunk arról, hogy nem használjuk az `y` változót, de a
`_x`-ről nem kapunk figyelmeztetést.

Vedd észre, hogy van egy finom különbség a puszta `_` és az aláhúzással kezdődő
név használata között. Az `_x` szintaxis továbbra is az értékhez köti a
változót, míg a `_` egyáltalán nem köt. Egy olyan eset bemutatására, ahol ez a
különbség számít, a 19-21. lista hibát eredményez.

<Listing number="19-21" caption="Az aláhúzással kezdődő, nem használt változó továbbra is az értékhez kötődik, ami átveheti az érték ownershipjét.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Hibát fogunk kapni, mert az `s` érték továbbra is bemove-olódik az `_s`-be, ami
megakadályozza, hogy újra használjuk az `s`-t. A magában álló aláhúzás azonban
soha nem kötődik az értékhez. A 19-22. lista hiba nélkül fordul le, mert az `s`
nem move-olódik a `_`-be.

<Listing number="19-22" caption="Az aláhúzás használata nem köti meg az értéket.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Ez a kód tökéletesen működik, mert az `s`-t soha nem kötjük semmihez; nem
move-olódik.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Egy érték megmaradt részei a `..` szintaxissal

Sok részből álló értékeknél a `..` szintaxissal használhatunk meghatározott
részeket, a többit pedig figyelmen kívül hagyhatjuk, így nem kell minden
mellőzött értékhez aláhúzást felsorolnunk. A `..` minta figyelmen kívül hagyja
az érték minden olyan részét, amelyre a minta többi részében nem illesztettünk
kifejezetten. A 19-23. listában van egy `Point` structunk, amely egy
háromdimenziós térbeli koordinátát tárol. A `match` kifejezésben csak az `x`
koordinátával akarunk dolgozni, az `y` és `z` mezők értékeit pedig figyelmen
kívül hagyni.

<Listing number="19-23" caption="A `Point` minden mezőjének figyelmen kívül hagyása az `x` kivételével a `..` használatával">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Felsoroljuk az `x` értéket, majd egyszerűen hozzávesszük a `..` mintát. Ez
gyorsabb, mint az `y: _` és `z: _` felsorolása, különösen ha sok mezőt
tartalmazó structokkal dolgozunk olyan helyzetekben, ahol csak egy-két mező
lényeges.

A `..` szintaxis annyi értékre bővül ki, amennyire szükséges. A 19-24. lista azt
mutatja be, hogyan használhatjuk a `..`-ot egy tuple-lel.

<Listing number="19-24" file-name="src/main.rs" caption="Csak egy tuple első és utolsó értékére illesztés, a többi érték figyelmen kívül hagyása">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Ebben a kódban az első és az utolsó érték a `first` és a `last` változóra
illeszkedik. A `..` illeszkedik mindenre, ami közte van, és figyelmen kívül
hagyja.

A `..` használatának azonban egyértelműnek kell lennie. Ha nem világos, mely
értékeket akarjuk illeszteni, és melyeket figyelmen kívül hagyni, a Rust hibát
jelez. A 19-25. lista a `..` kétértelmű használatára mutat példát, ezért nem
fordul le.

<Listing number="19-25" file-name="src/main.rs" caption="Kísérlet a `..` kétértelmű használatára">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Amikor lefordítjuk ezt a példát, a következő hibát kapjuk:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

A Rust képtelen eldönteni, hány értéket kell figyelmen kívül hagynia a
tuple-ben, mielőtt egy értéket a `second` változóra illeszt, és utána hány
további értéket kell mellőznie. Ez a kód jelenthetné azt, hogy a `2`-t figyelmen
kívül akarjuk hagyni, a `second`-öt a `4`-hez kötjük, majd a `8`-at, `16`-ot és
`32`-t mellőzzük; de azt is, hogy a `2`-t és a `4`-et hagyjuk figyelmen kívül, a
`second`-öt a `8`-hoz kötjük, majd a `16`-ot és a `32`-t mellőzzük; és így
tovább. A `second` változónév a Rust számára nem jelent semmi különöset, ezért
fordítási hibát kapunk, mivel a `..` ilyen kétszeri használata kétértelmű.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Feltételek hozzáadása match guardokkal {#adding-conditionals-with-match-guards}

A _match guard_ egy további `if` feltétel, amelyet a `match`-ág mintája után
adunk meg, és amelynek szintén teljesülnie kell ahhoz, hogy az adott ág legyen
kiválasztva. A match guardok olyan összetettebb gondolatok kifejezésére
hasznosak, amelyeket önmagában egy minta nem tesz lehetővé. Vedd figyelembe
azonban, hogy csak `match` kifejezésekben állnak rendelkezésre, `if let` vagy
`while let` kifejezésekben nem.

A feltétel használhatja a mintában létrehozott változókat. A 19-26. lista egy
olyan `match`-et mutat be, amelynek első ága a `Some(x)` mintát tartalmazza, és
egy `if x % 2 == 0` match guardot is (ez `true` lesz, ha a szám páros).

<Listing number="19-26" caption="Match guard hozzáadása egy mintához">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Ez a példa a `The number 4 is even` szöveget írja ki. Amikor a `num` értéket az
első ág mintájához hasonlítjuk, az illeszkedik, mert a `Some(4)` illeszkedik a
`Some(x)` mintára. Ezután a match guard megvizsgálja, hogy az `x` 2-vel való
osztásának maradéka egyenlő-e 0-val, és mivel igen, az első ág lesz kiválasztva.

Ha a `num` értéke `Some(5)` lett volna, az első ág match guardja `false` értéket
adott volna, mert az 5 osztva 2-vel maradéka 1, ami nem egyenlő 0-val. A Rust
ekkor a második ágra lépett volna, amely illeszkedett volna, hiszen a második
ágnak nincs match guardja, így minden `Some` variánsra illeszkedik.

Az `if x % 2 == 0` feltételt sehogy sem lehet mintán belül kifejezni, így a
match guard adja meg a lehetőséget e logika megfogalmazására. Ennek a
többletkifejező erőnek az az ára, hogy a fordító nem próbálja ellenőrizni a
kimerítőséget, ha match guard kifejezések is szerepelnek.

A 19-11. lista tárgyalásakor említettük, hogy a mintában történő shadowing
problémáját match guardokkal oldhatnánk meg. Emlékezz vissza: a `match`
kifejezésen belüli mintában új változót hoztunk létre ahelyett, hogy a
`match`-en kívüli változót használtuk volna. Ez az új változó azt jelentette,
hogy nem tudtunk a külső változó értékére vizsgálni. A 19-27. lista bemutatja,
hogyan javíthatjuk ki ezt a problémát egy match guarddal.

<Listing number="19-27" file-name="src/main.rs" caption="Match guard használata egy külső változóval való egyenlőség vizsgálatára">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Ez a kód most már a `Default case, x = Some(5)` szöveget írja ki. A második
`match`-ág mintája nem vezet be új `y` változót, amely shadowingolná a külső
`y`-t, így a match guardban a külső `y`-t használhatjuk. Ahelyett, hogy a mintát
`Some(y)`-ként adnánk meg – ami shadowingolta volna a külső `y`-t –, a `Some(n)`
mintát adjuk meg. Ez létrehoz egy új `n` változót, amely semmit sem shadowingol,
mert a `match`-en kívül nincs `n` változó.

Az `if n == y` match guard nem minta, ezért nem vezet be új változókat. Ez az
`y` _valóban_ a külső `y`, nem pedig egy azt shadowingoló új `y`, így az `n` és
az
`y` összehasonlításával olyan értéket kereshetünk, amely megegyezik a külső `y`
értékével.

A match guardban a _vagy_ operátort, a `|` jelet is használhatod több minta
megadására; a match guard feltétele az összes mintára vonatkozik. A 19-28. lista
azt mutatja be, milyen precedencia érvényes, amikor egy `|`-t használó mintát
match guarddal kombinálunk. A példa lényege, hogy az `if y` match guard a `4`,
az `5` _és_ a `6` értékre is vonatkozik, még ha úgy is tűnhet, mintha az `if y`
csak a `6`-ra vonatkozna.

<Listing number="19-28" caption="Több minta kombinálása match guarddal">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Az illesztési feltétel azt mondja ki, hogy az ág csak akkor illeszkedik, ha az
`x` értéke `4`, `5` vagy `6`, _és_ az `y` értéke `true`. Amikor ez a kód lefut,
az első ág mintája illeszkedik, mert az `x` értéke `4`, de az `if y` match guard
`false`, így nem az első ágat választja. A kód a második ágra lép, amely
illeszkedik, és a program a `no` szöveget írja ki. Ennek oka, hogy az `if`
feltétel a teljes `4 | 5 | 6` mintára vonatkozik, nem csak az utolsó `6`
értékre. Más szóval a match guard precedenciája a mintához képest így
viselkedik:

```text
(4 | 5 | 6) if y => ...
```

nem pedig így:

```text
4 | 5 | (6 if y) => ...
```

A kód lefuttatása után nyilvánvalóvá válik a precedencia viselkedése: ha a match
guard csak a `|` operátorral megadott értéklista utolsó elemére vonatkozna, az
ág illeszkedett volna, és a program a `yes` szöveget írta volna ki.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### `@` kötések használata

Az _at_ operátor, a `@` jel lehetővé teszi, hogy létrehozzunk egy változót,
amely egy értéket tárol, miközben egyúttal mintaillesztéssel vizsgáljuk is ezt
az értéket. A 19-29. listában azt akarjuk ellenőrizni, hogy egy `Message::Hello`
`id` mezője a `3..=7` tartományba esik-e. Emellett az értéket az `id` változóhoz
is szeretnénk kötni, hogy használhassuk az ághoz tartozó kódban.

<Listing number="19-29" caption="A `@` használata egy minta értékéhez való kötésre, egyúttal az érték vizsgálatára">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Ez a példa a `Found an id in range: 5` szöveget írja ki. Azzal, hogy az `id @`
részt a `3..=7` tartomány elé írjuk, az `id` nevű változóban elkapjuk azt az
értéket, amely a tartományra illeszkedett, miközben azt is vizsgáljuk, hogy az
érték illeszkedik-e a tartománymintára.

A második ágban, ahol a mintában csak egy tartomány szerepel, az ághoz tartozó
kódban nincs olyan változó, amely az `id` mező tényleges értékét tartalmazná. Az
`id` mező értéke lehetett 10, 11 vagy 12 is, de a mintához tartozó kód nem
tudja, melyik. A minta kódja nem tudja használni az `id` mező értékét, mert nem
mentettük el az `id` értékét egy változóba.

Az utolsó ágban, ahol tartomány nélkül adtunk meg egy változót, az érték
rendelkezésre áll az ág kódjában, egy `id` nevű változóban. Ennek oka, hogy a
struct-mezőrövidítés szintaxisát használtuk. Ebben az ágban viszont semmilyen
vizsgálatnak nem vetettük alá az `id` mező értékét, ahogy azt az első két ágban
tettük: erre a mintára bármilyen érték illeszkedik.

A `@` használatával egyetlen mintán belül vizsgálhatunk egy értéket, és el is
menthetjük egy változóba.

## Összefoglalás

A Rust mintái nagyon hasznosak abban, hogy különbséget tegyünk az adatok
különböző fajtái között. Ha `match` kifejezésekben használjuk őket, a Rust
biztosítja, hogy a mintáid minden lehetséges értéket lefedjenek, különben a
programod nem fordul le. A `let` utasításokban és a függvényparaméterekben
használt minták hasznosabbá teszik ezeket a szerkezeteket, mert lehetővé teszik
az értékek kisebb részekre bontását, és e részek változókhoz rendelését.
Szükségleteinknek megfelelően egyszerű és összetett mintákat is létrehozhatunk.

A következőkben, a könyv utolsó előtti fejezetében a Rust különféle nyelvi
elemeinek néhány haladó vonatkozását nézzük meg.
