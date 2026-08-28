<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Egyszálúból többszálú szerver

A szerverünk jelenleg egymás után dolgozza fel a kéréseket, vagyis addig nem
kezd hozzá a második kapcsolathoz, amíg az első feldolgozása be nem fejeződött.
Ha a szerver egyre több és több kérést kapna, ez a soros végrehajtás egyre
kevésbé lenne optimális. Ha a szerver olyan kérést kap, amelynek feldolgozása
sokáig tart, a soron következő kéréseknek meg kell várniuk a hosszú kérés
befejezését, még akkor is, ha az új kérések gyorsan feldolgozhatók lennének.
Ezt ki kell javítanunk, de először nézzük meg a problémát működés közben.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Lassú kérés szimulálása

Megnézzük, hogyan hat egy lassan feldolgozódó kérés a szerverünk jelenlegi
implementációjához érkező többi kérésre. A 21-10. lista a _/sleep_ útvonalra
érkező kérés kezelését implementálja szimulált lassú válasszal, amelynek hatására
a szerver öt másodpercig alszik, mielőtt válaszolna.

<Listing number="21-10" file-name="src/main.rs" caption="Lassú kérés szimulálása öt másodperces alvással">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Az `if`-ről `match`-re váltottunk, most, hogy három esetünk van. Kifejezetten a
`request_line` egy slice-ára kell illesztenünk, hogy a sztringliterál-értékekre
tudjunk mintát illeszteni; a `match` nem végez automatikus referenciaképzést és
dereferálást, ahogy azt az egyenlőségvizsgáló metódus teszi.

Az első ág megegyezik a 21-9. lista `if` blokkjával. A második ág a _/sleep_
útvonalra érkező kérésre illeszkedik. Amikor ilyen kérés érkezik, a szerver öt
másodpercig alszik, mielőtt megjelenítené a sikeres HTML-oldalt. A harmadik ág
megegyezik a 21-9. lista `else` blokkjával.

Jól látszik, mennyire kezdetleges a szerverünk: a valódi könyvtárak sokkal
kevésbé körülményesen kezelnék több kérés felismerését!

Indítsd el a szervert a `cargo run` paranccsal. Ezután nyiss két
böngészőablakot: az egyikben a _http://127.0.0.1:7878_, a másikban a
_http://127.0.0.1:7878/sleep_ címet. Ha néhányszor beírod a _/_ URI-t, mint
korábban, azt látod, hogy gyorsan válaszol. Ha viszont beírod a _/sleep_
címet, majd betöltöd a _/_ címet, azt fogod látni, hogy a _/_ megvárja, amíg a
`sleep` letölti a teljes öt másodpercét, és csak utána töltődik be.

Több technikával is elkerülhetnénk, hogy a kérések feltorlódjanak egy lassú
kérés mögött, például az asynckel, ahogy azt a 17. fejezetben tettük; mi most
egy thread poolt fogunk implementálni.

### Az átbocsátóképesség javítása thread poollal

A _thread pool_ előre elindított szálak csoportja, amelyek készen állnak és
várnak egy feladat kezelésére. Amikor a program új feladatot kap, a poolban
lévő szálak egyikét rendeli a feladathoz, és az a szál dolgozza fel a feladatot.
A pool többi szála rendelkezésre áll bármely más feladat kezelésére, amely
azalatt érkezik, amíg az első szál dolgozik. Amikor az első szál végzett a
feladatával, visszakerül a tétlen szálak pooljába, készen egy új feladatra. A
thread pool lehetővé teszi a kapcsolatok konkurens feldolgozását, ami növeli a
szervered átbocsátóképességét.

A poolban lévő szálak számát kis értékre korlátozzuk, hogy védve legyünk a
DoS-támadásoktól; ha a programunk minden beérkező kéréshez új szálat hozna
létre, valaki tízmillió kéréssel a szerverünkhöz komoly kárt okozhatna azzal,
hogy elhasználja a szerverünk összes erőforrását, és megakasztja a kérések
feldolgozását.

Korlátlan számú szál indítása helyett tehát fix számú szál fog várakozni a
poolban. A beérkező kéréseket feldolgozásra a poolnak küldjük. A pool sorban
tartja a beérkező kéréseket. A poolban lévő szálak mindegyike kivesz egy kérést
ebből a sorból, kezeli a kérést, majd újabb kérést kér a sortól. Ezzel a
kialakítással egyszerre legfeljebb _`N`_ kérést tudunk feldolgozni, ahol _`N`_
a szálak száma. Ha minden szál egy hosszan futó kérésre válaszol, a további
kérések akkor is feltorlódhatnak a sorban, de megnöveltük azoknak a hosszan
futó kéréseknek a számát, amelyeket még e pont elérése előtt kezelni tudunk.

Ez a technika csak egy a sok közül, amellyel javítható egy webszerver
átbocsátóképessége. További lehetőségek, amelyeket felfedezhetsz: a fork/join
modell, az egyszálú async I/O modell és a többszálú async I/O modell. Ha érdekel
ez a téma, olvashatsz a többi megoldásról, és megpróbálhatod implementálni
őket; egy olyan alacsony szintű nyelvvel, mint a Rust, mindegyik lehetőség
nyitva áll.

Mielőtt hozzákezdenénk egy thread pool implementálásához, beszéljünk arról,
hogyan is nézzen ki a pool használata. Amikor kódot próbálsz megtervezni, a
kliensoldali felület megírása segíthet a tervezés irányításában. Írd meg a kód
API-ját úgy, hogy a szerkezete olyan legyen, ahogy hívni szeretnéd; utána
implementáld a funkcionalitást ezen a szerkezeten belül, ne pedig fordítva:
előbb a funkcionalitást, aztán a publikus API tervezését.

Ahogy a 12. fejezetben a projektnél teszt-vezérelt fejlesztést használtunk, itt
fordító-vezérelt fejlesztést fogunk használni. Megírjuk azt a kódot, amely a
kívánt függvényeket hívja, majd megnézzük a fordító hibáit, hogy eldöntsük, mit
kell legközelebb változtatnunk, hogy a kód működjön. Előbb azonban azt a
technikát nézzük meg kiindulópontként, amelyet _nem_ fogunk használni.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Szál indítása minden kéréshez

Először nézzük meg, hogyan nézne ki a kódunk, ha minden kapcsolathoz új szálat
hozna létre. Ahogy korábban említettük, nem ez a végleges tervünk, mert
gondokat okoz, hogy potenciálisan korlátlan számú szálat indítanánk, de
kiindulópontnak jó, hogy először egy működő többszálú szerverünk legyen. Ezután
javításként hozzáadjuk a thread poolt, és így könnyebb lesz szembeállítani a két
megoldást.

A 21-11. lista mutatja azokat a változtatásokat, amelyeket a `main` függvényben
kell elvégezni, hogy a `for` cikluson belül minden streamhez új szálat
indítsunk.

<Listing number="21-11" file-name="src/main.rs" caption="Új szál indítása minden streamhez">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Ahogy a 16. fejezetben megtanultad, a `thread::spawn` új szálat hoz létre, majd
lefuttatja a closure kódját az új szálon. Ha futtatod ezt a kódot, és
betöltöd a _/sleep_ címet a böngésződben, majd a _/_ címet két további
böngészőfülön, valóban azt fogod látni, hogy a _/_ kéréseknek nem kell
megvárniuk a _/sleep_ befejeződését. Ahogy azonban említettük, ez végül
túlterheli a rendszert, mert korlátlanul hoznál létre új szálakat.

Talán arra is emlékszel a 17. fejezetből, hogy pontosan ez az a helyzet, ahol
az async és az await igazán jól teljesít! Tartsd ezt szem előtt, miközben
megépítjük a thread poolt, és gondold végig, mi lenne másképp vagy ugyanúgy
asynckel.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Véges számú szál létrehozása {#creating-a-finite-number-of-threads}

Azt szeretnénk, hogy a thread poolunk hasonló, ismerős módon működjön, hogy a
szálakról a thread poolra való átállás ne igényeljen nagy változtatásokat az
API-nkat használó kódban. A 21-12. lista annak a `ThreadPool` structnak a
feltételezett felületét mutatja, amelyet a `thread::spawn` helyett használni
szeretnénk.

<Listing number="21-12" file-name="src/main.rs" caption="Az ideális `ThreadPool` felületünk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

A `ThreadPool::new`-val hozunk létre új thread poolt, konfigurálható számú
szállal, ebben az esetben néggyel. Ezután a `for` ciklusban a `pool.execute`
hasonló felületet ad, mint a `thread::spawn`, amennyiben egy closure-t vesz át,
amelyet a poolnak minden streamhez le kell futtatnia. Úgy kell implementálnunk
a `pool.execute`-ot, hogy átvegye a closure-t, és odaadja a pool egyik
szálának futtatásra. Ez a kód még nem fordul le, de mindenképp megpróbáljuk,
hogy a fordító elvezessen minket a javításhoz.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### A `ThreadPool` megépítése fordító-vezérelt fejlesztéssel

Végezd el a 21-12. lista változtatásait a _src/main.rs_ fájlban, majd hagyjuk,
hogy a `cargo check` fordítási hibái irányítsák a fejlesztésünket. Íme az első
hiba, amelyet kapunk:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Nagyszerű! Ez a hiba azt mondja, hogy szükségünk van egy `ThreadPool` típusra
vagy modulra, úgyhogy most építsünk egyet. A `ThreadPool` implementációnk
független lesz attól, hogy milyen munkát végez a webszerverünk. Alakítsuk át
tehát a `hello` crate-et binary crate-ből library crate-té, hogy abban legyen a
`ThreadPool` implementációnk. Miután áttértünk library crate-re, a különálló
thread pool könyvtárat bármilyen olyan munkához használhatnánk, amelyet thread
poollal szeretnénk végezni, nemcsak webes kérések kiszolgálására.

Hozz létre egy _src/lib.rs_ fájlt a következő tartalommal, ez a `ThreadPool`
struct legegyszerűbb definíciója, amelyet egyelőre adhatunk neki:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Ezután szerkeszd a _main.rs_ fájlt úgy, hogy a `ThreadPool`-t behozza a
hatókörbe a library crate-ből: add hozzá a következő kódot a _src/main.rs_
elejéhez:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Ez a kód még mindig nem működik, de ellenőrizzük újra, hogy megkapjuk a
következő hibát, amellyel foglalkoznunk kell:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Ez a hiba azt jelzi, hogy legközelebb egy `new` nevű asszociált függvényt kell
létrehoznunk a `ThreadPool`-hoz. Azt is tudjuk, hogy a `new`-nak egy olyan
paraméterrel kell rendelkeznie, amely elfogadja a `4`-et argumentumként, és
`ThreadPool` példányt kell visszaadnia. Implementáljuk a legegyszerűbb `new`
függvényt, amely ezekkel a jellemzőkkel bír:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

A `size` paraméter típusának az `usize`-t választottuk, mert tudjuk, hogy
negatív számú szálnak semmi értelme. Azt is tudjuk, hogy ezt a `4`-et egy
szálakat tartalmazó kollekció elemszámaként fogjuk használni, és pontosan erre
való az `usize` típus, ahogy azt a 3. fejezet [„Egész típusok”][integer-types]<!--
ignore --> című szakaszában tárgyaltuk.

Ellenőrizzük újra a kódot:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Most azért lép fel a hiba, mert nincs `execute` metódusunk a `ThreadPool`-on.
Emlékezz vissza a [„Véges számú szál
létrehozása”](#creating-a-finite-number-of-threads)<!-- ignore --> című
szakaszra: úgy döntöttünk, hogy a thread poolunknak a `thread::spawn`-hoz
hasonló felülete legyen. Ezenfelül úgy implementáljuk az `execute` függvényt,
hogy átvegye a neki adott closure-t, és odaadja a pool egy tétlen szálának
futtatásra.

A `ThreadPool` `execute` metódusát úgy definiáljuk, hogy egy closure-t vegyen
át paraméterként. Emlékezz vissza a 13. fejezet [„Elkapott értékek kimozgatása
closure-ökből”][moving-out-of-closures]<!-- ignore --> szakaszára: closure-öket
három különböző trait-tel vehetünk át paraméterként: `Fn`, `FnMut` és
`FnOnce`. El kell döntenünk, melyik closure-fajtát használjuk itt. Tudjuk, hogy
végül valami hasonlót fogunk csinálni, mint a standard könyvtár
`thread::spawn` implementációja, tehát megnézhetjük, milyen bound-okat ír elő a
`thread::spawn` szignatúrája a paraméterére. A dokumentáció ezt mutatja:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Itt az `F` típusparaméter az, ami minket érdekel; a `T` típusparaméter a
visszatérési értékhez kapcsolódik, és az most nem foglalkoztat minket. Látjuk,
hogy a `spawn` az `FnOnce`-ot használja trait boundként az `F`-en.
Valószínűleg mi is ezt szeretnénk, mert végül az `execute`-ban kapott
argumentumot a `spawn`-nak fogjuk átadni. Abban is megerősíthet minket, hogy az
`FnOnce` a keresett trait, hogy a kérést futtató szál csak egyszer fogja
végrehajtani az adott kérés closure-jét, ami illik az `FnOnce` `Once` részéhez.

Az `F` típusparaméternek van egy `Send` trait boundja és egy `'static`
lifetime boundja is, amelyek hasznosak a mi helyzetünkben: a `Send` kell ahhoz,
hogy a closure-t az egyik szálról a másikra vigyük, a `'static` pedig azért,
mert nem tudjuk, mennyi ideig fog tartani a szál végrehajtása. Hozzunk létre a
`ThreadPool`-on egy `execute` metódust, amely egy `F` típusú generikus
paramétert vesz át ezekkel a bound-okkal:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Továbbra is kitesszük a `()`-t az `FnOnce` után, mert ez az `FnOnce` olyan
closure-t jelöl, amely nem vesz át paramétert, és a unit típussal, `()`-vel tér
vissza. Ahogy a függvénydefinícióknál, a visszatérési típus itt is elhagyható a
szignatúrából, de még ha nincs is paraméterünk, a zárójelekre akkor is szükség
van.

Ez megint csak az `execute` metódus legegyszerűbb implementációja: nem csinál
semmit, de egyelőre csak az a célunk, hogy a kódunk lefordítható legyen.
Ellenőrizzük újra:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Lefordul! De vedd észre: ha kipróbálod a `cargo run` parancsot, és kérést
küldesz a böngészőből, azokat a hibákat fogod látni a böngészőben, amelyeket a
fejezet elején láttunk. A könyvtárunk ugyanis még nem hívja meg az
`execute`-nak átadott closure-t!

> Megjegyzés: a szigorú fordítóval bíró nyelvekről, mint a Haskell és a Rust,
> gyakran hallani ezt a mondást: „Ha lefordul a kód, akkor működik.” De ez a
> mondás nem mindig igaz. A projektünk lefordul, de az égvilágon semmit nem
> csinál! Ha valódi, teljes projektet építenénk, most jönne el az ideje, hogy
> egységteszteket kezdjünk írni annak ellenőrzésére, hogy a kód lefordul _és_
> úgy is viselkedik, ahogy szeretnénk.

Gondolkodj el: mi lenne itt másképp, ha closure helyett egy future-t kellene
végrehajtanunk?

#### A szálak számának ellenőrzése a `new`-ban

Semmit nem kezdünk a `new` és az `execute` paramétereivel. Implementáljuk e
függvények törzsét a kívánt viselkedéssel. Kezdjük a `new` átgondolásával.
Korábban előjel nélküli típust választottunk a `size` paraméterhez, mert egy
negatív számú szálat tartalmazó poolnak nincs értelme. Csakhogy egy nulla szálas
poolnak sincs értelme, a nulla mégis tökéletesen érvényes `usize`. Adjunk hozzá
kódot, amely ellenőrzi, hogy a `size` nagyobb-e nullánál, mielőtt visszaadnánk
egy `ThreadPool` példányt, és váltsunk ki panicot az `assert!` makróval, ha a
program nullát kap, ahogy azt a 21-13. lista mutatja.

<Listing number="21-13" file-name="src/lib.rs" caption="A `ThreadPool::new` implementálása úgy, hogy panicot váltson ki, ha a `size` nulla">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Némi dokumentációt is hozzáadtunk a `ThreadPool`-hoz dokumentációs
kommentekkel. Vedd észre, hogy a jó dokumentációs gyakorlatot követve
hozzáadtunk egy szakaszt, amely felhívja a figyelmet azokra a helyzetekre,
amelyekben a függvényünk panicot válthat ki, ahogy azt a 14. fejezetben
tárgyaltuk. Próbáld ki a `cargo doc --open` parancsot, és kattints a
`ThreadPool` structra, hogy lásd, hogyan néz ki a `new`-hoz generált
dokumentáció!

Ahelyett, hogy az `assert!` makrót adnánk hozzá, ahogy itt tettük,
átalakíthatnánk a `new`-t `build`-dé, és `Result`-ot adhatnánk vissza, ahogy a
`Config::build`-del tettük az I/O projektben a 12-9. listában. Ebben az esetben
azonban úgy döntöttünk, hogy szálak nélküli thread pool létrehozásának
megkísérlése helyrehozhatatlan hiba legyen. Ha ambiciózus kedvedben vagy,
próbálj meg írni egy `build` nevű függvényt a következő szignatúrával, és
hasonlítsd össze a `new` függvénnyel:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Hely létrehozása a szálak tárolására

Most, hogy tudjuk, hogyan győződjünk meg róla, hogy érvényes számú szálat
kell tárolnunk a poolban, létrehozhatjuk ezeket a szálakat, és eltárolhatjuk
őket a `ThreadPool` structban, mielőtt visszaadnánk a structot. De hogyan
„tárolunk” egy szálat? Nézzük meg még egyszer a `thread::spawn` szignatúráját:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

A `spawn` függvény `JoinHandle<T>`-t ad vissza, ahol a `T` az a típus, amellyel
a closure visszatér. Próbáljuk ki, hogy mi is `JoinHandle`-t használunk, és
nézzük meg, mi történik. A mi esetünkben a thread poolnak átadott closure-ök a
kapcsolatot kezelik, és nem adnak vissza semmit, tehát a `T` a unit típus, `()`
lesz.

A 21-14. lista kódja lefordul, de még nem hoz létre szálakat. Módosítottuk a
`ThreadPool` definícióját, hogy `thread::JoinHandle<()>` példányok vektorát
tárolja, `size` kapacitással inicializáltuk a vektort, beállítottunk egy `for`
ciklust, amely majd lefuttat valamilyen kódot a szálak létrehozásához, és
visszaadtunk egy ezeket tartalmazó `ThreadPool` példányt.

<Listing number="21-14" file-name="src/lib.rs" caption="Vektor létrehozása, hogy a `ThreadPool` tárolja a szálakat">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

A library crate-ben behoztuk a hatókörbe a `std::thread`-et, mert a
`thread::JoinHandle`-t használjuk a `ThreadPool`-ban lévő vektor elemeinek
típusaként.

Ha érvényes méretet kapunk, a `ThreadPool`-unk létrehoz egy új vektort, amely
`size` darab elemet tud tárolni. A `with_capacity` függvény ugyanazt a feladatot
látja el, mint a `Vec::new`, egy fontos különbséggel: előre lefoglalja a helyet
a vektorban. Mivel tudjuk, hogy `size` elemet kell tárolnunk a vektorban, ez az
előzetes foglalás valamivel hatékonyabb, mint a `Vec::new` használata, amely
az elemek beszúrásakor átméretezi magát.

Ha újra futtatod a `cargo check` parancsot, sikerrel kell járnia.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Kód küldése a `ThreadPool`-ból egy szálnak

A 21-14. lista `for` ciklusában hagytunk egy kommentet a szálak létrehozásáról.
Most megnézzük, hogyan hozzuk létre valójában a szálakat. A standard könyvtár a
`thread::spawn`-t kínálja szálak létrehozására, és a `thread::spawn` azt várja,
hogy megkapja azt a kódot, amelyet a szálnak azonnal le kell futtatnia, amint a
szál létrejött. A mi esetünkben azonban azt szeretnénk, hogy a szálak
létrejöjjenek, és _várjanak_ arra a kódra, amelyet később küldünk nekik. A
standard könyvtár szálimplementációja nem tartalmaz erre módot; ezt nekünk kell
kézzel implementálnunk.

Ezt a viselkedést úgy implementáljuk, hogy egy új adatszerkezetet vezetünk be a
`ThreadPool` és a szálak közé, amely kezeli ezt az új viselkedést. Ezt az
adatszerkezetet _Worker_-nek nevezzük, ami gyakori kifejezés a pool-alapú
implementációkban. A `Worker` felveszi a futtatandó kódot, és lefuttatja a
kódot a saját szálán.

Gondolj úgy, mint egy étterem konyhájában dolgozó emberekre: a dolgozók
várnak, amíg megrendelések nem érkeznek a vendégektől, majd ők felelnek azért,
hogy átvegyék és teljesítsék ezeket a megrendeléseket.

Ahelyett, hogy `JoinHandle<()>` példányok vektorát tárolnánk a thread poolban,
a `Worker` struct példányait fogjuk tárolni. Minden `Worker` egyetlen
`JoinHandle<()>` példányt tárol. Ezután implementálunk a `Worker`-en egy
metódust, amely átvesz egy futtatandó kódot tartalmazó closure-t, és elküldi a
már futó szálnak végrehajtásra. Minden `Worker`-nek adunk egy `id`-t is, hogy
naplózáskor vagy hibakereséskor meg tudjuk különböztetni a pool egyes `Worker`
példányait.

Íme az új folyamat, amely a `ThreadPool` létrehozásakor le fog játszódni. Azt a
kódot, amely a closure-t elküldi a szálnak, azután implementáljuk, hogy a
`Worker`-t így beállítottuk:

1. Definiálunk egy `Worker` structot, amely egy `id`-t és egy `JoinHandle<()>`-t
   tárol.
2. Módosítjuk a `ThreadPool`-t, hogy `Worker` példányok vektorát tárolja.
3. Definiálunk egy `Worker::new` függvényt, amely átvesz egy `id` számot, és egy
   olyan `Worker` példányt ad vissza, amely tárolja az `id`-t és egy üres
   closure-rel indított szálat.
4. A `ThreadPool::new`-ban a `for` ciklus számlálóját használjuk `id`
   előállítására, létrehozunk egy új `Worker`-t ezzel az `id`-vel, és eltároljuk
   a `Worker`-t a vektorban.

Ha kedved van a kihíváshoz, próbáld meg magad implementálni ezeket a
változtatásokat, mielőtt megnéznéd a 21-15. lista kódját.

Készen állsz? Íme a 21-15. lista, amely a fenti módosítások egyik lehetséges
megvalósítását mutatja.

<Listing number="21-15" file-name="src/lib.rs" caption="A `ThreadPool` módosítása úgy, hogy `Worker` példányokat tároljon szálak közvetlen tárolása helyett">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

A `ThreadPool` mezőjének nevét `threads`-ről `workers`-re változtattuk, mert
most már `JoinHandle<()>` példányok helyett `Worker` példányokat tárol. A `for`
ciklus számlálóját argumentumként adjuk át a `Worker::new`-nak, és minden új
`Worker`-t eltárolunk a `workers` nevű vektorban.

A külső kódnak (mint a szerverünk a _src/main.rs_-ben) nem kell ismernie az
implementáció részleteit arról, hogy a `ThreadPool`-on belül `Worker` structot
használunk, ezért a `Worker` structot és a `new` függvényét priváttá tesszük. A
`Worker::new` függvény a neki adott `id`-t használja, és eltárol egy
`JoinHandle<()>` példányt, amely egy üres closure-rel indított új szál
létrehozásával jön létre.

> Megjegyzés: ha az operációs rendszer nem tud szálat létrehozni, mert nincs
> elég rendszererőforrás, a `thread::spawn` panicot vált ki. Ez az egész
> szerverünkben panicot okoz, még akkor is, ha néhány szál létrehozása
> sikerülhetne. Az egyszerűség kedvéért ez a viselkedés így megfelel, de egy
> éles thread pool implementációban valószínűleg a
> [`std::thread::Builder`][builder]<!-- ignore --> típust és annak
> [`spawn`][builder-spawn]<!-- ignore --> metódusát használnád, amely `Result`-ot
> ad vissza.

Ez a kód lefordul, és annyi `Worker` példányt fog tárolni, amennyit a
`ThreadPool::new` argumentumaként megadtunk. De _még mindig_ nem dolgozzuk fel
az `execute`-ban kapott closure-t. Nézzük meg legközelebb, hogyan tehetjük ezt
meg.

#### Kérések küldése a szálaknak csatornákon keresztül

A következő probléma, amelyet megoldunk, az, hogy a `thread::spawn`-nak adott
closure-ök az égvilágon semmit nem csinálnak. Jelenleg a végrehajtandó
closure-t az `execute` metódusban kapjuk meg. De a `thread::spawn`-nak akkor
kell futtatandó closure-t adnunk, amikor az egyes `Worker`-eket létrehozzuk a
`ThreadPool` létrehozása során.

Azt szeretnénk, hogy az imént létrehozott `Worker` structok a futtatandó kódot
egy, a `ThreadPool`-ban tárolt sorból vegyék ki, és elküldjék a saját szálukra
futtatásra.

A 16. fejezetben megismert csatornák – amelyek egyszerű módot adnak két szál
közti kommunikációra – tökéletesek lennének erre a célra. Egy csatornát fogunk
használni a feladatok sorának szerepében, és az `execute` a `ThreadPool`-ból
küld egy feladatot a `Worker` példányoknak, amelyek elküldik a feladatot a
szálukra. Íme a terv:

1. A `ThreadPool` létrehoz egy csatornát, és megtartja a küldő végét.
2. Minden `Worker` megtartja a fogadó véget.
3. Létrehozunk egy új `Job` structot, amely azokat a closure-öket tárolja,
   amelyeket a csatornán le akarunk küldeni.
4. Az `execute` metódus a küldő végen keresztül elküldi a végrehajtandó
   feladatot.
5. A `Worker` a saját szálán végigiterál a fogadó végén, és végrehajtja a
   beérkező feladatok closure-jeit.

Kezdjük azzal, hogy létrehozunk egy csatornát a `ThreadPool::new`-ban, és a
küldő véget a `ThreadPool` példányban tároljuk, ahogy azt a 21-16. lista
mutatja. A `Job` struct egyelőre nem tárol semmit, de ez lesz annak az elemnek
a típusa, amelyet a csatornán leküldünk.

<Listing number="21-16" file-name="src/lib.rs" caption="A `ThreadPool` módosítása úgy, hogy tárolja a `Job` példányokat továbbító csatorna küldő végét">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

A `ThreadPool::new`-ban létrehozzuk az új csatornánkat, és a pool megtartja a
küldő véget. Ez sikeresen lefordul.

Próbáljuk meg átadni a csatorna fogadó végét minden `Worker`-nek, amikor a
thread pool létrehozza a csatornát. Tudjuk, hogy a fogadó véget abban a szálban
akarjuk használni, amelyet a `Worker` példányok indítanak, ezért a closure-ben
hivatkozunk a `receiver` paraméterre. A 21-17. lista kódja még nem egészen
fordul le.

<Listing number="21-17" file-name="src/lib.rs" caption="A fogadó vég átadása minden `Worker`-nek">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Néhány apró és kézenfekvő változtatást végeztünk: átadjuk a fogadó véget a
`Worker::new`-nak, majd használjuk a closure-ön belül.

Amikor megpróbáljuk ellenőrizni ezt a kódot, ezt a hibát kapjuk:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

A kód a `receiver`-t próbálja átadni több `Worker` példánynak. Ez nem fog
működni, ahogy arra a 16. fejezetből emlékszel: a Rust által nyújtott
csatorna-implementáció több _producer_, egy _fogyasztó_ (consumer) elvű. Ez azt
jelenti, hogy nem klónozhatjuk egyszerűen a csatorna fogyasztói végét, hogy
javítsuk ezt a kódot. Azt sem szeretnénk, hogy egy üzenetet többször küldjünk
el több fogyasztónak; egyetlen üzenetlistát szeretnénk több `Worker`
példánnyal úgy, hogy minden üzenetet pontosan egyszer dolgozzon fel valaki.

Ráadásul egy feladat kivétele a csatorna sorából a `receiver` módosításával
jár, tehát a szálaknak biztonságos módra van szükségük a `receiver`
megosztására és módosítására; különben versenyhelyzetek alakulhatnak ki (ahogy
azt a 16. fejezet tárgyalta).

Emlékezz vissza a 16. fejezetben tárgyalt szálbiztos smart pointerekre: ahhoz,
hogy több szál között osszuk meg az ownershipet, és hogy a szálak módosíthassák
az értéket, `Arc<Mutex<T>>`-t kell használnunk. Az `Arc` típus lehetővé teszi,
hogy több `Worker` példány birtokolja a fogadó véget, a `Mutex` pedig
biztosítja, hogy egyszerre csak egy `Worker` kapjon feladatot a fogadó végről.
A 21-18. lista mutatja a szükséges változtatásokat.

<Listing number="21-18" file-name="src/lib.rs" caption="A fogadó vég megosztása a `Worker` példányok között `Arc` és `Mutex` segítségével">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

A `ThreadPool::new`-ban a fogadó véget egy `Arc`-ba és egy `Mutex`-be tesszük.
Minden új `Worker`-höz klónozzuk az `Arc`-ot, hogy megnöveljük a
referenciaszámlálót, és így a `Worker` példányok megoszthassák a fogadó vég
ownershipjét.

Ezekkel a változtatásokkal a kód lefordul! Kezd összeállni!

#### Az `execute` metódus implementálása

Végre implementáljuk a `ThreadPool` `execute` metódusát. A `Job`-ot is
átalakítjuk structból típusaliasszá egy trait objectre, amely az `execute` által
kapott closure típusát tartalmazza. Ahogy azt a 20. fejezet [„Típusszinonimák és
típusaliasok”][type-aliases]<!-- ignore --> című szakaszában tárgyaltuk, a
típusaliasokkal a hosszú típusokat lerövidíthetjük a könnyebb használhatóság
kedvéért. Nézd meg a 21-19. listát.

<Listing number="21-19" file-name="src/lib.rs" caption="`Job` típusalias létrehozása egy `Box`-hoz, amely az egyes closure-öket tárolja, majd a feladat leküldése a csatornán">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Miután létrehoztunk egy új `Job` példányt az `execute`-ban kapott closure-rel,
leküldjük ezt a feladatot a csatorna küldő végén. `unwrap`-et hívunk a `send`-en
arra az esetre, ha a küldés meghiúsulna. Ez például akkor fordulhat elő, ha
leállítjuk az összes szálunk végrehajtását, vagyis a fogadó vég már nem fogad új
üzeneteket. Pillanatnyilag nem tudjuk leállítani a szálaink végrehajtását: a
szálaink addig futnak tovább, amíg a pool létezik. Azért használunk `unwrap`-et,
mert tudjuk, hogy a hibaeset nem fog bekövetkezni, csak a fordító nem tudja ezt.

De még nem vagyunk egészen kész! A `Worker`-ben a `thread::spawn`-nak átadott
closure-ünk még mindig csak _hivatkozik_ a csatorna fogadó végére. Ehelyett azt
szeretnénk, hogy a closure örökké ismételjen, feladatot kérjen a csatorna fogadó
végétől, és futtassa a feladatot, amikor kap egyet. Végezzük el a 21-20.
listában látható változtatást a `Worker::new`-ban.

<Listing number="21-20" file-name="src/lib.rs" caption="A feladatok fogadása és végrehajtása a `Worker` példány szálán">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Itt először `lock`-ot hívunk a `receiver`-en, hogy megszerezzük a mutexet, majd
`unwrap`-et hívunk, hogy bármilyen hiba esetén panicot váltsunk ki. A zár
megszerzése meghiúsulhat, ha a mutex _mérgezett_ (poisoned) állapotban van, ami
akkor fordulhat elő, ha egy másik szál panicot váltott ki, miközben tartotta a
zárat, ahelyett hogy elengedte volna. Ebben a helyzetben az a helyes lépés, ha
`unwrap`-pel panicot váltunk ki ezen a szálon. Nyugodtan cseréld le ezt az
`unwrap`-et egy `expect`-re olyan hibaüzenettel, amely számodra beszédes.

Ha megkapjuk a zárat a mutexen, `recv`-et hívunk, hogy fogadjunk egy `Job`-ot a
csatornáról. Egy záró `unwrap` itt is túllép az esetleges hibákon, amelyek akkor
fordulhatnak elő, ha a küldő véget birtokló szál leállt, hasonlóan ahhoz,
ahogyan a `send` metódus `Err`-t ad vissza, ha a fogadó vég leáll.

A `recv` hívása blokkol, tehát ha még nincs feladat, az aktuális szál addig vár,
amíg feladat nem lesz elérhető. A `Mutex<T>` biztosítja, hogy egyszerre csak egy
`Worker` szál próbáljon feladatot kérni.

A thread poolunk most már működőképes állapotban van! Add ki rá a `cargo run`
parancsot, és küldj néhány kérést:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Sikerült! Most már van egy thread poolunk, amely aszinkron módon hajtja végre a
kapcsolatokat. Soha nem jön létre négynél több szál, így a rendszerünk nem
terhelődik túl, ha a szerver sok kérést kap. Ha kérést küldünk a _/sleep_
címre, a szerver más kéréseket is ki tud szolgálni azzal, hogy egy másik szál
futtatja őket.

> Megjegyzés: ha a _/sleep_ címet több böngészőablakban nyitod meg egyszerre,
> lehet, hogy öt másodperces időközönként, egyesével töltődnek be. Egyes
> böngészők gyorsítótárazási okokból egymás után hajtják végre ugyanannak a
> kérésnek a több példányát. Ezt a korlátot nem a mi webszerverünk okozza.

Itt jó alkalom megállni, és végiggondolni, mennyiben lenne más a 21-18., a
21-19. és a 21-20. lista kódja, ha closure helyett future-öket használnánk az
elvégzendő munkához. Mely típusok változnának? Mennyiben lennének mások a
metódusszignatúrák, ha egyáltalán? A kód mely részei maradnának ugyanazok?

Miután a 17. és a 19. fejezetben megismerted a `while let` ciklust, talán
felmerül benned, hogy miért nem úgy írtuk meg a `Worker` szálának kódját, ahogy
azt a 21-21. lista mutatja.

<Listing number="21-21" file-name="src/lib.rs" caption="A `Worker::new` egy alternatív implementációja `while let` használatával">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Ez a kód lefordul és fut, de nem eredményezi a kívánt szálkezelési viselkedést:
egy lassú kérés továbbra is várakozásra kényszeríti a többi kérés
feldolgozását. Az ok kissé finom: a `Mutex` structnak nincs publikus `unlock`
metódusa, mert a zár ownershipje azon a `MutexGuard<T>`-en múlik, amely a `lock`
metódus által visszaadott `LockResult<MutexGuard<T>>`-ben található. Fordítási
időben így a borrow checker be tudja tartatni azt a szabályt, hogy a `Mutex`
által őrzött erőforráshoz nem lehet hozzáférni, hacsak nem tartjuk a zárat. Ez
az implementáció azonban azt is eredményezheti, hogy a zárat a szándékoltnál
tovább tartjuk, ha nem figyelünk oda a `MutexGuard<T>` lifetime-jára.

A 21-20. lista kódja, amely a `let job =
receiver.lock().unwrap().recv().unwrap();` sort használja, azért működik, mert
`let` esetén az egyenlőségjel jobb oldalán álló kifejezésben használt ideiglenes
értékek azonnal eldobódnak, amint a `let` utasítás véget ér. A `while let`
(valamint az `if let` és a `match`) viszont csak a hozzá tartozó blokk végén
dobja el az ideiglenes értékeket. A 21-21. listában a zár a `job()` hívásának
teljes ideje alatt megmarad, vagyis a többi `Worker` példány nem tud feladatot
fogadni.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
