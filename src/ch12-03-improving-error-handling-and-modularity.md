## Refaktorálás a modularitás és a hibakezelés javítására

A programunk javításához négy olyan problémát orvosolunk, amely a program
szerkezetével és a lehetséges hibák kezelésével kapcsolatos. Először is, a
`main` függvényünk jelenleg két feladatot lát el: argumentumokat elemez és
fájlokat olvas be. Ahogy a programunk növekszik, egyre több különálló feladatot
kezel majd a `main` függvény. Minél több felelősséget kap egy függvény, annál
nehezebb átlátni, tesztelni és úgy módosítani, hogy közben ne romoljon el
valamelyik része. A legjobb, ha úgy választjuk szét a funkcionalitást, hogy
minden függvény egyetlen feladatért feleljen.

Ez a kérdés a második problémához is kapcsolódik: bár a `query` és a `file_path`
a programunk konfigurációs változói, az olyan változók, mint a `contents`, a
program logikájának végrehajtását szolgálják. Minél hosszabb lesz a `main`,
annál több változót kell hatókörbe hoznunk; és minél több változó van a
hatókörben, annál nehezebb számon tartani, melyiknek mi a szerepe. A legjobb, ha
a konfigurációs változókat egyetlen szerkezetbe csoportosítjuk, hogy világos
legyen a rendeltetésük.

A harmadik probléma az, hogy az `expect` segítségével írunk ki hibaüzenetet, ha
a fájl beolvasása nem sikerül, de a hibaüzenet csak annyit ír ki, hogy `Should
have been able to read the file`. Egy fájl beolvasása sokféleképpen
meghiúsulhat: hiányozhat például a fájl, vagy nincs jogosultságunk a
megnyitásához. Jelenleg a helyzettől függetlenül ugyanazt a hibaüzenetet írnánk
ki mindenre, ami semmilyen információt nem adna a felhasználónak!

Negyedszer, az `expect` segítségével kezelünk egy hibát, és ha a felhasználó úgy
futtatja a programunkat, hogy nem ad meg elegendő argumentumot, egy `index out
of bounds` hibát kap a Rusttól, amely nem magyarázza el világosan a problémát. A
legjobb az volna, ha a teljes hibakezelő kód egy helyen lenne, hogy a jövőbeli
karbantartóknak csak egyetlen helyen kelljen a kódot megnézniük, ha változtatni
kell a hibakezelés logikáján. Ha az összes hibakezelő kód egy helyen van, az azt
is biztosítja, hogy a végfelhasználóink számára értelmes üzeneteket írunk ki.

Foglalkozzunk ezzel a négy problémával a projektünk refaktorálásával.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Felelősségek szétválasztása bináris projektekben

Az a szervezési probléma, hogy több feladat felelősségét a `main` függvényre
bízzuk, sok bináris projektben előfordul. Ezért sok Rust-programozó hasznosnak
tartja, hogy szétválassza egy bináris program különálló felelősségeit, amikor a
`main` függvény kezd megnőni. Ez a folyamat a következő lépésekből áll:

- Bontsd szét a programodat egy _main.rs_ és egy _lib.rs_ fájlra, és mozgasd át
  a programod logikáját a _lib.rs_ fájlba.
- Amíg a parancssori argumentumokat elemző logikád kicsi, maradhat a `main`
  függvényben.
- Amikor a parancssori argumentumokat elemző logika bonyolulttá kezd válni,
  emeld ki a `main` függvényből más függvényekbe vagy típusokba.

Azoknak a felelősségeknek, amelyek a folyamat után a `main` függvényben
maradnak, a következőkre kell korlátozódniuk:

- A parancssori argumentumokat elemző logika meghívása az argumentumértékekkel
- Minden további konfiguráció beállítása
- Egy `run` függvény meghívása a _lib.rs_ fájlban
- A hiba kezelése, ha a `run` hibát ad vissza

Ez a minta a felelősségek szétválasztásáról szól: a _main.rs_ a program
futtatásáért felel, a _lib.rs_ pedig az adott feladat teljes logikájáért. Mivel
a `main` függvényt nem tudod közvetlenül tesztelni, ez a szerkezet lehetővé
teszi, hogy a program teljes logikáját tesztelhesd azáltal, hogy kimozgatod a
`main` függvényből. Az a kód, amely a `main` függvényben marad, elég rövid lesz
ahhoz, hogy elolvasással ellenőrizhessük a helyességét. Alakítsuk át a
programunkat ezt a folyamatot követve.

#### Az argumentumelemző kiemelése

Kiemeljük az argumentumok elemzését végző funkcionalitást egy függvénybe,
amelyet a `main` fog meghívni. A 12-5. lista a `main` függvény új kezdetét
mutatja, amely meghívja az új `parse_config` függvényt; ezt a függvényt az
_src/main.rs_ fájlban definiáljuk majd.

<Listing number="12-5" file-name="src/main.rs" caption="A `parse_config` függvény kiemelése a `main`-ből">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

A parancssori argumentumokat továbbra is egy vektorba gyűjtjük, de ahelyett,
hogy az 1-es indexen lévő argumentumértéket a `query`, a 2-es indexen lévőt
pedig a `file_path` változóhoz rendelnénk a `main` függvényen belül, az egész
vektort átadjuk a `parse_config` függvénynek. A `parse_config` függvény
tartalmazza azt a logikát, amely eldönti, melyik argumentum melyik változóba
kerül, majd visszaadja az értékeket a `main`-nek. A `query` és a `file_path`
változókat továbbra is a `main`-ben hozzuk létre, de a `main`-nek már nem
felelőssége eldönteni, hogyan felelnek meg egymásnak a parancssori argumentumok
és a változók.

Ez az átalakítás túlzásnak tűnhet a kicsi programunkhoz, de kis, fokozatos
lépésekben refaktorálunk. Miután elvégezted ezt a változtatást, futtasd le újra
a programot, hogy meggyőződj róla: az argumentumok elemzése továbbra is működik.
Érdemes gyakran ellenőrizni, hol tartasz, mert így könnyebb megtalálni a
problémák okát, amikor felbukkannak.

#### Konfigurációs értékek csoportosítása

Tehetünk még egy kis lépést a `parse_config` függvény további javítása felé.
Pillanatnyilag egy tuple-t adunk vissza, majd azonnal fel is bontjuk ezt a
tuple-t különálló részekre. Ez annak a jele, hogy talán még nem találtuk meg a
megfelelő absztrakciót.

Egy másik jel, amely arra utal, hogy van még mit javítani, a `parse_config`
nevében szereplő `config` rész, amely azt sugallja, hogy a két visszaadott érték
összetartozik, és mindkettő egyetlen konfigurációs érték része. Jelenleg az
adatok szerkezetében ezt a jelentést semmi más nem fejezi ki azon kívül, hogy a
két értéket egy tuple-be csoportosítottuk; helyette egyetlen structba tesszük a
két értéket, és a struct minden mezőjének beszédes nevet adunk. Ezzel
megkönnyítjük a kód jövőbeli karbantartóinak, hogy megértsék, hogyan
kapcsolódnak egymáshoz a különböző értékek, és mi a rendeltetésük.

A 12-6. lista a `parse_config` függvény javításait mutatja be.

<Listing number="12-6" file-name="src/main.rs" caption="A `parse_config` refaktorálása úgy, hogy egy `Config` struct példányát adja vissza">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Hozzáadtunk egy `Config` nevű structot, amelynek `query` és `file_path` nevű
mezői vannak. A `parse_config` szignatúrája most már jelzi, hogy egy `Config`
értéket ad vissza. A `parse_config` törzsében, ahol korábban olyan string
slice-okat adtunk vissza, amelyek az `args`-ban lévő `String` értékekre
hivatkoztak, most úgy definiáljuk a `Config`-ot, hogy birtokolt `String`
értékeket tartalmazzon. A `main`-ben lévő `args` változó az argumentumértékek
ownere, és csak kölcsönadja őket a `parse_config` függvénynek, ami azt jelenti,
hogy megsértenénk a Rust borrowing-szabályait, ha a `Config` megpróbálná átvenni
az `args` értékeinek ownershipjét.

Sokféleképpen kezelhetnénk a `String` adatokat; a legegyszerűbb – bár némileg
pazarló – út az, ha meghívjuk az értékeken a `clone` metódust. Ez az adatok
teljes másolatát elkészíti, hogy a `Config` példány birtokolhassa őket, ami több
időbe és memóriába kerül, mint a karakterlánc-adatra mutató referencia tárolása.
Az adatok klónozása viszont nagyon egyértelművé teszi a kódunkat, mert nem kell
kezelnünk a referenciák lifetime-jait; ebben a helyzetben megéri egy kis
teljesítményt feláldozni az egyszerűségért.

> ### A `clone` használatának előnyei és hátrányai
>
> Sok Rustacean körében megvan az a hajlam, hogy elkerülje a `clone`
> használatát az ownership-problémák megoldására, a futásidejű költsége miatt.
> A [13. fejezetben][ch13]<!-- ignore --> megtanulod, hogyan használhatsz
> hatékonyabb módszereket az ilyen helyzetekben. Egyelőre azonban rendben van,
> ha lemásolunk néhány karakterláncot, hogy tovább haladhassunk, mert ezeket a
> másolatokat csak egyszer készítjük el, és a fájlútvonalunk, valamint a
> keresési kifejezésünk nagyon rövid. Jobb, ha van egy működő programunk, amely
> kissé pazarló, mintha első nekifutásra próbálnánk agyonoptimalizálni a kódot.
> Ahogy egyre tapasztaltabb leszel a Rustban, könnyebb lesz rögtön a
> leghatékonyabb megoldással kezdeni, egyelőre viszont teljesen elfogadható a
> `clone` hívása.

Frissítettük a `main`-t úgy, hogy a `parse_config` által visszaadott `Config`
példányt egy `config` nevű változóba helyezze, és frissítettük azt a kódot is,
amely korábban a különálló `query` és `file_path` változókat használta, hogy
mostantól a `Config` struct mezőit használja.

Így a kódunk világosabban fejezi ki, hogy a `query` és a `file_path`
összetartozik, és hogy a rendeltetésük a program működésének beállítása. Minden
kód, amely ezeket az értékeket használja, tudja, hogy a `config` példányban
találja meg őket, a rendeltetésükről elnevezett mezőkben.

#### Konstruktor létrehozása a `Config`-hoz

Eddig kiemeltük a `main`-ből a parancssori argumentumok elemzéséért felelős
logikát, és a `parse_config` függvénybe helyeztük. Ezzel láthatóvá vált, hogy a
`query` és a `file_path` értékek összetartoznak, és ezt a kapcsolatot ki kell
fejeznünk a kódunkban. Ezután hozzáadtunk egy `Config` structot, hogy nevet
adjunk a `query` és a `file_path` közös rendeltetésének, és hogy a
`parse_config` függvényből az értékek nevét struct-mezőnevekként adhassuk
vissza.

Most tehát, hogy a `parse_config` függvény célja egy `Config` példány
létrehozása, a `parse_config`-ot egyszerű függvényből egy `new` nevű függvénnyé
alakíthatjuk, amely a `Config` structhoz kapcsolódik. Ez a változtatás
idiomatikusabbá teszi a kódot. A standard könyvtár típusaiból, például a
`String`-ből úgy hozhatunk létre példányokat, hogy meghívjuk a `String::new`
függvényt. Hasonlóképpen, ha a `parse_config`-ot a `Config`-hoz kapcsolódó `new`
függvénnyé alakítjuk, a `Config::new` hívásával tudunk majd `Config` példányokat
létrehozni. A 12-7. lista mutatja a szükséges változtatásokat.

<Listing number="12-7" file-name="src/main.rs" caption="A `parse_config` átalakítása `Config::new` függvénnyé">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Frissítettük a `main`-t ott, ahol a `parse_config`-ot hívtuk, hogy helyette a
`Config::new` függvényt hívja. A `parse_config` nevét `new`-ra változtattuk, és
áthelyeztük egy `impl` blokkba, amely a `new` függvényt a `Config`-hoz
kapcsolja. Próbáld meg újra lefordítani ezt a kódot, hogy megbizonyosodj róla:
működik.

### A hibakezelés javítása

Most a hibakezelésünk javításán dolgozunk. Emlékezz vissza: ha megpróbáljuk
elérni az `args` vektor 1-es vagy 2-es indexén lévő értékeket, a program panicot
vált ki, ha a vektor háromnál kevesebb elemet tartalmaz. Próbáld meg lefuttatni
a programot mindenféle argumentum nélkül; így fog kinézni:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Az `index out of bounds: the len is 1 but the index is 1` sor programozóknak
szánt hibaüzenet. A végfelhasználóinknak nem segít megérteni, mit kellene
tenniük helyette. Javítsuk ezt ki most.

#### A hibaüzenet javítása

A 12-8. listában hozzáadunk egy ellenőrzést a `new` függvényhez, amely
megvizsgálja, hogy a slice elég hosszú-e, mielőtt az 1-es és a 2-es indexhez
nyúlnánk. Ha a slice nem elég hosszú, a program panicot vált ki, és jobb
hibaüzenetet jelenít meg.

<Listing number="12-8" file-name="src/main.rs" caption="Az argumentumok számának ellenőrzése">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Ez a kód hasonló [a `Guess::new` függvényhez, amelyet a 9-13. listában
írtunk][ch9-custom-types]<!-- ignore -->, ahol a `panic!` makrót hívtuk, amikor
a `value` argumentum az érvényes értékek tartományán kívül esett. Itt nem egy
értéktartományt ellenőrzünk, hanem azt, hogy az `args` hossza legalább `3`, és a
függvény többi része már abból indulhat ki, hogy ez a feltétel teljesült. Ha az
`args` háromnál kevesebb elemet tartalmaz, ez a feltétel `true` lesz, és
meghívjuk a `panic!` makrót, hogy azonnal befejezzük a programot.

Ezzel a néhány plusz kódsorral a `new`-ban futtassuk le újra a programot
argumentumok nélkül, hogy lássuk, hogyan néz ki most a hiba:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Ez a kimenet jobb: immár van egy értelmes hibaüzenetünk. Van benne azonban
fölösleges információ is, amelyet nem szeretnénk a felhasználóink elé tárni.
Talán az a technika, amelyet a 9-13. listában használtunk, itt nem a legjobb: a
`panic!` hívása inkább programozási hibához illik, mint használati problémához,
[ahogy a 9. fejezetben tárgyaltuk][ch9-error-guidelines]<!-- ignore -->.
Helyette azt a másik technikát használjuk, amelyet a 9. fejezetben tanultál –
egy [`Result` visszaadását][ch9-result]<!-- ignore -->, amely vagy a sikert,
vagy a hibát jelzi.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### `Result` visszaadása a `panic!` hívása helyett

Ehelyett visszaadhatunk egy `Result` értéket, amely sikeres esetben egy `Config`
példányt tartalmaz, hiba esetén pedig leírja a problémát. A függvény nevét is
megváltoztatjuk `new`-ról `build`-re, mert sok programozó elvárja, hogy a `new`
függvények soha ne hibázzanak. Amikor a `Config::build` a `main`-nel kommunikál,
a `Result` típussal jelezhetjük, hogy probléma történt. Ezután módosíthatjuk a
`main`-t úgy, hogy az `Err` variánst a felhasználóink számára gyakorlatiasabb
hibává alakítsa, a `thread 'main'` és a `RUST_BACKTRACE` kifejezéseket
tartalmazó körítés nélkül, amelyet a `panic!` hívása okoz.

A 12-9. lista mutatja azokat a változtatásokat, amelyeket a most már
`Config::build` néven hívott függvény visszatérési értékén, valamint a függvény
törzsén kell elvégeznünk ahhoz, hogy `Result` értéket adjon vissza. Vedd
figyelembe, hogy ez addig nem fordul le, amíg a `main`-t is nem frissítjük, amit
a következő listában teszünk meg.

<Listing number="12-9" file-name="src/main.rs" caption="`Result` visszaadása a `Config::build`-ból">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

A `build` függvényünk egy `Result` értéket ad vissza, sikeres esetben egy
`Config` példánnyal, hiba esetén pedig egy string literállal. A hibaértékeink
mindig olyan string literálok lesznek, amelyeknek `'static` a lifetime-juk.

Két változtatást végeztünk a függvény törzsében: ahelyett, hogy a `panic!`
makrót hívnánk, amikor a felhasználó nem ad át elegendő argumentumot, most egy
`Err` értéket adunk vissza, a `Config` visszatérési értéket pedig egy `Ok`-ba
csomagoltuk. Ezekkel a változtatásokkal a függvény megfelel az új
típusszignatúrájának.

Ha a `Config::build` egy `Err` értéket ad vissza, az lehetővé teszi a `main`
függvénynek, hogy kezelje a `build` függvény által visszaadott `Result` értéket,
és hiba esetén tisztábban lépjen ki a folyamatból.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### A `Config::build` hívása és a hibák kezelése

Ahhoz, hogy kezeljük a hibás esetet, és felhasználóbarát üzenetet írjunk ki,
frissítenünk kell a `main`-t, hogy kezelje a `Config::build` által visszaadott
`Result` értéket, ahogy a 12-10. listában látható. Emellett a `panic!`-tól azt a
felelősséget is elvesszük, hogy nem nulla hibakóddal lépjen ki a parancssori
eszközből, és helyette saját kezűleg valósítjuk meg. A nem nulla kilépési
állapot bevett szokás annak jelzésére a programunkat meghívó folyamat felé, hogy
a program hibás állapotban fejeződött be.

<Listing number="12-10" file-name="src/main.rs" caption="Kilépés hibakóddal, ha a `Config` felépítése nem sikerül">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Ebben a listában olyan metódust használtunk, amelyet még nem tárgyaltunk
részletesen: az `unwrap_or_else` metódust, amelyet a standard könyvtár definiál
a `Result<T, E>` típuson. Az `unwrap_or_else` használatával egyedi, nem a
`panic!`-ra épülő hibakezelést határozhatunk meg. Ha a `Result` egy `Ok` érték,
ennek a metódusnak a viselkedése hasonló az `unwrap`-éhoz: visszaadja azt a
belső értéket, amelyet az `Ok` becsomagol. Ha viszont az érték egy `Err` érték,
ez a metódus meghívja a closure-ben lévő kódot, vagyis azt a névtelen függvényt,
amelyet mi definiálunk, és argumentumként átadunk az `unwrap_or_else`
metódusnak. A closure-öket részletesebben a [13.
fejezetben][ch13]<!-- ignore --> tárgyaljuk. Egyelőre csak azt kell tudnod, hogy
az `unwrap_or_else` átadja az `Err` belső értékét – ami ebben az esetben a `"not
enough arguments"` statikus karakterlánc, amelyet a 12-9. listában adtunk hozzá
– a closure-ünknek, a függőleges vonalak között megjelenő `err` argumentumban. A
closure-ben lévő kód futáskor használhatja az `err` értéket.

Hozzáadtunk egy új `use` sort, hogy hatókörbe hozzuk a `process` modult a
standard könyvtárból. A closure-ben lévő kód, amely hiba esetén lefut, mindössze
két sor: kiírjuk az `err` értéket, majd meghívjuk a `process::exit` függvényt. A
`process::exit` függvény azonnal leállítja a programot, és visszaadja azt a
számot, amelyet kilépési állapotkódként átadtunk neki. Ez hasonló ahhoz a
`panic!`-alapú kezeléshez, amelyet a 12-8. listában használtunk, de már nem
kapjuk meg az összes fölösleges kimenetet. Próbáljuk ki:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Nagyszerű! Ez a kimenet sokkal barátságosabb a felhasználóink számára.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### A logika kiemelése a `main`-ből

Most, hogy befejeztük a konfigurációelemzés refaktorálását, forduljunk a program
logikája felé. Ahogy a [„Felelősségek szétválasztása bináris
projektekben”](#separation-of-concerns-for-binary-projects)<!-- ignore -->
részben leírtuk, kiemelünk egy `run` nevű függvényt, amely a `main` függvényben
jelenleg meglévő teljes logikát tartalmazza majd, azt kivéve, ami a konfiguráció
beállításához vagy a hibák kezeléséhez tartozik. Amikor elkészülünk, a `main`
függvény tömör lesz, és ránézésre ellenőrizhető, a többi logikára pedig
teszteket írhatunk.

A 12-11. lista a `run` függvény kiemelésének kicsi, fokozatos javítását mutatja
be.

<Listing number="12-11" file-name="src/main.rs" caption="A program logikájának többi részét tartalmazó `run` függvény kiemelése">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

A `run` függvény most már a `main` teljes megmaradt logikáját tartalmazza, a
fájl beolvasásától kezdve. A `run` függvény argumentumként kapja a `Config`
példányt.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Hibák visszaadása a `run`-ból

Miután a program megmaradt logikáját a `run` függvénybe választottuk szét,
javíthatjuk a hibakezelést, ahogy a `Config::build` esetében tettük a 12-9.
listában. Ahelyett, hogy hagynánk a programot panicot kiváltani az `expect`
hívásával, a `run` függvény egy `Result<T, E>` értéket ad vissza, ha valami
elromlik. Így tovább vonhatjuk össze a hibakezelés körüli logikát a `main`-ben,
mégpedig felhasználóbarát módon. A 12-12. lista mutatja azokat a
változtatásokat, amelyeket a `run` szignatúráján és törzsén el kell végeznünk.

<Listing number="12-12" file-name="src/main.rs" caption="A `run` függvény átalakítása úgy, hogy `Result` értéket adjon vissza">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Itt három jelentős változtatást végeztünk. Először is, a `run` függvény
visszatérési típusát `Result<(), Box<dyn Error>>`-ra változtattuk. Ez a függvény
korábban a unit típust, a `()`-t adta vissza, és ezt megtartjuk az `Ok` esetben
visszaadott értékként.

A hibatípushoz a `Box<dyn Error>` trait objectet használtuk (a
`std::error::Error` típust pedig egy `use` utasítással hoztuk hatókörbe a fájl
elején). A trait objecteket a [18. fejezetben][ch18]<!-- ignore --> tárgyaljuk.
Egyelőre csak azt kell tudni, hogy a `Box<dyn Error>` azt jelenti: a függvény
olyan típust ad vissza, amely implementálja az `Error` traitet, de nem kell
megadnunk, pontosan milyen típusú lesz a visszatérési érték. Ez rugalmasságot ad
nekünk ahhoz, hogy különböző hibaesetekben különböző típusú hibaértékeket
adhassunk vissza. A `dyn` kulcsszó a _dynamic_ (dinamikus) szó rövidítése.

Másodszor, elhagytuk az `expect` hívását a `?` operátor javára, ahogy arról a
[9. fejezetben][ch9-question-mark]<!-- ignore --> beszéltünk. Ahelyett, hogy
hiba esetén panicot váltana ki, a `?` visszaadja a hibaértéket az aktuális
függvényből, hogy a hívó kezelhesse.

Harmadszor, a `run` függvény most sikeres esetben egy `Ok` értéket ad vissza. A
`run` függvény sikeres típusát `()`-ként adtuk meg a szignatúrában, ami azt
jelenti, hogy a unit típus értékét be kell csomagolnunk az `Ok` értékbe. Ez az
`Ok(())` szintaxis elsőre kissé furcsán nézhet ki. A `()` ilyen használata
viszont az idiomatikus módja annak, hogy jelezzük: a `run` függvényt csak a
mellékhatásaiért hívjuk meg; nem ad vissza olyan értéket, amelyre szükségünk
volna.

Ha lefuttatod ezt a kódot, le fog fordulni, de egy figyelmeztetést jelenít meg:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

A Rust azt mondja nekünk, hogy a kódunk figyelmen kívül hagyta a `Result`
értéket, és a `Result` érték hiba bekövetkeztét jelezheti. Mi viszont nem
ellenőrizzük, hogy történt-e hiba, és a fordító emlékeztet minket rá, hogy
valószínűleg valamilyen hibakezelő kódot akartunk ide írni! Orvosoljuk most ezt
a problémát.

#### A `run` által visszaadott hibák kezelése a `main`-ben

Ellenőrizzük a hibákat, és olyan technikával kezeljük őket, amely hasonlít arra,
amelyet a `Config::build` esetében használtunk a 12-10. listában, de van egy
apró eltérés:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Az `unwrap_or_else` helyett az `if let` szerkezetet használjuk annak
ellenőrzésére, hogy a `run` `Err` értéket ad-e vissza, és hogy meghívjuk a
`process::exit(1)` függvényt, ha igen. A `run` függvény nem ad vissza olyan
értéket, amelyet ugyanúgy `unwrap`-elni akarnánk, ahogy a `Config::build` adja
vissza a `Config` példányt. Mivel a `run` sikeres esetben `()`-t ad vissza,
minket csak a hiba észlelése érdekel, ezért nincs szükségünk az
`unwrap_or_else`-re ahhoz, hogy visszaadja a kicsomagolt értéket, amely úgyis
csak `()` lenne.

Az `if let` és az `unwrap_or_else` törzse mindkét esetben ugyanaz: kiírjuk a
hibát, és kilépünk.

### A kód szétbontása library crate-be

A `minigrep`-projektünk eddig jól fest! Most szétbontjuk az _src/main.rs_ fájlt,
és egy részét áthelyezzük az _src/lib.rs_ fájlba. Így tesztelhetjük a kódot, és
az _src/main.rs_ fájlnak kevesebb felelőssége lesz.

Definiáljuk a szövegben való keresésért felelős kódot az _src/lib.rs_ fájlban az
_src/main.rs_ helyett, így mi (vagy bárki más, aki a `minigrep` könyvtárunkat
használja) a `minigrep` binárisunkon kívül más környezetekből is meghívhatjuk a
kereső függvényt.

Először definiáljuk a `search` függvény szignatúráját az _src/lib.rs_ fájlban,
ahogy a 12-13. listában látható, olyan törzzsel, amely az `unimplemented!`
makrót hívja. A szignatúrát részletesebben akkor magyarázzuk el, amikor
kitöltjük az implementációt.

<Listing number="12-13" file-name="src/lib.rs" caption="A `search` függvény definiálása az *src/lib.rs* fájlban">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

A függvénydefiníción a `pub` kulcsszót használtuk, hogy a `search` függvényt a
library crate-ünk publikus API-jának részévé tegyük. Most már van egy library
crate-ünk, amelyet használhatunk a binary crate-ünkből, és amelyet tesztelhetünk
is!

Most hatókörbe kell hoznunk az _src/lib.rs_ fájlban definiált kódot az
_src/main.rs_ binary crate-jében, és meg kell hívnunk, ahogy a 12-14. listában
látható.

<Listing number="12-14" file-name="src/main.rs" caption="A `minigrep` library crate `search` függvényének használata az *src/main.rs* fájlban">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Hozzáadunk egy `use minigrep::search` sort, hogy a `search` függvényt a library
crate-ből a binary crate hatókörébe hozzuk. Ezután a `run` függvényben ahelyett,
hogy kiírnánk a fájl tartalmát, meghívjuk a `search` függvényt, és
argumentumként átadjuk neki a `config.query` értéket, valamint a `contents`
értéket. Ezután a `run` egy `for` ciklussal kiírja a `search` által visszaadott
minden olyan sort, amely illeszkedett a keresési kifejezésre. Ez egyben jó
alkalom arra is, hogy eltávolítsuk a `main` függvényből azokat a `println!`
hívásokat, amelyek a keresési kifejezést és a fájlútvonalat írták ki, hogy a
programunk csak a keresés eredményeit írja ki (ha nem történik hiba).

Vedd figyelembe, hogy a keresést végző függvény minden eredményt egy vektorba
gyűjt, amelyet visszaad, mielőtt bármilyen kiírás történne. Ez az implementáció
lassan jelenítheti meg az eredményeket nagy fájlokban való kereséskor, mert az
eredmények nem íródnak ki, ahogy megtaláljuk őket; a 13. fejezetben megbeszéljük
ennek egy lehetséges javítási módját iterátorok segítségével.

Hűha! Ez sok munka volt, de megalapoztuk a jövőbeli sikerünket. Mostantól sokkal
könnyebb kezelni a hibákat, és modulárisabbá tettük a kódot. Innentől szinte
minden munkánkat az _src/lib.rs_ fájlban végezzük.

Használjuk ki ezt az újonnan szerzett modularitást azzal, hogy olyasmit teszünk,
ami a régi kóddal nehéz lett volna, az újjal viszont könnyű: írunk néhány
tesztet!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
