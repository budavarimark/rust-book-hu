## A `Box<T>` használata heapen lévő adatra mutatáshoz

A legegyszerűbb smart pointer a box, amelynek típusát `Box<T>` alakban írjuk. A
_boxok_ lehetővé teszik, hogy az adatot a stack helyett a heapen tárold. A
stacken csak a heapen lévő adatra mutató pointer marad. A stack és a heap közötti
különbség felelevenítéséhez lapozz vissza a 4. fejezethez.

A boxok nem járnak teljesítménybeli többletköltséggel azon kívül, hogy az
adatukat a stack helyett a heapen tárolják. Ugyanakkor sok extra képességük
sincs. Leggyakrabban ezekben a helyzetekben fogod használni őket:

- Amikor olyan típusod van, amelynek a mérete fordítási időben nem ismerhető meg,
  és ilyen típusú értéket szeretnél használni olyan környezetben, amely pontos
  méretet vár
- Amikor nagy mennyiségű adatod van, és át szeretnéd adni az ownershipet, de
  biztosítani szeretnéd, hogy az adat eközben ne másolódjon
- Amikor birtokolni szeretnél egy értéket, és csak az számít, hogy egy adott
  trait-et implementáló típus legyen, nem pedig az, hogy konkrétan milyen típus

Az első helyzetet a [„Rekurzív típusok engedélyezése
boxokkal”](#enabling-recursive-types-with-boxes)<!-- ignore --> szakaszban
mutatjuk be. A második esetben nagy mennyiségű adat ownershipjének átadása sokáig
tarthat, mert az adat ide-oda másolódik a stacken. Hogy ebben a helyzetben
javítsuk a teljesítményt, a nagy mennyiségű adatot egy boxban a heapen
tárolhatjuk. Ekkor csak a kevés pointeradat másolódik a stacken, míg a
hivatkozott adat egy helyben marad a heapen. A harmadik esetet _trait
object_-nek nevezik, és a 18. fejezet [„Trait objectek használata közös
viselkedés absztrahálására”][trait-objects]<!-- ignore --> című szakasza teljes
egészében ezzel a témával foglalkozik. Amit tehát itt megtanulsz, azt abban a
szakaszban újra alkalmazni fogod!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Adatok tárolása a heapen

Mielőtt a `Box<T>` heapes tárolásra vonatkozó felhasználási esetét tárgyalnánk,
nézzük meg a szintaxist, és azt, hogyan dolgozhatunk a `Box<T>`-ben tárolt
értékekkel.

A 15-1. lista bemutatja, hogyan tárolhatunk egy `i32` értéket a heapen egy box
segítségével.

<Listing number="15-1" file-name="src/main.rs" caption="Egy `i32` érték tárolása a heapen box használatával">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

A `b` változót úgy definiáljuk, hogy egy `Box` értékét vegye fel, amely az `5`
értékre mutat; ez az érték a heapen van lefoglalva. Ez a program a `b = 5`
szöveget írja ki; ebben az esetben ugyanúgy férhetünk hozzá a boxban lévő
adathoz, ahogy akkor tennénk, ha ez az adat a stacken lenne. Mint minden
birtokolt érték, a box is felszabadul, amikor kilép a hatóköréből – ahogy a `b`
teszi a `main` végén. A felszabadítás egyaránt vonatkozik magára a boxra (amely a
stacken van tárolva) és az adatra, amelyre mutat (amely a heapen van tárolva).

Egyetlen érték heapre helyezése nem túl hasznos, ezért a boxokat önmagukban
ilyen módon nem fogod gyakran használni. Az olyan értékeket, mint egyetlen `i32`,
a legtöbb helyzetben helyénvalóbb a stacken tartani, ahol alapértelmezés szerint
tárolódnak. Nézzünk meg egy olyan esetet, ahol a boxok olyan típusok
definiálását teszik lehetővé, amelyeket boxok nélkül nem definiálhatnánk.

### Rekurzív típusok engedélyezése boxokkal {#enabling-recursive-types-with-boxes}

Egy _rekurzív típus_ értéke saját magának a részeként tartalmazhat egy másik,
ugyanolyan típusú értéket. A rekurzív típusok azért jelentenek problémát, mert a
Rustnak fordítási időben tudnia kell, mennyi helyet foglal egy típus. A rekurzív
típusok értékeinek egymásba ágyazása azonban elméletileg a végtelenségig
folytatódhat, így a Rust nem tudhatja, mennyi helyre van szüksége az értéknek.
Mivel a boxoknak ismert a mérete, a rekurzív típusdefinícióba beszúrt box
lehetővé teszi a rekurzív típusokat.

Rekurzív típusra példaként nézzük meg a cons listát. Ez a funkcionális
programozási nyelvekben gyakori adattípus. A cons lista típusa, amelyet
definiálni fogunk, a rekurziót leszámítva egyszerű; ezért a példában szereplő
fogalmak bármikor hasznosak lesznek, amikor rekurzív típusokat érintő
bonyolultabb helyzetekbe kerülsz.

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### A cons lista megértése

A _cons lista_ olyan adatszerkezet, amely a Lisp programozási nyelvből és annak
dialektusaiból származik, egymásba ágyazott párokból épül fel, és a láncolt lista
Lisp-beli megfelelője. A nevét a Lisp `cons` függvényéről kapta (a _construct
function_ rövidítése), amely két argumentumából egy új párt hoz létre. Ha a
`cons`-t egy olyan páron hívjuk meg, amely egy értékből és egy másik párból áll,
rekurzív párokból felépülő cons listákat állíthatunk össze.

Például itt van egy cons lista pszeudokódos ábrázolása, amely az `1, 2, 3`
listát tartalmazza, minden párt zárójelbe téve:

```text
(1, (2, (3, Nil)))
```

A cons lista minden eleme két részt tartalmaz: az aktuális elem és a következő
elem értékét. A lista utolsó eleme csak egy `Nil` nevű értéket tartalmaz,
következő elem nélkül. A cons lista a `cons` függvény rekurzív hívásával jön
létre. A rekurzió alapesetét jelölő bevett név a `Nil`. Ne feledd, hogy ez nem
azonos a 6. fejezetben tárgyalt „null” vagy „nil” fogalommal, amely érvénytelen
vagy hiányzó értéket jelent.

A cons lista a Rustban nem gyakran használt adatszerkezet. Ha a Rustban elemek
listájára van szükséged, a legtöbbször a `Vec<T>` a jobb választás. Más,
bonyolultabb rekurzív adattípusok _valóban_ hasznosak különféle helyzetekben, de
azzal, hogy ebben a fejezetben a cons listával kezdünk, sok elterelés nélkül
feltárhatjuk, hogyan tesznek lehetővé a boxok egy rekurzív adattípus
definiálását.

A 15-2. lista egy enum definícióját tartalmazza egy cons listához. Ne feledd,
hogy ez a kód még nem fordul le, mert a `List` típusnak nem ismert a mérete –
ezt mindjárt be is mutatjuk.

<Listing number="15-2" file-name="src/main.rs" caption="Első próbálkozás egy `i32` értékeket tartalmazó cons lista adatszerkezetet reprezentáló enum definiálására">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> Megjegyzés: ebben a példában olyan cons listát implementálunk, amely csak
> `i32` értékeket tárol. Implementálhattuk volna generikusokkal is – ahogy a 10.
> fejezetben tárgyaltuk –, hogy olyan cons lista típust definiáljunk, amely
> bármilyen típusú értéket tárolni tud.

Ha a `List` típust használnánk az `1, 2, 3` lista tárolására, az a 15-3. lista
kódjához hasonlóan nézne ki.

<Listing number="15-3" file-name="src/main.rs" caption="A `List` enum használata az `1, 2, 3` lista tárolására">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

Az első `Cons` érték az `1`-et és egy másik `List` értéket tartalmaz. Ez a `List`
érték egy újabb `Cons` érték, amely a `2`-t és egy másik `List` értéket
tartalmaz. Ez a `List` érték még egy `Cons` érték, amely a `3`-at és egy `List`
értéket tartalmaz, amely végül `Nil`, vagyis az a nem rekurzív variáns, amely a
lista végét jelzi.

Ha megpróbáljuk lefordítani a 15-3. lista kódját, a 15-4. listában látható hibát
kapjuk.

<Listing number="15-4" caption="A hiba, amelyet egy rekurzív enum definiálásának megkísérlésekor kapunk">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

A hiba szerint ez a típus „végtelen méretű”. Ennek az az oka, hogy a `List`-et
egy olyan varianssal definiáltuk, amely rekurzív: közvetlenül önmagának egy
másik értékét tartalmazza. Ennek eredményeként a Rust nem tudja kitalálni,
mennyi helyre van szüksége egy `List` érték tárolásához. Bontsuk elemeire, miért
kapjuk ezt a hibát. Először nézzük meg, hogyan dönti el a Rust, mennyi helyre van
szüksége egy nem rekurzív típusú érték tárolásához.

#### Nem rekurzív típus méretének kiszámítása

Emlékezz vissza a `Message` enumra, amelyet a 6-2. listában definiáltunk, amikor
a 6. fejezetben az enumdefiníciókról volt szó:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Annak eldöntéséhez, mennyi helyet foglaljon le egy `Message` értéknek, a Rust
végigmegy az egyes variánsokon, hogy lássa, melyik variánsnak van szüksége a
legtöbb helyre. A Rust látja, hogy a `Message::Quit`-nak egyáltalán nincs
szüksége helyre, a `Message::Move`-nak elegendő hely kell két `i32` érték
tárolásához, és így tovább. Mivel egyszerre csak egy variánst használunk, egy
`Message` érték legfeljebb annyi helyet igényel, amennyit a legnagyobb variánsa
tárolása elfoglalna.

Ezzel szemben nézzük meg, mi történik, amikor a Rust megpróbálja meghatározni,
mennyi helyre van szüksége egy olyan rekurzív típusnak, mint a `List` enum a
15-2. listában. A fordító azzal kezdi, hogy megnézi a `Cons` variánst, amely egy
`i32` és egy `List` típusú értéket tartalmaz. Ezért a `Cons`-nak annyi helyre van
szüksége, amennyi egy `i32` mérete plusz egy `List` mérete. Annak
kiderítéséhez, mennyi memóriát igényel a `List` típus, a fordító megnézi a
variánsokat, kezdve a `Cons` varianssal. A `Cons` variáns egy `i32` és egy `List`
típusú értéket tartalmaz, és ez a folyamat a végtelenségig folytatódik, ahogy azt
a 15-1. ábra mutatja.

<img alt="Egy végtelen Cons lista: egy „Cons” feliratú téglalap két kisebb téglalapra osztva. Az első kisebb téglalapban az „i32” felirat áll, a második kisebb téglalapban pedig a „Cons” felirat és a külső „Cons” téglalap egy kisebb változata. A „Cons” téglalapok egyre kisebb és kisebb változatokat tartalmaznak önmagukból, egészen addig, amíg a legkisebb, még kényelmesen látható téglalapban egy végtelenjel áll, jelezve, hogy ez az ismétlődés örökké folytatódik." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">15-1. ábra: Egy végtelen `List`, amely végtelen sok `Cons`
variánsból áll</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### Ismert méretű rekurzív típus létrehozása

Mivel a Rust nem tudja kitalálni, mennyi helyet foglaljon le a rekurzívan
definiált típusoknak, a fordító hibát ad ezzel a hasznos javaslattal:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

Ebben a javaslatban az _indirekció_ azt jelenti, hogy ahelyett, hogy az értéket
közvetlenül tárolnánk, változtassuk meg az adatszerkezetet úgy, hogy közvetetten
tárolja az értéket: az érték helyett egy rá mutató pointert tároljon.

Mivel a `Box<T>` egy pointer, a Rust mindig tudja, mennyi helyre van szüksége egy
`Box<T>`-nek: egy pointer mérete nem változik attól függően, mennyi adatra mutat.
Ez azt jelenti, hogy a `Cons` variánsba egy `Box<T>`-t tehetünk közvetlenül egy
másik `List` érték helyett. A `Box<T>` a következő `List` értékre fog mutatni,
amely a heapen lesz, nem pedig a `Cons` variánson belül. Fogalmilag még mindig
egy listánk van, amelyet más listákat tartalmazó listákból hoztunk létre, de ez
az implementáció most már inkább arra hasonlít, mintha az elemeket egymás mellé,
nem pedig egymásba helyeznénk.

A 15-2. listában szereplő `List` enum definícióját és a `List` 15-3. listabeli
használatát a 15-5. lista kódjára módosíthatjuk, amely már le fog fordulni.

<Listing number="15-5" file-name="src/main.rs" caption="A `List` definíciója, amely a `Box<T>`-t használja az ismert méret érdekében">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

A `Cons` variánsnak egy `i32` méretére, plusz a box pointeradatának tárolásához
szükséges helyre van szüksége. A `Nil` variáns nem tárol értéket, ezért kevesebb
helyet igényel a stacken, mint a `Cons` variáns. Most már tudjuk, hogy bármely
`List` érték egy `i32` méretét plusz egy box pointeradatának méretét foglalja el.
A box használatával megtörtük a végtelen, rekurzív láncot, így a fordító ki tudja
számítani, mekkora helyre van szüksége egy `List` érték tárolásához. A 15-2. ábra
mutatja, hogyan néz ki most a `Cons` variáns.

<img alt="Egy „Cons” feliratú téglalap két kisebb téglalapra osztva. Az első kisebb téglalapban az „i32” felirat áll, a második kisebb téglalapban pedig a „Box” felirat, benne egy belső téglalappal, amelyben az „usize” felirat áll, ami a box pointerének véges méretét jelképezi." src="img/trpl15-02.svg" class="center" />

<span class="caption">15-2. ábra: Egy `List`, amely nem végtelen méretű, mert a
`Cons` egy `Box`-ot tartalmaz</span>

A boxok csak az indirekciót és a heapen való lefoglalást biztosítják; nincs
semmilyen más különleges képességük, mint amilyeneket a többi smart pointer
típusnál látni fogunk. Ugyanakkor a teljesítménybeli többletköltségük sincs meg,
amellyel ezek a különleges képességek járnak, így hasznosak lehetnek olyan
esetekben, mint a cons lista, ahol az indirekció az egyetlen szükséges képesség.
A boxok további felhasználási eseteit a 18. fejezetben nézzük meg.

A `Box<T>` típus azért smart pointer, mert implementálja a `Deref` trait-et,
amely lehetővé teszi, hogy a `Box<T>` értékeket referenciaként kezeljük. Amikor
egy `Box<T>` érték kilép a hatóköréből, a `Drop` trait implementációja miatt a
heapen lévő adat is felszabadul, amelyre a box mutat. Ez a két trait még
fontosabb lesz a többi smart pointer típus által nyújtott funkcionalitásban,
amelyekről a fejezet hátralévő részében lesz szó. Nézzük meg részletesebben ezt a
két trait-et.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
