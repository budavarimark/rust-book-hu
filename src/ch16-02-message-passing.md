<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Adatátvitel szálak között üzenetküldéssel

A biztonságos konkurencia egyik egyre népszerűbb megközelítése az üzenetküldés,
amelyben a szálak vagy aktorok úgy kommunikálnak, hogy adatot tartalmazó
üzeneteket küldenek egymásnak. Az alapgondolatot [a Go nyelv dokumentációjának](https://golang.org/doc/effective_go.html#concurrency)
jelmondata így fogalmazza meg: „Ne memóriamegosztással kommunikálj; ehelyett
kommunikációval oszd meg a memóriát.”

Az üzenetküldésen alapuló konkurenciához a Rust standard könyvtára ad egy
csatorna-implementációt. A _csatorna_ általános programozási fogalom, amellyel
adatot küldünk az egyik szálról a másikra.

A programozásbeli csatornát elképzelheted úgy, mint egy irányított vízi utat,
például egy patakot vagy folyót. Ha beledobsz valamit, mondjuk egy gumikacsát a
folyóba, az sodródni fog lefelé, egészen a vízi út végéig.

A csatornának két fele van: egy adó és egy fogadó. Az adó fele az a folyásirány
szerint feljebb lévő hely, ahol a gumikacsát a folyóba teszed, a fogadó fele
pedig az, ahol a gumikacsa lejjebb kiköt. A kódod egyik része metódusokat hív
az adón azzal az adattal, amit el akarsz küldeni, egy másik része pedig a fogadó
végén figyeli a beérkező üzeneteket. Egy csatornát _lezártnak_ nevezünk, ha az
adó vagy a fogadó fele eldobásra kerül.

Itt fokozatosan eljutunk egy olyan programig, amelyben az egyik szál értékeket
állít elő, és leküldi őket egy csatornán, egy másik szál pedig fogadja és
kiírja ezeket az értékeket. Egyszerű értékeket fogunk küldeni a szálak között
egy csatornán keresztül, hogy szemléltessük a képességet. Ha egyszer
elsajátítottad a technikát, csatornákat használhatsz bármely egymással
kommunikálni akaró szálhoz, például egy chatrendszerhez, vagy egy olyan
rendszerhez, ahol sok szál végzi egy számítás egy-egy részét, és küldi el a
részeredményeket egyetlen szálnak, amely összesíti őket.

Először, a 16-6. listában létrehozunk egy csatornát, de nem kezdünk vele semmit.
Vedd észre, hogy ez egyelőre nem fordul le, mert a Rust nem tudja megállapítani,
milyen típusú értékeket akarunk a csatornán küldeni.

<Listing number="16-6" file-name="src/main.rs" caption="Csatorna létrehozása és a két felének hozzárendelése a `tx` és `rx` változókhoz">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Új csatornát az `mpsc::channel` függvénnyel hozunk létre; az `mpsc` a _multiple
producer, single consumer_ („több termelő, egy fogyasztó”) rövidítése. Röviden:
a Rust standard könyvtárának csatorna-implementációja miatt egy csatornának több
_küldő_ vége lehet, amelyek értékeket állítanak elő, de csak egyetlen _fogadó_
vége, amely ezeket az értékeket elfogyasztja. Képzelj el több patakot, amelyek
egyetlen nagy folyóba ömlenek: minden, amit bármelyik patakon leküldesz, a végén
ugyanabban a folyóban köt ki. Egyelőre egyetlen termelővel kezdünk, de amint ez
a példa működik, hozzáadunk több termelőt is.

Az `mpsc::channel` függvény egy tuple-t ad vissza, amelynek első eleme a küldő
vég – az adó –, második eleme pedig a fogadó vég – a fogadó. A `tx` és `rx`
rövidítéseket hagyományosan sok területen használják a _transmitter_ (adó),
illetve a _receiver_ (fogadó) jelölésére, ezért mi is így nevezzük el a
változóinkat, hogy jelezzük, melyik vég melyik. Egy `let` utasítást használunk
olyan mintával, amely szétbontja a tuple-t; a `let` utasításokban használt
mintákról és a szétbontásról a 19. fejezetben lesz szó. Egyelőre elég annyi,
hogy a `let` utasítás ilyen használata kényelmes módja az `mpsc::channel` által
visszaadott tuple darabjainak kinyerésére.

Mozgassuk át az adó véget egy elindított szálba, és küldessünk vele egy
sztringet, hogy az elindított szál kommunikáljon a fő szállal, ahogy a 16-7.
listában látható. Ez olyan, mintha a gumikacsát a folyó felső szakaszán a vízbe
tennénk, vagy chatüzenetet küldenénk az egyik szálról a másikra.

<Listing number="16-7" file-name="src/main.rs" caption='A `tx` átmozgatása egy elindított szálba és a `"hi"` elküldése'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Ismét a `thread::spawn`-t használjuk egy új szál létrehozásához, majd a `move`
segítségével bemozgatjuk a `tx`-et a closure-be, hogy az elindított szál
birtokolja a `tx`-et. Az elindított szálnak birtokolnia kell az adót ahhoz, hogy
üzeneteket tudjon küldeni a csatornán.

Az adónak van egy `send` metódusa, amely az elküldeni kívánt értéket veszi át. A
`send` metódus `Result<T, E>` típussal tér vissza, tehát ha a fogadót már
eldobták, és nincs hova küldeni az értéket, a küldési művelet hibát ad vissza.
Ebben a példában az `unwrap` hívással váltunk ki panicot hiba esetén. Egy valódi
alkalmazásban azonban rendesen kezelnénk: térj vissza a 9. fejezethez a
megfelelő hibakezelési stratégiák átnézéséhez.

A 16-8. listában a fő szálon vesszük át az értéket a fogadótól. Ez olyan, mintha
a folyó végén kihalásznánk a gumikacsát a vízből, vagy fogadnánk egy
chatüzenetet.

<Listing number="16-8" file-name="src/main.rs" caption='A `"hi"` érték fogadása a fő szálon és kiírása'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

A fogadónak két hasznos metódusa van: a `recv` és a `try_recv`. Mi a `recv`-et
használjuk, amely a _receive_ rövidítése; ez blokkolja a fő szál futását, és
megvárja, amíg egy érték megérkezik a csatornán. Amint egy értéket elküldenek, a
`recv` egy `Result<T, E>`-ben adja vissza. Amikor az adó lezárul, a `recv` hibát
ad vissza jelezve, hogy több érték nem fog érkezni.

A `try_recv` metódus nem blokkol, hanem azonnal visszaad egy `Result<T, E>`-t:
egy `Ok` értéket, amely az üzenetet tartalmazza, ha van elérhető, vagy egy `Err`
értéket, ha ezúttal nincs üzenet. A `try_recv` akkor hasznos, ha a szálnak más
dolga is van, miközben üzenetekre vár: írhatnánk egy ciklust, amely időnként
meghívja a `try_recv`-et, kezeli az üzenetet, ha van, egyébként pedig egy kis
ideig mást csinál, mielőtt újra ellenőrizné.

Ebben a példában az egyszerűség kedvéért a `recv`-et használtuk; a fő szálnak
nincs más dolga azon kívül, hogy üzenetekre várjon, így a fő szál blokkolása itt
helyénvaló.

Amikor lefuttatjuk a 16-8. lista kódját, látni fogjuk az értéket kiírva a fő
szálról:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Tökéletes!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Ownership átadása csatornákon keresztül

Az ownership-szabályok létfontosságú szerepet játszanak az üzenetküldésben, mert
segítenek biztonságos, konkurens kódot írni. A konkurens programozás hibáinak
megelőzése az az előny, amit abból nyerünk, hogy a Rust programjaink során végig
az ownershipben gondolkodunk. Végezzünk egy kísérletet, amely megmutatja, hogyan
működik együtt a csatorna és az ownership a problémák megelőzésében: megpróbáljuk
használni a `val` értéket az elindított szálban _azután_, hogy már leküldtük a
csatornán. Próbáld lefordítani a 16-9. lista kódját, hogy lásd, miért nem
megengedett ez a kód.

<Listing number="16-9" file-name="src/main.rs" caption="Kísérlet a `val` használatára azután, hogy leküldtük a csatornán">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Itt megpróbáljuk kiírni a `val`-t azután, hogy a `tx.send` hívással már
leküldtük a csatornán. Ezt megengedni rossz ötlet lenne: ha egyszer az értéket
elküldtük egy másik szálnak, az a szál módosíthatja vagy eldobhatja, mielőtt mi
újra használni próbálnánk. A másik szál módosításai a nem konzisztens vagy nem
létező adat miatt hibákat vagy váratlan eredményeket okozhatnának. A Rust
azonban hibát ad, ha megpróbáljuk lefordítani a 16-9. lista kódját:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

A konkurenciával kapcsolatos hibánk fordítási idejű hibát okozott. A `send`
függvény átveszi a paramétere ownershipjét, és amikor az érték átmozog, a fogadó
veszi át az ownershipjét. Ez megakadályozza, hogy véletlenül újra használjuk az
értéket a küldés után; az ownership-rendszer ellenőrzi, hogy minden rendben
van-e.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Több érték küldése

A 16-8. lista kódja lefordult és lefutott, de nem mutatta meg világosan, hogy
két külön szál beszélgetett egymással a csatornán keresztül.

A 16-10. listában olyan módosításokat végeztünk, amelyek bizonyítják, hogy a
16-8. lista kódja konkurensen fut: az elindított szál mostantól több üzenetet
küld, és minden üzenet között tart egy másodperc szünetet.

<Listing number="16-10" file-name="src/main.rs" caption="Több üzenet küldése, közöttük szünetekkel">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Ezúttal az elindított szálnak van egy sztringekből álló vektora, amelyet el
akarunk küldeni a fő szálnak. Végigiterálunk rajtuk, egyenként elküldjük őket,
és mindegyik között szünetet tartunk a `thread::sleep` függvény hívásával, egy
egy másodperces `Duration` értékkel.

A fő szálon már nem hívjuk meg explicit módon a `recv` függvényt: ehelyett úgy
kezeljük az `rx`-et, mint egy iterátort. Minden fogadott értéket kiírunk. Amikor
a csatorna lezárul, az iteráció véget ér.

Amikor lefuttatod a 16-10. lista kódját, a következő kimenetet kell látnod, a
sorok között egy-egy másodperces szünettel:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Mivel a fő szál `for` ciklusában nincs semmilyen szüneteltető vagy késleltető
kód, ebből tudhatjuk, hogy a fő szál vár az elindított száltól érkező értékekre.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Több termelő létrehozása

Korábban említettük, hogy az `mpsc` a _multiple producer, single consumer_
rövidítése. Vegyük hasznát az `mpsc`-nek, és bővítsük ki a 16-10. lista kódját
úgy, hogy több szálat hozzunk létre, amelyek mind ugyanannak a fogadónak küldenek
értékeket. Ezt az adó klónozásával tehetjük meg, ahogy a 16-11. listában
látható.

<Listing number="16-11" file-name="src/main.rs" caption="Több üzenet küldése több termelőtől">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Ezúttal az első elindított szál létrehozása előtt meghívjuk a `clone`-t az adón.
Ez ad nekünk egy új adót, amelyet átadhatunk az első elindított szálnak. Az
eredeti adót egy második elindított szálnak adjuk át. Így két szálunk lesz,
amelyek különböző üzeneteket küldenek az egyetlen fogadónak.

Amikor lefuttatod a kódot, a kimenet nagyjából így fog kinézni:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Elképzelhető, hogy az értékeket más sorrendben látod, a rendszeredtől függően.
Ez az, ami a konkurenciát egyszerre érdekessé és nehézzé teszi. Ha kísérletezel
a `thread::sleep`-pel, és különböző értékeket adsz neki a különböző szálakban,
minden futás nemdeterminisztikusabb lesz, és minden alkalommal más kimenetet
hoz létre.

Most, hogy megnéztük, hogyan működnek a csatornák, nézzünk meg egy másik
konkurenciakezelési módszert.
