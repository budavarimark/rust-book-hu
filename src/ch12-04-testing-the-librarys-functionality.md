<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Funkcionalitás hozzáadása tesztvezérelt fejlesztéssel

Most, hogy a keresési logika a _src/lib.rs_ fájlban külön van a `main`
függvénytől, sokkal könnyebb teszteket írni a kódunk lényegi
funkcionalitására. A függvényeket közvetlenül hívhatjuk különféle
argumentumokkal, és ellenőrizhetjük a visszatérési értékeket anélkül, hogy a
binárisunkat a parancssorból kellene meghívnunk.

Ebben a szakaszban a `minigrep` programhoz a tesztvezérelt fejlesztés (TDD,
test-driven development) folyamatával adjuk hozzá a keresési logikát, a
következő lépésekkel:

1. Írj egy tesztet, amely elbukik, és futtasd le, hogy megbizonyosodj róla:
   valóban azért bukik el, amiért várod.
2. Írj vagy módosíts épp csak annyi kódot, hogy az új teszt átmenjen.
3. Refaktoráld az imént hozzáadott vagy módosított kódot, és győződj meg róla,
   hogy a tesztek továbbra is átmennek.
4. Ismételd az 1. lépéstől!

Bár a szoftverírásnak csak az egyik módja, a TDD segíthet a kód tervezésének
irányításában. Ha a tesztet azelőtt írod meg, hogy megírnád a kódot, amitől a
teszt átmegy, az segít magas teszt-lefedettséget fenntartani az egész folyamat
során.

Tesztvezérelten fogjuk implementálni azt a funkcionalitást, amely ténylegesen
elvégzi a keresett szöveg keresését a fájl tartalmában, és előállítja a
lekérdezésre illeszkedő sorok listáját. Ezt a funkcionalitást egy `search` nevű
függvényben adjuk hozzá.

### Elbukó teszt írása

A _src/lib.rs_ fájlban felveszünk egy `tests` modult egy tesztfüggvénnyel,
ahogy azt a [11. fejezetben][ch11-anatomy]<!-- ignore --> is tettük. A
tesztfüggvény megadja azt a viselkedést, amit a `search` függvénytől várunk:
kap egy lekérdezést és a szöveget, amelyben keresni kell, és csak azokat a
sorokat adja vissza a szövegből, amelyek tartalmazzák a lekérdezést. A 12-15.
listában látható ez a teszt.

<Listing number="12-15" file-name="src/lib.rs" caption="Elbukó teszt írása a `search` függvényre, arra a funkcionalitásra, amit szeretnénk, ha meglenne">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Ez a teszt a `"duct"` szövegre keres. A szöveg, amelyben keresünk, három sorból
áll, amelyek közül csak egy tartalmazza a `"duct"` részt (figyeld meg, hogy a
nyitó idézőjel után álló backslash azt mondja a Rustnak, hogy ne tegyen
soremelés karaktert ennek a szöveges literálnak a tartalma elé). Azt állítjuk,
hogy a `search` függvény által visszaadott érték csak a várt sort tartalmazza.

Ha lefuttatjuk ezt a tesztet, jelenleg elbukik, mert az `unimplemented!` makró
a „not implemented” üzenettel vált ki panicot. A TDD elveinek megfelelően
teszünk egy kis lépést: épp csak annyi kódot adunk hozzá, hogy a függvény
hívásakor a teszt ne váltson ki panicot, vagyis a `search` függvényt úgy
definiáljuk, hogy mindig üres vektort adjon vissza, ahogy a 12-16. listában
látható. Ekkor a tesztnek le kell fordulnia és el kell buknia, mert az üres
vektor nem egyezik meg azzal a vektorral, amely a `"safe, fast, productive."`
sort tartalmazza.

<Listing number="12-16" file-name="src/lib.rs" caption="A `search` függvény épp elegendő részének definiálása ahhoz, hogy a hívása ne váltson ki panicot">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Most beszéljük meg, miért kell explicit `'a` lifetime-ot megadnunk a `search`
szignatúrájában, és miért kell ezt a lifetime-ot a `contents` argumentumnál és
a visszatérési értéknél használnunk. Emlékezz vissza a [10.
fejezetre][ch10-lifetimes]<!-- ignore -->: a lifetime-paraméterek adják meg,
melyik argumentum lifetime-ja kapcsolódik a visszatérési érték lifetime-jához.
Ebben az esetben azt jelezzük, hogy a visszaadott vektor olyan string
slice-okat tartalmaz, amelyek a `contents` argumentum részeire hivatkoznak (nem
pedig a `query` argumentumra).

Más szóval azt mondjuk a Rustnak, hogy a `search` függvény által visszaadott
adat addig fog élni, ameddig a `search` függvénynek a `contents` argumentumban
átadott adat. Ez fontos! Annak az adatnak, amelyre egy slice _hivatkozik_,
érvényesnek kell lennie ahhoz, hogy a referencia is érvényes legyen; ha a
fordító azt feltételezi, hogy a `query`-ből, nem pedig a `contents`-ből
készítünk string slice-okat, akkor helytelenül végzi el a biztonsági
ellenőrzéseit.

Ha elfelejtjük a lifetime-annotációkat, és megpróbáljuk lefordítani ezt a
függvényt, ezt a hibát kapjuk:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

A Rust nem tudhatja, hogy a két paraméter közül melyikre van szükségünk a
kimenethez, ezért ezt explicit módon meg kell mondanunk neki. Figyeld meg, hogy
a súgószöveg azt javasolja, hogy minden paraméternek és a kimeneti típusnak
ugyanazt a lifetime-paramétert adjuk meg, ami helytelen! Mivel a `contents` az
a paraméter, amely a teljes szövegünket tartalmazza, és ennek a szövegnek az
illeszkedő részeit akarjuk visszaadni, tudjuk, hogy a `contents` az egyetlen
paraméter, amelyet a lifetime-szintaxissal a visszatérési értékhez kell
kapcsolnunk.

Más programozási nyelvek nem követelik meg, hogy a szignatúrában összekapcsold
az argumentumokat a visszatérési értékekkel, de ez a gyakorlat idővel egyre
könnyebb lesz. Érdemes összevetned ezt a példát a 10. fejezet [„Referenciák
érvényesítése lifetime-okkal”][validating-references-with-lifetimes]<!-- ignore
--> című szakaszának példáival.

### Kód írása a teszt teljesítéséhez

Jelenleg a tesztünk elbukik, mert mindig üres vektort adunk vissza. Ennek
javításához és a `search` implementálásához a programunknak a következő
lépéseket kell követnie:

1. Iteráljon végig a tartalom minden során.
2. Ellenőrizze, hogy a sor tartalmazza-e a keresett szövegünket.
3. Ha igen, adja hozzá a visszaadandó értékek listájához.
4. Ha nem, ne csináljon semmit.
5. Adja vissza az illeszkedő eredmények listáját.

Nézzük végig lépésről lépésre, kezdve a sorokon való iterálással.

#### Iterálás a sorokon a `lines` metódussal

A Rustban van egy hasznos metódus a szövegek soronkénti bejárására, amelynek
találó neve `lines`, és úgy működik, ahogy a 12-17. listában látható. Figyeld
meg, hogy ez még nem fordul le.

<Listing number="12-17" file-name="src/lib.rs" caption="Iterálás a `contents` minden során">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

A `lines` metódus egy iterátort ad vissza. Az iterátorokról részletesen a [13.
fejezetben][ch13-iterators]<!-- ignore --> lesz szó. De emlékezz rá, hogy az
iterátorok ilyen használatát már láttad a [3-5. listában][ch3-iter]<!-- ignore
-->, ahol egy `for` ciklust használtunk egy iterátorral, hogy egy kollekció
minden elemén lefuttassunk valamilyen kódot.

#### Minden sor átvizsgálása a lekérdezésre

Ezután megnézzük, hogy az aktuális sor tartalmazza-e a keresett szövegünket.
Szerencsére a szövegeknek van egy hasznos, `contains` nevű metódusa, amely épp
ezt teszi meg helyettünk! Add hozzá a `contains` metódus hívását a `search`
függvényhez, ahogy a 12-18. listában látható. Figyeld meg, hogy ez még mindig
nem fordul le.

<Listing number="12-18" file-name="src/lib.rs" caption="Funkcionalitás hozzáadása annak megállapítására, hogy a sor tartalmazza-e a `query` szövegét">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Pillanatnyilag épp építjük fel a funkcionalitást. Ahhoz, hogy a kód
lefordulhasson, vissza kell adnunk egy értéket a törzsből, ahogy azt a függvény
szignatúrájában jeleztük.

#### Az illeszkedő sorok tárolása

A függvény befejezéséhez szükségünk van valamilyen módra, amellyel tárolni
tudjuk a visszaadni kívánt illeszkedő sorokat. Ehhez létrehozhatunk egy
módosítható vektort a `for` ciklus előtt, és a `push` metódussal eltárolhatjuk
a `line` értéket a vektorban. A `for` ciklus után visszaadjuk a vektort, ahogy
a 12-19. listában látható.

<Listing number="12-19" file-name="src/lib.rs" caption="Az illeszkedő sorok tárolása, hogy vissza tudjuk adni őket">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Most a `search` függvénynek már csak azokat a sorokat kell visszaadnia, amelyek
tartalmazzák a `query`-t, és a tesztünknek át kell mennie. Futtassuk le a
tesztet:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

A tesztünk átment, tehát tudjuk, hogy működik!

Ezen a ponton megfontolhatnánk a keresőfüggvény implementációjának
refaktorálási lehetőségeit, ügyelve arra, hogy a tesztek továbbra is átmenjenek,
és így ugyanaz maradjon a funkcionalitás. A keresőfüggvény kódja nem is olyan
rossz, de nem használja ki az iterátorok néhány hasznos képességét. Ehhez a
példához a [13. fejezetben][ch13-iterators]<!-- ignore --> térünk vissza, ahol
részletesen megvizsgáljuk az iterátorokat, és megnézzük, hogyan lehetne
javítani rajta.

Most már az egész programnak működnie kell! Próbáljuk ki, először egy olyan
szóval, amely pontosan egy sort ad vissza az Emily Dickinson-versből: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Klassz! Most próbáljunk ki egy olyan szót, amely több sorra is illeszkedik,
például a _body_ szót:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Végül pedig győződjünk meg róla, hogy nem kapunk egyetlen sort sem, amikor egy
olyan szóra keresünk, amely sehol nem szerepel a versben, például a
_monomorphization_ szóra:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Kiváló! Megépítettük egy klasszikus eszköz saját mini változatát, és sokat
tanultunk arról, hogyan érdemes alkalmazásokat felépíteni. Tanultunk egy keveset
a fájlok be- és kimenetéről, a lifetime-okról, a tesztelésről és a parancssori
argumentumok feldolgozásáról is.

A projekt lekerekítéseként röviden bemutatjuk, hogyan lehet környezeti
változókkal dolgozni, és hogyan lehet a standard hibakimenetre írni; mindkettő
hasznos, amikor parancssori programokat írsz.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
