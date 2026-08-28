## Tegyük össze: future-ök, taskok és szálak

Ahogy a [16. fejezetben][ch16]<!-- ignore --> láttuk, a szálak egyfajta
megközelítést kínálnak a konkurenciához. Ebben a fejezetben egy másik
megközelítést láttunk: az async használatát future-ökkel és stream-ekkel. Ha
azon töprengsz, mikor melyiket válaszd, a válasz: attól függ! És sok esetben
nem is szálak _vagy_ async a kérdés, hanem szálak _és_ async.

Sok operációs rendszer már évtizedek óta kínál szálalapú konkurenciamodelleket,
és ennek megfelelően sok programozási nyelv is támogatja őket. Ezeknek a
modelleknek azonban megvannak a maguk kompromisszumai. Számos operációs
rendszeren minden szál elég sok memóriát használ. A szálak ráadásul csak akkor
jöhetnek szóba, ha az operációs rendszered és a hardvered támogatja őket. A
mainstream asztali és mobil számítógépekkel ellentétben egyes beágyazott
rendszereken egyáltalán nincs operációs rendszer, tehát szálak sincsenek.

Az async modell másfajta – és végső soron kiegészítő – kompromisszumokat kínál.
Az async modellben a konkurens műveleteknek nincs szükségük saját szálra.
Helyette taskokon futhatnak, ahogy akkor is, amikor a stream-ekről szóló
szakaszban a `trpl::spawn_task` hívással indítottunk el munkát egy szinkron
függvényből. A task hasonlít a szálhoz, de nem az operációs rendszer kezeli,
hanem könyvtári szintű kód: a runtime.

Nem véletlen, hogy a szálak és a taskok indítására szolgáló API-k ennyire
hasonlítanak egymásra. A szálak határt húznak szinkron műveletek csoportjai
köré; a konkurencia a szálak _között_ lehetséges. A taskok _aszinkron_
műveletek csoportjai köré húznak határt; a konkurencia a taskok _között_ és a
taskokon _belül_ is lehetséges, mert egy task válthat a törzsében lévő
future-ök között. Végül a future-ök a Rust legfinomabb szemcsézettségű
konkurencia-egységei, és minden future future-ök egész fáját képviselheti. A
runtime – pontosabban annak executora – a taskokat kezeli, a taskok pedig a
future-öket. Ilyen értelemben a taskok könnyűsúlyú, runtime által kezelt
szálakhoz hasonlítanak, kiegészítve azokkal a képességekkel, amelyek abból
fakadnak, hogy nem az operációs rendszer, hanem egy runtime kezeli őket.

Ez nem jelenti azt, hogy az async taskok mindig jobbak a szálaknál (vagy
fordítva). A szálakkal megvalósított konkurencia bizonyos szempontból
egyszerűbb programozási modell, mint az `async`-kal megvalósított. Ez lehet erő
és gyengeség is. A szálak némileg „elindítod és elfelejted” jellegűek; nincs
natív megfelelőjük a future-re, így egyszerűen befejezésig futnak, és csak maga
az operációs rendszer szakítja meg őket.

Kiderül továbbá, hogy a szálak és a taskok gyakran nagyon jól működnek együtt,
mert a taskok (legalábbis egyes runtime-okban) mozgathatók a szálak között.
Sőt, a motorháztető alatt az általunk használt runtime – beleértve a
`spawn_blocking` és a `spawn_task` függvényt is – alapértelmezés szerint
többszálú! Sok runtime a _work stealing_ (munkalopás) nevű megközelítést
használja arra, hogy a szálak aktuális kihasználtsága alapján átlátszó módon
mozgassa a taskokat a szálak között, javítva ezzel a rendszer
összteljesítményét. Ehhez a megközelítéshez valójában szálak _és_ taskok,
tehát future-ök is kellenek.

Amikor azon gondolkodsz, mikor melyik módszert használd, vedd figyelembe ezeket
az ökölszabályokat:

- Ha a munka _jól párhuzamosítható_ (vagyis CPU-igényes), például egy csomó
  adatot kell feldolgozni úgy, hogy minden rész külön feldolgozható, akkor a
  szálak a jobb választás.
- Ha a munka _erősen konkurens_ (vagyis I/O-igényes), például egy csomó
  különböző forrásból érkező üzenetet kell kezelni, amelyek eltérő időközönként
  vagy eltérő ütemben érkezhetnek, akkor az async a jobb választás.

És ha egyszerre van szükséged párhuzamosságra és konkurenciára, nem kell
választanod a szálak és az async között. Szabadon használhatod őket együtt,
hagyva, hogy mindegyik azt a szerepet töltse be, amelyben a legjobb. A 17-25.
lista például egy elég gyakori példát mutat az ilyen keverésre a valós Rust
kódban.

<Listing number="17-25" caption="Üzenetek küldése blokkoló kóddal egy szálban, és az üzenetek bevárása egy async blokkban" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Először létrehozunk egy async csatornát, majd indítunk egy szálat, amely a
`move` kulcsszóval átveszi a csatorna küldő oldalának ownershipjét. A szálon
belül elküldjük az 1-től 10-ig terjedő számokat, és mindegyik között alszunk egy
másodpercet. Végül lefuttatunk egy future-t, amelyet a `trpl::block_on`-nak
átadott async blokkból hoztunk létre, ahogy a fejezet során végig tettük. Ebben
a future-ben bevárjuk ezeket az üzeneteket, akárcsak a többi, üzenetküldéssel
kapcsolatos példában, amelyet láttunk.

Visszatérve a fejezet elején felvázolt forgatókönyvhöz, képzeld el, hogy egy
csomó videokódolási feladatot futtatsz egy dedikált szálon (mert a videokódolás
számításigényes), de egy async csatornán értesíted a felhasználói felületet,
hogy ezek a műveletek elkészültek. Az ilyen kombinációkra számtalan példa akad a
valós felhasználási esetekben.

## Összefoglalás

Nem ez az utolsó alkalom, hogy konkurenciával találkozol ebben a könyvben. A
[21. fejezet][ch21]<!-- ignore --> projektje az itt tárgyalt egyszerűbb
példáknál valósághűbb helyzetben alkalmazza ezeket a fogalmakat, és
közvetlenebbül hasonlítja össze a szálakkal, illetve a taskokkal és future-ökkel
való problémamegoldást.

Bármelyik megközelítést választod is, a Rust megadja a szükséges eszközöket
ahhoz, hogy biztonságos, gyors, konkurens kódot írj – akár egy nagy
átbocsátóképességű webszerverhez, akár egy beágyazott operációs rendszerhez.

Ezután arról lesz szó, hogyan modellezhetsz problémákat és hogyan
strukturálhatsz megoldásokat idiomatikus módon, ahogy a Rust programjaid egyre
nagyobbak lesznek. Emellett megbeszéljük, hogyan viszonyulnak a Rust idiómái
azokhoz, amelyeket az objektumorientált programozásból ismerhetsz.

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
