## `panic!` vagy mégsem `panic!`? {#to-panic-or-not-to-panic}

Hogyan döntöd el hát, mikor kell `panic!`-ot hívnod, és mikor kell `Result`-ot
visszaadnod? Ha a kód panicot vált ki, nincs mód a helyreállásra. Bármelyik
hibahelyzetben hívhatnál `panic!`-ot, akár van lehetőség a helyreállásra, akár
nincs, csakhogy ezzel a hívó kód helyett döntenéd el, hogy a helyzet
helyrehozhatatlan. Ha a `Result` érték visszaadását választod, választási
lehetőséget adsz a hívó kódnak. A hívó kód dönthet úgy, hogy a saját
helyzetéhez illő módon próbál helyreállni, vagy úgy is, hogy az `Err` érték
ebben az esetben helyrehozhatatlan, így hívhat `panic!`-ot, és a helyrehozható
hibádat helyrehozhatatlanná alakíthatja. Ezért a `Result` visszaadása jó
alapértelmezett választás, amikor olyan függvényt definiálsz, amely elbukhat.

Bizonyos helyzetekben – például példakódban, prototípuskódban és tesztekben –
helyénvalóbb olyan kódot írni, amely panicot vált ki, ahelyett hogy `Result`-ot
adna vissza. Nézzük meg, miért, majd beszéljünk azokról a helyzetekről,
amelyekben a fordító nem tudja megállapítani, hogy a hiba lehetetlen, te
viszont emberként igen. A fejezetet néhány általános irányelvvel zárjuk arról,
hogyan dönts a panicról library kódban.

### Példák, prototípuskód és tesztek

Amikor egy fogalom szemléltetésére példát írsz, a robusztus hibakezelő kód
beemelése kevésbé érthetővé teheti a példát. A példákban magától értetődő, hogy
egy olyan metódus hívása, mint az `unwrap`, amely panicot válthat ki, csupán
helykitöltő arra a módra, ahogyan az alkalmazásoddal kezeltetni szeretnéd a
hibákat – ez pedig attól függően változhat, mit csinál a kódod többi része.

Hasonlóképpen az `unwrap` és az `expect` metódus nagyon kézre áll
prototípuskészítés közben, amikor még nem állsz készen annak eldöntésére,
hogyan kezeld a hibákat. Világos jelöléseket hagynak a kódodban arra az időre,
amikor készen állsz a programod robusztusabbá tételére.

Ha egy metódushívás elbukik egy tesztben, azt szeretnéd, hogy az egész teszt
elbukjon, még akkor is, ha nem az a metódus a tesztelt funkcionalitás. Mivel a
`panic!` az a mód, ahogyan egy teszt bukottnak minősül, az `unwrap` vagy az
`expect` hívása pontosan az, aminek történnie kell.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Amikor több információd van, mint a fordítónak

Az `expect` hívása akkor is helyénvaló, ha van valamilyen más logikád, amely
biztosítja, hogy a `Result` `Ok` értéket fog tartalmazni, csakhogy ezt a
logikát a fordító nem érti. Ettől még kapsz egy `Result` értéket, amelyet
kezelned kell: a hívott művelet általánosságban továbbra is elbukhat, még ha a
te konkrét helyzetedben logikailag lehetetlen is. Ha a kód kézi átvizsgálásával
biztosítani tudod, hogy soha nem kapsz `Err` variánst, teljesen elfogadható az
`expect` hívása, és az, hogy az argumentum szövegében dokumentálod, miért
gondolod, hogy soha nem lesz `Err` variánsod. Íme egy példa:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Egy `IpAddr` példányt hozunk létre egy beégetett string feldolgozásával.
Látjuk, hogy a `127.0.0.1` érvényes IP-cím, ezért itt elfogadható az `expect`
használata. Attól azonban, hogy egy beégetett, érvényes stringünk van, még nem
változik meg a `parse` metódus visszatérési típusa: továbbra is `Result`
értéket kapunk, és a fordító továbbra is arra kényszerít, hogy úgy kezeljük a
`Result`-ot, mintha az `Err` variáns is lehetséges volna, mert a fordító nem
elég okos ahhoz, hogy lássa: ez a string mindig érvényes IP-cím. Ha az
IP-címet tartalmazó string a felhasználótól érkezne ahelyett, hogy a programba
lenne beégetve, és így _valóban_ lenne hibalehetőség, mindenképpen
robusztusabb módon szeretnénk kezelni a `Result`-ot. Ha megemlítjük azt a
feltevést, hogy ez az IP-cím be van égetve, az arra ösztönöz majd minket, hogy
az `expect`-et jobb hibakezelő kódra cseréljük, ha a jövőben más forrásból kell
megszereznünk az IP-címet.

### Hibakezelési irányelvek {#guidelines-for-error-handling}

Ajánlott panicot kiváltani a kódodban akkor, ha előfordulhat, hogy a kód rossz
állapotba kerül. Ebben az összefüggésben _rossz állapotról_ akkor beszélünk,
amikor valamilyen feltevés, garancia, szerződés vagy invariáns sérül – például
amikor érvénytelen, ellentmondó vagy hiányzó értékek jutnak el a kódodhoz –, és
emellett az alábbiak közül egy vagy több is teljesül:

- A rossz állapot valami váratlan, nem pedig olyasmi, ami időnként
  valószínűleg megtörténik, mint amikor a felhasználó rossz formátumban ad meg
  adatot.
- Az ezen a ponton túli kódodnak arra kell támaszkodnia, hogy nincs ebben a
  rossz állapotban, ahelyett hogy minden lépésnél ellenőrizné a problémát.
- Nincs jó mód arra, hogy ezt az információt a használt típusokba kódold. Egy
  példán keresztül mutatjuk meg, mire gondolunk, a 18. fejezet [„Állapotok és
  viselkedés kódolása típusokként”][encoding]<!-- ignore --> című részében.

Ha valaki meghívja a kódodat, és értelmetlen értékeket ad át, a legjobb, ha
lehetőség szerint hibát adsz vissza, hogy a library felhasználója eldönthesse,
mit szeretne tenni ebben az esetben. Azokban az esetekben viszont, amikor a
folytatás nem lenne biztonságos vagy egyenesen káros volna, a legjobb választás
az lehet, hogy `panic!`-ot hívsz, és figyelmezteted a libraryd használóját a
kódjában lévő hibára, hogy még a fejlesztés során kijavíthassa. Hasonlóképpen
gyakran helyénvaló a `panic!`, ha olyan külső kódot hívsz, amely nincs a te
irányításod alatt, és érvénytelen állapotot ad vissza, amit sehogy sem tudsz
kijavítani.

Amikor viszont a hiba várható, helyénvalóbb `Result`-ot visszaadni, mint
`panic!`-ot hívni. Ilyen például, amikor egy parser hibás formátumú adatot kap,
vagy amikor egy HTTP-kérés olyan státuszt ad vissza, amely azt jelzi, hogy
elérted a kéréskorlátot. Ezekben az esetekben a `Result` visszaadása azt jelzi,
hogy a hiba várható lehetőség, és a hívó kódnak kell eldöntenie, hogyan kezeli.

Ha a kódod olyan műveletet végez, amely veszélybe sodorhatja a felhasználót,
amennyiben érvénytelen értékekkel hívják meg, a kódodnak először ellenőriznie
kell, hogy az értékek érvényesek-e, és panicot kell kiváltania, ha nem azok.
Ennek elsősorban biztonsági okai vannak: az érvénytelen adatokon végzett
műveletek sebezhetőségeknek tehetik ki a kódodat. Főként ezért hív `panic!`-ot
a standard könyvtár, ha határon kívüli memóriaelérést kísérelsz meg: olyan
memóriához hozzáférni, amely nem az aktuális adatszerkezethez tartozik, gyakori
biztonsági probléma. A függvényeknek gyakran vannak _szerződéseik_: a
viselkedésük csak akkor garantált, ha a bemenetek megfelelnek bizonyos
követelményeknek. Van értelme panicot kiváltani a szerződés megsértésekor,
mert a szerződés megsértése mindig a hívó oldalán lévő hibára utal, és nem
olyan hiba, amelyet a hívó kóddal kifejezetten kezeltetni szeretnél. Valójában
nincs is ésszerű mód arra, hogy a hívó kód helyreálljon; a hívó
_programozóknak_ kell kijavítaniuk a kódot. Egy függvény szerződéseit –
különösen, ha a megsértésük panicot okoz – el kell magyarázni a függvény
API-dokumentációjában.

Ha viszont az összes függvényedben rengeteg hibaellenőrzés lenne, az
bőbeszédű és bosszantó volna. Szerencsére a Rust típusrendszerét (és így a
fordító által végzett típusellenőrzést) használhatod arra, hogy sok ellenőrzést
elvégezzen helyetted. Ha a függvényednek egy adott típusú paramétere van, a
kódod logikájával úgy haladhatsz tovább, hogy tudod: a fordító már
gondoskodott róla, hogy érvényes értéked legyen. Ha például `Option` helyett
egy konkrét típusod van, a programod _valamit_ vár, nem pedig _semmit_. A
kódodnak ekkor nem kell két esetet kezelnie a `Some` és a `None` variánsra:
csak egyetlen esete lesz, amikor biztosan van érték. Az a kód, amely semmit
próbálna átadni a függvényednek, le sem fordul, így a függvényednek futásidőben
nem is kell erre az esetre ellenőriznie. Egy másik példa az előjel nélküli
egész típus, például az `u32` használata, amely biztosítja, hogy a paraméter
soha nem negatív.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Egyedi típusok az érvényesítéshez

Vigyük egy lépéssel tovább azt az ötletet, hogy a Rust típusrendszerével
biztosítjuk az érvényes érték meglétét, és nézzük meg, hogyan hozhatunk létre
egyedi típust az érvényesítéshez. Emlékezz vissza a 2. fejezet kitalálós
játékára, amelyben a kódunk arra kérte a felhasználót, hogy tippeljen meg egy 1
és 100 közötti számot. Sosem ellenőriztük, hogy a felhasználó tippje e két szám
közé esik-e, mielőtt összevetettük volna a titkos számunkkal; csak azt
ellenőriztük, hogy a tipp pozitív. Ebben az esetben a következmények nem voltak
túl súlyosak: a „Too high” vagy „Too low” kimenetünk így is helyes lett volna.
Hasznos fejlesztés lenne azonban a felhasználót az érvényes tippek felé
terelni, és másképp viselkedni, amikor a felhasználó tartományon kívüli számot
tippel, mint amikor például betűket ír be.

Ennek egyik módja az lenne, hogy a tippet `i32`-ként dolgozzuk fel a puszta
`u32` helyett, hogy az esetleges negatív számokat is megengedjük, majd
hozzáadunk egy ellenőrzést arra, hogy a szám a tartományon belül van-e, így:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Az `if` kifejezés ellenőrzi, hogy az értékünk kívül esik-e a tartományon,
tájékoztatja a felhasználót a problémáról, és meghívja a `continue`-t, hogy
elindítsa a ciklus következő iterációját, és új tippet kérjen. Az `if` kifejezés
után folytathatjuk a `guess` és a titkos szám összehasonlítását, tudva, hogy a
`guess` 1 és 100 közé esik.

Ez azonban nem ideális megoldás: ha teljesen kritikus volna, hogy a program
csak 1 és 100 közötti értékekkel dolgozzon, és sok függvény támasztaná ezt a
követelményt, fárasztó lenne minden függvénybe ilyen ellenőrzést tenni (és a
teljesítményre is hatással lehetne).

Ehelyett létrehozhatunk egy új típust egy külön modulban, és az érvényesítéseket
egy olyan függvénybe tehetjük, amely a típus egy példányát hozza létre, ahelyett
hogy az érvényesítéseket mindenütt megismételnénk. Így biztonságos, ha a
függvények az új típust használják a szignatúrájukban, és magabiztosan
használják a kapott értékeket. A 9-13. listázás egy módot mutat a `Guess` típus
definiálására, amely csak akkor hoz létre `Guess` példányt, ha a `new` függvény
1 és 100 közötti értéket kap.

<Listing number="9-13" caption="Egy `Guess` típus, amely csak 1 és 100 közötti értékekkel folytatja" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Vedd figyelembe, hogy a *src/guessing_game.rs* fájlban lévő kód feltételezi,
hogy a *src/lib.rs* fájlban szerepel egy `mod guessing_game;` modul-deklaráció,
amelyet itt nem mutattunk meg. Ebben az új modulfájlban definiálunk egy `Guess`
nevű structot, amelynek van egy `value` nevű mezője, ez pedig egy `i32`-t tárol.
Itt fog tárolódni a szám.

Ezután implementálunk egy `new` nevű asszociált függvényt a `Guess`-en, amely
`Guess` értékek példányait hozza létre. A `new` függvényt úgy definiáljuk, hogy
egyetlen `value` nevű, `i32` típusú paramétere legyen, és `Guess`-t adjon
vissza. A `new` függvény törzsében lévő kód megvizsgálja a `value`-t, hogy 1 és
100 közé esik-e. Ha a `value` nem megy át ezen a teszten, `panic!` hívást
hajtunk végre, ami figyelmezteti a hívó kódot író programozót, hogy van egy
javítandó hiba a kódjában, mert egy ezen a tartományon kívüli `value`-jú `Guess`
létrehozása megsértené azt a szerződést, amelyre a `Guess::new` támaszkodik.
Azokat a feltételeket, amelyek mellett a `Guess::new` panicot válthat ki, a
nyilvános API-dokumentációjában érdemes tárgyalni; a 14. fejezetben szólunk
majd azokról a dokumentációs konvenciókról, amelyekkel az általad készített
API-dokumentációban jelezheted a `panic!` lehetőségét. Ha a `value` átmegy a
teszten, létrehozunk egy új `Guess`-t, amelynek a `value` mezőjét a `value`
paraméterre állítjuk, és visszaadjuk a `Guess`-t.

Ezután implementálunk egy `value` nevű metódust, amely kölcsönveszi a
`self`-et, nincs más paramétere, és `i32`-t ad vissza. Az ilyen metódust néha
_getternek_ nevezik, mert az a célja, hogy valamilyen adatot kiolvasson a
mezőkből, és visszaadja. Erre a nyilvános metódusra azért van szükség, mert a
`Guess` struct `value` mezője privát. Fontos, hogy a `value` mező privát
legyen, így a `Guess` structot használó kód nem állíthatja be közvetlenül a
`value`-t: a `guessing_game` modulon kívüli kódnak _muszáj_ a `Guess::new`
függvényt használnia egy `Guess` példány létrehozásához, ezzel biztosítva, hogy
egy `Guess`-nek semmiképp ne lehessen olyan `value`-ja, amelyet a `Guess::new`
függvény feltételei ne ellenőriztek volna.

Egy olyan függvény, amelynek paramétere csak 1 és 100 közötti szám, vagy amely
csak ilyet ad vissza, ezután a szignatúrájában deklarálhatja, hogy `i32` helyett
`Guess`-t vesz át vagy ad vissza, és a törzsében nem kellene további
ellenőrzéseket végeznie.

## Összefoglalás

A Rust hibakezelési eszközeit arra tervezték, hogy robusztusabb kód írásában
segítsenek. A `panic!` makró azt jelzi, hogy a programod olyan állapotba
került, amelyet nem tud kezelni, és lehetővé teszi, hogy leállítsd a
folyamatot, ahelyett hogy érvénytelen vagy hibás értékekkel próbálnál
továbbhaladni. A `Result` enum a Rust típusrendszerét használja annak
jelzésére, hogy egy művelet olyan módon hiúsulhat meg, amelyből a kódod helyre
tud állni. A `Result` segítségével a kódodat hívó kóddal is közölheted, hogy
neki is kezelnie kell a lehetséges sikert vagy hibát. Ha a `panic!`-ot és a
`Result`-ot a megfelelő helyzetekben használod, a kódod megbízhatóbb lesz az
elkerülhetetlen problémákkal szemben.

Most, hogy láttad, milyen hasznos módokon használja a standard könyvtár a
generikusokat az `Option` és a `Result` enummal, beszéljünk arról, hogyan
működnek a generikusok, és hogyan használhatod őket a kódodban.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
