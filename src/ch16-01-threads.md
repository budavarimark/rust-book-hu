## Szálak használata kód egyidejű futtatására

A legtöbb mai operációs rendszerben egy futtatott program kódja egy
_folyamatban_ (process) fut, és az operációs rendszer egyszerre több folyamatot
kezel. Egy programon belül is lehetnek egymástól független részek, amelyek
egyszerre futnak. Az ezeket a független részeket futtató elemeket _szálaknak_
nevezzük. Egy webszervernek például több szála is lehet, hogy egyszerre több
kérésre is válaszolni tudjon.

Ha a programod számításait több szálra osztod, hogy egyszerre több feladat
fusson, azzal javíthatod a teljesítményt, de bonyolultságot is viszel a
rendszerbe. Mivel a szálak egyidejűleg futnak, semmi nem garantálja eleve, hogy
a kódod különböző szálakon futó részei milyen sorrendben hajtódnak végre. Ez
problémákhoz vezethet, például:

- Versenyhelyzetek, amelyekben a szálak inkonzisztens sorrendben férnek hozzá
  adatokhoz vagy erőforrásokhoz
- Holtpontok, amelyekben két szál egymásra vár, így egyikük sem tud
  továbblépni
- Olyan hibák, amelyek csak bizonyos helyzetekben jelentkeznek, és nehéz őket
  megbízhatóan reprodukálni és javítani

A Rust igyekszik mérsékelni a szálak használatának negatív hatásait, de a
többszálú környezetben való programozás így is alapos átgondolást igényel, és
más kódszerkezetet kíván, mint az egyetlen szálon futó programoké.

A programozási nyelvek többféleképpen implementálják a szálakat, és sok
operációs rendszer olyan API-t kínál, amelyet a programozási nyelv új szálak
létrehozásához hívhat. A Rust standard könyvtára a szálak _1:1_ modelljét
használja: a program nyelvi szálanként egy operációsrendszer-szálat használ.
Léteznek crate-ek, amelyek másfajta szálmodelleket implementálnak, más
kompromisszumokkal, mint az 1:1 modell. (A Rust async rendszere, amelyet a
következő fejezetben látunk majd, szintén másféle megközelítést ad a
konkurenciához.)

### Új szál létrehozása a `spawn` függvénnyel {#creating-a-new-thread-with-spawn}

Új szál létrehozásához meghívjuk a `thread::spawn` függvényt, és átadunk neki
egy closure-t (a closure-ökről a 13. fejezetben volt szó), amely az új szálon
futtatni kívánt kódot tartalmazza. A 16-1. listában látható példa kiír némi
szöveget a fő szálról, és más szöveget egy új szálról.

<Listing number="16-1" file-name="src/main.rs" caption="Új szál létrehozása, amely kiír valamit, miközben a fő szál mást ír ki">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Vedd észre, hogy amikor egy Rust program fő szála befejeződik, minden elindított
szál leáll, függetlenül attól, hogy befejezte-e a futását. A program kimenete
minden alkalommal kicsit más lehet, de nagyjából így fog kinézni:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

A `thread::sleep` hívások arra kényszerítenek egy szálat, hogy rövid időre
szüneteltesse a futását, így egy másik szál futhat. A szálak valószínűleg
váltogatni fogják egymást, de ez nem garantált: attól függ, hogyan ütemezi őket
az operációs rendszered. Ebben a futásban a fő szál írt ki először, pedig az
elindított szál kiíró utasítása szerepel előbb a kódban. És bár azt mondtuk az
elindított szálnak, hogy addig írjon ki, amíg `i` el nem éri a `9`-et, csak
`5`-ig jutott, mielőtt a fő szál leállt.

Ha lefuttatod ezt a kódot, és csak a fő szál kimenetét látod, vagy nem látsz
átfedést, próbáld megnövelni a tartományokban szereplő számokat, hogy több
lehetőséget adj az operációs rendszernek a szálak közötti váltásra.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Várakozás az összes szál befejeződésére {#waiting-for-all-threads-to-finish}

A 16-1. lista kódja nemcsak azért állítja le idő előtt az elindított szálat az
esetek nagy részében, mert a fő szál véget ér, hanem mivel a szálak futási
sorrendjére sincs garancia, azt sem tudjuk garantálni, hogy az elindított szál
egyáltalán fut-e!

Azt a problémát, hogy az elindított szál nem fut, vagy idő előtt véget ér,
megoldhatjuk úgy, hogy a `thread::spawn` visszatérési értékét elmentjük egy
változóba. A `thread::spawn` visszatérési típusa `JoinHandle<T>`. A
`JoinHandle<T>` egy birtokolt érték, amelyen a `join` metódust meghívva megvárja,
amíg a hozzá tartozó szál befejeződik. A 16-2. lista bemutatja, hogyan
használjuk a 16-1. listában létrehozott szál `JoinHandle<T>` értékét, és hogyan
hívjuk meg a `join`-t annak biztosítására, hogy az elindított szál a `main`
kilépése előtt befejeződjön.

<Listing number="16-2" file-name="src/main.rs" caption="A `thread::spawn` által adott `JoinHandle<T>` elmentése annak garantálására, hogy a szál végigfusson">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Ha meghívjuk a `join`-t a handle-ön, az blokkolja az éppen futó szálat mindaddig,
amíg a handle által képviselt szál be nem fejeződik. Egy szál _blokkolása_ azt
jelenti, hogy a szál nem tud munkát végezni vagy kilépni. Mivel a `join` hívást
a fő szál `for` ciklusa után helyeztük el, a 16-2. lista futtatása körülbelül
ilyen kimenetet ad:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

A két szál továbbra is váltogatja egymást, de a fő szál a `handle.join()` hívás
miatt vár, és nem ér véget, amíg az elindított szál be nem fejeződik.

De nézzük meg, mi történik, ha ehelyett a `handle.join()` hívást a `main`
`for` ciklusa elé mozgatjuk, így:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

A fő szál megvárja, amíg az elindított szál befejeződik, és csak utána futtatja
a saját `for` ciklusát, így a kimenet többé nem lesz összefésülve, ahogy itt
látható:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Az apró részletek, például az, hogy hol hívjuk meg a `join`-t, befolyásolhatják,
hogy a szálaid egyszerre futnak-e vagy sem.

### `move` closure-ök használata szálakkal {#using-move-closures-with-threads}

A `thread::spawn`-nak átadott closure-öknél gyakran használjuk a `move`
kulcsszót, mert így a closure átveszi az ownershipet a környezetből használt
értékek felett, ezzel átadva ezen értékek ownershipjét az egyik szálról a
másikra. A 13. fejezet [„Referenciák elkapása vagy az ownership
átadása”][capture]<!-- ignore --> című részében a closure-ök kapcsán tárgyaltuk
a `move`-ot. Most inkább a `move` és a `thread::spawn` együttműködésére
összpontosítunk.

Figyeld meg, hogy a 16-1. listában a `thread::spawn`-nak átadott closure nem vesz
át argumentumot: az elindított szál kódjában nem használunk semmilyen adatot a
fő szálról. Ahhoz, hogy az elindított szálban a fő szál adatait használhassuk, az
elindított szál closure-jének el kell kapnia a szükséges értékeket. A 16-3. lista
egy olyan kísérletet mutat, amelyben a fő szálon létrehozunk egy vektort, és az
elindított szálban használjuk. Ez azonban egyelőre nem fog működni, ahogy
mindjárt látni fogod.

<Listing number="16-3" file-name="src/main.rs" caption="Kísérlet a fő szálon létrehozott vektor használatára egy másik szálban">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

A closure használja a `v`-t, tehát el fogja kapni, és a closure környezetének
részévé teszi. Mivel a `thread::spawn` ezt a closure-t egy új szálon futtatja,
elvileg hozzá kellene férnünk a `v`-hez az új szálon belül. Amikor viszont
lefordítjuk ezt a példát, a következő hibát kapjuk:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

A Rust _kikövetkezteti_, hogyan kapja el a `v`-t, és mivel a `println!`-nek csak
egy referenciára van szüksége a `v`-hez, a closure megpróbálja kölcsönvenni
(borrow) a `v`-t. Csakhogy van egy probléma: a Rust nem tudja megmondani, meddig
fog futni az elindított szál, így azt sem tudja, hogy a `v`-re mutató referencia
mindig érvényes lesz-e.

A 16-4. lista egy olyan forgatókönyvet mutat be, amelyben nagyobb az esély arra,
hogy a `v`-re mutató referencia érvénytelenné válik.

<Listing number="16-4" file-name="src/main.rs" caption="Szál olyan closure-rel, amely megpróbál elkapni egy `v`-re mutató referenciát egy olyan fő szálról, amely eldobja a `v`-t">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Ha a Rust megengedné, hogy ezt a kódot futtassuk, előfordulhatna, hogy az
elindított szál azonnal a háttérbe kerül, és egyáltalán nem fut le. Az elindított
szál egy `v`-re mutató referenciát tartalmaz, de a fő szál azonnal eldobja a
`v`-t a 15. fejezetben tárgyalt `drop` függvénnyel. Ezután, amikor az elindított
szál futni kezd, a `v` már nem érvényes, így a rá mutató referencia is
érvénytelen. Jaj, ne!

A 16-3. lista fordítási hibájának javításához követhetjük a hibaüzenet
tanácsát:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Ha a closure elé odaírjuk a `move` kulcsszót, arra kényszerítjük a closure-t,
hogy vegye át az ownershipet az általa használt értékek felett, ahelyett hogy
hagynánk a Rustot arra következtetni, hogy kölcsönvegye őket. A 16-3. lista
16-5. listában látható módosítása le fog fordulni, és úgy fog futni, ahogy
szeretnénk.

<Listing number="16-5" file-name="src/main.rs" caption="A `move` kulcsszó használata arra, hogy a closure átvegye az ownershipet az általa használt értékek felett">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Kísértést érezhetnénk arra, hogy ugyanezzel próbáljuk megjavítani a 16-4. lista
kódját, ahol a fő szál meghívta a `drop`-ot, vagyis hogy `move` closure-t
használjunk. Ez a javítás azonban nem működik, mert amit a 16-4. lista meg
akar tenni, az egy másik ok miatt nem megengedett. Ha hozzáadnánk a `move`-ot a
closure-höz, a `v`-t bemozgatnánk a closure környezetébe, és többé nem tudnánk
meghívni rá a `drop`-ot a fő szálon. Helyette ezt a fordítási hibát kapnánk:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

A Rust ownership-szabályai megint megmentettek minket! A 16-3. lista kódjából
azért kaptunk hibát, mert a Rust óvatos volt, és a `v`-t csak kölcsönvette a
szál számára, ami azt jelentette, hogy a fő szál elméletileg érvénytelenné
tehette volna az elindított szál referenciáját. Azzal, hogy megmondjuk a
Rustnak, mozgassa át a `v` ownershipjét az elindított szálra, garantáljuk a
Rustnak, hogy a fő szál többé nem használja a `v`-t. Ha a 16-4. listát ugyanígy
módosítjuk, akkor megsértjük az ownership-szabályokat, amikor a fő szálon
próbáljuk használni a `v`-t. A `move` kulcsszó felülírja a Rust óvatos,
alapértelmezett kölcsönzési viselkedését; azt nem engedi meg, hogy megsértsük
az ownership-szabályokat.

Most, hogy áttekintettük, mik a szálak, és milyen metódusokat kínál a szál-API,
nézzünk meg néhány helyzetet, amelyben szálakat használhatunk.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
