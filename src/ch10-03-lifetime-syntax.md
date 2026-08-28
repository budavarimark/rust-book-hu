## Referenciák érvényességének ellenőrzése lifetime-okkal {#validating-references-with-lifetimes}

A lifetime-ok a generikusok egy másik fajtáját jelentik, amelyet már eddig is
használtunk. Ahelyett, hogy azt biztosítanák, hogy egy típus a kívánt
viselkedéssel rendelkezik, a lifetime-ok azt garantálják, hogy a referenciák
addig érvényesek, ameddig szükségünk van rájuk.

Az egyik részlet, amelyről a 4. fejezet [„Referenciák és
borrowing”][references-and-borrowing]<!-- ignore --> című szakaszában nem
beszéltünk, az, hogy a Rustban minden referenciának van lifetime-ja, vagyis egy
hatóköre, amelyen belül az adott referencia érvényes. A lifetime-ok legtöbbször
implicitek, és a fordító következteti ki őket, ahogyan a típusok is legtöbbször
kikövetkeztethetők. Csak akkor kell típust megadnunk, ha több típus is szóba
jöhet. Hasonlóképpen akkor kell lifetime-okat megadnunk, ha a referenciák
lifetime-jai többféleképpen is összefügghetnének egymással. A Rust megköveteli,
hogy generikus lifetime-paraméterekkel jelöljük ezeket az összefüggéseket, így
biztosítva, hogy a futásidőben ténylegesen használt referenciák biztosan
érvényesek legyenek.

A lifetime-ok jelölése olyan fogalom, amely a legtöbb más programozási nyelvben
nem is létezik, ezért szokatlannak fog tűnni. Bár a lifetime-okat ebben a
fejezetben nem tárgyaljuk a teljes mélységükben, azokat a gyakori eseteket
átbeszéljük, amelyekben a lifetime-szintaxissal találkozhatsz, hogy
megbarátkozz a fogalommal.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Dangling referenciák

A lifetime-ok fő célja a dangling referenciák megelőzése, amelyek — ha
létezhetnének — azt okoznák, hogy egy program nem arra az adatra hivatkozik,
amelyre hivatkoznia kellene. Nézzük meg a 10-16. listában szereplő programot,
amelyben van egy külső és egy belső hatókör.

<Listing number="10-16" caption="Kísérlet egy olyan referencia használatára, amelynek az értéke kikerült a hatóköréből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Megjegyzés: A 10-16., a 10-17. és a 10-23. lista példáiban a változókat
> kezdőérték nélkül deklaráljuk, így a változónév a külső hatókörben létezik.
> Első pillantásra úgy tűnhet, hogy ez ellentmond annak, hogy a Rustban nincs
> null érték. Ha azonban megpróbálunk használni egy változót, mielőtt értéket
> adnánk neki, fordítási idejű hibát kapunk, ami épp azt mutatja, hogy a Rust
> valóban nem enged meg null értékeket.

A külső hatókör deklarál egy `r` nevű változót kezdőérték nélkül, a belső
hatókör pedig egy `x` nevű változót `5` kezdőértékkel. A belső hatókörben
megpróbáljuk az `r` értékét egy `x`-re mutató referenciára állítani. Ezután a
belső hatókör véget ér, mi pedig megpróbáljuk kiírni az `r`-ben lévő értéket.
Ez a kód nem fordul le, mert az az érték, amelyre az `r` hivatkozik, kikerült a
hatóköréből, mielőtt használni próbálnánk. Íme a hibaüzenet:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

A hibaüzenet szerint az `x` változó „does not live long enough”, vagyis nem él
elég sokáig. Ennek az az oka, hogy az `x` kikerül a hatóköréből, amikor a belső
hatókör a 7. sorban véget ér. Az `r` viszont a külső hatókörben még érvényes;
mivel a hatóköre nagyobb, azt mondjuk, hogy „tovább él”. Ha a Rust megengedné,
hogy ez a kód működjön, az `r` olyan memóriára hivatkozna, amelyet felszabadított
a rendszer, amikor az `x` kikerült a hatóköréből, és semmi sem működne rendesen,
amit az `r`-rel próbálnánk csinálni. Hogyan állapítja meg tehát a Rust, hogy ez
a kód érvénytelen? A borrow checkert használja hozzá.

### A borrow checker

A Rust fordítójában van egy _borrow checker_, amely hatóköröket hasonlít össze
annak eldöntésére, hogy minden borrow érvényes-e. A 10-17. lista ugyanazt a
kódot mutatja, mint a 10-16. lista, de jelölésekkel kiegészítve, amelyek a
változók lifetime-ját mutatják.

<Listing number="10-17" caption="Az `r` és az `x` lifetime-jának jelölése `'a`, illetve `'b` néven">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Itt az `r` lifetime-ját `'a`-val, az `x` lifetime-ját pedig `'b`-vel jelöltük.
Ahogy látod, a belső `'b` blokk sokkal kisebb, mint a külső `'a`
lifetime-blokk. Fordítási időben a Rust összehasonlítja a két lifetime méretét,
és látja, hogy az `r` lifetime-ja `'a`, ám olyan memóriára hivatkozik, amelynek
a lifetime-ja `'b`. A program elutasításra kerül, mert a `'b` rövidebb, mint az
`'a`: a referencia tárgya nem él olyan sokáig, mint maga a referencia.

A 10-18. lista úgy javítja ki a kódot, hogy ne legyen benne dangling
referencia, és hiba nélkül lefordul.

<Listing number="10-18" caption="Érvényes referencia, mert az adat lifetime-ja hosszabb, mint a referenciáé">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Itt az `x` lifetime-ja `'b`, amely ebben az esetben nagyobb, mint az `'a`. Ez
azt jelenti, hogy az `r` hivatkozhat az `x`-re, mert a Rust tudja, hogy az
`r`-ben lévő referencia mindig érvényes lesz, amíg az `x` érvényes.

Most, hogy tudod, hol vannak a referenciák lifetime-jai, és hogyan elemzi a
Rust a lifetime-okat annak biztosítására, hogy a referenciák mindig érvényesek
legyenek, nézzük meg a generikus lifetime-okat a függvények paramétereiben és
visszatérési értékeiben.

### Generikus lifetime-ok függvényekben

Írunk egy függvényt, amely két string slice közül a hosszabbikat adja vissza.
Ez a függvény két string slice-t vesz át, és egyetlen string slice-t ad vissza.
Miután megírtuk a `longest` függvény implementációját, a 10-19. listában lévő
kódnak a `The longest string is abcd` szöveget kell kiírnia.

<Listing number="10-19" file-name="src/main.rs" caption="Egy `main` függvény, amely a `longest` függvényt hívja meg, hogy megkeresse a hosszabbik string slice-t">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Figyeld meg, hogy azt szeretnénk, ha a függvény string slice-okat venne át,
amelyek referenciák, nem pedig stringeket, mert nem akarjuk, hogy a `longest`
függvény átvegye a paraméterei ownershipjét. A 4. fejezet [„String slice-ok
paraméterként”][string-slices-as-parameters]<!-- ignore --> című szakaszában
bővebben olvashatsz arról, miért éppen azok a paraméterek felelnek meg nekünk,
amelyeket a 10-19. listában használunk.

Ha a `longest` függvényt a 10-20. listában látható módon próbáljuk
implementálni, nem fog lefordulni.

<Listing number="10-20" file-name="src/main.rs" caption="A `longest` függvény egy implementációja, amely két string slice közül a hosszabbikat adja vissza, de még nem fordul le">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Ehelyett a következő hibát kapjuk, amely a lifetime-okról szól:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

A segítő szövegből kiderül, hogy a visszatérési típushoz generikus
lifetime-paraméter kell, mert a Rust nem tudja megállapítani, hogy a
visszaadott referencia az `x`-re vagy az `y`-ra hivatkozik-e. Valójában mi sem
tudjuk, hiszen a függvény törzsében az `if` blokk egy `x`-re mutató
referenciát, az `else` blokk pedig egy `y`-ra mutató referenciát ad vissza!

Amikor ezt a függvényt definiáljuk, nem tudjuk, milyen konkrét értékeket adnak
majd át neki, tehát azt sem tudjuk, hogy az `if` vagy az `else` ág fog-e
lefutni. Azt sem tudjuk, mik lesznek az átadott referenciák konkrét
lifetime-jai, így nem tudjuk megvizsgálni a hatóköröket úgy, ahogy a 10-17. és
a 10-18. listában tettük, hogy eldöntsük, a visszaadott referencia mindig
érvényes lesz-e. A borrow checker sem tudja ezt megállapítani, mert nem tudja,
hogyan viszonyul az `x` és az `y` lifetime-ja a visszatérési érték
lifetime-jához. A hiba javításához generikus lifetime-paramétereket adunk
hozzá, amelyek meghatározzák a referenciák közötti kapcsolatot, hogy a borrow
checker elvégezhesse az elemzését.

### A lifetime-jelölés szintaxisa

A lifetime-jelölések nem változtatják meg, hogy a referenciák meddig élnek.
Ehelyett azt írják le, hogy több referencia lifetime-ja hogyan viszonyul
egymáshoz, anélkül hogy hatással lennének magukra a lifetime-okra. Ahogy egy
függvény bármilyen típust elfogadhat, ha a szignatúrája generikus
típusparamétert ad meg, ugyanúgy egy függvény bármilyen lifetime-ú referenciát
elfogadhat, ha generikus lifetime-paramétert ad meg.

A lifetime-jelölések szintaxisa kissé szokatlan: a lifetime-paraméterek nevének
aposztróffal (`'`) kell kezdődnie, és általában csupa kisbetűsek és nagyon
rövidek, akárcsak a generikus típusok nevei. A legtöbben az `'a` nevet
használják az első lifetime-jelöléshez. A lifetime-paraméter jelölését a
referencia `&` jele után helyezzük el, és egy szóközzel választjuk el a
referencia típusától.

Íme néhány példa: egy `i32`-re mutató referencia lifetime-paraméter nélkül, egy
`i32`-re mutató referencia `'a` nevű lifetime-paraméterrel, valamint egy
`i32`-re mutató módosítható referencia, szintén `'a` lifetime-mal:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Egyetlen lifetime-jelölés önmagában nem sokat jelent, mert a jelölések célja
az, hogy elmondják a Rustnak, több referencia generikus lifetime-paraméterei
hogyan viszonyulnak egymáshoz. Nézzük meg, hogyan viszonyulnak egymáshoz a
lifetime-jelölések a `longest` függvény esetében.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Függvényszignatúrákban

Ahhoz, hogy lifetime-jelöléseket használjunk a függvényszignatúrákban, a
generikus lifetime-paramétereket a függvény neve és a paraméterlista között,
csúcsos zárójelek között kell deklarálnunk, ugyanúgy, ahogy a generikus
típusparamétereknél tettük.

Azt szeretnénk, ha a szignatúra a következő megkötést fejezné ki: a visszaadott
referencia addig lesz érvényes, amíg mindkét paraméter érvényes. Ez a
paraméterek és a visszatérési érték lifetime-jai közötti kapcsolat. Nevezzük a
lifetime-ot `'a`-nak, majd adjuk hozzá minden referenciához, ahogy a 10-21.
listában látható.

<Listing number="10-21" file-name="src/main.rs" caption="A `longest` függvény definíciója, amely megadja, hogy a szignatúrában szereplő összes referenciának azonos, `'a` lifetime-mal kell rendelkeznie">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Ennek a kódnak le kell fordulnia, és a kívánt eredményt kell adnia, ha a 10-19.
listában szereplő `main` függvénnyel használjuk.

A függvényszignatúra most már elmondja a Rustnak, hogy valamely `'a`
lifetime-ra a függvény két paramétert vesz át, mindkettő olyan string slice,
amely legalább addig él, mint az `'a` lifetime. A függvényszignatúra azt is
elmondja a Rustnak, hogy a függvényből visszaadott string slice szintén
legalább addig fog élni, mint az `'a` lifetime. A gyakorlatban ez azt jelenti,
hogy a `longest` függvény által visszaadott referencia lifetime-ja megegyezik a
függvény argumentumai által hivatkozott értékek lifetime-jai közül a
rövidebbel. Ezek azok az összefüggések, amelyeket a Rusttól elvárunk a kód
elemzésekor.

Ne feledd: amikor megadjuk a lifetime-paramétereket ebben a
függvényszignatúrában, nem változtatjuk meg egyik átadott vagy visszaadott
érték lifetime-ját sem. Inkább azt adjuk meg, hogy a borrow checker utasítson
el minden olyan értéket, amely nem felel meg ezeknek a megkötéseknek. Vedd
észre, hogy a `longest` függvénynek nem kell pontosan tudnia, meddig fog élni
az `x` és az `y`, csak azt, hogy valamilyen hatókör behelyettesíthető az `'a`
helyére, amely kielégíti ezt a szignatúrát.

Amikor lifetime-okat jelölünk a függvényekben, a jelölések a
függvényszignatúrába kerülnek, nem a függvény törzsébe. A lifetime-jelölések a
függvény szerződésének részévé válnak, nagyjából úgy, mint a szignatúrában
szereplő típusok. Az, hogy a függvényszignatúrák tartalmazzák a
lifetime-szerződést, egyszerűbbé teszi a Rust fordítójának elemzését. Ha
probléma van azzal, ahogyan egy függvényt jelöltünk, vagy ahogyan meghívjuk, a
fordítási hibák pontosabban rá tudnak mutatni a kódunk adott részére és a
megkötésekre. Ha ehelyett a Rust fordítója többet következtetne ki arról, hogy
milyen kapcsolatokat szántunk a lifetime-oknak, akkor lehet, hogy csak a kódunk
egy olyan felhasználására tudna rámutatni, amely sok lépésnyire van a probléma
okától.

Amikor konkrét referenciákat adunk át a `longest` függvénynek, az `'a` helyére
behelyettesített konkrét lifetime az `x` hatókörének azon része, amely átfed az
`y` hatókörével. Más szóval a generikus `'a` lifetime azt a konkrét lifetime-ot
kapja, amely az `x` és az `y` lifetime-jai közül a rövidebbel egyenlő. Mivel a
visszaadott referenciát ugyanazzal az `'a` lifetime-paraméterrel jelöltük, a
visszaadott referencia is az `x` és az `y` lifetime-jai közül a rövidebb
hosszáig lesz érvényes.

Nézzük meg, hogyan korlátozzák a lifetime-jelölések a `longest` függvényt: adjunk
át neki olyan referenciákat, amelyeknek eltérő a konkrét lifetime-juk. A 10-22.
lista egy egyszerű példa erre.

<Listing number="10-22" file-name="src/main.rs" caption="A `longest` függvény használata olyan `String` értékekre mutató referenciákkal, amelyeknek eltérő a konkrét lifetime-juk">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Ebben a példában a `string1` a külső hatókör végéig érvényes, a `string2` a
belső hatókör végéig érvényes, a `result` pedig valami olyanra hivatkozik, ami
a belső hatókör végéig érvényes. Futtasd le ezt a kódot, és látni fogod, hogy a
borrow checker jóváhagyja; le fog fordulni, és kiírja: `The longest string is
long string is long`.

Következzék egy olyan példa, amely megmutatja, hogy a `result`-ban lévő
referencia lifetime-jának a két argumentum közül a rövidebb lifetime-nak kell
lennie. A `result` változó deklarációját kivisszük a belső hatókörön kívülre, de
az értékadást a `result` változónak a `string2`-t tartalmazó hatókörön belül
hagyjuk. Ezután a `result`-ot használó `println!` hívást a belső hatókörön
kívülre visszük, a belső hatókör vége utánra. A 10-23. listában lévő kód nem
fog lefordulni.

<Listing number="10-23" file-name="src/main.rs" caption="Kísérlet a `result` használatára, miután a `string2` kikerült a hatóköréből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Amikor megpróbáljuk lefordítani ezt a kódot, ezt a hibát kapjuk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

A hiba azt mutatja, hogy ahhoz, hogy a `result` érvényes legyen a `println!`
utasításnál, a `string2`-nek a külső hatókör végéig érvényesnek kellene lennie.
A Rust ezt azért tudja, mert a függvény paramétereinek és visszatérési
értékének lifetime-ját ugyanazzal az `'a` lifetime-paraméterrel jelöltük.

Emberként ránézhetünk erre a kódra, és láthatjuk, hogy a `string1` hosszabb,
mint a `string2`, ezért a `result` a `string1`-re mutató referenciát fogja
tartalmazni. Mivel a `string1` még nem került ki a hatóköréből, a `string1`-re
mutató referencia a `println!` utasításnál még érvényes lenne. A fordító
azonban nem látja, hogy a referencia ebben az esetben érvényes. Azt mondtuk a
Rustnak, hogy a `longest` függvény által visszaadott referencia lifetime-ja
megegyezik az átadott referenciák lifetime-jai közül a rövidebbel. Ezért a
borrow checker a 10-23. listában lévő kódot elutasítja, mint amelyben lehet
érvénytelen referencia.

Próbálj meg további kísérleteket kitalálni, amelyekben változtatod a `longest`
függvénynek átadott referenciák értékeit és lifetime-jait, valamint azt, hogyan
használod a visszaadott referenciát. Állíts fel feltevéseket arról, hogy a
kísérleteid átmennek-e a borrow checkeren, mielőtt fordítanál; utána pedig
ellenőrizd, igazad volt-e!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Kapcsolatok

Az, hogyan kell megadnod a lifetime-paramétereket, attól függ, mit csinál a
függvényed. Ha például úgy változtatnánk meg a `longest` függvény
implementációját, hogy mindig az első paramétert adja vissza a hosszabbik
string slice helyett, akkor nem kellene lifetime-ot megadnunk az `y`
paraméterhez. A következő kód le fog fordulni:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Megadtunk egy `'a` lifetime-paramétert az `x` paraméterhez és a visszatérési
típushoz, de az `y` paraméterhez nem, mert az `y` lifetime-jának semmilyen
kapcsolata nincs az `x` vagy a visszatérési érték lifetime-jával.

Amikor egy függvényből referenciát adunk vissza, a visszatérési típus
lifetime-paraméterének meg kell egyeznie valamelyik paraméter
lifetime-paraméterével. Ha a visszaadott referencia _nem_ valamelyik
paraméterre hivatkozik, akkor egy, a függvényen belül létrehozott értékre kell
hivatkoznia. Ez azonban dangling referencia lenne, mert az érték a függvény
végén kikerül a hatóköréből. Nézzük a `longest` függvénynek ezt a kísérleti
implementációját, amely nem fordul le:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Itt annak ellenére, hogy megadtunk egy `'a` lifetime-paramétert a visszatérési
típushoz, ez az implementáció nem fog lefordulni, mert a visszatérési érték
lifetime-ja egyáltalán nem függ össze a paraméterek lifetime-jával. Íme a
hibaüzenet, amelyet kapunk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

A gond az, hogy a `result` a `longest` függvény végén kikerül a hatóköréből, és
felszabadul. Ugyanakkor egy `result`-ra mutató referenciát próbálunk
visszaadni a függvényből. Nincs mód olyan lifetime-paraméterek megadására,
amelyek megváltoztatnák a dangling referenciát, a Rust pedig nem engedi, hogy
dangling referenciát hozzunk létre. Ebben az esetben a legjobb megoldás az
lenne, ha referencia helyett birtokolt (owned) adattípust adnánk vissza, így a
hívó függvény felelne az érték felszabadításáért.

Végső soron a lifetime-szintaxis arról szól, hogy összekapcsoljuk a függvények
különböző paramétereinek és visszatérési értékeinek lifetime-jait. Ha egyszer
összekapcsoltuk őket, a Rustnak elég információja van ahhoz, hogy engedélyezze
a memóriabiztos műveleteket, és megtiltsa azokat, amelyek dangling pointereket
hoznának létre, vagy más módon sértenék a memóriabiztonságot.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Struct-definíciókban

Eddig minden struct, amelyet definiáltunk, birtokolt típusokat tárolt.
Definiálhatunk olyan structokat is, amelyek referenciákat tárolnak, ebben az
esetben viszont a struct definíciójában minden referenciához
lifetime-jelölést kell tennünk. A 10-24. listában egy `ImportantExcerpt` nevű
struct szerepel, amely egy string slice-t tárol.

<Listing number="10-24" file-name="src/main.rs" caption="Egy struct, amely referenciát tárol, ezért lifetime-jelölést igényel">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Ennek a structnak egyetlen mezője van, a `part`, amely egy string slice-t
tárol; ez pedig egy referencia. Ahogy a generikus adattípusoknál, a generikus
lifetime-paraméter nevét a struct neve után, csúcsos zárójelek között
deklaráljuk, hogy a lifetime-paramétert használhassuk a struct definíciójának
törzsében. Ez a jelölés azt jelenti, hogy egy `ImportantExcerpt` példány nem
élhet tovább, mint az a referencia, amelyet a `part` mezőjében tárol.

Az itteni `main` függvény létrehozza az `ImportantExcerpt` struct egy példányát,
amely a `novel` változó által birtokolt `String` első mondatára mutató
referenciát tárol. A `novel`-ben lévő adat már azelőtt létezik, hogy az
`ImportantExcerpt` példány létrejönne. Ráadásul a `novel` csak azután kerül ki
a hatóköréből, hogy az `ImportantExcerpt` kikerült a hatóköréből, így az
`ImportantExcerpt` példányban lévő referencia érvényes.

### Lifetime elision

Megtanultad, hogy minden referenciának van lifetime-ja, és hogy meg kell adnod
a lifetime-paramétereket azokhoz a függvényekhez vagy structokhoz, amelyek
referenciákat használnak. A 4-9. listában azonban volt egy függvényünk —
amelyet a 10-25. listában újra megmutatunk —, amely lifetime-jelölések nélkül
is lefordult.

<Listing number="10-25" file-name="src/lib.rs" caption="Egy függvény, amelyet a 4-9. listában definiáltunk, és amely lifetime-jelölések nélkül is lefordult, pedig a paramétere és a visszatérési típusa is referencia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Annak, hogy ez a függvény lifetime-jelölések nélkül lefordul, történeti oka
van: a Rust korai (1.0 előtti) verzióiban ez a kód nem fordult volna le, mert
minden referenciához explicit lifetime kellett. Akkoriban a
függvényszignatúrát így kellett volna leírni:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Sok Rust-kód megírása után a Rust csapata azt tapasztalta, hogy a Rust
programozói bizonyos helyzetekben újra és újra ugyanazokat a
lifetime-jelöléseket gépelik be. Ezek a helyzetek kiszámíthatók voltak, és
néhány determinisztikus mintát követtek. A fejlesztők beleprogramozták ezeket a
mintákat a fordító kódjába, hogy a borrow checker ezekben az esetekben ki tudja
következtetni a lifetime-okat, és ne legyen szükség explicit jelölésekre.

A Rust történetének ez a darabja azért lényeges, mert elképzelhető, hogy újabb
determinisztikus minták bukkannak fel, és bekerülnek a fordítóba. A jövőben
akár még kevesebb lifetime-jelölésre lehet szükség.

Azokat a mintákat, amelyeket beleprogramoztak a Rust referenciaelemzésébe,
_lifetime elision szabályoknak_ nevezzük. Ezek nem olyan szabályok, amelyeket a
programozóknak követniük kell; ezek olyan konkrét esetek halmaza, amelyeket a
fordító figyelembe vesz, és ha a kódod illeszkedik ezekre az esetekre, nem kell
explicit módon kiírnod a lifetime-okat.

Az elision szabályok nem adnak teljes következtetést. Ha azután is
kétértelműség marad azzal kapcsolatban, hogy a referenciáknak milyen
lifetime-juk van, hogy a Rust alkalmazta a szabályokat, a fordító nem fogja
kitalálni, milyen lifetime-ja legyen a fennmaradó referenciáknak. Találgatás
helyett a fordító hibát ad, amelyet lifetime-jelölések hozzáadásával oldhatsz
meg.

A függvény- vagy metódusparamétereken lévő lifetime-okat _input
lifetime_-oknak, a visszatérési értékeken lévőket pedig _output lifetime_-oknak
nevezzük.

A fordító három szabályt használ, hogy explicit jelölések hiányában
kikövetkeztesse a referenciák lifetime-jait. Az első szabály az input
lifetime-okra vonatkozik, a második és a harmadik pedig az output
lifetime-okra. Ha a fordító a három szabály végére ér, és még mindig vannak
olyan referenciák, amelyekhez nem tudja meghatározni a lifetime-ot, akkor a
fordító hibával leáll. Ezek a szabályok az `fn` definíciókra és az `impl`
blokkokra egyaránt érvényesek.

Az első szabály az, hogy a fordító minden olyan paraméterhez hozzárendel egy
lifetime-paramétert, amely referencia. Más szóval egy egyparaméteres függvény
egy lifetime-paramétert kap: `fn foo<'a>(x: &'a i32)`; egy kétparaméteres
függvény két külön lifetime-paramétert kap: `fn foo<'a, 'b>(x: &'a i32, y: &'b
i32)`; és így tovább.

A második szabály az, hogy ha pontosan egy input lifetime-paraméter van, akkor
ez a lifetime kerül az összes output lifetime-paraméterhez: `fn foo<'a>(x: &'a
i32) -> &'a i32`.

A harmadik szabály az, hogy ha több input lifetime-paraméter van, de az egyikük
`&self` vagy `&mut self`, mert metódusról van szó, akkor a `self` lifetime-ja
kerül az összes output lifetime-paraméterhez. Ez a harmadik szabály sokkal
kellemesebbé teszi a metódusok olvasását és írását, mert kevesebb jelre van
szükség.

Képzeljük magunkat a fordító helyébe. Alkalmazzuk ezeket a szabályokat, hogy
kiderítsük a 10-25. listában lévő `first_word` függvény szignatúrájában
szereplő referenciák lifetime-jait. A szignatúra úgy indul, hogy a
referenciákhoz semmilyen lifetime nem tartozik:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Ezután a fordító alkalmazza az első szabályt, amely szerint minden paraméter
saját lifetime-ot kap. Szokás szerint nevezzük ezt `'a`-nak, így a szignatúra
most ez:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

A második szabály is alkalmazható, mert pontosan egy input lifetime van. A
második szabály szerint az egyetlen input paraméter lifetime-ja kerül az output
lifetime-hoz, tehát a szignatúra most ez:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Most már minden referenciának van lifetime-ja ebben a
függvényszignatúrában, és a fordító folytathatja az elemzést anélkül, hogy a
programozónak jelölnie kellene a lifetime-okat ebben a szignatúrában.

Nézzünk egy másik példát, ezúttal a `longest` függvényt, amelynek nem voltak
lifetime-paraméterei, amikor a 10-20. listában elkezdtünk vele foglalkozni:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Alkalmazzuk az első szabályt: minden paraméter saját lifetime-ot kap. Ezúttal
egy helyett két paraméterünk van, tehát két lifetime-unk lesz:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Látható, hogy a második szabály nem alkalmazható, mert egynél több input
lifetime van. A harmadik szabály sem alkalmazható, mert a `longest` függvény,
nem metódus, tehát egyik paramétere sem `self`. Miután végigmentünk mind a
három szabályon, még mindig nem derült ki, mi a visszatérési típus lifetime-ja.
Ezért kaptunk hibát, amikor megpróbáltuk lefordítani a 10-20. listában lévő
kódot: a fordító végigment a lifetime elision szabályokon, de továbbra sem
tudta meghatározni a szignatúrában szereplő összes referencia lifetime-ját.

Mivel a harmadik szabály valójában csak metódusszignatúrákra vonatkozik,
következőként a lifetime-okat ebben a kontextusban nézzük meg, hogy lássuk,
miért jelenti a harmadik szabály azt, hogy metódusszignatúrákban ritkán kell
lifetime-okat jelölnünk.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Metódusdefiníciókban

Amikor lifetime-okkal rendelkező structon implementálunk metódusokat,
ugyanazt a szintaxist használjuk, mint a generikus típusparamétereknél, ahogy a
10-11. listában látható. Az, hogy hol deklaráljuk és hol használjuk a
lifetime-paramétereket, attól függ, hogy a struct mezőihez vagy a metódus
paramétereihez és visszatérési értékeihez kapcsolódnak-e.

A struct mezőihez tartozó lifetime-neveket mindig az `impl` kulcsszó után kell
deklarálni, majd a struct neve után használni, mert ezek a lifetime-ok a struct
típusának részei.

Az `impl` blokkon belüli metódusszignatúrákban a referenciák kötődhetnek a
struct mezőiben lévő referenciák lifetime-jához, de lehetnek függetlenek is.
Ráadásul a lifetime elision szabályok gyakran feleslegessé teszik a
lifetime-jelöléseket a metódusszignatúrákban. Nézzünk néhány példát a 10-24.
listában definiált `ImportantExcerpt` struct segítségével.

Először egy `level` nevű metódust használunk, amelynek egyetlen paramétere egy
`self`-re mutató referencia, a visszatérési értéke pedig egy `i32`, ami nem
referencia semmire:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Az `impl` utáni lifetime-paraméter deklarációja és a típusnév utáni használata
kötelező, de az első elision szabály miatt nem kell jelölnünk a `self`-re
mutató referencia lifetime-ját.

Íme egy példa, ahol a harmadik lifetime elision szabály érvényesül:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Két input lifetime van, ezért a Rust alkalmazza az első lifetime elision
szabályt, és a `&self` is, az `announcement` is saját lifetime-ot kap. Ezután,
mivel az egyik paraméter a `&self`, a visszatérési típus a `&self`
lifetime-ját kapja, és ezzel minden lifetime tisztázva van.

### A `'static` lifetime

Egy különleges lifetime-ról mindenképp beszélnünk kell: ez a `'static`, amely
azt jelöli, hogy az érintett referencia _élhet_ a program teljes futása alatt.
Minden string literál `'static` lifetime-mal rendelkezik, amit így jelölhetünk:

```rust
let s: &'static str = "I have a static lifetime.";
```

Ennek a stringnek a szövege közvetlenül a program binárisában tárolódik, amely
mindig elérhető. Ezért minden string literál lifetime-ja `'static`.

Előfordulhat, hogy a hibaüzenetekben javaslatot látsz a `'static` lifetime
használatára. Mielőtt azonban `'static`-ként adnád meg egy referencia
lifetime-ját, gondold végig, hogy a kérdéses referencia valóban a programod
teljes futása alatt él-e, és hogy egyáltalán ezt akarod-e. A `'static`
lifetime-ot javasló hibaüzenetek legtöbbször abból fakadnak, hogy dangling
referenciát próbálunk létrehozni, vagy hogy nem stimmelnek az elérhető
lifetime-ok. Ilyen esetekben a megoldás ezeknek a problémáknak a kijavítása,
nem pedig a `'static` lifetime megadása.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generikus típusparaméterek, trait bound-ok és lifetime-ok

Nézzük meg röviden, hogyan adhatunk meg generikus típusparamétereket, trait
bound-okat és lifetime-okat egyetlen függvényben!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Ez a 10-21. listából származó `longest` függvény, amely két string slice közül
a hosszabbikat adja vissza. Most azonban van egy extra, `ann` nevű paramétere
`T` generikus típussal, amelynek a helyére bármilyen olyan típus kerülhet,
amely implementálja a `Display` trait-et, ahogy azt a `where` klóz megadja. Ezt
az extra paramétert a `{}` segítségével írjuk ki, ezért van szükség a `Display`
trait bound-ra. Mivel a lifetime-ok a generikusok egy fajtája, az `'a`
lifetime-paraméter és a `T` generikus típusparaméter deklarációja ugyanabba a
listába kerül a függvénynév utáni csúcsos zárójelek között.

## Összefoglalás

Sok mindent áttekintettünk ebben a fejezetben! Most, hogy ismered a generikus
típusparamétereket, a trait-eket és a trait bound-okat, valamint a generikus
lifetime-paramétereket, készen állsz arra, hogy ismétlés nélküli kódot írj,
amely sokféle különböző helyzetben működik. A generikus típusparaméterekkel
különböző típusokra alkalmazhatod ugyanazt a kódot. A trait-ek és a trait
bound-ok biztosítják, hogy a típusok generikussága ellenére meglegyen az a
viselkedésük, amelyre a kódnak szüksége van. Megtanultad, hogyan használd a
lifetime-jelöléseket annak biztosítására, hogy ebben a rugalmas kódban ne
legyenek dangling referenciák. Mindez az elemzés pedig fordítási időben
történik, így nincs hatással a futásidejű teljesítményre!

Akár hiszed, akár nem, az ebben a fejezetben tárgyalt témákról még sokat lehet
tanulni: a 18. fejezet a trait objectekről szól, amelyek a trait-ek
használatának egy másik módját jelentik. Vannak ezenkívül bonyolultabb,
lifetime-jelölésekkel kapcsolatos esetek is, amelyekre csak nagyon haladó
helyzetekben lesz szükséged; ezekhez érdemes elolvasnod a [Rust
Reference-t][reference]. Következőként azonban azt tanulod meg, hogyan írj
teszteket Rustban, hogy meggyőződhess arról: a kódod úgy működik, ahogyan
kell.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
