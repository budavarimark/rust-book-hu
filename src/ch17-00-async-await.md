# Az aszinkron programozás alapjai: async, await, future-ök és stream-ek

Sok művelet, amelynek elvégzésére megkérjük a számítógépet, hosszabb ideig
tarthat. Jó lenne, ha csinálhatnánk valami mást, amíg ezekre a hosszan futó
folyamatokra várunk. A modern számítógépek két technikát kínálnak arra, hogy
egyszerre több műveleten dolgozzunk: a párhuzamosságot és a konkurenciát. A
programjaink logikája azonban többnyire lineárisan íródik. Szeretnénk meg tudni
adni, milyen műveleteket végezzen el a program, és mely pontokon szüneteltethet
egy függvény, hogy helyette a program más része fusson, anélkül hogy előre
pontosan meg kellene határoznunk, milyen sorrendben és módon fusson az egyes
kódrészletek mindegyike. Az _aszinkron programozás_ olyan absztrakció, amely
lehetővé teszi, hogy a kódunkat lehetséges szünetelési pontok és később
megérkező eredmények formájában fejezzük ki, a koordináció részleteit pedig
elintézi helyettünk.

Ez a fejezet a 16. fejezet szálakra épülő párhuzamosságára és konkurenciájára
épít, és a kódírásnak egy alternatív megközelítését mutatja be: a Rust
future-jeit, stream-jeit, valamint az `async` és `await` szintaxist, amelyekkel
kifejezhetjük, hogy mely műveletek lehetnek aszinkronok, továbbá azokat a
harmadik féltől származó crate-eket, amelyek aszinkron runtime-okat
implementálnak: olyan kódot, amely az aszinkron műveletek végrehajtását kezeli
és koordinálja.

Nézzünk egy példát. Tegyük fel, hogy éppen exportálsz egy videót, amit egy
családi ünnepségről készítettél; ez a művelet percektől órákig bármeddig
eltarthat. A videóexport annyi CPU- és GPU-teljesítményt használ fel,
amennyit csak tud. Ha csak egyetlen CPU-magod lenne, és az operációs rendszered
nem szüneteltetné az exportot annak befejeződéséig – azaz ha _szinkron_ módon
hajtaná végre az exportot –, semmi mást nem tudnál csinálni a számítógépeden,
amíg az a feladat fut. Ez elég frusztráló élmény lenne. Szerencsére a
számítógéped operációs rendszere képes elég gyakran, láthatatlanul megszakítani
az exportot ahhoz, hogy közben más munkát is el tudj végezni.

Most tegyük fel, hogy egy másvalaki által megosztott videót töltesz le; ez is
eltarthat egy ideig, de nem foglal le annyi CPU-időt. Ebben az esetben a
CPU-nak arra kell várnia, hogy megérkezzenek az adatok a hálózatról. Bár
elkezdheted olvasni az adatokat, amint megjelennek, eltarthat egy ideig, amíg
mind megérkezik. Még ha az összes adat meg is van, egy nagyobb videónál
legalább egy-két másodpercig is eltarthat a betöltésük. Ez talán nem hangzik
soknak, de egy modern processzor számára – amely másodpercenként több milliárd
műveletet képes végrehajtani – nagyon hosszú idő. Az operációs rendszer itt is
láthatatlanul megszakítja a programodat, hogy a CPU más munkát végezhessen,
miközben a hálózati hívás befejeződésére vár.

A videóexport a _CPU-bound_, vagyis _compute-bound_ műveletek példája. Azt
korlátozza, hogy a számítógép mekkora adatfeldolgozási sebességre képes a
CPU-ban vagy a GPU-ban, és ebből mennyit tud az adott műveletre fordítani. A
videóletöltés viszont az _I/O-bound_ műveletek példája, mert a számítógép
_bemenetének és kimenetének_ (input és output) sebessége korlátozza: csak
olyan gyors lehet, amilyen gyorsan az adatok átküldhetők a hálózaton.

Mindkét példában az operációs rendszer láthatatlan megszakításai a konkurencia
egy formáját nyújtják. Ez a konkurencia azonban csak az egész program szintjén
jelenik meg: az operációs rendszer az egyik programot megszakítja, hogy más
programok is haladhassanak a munkájukkal. Sok esetben viszont – mivel mi
sokkal részletesebb szinten értjük a saját programjainkat, mint az operációs
rendszer – olyan konkurenciára adódó lehetőségeket is észreveszünk, amelyeket
az operációs rendszer nem lát.

Ha például egy fájlletöltéseket kezelő eszközt építünk, olyan programot
szeretnénk írni, amelyben az egyik letöltés elindítása nem fagyasztja be a
felhasználói felületet, és a felhasználók egyszerre több letöltést is
elindíthatnak. A hálózattal való kommunikációhoz használt operációsrendszer-API-k
közül azonban sok _blokkoló_; vagyis addig akadályozzák a program haladását,
amíg az általuk feldolgozott adatok teljesen készen nem állnak.

> Megjegyzés: ha belegondolsz, a függvényhívások _többsége_ így működik. A
> _blokkoló_ kifejezést azonban általában olyan függvényhívásokra tartjuk fenn,
> amelyek fájlokkal, a hálózattal vagy a számítógép más erőforrásaival lépnek
> kapcsolatba, mert ezekben az esetekben járna jól egy adott program azzal, ha
> a művelet _nem_ blokkolna.

Elkerülhetnénk a fő szálunk blokkolását azzal, hogy minden fájl letöltéséhez
külön szálat indítunk. Az ezek a szálak által használt rendszererőforrások
többletterhelése azonban előbb-utóbb problémává válna. Jobb lenne, ha a hívás
eleve nem blokkolna, mi pedig megadhatnánk azoknak a task-oknak a halmazát,
amelyeket a programunkkal el szeretnénk végeztetni, és a runtime-ra bíznánk,
hogy a legjobb sorrendben és módon futtassa őket.

Pontosan ezt adja nekünk a Rust _async_ (az _asynchronous_, azaz aszinkron
rövidítése) absztrakciója. Ebben a fejezetben mindent megtudsz az asyncről,
miközben a következő témákat tekintjük át:

- Hogyan használjuk a Rust `async` és `await` szintaxisát, és hogyan hajtsunk
  végre aszinkron függvényeket egy runtime segítségével
- Hogyan oldjuk meg az async modellel ugyanazokat a kihívásokat, amelyekkel a
  16. fejezetben foglalkoztunk
- Hogyan nyújt a többszálúság és az async egymást kiegészítő megoldásokat,
  amelyeket sok esetben kombinálhatsz is

Mielőtt azonban megnéznénk, hogyan működik az async a gyakorlatban, tegyünk egy
rövid kitérőt a párhuzamosság és a konkurencia közötti különbségek
megbeszélésére.

## Párhuzamosság és konkurencia

Eddig a párhuzamosságot és a konkurenciát nagyjából felcserélhetőként kezeltük.
Most pontosabban meg kell különböztetnünk őket, mert a különbségek elő fognak
kerülni, amint munkához látunk.

Gondold végig, milyen módokon oszthat fel egy csapat egy szoftverprojekten
végzendő munkát. Adhatsz egyetlen tagnak több feladatot, adhatsz minden tagnak
egy-egy feladatot, vagy keverheted a két megközelítést.

Amikor egyetlen ember több különböző feladaton dolgozik úgy, hogy egyik sincs
még kész, az a _konkurencia_. A konkurencia megvalósításának egyik módja
hasonlít ahhoz, mintha két különböző projekt lenne kicsekkolva a
számítógépeden, és amikor az egyikbe beleunsz vagy elakadsz, átváltasz a
másikra. Csak egy ember vagy, így nem tudsz mindkét feladaton pontosan
ugyanabban a pillanatban haladni, de tudsz többfelé figyelni: egyszerre az
egyiken haladsz, váltogatva köztük (lásd a 17-1. ábrát).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="Egy diagram egymás fölé helyezett dobozokkal, amelyek címkéje Task A és Task B, bennük rombuszok jelölik a részfeladatokat. Nyilak mutatnak A1-től B1-ig, B1-től A2-ig, A2-től B2-ig, B2-től A3-ig, A3-tól A4-ig és A4-től B3-ig. A részfeladatok közötti nyilak átlépik a Task A és a Task B doboza közötti határt." />

<figcaption>17-1. ábra: Konkurens munkafolyamat, váltogatva a Task A és a Task B között</figcaption>

</figure>

Amikor a csapat úgy osztja fel a feladatokat, hogy mindenki elvállal egyet, és
azon egyedül dolgozik, az a _párhuzamosság_. A csapat minden tagja pontosan
ugyanabban a pillanatban tud haladni (lásd a 17-2. ábrát).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="Egy diagram egymás fölé helyezett dobozokkal, amelyek címkéje Task A és Task B, bennük rombuszok jelölik a részfeladatokat. Nyilak mutatnak A1-től A2-ig, A2-től A3-ig, A3-tól A4-ig, B1-től B2-ig és B2-től B3-ig. Egyetlen nyíl sem lép át a Task A és a Task B doboza között." />

<figcaption>17-2. ábra: Párhuzamos munkafolyamat, ahol a Task A és a Task B munkája egymástól függetlenül zajlik</figcaption>

</figure>

Mindkét munkafolyamatban előfordulhat, hogy koordinálnod kell a különböző
feladatok között. Talán azt hitted, hogy az egyik emberre bízott feladat
teljesen független mindenki más munkájától, valójában viszont a csapat egy
másik tagjának előbb be kell fejeznie a saját feladatát. A munka egy része
végezhető párhuzamosan, egy másik része azonban valójában _soros_: csak
sorozatban, egyik feladat a másik után történhet, ahogy a 17-3. ábrán látható.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="Egy diagram egymás fölé helyezett dobozokkal, amelyek címkéje Task A és Task B, bennük rombuszok jelölik a részfeladatokat. A Task A-ban nyilak mutatnak A1-től A2-ig, A2-től egy pár vastag függőleges vonalig, amely a „szünet” szimbólumra hasonlít, majd ettől a szimbólumtól A3-ig. A Task B-ben nyilak mutatnak B1-től B2-ig, B2-től B3-ig, B3-tól A3-ig és B3-tól B4-ig." />

<figcaption>17-3. ábra: Részben párhuzamos munkafolyamat, ahol a Task A és a Task B munkája egymástól függetlenül zajlik, amíg a Task A3 el nem akad a Task B3 eredményein.</figcaption>

</figure>

Hasonlóképpen az is kiderülhet, hogy az egyik saját feladatod egy másik saját
feladatodtól függ. Ekkor a konkurens munkád is sorossá vált.

A párhuzamosság és a konkurencia egymást is metszheti. Ha megtudod, hogy egy
kollégád addig nem tud haladni, amíg te be nem fejezed az egyik feladatodat,
valószínűleg minden erőddel arra a feladatra fogsz koncentrálni, hogy
„feloldd” a kollégádat. Ekkor te és a munkatársad már nem tudtok párhuzamosan
dolgozni, és te sem tudsz többé konkurensen dolgozni a saját feladataidon.

Ugyanezek az alapvető dinamikák érvényesülnek a szoftver és a hardver
világában is. Egy egymagos CPU-val rendelkező gépen a CPU egyszerre csak egy
műveletet tud végrehajtani, konkurensen mégis tud dolgozni. Olyan eszközök
segítségével, mint a szálak, a folyamatok és az async, a számítógép
szüneteltetheti az egyik tevékenységet, átválthat másokra, majd végül
visszatérhet az első tevékenységhez. Egy több CPU-maggal rendelkező gépen
párhuzamosan is tud dolgozni. Az egyik mag végezhet egy feladatot, miközben egy
másik mag egy teljesen független feladatot végez, és ezek a műveletek
ténylegesen egy időben zajlanak.

A Rustban az async kód futtatása általában konkurensen történik. A hardvertől,
az operációs rendszertől és a használt async runtime-tól függően (az async
runtime-okról hamarosan bővebben) ez a konkurencia a motorháztető alatt
párhuzamosságot is használhat.

Most pedig merüljünk el abban, hogyan is működik valójában az aszinkron
programozás a Rustban.
