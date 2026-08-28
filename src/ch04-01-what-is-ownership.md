## Mi az az ownership?

Az _ownership_ szabályok együttese, amelyek megszabják, hogyan kezeli a memóriát
egy Rust-program. Minden programnak kezelnie kell, hogyan használja futás közben
a számítógép memóriáját. Egyes nyelvekben garbage collection van, amely a program
futása során rendszeresen megkeresi a már nem használt memóriát; más nyelvekben a
programozónak kell explicit módon lefoglalnia és felszabadítania a memóriát. A
Rust egy harmadik megközelítést használ: a memóriát az ownership rendszere kezeli,
olyan szabályokkal, amelyeket a fordító ellenőriz. Ha bármelyik szabály sérül, a
program nem fordul le. Az ownership egyetlen eleme sem lassítja a programodat
futás közben.

Mivel az ownership sok programozó számára új fogalom, időbe telik megszokni. A jó
hír az, hogy minél nagyobb tapasztalatot szerzel a Rustban és az ownership
rendszerének szabályaiban, annál könnyebben fogsz természetes módon biztonságos
és hatékony kódot írni. Ne add fel!

Ha megérted az ownershipet, szilárd alapod lesz azoknak a képességeknek a
megértéséhez, amelyek a Rustot egyedivé teszik. Ebben a fejezetben néhány olyan
példán keresztül ismerkedsz meg az ownershippel, amelyek egy nagyon gyakori
adatszerkezetre összpontosítanak: a sztringekre.

> ### A stack és a heap {#the-stack-and-the-heap}
>
> Sok programozási nyelvben nem kell túl gyakran a stackkel és a heappel
> foglalkoznod. Egy olyan rendszerprogramozási nyelvben azonban, mint a Rust, az,
> hogy egy érték a stacken vagy a heapen van-e, befolyásolja a nyelv
> viselkedését, és azt is, miért kell bizonyos döntéseket meghoznod. Az ownership
> egyes részeit a fejezet későbbi részében a stackhez és a heaphez viszonyítva
> mutatjuk be, ezért itt egy rövid magyarázat következik felkészülésképpen.
>
> A stack és a heap egyaránt a kódod számára futásidőben elérhető memória része,
> de eltérő módon vannak felépítve. A stack abban a sorrendben tárolja az
> értékeket, ahogy megkapja őket, és fordított sorrendben veszi ki őket. Ezt
> nevezzük _utoljára be, elsőként ki (last in, first out, LIFO)_ elvnek. Gondolj
> egy tányérhalomra: amikor újabb tányérokat teszel hozzá, a halom tetejére
> helyezed őket, és amikor tányérra van szükséged, a tetejéről veszel el egyet. A
> halom közepéről vagy aljáról tányért betenni vagy kivenni nem menne ilyen
> jól! Az adat hozzáadását _a stackre helyezésnek (push)_, az adat eltávolítását
> pedig _a stackről levételnek (pop)_ nevezzük. Minden, a stacken tárolt adatnak
> ismert, rögzített méretűnek kell lennie. Az olyan adatot, amelynek a mérete
> fordítási időben ismeretlen, vagy amelynek a mérete változhat, a heapen kell
> tárolni.
>
> A heap kevésbé rendezett: amikor adatot teszel a heapre, egy bizonyos mennyiségű
> helyet kérsz. A memóriafoglaló (allokátor) talál egy elég nagy üres helyet a
> heapen, megjelöli használtként, és visszaad egy _pointert_, amely az adott hely
> címe. Ezt a folyamatot _a heapen való lefoglalásnak_ nevezzük, és néha csak
> _lefoglalásként_ rövidítjük (az értékek stackre helyezését nem tekintjük
> lefoglalásnak). Mivel a heapre mutató pointer ismert, rögzített méretű, a
> pointert a stacken tárolhatod, de amikor a tényleges adatra van szükséged, a
> pointert követned kell. Gondolj arra, amikor egy étteremben leültetnek. Amikor
> belépsz, megmondod, hányan vagytok, a hostess pedig talál egy üres asztalt,
> ahová mindenki elfér, és odavezet titeket. Ha valaki később érkezik a
> társaságból, megkérdezheti, hová ültettek titeket, hogy megtaláljon.
>
> A stackre helyezés gyorsabb, mint a heapen való lefoglalás, mert az
> allokátornak sosem kell helyet keresnie az új adat tárolásához; az a hely mindig
> a stack teteje. Ehhez képest a heapen való helyfoglalás több munkát igényel,
> mert az allokátornak először találnia kell egy elég nagy helyet az adat
> tárolásához, majd nyilvántartást kell vezetnie a következő foglalás
> előkészítéséhez.
>
> A heapen lévő adat elérése általában lassabb, mint a stacken lévőé, mert oda
> egy pointert követve jutsz el. A mai processzorok gyorsabbak, ha kevesebbet
> ugrálnak a memóriában. Folytatva a hasonlatot, képzelj el egy pincért az
> étteremben, aki sok asztaltól vesz fel rendelést. A leghatékonyabb, ha egy
> asztalnál az összes rendelést felveszi, mielőtt a következő asztalhoz megy. Ha
> felvenne egy rendelést az A asztalnál, majd egyet a B asztalnál, aztán megint
> egyet A-nál, majd megint egyet B-nél, az sokkal lassabb folyamat lenne. Ehhez
> hasonlóan a processzor általában jobban végzi a dolgát, ha olyan adaton
> dolgozik, amely közel van más adatokhoz (mint a stacken), nem pedig távolabb
> (mint ahogy az a heapen lehet).
>
> Amikor a kódod meghív egy függvényt, a függvénynek átadott értékek (beleértve
> adott esetben a heapen lévő adatra mutató pointereket is) és a függvény lokális
> változói a stackre kerülnek. Amikor a függvény véget ér, ezek az értékek
> lekerülnek a stackről.
>
> Annak nyilvántartása, hogy a kód mely részei milyen adatot használnak a heapen,
> a heapen lévő adatduplikációk minimalizálása, valamint a heapen lévő nem
> használt adat kitakarítása, hogy ne fogyj ki a helyből – ezek mind olyan
> problémák, amelyeket az ownership old meg. Ha egyszer megérted az ownershipet,
> nem kell majd túl gyakran a stackkel és a heappel foglalkoznod. Az viszont, ha
> tudod, hogy az ownership fő célja a heapen lévő adat kezelése, segíthet
> megmagyarázni, miért éppen úgy működik, ahogy.

### Az ownership szabályai

Először nézzük meg az ownership szabályait. Tartsd észben ezeket a szabályokat,
miközben végigmegyünk az őket szemléltető példákon:

- A Rustban minden értéknek van egy _ownere_.
- Egyszerre csak egy owner lehet.
- Amikor az owner kilép a hatóköréből, az érték eldobásra kerül.

### Változók hatóköre

Most, hogy túl vagyunk a Rust alapvető szintaxisán, nem szerepeltetjük a
példákban a teljes `fn main() {` kódot, így ha együtt haladsz velünk, ügyelj rá,
hogy a következő példákat kézzel egy `main` függvénybe helyezd. Ennek
eredményeként a példáink tömörebbek lesznek, és a sablonkód helyett a valódi
részletekre tudunk összpontosítani.

Az ownership első példájaként néhány változó hatókörét fogjuk megnézni. A
_hatókör_ az a tartomány a programon belül, amelyen belül egy elem érvényes.
Vegyük a következő változót:

```rust
let s = "hello";
```

Az `s` változó egy sztringliterálra hivatkozik, ahol a sztring értéke a
programunk szövegébe van beégetve. A változó attól a ponttól kezdve érvényes,
ahol deklaráljuk, egészen az aktuális hatókör végéig. A 4-1. lista egy programot
mutat be olyan kommentekkel, amelyek jelzik, hol lenne érvényes az `s` változó.

<Listing number="4-1" caption="Egy változó és a hatókör, amelyen belül érvényes">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-01/src/main.rs:here}}
```

</Listing>

Más szóval két fontos időpont van itt:

- Amikor `s` _belép_ a hatókörbe, érvényessé válik.
- Érvényes marad, amíg _ki nem lép_ a hatóköréből.

Ezen a ponton a hatókörök és a változók érvényessége közötti kapcsolat hasonló
ahhoz, amit más programozási nyelvekben látunk. Most erre a megértésre építve
bevezetjük a `String` típust.

### A `String` típus

Az ownership szabályainak szemléltetéséhez egy olyan adattípusra van szükségünk,
amely bonyolultabb azoknál, amelyeket a 3. fejezet [„Adattípusok”][data-types]<!-- ignore -->
című szakaszában tárgyaltunk. A korábban tárgyalt típusok ismert méretűek, a
stacken tárolhatók, és lekerülnek a stackről, amikor a hatókörük véget ér,
továbbá gyorsan és egyszerűen másolhatók egy új, független példány
létrehozásához, ha a kód egy másik részének ugyanazt az értéket kell használnia
egy másik hatókörben. Mi azonban olyan adatot szeretnénk megnézni, amely a heapen
tárolódik, és fel akarjuk fedezni, honnan tudja a Rust, mikor kell kitakarítania
ezt az adatot – a `String` típus pedig kiváló példa erre.

A `String` típusnak azokra a részeire fogunk összpontosítani, amelyek az
ownershiphez kapcsolódnak. Ezek a szempontok más összetett adattípusokra is
érvényesek, akár a standard könyvtár biztosítja őket, akár te hozod létre őket. A
`String` ownershiptől független szempontjait a [8. fejezetben][ch8]<!-- ignore -->
tárgyaljuk.

A sztringliterálokat már láttuk, ahol a sztring értéke bele van égetve a
programunkba. A sztringliterálok kényelmesek, de nem minden olyan helyzetre
alkalmasak, amelyben szöveget szeretnénk használni. Az egyik ok, hogy nem
módosíthatók. A másik, hogy nem minden sztringérték ismerhető meg akkor, amikor a
kódunkat írjuk: mi van például akkor, ha a felhasználó bemenetét szeretnénk venni
és eltárolni? Ilyen helyzetekre való a Rustban a `String` típus. Ez a típus a
heapen lefoglalt adatot kezel, és így olyan mennyiségű szöveget tud tárolni,
amely fordítási időben ismeretlen a számunkra. Egy `String` értéket a `from`
függvénnyel hozhatsz létre egy sztringliterálból, így:

```rust
let s = String::from("hello");
```

A kettős kettőspont `::` operátor lehetővé teszi, hogy ezt a bizonyos `from`
függvényt a `String` típus névterébe soroljuk ahelyett, hogy valamilyen
`string_from`-féle nevet használnánk. Erről a szintaxisról részletesebben az 5.
fejezet [„Metódusok”][methods]<!-- ignore --> című szakaszában lesz szó, valamint
akkor, amikor a 7. fejezet [„Útvonalak a modulfában lévő elemekre való
hivatkozáshoz”][paths-module-tree]<!-- ignore --> részében a modulokkal való
névterezésről beszélünk.

Ez a fajta sztring _módosítható_:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-01-can-mutate-string/src/main.rs:here}}
```

Mi tehát itt a különbség? Miért módosítható a `String`, a literálok pedig miért
nem? A különbség abban rejlik, hogyan bánik ez a két típus a memóriával.

### Memória és foglalás

Egy sztringliterál esetében fordítási időben ismerjük a tartalmat, így a szöveg
közvetlenül bele van égetve a végleges futtatható állományba. Ezért gyorsak és
hatékonyak a sztringliterálok. Ezek a tulajdonságok azonban csak a
sztringliterálok módosíthatatlanságából fakadnak. Sajnos nem tehetünk egy
memóriadarabot a binárisba minden olyan szövegrészlet számára, amelynek a mérete
fordítási időben ismeretlen, és amelynek a mérete a program futása közben
változhat.

A `String` típusnál ahhoz, hogy módosítható, növelhető szövegdarabot
támogassunk, fordítási időben ismeretlen mennyiségű memóriát kell lefoglalnunk a
heapen a tartalom tárolására. Ez a következőket jelenti:

- A memóriát futásidőben kell kérnünk a memóriafoglalótól.
- Szükségünk van egy módra, amellyel ezt a memóriát visszaadjuk az allokátornak,
  amikor végeztünk a `String` értékünkkel.

Az első részt mi végezzük el: amikor meghívjuk a `String::from` függvényt, annak
implementációja kikéri a szükséges memóriát. Ez nagyjából minden programozási
nyelvben így van.

A második rész azonban más. Az olyan nyelvekben, amelyekben van _garbage
collector (GC)_, a GC tartja nyilván és takarítja ki a már nem használt
memóriát, nekünk pedig nem kell ezzel foglalkoznunk. A legtöbb GC nélküli
nyelvben a mi felelősségünk felismerni, mikor nem használjuk már a memóriát, és
meghívni azt a kódot, amely explicit módon felszabadítja – ugyanúgy, ahogy a
kérésénél is tettük. Ennek helyes elvégzése történetileg nehéz programozási
probléma volt. Ha elfelejtjük, memóriát pazarlunk. Ha túl korán tesszük meg,
érvénytelen változónk lesz. Ha kétszer tesszük meg, az is hiba. Pontosan egy
`allocate` hívást kell pontosan egy `free` hívással párosítanunk.

A Rust más utat választ: a memória automatikusan visszaadásra kerül, amint az azt
birtokló változó kilép a hatóköréből. Íme a 4-1. listában szereplő hatókörpéldánk
egy változata, amely sztringliterál helyett `String` értéket használ:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
```

Van egy természetes pont, ahol a `String` értékünkhöz szükséges memóriát
visszaadhatjuk az allokátornak: amikor `s` kilép a hatóköréből. Amikor egy változó
kilép a hatóköréből, a Rust meghív helyettünk egy speciális függvényt. Ennek a
függvénynek a neve `drop`, és ide helyezheti a `String` szerzője a memóriát
visszaadó kódot. A Rust automatikusan meghívja a `drop` függvényt a záró kapcsos
zárójelnél.

> Megjegyzés: a C++-ban az erőforrások felszabadításának ezt a mintáját, amely egy
> elem élettartamának végén történik, néha _Resource Acquisition Is
> Initialization (RAII)_ néven emlegetik. A Rust `drop` függvénye ismerős lesz
> számodra, ha használtál már RAII-mintákat.

Ennek a mintának mélyreható hatása van arra, ahogyan a Rust-kódot írjuk. Most még
egyszerűnek tűnhet, de a kód viselkedése váratlan lehet bonyolultabb
helyzetekben, amikor azt szeretnénk, hogy több változó használja a heapen
lefoglalt adatunkat. Nézzünk meg most néhányat ezek közül a helyzetek közül.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-move"></a>

#### Változók és adatok kölcsönhatása: move {#variables-and-data-interacting-with-move}

A Rustban több változó is különböző módokon léphet kölcsönhatásba ugyanazzal az
adattal. A 4-2. lista egy egész számot használó példát mutat be.

<Listing number="4-2" caption="Az `x` változó egész értékének hozzárendelése `y`-hoz">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-02/src/main.rs:here}}
```

</Listing>

Valószínűleg ki tudjuk találni, mit csinál ez: „Kösd az `5` értéket `x`-hez;
aztán készíts másolatot az `x`-ben lévő értékről, és kösd azt `y`-hoz.” Most két
változónk van, `x` és `y`, és mindkettő `5`-tel egyenlő. Valóban ez történik,
mert az egész számok egyszerű, ismert és rögzített méretű értékek, és ez a két
`5` érték a stackre kerül.

Most nézzük meg a `String` változatot:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-03-string-move/src/main.rs:here}}
```

Ez nagyon hasonlónak tűnik, így azt feltételezhetnénk, hogy a működése is
ugyanaz: vagyis a második sor másolatot készít az `s1`-ben lévő értékről, és azt
`s2`-höz köti. De nem egészen ez történik.

Nézd meg a 4-1. ábrát, hogy lásd, mi történik a `String` értékkel a színfalak
mögött. Egy `String` három részből áll, amelyeket a bal oldal mutat: egy
pointerből, amely a sztring tartalmát tároló memóriára mutat, egy hosszból és egy
kapacitásból. Ez az adatcsoport a stacken tárolódik. A jobb oldalon a heapen lévő
memória látható, amely a tartalmat tárolja.

<img alt="Két táblázat: az első táblázat az s1 stacken lévő ábrázolását
tartalmazza, amely a hosszából (5), a kapacitásából (5) és egy pointerből áll,
amely a második táblázat első értékére mutat. A második táblázat a sztringadat
heapen lévő ábrázolását tartalmazza, bájtról bájtra." src="img/trpl04-01.svg" class="center"
style="width: 50%;" />

<span class="caption">4-1. ábra: Egy `"hello"` értéket tartalmazó, `s1`-hez
kötött `String` memóriabeli ábrázolása</span>

A hossz azt mutatja meg, mennyi memóriát – bájtban – használ jelenleg a `String`
tartalma. A kapacitás az a teljes memóriamennyiség – bájtban –, amelyet a
`String` az allokátortól kapott. A hossz és a kapacitás közötti különbség
számít, de nem ebben az összefüggésben, ezért egyelőre nyugodtan figyelmen kívül
hagyhatjuk a kapacitást.

Amikor `s1`-et `s2`-höz rendeljük, a `String` adatai másolódnak, vagyis lemásoljuk
a pointert, a hosszt és a kapacitást, amelyek a stacken vannak. Nem másoljuk le a
heapen lévő adatot, amelyre a pointer hivatkozik. Más szóval a memóriabeli
adatábrázolás a 4-2. ábrán láthatóhoz hasonlóan néz ki.

<img alt="Három táblázat: az s1 és s2 táblázatok ezeket a sztringeket ábrázolják
a stacken, és mindkettő ugyanarra a sztringadatra mutat a heapen."
src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">4-2. ábra: Az `s2` változó memóriabeli ábrázolása, amely az
`s1` pointerének, hosszának és kapacitásának másolatát tartalmazza</span>

Az ábrázolás _nem_ úgy néz ki, mint a 4-3. ábra, amely azt mutatja, hogyan
festene a memória, ha a Rust a heapen lévő adatot is lemásolná. Ha a Rust ezt
tenné, az `s2 = s1` művelet futásidejű teljesítmény szempontjából nagyon
költséges lehetne, ha a heapen lévő adat nagy méretű volna.

<img alt="Négy táblázat: két táblázat az s1 és s2 stacken lévő adatait
ábrázolja, és mindegyik a heapen lévő saját sztringadat-másolatára mutat."
src="img/trpl04-03.svg" class="center" style="width: 50%;" />

<span class="caption">4-3. ábra: Egy másik lehetőség arra, mit tehetne az `s2 =
s1`, ha a Rust a heapen lévő adatot is lemásolná</span>

Korábban azt mondtuk, hogy amikor egy változó kilép a hatóköréből, a Rust
automatikusan meghívja a `drop` függvényt, és kitakarítja az adott változóhoz
tartozó heapmemóriát. A 4-2. ábrán viszont mindkét adatpointer ugyanarra a helyre
mutat. Ez probléma: amikor `s2` és `s1` kilép a hatóköréből, mindkettő ugyanazt a
memóriát próbálja majd felszabadítani. Ezt _double free_ hibának nevezzük, és ez
az egyik korábban említett memóriabiztonsági hiba. A memória kétszeri
felszabadítása memóriasérüléshez vezethet, ami akár biztonsági sebezhetőségeket
is eredményezhet.

A memóriabiztonság garantálása érdekében a Rust a `let s2 = s1;` sor után `s1`-et
már nem tekinti érvényesnek. Ezért a Rustnak semmit nem kell felszabadítania,
amikor `s1` kilép a hatóköréből. Nézd meg, mi történik, ha megpróbálod használni
`s1`-et azután, hogy `s2` létrejött; nem fog működni:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/src/main.rs:here}}
```

A következőhöz hasonló hibát kapsz, mert a Rust megakadályozza, hogy az
érvénytelenített referenciát használd:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/output.txt}}
```

Ha más nyelvekkel dolgozva már hallottad a _sekély másolat_ (shallow copy) és a
_mély másolat_ (deep copy) kifejezéseket, akkor a pointer, a hossz és a kapacitás
másolása az adat másolása nélkül valószínűleg sekély másolat készítésének hangzik.
Mivel azonban a Rust az első változót ráadásul érvényteleníti is, ezt nem sekély
másolatnak, hanem _move_-nak nevezzük. Ebben a példában azt mondanánk, hogy `s1`
_move_-olva lett `s2`-be. Tehát valójában az történik, amit a 4-4. ábra mutat.

<img alt="Három táblázat: az s1 és s2 táblázatok ezeket a sztringeket ábrázolják
a stacken, és mindkettő ugyanarra a sztringadatra mutat a heapen. Az s1 táblázat
szürkített, mert s1 már nem érvényes; a heapen lévő adat csak s2-n keresztül
érhető el." src="img/trpl04-04.svg" class="center" style="width:
50%;" />

<span class="caption">4-4. ábra: A memória ábrázolása azután, hogy `s1`
érvénytelenné vált</span>

Ezzel meg is oldódott a problémánk! Mivel csak `s2` érvényes, amikor kilép a
hatóköréből, egyedül ő szabadítja fel a memóriát, és ezzel készen is vagyunk.

Ezenfelül van egy tervezési döntés, amely mindebből következik: a Rust soha nem
készít automatikusan „mély” másolatot az adataidról. Ezért bármely _automatikus_
másolásról feltételezhető, hogy futásidejű teljesítmény szempontjából nem
költséges.

#### Hatókör és értékadás

Ennek a fordítottja is igaz a hatókör, az ownership és a memória `drop`
függvényen keresztüli felszabadítása közötti kapcsolatra. Amikor egy létező
változóhoz teljesen új értéket rendelsz, a Rust meghívja a `drop` függvényt, és
azonnal felszabadítja az eredeti érték memóriáját. Vedd például a következő
kódot:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04b-replacement-drop/src/main.rs:here}}
```

Először deklarálunk egy `s` változót, és egy `"hello"` értékű `String` értékhez
kötjük. Ezután azonnal létrehozunk egy új, `"ahoy"` értékű `String` értéket, és
azt rendeljük `s`-hez. Ezen a ponton már semmi nem hivatkozik az eredeti, heapen
lévő értékre. A 4-5. ábra a stack és a heap adatait szemlélteti ekkor:

<img alt="Egy táblázat, amely a stacken lévő sztringértéket ábrázolja, és a
heapen lévő második sztringadatra (ahoy) mutat, míg az eredeti sztringadat
(hello) szürkített, mert már nem érhető el."
src="img/trpl04-05.svg" class="center" style="width: 50%;" />

<span class="caption">4-5. ábra: A memória ábrázolása azután, hogy a kezdeti
értéket teljes egészében lecseréltük</span>

Az eredeti sztring így azonnal kilép a hatóköréből. A Rust lefuttatja rajta a
`drop` függvényt, és a memóriája azonnal felszabadul. Amikor a végén kiírjuk az
értéket, az `"ahoy, world!"` lesz.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-clone"></a>

#### Változók és adatok kölcsönhatása: clone {#variables-and-data-interacting-with-clone}

Ha _tényleg_ mélymásolatot szeretnénk készíteni a `String` heapen lévő adatáról,
nem csak a stacken lévő adatáról, használhatunk egy elterjedt metódust, a `clone`
metódust. A metódusszintaxist az 5. fejezetben tárgyaljuk, de mivel a metódusok
sok programozási nyelvben megszokott elemek, valószínűleg találkoztál már velük.

Íme egy példa a `clone` metódus működésére:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-05-clone/src/main.rs:here}}
```

Ez remekül működik, és explicit módon azt a viselkedést eredményezi, amelyet a
4-3. ábra mutat, ahol a heapen lévő adat _valóban_ másolódik.

Amikor egy `clone` hívást látsz, tudod, hogy valamilyen tetszőleges kód fut le,
és az a kód költséges lehet. Ez egy vizuális jelzés arról, hogy valami más
történik.

#### Csak a stacken lévő adat: `Copy` {#stack-only-data-copy}

Van még egy dolog, amiről eddig nem beszéltünk. Ez az egész számokat használó kód
– amelynek egy részét a 4-2. listában láttuk – működik és érvényes:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-06-copy/src/main.rs:here}}
```

Ez a kód azonban ellentmondani látszik annak, amit épp most tanultunk: nincs
`clone` hívásunk, `x` mégis érvényes, és nem lett `y`-ba move-olva.

Ennek az az oka, hogy az olyan típusok, mint az egész számok, amelyeknek a mérete
fordítási időben ismert, teljes egészében a stacken tárolódnak, így a tényleges
értékek másolatai gyorsan elkészíthetők. Ez azt jelenti, hogy semmi okunk nem
lenne megakadályozni, hogy `x` érvényes maradjon azután, hogy létrehoztuk az `y`
változót. Más szóval itt nincs különbség a mély és a sekély másolás között, így a
`clone` hívása sem tenne mást, mint a szokásos sekély másolás, ezért el is
hagyhatjuk.

A Rustban van egy speciális annotáció, a `Copy` trait, amelyet olyan típusokra
helyezhetünk, amelyek a stacken tárolódnak, ahogy az egész számok is (a
trait-ekről bővebben a [10. fejezetben][traits]<!-- ignore --> lesz szó). Ha egy
típus implementálja a `Copy` traitet, az azt használó változók nem move-olódnak,
hanem egyszerűen másolódnak, így egy másik változóhoz való hozzárendelés után is
érvényesek maradnak.

A Rust nem engedi, hogy egy típust `Copy` annotációval lássunk el, ha a típus
vagy annak bármely része implementálta a `Drop` traitet. Ha a típusnak valami
speciálisra van szüksége akkor, amikor az érték kilép a hatóköréből, és mi
ellátjuk azt a típust a `Copy` annotációval, fordítási idejű hibát kapunk. Ha
szeretnéd megtudni, hogyan add hozzá a `Copy` annotációt a saját típusodhoz a
trait implementálásához, lásd a C függelék [„Származtatható
trait-ek”][derivable-traits]<!-- ignore --> című részét.

Mely típusok implementálják tehát a `Copy` traitet? A biztonság kedvéért
megnézheted az adott típus dokumentációját, de általános szabályként bármely
egyszerű skalárértékekből álló csoport implementálhatja a `Copy` traitet, és
semmi olyan nem implementálhatja, ami memóriafoglalást igényel, vagy valamilyen
erőforrás. Íme néhány olyan típus, amely implementálja a `Copy` traitet:

- Az összes egész típus, például az `u32`.
- A logikai típus, a `bool`, `true` és `false` értékekkel.
- Az összes lebegőpontos típus, például az `f64`.
- A karaktertípus, a `char`.
- A tuple-ök, ha csak olyan típusokat tartalmaznak, amelyek szintén
  implementálják a `Copy` traitet. Például az `(i32, i32)` implementálja a
  `Copy` traitet, az `(i32, String)` viszont nem.

### Az ownership és a függvények

Egy érték függvénynek való átadásának mechanizmusa hasonló ahhoz, mint amikor egy
értéket egy változóhoz rendelünk. Egy változó függvénynek való átadása
move-olással vagy másolással jár, ugyanúgy, mint az értékadás. A 4-3. listában
egy példa látható néhány kommenttel, amelyek megmutatják, hol lépnek be a
változók a hatókörbe, és hol lépnek ki belőle.

<Listing number="4-3" file-name="src/main.rs" caption="Függvények az ownership és a hatókör kommentekkel jelölve">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</Listing>

Ha a `takes_ownership` hívása után megpróbálnánk használni `s`-et, a Rust
fordítási idejű hibát dobna. Ezek a statikus ellenőrzések megóvnak minket a
hibáktól. Próbálj meg olyan kódot hozzáadni a `main` függvényhez, amely `s`-et és
`x`-et használja, hogy lásd, hol használhatod őket, és hol akadályoznak meg ebben
az ownership szabályai.

### Visszatérési értékek és hatókör

A visszatérési értékek szintén átadhatják az ownershipet. A 4-4. lista egy olyan
függvényre mutat példát, amely visszaad valamilyen értéket, a 4-3. listához
hasonló kommentekkel.

<Listing number="4-4" file-name="src/main.rs" caption="A visszatérési értékek ownershipjének átadása">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-04/src/main.rs}}
```

</Listing>

Egy változó ownershipje minden alkalommal ugyanezt a mintát követi: ha egy
értéket egy másik változóhoz rendelünk, az move-olódik. Amikor egy heapen lévő
adatot tartalmazó változó kilép a hatóköréből, az értéket a `drop` takarítja ki,
hacsak az adat ownershipje nem került át egy másik változóhoz.

Bár ez működik, kissé fárasztó minden függvénynél átvenni, majd visszaadni az
ownershipet. Mi van akkor, ha azt szeretnénk, hogy egy függvény használhasson egy
értéket anélkül, hogy átvenné az ownershipjét? Elég bosszantó, hogy bármit, amit
átadunk, vissza is kell adni, ha újra használni akarjuk – azon az adaton felül,
amely a függvény törzséből eredményként adódik, és amelyet szintén vissza
szeretnénk kapni.

A Rust lehetővé teszi, hogy tuple használatával több értéket adjunk vissza, ahogy
azt a 4-5. lista mutatja.

<Listing number="4-5" file-name="src/main.rs" caption="A paraméterek ownershipjének visszaadása">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-05/src/main.rs}}
```

</Listing>

Ez azonban túl sok ceremónia és túl sok munka egy olyan fogalomhoz, amelynek
megszokottnak kellene lennie. Szerencsénkre a Rustnak van egy olyan képessége,
amellyel úgy használhatunk egy értéket, hogy közben nem adjuk át az ownershipjét:
ezek a referenciák.

[data-types]: ch03-02-data-types.html#data-types
[ch8]: ch08-02-strings.html
[traits]: ch10-02-traits.html
[derivable-traits]: appendix-03-derivable-traits.html
[methods]: ch05-03-method-syntax.html#methods
[paths-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
