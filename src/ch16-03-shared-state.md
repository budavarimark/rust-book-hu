## Osztott állapotú konkurencia

Az üzenetküldés remek módja a konkurencia kezelésének, de nem az egyetlen. Egy
másik módszer az, ha több szál ugyanahhoz az osztott adathoz fér hozzá. Nézzük
meg újra a Go nyelv dokumentációjából származó jelmondat elejét: „Ne
memóriamegosztással kommunikálj.”

Hogyan nézne ki a memóriamegosztással való kommunikáció? És egyáltalán miért
óvnak az üzenetküldés hívei a memóriamegosztástól?

Bizonyos értelemben a csatornák bármely programozási nyelvben hasonlítanak az
egyszeres ownershipre, hiszen ha egyszer leküldtél egy értéket egy csatornán,
utána már nem szabad használnod azt az értéket. Az osztott memóriájú konkurencia
inkább a többszörös ownershiphez hasonlít: több szál is hozzáférhet ugyanahhoz a
memóriaterülethez egy időben. Ahogy a 15. fejezetben láttad, ahol a smart
pointerek tették lehetővé a többszörös ownershipet, a többszörös ownership
bonyolultságot visz a rendszerbe, mert ezeket a különböző ownereket kezelni
kell. A Rust típusrendszere és ownership-szabályai sokat segítenek abban, hogy
ez a kezelés helyes legyen. Példaként nézzük meg a mutexeket, amelyek az osztott
memória egyik legelterjedtebb konkurencia-primitívjei.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### A hozzáférés szabályozása mutexekkel

A _mutex_ a _mutual exclusion_ („kölcsönös kizárás”) rövidítése: a mutex
egyszerre csak egyetlen szálnak engedi meg, hogy hozzáférjen egy adathoz. Ahhoz,
hogy egy szál hozzáférjen a mutexben lévő adathoz, előbb jeleznie kell, hogy
hozzáférést kér, méghozzá úgy, hogy megszerzi a mutex zárját (lock). A _lock_
egy olyan adatszerkezet, amely a mutex része, és nyilvántartja, kinek van éppen
kizárólagos hozzáférése az adathoz. Ezért azt mondjuk, hogy a mutex a zárolási
rendszeren keresztül _őrzi_ az általa tárolt adatot.

A mutexeknek az a hírük, hogy nehéz őket használni, mert két szabályt kell
észben tartani:

1. Az adat használata előtt meg kell próbálnod megszerezni a lockot.
2. Amikor végeztél a mutex által őrzött adattal, fel kell oldanod a zárolást,
   hogy más szálak is megszerezhessék a lockot.

Valós példaként a mutexre képzelj el egy konferencián zajló kerekasztal-
beszélgetést egyetlen mikrofonnal. Mielőtt egy résztvevő megszólalhatna, kérnie
vagy jeleznie kell, hogy használni szeretné a mikrofont. Amikor megkapja a
mikrofont, addig beszélhet, ameddig akar, majd továbbadja a mikrofont a
következő résztvevőnek, aki szót kér. Ha egy résztvevő elfelejti továbbadni a
mikrofont, amikor végzett vele, senki más nem tud megszólalni. Ha az osztott
mikrofon kezelése félresiklik, a kerekasztal nem a tervek szerint fog működni!

A mutexek helyes kezelése rendkívül trükkös lehet, ezért lelkesednek olyan sokan
a csatornákért. A Rust típusrendszerének és ownership-szabályainak hála azonban
a zárolást és a feloldást nem tudod elrontani.

#### A `Mutex<T>` API-ja

Példaként a mutex használatára kezdjük azzal, hogy egyszálú környezetben
használunk egy mutexet, ahogy a 16-12. listában látható.

<Listing number="16-12" file-name="src/main.rs" caption="A `Mutex<T>` API-jának megismerése egyszálú környezetben, az egyszerűség kedvéért">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Sok más típushoz hasonlóan a `Mutex<T>`-t is a `new` asszociált függvénnyel
hozzuk létre. A mutexben lévő adat eléréséhez a `lock` metódussal szerezzük meg
a lockot. Ez a hívás blokkolja az aktuális szálat, így az nem tud dolgozni
addig, amíg ránk nem kerül a sor a lock birtoklásában.

A `lock` hívás akkor bukna el, ha egy másik szál, amely a lockot tartja,
panicot váltana ki. Ebben az esetben soha senki nem tudná megszerezni a lockot,
ezért úgy döntöttünk, hogy `unwrap`-et hívunk, és ilyen helyzetben ez a szál
panicot vált ki.

Miután megszereztük a lockot, a visszatérési értéket – ebben az esetben `num` a
neve – úgy kezelhetjük, mint a benne lévő adatra mutató módosítható
referenciát. A típusrendszer gondoskodik arról, hogy megszerezzük a lockot, még
mielőtt használnánk az `m`-ben lévő értéket. Az `m` típusa `Mutex<i32>`, nem
`i32`, ezért _muszáj_ meghívnunk a `lock`-ot ahhoz, hogy használhassuk az `i32`
értéket. Nem felejthetjük el; a típusrendszer másképp nem enged hozzáférni a
belső `i32`-höz.

A `lock` hívás egy `MutexGuard` nevű típussal tér vissza, egy `LockResult`-be
csomagolva, amelyet az `unwrap` hívással kezeltünk. A `MutexGuard` típus
implementálja a `Deref`-et, hogy a belső adatunkra mutasson; a típusnak van
`Drop` implementációja is, amely automatikusan elengedi a lockot, amikor a
`MutexGuard` kikerül a hatóköréből, ami a belső hatókör végén történik meg.
Ennek eredményeként nem kockáztatjuk, hogy elfelejtjük elengedni a lockot, és
ezzel megakadályozzuk, hogy más szálak használhassák a mutexet, mert a lock
elengedése automatikusan megtörténik.

A lock eldobása után kiírhatjuk a mutex értékét, és láthatjuk, hogy sikerült a
belső `i32`-t `6`-ra módosítanunk.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Osztott hozzáférés a `Mutex<T>`-hez {#shared-access-to-mutext}

Most próbáljunk meg egy értéket megosztani több szál között `Mutex<T>`
segítségével. Elindítunk 10 szálat, és mindegyikkel megnöveltetünk egy
számlálóértéket 1-gyel, hogy a számláló 0-ról 10-re jusson. A 16-13. listában
szereplő példa fordítási hibát fog adni, és ezt a hibát arra használjuk, hogy
többet tanuljunk a `Mutex<T>` használatáról, és arról, hogyan segít a Rust
abban, hogy helyesen használjuk.

<Listing number="16-13" file-name="src/main.rs" caption="Tíz szál, amelyek mindegyike növel egy `Mutex<T>` által őrzött számlálót">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Létrehozunk egy `counter` változót, amely egy `i32`-t tárol egy `Mutex<T>`-n
belül, ahogy a 16-12. listában is tettük. Ezután 10 szálat hozunk létre úgy,
hogy végigiterálunk egy számtartományon. A `thread::spawn`-t használjuk, és
minden szálnak ugyanazt a closure-t adjuk: olyat, amely bemozgatja a számlálót a
szálba, a `lock` metódus hívásával megszerzi a `Mutex<T>` lockját, majd hozzáad
1-et a mutexben lévő értékhez. Amikor egy szál befejezi a closure futtatását, a
`num` kikerül a hatóköréből, és elengedi a lockot, hogy egy másik szál
megszerezhesse.

A fő szálon összegyűjtjük az összes join handle-t. Ezután, ahogy a 16-2. listában
is, meghívjuk a `join`-t mindegyik handle-ön, hogy megbizonyosodjunk arról, hogy
minden szál befejeződött. Ezen a ponton a fő szál megszerzi a lockot, és kiírja
a program eredményét.

Utaltunk rá, hogy ez a példa nem fog lefordulni. Nézzük meg, miért!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

A hibaüzenet azt mondja, hogy a `counter` érték a ciklus előző iterációjában
átmozgatásra került. A Rust azt közli velünk, hogy nem mozgathatjuk a `counter`
lock ownershipjét több szálba. Javítsuk ki a fordítási hibát a 15. fejezetben
tárgyalt többszörös ownership módszerével.

#### Többszörös ownership több szállal

A 15. fejezetben úgy adtunk egy értéket több ownernek, hogy az `Rc<T>` smart
pointerrel referenciaszámlált értéket hoztunk létre. Tegyük ugyanezt itt is, és
nézzük meg, mi történik. A 16-14. listában becsomagoljuk a `Mutex<T>`-t egy
`Rc<T>`-be, és klónozzuk az `Rc<T>`-t, mielőtt átadnánk az ownershipet a
szálnak.

<Listing number="16-14" file-name="src/main.rs" caption="Kísérlet az `Rc<T>` használatára, hogy több szál birtokolhassa a `Mutex<T>`-t">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Fordítunk egyet, és megint... más hibákat kapunk! A fordító rengeteg mindenre
megtanít minket:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Hűha, ez a hibaüzenet nagyon bőbeszédű! Íme a fontos rész, amelyre figyelnünk
kell: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``. A fordító
azt is elárulja, miért: `` the trait `Send` is not implemented for
`Rc<Mutex<i32>>` ``. A `Send`-ről a következő szakaszban lesz szó: ez az egyik
olyan trait, amely biztosítja, hogy a szálakkal használt típusaink konkurens
helyzetekben való használatra készültek.

Sajnos az `Rc<T>` nem biztonságos szálak között megosztani. Amikor az `Rc<T>`
kezeli a referenciaszámlálót, minden `clone` híváskor növeli a számlálót, és
minden klón eldobásakor csökkenti. De semmilyen konkurencia-primitívet nem
használ annak biztosítására, hogy a számláló módosításait ne szakíthassa félbe
egy másik szál. Ez hibás számlálókhoz vezethetne – rejtett hibákhoz, amelyek
memóriaszivárgást okozhatnak, vagy azt, hogy egy értéket eldobnak, mielőtt
végeztünk volna vele. Olyan típusra van szükségünk, amely pontosan olyan, mint
az `Rc<T>`, de szálbiztos módon módosítja a referenciaszámlálót.

#### Atomi referenciaszámlálás az `Arc<T>` típussal

Szerencsére az `Arc<T>` _pont_ egy olyan típus, mint az `Rc<T>`, amelyet
biztonságosan használhatunk konkurens helyzetekben. Az _a_ az _atomic_ szót
jelöli, vagyis _atomi módon referenciaszámlált_ típusról van szó. Az atomi
műveletek a konkurencia-primitívek egy további fajtáját jelentik, amelyet itt
nem tárgyalunk részletesen: a részletekért lásd a standard könyvtár
[`std::sync::atomic`][atomic]<!-- ignore --> dokumentációját. Ezen a ponton
csak azt kell tudnod, hogy az atomi típusok úgy működnek, mint a primitív
típusok, de biztonságosan megoszthatók szálak között.

Felmerülhet benned, miért nem atomi minden primitív típus, és miért nem
implementálják a standard könyvtár típusait alapértelmezés szerint `Arc<T>`
használatával. A válasz az, hogy a szálbiztonságnak teljesítménybeli ára van,
amelyet csak akkor akarunk megfizetni, amikor tényleg szükség van rá. Ha csak
egyetlen szálon belül végzel műveleteket értékeken, a kódod gyorsabban futhat,
ha nem kell betartatnia az atomi típusok által nyújtott garanciákat.

Térjünk vissza a példánkhoz: az `Arc<T>` és az `Rc<T>` API-ja azonos, így úgy
javítjuk ki a programunkat, hogy módosítjuk a `use` sort, a `new` hívást és a
`clone` hívást. A 16-15. lista kódja végre le fog fordulni és futni fog.

<Listing number="16-15" file-name="src/main.rs" caption="Az `Arc<T>` használata a `Mutex<T>` becsomagolására, hogy több szál között megoszthassuk az ownershipet">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Ez a kód a következőt írja ki:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Sikerült! Elszámoltunk 0-tól 10-ig, ami talán nem tűnik túl lenyűgözőnek, de
sokat tanultunk közben a `Mutex<T>`-ről és a szálbiztonságról. Ennek a
programnak a szerkezetét bonyolultabb műveletekre is használhatnád, nem csak egy
számláló növelésére. Ezzel a stratégiával feloszthatsz egy számítást független
részekre, szétoszthatod ezeket a részeket a szálak között, majd egy `Mutex<T>`
segítségével minden szállal frissíttetheted a végeredményt a saját részével.

Vedd figyelembe, hogy ha egyszerű numerikus műveleteket végzel, a `Mutex<T>`-nél
egyszerűbb típusok is léteznek, amelyeket a [standard könyvtár
`std::sync::atomic` modulja][atomic]<!-- ignore --> kínál. Ezek a típusok
biztonságos, konkurens, atomi hozzáférést adnak a primitív típusokhoz. Ebben a
példában azért választottuk a `Mutex<T>`-t primitív típussal, hogy arra tudjunk
összpontosítani, hogyan működik a `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### A `RefCell<T>`/`Rc<T>` és a `Mutex<T>`/`Arc<T>` összehasonlítása

Talán feltűnt, hogy a `counter` nem módosítható, mégis kaphattunk módosítható
referenciát a benne lévő értékre; ez azt jelenti, hogy a `Mutex<T>` interior
mutabilityt nyújt, ahogy a `Cell` család is. Ugyanúgy, ahogy a 15. fejezetben a
`RefCell<T>`-t használtuk arra, hogy egy `Rc<T>` tartalmát módosíthassuk, a
`Mutex<T>`-t használjuk egy `Arc<T>` tartalmának módosítására.

Egy másik említésre méltó részlet, hogy a Rust nem véd meg mindenféle logikai
hibától, amikor `Mutex<T>`-t használsz. Emlékezz vissza a 15. fejezetre: az
`Rc<T>` használata azzal a kockázattal járt, hogy referenciaciklusokat hozunk
létre, amelyekben két `Rc<T>` érték hivatkozik egymásra, memóriaszivárgást
okozva. Hasonlóképpen a `Mutex<T>` azzal a kockázattal jár, hogy _holtpontot_
hozunk létre. Ezek akkor keletkeznek, amikor egy művelethez két erőforrást kell
zárolni, és két szál egyenként megszerezte az egyik lockot, így örökké egymásra
várnak. Ha érdekelnek a holtpontok, próbálj meg írni egy Rust programot, amely
holtpontba fut; azután nézz utána a mutexekhez kapcsolódó holtpont-elhárítási
stratégiáknak bármely nyelvben, és próbáld meg implementálni őket Rustban. A
standard könyvtár API-dokumentációja a `Mutex<T>`-ről és a `MutexGuard`-ról
hasznos információkat kínál.

Ezt a fejezetet a `Send` és `Sync` trait-ekkel zárjuk, és azzal, hogyan
használhatjuk őket saját típusokkal.

[atomic]: ../std/sync/atomic/index.html
