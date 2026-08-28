# Bevezetés

> Megjegyzés: A könyv jelen kiadása megegyezik a [The Rust Programming
> Language][nsprust] című, a [No Starch Press][nsp] gondozásában nyomtatott és
> e-könyv formátumban is elérhető kötettel.

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Üdvözlünk a _The Rust Programming Language_ lapjain, amely egy Rustról szóló
bevezető könyv. A Rust programozási nyelv abban segít, hogy gyorsabb és
megbízhatóbb szoftvert írj. A magas szintű ergonómia és az alacsony szintű
irányítás a programozásinyelv-tervezésben gyakran ütközik egymással; a Rust
kihívást intéz ez ellen az ellentét ellen. Azzal, hogy egyensúlyt teremt az
erőteljes technikai képességek és a kellemes fejlesztői élmény között, a Rust
lehetőséget ad az alacsony szintű részletek (például a memóriahasználat)
kézben tartására, mégpedig azon vesződségek nélkül, amelyek az ilyen irányítást
hagyományosan kísérik.

## Kinek való a Rust

A Rust sokféle okból sokak számára ideális. Nézzünk meg néhányat a
legfontosabb csoportok közül.

### Fejlesztőcsapatok

A Rust termékeny eszköznek bizonyul olyan nagy fejlesztőcsapatok
együttműködésében, amelyek tagjai eltérő mélységben ismerik a
rendszerprogramozást. Az alacsony szintű kód hajlamos mindenféle alattomos
hibára, amelyeket a legtöbb más nyelvben csak kiterjedt teszteléssel és
tapasztalt fejlesztők alapos kódátvizsgálásával lehet elkapni. A Rustban a
fordító kapuőri szerepet játszik: nem hajlandó lefordítani az ilyen
megfoghatatlan hibákat – köztük a konkurenciahibákat – tartalmazó kódot. Ha a
csapat a fordítóval együtt dolgozik, akkor az idejét a program logikájára
fordíthatja ahelyett, hogy hibákat üldözne.

A Rust ráadásul korszerű fejlesztői eszközöket hoz a rendszerprogramozás
világába:

- A Cargo, a hozzá tartozó függőségkezelő és build eszköz fájdalommentessé és a
  Rust-ökoszisztémán belül egységessé teszi a függőségek hozzáadását,
  fordítását és kezelését.
- A `rustfmt` formázóeszköz egységes kódolási stílust biztosít a fejlesztők
  között.
- A Rust Language Server hajtja az integrált fejlesztői környezetek (IDE-k)
  integrációját: a kódkiegészítést és a soron belüli hibaüzeneteket.

Ezeknek és a Rust-ökoszisztéma egyéb eszközeinek használatával a fejlesztők
termelékenyek maradhatnak, miközben rendszerszintű kódot írnak.

### Diákok

A Rust a diákoké és mindazoké, akiket érdekel a rendszerszintű fogalmak
megismerése. A Rust segítségével sokan ismerkedtek meg olyan témákkal, mint az
operációsrendszer-fejlesztés. A közösség nagyon befogadó, és szívesen válaszol
a diákok kérdéseire. Az olyan törekvésekkel, mint ez a könyv, a Rust csapatai
azt szeretnék elérni, hogy a rendszerszintű fogalmak minél többek számára
hozzáférhetők legyenek, különösen a programozásban újoncok számára.

### Cégek

Több száz kis és nagy cég használja a Rustot éles környezetben a
legkülönbözőbb feladatokra, például parancssori eszközökhöz,
webszolgáltatásokhoz, DevOps-eszközökhöz, beágyazott eszközökhöz, hang- és
videóelemzéshez és -átkódoláshoz, kriptovalutákhoz, bioinformatikához,
keresőmotorokhoz, a dolgok internete (IoT) alkalmazásaihoz, gépi tanuláshoz,
sőt a Firefox webböngésző jelentős részeihez is.

### Nyílt forráskódú fejlesztők

A Rust azoké, akik szeretnék építeni a Rust programozási nyelvet, a
közösségét, a fejlesztői eszközeit és a könyvtárait. Örömmel vennénk, ha te is
hozzájárulnál a Rust nyelvhez.

### Akik értékelik a sebességet és a stabilitást

A Rust azoké, akik sebességre és stabilitásra vágynak egy nyelvben. Sebesség
alatt egyszerre értjük azt, hogy a Rust-kód milyen gyorsan fut, és azt, hogy a
Rustban milyen gyorsan tudsz programokat írni. A Rust fordítójának
ellenőrzései a stabilitást biztosítják az újabb képességek hozzáadása és a
refaktorálás során is. Ez éles ellentétben áll az ilyen ellenőrzések nélküli
nyelvek törékeny, örökölt kódjával, amelyhez a fejlesztők gyakran hozzányúlni
sem mernek. A nulla költségű absztrakciókra – magasabb szintű képességekre,
amelyek olyan gyors alacsony szintű kóddá fordulnak, mintha kézzel írták volna
őket – törekedve a Rust arra igyekszik, hogy a biztonságos kód egyben gyors
kód is legyen.

A Rust nyelv reméli, hogy sok más felhasználót is támogatni tud; az itt
említettek csupán a legnagyobb érdekelt csoportok közül valók. Összességében a
Rust legnagyobb ambíciója az, hogy megszüntesse azokat a kompromisszumokat,
amelyeket a programozók évtizedeken át elfogadtak: egyszerre nyújt
biztonságot _és_ termelékenységet, sebességet _és_ ergonómiát. Próbáld ki a
Rustot, és nézd meg, beválnak-e nálad a döntései.

## Kinek szól ez a könyv

Ez a könyv feltételezi, hogy már írtál kódot valamilyen másik programozási
nyelven, de nem feltételezi, hogy melyiken. Igyekeztünk az anyagot széles
körben hozzáférhetővé tenni a legkülönfélébb programozói háttérrel
rendelkezők számára. Nem foglalkozunk sokat azzal, hogy _mi is_ a programozás,
vagy hogyan gondolkodjunk róla. Ha teljesen kezdő vagy a programozásban, jobban
jársz, ha előbb egy kifejezetten a programozásba bevezető könyvet olvasol el.

## Hogyan használd ezt a könyvet

A könyv általában azt feltételezi, hogy elölről hátrafelé, sorrendben olvasod.
A későbbi fejezetek a korábbi fejezetek fogalmaira épülnek, a korábbi fejezetek
pedig lehet, hogy nem mennek bele egy-egy téma részleteibe, de valamelyik
későbbi fejezetben visszatérnek rá.

Kétféle fejezetet találsz a könyvben: fogalmi fejezeteket és
projektfejezeteket. A fogalmi fejezetekben a Rust egy-egy vonatkozásáról
tanulsz. A projektfejezetekben együtt építünk kis programokat, alkalmazva az
addig tanultakat. A 2., a 12. és a 21. fejezet projektfejezet; a többi fogalmi
fejezet.

**Az 1. fejezet** elmagyarázza, hogyan telepítsd a Rustot, hogyan írj egy
„Hello, world!” programot, és hogyan használd a Cargót, a Rust
csomagkezelőjét és build eszközét. **A 2. fejezet** gyakorlatias bevezetés a
Rust-programok írásába: egy számkitalálós játékot építesz fel benne. Itt magas
szinten tárgyaljuk a fogalmakat, a további részleteket a későbbi fejezetek
adják meg. Ha rögtön bele akarsz vetni magad a munkába, a 2. fejezet való
neked. Ha viszont különösen alapos tanuló vagy, aki szereti minden részletet
megismerni, mielőtt továbblép, akkor átugorhatod a 2. fejezetet, és rögtön a
**3. fejezettel** folytathatod, amely a Rust más programozási nyelvekéhez
hasonló képességeit veszi sorra; a 2. fejezethez pedig akkor térhetsz vissza,
amikor egy projekten szeretnéd alkalmazni a megismert részleteket.

**A 4. fejezetben** a Rust ownership rendszerét ismered meg. **Az 5. fejezet** a
structokról és a metódusokról szól. **A 6. fejezet** az enumokat, a `match`
kifejezéseket, valamint az `if let` és a `let...else` vezérlési szerkezeteket
tárgyalja. A structokkal és az enumokkal saját típusokat készíthetsz.

**A 7. fejezetben** a Rust modulrendszerével és a láthatósági szabályokkal
ismerkedsz meg, amelyekkel a kódodat és annak nyilvános programozási felületét
(API-ját) szervezheted. **A 8. fejezet** néhány gyakori kollekciós
adatszerkezetet tárgyal, amelyet a standard könyvtár nyújt: a vektorokat, a
stringeket és a hash mapeket. **A 9. fejezet** a Rust hibakezelési filozófiáját
és technikáit járja körül.

**A 10. fejezet** a generikusokba, a trait-ekbe és a lifetime-okba ás bele,
amelyekkel több típusra is alkalmazható kódot definiálhatsz. **A 11. fejezet**
teljes egészében a tesztelésről szól, amely a Rust biztonsági garanciái mellett
is szükséges ahhoz, hogy a programod logikája biztosan helyes legyen. **A 12.
fejezetben** megírjuk a saját implementációnkat a `grep` parancssori eszköz
egy részhalmazának funkcionalitásáról, amellyel fájlokban lehet szöveget
keresni. Ehhez sok olyan fogalmat felhasználunk, amelyet az előző fejezetekben
tárgyaltunk.

**A 13. fejezet** a closure-öket és az iterátorokat járja körül: a Rust olyan
képességeit, amelyek a funkcionális programozási nyelvekből származnak. **A 14.
fejezetben** alaposabban megvizsgáljuk a Cargót, és a könyvtáraid másokkal való
megosztásának bevált gyakorlatairól beszélünk. **A 15. fejezet** a standard
könyvtár által nyújtott smart pointereket tárgyalja, valamint azokat a
trait-eket, amelyek a működésüket lehetővé teszik.

**A 16. fejezetben** végigvesszük a konkurens programozás különböző modelljeit,
és arról beszélünk, hogyan segít a Rust abban, hogy félelem nélkül programozz
több szálon. **A 17. fejezetben** erre építve a Rust async és await
szintaxisát vizsgáljuk meg a taskokkal, future-ökkel és streamekkel együtt,
valamint az általuk lehetővé tett könnyűsúlyú konkurenciamodellt.

**A 18. fejezet** azt nézi meg, hogyan viszonyulnak a Rust idiómái az
objektumorientált programozás elveihez, amelyeket talán már ismersz. **A 19.
fejezet** referencia a mintákról és a mintaillesztésről, amelyek a
Rust-programokban végig erőteljes eszközei a gondolatok kifejezésének. **A 20.
fejezet** haladó témák tarka gyűjteményét tartalmazza, köztük az unsafe Rustot,
a makrókat, valamint további tudnivalókat a lifetime-okról, a trait-ekről, a
típusokról, a függvényekről és a closure-ökről.

**A 21. fejezetben** befejezünk egy projektet, amelyben egy alacsony szintű,
többszálú webszervert implementálunk!

Végül néhány függelék tartalmaz hasznos, inkább referenciaszerű információt a
nyelvről. **Az A függelék** a Rust kulcsszavait, **a B függelék** a Rust
operátorait és szimbólumait, **a C függelék** a standard könyvtár által
nyújtott származtatható trait-eket, **a D függelék** néhány hasznos fejlesztői
eszközt tárgyal, **az E függelék** pedig a Rust editionjeit magyarázza el. **Az
F függelékben** a könyv fordításait találod, **a G függelékben** pedig azt
vesszük végig, hogyan készül a Rust, és mi az a nightly Rust.

Ezt a könyvet nem lehet rosszul olvasni: ha előre akarsz ugrani, csak
nyugodtan! Ha bármi zavarossá válik, lehet, hogy vissza kell ugranod korábbi
fejezetekhez. De tedd azt, ami neked bejön.

<span id="ferris"></span>

A Rust tanulási folyamatának fontos része megtanulni elolvasni a fordító által
megjelenített hibaüzeneteket: ezek elvezetnek a működő kódhoz. Ezért sok olyan
példát is mutatunk, amely nem fordul le, és mellé azt a hibaüzenetet, amelyet a
fordító az adott helyzetben mutat. Tudd hát, hogy ha csak úgy találomra beírsz
és lefuttatsz egy példát, lehet, hogy nem fordul le! Mindig olvasd el a körülötte
lévő szöveget, hogy kiderüljön, a futtatni kívánt példának hibát kell-e adnia. A
legtöbb esetben elvezetünk a le nem forduló kód helyes változatához. Ferris is
segít megkülönböztetni azt a kódot, amelynek nem is kell működnie:

| Ferris                                                                                                           | Jelentés                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris kérdőjellel"/>            | Ez a kód nem fordul le!                      |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris égnek emelt kezekkel"/>                   | Ez a kód panicot vált ki!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris felemelt ollóval, vállat vonva"/> | Ez a kód nem a kívánt viselkedést produkálja. |

A legtöbb esetben elvezetünk a le nem forduló kód helyes változatához.

## Forráskód

Azok a forrásfájlok, amelyekből ez a könyv készül, megtalálhatók a
[GitHubon][book].

[book]: https://github.com/rust-lang/book/tree/main/src
