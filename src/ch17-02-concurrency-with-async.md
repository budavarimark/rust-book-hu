<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Konkurencia alkalmazása asynckel

Ebben a szakaszban az asyncet fogjuk alkalmazni néhány olyan konkurenciával
kapcsolatos kihívásra, amelyeket a 16. fejezetben szálakkal oldottunk meg.
Mivel a kulcsgondolatok közül sokról már ott beszéltünk, ebben a szakaszban
arra összpontosítunk, hogy mi különbözik a szálak és a future-ök között.

Sok esetben az asynckel való konkurens munkára szolgáló API-k nagyon
hasonlítanak a szálakéhoz. Más esetekben viszont egészen eltérőnek bizonyulnak.
Még akkor is, ha az API-k a szálak és az async esetében hasonlónak _tűnnek_,
gyakran más a viselkedésük – és szinte mindig más a teljesítménybeli
jellemzőjük.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Új task létrehozása a `spawn_task` segítségével

Az első művelet, amellyel a 16. fejezet [„Új szál létrehozása a `spawn`
segítségével”][thread-spawn]<!-- ignore --> szakaszában megbirkóztunk, a két
külön szálon való számlálás volt. Csináljuk meg ugyanezt asynckel! A `trpl`
crate biztosít egy `spawn_task` függvényt, amely nagyon hasonlít a
`thread::spawn` API-ra, és egy `sleep` függvényt, amely a `thread::sleep` API
async változata. Ezeket együtt használva implementálhatjuk a számlálós példát,
ahogy a 17-6. lista mutatja.

<Listing number="17-6" caption="Új task létrehozása, amely egy dolgot ír ki, miközben a fő task valami mást ír ki" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Kiindulásként a `main` függvényünket a `trpl::block_on` segítségével állítjuk
be, hogy a legfelső szintű függvényünk async lehessen.

> Megjegyzés: a fejezetben innentől kezdve minden példa pontosan ugyanezt a
> `trpl::block_on`-os becsomagoló kódot tartalmazza a `main`-ben, ezért gyakran
> ki fogjuk hagyni, éppúgy, ahogy magát a `main`-t is. Ne feledd beletenni a
> saját kódodba!

Ezután két ciklust írunk a blokkon belül, mindegyikben egy `trpl::sleep`
hívással, amely fél másodpercet (500 ezredmásodpercet) vár a következő üzenet
elküldése előtt. Az egyik ciklust egy `trpl::spawn_task` törzsébe tesszük, a
másikat pedig egy legfelső szintű `for` ciklusba. A `sleep` hívások után egy-egy
`await`-et is teszünk.

Ez a kód hasonlóan viselkedik a szálakra épülő implementációhoz – beleértve azt
is, hogy a saját termináljában futtatva más sorrendben is megjelenhetnek az
üzenetek:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Ez a változat azonnal leáll, amint a fő async blokk törzsében lévő `for` ciklus
véget ér, mert a `spawn_task` által indított task leáll, amikor a `main`
függvény befejeződik. Ha azt szeretnéd, hogy a task teljes befejeződéséig
fusson, egy join handle-t kell használnod, hogy megvárd az első task
befejeződését. A szálaknál a `join` metódust használtuk, hogy „blokkoljunk”,
amíg a szál le nem futott. A 17-7. listában az `await`-tel érhetjük el
ugyanezt, mert maga a task handle is egy future. Az `Output` típusa egy
`Result`, ezért a bevárása után ki is csomagoljuk.

<Listing number="17-7" caption="Az `await` használata join handle-lel, hogy a task teljesen lefusson" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Ez a frissített változat addig fut, amíg _mindkét_ ciklus be nem fejeződik:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Eddig úgy tűnik, hogy az async és a szálak hasonló eredményt adnak, csak más
szintaxissal: a join handle-ön a `join` hívása helyett az `await`-et
használjuk, és bevárjuk a `sleep` hívásokat.

A nagyobb különbség az, hogy ehhez nem kellett újabb operációsrendszer-szálat
indítanunk. Sőt, itt még task-ot sem kell indítanunk. Mivel az async blokkok
névtelen future-ökké fordulnak, mindegyik ciklust egy-egy async blokkba
tehetjük, és a `trpl::join` függvénnyel futtathatjuk le mindkettőt a
runtime-mal.

A 16. fejezet [„Várakozás az összes szál
befejeződésére”][join-handles]<!-- ignore --> szakaszában megmutattuk, hogyan
használjuk a `join` metódust azon a `JoinHandle` típuson, amellyel a
`std::thread::spawn` hívása visszatér. A `trpl::join` függvény ehhez hasonló, de
future-ökre. Ha két future-t adsz neki, egyetlen új future-t állít elő, amelynek
a kimenete egy olyan tuple, amely az átadott future-ök kimeneteit tartalmazza,
amint _mindkettő_ befejeződött. Így a 17-8. listában a `trpl::join`-t
használjuk, hogy megvárjuk mind a `fut1`, mind a `fut2` befejeződését. _Nem_ a
`fut1`-et és a `fut2`-t várjuk be, hanem a `trpl::join` által előállított új
future-t. A kimenetet figyelmen kívül hagyjuk, mert az csak egy két unit
értéket tartalmazó tuple.

<Listing number="17-8" caption="A `trpl::join` használata két névtelen future bevárására" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Amikor ezt lefuttatjuk, azt látjuk, hogy mindkét future teljesen lefut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Most már minden alkalommal pontosan ugyanazt a sorrendet fogod látni, ami
nagyon eltér attól, amit a szálaknál és a `trpl::spawn_task`-nál láttunk a 17-7.
listában. Ennek az az oka, hogy a `trpl::join` függvény _igazságos_, vagyis
minden future-t ugyanolyan gyakran ellenőriz, váltogatva köztük, és sosem engedi
előreszaladni az egyiket, ha a másik készen áll. A szálaknál az operációs
rendszer dönti el, melyik szálat ellenőrzi, és mennyi ideig hagyja futni. Az
async Rustban a runtime dönti el, melyik task-ot ellenőrzi. (A gyakorlatban a
részletek bonyolultak, mert egy async runtime a motorháztető alatt akár
operációsrendszer-szálakat is használhat a konkurencia kezelésének részeként,
így az igazságosság garantálása több munkát jelenthet a runtime számára – de
attól még lehetséges!) A runtime-oknak nem kell garantálniuk az igazságosságot
egyetlen adott műveletre sem, és gyakran különböző API-kat kínálnak, hogy
választhass, akarsz-e igazságosságot.

Próbáld ki a future-ök bevárásának néhány alábbi változatát, és nézd meg, mit
csinálnak:

- Vedd el az async blokkot az egyik vagy mindkét ciklus körül.
- Várj be minden async blokkot közvetlenül a definiálása után.
- Csak az első ciklust csomagold async blokkba, és a kapott future-t a második
  ciklus törzse után várd be.

Külön kihívásként nézd meg, ki tudod-e találni, mi lesz a kimenet az egyes
esetekben, _mielőtt_ lefuttatnád a kódot!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Adatküldés két task között üzenetküldéssel {#sending-data-between-two-tasks-using-message-passing}

A future-ök közötti adatmegosztás is ismerős lesz: ismét üzenetküldést
használunk, de ezúttal a típusok és függvények async változataival. Kicsit más
utat járunk be, mint a 16. fejezet [„Adatátvitel szálak között
üzenetküldéssel”][message-passing-threads]<!-- ignore --> szakaszában, hogy
szemléltessük a szálakra, illetve a future-ökre épülő konkurencia néhány
lényeges különbségét. A 17-9. listában mindössze egyetlen async blokkal
kezdünk – _nem_ indítunk külön task-ot, ahogy korábban külön szálat indítottunk.

<Listing number="17-9" caption="Async csatorna létrehozása és a két felének hozzárendelése a `tx`-hez és az `rx`-hez" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Itt a `trpl::channel`-t használjuk, annak a több termelős, egy fogyasztós
csatorna-API-nak az async változatát, amelyet a 16. fejezetben a szálaknál
használtunk. Az API async változata csak kicsit tér el a szálakra épülő
változattól: nem módosíthatatlan, hanem módosítható `rx` fogadót használ, és a
`recv` metódusa nem közvetlenül az értéket állítja elő, hanem egy future-t,
amelyet be kell várnunk. Most már küldhetünk üzeneteket a küldőtől a fogadóhoz.
Figyeld meg, hogy nem kell külön szálat, sőt még task-ot sem indítanunk;
mindössze be kell várnunk az `rx.recv` hívást.

A `std::mpsc::channel` szinkron `Receiver::recv` metódusa blokkol, amíg meg nem
kap egy üzenetet. A `trpl::Receiver::recv` metódus nem, mert async. Blokkolás
helyett visszaadja a vezérlést a runtime-nak, amíg vagy meg nem érkezik egy
üzenet, vagy be nem zárul a csatorna küldő oldala. Ezzel szemben a `send`
hívást nem várjuk be, mert az nem blokkol. Nincs is rá szüksége, mert a
csatorna, amelybe küldünk, korlátlan.

> Megjegyzés: mivel ez az egész async kód egy `trpl::block_on` hívásban lévő
> async blokkban fut, minden, ami benne van, elkerülheti a blokkolást. A
> _rajta kívüli_ kód viszont blokkolva vár arra, hogy a `block_on` függvény
> visszatérjen. Pontosan ez a `trpl::block_on` függvény lényege: lehetővé
> teszi, hogy _megválaszd_, hol blokkolj egy adott async kódrészleten, és így
> azt is, hol legyen az átmenet a szinkron és az async kód között.

Két dolgot vegyél észre ebben a példában. Egyrészt az üzenet azonnal megérkezik.
Másrészt, bár future-t használunk itt, egyelőre nincs konkurencia. A listában
minden sorban zajlik, éppúgy, mintha egyáltalán nem lennének future-ök a
játékban.

Foglalkozzunk az első résszel úgy, hogy egy sor üzenetet küldünk, és köztük
alszunk egy kicsit, ahogy a 17-10. lista mutatja.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Több üzenet küldése és fogadása az async csatornán, minden üzenet között egy `await`-tel megvárt alvással" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Az üzenetek küldésén túl fogadnunk is kell őket. Ebben az esetben, mivel tudjuk,
hány üzenet érkezik, ezt kézzel is megtehetnénk úgy, hogy négyszer meghívjuk az
`rx.recv().await`-et. A való világban azonban általában _ismeretlen_ számú
üzenetre várunk, ezért addig kell várakoznunk, amíg meg nem állapítjuk, hogy
nincs több üzenet.

A 16-10. listában egy `for` ciklussal dolgoztuk fel a szinkron csatornáról
fogadott összes elemet. A Rustban azonban egyelőre nincs mód arra, hogy `for`
ciklust használjunk _aszinkron módon előállított_ elemsorozaton, ezért olyan
ciklust kell használnunk, amellyel eddig nem találkoztunk: a `while let`
feltételes ciklust. Ez annak az `if let` szerkezetnek a ciklusváltozata, amelyet
még a 6. fejezet [„Tömör vezérlési folyamat az `if let` és a `let...else`
segítségével”][if-let]<!-- ignore --> szakaszában láttunk. A ciklus addig fut
tovább, amíg a megadott minta illeszkedik az értékre.

Az `rx.recv` hívás egy future-t állít elő, amelyet bevárunk. A runtime addig
szünetelteti a future-t, amíg az készen nem áll. Amint megérkezik egy üzenet, a
future `Some(message)` értékké oldódik fel, annyiszor, ahányszor üzenet
érkezik. Amikor a csatorna bezárul – függetlenül attól, hogy érkezett-e
_bármilyen_ üzenet –, a future ehelyett `None` értékké oldódik fel, jelezve,
hogy nincs több érték, tehát abba kell hagynunk a poll-ozást, vagyis a
bevárását.

A `while let` ciklus mindezt összefogja. Ha az `rx.recv().await` hívás eredménye
`Some(message)`, hozzáférünk az üzenethez, és felhasználhatjuk a ciklus
törzsében, éppúgy, ahogy az `if let`-tel tehettük. Ha az eredmény `None`, a
ciklus véget ér. Valahányszor a ciklus lefut, ismét eléri az await pontot, így a
runtime újra szünetelteti, amíg újabb üzenet nem érkezik.

A kód most már sikeresen elküldi és fogadja az összes üzenetet. Sajnos még
mindig van néhány probléma. Egyrészt az üzenetek nem félmásodperces időközönként
érkeznek. Egyszerre érkeznek meg, 2 másodperccel (2000 ezredmásodperccel) a
program indítása után. Másrészt ez a program soha nem is lép ki! Ehelyett örökké
új üzenetekre vár. A <kbd>ctrl</kbd>-<kbd>C</kbd> billentyűkombinációval kell
leállítanod.

#### Egy async blokkon belüli kód lineárisan hajtódik végre

Kezdjük annak megvizsgálásával, miért érkezik minden üzenet egyszerre, a teljes
késleltetés után, ahelyett hogy egyenként, közöttük késleltetéssel érkeznének.
Egy adott async blokkon belül az a sorrend, amelyben az `await` kulcsszavak
megjelennek a kódban, egyben az a sorrend is, amelyben a program futásakor
végrehajtódnak.

A 17-10. listában csak egyetlen async blokk van, így minden lineárisan fut.
Konkurencia továbbra sincs. Az összes `tx.send` hívás lezajlik, közéjük
keveredve az összes `trpl::sleep` hívással és a hozzájuk tartozó await
pontokkal. Csak ezután jut el a `while let` ciklus a `recv` hívásokon lévő
`await` pontok bármelyikéhez.

Ahhoz, hogy megkapjuk a kívánt viselkedést, amelyben az alvási késleltetés az
egyes üzenetek között történik, a `tx`- és `rx`-műveleteket saját async
blokkokba kell tennünk, ahogy a 17-11. lista mutatja. Ekkor a runtime a
`trpl::join` segítségével külön-külön hajthatja végre őket, éppúgy, mint a 17-8.
listában. Ismét a `trpl::join` hívás eredményét várjuk be, nem az egyes
future-öket. Ha az egyes future-öket sorban várnánk be, csak visszajutnánk a
soros folyamathoz – pontosan ahhoz, amit _nem_ akarunk.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="A `send` és a `recv` szétválasztása saját `async` blokkokra, majd az ezekhez a blokkokhoz tartozó future-ök bevárása" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

A 17-11. listában szereplő frissített kóddal az üzenetek 500 ezredmásodperces
időközönként íródnak ki, nem pedig egyszerre, 2 másodperc után.

#### Ownership átmozgatása egy async blokkba

A program azonban továbbra sem lép ki soha, mégpedig amiatt, ahogyan a
`while let` ciklus és a `trpl::join` együttműködik:

- A `trpl::join` által visszaadott future csak akkor fejeződik be, ha a neki
  átadott _mindkét_ future befejeződött.
- A `tx_fut` future akkor fejeződik be, amikor befejezi az alvást a `vals`-ban
  lévő utolsó üzenet elküldése után.
- Az `rx_fut` future addig nem fejeződik be, amíg a `while let` ciklus véget nem
  ér.
- A `while let` ciklus addig nem ér véget, amíg az `rx.recv` bevárása `None`
  értéket nem ad.
- Az `rx.recv` bevárása csak akkor ad `None`-t, ha a csatorna másik vége
  bezárult.
- A csatorna csak akkor zárul be, ha meghívjuk az `rx.close`-t, vagy amikor a
  küldő oldal, a `tx` eldobásra kerül.
- Sehol sem hívjuk meg az `rx.close`-t, a `tx` pedig addig nem kerül eldobásra,
  amíg a `trpl::block_on`-nak átadott legkülső async blokk véget nem ér.
- A blokk nem érhet véget, mert blokkolva vár a `trpl::join` befejeződésére, ami
  visszavisz minket ennek a listának az elejére.

Jelenleg az az async blokk, amelyben az üzeneteket küldjük, csak _kölcsönveszi_
a `tx`-et, mert egy üzenet elküldéséhez nem kell ownership, de ha a `tx`-et be
tudnánk _mozgatni_ abba az async blokkba, akkor a blokk végén eldobásra kerülne.
A 13. fejezet [„Referenciák elkapása vagy az ownership
átmozgatása”][capture-or-move]<!-- ignore --> szakaszában megtanultad, hogyan
használd a `move` kulcsszót closure-ökkel, és ahogy a 16. fejezet [„`move`
closure-ök használata szálakkal”][move-threads]<!-- ignore --> szakaszában szó
volt róla, szálakkal dolgozva gyakran kell adatokat closure-ökbe mozgatnunk.
Ugyanezek az alapvető dinamikák érvényesek az async blokkokra is, így a `move`
kulcsszó ugyanúgy működik async blokkokkal, mint closure-ökkel.

A 17-12. listában az üzenetek küldésére használt blokkot `async`-ról `async
move`-ra változtatjuk.

<Listing number="17-12" caption="A 17-11. lista kódjának átdolgozása, amely a befejeződéskor helyesen leáll" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Amikor a kód _ezt_ a változatát futtatjuk, szabályosan leáll, miután az utolsó
üzenetet elküldtük és fogadtuk. Ezután nézzük meg, min kellene változtatni
ahhoz, hogy egynél több future-ből küldjünk adatot.

#### Több future összefogása a `join!` makróval

Ez az async csatorna egyben több termelős csatorna is, így meghívhatjuk a
`clone`-t a `tx`-en, ha több future-ből szeretnénk üzeneteket küldeni, ahogy a
17-13. lista mutatja.

<Listing number="17-13" caption="Több termelő használata async blokkokkal" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Először klónozzuk a `tx`-et, létrehozva a `tx1`-et az első async blokkon kívül.
A `tx1`-et bemozgatjuk abba a blokkba, ahogy korábban a `tx`-szel tettük.
Később aztán az eredeti `tx`-et egy _új_ async blokkba mozgatjuk, ahol kicsit
lassabb késleltetéssel küldünk további üzeneteket. Ezt az új async blokkot most
az üzenetfogadó async blokk után helyeztük el, de éppúgy elé is kerülhetne. A
lényeg az a sorrend, amelyben a future-öket bevárjuk, nem pedig az, amelyben
létrehozzuk őket.

Az üzenetküldésre szolgáló mindkét async blokknak `async move` blokknak kell
lennie, hogy a `tx` és a `tx1` is eldobásra kerüljön, amikor ezek a blokkok
befejeződnek. Különben visszajutunk ugyanabba a végtelen ciklusba, amelyből
elindultunk.

Végül a `trpl::join`-ról a `trpl::join!`-ra váltunk, hogy a további future-t is
kezelni tudjuk: a `join!` makró tetszőleges számú future-t vár be, olyan
esetekben, amikor fordítási időben tudjuk a future-ök számát. Az ismeretlen
számú future-ből álló kollekciók bevárásáról később, ebben a fejezetben lesz
szó.

Most már látjuk mindkét küldő future összes üzenetét, és mivel a küldő future-ök
a küldés után kissé eltérő késleltetést használnak, az üzenetek is ezekkel az
eltérő időközökkel érkeznek meg:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Megnéztük, hogyan használjunk üzenetküldést future-ök közötti adatküldésre,
hogyan fut egy async blokkon belüli kód sorban, hogyan mozgassunk ownershipet
egy async blokkba, és hogyan fogjunk össze több future-t. Ezután beszéljünk
arról, hogyan és miért jelezzük a runtime-nak, hogy átválthat egy másik
task-ra.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
