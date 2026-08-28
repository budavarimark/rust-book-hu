## Unsafe Rust

Az eddig tárgyalt kód mindegyikére érvényesek voltak a Rust fordítási időben
kikényszerített memóriabiztonsági garanciái. A Rustban azonban egy második
nyelv is rejtőzik, amely nem kényszeríti ki ezeket a memóriabiztonsági
garanciákat: ezt hívjuk _unsafe Rust_-nak, és pontosan úgy működik, mint a
szokásos Rust, csak extra szupererőket ad nekünk.

Az unsafe Rust azért létezik, mert a statikus analízis természeténél fogva
konzervatív. Amikor a fordító megpróbálja eldönteni, hogy egy kód betartja-e a
garanciákat, jobb, ha inkább elutasít néhány érvényes programot, mint hogy
elfogadjon néhány érvénytelent. Bár a kód _lehet_, hogy rendben van, ha a Rust
fordítójának nincs elég információja ahhoz, hogy biztos legyen a dolgában,
elutasítja a kódot. Ilyen esetekben unsafe kóddal mondhatod a fordítónak, hogy
„bízz bennem, tudom, mit csinálok”. Vigyázz azonban: az unsafe Rustot a saját
felelősségedre használod. Ha helytelenül használsz unsafe kódot, problémák
adódhatnak a memóriabiztonság sérüléséből, például null pointer
dereferálásából.

A Rust másik oka arra, hogy legyen egy unsafe alteregója, az, hogy a mögöttes
számítógépes hardver eleve nem biztonságos. Ha a Rust nem engedne unsafe
műveleteket, bizonyos feladatokat nem tudnál elvégezni. A Rustnak lehetővé kell
tennie az alacsony szintű rendszerprogramozást, például az operációs
rendszerrel való közvetlen interakciót, vagy akár a saját operációs rendszered
megírását. Az alacsony szintű rendszerprogramozás támogatása a nyelv egyik
célja. Nézzük meg, mit tehetünk az unsafe Rusttal, és hogyan.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Az unsafe szupererők használata

Ahhoz, hogy átválts unsafe Rustra, használd az `unsafe` kulcsszót, majd nyiss
egy új blokkot, amely az unsafe kódot tartalmazza. Az unsafe Rustban öt olyan
műveletet végezhetsz el, amit a safe Rustban nem; ezeket nevezzük _unsafe
szupererőknek_. Ezek a szupererők a következő képességeket foglalják magukban:

1. Nyers pointer dereferálása.
1. Unsafe függvény vagy metódus hívása.
1. Módosítható statikus változó elérése vagy módosítása.
1. Unsafe trait implementálása.
1. `union`-ök mezőinek elérése.

Fontos megérteni, hogy az `unsafe` nem kapcsolja ki a borrow checkert, és nem
tiltja le a Rust többi biztonsági ellenőrzését sem: ha unsafe kódban használsz
referenciát, azt a fordító továbbra is ellenőrzi. Az `unsafe` kulcsszó csak
ehhez az öt képességhez ad hozzáférést, amelyeket a fordító nem ellenőriz
memóriabiztonság szempontjából. Egy unsafe blokkon belül is kapsz tehát némi
biztonságot.

Ráadásul az `unsafe` nem jelenti azt, hogy a blokkban lévő kód szükségszerűen
veszélyes, vagy hogy biztosan memóriabiztonsági gondjai lesznek: a szándék az,
hogy programozóként te gondoskodj arról, hogy az `unsafe` blokkban lévő kód
érvényes módon férjen hozzá a memóriához.

Az emberek hibáznak, és a hibák elő fognak fordulni, de azzal, hogy ennek az öt
unsafe műveletnek `unsafe`-fel jelölt blokkokon belül kell lennie, tudni fogod,
hogy a memóriabiztonsághoz kapcsolódó hibák csakis egy `unsafe` blokkon belül
lehetnek. Tartsd kicsiben az `unsafe` blokkokat; hálás leszel érte később,
amikor memóriahibák után nyomozol.

Ahhoz, hogy az unsafe kódot a lehető legjobban elszigeteld, a legjobb, ha egy
biztonságos absztrakcióba zárod, és biztonságos API-t adsz hozzá; erről később
a fejezetben, az unsafe függvények és metódusok tárgyalásánál lesz szó. A
standard könyvtár egyes részei auditált unsafe kód fölé épített biztonságos
absztrakciók. Ha az unsafe kódot biztonságos absztrakcióba csomagolod, azzal
megakadályozod, hogy az `unsafe` használata kiszivárogjon mindazokra a
helyekre, ahol te vagy a felhasználóid az `unsafe` kóddal megvalósított
funkcionalitást használni szeretnétek, hiszen egy biztonságos absztrakció
használata biztonságos.

Nézzük meg sorban mind az öt unsafe szupererőt. Megvizsgálunk néhány olyan
absztrakciót is, amely biztonságos felületet ad unsafe kódhoz.

### Nyers pointer dereferálása

A 4. fejezet [„Dangling referenciák”][dangling-references]<!-- ignore --> című
szakaszában megemlítettük, hogy a fordító gondoskodik arról, hogy a
referenciák mindig érvényesek legyenek. Az unsafe Rustnak két új típusa van,
a _nyers pointerek_, amelyek hasonlítanak a referenciákra. A referenciákhoz
hasonlóan a nyers pointerek is lehetnek nem módosíthatók vagy módosíthatók, és
`*const T`, illetve `*mut T` alakban írjuk őket. A csillag itt nem a
dereferáló operátor, hanem a típusnév része. A nyers pointerek kontextusában a
_nem módosítható_ azt jelenti, hogy a pointernek dereferálás után nem lehet
közvetlenül értéket adni.

A referenciáktól és a smart pointerektől eltérően a nyers pointerek:

- Figyelmen kívül hagyhatják a borrowing szabályait: lehet egyszerre nem
  módosítható és módosítható pointer, vagy több módosítható pointer is ugyanarra
  a helyre
- Nem garantáltan mutatnak érvényes memóriára
- Lehetnek nullák
- Nem valósítanak meg semmilyen automatikus takarítást

Ha lemondasz arról, hogy a Rust kikényszerítse ezeket a garanciákat, a
garantált biztonságot cseréled nagyobb teljesítményre, vagy arra a képességre,
hogy egy másik nyelvvel vagy hardverrel dolgozz együtt, ahol a Rust garanciái
nem érvényesek.

A 20-1. lista mutatja, hogyan hozhatunk létre egy nem módosítható és egy
módosítható nyers pointert.

<Listing number="20-1" caption="Nyers pointerek létrehozása a nyers borrow operátorokkal">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy ebben a kódban nem szerepel az `unsafe` kulcsszó. Nyers
pointereket biztonságos kódban is létrehozhatunk; csak dereferálni nem tudjuk
őket unsafe blokkon kívül, ahogy azt mindjárt látni fogod.

A nyers pointereket a nyers borrow operátorokkal hoztuk létre: a `&raw const
num` egy `*const i32` típusú, nem módosítható nyers pointert hoz létre, a `&raw
mut num` pedig egy `*mut i32` típusú, módosíthatót. Mivel közvetlenül egy
lokális változóból hoztuk létre őket, tudjuk, hogy ezek a konkrét nyers
pointerek érvényesek, de ezt nem feltételezhetjük akármelyik nyers pointerről.

Hogy ezt bemutassuk, most olyan nyers pointert hozunk létre, amelynek az
érvényességében nem lehetünk ennyire biztosak: a nyers borrow operátor helyett
az `as` kulcsszóval alakítunk át egy értéket. A 20-2. lista azt mutatja,
hogyan hozhatunk létre nyers pointert egy tetszőleges memóriahelyre. A
tetszőleges memória használata nem definiált: lehet, hogy van adat azon a
címen, lehet, hogy nincs; a fordító optimalizálhatja úgy a kódot, hogy ne
történjen memóriahozzáférés; vagy a program leállhat egy szegmentálási hibával.
Általában nincs jó ok ilyen kód írására, különösen ott, ahol helyette nyers
borrow operátort is használhatnál, de lehetséges.

<Listing number="20-2" caption="Nyers pointer létrehozása tetszőleges memóriacímre">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Emlékezz: nyers pointereket biztonságos kódban is létrehozhatunk, de nem
dereferálhatjuk őket, és nem olvashatjuk ki a mutatott adatot. A 20-3. listában
a `*` dereferáló operátort használjuk egy nyers pointeren, ami `unsafe` blokkot
igényel.

<Listing number="20-3" caption="Nyers pointerek dereferálása `unsafe` blokkon belül">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Egy pointer létrehozása nem árt senkinek; csak akkor kerülhetünk érvénytelen
érték közelébe, amikor megpróbáljuk elérni azt az értéket, amelyre mutat.

Vedd észre azt is, hogy a 20-1. és a 20-3. listában olyan `*const i32` és `*mut
i32` nyers pointereket hoztunk létre, amelyek ugyanarra a memóriahelyre
mutattak, oda, ahol a `num` tárolódik. Ha ehelyett egy nem módosítható és egy
módosítható referenciát próbáltunk volna létrehozni a `num`-ra, a kód nem
fordult volna le, mert a Rust ownership-szabályai nem engednek meg egy
módosítható referenciát egyidejűleg bármilyen nem módosítható referenciával.
Nyers pointerekkel létrehozhatunk egy módosítható és egy nem módosítható
pointert ugyanarra a helyre, és a módosíthatón keresztül megváltoztathatjuk az
adatot, ami akár versenyhelyzethez is vezethet. Légy óvatos!

Ennyi veszély mellett miért használnál valaha is nyers pointert? Az egyik fő
felhasználási eset a C kóddal való együttműködés, ahogy a következő szakaszban
látni fogod. A másik eset az olyan biztonságos absztrakciók építése, amelyeket
a borrow checker nem ért. Bemutatjuk az unsafe függvényeket, majd megnézünk egy
példát egy unsafe kódot használó biztonságos absztrakcióra.

### Unsafe függvény vagy metódus hívása

A második típusú művelet, amelyet unsafe blokkban végezhetsz, az unsafe
függvények hívása. Az unsafe függvények és metódusok pontosan úgy néznek ki,
mint a szokásosak, csak a definíció többi része előtt szerepel egy `unsafe`. Az
`unsafe` kulcsszó ebben a kontextusban azt jelzi, hogy a függvénynek vannak
követelményei, amelyeket a híváskor be kell tartanunk, mert a Rust nem tudja
garantálni, hogy ezeket teljesítettük. Azzal, hogy egy unsafe függvényt
`unsafe` blokkon belül hívunk meg, azt mondjuk, hogy elolvastuk a függvény
dokumentációját, és vállaljuk a felelősséget a függvény szerződésének
betartásáért.

Íme egy `dangerous` nevű unsafe függvény, amelynek a törzse nem csinál semmit:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

A `dangerous` függvényt egy külön `unsafe` blokkon belül kell meghívnunk. Ha
`unsafe` blokk nélkül próbáljuk meghívni a `dangerous` függvényt, hibát kapunk:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Az `unsafe` blokkal azt állítjuk a Rustnak, hogy elolvastuk a függvény
dokumentációját, értjük, hogyan kell helyesen használni, és meggyőződtünk
arról, hogy teljesítjük a függvény szerződését.

Ahhoz, hogy egy `unsafe` függvény törzsében unsafe műveleteket végezz,
továbbra is `unsafe` blokkot kell használnod, éppúgy, mint egy szokásos
függvényen belül, és a fordító figyelmeztet, ha elfelejted. Ez segít abban,
hogy az `unsafe` blokkok a lehető legkisebbek maradjanak, hiszen unsafe
műveletekre nem feltétlenül van szükség a teljes függvénytörzsben.

#### Biztonságos absztrakció készítése unsafe kód fölé

Attól, hogy egy függvény unsafe kódot tartalmaz, még nem kell az egész
függvényt unsafe-nek jelölnünk. Sőt, az unsafe kód biztonságos függvénybe
csomagolása gyakori absztrakció. Példaként vizsgáljuk meg a standard könyvtár
`split_at_mut` függvényét, amelyhez unsafe kódra van szükség. Nézzük meg,
hogyan implementálhatnánk. Ezt a biztonságos metódust módosítható slice-okon
definiálják: egy slice-ot vesz át, és kettőt csinál belőle úgy, hogy az
argumentumként megadott indexnél kettévágja. A 20-4. lista mutatja a
`split_at_mut` használatát.

<Listing number="20-4" caption="A biztonságos `split_at_mut` függvény használata">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Ezt a függvényt nem tudjuk kizárólag safe Rusttal implementálni. Egy próbálkozás
körülbelül úgy nézhet ki, mint a 20-5. lista, amely nem fordul le. Az
egyszerűség kedvéért a `split_at_mut`-ot metódus helyett függvényként, és
generikus `T` típus helyett csak `i32` értékek slice-aira implementáljuk.

<Listing number="20-5" caption="Kísérlet a `split_at_mut` implementálására kizárólag safe Rusttal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Ez a függvény először lekéri a slice teljes hosszát. Ezután állítást tesz arra,
hogy a paraméterként kapott index a slice-on belül van, méghozzá úgy, hogy
ellenőrzi, kisebb-e vagy egyenlő-e a hossznál. Az állítás azt jelenti, hogy ha
a hossznál nagyobb indexet adunk át vágási pontnak, a függvény panicot vált ki,
mielőtt megpróbálná használni azt az indexet.

Ezután két módosítható slice-ot adunk vissza egy tuple-ben: az egyik az eredeti
slice elejétől a `mid` indexig tart, a másik a `mid`-től a slice végéig.

Amikor megpróbáljuk lefordítani a 20-5. listában lévő kódot, hibát kapunk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

A Rust borrow checkere nem tudja megérteni, hogy a slice különböző részeit
kölcsönözzük ki; csak annyit lát, hogy kétszer kölcsönzünk ugyanabból a
slice-ból. Egy slice különböző részeinek kölcsönzése alapvetően rendben van,
hiszen a két slice nem fed át, de a Rust nem elég okos ahhoz, hogy ezt tudja.
Amikor mi tudjuk, hogy a kód rendben van, a Rust viszont nem, akkor jött el az
unsafe kód ideje.

A 20-6. lista mutatja, hogyan használhatunk `unsafe` blokkot, nyers pointert és
néhány unsafe függvényhívást ahhoz, hogy a `split_at_mut` implementációja
működjön.

<Listing number="20-6" caption="Unsafe kód használata a `split_at_mut` függvény implementációjában">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Emlékezz vissza a 4. fejezet [„A slice típus”][the-slice-type]<!-- ignore -->
című szakaszára: a slice egy pointer valamilyen adatra, plusz a slice hossza. A
slice hosszát a `len` metódussal kapjuk meg, a slice nyers pointerét pedig az
`as_mut_ptr` metódussal érjük el. Ebben az esetben, mivel `i32` értékekre
mutató módosítható slice-unk van, az `as_mut_ptr` egy `*mut i32` típusú nyers
pointert ad vissza, amelyet a `ptr` változóban tárolunk.

Megtartjuk azt az állítást, hogy a `mid` index a slice-on belül van. Ezután
következik az unsafe kód: a `slice::from_raw_parts_mut` függvény egy nyers
pointert és egy hosszt vesz át, és létrehoz belőlük egy slice-ot. Ezzel a
függvénnyel hozunk létre egy olyan slice-ot, amely a `ptr`-től indul, és `mid`
elem hosszú. Ezután meghívjuk a `ptr`-en az `add` metódust `mid` argumentummal,
hogy kapjunk egy `mid`-nél kezdődő nyers pointert, majd ezzel a pointerrel és a
`mid` utáni elemek számával mint hosszal létrehozzuk a másik slice-ot.

A `slice::from_raw_parts_mut` függvény unsafe, mert nyers pointert vesz át, és
meg kell bíznia abban, hogy ez a pointer érvényes. A nyers pointerek `add`
metódusa szintén unsafe, mert meg kell bíznia abban, hogy az eltolt hely is
érvényes pointer. Ezért az `unsafe` blokkot a `slice::from_raw_parts_mut` és az
`add` hívásai köré kellett tennünk, hogy meghívhassuk őket. A kód
átnézésével, és azzal az állítással, hogy a `mid`-nek kisebbnek vagy egyenlőnek
kell lennie a `len`-nél, meg tudjuk állapítani, hogy az `unsafe` blokkban
használt összes nyers pointer a slice-on belüli adatra mutató, érvényes pointer
lesz. Ez az `unsafe` elfogadható és helyénvaló használata.

Vedd észre, hogy az így kapott `split_at_mut` függvényt nem kell `unsafe`-nek
jelölnünk, és safe Rustból is meghívhatjuk. Biztonságos absztrakciót
készítettünk az unsafe kód fölé a függvény olyan implementációjával, amely
biztonságos módon használ `unsafe` kódot, hiszen csakis érvényes pointereket
hoz létre abból az adatból, amelyhez a függvény hozzáfér.

Ezzel szemben a `slice::from_raw_parts_mut` 20-7. listában látható használata
nagy valószínűséggel összeomlana a slice használatakor. Ez a kód egy
tetszőleges memóriahelyet vesz, és 10 000 elem hosszú slice-ot hoz létre
belőle.

<Listing number="20-7" caption="Slice létrehozása tetszőleges memóriahelyről">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Nem mi birtokoljuk a memóriát ezen a tetszőleges helyen, és semmi sem
garantálja, hogy az itt létrehozott slice érvényes `i32` értékeket tartalmaz.
Ha a `values`-t úgy próbáljuk használni, mintha érvényes slice lenne, az nem
definiált viselkedéshez vezet.

#### Külső kód hívása `extern` függvényekkel

Néha a Rust kódodnak más nyelven írt kóddal kell együttműködnie. Ehhez a
Rustnak van egy `extern` kulcsszava, amely megkönnyíti egy _Foreign Function
Interface (FFI)_ létrehozását és használatát; ez az a mód, ahogyan egy
programozási nyelv függvényeket definiálhat, és lehetővé teheti, hogy egy másik
(idegen) programozási nyelv meghívja ezeket a függvényeket.

A 20-8. lista bemutatja, hogyan állíthatunk be integrációt a C standard
könyvtárának `abs` függvényével. Az `extern` blokkokban deklarált függvények
Rust kódból általában unsafe módon hívhatók, ezért az `extern` blokkokat is
`unsafe`-nek kell jelölni. Ennek oka, hogy más nyelvek nem kényszerítik ki a
Rust szabályait és garanciáit, a Rust pedig nem tudja ellenőrizni őket, így a
biztonság szavatolása a programozó felelőssége.

<Listing number="20-8" file-name="src/main.rs" caption="Egy másik nyelvben definiált `extern` függvény deklarálása és hívása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Az `unsafe extern "C"` blokkon belül felsoroljuk azoknak a másik nyelvből
származó külső függvényeknek a nevét és szignatúráját, amelyeket meg akarunk
hívni. A `"C"` rész azt adja meg, melyik _application binary interface-t (ABI)_
használja a külső függvény: az ABI határozza meg, hogyan kell a függvényt
assembly szinten meghívni. A `"C"` ABI a leggyakoribb, és a C programozási
nyelv ABI-ját követi. A Rust által támogatott összes ABI-ról [a Rust
referenciájában][ABI] találsz információt.

Az `unsafe extern` blokkban deklarált minden elem implicit módon unsafe.
Néhány FFI-függvény azonban *biztonságosan* hívható. Például a C standard
könyvtárának `abs` függvényénél nincsenek memóriabiztonsági megfontolások, és
tudjuk, hogy bármilyen `i32` értékkel meghívható. Ilyen esetekben a `safe`
kulcsszóval jelezhetjük, hogy ez a konkrét függvény biztonságosan hívható, még
ha `unsafe extern` blokkban van is. Ha ezt a változtatást megtesszük, a hívása
többé nem igényel `unsafe` blokkot, ahogy a 20-9. listában látható.

<Listing number="20-9" file-name="src/main.rs" caption="Egy függvény kifejezett `safe` jelölése `unsafe extern` blokkon belül, majd biztonságos hívása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Attól, hogy egy függvényt `safe`-nek jelölsz, az még önmagában nem lesz
biztonságos! Ez inkább egy ígéret, amelyet a Rustnak teszel, hogy az adott
függvény biztonságos. Az továbbra is a te felelősséged, hogy ez az ígéret
teljesüljön is!

#### Rust függvények hívása más nyelvekből

Az `extern`-t arra is használhatjuk, hogy olyan felületet hozzunk létre, amely
lehetővé teszi más nyelvek számára Rust függvények hívását. Egész `extern`
blokk létrehozása helyett közvetlenül az adott függvény `fn` kulcsszava elé
írjuk az `extern` kulcsszót, és megadjuk a használandó ABI-t. Egy
`#[unsafe(no_mangle)]` annotációt is hozzá kell adnunk, amellyel megmondjuk a
Rust fordítójának, hogy ne torzítsa el ennek a függvénynek a nevét. A
_névtorzításról (mangling)_ akkor beszélünk, amikor a fordító a függvénynek
adott nevet egy másik névre cseréli, amely több információt tartalmaz a
fordítási folyamat többi része számára, de kevésbé olvasható ember számára.
Minden programozási nyelv fordítója kicsit másképp torzítja a neveket, ezért
ahhoz, hogy egy Rust függvényt más nyelvek néven tudjanak szólítani, ki kell
kapcsolnunk a Rust fordítójának névtorzítását. Ez unsafe, mert a beépített
torzítás nélkül a könyvtárak között névütközések lehetnek, így a mi
felelősségünk, hogy a választott név torzítás nélkül is biztonságosan
exportálható legyen.

A következő példában a `call_from_c` függvényt tesszük elérhetővé C kód
számára, miután megosztott könyvtárrá fordítottuk és C-ből belinkeltük:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Az `extern` ilyen használatához csak az attribútumban van szükség `unsafe`-re,
magán az `extern` blokkon nem.

### Módosítható statikus változó elérése vagy módosítása

Ebben a könyvben eddig nem beszéltünk a globális változókról, amelyeket a Rust
támogat ugyan, de amelyek problémásak lehetnek a Rust ownership-szabályai
mellett. Ha két szál ugyanahhoz a módosítható globális változóhoz fér hozzá, az
versenyhelyzetet okozhat.

A Rustban a globális változókat _statikus_ (static) változóknak hívjuk. A
20-10. lista egy statikus változó deklarálására és használatára mutat példát,
ahol az érték egy string slice.

<Listing number="20-10" file-name="src/main.rs" caption="Nem módosítható statikus változó definiálása és használata">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

A statikus változók hasonlítanak a konstansokra, amelyekről a 3. fejezet
[„Konstansok deklarálása”][constants]<!-- ignore --> című szakaszában
beszéltünk. A statikus változók nevét megállapodás szerint
`SCREAMING_SNAKE_CASE` alakban írjuk. A statikus változók csak `'static`
lifetime-mal rendelkező referenciákat tárolhatnak, ami azt jelenti, hogy a Rust
fordítója ki tudja következtetni a lifetime-ot, és nem kell kifejezetten
annotálnunk. Egy nem módosítható statikus változó elérése biztonságos.

A konstansok és a nem módosítható statikus változók között finom különbség,
hogy a statikus változóban lévő értéknek rögzített címe van a memóriában. Az
érték használata mindig ugyanahhoz az adathoz fér hozzá. A konstansok ezzel
szemben minden használatkor duplikálhatják az adatukat. További különbség, hogy
a statikus változók lehetnek módosíthatók. A módosítható statikus változók
elérése és módosítása _unsafe_. A 20-11. lista azt mutatja, hogyan lehet egy
`COUNTER` nevű módosítható statikus változót deklarálni, elérni és módosítani.

<Listing number="20-11" file-name="src/main.rs" caption="Módosítható statikus változó olvasása vagy írása unsafe művelet.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

A szokásos változókhoz hasonlóan a módosíthatóságot a `mut` kulcsszóval adjuk
meg. Minden kódnak, amely a `COUNTER`-ből olvas vagy abba ír, `unsafe` blokkon
belül kell lennie. A 20-11. listában lévő kód lefordul, és a várt módon
`COUNTER: 3`-at ír ki, mert egyszálú. Ha több szál férne hozzá a `COUNTER`-hez,
az nagy valószínűséggel versenyhelyzethez vezetne, tehát nem definiált
viselkedés lenne. Ezért az egész függvényt `unsafe`-nek kell jelölnünk, és
dokumentálnunk kell a biztonsági korlátozást, hogy aki meghívja a függvényt,
tudja, mit tehet és mit nem biztonságosan.

Amikor unsafe függvényt írunk, idiomatikus egy `SAFETY` szóval kezdődő
kommentet írni, amely elmagyarázza, mit kell tennie a hívónak ahhoz, hogy
biztonságosan hívja meg a függvényt. Hasonlóképp, amikor unsafe műveletet
végzünk, idiomatikus egy `SAFETY` szóval kezdődő kommentet írni arról, hogyan
teljesülnek a biztonsági szabályok.

Ezenfelül a fordító alapértelmezés szerint egy fordítói lint segítségével
elutasít minden olyan kísérletet, amely módosítható statikus változóra
referenciát hozna létre. Vagy kifejezetten le kell mondanod ennek a lintnek a
védelméről egy `#[allow(static_mut_refs)]` annotációval, vagy a valamelyik
nyers borrow operátorral létrehozott nyers pointeren keresztül kell elérned a
módosítható statikus változót. Ez azokra az esetekre is vonatkozik, amikor a
referencia láthatatlanul jön létre, például amikor a `println!` használja ebben
a kódlistában. Az, hogy a módosítható statikus változókra mutató referenciákat
nyers pointereken keresztül kell létrehozni, segít nyilvánvalóbbá tenni a
használatukhoz tartozó biztonsági követelményeket.

Globálisan elérhető, módosítható adat mellett nehéz biztosítani, hogy ne
legyenek versenyhelyzetek; ezért tekinti a Rust a módosítható statikus
változókat unsafe-nek. Ahol lehet, érdemesebb a 16. fejezetben tárgyalt
konkurenciakezelési technikákat és szálbiztos smart pointereket használni, hogy
a fordító ellenőrizze: a különböző szálakból történő adathozzáférés
biztonságosan zajlik.

### Unsafe trait implementálása

Az `unsafe` használható unsafe trait implementálására is. Egy trait akkor
unsafe, ha legalább az egyik metódusának van olyan invariánsa, amelyet a
fordító nem tud ellenőrizni. Egy traitet úgy nyilvánítunk `unsafe`-nek, hogy a
`trait` elé írjuk az `unsafe` kulcsszót, és a trait implementációját is
`unsafe`-nek jelöljük, ahogy a 20-12. listában látható.

<Listing number="20-12" caption="Unsafe trait definiálása és implementálása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Az `unsafe impl` használatával megígérjük, hogy betartjuk azokat az
invariánsokat, amelyeket a fordító nem tud ellenőrizni.

Példaként emlékezz vissza a `Send` és `Sync` jelölő trait-ekre, amelyekről a
16. fejezet [„Bővíthető konkurencia a `Send` és a `Sync`
segítségével”][send-and-sync]<!-- ignore --> című szakaszában beszéltünk: a
fordító automatikusan implementálja ezeket a trait-eket, ha a típusaink
kizárólag olyan más típusokból állnak, amelyek implementálják a `Send`-et és a
`Sync`-et. Ha olyan típust implementálunk, amely tartalmaz egy `Send`-et vagy
`Sync`-et nem implementáló típust, például nyers pointereket, és ezt a típust
`Send`-nek vagy `Sync`-nek szeretnénk jelölni, akkor `unsafe`-et kell
használnunk. A Rust nem tudja ellenőrizni, hogy a típusunk teljesíti-e azokat a
garanciákat, amelyek szerint biztonságosan átküldhető szálak között vagy több
szálból is elérhető; ezért ezeket az ellenőrzéseket nekünk kell kézzel
elvégeznünk, és ezt `unsafe`-fel jeleznünk.

### Union mezőinek elérése

Az utolsó művelet, amely csak `unsafe`-fel működik, egy union mezőinek elérése.
A *union* hasonlít a `struct`-ra, azzal a különbséggel, hogy egy adott
példányban egyszerre csak egy deklarált mezőt használunk. A unionokat
elsősorban arra használjuk, hogy C kódban lévő unionokkal működjünk együtt. A
union mezőinek elérése unsafe, mert a Rust nem tudja garantálni, hogy éppen
milyen típusú adat van tárolva a union példányában. A unionokról többet [a Rust
referenciájában][unions] tudhatsz meg.

### A Miri használata unsafe kód ellenőrzésére

Amikor unsafe kódot írsz, érdemes ellenőrizned, hogy amit írtál, valóban
biztonságos és helyes-e. Ennek az egyik legjobb módja a Miri használata, amely
a Rust hivatalos eszköze a nem definiált viselkedés felderítésére. Míg a borrow
checker _statikus_ eszköz, amely fordítási időben dolgozik, a Miri _dinamikus_
eszköz, amely futásidőben működik. Úgy ellenőrzi a kódodat, hogy lefuttatja a
programodat vagy a tesztkészletét, és észleli, ha megsérted azokat a
szabályokat, amelyeket a Rust működéséről ismer.

A Miri használatához a Rust nightly buildjére van szükség (erről bővebben a
[G. függelékben: Hogyan készül a Rust, és a „Nightly Rust”][nightly]<!-- ignore
--> olvashatsz). A Rust nightly verzióját és a Miri eszközt is telepítheted a
`rustup +nightly component add miri` beírásával. Ez nem változtatja meg, hogy a
projekted melyik Rust-verziót használja; csak hozzáadja az eszközt a
rendszeredhez, hogy használhasd, amikor akarod. A Mirit egy projekten a `cargo
+nightly miri run` vagy a `cargo +nightly miri test` beírásával futtathatod.

Hogy lásd, mennyire hasznos tud lenni, nézzük meg, mi történik, amikor a 20-7.
listára futtatjuk.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

A Miri helyesen figyelmeztet arra, hogy egész számot alakítunk pointerré, ami
gond lehet, de a Miri nem tudja eldönteni, hogy tényleg gond van-e, mert nem
tudja, honnan származik a pointer. Ezután a Miri hibát jelez, mert a 20-7.
listában nem definiált viselkedés van: dangling pointerünk van. A Mirinek
köszönhetően most már tudjuk, hogy fennáll a nem definiált viselkedés
kockázata, és elgondolkodhatunk azon, hogyan tegyük biztonságossá a kódot.
Egyes esetekben a Miri még javaslatot is tud tenni a hibák javítására.

A Miri nem kap el mindent, amit unsafe kód írásakor elronthatsz. A Miri
dinamikus analízist végző eszköz, így csak azzal a kóddal kapcsolatos
problémákat találja meg, amely ténylegesen lefut. Ez azt jelenti, hogy jó
tesztelési technikákkal együtt kell használnod, hogy magabiztosabb legyél az
általad írt unsafe kódban. A Miri arra sem terjed ki, ahogyan a kódod
mindenféle módon helytelenné (unsound) válhat.

Másképp fogalmazva: ha a Miri _talál_ egy problémát, akkor tudod, hogy van egy
bug; de attól, hogy a Miri _nem_ talál bugot, még lehet, hogy van probléma.
Azért sokat el tud kapni. Próbáld ki a fejezet többi unsafe kódpéldáján is, és
nézd meg, mit mond!

A Miriről többet [a GitHub-repójában][miri] tudhatsz meg.

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Az unsafe kód helyes használata

Az `unsafe` használata az imént tárgyalt öt szupererő valamelyikéhez nem hiba,
és nem is nézik rossz szemmel, de nehezebb az `unsafe` kódot helyesen megírni,
mert a fordító nem tud segíteni a memóriabiztonság betartásában. Ha okod van
`unsafe` kód használatára, használd; a kifejezett `unsafe` annotáció pedig
megkönnyíti a problémák forrásának megtalálását, amikor előfordulnak. Amikor
unsafe kódot írsz, a Mirivel növelheted a magabiztosságodat abban, hogy a
megírt kód betartja a Rust szabályait.

Ha sokkal mélyebben szeretnél elmerülni abban, hogyan lehet hatékonyan dolgozni
az unsafe Rusttal, olvasd el a Rust hivatalos `unsafe`-útmutatóját, [a
Rustonomicont][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
