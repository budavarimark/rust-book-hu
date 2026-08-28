## A referenciaciklusok memóriaszivárgást okozhatnak

A Rust memóriabiztonsági garanciái megnehezítik – de nem teszik lehetetlenné –,
hogy véletlenül soha meg nem tisztított memóriát hozz létre (ezt nevezzük
_memóriaszivárgásnak_). A memóriaszivárgás teljes megakadályozása nem tartozik
a Rust garanciái közé, vagyis a memóriaszivárgás Rustban memóriabiztonságos.
Azt, hogy a Rust megengedi a memóriaszivárgást, az `Rc<T>` és a `RefCell<T>`
használatával láthatjuk: lehetséges olyan referenciákat létrehozni, amelyekben
az elemek körkörösen hivatkoznak egymásra. Ez memóriaszivárgást okoz, mert a
ciklusban lévő elemek referenciaszámlálója soha nem éri el a 0-t, és az értékek
soha nem semmisülnek meg.

### Referenciaciklus létrehozása

Nézzük meg, hogyan alakulhat ki referenciaciklus, és hogyan előzhető meg;
kezdjük a `List` enum és egy `tail` metódus definíciójával a 15-25. listában.

<Listing number="15-25" file-name="src/main.rs" caption="Egy cons list definíció, amely `RefCell<T>`-t tárol, hogy módosítani tudjuk, mire hivatkozik egy `Cons` variáns">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

A 15-5. listában szereplő `List` definíció egy újabb változatát használjuk. A
`Cons` variáns második eleme mostantól `RefCell<Rc<List>>`, ami azt jelenti,
hogy ahelyett, hogy az `i32` értéket tudnánk módosítani, ahogy a 15-24. listában
tettük, azt a `List` értéket akarjuk módosítani, amelyre egy `Cons` variáns
mutat. Hozzáadunk egy `tail` metódust is, hogy kényelmesen elérhessük a második
elemet, ha van egy `Cons` variánsunk.

A 15-26. listában hozzáadunk egy `main` függvényt, amely a 15-25. lista
definícióit használja. Ez a kód létrehoz egy listát `a`-ban, és egy listát
`b`-ben, amely az `a`-ban lévő listára mutat. Ezután módosítja az `a`-ban lévő
listát, hogy `b`-re mutasson, ezzel referenciaciklust hozva létre. Útközben
`println!` utasítások mutatják, hogy a folyamat különböző pontjain mennyi a
referenciaszámláló értéke.

<Listing number="15-26" file-name="src/main.rs" caption="Két, egymásra mutató `List` értékből álló referenciaciklus létrehozása">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Létrehozunk egy `Rc<List>` példányt, amely egy `List` értéket tárol az `a`
változóban, kezdetben az `5, Nil` listával. Ezután létrehozunk egy `Rc<List>`
példányt, amely egy másik `List` értéket tárol a `b` változóban; ez a `10`
értéket tartalmazza, és az `a`-ban lévő listára mutat.

Módosítjuk `a`-t úgy, hogy a `Nil` helyett `b`-re mutasson, ezzel ciklust
hozunk létre. Ezt úgy tesszük meg, hogy a `tail` metódussal referenciát kérünk
az `a`-ban lévő `RefCell<Rc<List>>`-re, amelyet a `link` változóba teszünk.
Ezután a `RefCell<Rc<List>>` `borrow_mut` metódusával megváltoztatjuk a benne
lévő értéket: a `Nil` értéket tároló `Rc<List>` helyett a `b`-ben lévő
`Rc<List>`-re.

Ha lefuttatjuk ezt a kódot, egyelőre kikommentezve hagyva az utolsó
`println!`-t, ezt a kimenetet kapjuk:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

Az `a`-ban és a `b`-ben lévő `Rc<List>` példányok referenciaszámlálója egyaránt
2, miután az `a`-ban lévő listát úgy változtattuk meg, hogy `b`-re mutasson. A
`main` végén a Rust megsemmisíti a `b` változót, ami a `b`-beli `Rc<List>`
példány referenciaszámlálóját 2-ről 1-re csökkenti. Az a memória, amelyet az
`Rc<List>` a heapen foglal, ezen a ponton nem szabadul fel, mert a
referenciaszámlálója 1, nem 0. Ezután a Rust megsemmisíti `a`-t, ami az
`a`-beli `Rc<List>` példány referenciaszámlálóját szintén 2-ről 1-re csökkenti.
Ennek a példánynak a memóriája sem szabadulhat fel, mert a másik `Rc<List>`
példány továbbra is hivatkozik rá. A listának lefoglalt memória örökre
felszabadítatlan marad. Hogy szemléltessük ezt a referenciaciklust,
elkészítettük a 15-4. ábrát.

<img alt="Egy 'a' címkéjű téglalap, amely egy 5 egész számot tartalmazó téglalapra mutat. Egy 'b' címkéjű téglalap, amely egy 10 egész számot tartalmazó téglalapra mutat. Az 5-öt tartalmazó téglalap a 10-et tartalmazó téglalapra mutat, a 10-et tartalmazó téglalap pedig vissza az 5-öt tartalmazó téglalapra, így ciklus jön létre." src="img/trpl15-04.svg" class="center" />

<span class="caption">15-4. ábra: Az egymásra mutató `a` és `b` listákból álló
referenciaciklus</span>

Ha kikommentezed az utolsó `println!`-t, és lefuttatod a programot, a Rust
megpróbálja kiírni ezt a ciklust, ahol `a` mutat `b`-re, az `a`-ra, és így
tovább, amíg túl nem csordul a stack.

Egy valós programhoz képest egy referenciaciklus létrehozásának a
következményei ebben a példában nem túl súlyosak: közvetlenül a
referenciaciklus létrehozása után a program véget ér. Ha azonban egy
összetettebb program sok memóriát foglalna le egy ciklusban, és azt hosszú
ideig tartaná, a program több memóriát használna a szükségesnél, és
túlterhelhetné a rendszert, kifogyasztva azt az elérhető memóriából.

Referenciaciklusokat nem könnyű létrehozni, de nem is lehetetlen. Ha vannak
olyan `RefCell<T>` értékeid, amelyek `Rc<T>` értékeket tartalmaznak, vagy
hasonló, egymásba ágyazott, interior mutabilityt és referenciaszámlálást
használó típuskombinációid, neked kell gondoskodnod arról, hogy ne hozz létre
ciklusokat; nem támaszkodhatsz arra, hogy a Rust majd elkapja őket. Egy
referenciaciklus létrehozása logikai hiba lenne a programodban, amelyet
automatizált tesztekkel, kódellenőrzésekkel és más szoftverfejlesztési
gyakorlatokkal érdemes minimalizálni.

A referenciaciklusok elkerülésének egy másik megoldása az adatszerkezeteid
átszervezése úgy, hogy egyes referenciák ownership-et fejezzenek ki, mások pedig
ne. Ennek eredményeként lehetnek olyan ciklusaid, amelyek részben
ownership-kapcsolatokból, részben nem ownership jellegű kapcsolatokból állnak,
és csak az ownership-kapcsolatok befolyásolják, hogy egy érték
megsemmisíthető-e. A 15-25. listában mindig azt akarjuk, hogy a `Cons` variánsok
birtokolják a listájukat, ezért az adatszerkezet átszervezése nem lehetséges.
Nézzünk meg egy példát szülő- és gyerekcsomópontokból álló gráfokkal, hogy
lássuk, mikor alkalmas megoldás a nem ownership jellegű kapcsolat a
referenciaciklusok megelőzésére.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### Referenciaciklusok megelőzése `Weak<T>` használatával

Eddig azt mutattuk be, hogy az `Rc::clone` hívása növeli egy `Rc<T>` példány
`strong_count`-ját, és hogy egy `Rc<T>` példány csak akkor tisztul meg, ha a
`strong_count`-ja 0. Létrehozhatsz gyenge (weak) referenciát is egy `Rc<T>`
példányon belüli értékre, ha meghívod az `Rc::downgrade`-et, és átadsz neki egy
referenciát az `Rc<T>`-re. Az *erős referenciákkal* tudod megosztani egy `Rc<T>`
példány ownership-jét. A *gyenge referenciák* nem fejeznek ki
ownership-kapcsolatot, és a számuk nem befolyásolja, mikor tisztul meg egy
`Rc<T>` példány. Nem okoznak referenciaciklust, mert minden olyan ciklus,
amelyben gyenge referenciák is szerepelnek, megszakad, amint az érintett értékek
erős referenciaszámlálója 0 lesz.

Amikor meghívod az `Rc::downgrade`-et, egy `Weak<T>` típusú smart pointert
kapsz. Az `Rc::downgrade` hívása nem az `Rc<T>` példány `strong_count`-ját
növeli 1-gyel, hanem a `weak_count`-ot. Az `Rc<T>` típus a `weak_count`
segítségével tartja nyilván, hány `Weak<T>` referencia létezik, hasonlóan a
`strong_count`-hoz. A különbség az, hogy a `weak_count`-nak nem kell 0-nak
lennie ahhoz, hogy az `Rc<T>` példány megtisztuljon.

Mivel az az érték, amelyre a `Weak<T>` hivatkozik, lehet, hogy már megsemmisült,
ahhoz, hogy bármit kezdj azzal az értékkel, amelyre egy `Weak<T>` mutat, meg
kell bizonyosodnod arról, hogy az érték még létezik. Ezt úgy teheted meg, hogy
meghívod az `upgrade` metódust egy `Weak<T>` példányon, amely egy
`Option<Rc<T>>`-t ad vissza. `Some` eredményt kapsz, ha az `Rc<T>` érték még nem
semmisült meg, és `None` eredményt, ha az `Rc<T>` érték már megsemmisült. Mivel
az `upgrade` egy `Option<Rc<T>>`-t ad vissza, a Rust gondoskodik arról, hogy
mind a `Some`, mind a `None` esetet kezeld, így nem lesz érvénytelen pointer.

Példaként ahelyett, hogy olyan listát használnánk, amelynek az elemei csak a
következő elemről tudnak, olyan fát hozunk létre, amelynek az elemei ismerik a
gyerekelemeiket _és_ a szülőelemüket is.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### Fa adatszerkezet létrehozása

Először olyan fát építünk, amelynek a csomópontjai ismerik a
gyerekcsomópontjaikat. Létrehozunk egy `Node` nevű structot, amely a saját `i32`
értékét, valamint a gyerek `Node` értékeire mutató referenciákat tárolja:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Azt akarjuk, hogy egy `Node` birtokolja a gyerekeit, és ezt az ownership-et
változókkal is meg akarjuk osztani, hogy a fa minden `Node`-jához közvetlenül
hozzáférhessünk. Ehhez a `Vec<T>` elemeit `Rc<Node>` típusú értékeknek
definiáljuk. Azt is módosítani akarjuk, hogy mely csomópontok gyerekei egy másik
csomópontnak, ezért a `children` mezőben egy `RefCell<T>` van a
`Vec<Rc<Node>>` körül.

Ezután a struct definíciónkat használva létrehozunk egy `leaf` nevű `Node`
példányt a `3` értékkel és gyerekek nélkül, valamint egy másik, `branch` nevű
példányt az `5` értékkel, amelynek `leaf` az egyik gyereke – ahogy azt a 15-27.
lista mutatja.

<Listing number="15-27" file-name="src/main.rs" caption="Egy gyerekek nélküli `leaf` csomópont és egy `branch` csomópont létrehozása, amelynek `leaf` az egyik gyereke">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Klónozzuk a `leaf`-ben lévő `Rc<Node>`-ot, és eltároljuk a `branch`-ben, ami azt
jelenti, hogy a `leaf`-ben lévő `Node`-nak most két ownere van: `leaf` és
`branch`. A `branch`-től eljuthatunk a `leaf`-hez a `branch.children`
segítségével, de a `leaf`-től nem juthatunk el a `branch`-hez. Ennek az az oka,
hogy a `leaf`-nek nincs referenciája a `branch`-re, és nem tud arról, hogy
kapcsolatban állnak. Azt szeretnénk, hogy a `leaf` tudja, hogy a `branch` a
szülője. Ezt tesszük meg a következőkben.

#### Referencia hozzáadása a gyerektől a szülőjéhez

Ahhoz, hogy a gyerekcsomópont tudjon a szülőjéről, hozzá kell adnunk egy
`parent` mezőt a `Node` struct definíciójához. A gond az, hogy el kell
döntenünk, mi legyen a `parent` típusa. Tudjuk, hogy nem tartalmazhat `Rc<T>`-t,
mert az referenciaciklust hozna létre, ahol a `leaf.parent` a `branch`-re, a
`branch.children` pedig a `leaf`-re mutatna, aminek következtében a
`strong_count` értékük soha nem lenne 0.

Ha másképp gondolunk a kapcsolatokra: egy szülőcsomópontnak birtokolnia kell a
gyerekeit – ha egy szülőcsomópont megsemmisül, a gyerekcsomópontjainak is meg
kell semmisülniük. Egy gyereknek viszont nem szabad birtokolnia a szülőjét: ha
megsemmisítünk egy gyerekcsomópontot, a szülőnek továbbra is léteznie kell. Ez
a gyenge referenciák esete!

Így az `Rc<T>` helyett a `parent` típusa `Weak<T>`-t fog használni, pontosabban
`RefCell<Weak<Node>>`-ot. A `Node` struct definíciónk mostantól így néz ki:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Egy csomópont képes lesz hivatkozni a szülőcsomópontjára, de nem birtokolja a
szülőjét. A 15-28. listában frissítjük a `main`-t, hogy ezt az új definíciót
használja, így a `leaf` csomópontnak lesz módja hivatkozni a szülőjére, a
`branch`-re.

<Listing number="15-28" file-name="src/main.rs" caption="Egy `leaf` csomópont, amelynek gyenge referenciája van a szülőcsomópontjára, a `branch`-re">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

A `leaf` csomópont létrehozása hasonlóan néz ki, mint a 15-27. listában, a
`parent` mező kivételével: a `leaf` szülő nélkül indul, ezért egy új, üres
`Weak<Node>` referenciapéldányt hozunk létre.

Ezen a ponton, amikor az `upgrade` metódussal próbálunk referenciát szerezni a
`leaf` szülőjére, `None` értéket kapunk. Ezt látjuk az első `println!` utasítás
kimenetében:

```text
leaf parent = None
```

Amikor létrehozzuk a `branch` csomópontot, annak is új `Weak<Node>` referenciája
lesz a `parent` mezőben, mert a `branch`-nek nincs szülőcsomópontja. A `leaf`
továbbra is a `branch` egyik gyereke. Miután megvan a `branch`-ben lévő `Node`
példány, módosíthatjuk a `leaf`-et, hogy `Weak<Node>` referenciát adjunk neki a
szülőjére. A `leaf` `parent` mezőjében lévő `RefCell<Weak<Node>>`-on meghívjuk a
`borrow_mut` metódust, majd az `Rc::downgrade` függvénnyel `Weak<Node>`
referenciát hozunk létre a `branch`-re a `branch`-ben lévő `Rc<Node>`-ból.

Amikor újra kiírjuk a `leaf` szülőjét, ezúttal egy `branch`-et tároló `Some`
variánst kapunk: a `leaf` mostantól hozzáfér a szülőjéhez! Amikor kiírjuk a
`leaf`-et, azt a ciklust is elkerüljük, amely a 15-26. listában végül stack
overflowhoz vezetett; a `Weak<Node>` referenciák `(Weak)` alakban jelennek meg:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

A végtelen kimenet hiánya azt jelzi, hogy ez a kód nem hozott létre
referenciaciklust. Ezt abból is megállapíthatjuk, ha megnézzük az
`Rc::strong_count` és az `Rc::weak_count` hívásától kapott értékeket.

#### A `strong_count` és a `weak_count` változásainak szemléltetése

Nézzük meg, hogyan változik az `Rc<Node>` példányok `strong_count` és
`weak_count` értéke: ehhez létrehozunk egy új belső hatókört, és abba helyezzük
át a `branch` létrehozását. Így láthatjuk, mi történik, amikor a `branch`
létrejön, majd megsemmisül, amint kilép a hatóköréből. A módosításokat a 15-29.
lista mutatja.

<Listing number="15-29" file-name="src/main.rs" caption="A `branch` létrehozása egy belső hatókörben, valamint az erős és gyenge referenciaszámlálók vizsgálata">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Miután a `leaf` létrejött, az `Rc<Node>`-jának erős számlálója 1, gyenge
számlálója 0. A belső hatókörben létrehozzuk a `branch`-et, és összekapcsoljuk a
`leaf`-fel; ezen a ponton, amikor kiírjuk a számlálókat, a `branch`-ben lévő
`Rc<Node>` erős számlálója 1, gyenge számlálója pedig 1 lesz (mert a
`leaf.parent` egy `Weak<Node>`-dal a `branch`-re mutat). Amikor a `leaf`
számlálóit írjuk ki, látni fogjuk, hogy az erős számlálója 2, mert a `branch`
mostantól a `leaf` `Rc<Node>`-jának egy klónját tárolja a `branch.children`-ben,
a gyenge számlálója viszont továbbra is 0.

Amikor a belső hatókör véget ér, a `branch` kilép a hatóköréből, és az
`Rc<Node>` erős számlálója 0-ra csökken, így a `Node`-ja megsemmisül. A
`leaf.parent`-től származó 1-es gyenge számláló nem befolyásolja, hogy a `Node`
megsemmisül-e, így nem keletkezik memóriaszivárgás!

Ha a hatókör vége után próbáljuk elérni a `leaf` szülőjét, ismét `None`-t
kapunk. A program végén a `leaf`-ben lévő `Rc<Node>` erős számlálója 1, gyenge
számlálója 0, mert a `leaf` változó megint az egyetlen referencia az
`Rc<Node>`-ra.

A számlálókat és az értékek megsemmisítését kezelő teljes logika be van építve
az `Rc<T>`-be és a `Weak<T>`-be, valamint a `Drop` trait implementációikba.
Azzal, hogy a `Node` definíciójában a gyerektől a szülőhöz vezető kapcsolatot
`Weak<T>` referenciának adod meg, elérheted, hogy a szülőcsomópontok a
gyerekcsomópontokra mutassanak és fordítva, anélkül hogy referenciaciklus és
memóriaszivárgás jönne létre.

## Összefoglalás

Ez a fejezet arról szólt, hogyan használhatók a smart pointerek arra, hogy más
garanciákat és kompromisszumokat adjanak, mint amilyeneket a Rust
alapértelmezés szerint a közönséges referenciákkal biztosít. A `Box<T>` típus
ismert méretű, és a heapen lefoglalt adatokra mutat. Az `Rc<T>` típus
nyilvántartja, hány referencia mutat a heapen lévő adatokra, így az adatoknak
több ownere is lehet. A `RefCell<T>` típus az interior mutabilityjével olyan
típust ad a kezünkbe, amelyet akkor használhatunk, amikor nem módosítható
típusra van szükségünk, de a típus egy belső értékét meg kell változtatnunk;
emellett a borrowing-szabályokat futásidőben érvényesíti fordítási idő helyett.

Szó volt a `Deref` és a `Drop` trait-ekről is, amelyek a smart pointerek
funkcionalitásának nagy részét lehetővé teszik. Megvizsgáltuk a
memóriaszivárgást okozó referenciaciklusokat, és azt, hogyan előzhetők meg a
`Weak<T>` segítségével.

Ha ez a fejezet felkeltette az érdeklődésedet, és saját smart pointereket
szeretnél implementálni, nézd meg a [„The Rustonomicon”][nomicon] című művet
további hasznos információkért.

Ezután a Rust konkurenciájáról lesz szó. Néhány új smart pointert is meg fogsz
ismerni.

[nomicon]: ../nomicon/index.html
