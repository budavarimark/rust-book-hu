## `RefCell<T>` és az interior mutability minta

Az _interior mutability_ olyan Rust tervezési minta, amely lehetővé teszi az
adatok módosítását még akkor is, ha nem módosítható referenciák mutatnak rájuk;
ezt a műveletet a borrowing-szabályok normál esetben nem engedik meg. Az adatok
módosításához a minta `unsafe` kódot használ egy adatszerkezeten belül, hogy
kicselezze a Rust szokásos, a módosítást és a borrowingot szabályozó
előírásait. Az unsafe kód azt jelzi a fordítónak, hogy a szabályokat kézzel
ellenőrizzük ahelyett, hogy a fordítóra bíznánk; az unsafe kódról bővebben a
20. fejezetben lesz szó.

Az interior mutability mintát használó típusokat csak akkor használhatjuk, ha
biztosítani tudjuk, hogy a borrowing-szabályok futásidőben teljesülni fognak,
még ha a fordító ezt nem is tudja garantálni. Az érintett `unsafe` kód ilyenkor
biztonságos API-ba van becsomagolva, a külső típus pedig továbbra sem
módosítható.

Járjuk körbe ezt a fogalmat a `RefCell<T>` típuson keresztül, amely az interior
mutability mintát követi.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### A borrowing-szabályok érvényesítése futásidőben

Az `Rc<T>`-vel ellentétben a `RefCell<T>` típus egyedüli ownershipet képvisel
az általa tárolt adatok felett. Mitől más akkor a `RefCell<T>`, mint mondjuk egy
`Box<T>`? Idézzük fel a borrowing-szabályokat a 4. fejezetből:

- Egy adott időpontban _vagy_ egy módosítható referenciád lehet, _vagy_
  tetszőleges számú nem módosítható referenciád (de nem mindkettő).
- A referenciáknak mindig érvényesnek kell lenniük.

Referenciák és `Box<T>` esetén a borrowing-szabályok invariánsai fordítási
időben érvényesülnek. `RefCell<T>` esetén ezek az invariánsok _futásidőben_
érvényesülnek. Referenciáknál, ha megszeged ezeket a szabályokat, fordítási
hibát kapsz. `RefCell<T>`-nél, ha megszeged ezeket a szabályokat, a programod
panicot vált ki és kilép.

A borrowing-szabályok fordítási idejű ellenőrzésének az az előnye, hogy a hibák
korábban derülnek ki a fejlesztés során, és nincs hatás a futásidejű
teljesítményre, mert minden elemzés előre lefut. Ezen okokból az esetek
többségében a borrowing-szabályok fordítási idejű ellenőrzése a legjobb
választás – ezért is ez a Rust alapértelmezése.

Annak viszont, hogy a borrowing-szabályokat inkább futásidőben ellenőrizzük, az
az előnye, hogy bizonyos memóriabiztonságos helyzetek megengedetté válnak,
amelyeket a fordítási idejű ellenőrzések tiltottak volna. A statikus elemzés –
amilyen a Rust fordítója is – természeténél fogva óvatos. A kód egyes
tulajdonságai a kód elemzésével felderíthetetlenek: a leghíresebb példa erre a
megállási probléma (Halting Problem), amely túlmutat e könyv keretein, de
érdekes téma utánaolvasni.

Mivel bizonyos elemzések lehetetlenek, ha a Rust fordítója nem tud
megbizonyosodni arról, hogy a kód megfelel az ownership-szabályoknak, akár egy
helyes programot is elutasíthat; ebben az értelemben óvatos. Ha a Rust
elfogadna egy helytelen programot, a felhasználók nem bízhatnának a Rust
garanciáiban. Ha viszont a Rust elutasít egy helyes programot, az a
programozónak kényelmetlen, de semmi katasztrofális nem történik. A `RefCell<T>`
típus akkor hasznos, amikor biztos vagy benne, hogy a kódod betartja a
borrowing-szabályokat, de a fordító ezt nem tudja megérteni és garantálni.

Az `Rc<T>`-hez hasonlóan a `RefCell<T>` is csak egyszálú helyzetekben
használható, és fordítási idejű hibát ad, ha többszálú környezetben próbálod
használni. A 16. fejezetben lesz szó arról, hogyan érhetjük el a `RefCell<T>`
funkcionalitását többszálú programban.

Íme egy összefoglaló arról, mikor melyiket érdemes választani a `Box<T>`, az
`Rc<T>` és a `RefCell<T>` közül:

- Az `Rc<T>` lehetővé teszi, hogy ugyanannak az adatnak több ownere legyen; a
  `Box<T>`-nek és a `RefCell<T>`-nek egyetlen ownere van.
- A `Box<T>` fordítási időben ellenőrzött nem módosítható vagy módosítható
  borrowokat enged meg; az `Rc<T>` csak fordítási időben ellenőrzött nem
  módosítható borrowokat enged meg; a `RefCell<T>` futásidőben ellenőrzött nem
  módosítható vagy módosítható borrowokat enged meg.
- Mivel a `RefCell<T>` futásidőben ellenőrzött módosítható borrowokat enged meg,
  a `RefCell<T>`-n belüli értéket akkor is módosíthatod, ha maga a `RefCell<T>`
  nem módosítható.

Az interior mutability minta lényege az, hogy egy nem módosítható értéken belüli
értéket módosítunk. Nézzünk meg egy helyzetet, amelyben az interior mutability
hasznos, és vizsgáljuk meg, hogyan lehetséges ez.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Az interior mutability használata

A borrowing-szabályok egyik következménye, hogy ha van egy nem módosítható
értéked, azt nem borrow-olhatod módosíthatóként. Ez a kód például nem fordul le:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Ha megpróbálnád lefordítani ezt a kódot, a következő hibát kapnád:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Vannak azonban helyzetek, amikor hasznos lenne, ha egy érték a saját metódusain
belül módosítaná önmagát, kifelé, a többi kód felé viszont nem módosíthatónak
látszana. Az érték metódusain kívüli kód nem tudná módosítani az értéket. A
`RefCell<T>` használata az egyik módja annak, hogy interior mutabilityt
kapjunk, de a `RefCell<T>` nem kerüli meg teljesen a borrowing-szabályokat: a
fordítóban lévő borrow checker megengedi ezt az interior mutabilityt, a
borrowing-szabályokat pedig futásidőben ellenőrzi a rendszer. Ha megszeged a
szabályokat, fordítási hiba helyett `panic!`-ot kapsz.

Dolgozzunk végig egy gyakorlati példát, ahol a `RefCell<T>` segítségével
módosítunk egy nem módosítható értéket, és nézzük meg, ez miért hasznos.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Tesztelés mock objektumokkal

Tesztelés közben a programozó időnként egy típus helyett egy másikat használ,
hogy megfigyeljen egy adott viselkedést, és állítást fogalmazzon meg arról, hogy
az helyesen van implementálva. Ezt a helyettesítő típust _test double_-nek
nevezzük. Gondolj rá úgy, mint a filmezésben a kaszkadőrre (stunt double), aki
beugrik a színész helyére egy különösen trükkös jelenetnél. A test double-ök más
típusok helyett állnak be, amikor teszteket futtatunk. A _mock objektumok_ a
test double-ök egy sajátos fajtája: rögzítik, mi történik a teszt során, hogy
állításokat fogalmazhass meg arról, hogy a megfelelő műveletek zajlottak-e le.

A Rustban nincsenek objektumok abban az értelemben, ahogy más nyelvekben, és a
Rust standard könyvtára sem tartalmaz beépített mock objektum funkcionalitást,
ahogy néhány más nyelv teszi. Létrehozhatsz viszont egy structot, amely
ugyanazt a célt szolgálja, mint egy mock objektum.

Íme a forgatókönyv, amelyet tesztelni fogunk: készítünk egy könyvtárat, amely
egy értéket követ nyomon egy maximális értékhez képest, és aszerint küld
üzeneteket, hogy az aktuális érték mennyire közelíti meg a maximumot. Ezt a
könyvtárat lehetne például arra használni, hogy nyomon kövessük egy felhasználó
kvótáját arra vonatkozóan, hány API-hívást tehet.

A könyvtárunk csak azt a funkcionalitást biztosítja, hogy nyomon követi, egy
érték mennyire közelíti meg a maximumot, és hogy mikor milyen üzenetnek kell
elhangoznia. Az üzenetek küldésének mechanizmusát a könyvtárunkat használó
alkalmazásoknak kell biztosítaniuk: az alkalmazás megjelenítheti az üzenetet
közvetlenül a felhasználónak, küldhet e-mailt, küldhet SMS-t, vagy tehet valami
mást. A könyvtárnak nem kell ismernie ezt a részletet. Csak annyira van
szüksége, hogy legyen valami, ami implementálja az általunk biztosított
`Messenger` trait-et. A 15-20. lista mutatja a könyvtár kódját.

<Listing number="15-20" file-name="src/lib.rs" caption="Egy könyvtár, amely nyomon követi, mennyire közelít egy érték a maximumhoz, és figyelmeztet, amikor az érték bizonyos szintekre ér">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Ennek a kódnak az egyik fontos része, hogy a `Messenger` trait-nek egyetlen,
`send` nevű metódusa van, amely egy nem módosítható referenciát vesz át a
`self`-re, valamint az üzenet szövegét. Ez a trait az az interfész, amelyet a
mock objektumunknak implementálnia kell, hogy ugyanúgy lehessen használni, mint
egy valódi objektumot. A másik fontos rész, hogy a `LimitTracker` `set_value`
metódusának viselkedését akarjuk tesztelni. Meg tudjuk változtatni, mit adunk át
a `value` paraméternek, de a `set_value` nem ad vissza semmit, amiről állítást
fogalmazhatnánk meg. Azt szeretnénk kimondani, hogy ha létrehozunk egy
`LimitTracker`-t valamivel, ami implementálja a `Messenger` trait-et, és egy
adott `max` értékkel, akkor a messenger utasítást kap a megfelelő üzenetek
elküldésére, amikor különböző számokat adunk át a `value`-nak.

Szükségünk van egy mock objektumra, amely – ahelyett, hogy e-mailt vagy SMS-t
küldene a `send` hívásakor – csak nyilvántartja azokat az üzeneteket, amelyek
elküldésére utasítást kapott. Létrehozhatjuk a mock objektum egy új példányát,
készíthetünk egy `LimitTracker`-t, amely ezt a mock objektumot használja,
meghívhatjuk a `LimitTracker` `set_value` metódusát, majd ellenőrizhetjük, hogy
a mock objektumban a várt üzenetek szerepelnek-e. A 15-21. lista egy kísérletet
mutat egy pontosan ezt csináló mock objektum implementálására, de a borrow
checker nem engedi meg.

<Listing number="15-21" file-name="src/lib.rs" caption="Kísérlet egy olyan `MockMessenger` implementálására, amelyet a borrow checker nem enged meg">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Ez a tesztkód definiál egy `MockMessenger` structot, amelynek van egy
`sent_messages` mezője `String` értékek `Vec`-jével, hogy nyilvántartsa azokat
az üzeneteket, amelyek elküldésére utasítást kapott. Definiálunk egy `new`
asszociált függvényt is, hogy kényelmesen létrehozhassunk üres üzenetlistával
induló új `MockMessenger` értékeket. Ezután implementáljuk a `Messenger`
trait-et a `MockMessenger`-re, hogy egy `MockMessenger`-t adhassunk egy
`LimitTracker`-nek. A `send` metódus definíciójában fogjuk a paraméterként
átadott üzenetet, és eltároljuk a `MockMessenger` `sent_messages` listájában.

A tesztben azt vizsgáljuk, mi történik, amikor a `LimitTracker` azt az utasítást
kapja, hogy a `value`-t a `max` érték 75 százalékánál nagyobbra állítsa.
Először létrehozunk egy új `MockMessenger`-t, amely üres üzenetlistával indul.
Ezután létrehozunk egy új `LimitTracker`-t, és átadjuk neki az új
`MockMessenger`-re mutató referenciát, valamint a `100`-as `max` értéket.
Meghívjuk a `LimitTracker` `set_value` metódusát `80`-as értékkel, ami több mint
a 100 75 százaléka. Ezután megfogalmazzuk azt az állítást, hogy a
`MockMessenger` által nyilvántartott üzenetlistában immár egy üzenetnek kell
lennie.

Ezzel a teszttel azonban van egy probléma, ahogy az alábbi mutatja:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Nem tudjuk úgy módosítani a `MockMessenger`-t, hogy nyilvántartsa az üzeneteket,
mert a `send` metódus nem módosítható referenciát vesz át a `self`-re. A
hibaüzenet javaslatát sem tudjuk követni, amely szerint `&mut self`-et
használjunk mind az `impl`-beli metódusban, mind a trait definíciójában. Nem
akarjuk pusztán a tesztelés kedvéért megváltoztatni a `Messenger` trait-et.
Ehelyett olyan megoldást kell találnunk, amellyel a tesztkódunk helyesen működik
a meglévő tervünkkel.

Ez az a helyzet, amikor az interior mutability segíthet! A `sent_messages`-t egy
`RefCell<T>`-ben tároljuk, és akkor a `send` metódus képes lesz módosítani a
`sent_messages`-t, hogy eltárolja a látott üzeneteket. A 15-22. lista mutatja,
hogyan néz ki ez.

<Listing number="15-22" file-name="src/lib.rs" caption="A `RefCell<T>` használata egy belső érték módosítására, miközben a külső érték nem módosíthatónak számít">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

A `sent_messages` mező típusa mostantól `RefCell<Vec<String>>` a `Vec<String>`
helyett. A `new` függvényben egy új `RefCell<Vec<String>>` példányt hozunk létre
az üres vektor köré.

A `send` metódus implementációjában az első paraméter továbbra is `self` nem
módosítható borrowja, ami megfelel a trait definíciójának. Meghívjuk a
`borrow_mut`-ot a `self.sent_messages`-ben lévő `RefCell<Vec<String>>`-en, hogy
módosítható referenciát kapjunk a `RefCell<Vec<String>>`-en belüli értékre,
vagyis a vektorra. Ezután meghívhatjuk a `push`-t a vektorra mutató módosítható
referencián, hogy nyilvántartsuk a teszt során elküldött üzeneteket.

Az utolsó változtatás, amit meg kell tennünk, az állításban van: hogy lássuk,
hány elem van a belső vektorban, meghívjuk a `borrow`-t a
`RefCell<Vec<String>>`-en, így nem módosítható referenciát kapunk a vektorra.

Most, hogy láttad, hogyan kell használni a `RefCell<T>`-t, nézzük meg
alaposabban, hogyan is működik!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### A borrowok nyomon követése futásidőben

Nem módosítható és módosítható referenciák létrehozásakor a `&`, illetve a
`&mut` szintaxist használjuk. A `RefCell<T>` esetén a `borrow` és a `borrow_mut`
metódusokat használjuk, amelyek a `RefCell<T>` biztonságos API-jának részei. A
`borrow` metódus a `Ref<T>` smart pointer típust adja vissza, a `borrow_mut`
pedig a `RefMut<T>` smart pointer típust. Mindkét típus implementálja a
`Deref`-et, így közönséges referenciaként kezelhetjük őket.

A `RefCell<T>` nyilvántartja, hány `Ref<T>` és `RefMut<T>` smart pointer aktív
éppen. Minden alkalommal, amikor meghívjuk a `borrow`-t, a `RefCell<T>` növeli
az aktív nem módosítható borrowok számát. Amikor egy `Ref<T>` érték kilép a
hatóköréből, a nem módosítható borrowok száma 1-gyel csökken. Akárcsak a
fordítási idejű borrowing-szabályok, a `RefCell<T>` is azt engedi meg, hogy egy
adott időpontban sok nem módosítható borrowunk vagy egy módosítható borrowunk
legyen.

Ha megpróbáljuk megszegni ezeket a szabályokat, akkor – ahelyett hogy fordítási
hibát kapnánk, mint referenciák esetén – a `RefCell<T>` implementációja
futásidőben panicot vált ki. A 15-23. lista a `send` 15-22. listabeli
implementációjának módosítását mutatja. Szándékosan próbálunk két aktív
módosítható borrowot létrehozni ugyanabban a hatókörben, hogy szemléltessük:
a `RefCell<T>` ezt futásidőben megakadályozza.

<Listing number="15-23" file-name="src/lib.rs" caption="Két módosítható referencia létrehozása ugyanabban a hatókörben, hogy lássuk, a `RefCell<T>` panicot vált ki">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Létrehozunk egy `one_borrow` nevű változót a `borrow_mut` által visszaadott
`RefMut<T>` smart pointer számára. Ezután ugyanígy létrehozunk egy másik
módosítható borrowot a `two_borrow` változóban. Ez két módosítható referenciát
jelent ugyanabban a hatókörben, ami nem megengedett. Amikor lefuttatjuk a
könyvtárunk tesztjeit, a 15-23. lista kódja hibák nélkül lefordul, de a teszt
elbukik:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Vedd észre, hogy a kód az `already borrowed: BorrowMutError` üzenettel váltott
ki panicot. Így kezeli a `RefCell<T>` a borrowing-szabályok megsértését
futásidőben.

Ha azt választjuk, hogy a borrowing-hibákat futásidőben és nem fordítási időben
kapjuk el – ahogy itt tettük –, az azt jelenti, hogy a kódod hibáit
elképzelhetően csak később, a fejlesztési folyamat egy későbbi szakaszában
találod meg: akár csak azután, hogy a kódod élesbe került. Ráadásul a kódod kis
futásidejű teljesítményveszteséget szenved amiatt, hogy a borrowokat futásidőben
és nem fordítási időben tartja nyilván. A `RefCell<T>` használata viszont
lehetővé teszi olyan mock objektum írását, amely módosíthatja önmagát, hogy
nyilvántartsa a látott üzeneteket, miközben olyan környezetben használod, ahol
csak nem módosítható értékek megengedettek. A kompromisszumok ellenére
használhatod a `RefCell<T>`-t, hogy több funkcionalitást kapj, mint amennyit a
közönséges referenciák nyújtanak.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Több owner engedélyezése módosítható adatokhoz

A `RefCell<T>` egyik gyakori felhasználási módja az, hogy `Rc<T>`-vel együtt
alkalmazzuk. Emlékezz rá, hogy az `Rc<T>` lehetővé teszi, hogy egy adatnak több
ownere legyen, de csak nem módosítható hozzáférést ad ezekhez az adatokhoz. Ha
van egy `Rc<T>`-d, amely egy `RefCell<T>`-t tárol, olyan értéket kapsz,
amelynek több ownere lehet, _és_ amelyet módosítani is tudsz!

Idézzük fel például a 15-18. lista cons list példáját, ahol `Rc<T>` segítségével
tettük lehetővé, hogy több lista osztozzon egy másik lista ownershipjén. Mivel
az `Rc<T>` csak nem módosítható értékeket tárol, a lista egyetlen értékét sem
tudjuk megváltoztatni, miután létrehoztuk őket. Vegyük hozzá a `RefCell<T>`-t,
amely képes a listákban lévő értékek megváltoztatására. A 15-24. lista mutatja,
hogy egy `RefCell<T>` `Cons`-definícióbeli használatával módosítani tudjuk az
összes listában tárolt értéket.

<Listing number="15-24" file-name="src/main.rs" caption="Az `Rc<RefCell<i32>>` használata olyan `List` létrehozására, amelyet módosítani tudunk">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Létrehozunk egy értéket, amely egy `Rc<RefCell<i32>>` példány, és eltároljuk egy
`value` nevű változóban, hogy később közvetlenül elérhessük. Ezután létrehozunk
egy `List`-et `a`-ban egy olyan `Cons` variánssal, amely a `value`-t tárolja.
Klónoznunk kell a `value`-t, hogy `a` és `value` egyaránt birtokolja a belső `5`
értéket, ahelyett hogy az ownership átkerülne a `value`-ról `a`-ra, vagy hogy
`a` borrow-olna a `value`-ból.

Az `a` listát egy `Rc<T>`-be csomagoljuk, hogy amikor létrehozzuk a `b` és `c`
listákat, mindkettő hivatkozhasson `a`-ra – ahogy azt a 15-18. listában tettük.

Miután létrehoztuk az `a`, `b` és `c` listákat, 10-et akarunk hozzáadni a
`value`-ban lévő értékhez. Ezt úgy tesszük meg, hogy meghívjuk a `borrow_mut`-ot
a `value`-n, amely az 5. fejezet
[„Hol van a `->` operátor?”][wheres-the---operator]<!-- ignore --> részében
tárgyalt automatikus dereferálást használja, hogy az `Rc<T>`-t a benne lévő
`RefCell<T>` értékre dereferálja. A `borrow_mut` metódus egy `RefMut<T>`
smart pointert ad vissza, amelyre alkalmazzuk a dereferáló operátort, és
megváltoztatjuk a belső értéket.

Amikor kiírjuk `a`-t, `b`-t és `c`-t, láthatjuk, hogy mindegyikben a módosított
`15`-ös érték szerepel az `5` helyett:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Ez a technika elég ügyes! A `RefCell<T>` használatával kifelé nem módosítható
`List` értékünk van. De használhatjuk a `RefCell<T>` azon metódusait, amelyek
hozzáférést adnak az interior mutabilityjéhez, így módosíthatjuk az adatainkat,
amikor szükséges. A borrowing-szabályok futásidejű ellenőrzései megvédenek
minket az adatversenyhelyzetektől, és az adatszerkezeteinkben néha megéri egy
kis sebességet feláldozni ezért a rugalmasságért. Vedd figyelembe, hogy a
`RefCell<T>` nem működik többszálú kódban! A `Mutex<T>` a `RefCell<T>`
szálbiztos változata, és a `Mutex<T>`-ről a 16. fejezetben lesz szó.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
