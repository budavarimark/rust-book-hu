# Egy kitalálós játék programozása

Vágjunk bele a Rustba egy közös, gyakorlati projekttel! Ez a fejezet néhány
gyakori Rust-fogalmat mutat be azzal, hogy megmutatja, hogyan használd őket egy
valódi programban. Megismerkedsz a `let`-tel, a `match`-csel, a metódusokkal, az
asszociált függvényekkel, a külső crate-ekkel és még sok mással! A következő
fejezetekben részletesebben is körüljárjuk ezeket a gondolatokat. Ebben a
fejezetben csak az alapokat gyakorlod.

Egy klasszikus kezdő programozási feladatot implementálunk: egy kitalálós
játékot. Így működik: a program generál egy véletlen egész számot 1 és 100
között. Ezután felszólítja a játékost, hogy adjon meg egy tippet. Miután
megkapta a tippet, a program jelzi, hogy a tipp túl alacsony vagy túl magas
volt-e. Ha a tipp helyes, a játék kiír egy gratuláló üzenetet, és kilép.

## Új projekt létrehozása

Új projekt létrehozásához lépj be a _projects_ könyvtárba, amelyet az 1.
fejezetben hoztál létre, és készíts egy új projektet a Cargo segítségével, így:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Az első parancs, a `cargo new`, a projekt nevét (`guessing_game`) kapja meg első
argumentumként. A második parancs átvált az új projekt könyvtárába.

Nézd meg a generált _Cargo.toml_ fájlt:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Ahogy az 1. fejezetben láttad, a `cargo new` generál neked egy „Hello, world!”
programot. Nézd meg a _src/main.rs_ fájlt:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Most pedig fordítsuk le ezt a „Hello, world!” programot, és ugyanabban a
lépésben futtassuk is a `cargo run` paranccsal:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

A `run` parancs akkor jön jól, amikor gyorsan kell iterálnod egy projekten,
ahogy azt ebben a játékban is tesszük: minden iterációt gyorsan kipróbálunk,
mielőtt továbblépnénk a következőre.

Nyisd meg újra a _src/main.rs_ fájlt. Az összes kódot ebbe a fájlba fogod írni.

## Egy tipp feldolgozása

A kitalálós játék programjának első része bekéri a felhasználói bemenetet,
feldolgozza azt, és ellenőrzi, hogy a bemenet a várt formában van-e. Kezdésként
engedjük meg a játékosnak, hogy megadjon egy tippet. Írd be a 2-1. listában
látható kódot a _src/main.rs_ fájlba.

<Listing number="2-1" file-name="src/main.rs" caption="Kód, amely bekér egy tippet a felhasználótól, és kiírja azt">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Ez a kód rengeteg információt tartalmaz, úgyhogy nézzük végig soronként. Ahhoz,
hogy felhasználói bemenetet szerezzünk, majd az eredményt kimenetként kiírjuk,
be kell hoznunk a hatókörbe az `io` bemeneti/kimeneti könyvtárat. Az `io`
könyvtár a standard könyvtárból származik, amelyet `std` néven ismerünk:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Alapértelmezés szerint a Rustnak van egy készlete a standard könyvtárban
definiált elemekből, amelyeket minden program hatókörébe behoz. Ezt a készletet
_prelude_-nak hívjuk, és mindent megnézhetsz benne [a standard könyvtár
dokumentációjában][prelude].

Ha egy típus, amelyet használni szeretnél, nincs benne a prelude-ban, akkor azt
a típust kifejezetten be kell hoznod a hatókörbe egy `use` utasítással. A
`std::io` könyvtár használata számos hasznos képességet ad neked, köztük azt a
lehetőséget, hogy felhasználói bemenetet fogadj.

Ahogy az 1. fejezetben láttad, a `main` függvény a program belépési pontja:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Az `fn` szintaxis új függvényt deklarál; a zárójelek, `()`, azt jelzik, hogy
nincsenek paraméterek; a nyitó kapcsos zárójel, `{`, pedig elkezdi a függvény
törzsét.

Szintén az 1. fejezetben tanultad, hogy a `println!` egy makró, amely egy
sztringet ír ki a képernyőre:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Ez a kód egy felszólítást ír ki, amely elmondja, mi ez a játék, és bemenetet kér
a felhasználótól.

### Értékek tárolása változókban {#storing-values-with-variables}

Ezután létrehozunk egy _változót_, amely tárolja a felhasználói bemenetet, így:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Most kezd érdekessé válni a program! Sok minden történik ebben a rövid sorban. A
változó létrehozásához a `let` utasítást használjuk. Íme egy másik példa:

```rust,ignore
let apples = 5;
```

Ez a sor létrehoz egy új, `apples` nevű változót, és hozzáköti az `5` értéket. A
Rustban a változók alapértelmezés szerint nem módosíthatók, vagyis ha egyszer
értéket adtunk a változónak, az érték nem fog megváltozni. Ezt a fogalmat
részletesen a 3. fejezet
[„Változók és módosíthatóság”][variables-and-mutability]<!-- ignore --> című
szakaszában tárgyaljuk. Ahhoz, hogy egy változó módosítható legyen, a
változónév elé írjuk a `mut` kulcsszót:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Megjegyzés: A `//` szintaxis egy kommentet indít, amely a sor végéig tart. A
> Rust mindent figyelmen kívül hagy a kommentekben. A kommenteket
> részletesebben a [3. fejezetben][comments]<!-- ignore --> tárgyaljuk.

Visszatérve a kitalálós játék programjához, most már tudod, hogy a
`let mut guess` egy `guess` nevű módosítható változót vezet be. Az egyenlőségjel
(`=`) azt mondja a Rustnak, hogy most valamit hozzá akarunk kötni a változóhoz.
Az egyenlőségjeltől jobbra az az érték áll, amelyhez a `guess` hozzákötődik, ez
pedig a `String::new` hívásának eredménye – annak a függvénynek az eredménye,
amely egy új `String` példányt ad vissza. A [`String`][string]<!-- ignore --> a
standard könyvtár által biztosított sztringtípus, amely egy növelhető, UTF-8
kódolású szövegdarab.

A `::new` sorban a `::` szintaxis azt jelzi, hogy a `new` a `String` típus
asszociált függvénye. Az _asszociált függvény_ olyan függvény, amely egy típusra
van implementálva, ebben az esetben a `String`-re. Ez a `new` függvény egy új,
üres sztringet hoz létre. Sok típusnál találsz majd `new` függvényt, mert ez
gyakori név az olyan függvényekre, amelyek valamilyen új értéket készítenek.

Összességében a `let mut guess = String::new();` sor létrehozott egy módosítható
változót, amely jelenleg egy új, üres `String` példányhoz van kötve. Hűha!

### Felhasználói bemenet fogadása

Emlékezz vissza, hogy a program első sorában a `use std::io;` utasítással
behoztuk a standard könyvtár bemeneti/kimeneti funkcionalitását. Most meghívjuk
az `io` modul `stdin` függvényét, amely lehetővé teszi, hogy kezeljük a
felhasználói bemenetet:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Ha nem importáltuk volna az `io` modult a `use std::io;` utasítással a program
elején, akkor is használhatnánk a függvényt, ha a függvényhívást
`std::io::stdin` alakban írnánk. Az `stdin` függvény egy
[`std::io::Stdin`][iostdin]<!-- ignore --> példányt ad vissza, ami egy olyan
típus, amely a terminálod standard bemenetére mutató handle-t képviseli.

Ezután a `.read_line(&mut guess)` sor meghívja a standard bemenet handle-jén a
[`read_line`][read_line]<!-- ignore --> metódust, hogy bemenetet kapjon a
felhasználótól. A `&mut guess`-t is átadjuk argumentumként a `read_line`-nak,
hogy megmondjuk neki, melyik sztringben tárolja a felhasználói bemenetet. A
`read_line` teljes feladata az, hogy fogja, amit a felhasználó a standard
bemenetre gépel, és hozzáfűzze egy sztringhez (anélkül, hogy felülírná annak
tartalmát), ezért adjuk át azt a sztringet argumentumként. A sztringargumentumnak
módosíthatónak kell lennie, hogy a metódus meg tudja változtatni a sztring
tartalmát.

Az `&` azt jelzi, hogy ez az argumentum egy _referencia_, ami módot ad arra,
hogy a kódod több része is hozzáférjen egyetlen adatdarabhoz anélkül, hogy azt
az adatot többször be kellene másolni a memóriába. A referenciák összetett
képességet jelentenek, és a Rust egyik nagy előnye éppen az, hogy milyen
biztonságos és egyszerű a referenciák használata. Nem kell sokat tudnod ezekről
a részletekről ahhoz, hogy befejezd ezt a programot. Egyelőre annyit kell
tudnod, hogy a referenciák – akárcsak a változók – alapértelmezés szerint nem
módosíthatók. Ezért kell `&mut guess`-t írnod `&guess` helyett, hogy
módosítható legyen. (A 4. fejezet alaposabban elmagyarázza a referenciákat.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Lehetséges hibák kezelése a `Result` típussal {#handling-potential-failure-with-result}

Még mindig ezen a kódsoron dolgozunk. Most a szöveg harmadik sorát tárgyaljuk,
de vedd észre, hogy ez még mindig egyetlen logikai kódsor része. A következő
rész ez a metódus:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Ezt a kódot írhattuk volna így is:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Egy hosszú sort azonban nehéz olvasni, ezért érdemes feldarabolni. Gyakran
bölcs dolog sortörést és egyéb whitespace-t beiktatni, hogy tagoljuk a hosszú
sorokat, amikor egy metódust a `.method_name()` szintaxissal hívunk meg. Most
pedig nézzük meg, mit csinál ez a sor.

Ahogy korábban említettük, a `read_line` beteszi azt, amit a felhasználó beír,
abba a sztringbe, amelyet átadunk neki, de emellett visszaad egy `Result`
értéket is. A [`Result`][result]<!-- ignore --> egy
[_felsorolás_][enums]<!-- ignore -->, amelyet gyakran _enum_-nak neveznek, és ez
egy olyan típus, amely több lehetséges állapot egyikében lehet. Minden egyes
lehetséges állapotot _variánsnak_ hívunk.

A [6. fejezet][enums]<!-- ignore --> részletesebben tárgyalja az enumokat. Ezen
`Result` típusok célja a hibakezelési információk kódolása.

A `Result` variánsai az `Ok` és az `Err`. Az `Ok` variáns azt jelzi, hogy a
művelet sikeres volt, és tartalmazza a sikeresen előállított értéket. Az `Err`
variáns azt jelenti, hogy a művelet meghiúsult, és információt tartalmaz arról,
hogyan vagy miért hiúsult meg a művelet.

A `Result` típusú értékeknek – mint bármely típus értékeinek – vannak rájuk
definiált metódusai. Egy `Result` példányon meghívható az
[`expect` metódus][expect]<!-- ignore -->. Ha ez a `Result` példány egy `Err`
érték, az `expect` összeomlasztja a programot, és megjeleníti azt az üzenetet,
amelyet argumentumként adtál át az `expect`-nek. Ha a `read_line` metódus `Err`
értéket ad vissza, az valószínűleg az alatta lévő operációs rendszerből érkező
hiba eredménye. Ha ez a `Result` példány egy `Ok` érték, az `expect` fogja az
`Ok` által tárolt visszatérési értéket, és pontosan azt az értéket adja vissza
neked, hogy használhasd. Ebben az esetben ez az érték a felhasználó bemenetének
bájtokban mért hossza.

Ha nem hívod meg az `expect`-et, a program lefordul, de figyelmeztetést kapsz:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

A Rust arra figyelmeztet, hogy nem használtad fel a `read_line` által
visszaadott `Result` értéket, ami azt jelzi, hogy a program nem kezelt egy
lehetséges hibát.

A figyelmeztetés elnyomásának helyes módja az, ha ténylegesen írsz hibakezelő
kódot, de a mi esetünkben egyszerűen azt akarjuk, hogy a program összeomoljon,
amikor probléma történik, ezért használhatjuk az `expect`-et. A hibákból való
helyreállásról a [9. fejezetben][recover]<!-- ignore --> tanulsz majd.

### Értékek kiírása `println!` helyőrzőkkel

A záró kapcsos zárójelen kívül már csak egyetlen sort kell megtárgyalnunk az
eddigi kódban:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Ez a sor kiírja azt a sztringet, amely most a felhasználó bemenetét tartalmazza.
A `{}` kapcsoszárójel-pár egy helyőrző: gondolj a `{}` jelre úgy, mint kis
rákollókra, amelyek a helyükön tartanak egy értéket. Egy változó értékének
kiírásakor a változónév a kapcsos zárójelek közé kerülhet. Egy kifejezés
kiértékelésének eredményét úgy írjuk ki, hogy üres kapcsos zárójeleket teszünk a
formátumsztringbe, majd a formátumsztring után vesszővel elválasztva
felsoroljuk azokat a kifejezéseket, amelyeket az egyes üres
kapcsoszárójel-helyőrzőkbe kell kiírni, ugyanabban a sorrendben. Egy változó és
egy kifejezés eredményének kiírása egyetlen `println!` hívásban így nézne ki:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Ez a kód a következőt írná ki: `x = 5 and y + 2 = 12`.

### Az első rész tesztelése

Teszteljük a kitalálós játék első részét. Futtasd a `cargo run` paranccsal:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Ezen a ponton a játék első része kész: bemenetet kapunk a billentyűzetről, majd
kiírjuk azt.

## A titkos szám generálása

Ezután generálnunk kell egy titkos számot, amelyet a felhasználó megpróbál majd
kitalálni. A titkos számnak minden alkalommal másnak kell lennie, hogy a
játékkal többször is szórakoztató legyen játszani. Egy 1 és 100 közötti
véletlen számot fogunk használni, hogy a játék ne legyen túl nehéz. A Rust
standard könyvtára egyelőre nem tartalmaz véletlenszám-generáló
funkcionalitást. A Rust csapata azonban biztosít egy [`rand`
crate-et][randcrate] ezzel a funkcionalitással.

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### A funkcionalitás bővítése egy crate-tel

Ne feledd, hogy a crate Rust forráskódfájlok gyűjteménye. Az a projekt, amelyet
eddig építettünk, egy binary crate, ami egy futtatható program. A `rand` crate
egy library crate, amely olyan kódot tartalmaz, amelyet más programokban való
felhasználásra szántak, és önmagában nem futtatható.

A Cargo igazán a külső crate-ek összehangolásában ragyog. Mielőtt olyan kódot
írhatnánk, amely a `rand`-ot használja, módosítanunk kell a _Cargo.toml_ fájlt,
hogy a `rand` crate függőségként szerepeljen benne. Nyisd meg most ezt a fájlt,
és add hozzá a következő sort az aljához, a Cargo által létrehozott
`[dependencies]` szakaszfejléc alá. Ügyelj rá, hogy a `rand`-ot pontosan úgy add
meg, ahogy itt szerepel, ezzel a verziószámmal, különben előfordulhat, hogy az
oktatóanyag kódpéldái nem működnek:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

A _Cargo.toml_ fájlban minden, ami egy fejléc után következik, annak a
szakasznak a része, és addig tart, amíg egy másik szakasz el nem kezdődik. A
`[dependencies]` szakaszban mondod meg a Cargónak, hogy a projekted mely külső
crate-ektől függ, és azoknak a crate-eknek mely verzióira van szükséged. Ebben
az esetben a `rand` crate-et a `0.10.1` szemantikus verziómegjelöléssel adjuk
meg. A Cargo érti a [szemantikus verziózást][semver]<!-- ignore --> (amelyet
néha _SemVer_-nek hívnak), ami a verziószámok írásának szabványa. A `0.10.1`
megjelölés valójában a `^0.10.1` rövidítése, ami bármely olyan verziót jelent,
amely legalább 0.10.1, de 0.11.0 alatt van.

A Cargo úgy tekinti, hogy ezeknek a verzióknak a publikus API-ja kompatibilis a
0.10.1-es verzióéval, és ez a megadás biztosítja, hogy a legfrissebb olyan
javítóverziót kapod, amely még lefordul az ebben a fejezetben szereplő kóddal. A
0.11.0-s vagy annál nagyobb verziókról nem garantált, hogy ugyanaz az API-juk,
mint amit a következő példák használnak.

Most pedig – anélkül, hogy bármit is változtatnánk a kódon – buildeljük a
projektet, ahogy a 2-2. listában látható.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="A `cargo build` futtatásának kimenete, miután függőségként hozzáadtuk a `rand` crate-et">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

Előfordulhat, hogy más verziószámokat látsz (de mind kompatibilis lesz a
kóddal, hála a SemVernek!), és más sorokat is (az operációs rendszertől
függően), a sorok pedig más sorrendben is állhatnak.

Amikor külső függőséget veszünk fel, a Cargo letölti mindannak a legfrissebb
verzióját, amire annak a függőségnek szüksége van, a _registryből_, ami a
[Crates.io][cratesio] adatainak másolata. A Crates.io az a hely, ahová a Rust
ökoszisztéma tagjai feltöltik a nyílt forráskódú Rust-projektjeiket, hogy mások
is használhassák őket.

A registry frissítése után a Cargo megnézi a `[dependencies]` szakaszt, és
letölti az ott felsorolt crate-ek közül azokat, amelyek még nincsenek letöltve.
Ebben az esetben, bár mi csak a `rand`-ot soroltuk fel függőségként, a Cargo
megszerzett más crate-eket is, amelyektől a `rand` működése függ. A crate-ek
letöltése után a Rust lefordítja őket, majd lefordítja a projektet is a
rendelkezésre álló függőségekkel.

Ha azonnal újra lefuttatod a `cargo build`-et anélkül, hogy bármit
változtatnál, a `Finished` soron kívül nem kapsz kimenetet. A Cargo tudja, hogy
már letöltötte és lefordította a függőségeket, és te semmit sem változtattál
rajtuk a _Cargo.toml_ fájlodban. A Cargo azt is tudja, hogy a kódodon sem
változtattál semmit, ezért azt sem fordítja újra. Mivel nincs mit tennie,
egyszerűen kilép.

Ha megnyitod a _src/main.rs_ fájlt, végzel benne egy apró változtatást, majd
elmented és újra buildelsz, csak két sor kimenetet fogsz látni:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Ezek a sorok azt mutatják, hogy a Cargo csak a _src/main.rs_ fájlon végzett
apró változtatásoddal frissíti a buildet. A függőségeid nem változtak, így a
Cargo tudja, hogy azokhoz újra felhasználhatja azt, amit már letöltött és
lefordított.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Reprodukálható buildek biztosítása

A Cargóban van egy mechanizmus, amely biztosítja, hogy minden alkalommal
ugyanazt az artifactot tudd újraépíteni, akár te, akár bárki más buildeli a
kódodat: a Cargo csak az általad megadott függőségverziókat fogja használni,
amíg másképp nem rendelkezel. Tegyük fel például, hogy jövő héten megjelenik a
`rand` crate 0.10.2-es verziója, és az a verzió tartalmaz egy fontos
hibajavítást, de tartalmaz egy regressziót is, amely eltöri a kódodat. Ennek
kezelésére a Rust az első `cargo build` futtatásakor létrehozza a _Cargo.lock_
fájlt, így most már ez is megvan a _guessing_game_ könyvtárban.

Amikor először buildelsz egy projektet, a Cargo kitalálja a függőségek összes
olyan verzióját, amely megfelel a feltételeknek, majd beírja őket a
_Cargo.lock_ fájlba. Amikor a jövőben buildeled a projektedet, a Cargo látni
fogja, hogy a _Cargo.lock_ fájl létezik, és az ott megadott verziókat fogja
használni ahelyett, hogy újra elvégezné a verziók kitalálásának munkáját. Ez
lehetővé teszi, hogy automatikusan reprodukálható buildjeid legyenek. Más
szóval a projekted a 0.10.1-es verziónál marad, amíg kifejezetten nem
frissítesz, hála a _Cargo.lock_ fájlnak. Mivel a _Cargo.lock_ fájl fontos a
reprodukálható buildekhez, gyakran a projekted többi kódjával együtt
verziókövetés alá helyezik.

#### Crate frissítése új verzióra

Amikor _tényleg_ frissíteni akarsz egy crate-et, a Cargo biztosítja az `update`
parancsot, amely figyelmen kívül hagyja a _Cargo.lock_ fájlt, és kitalálja az
összes olyan legfrissebb verziót, amely megfelel a _Cargo.toml_ fájlban
megadott specifikációidnak. A Cargo ezután beírja ezeket a verziókat a
_Cargo.lock_ fájlba. Egyébként alapértelmezés szerint a Cargo csak a 0.10.1-nél
nagyobb és 0.11.0-nál kisebb verziókat keresi. Ha a `rand` crate kiadta a két
új, 0.10.2-es és 0.999.0-s verziót, a következőt látnád, ha lefuttatnád a
`cargo update` parancsot:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

A Cargo figyelmen kívül hagyja a 0.999.0-s kiadást. Ezen a ponton azt is
észrevennéd, hogy a _Cargo.lock_ fájlod megváltozott, és most azt jelzi, hogy a
használt `rand` crate verziója 0.10.2. Ahhoz, hogy a `rand` 0.999.0-s verzióját
vagy a 0.999._x_ sorozat bármely verzióját használd, a _Cargo.toml_ fájlt
ehelyett így kellene frissítened (valójában ne végezd el ezt a változtatást,
mert a következő példák azt feltételezik, hogy a `rand` 0.10-et használod):

```toml
[dependencies]
rand = "0.999.0"
```

Amikor legközelebb lefuttatod a `cargo build`-et, a Cargo frissíti az elérhető
crate-ek registryjét, és az általad megadott új verzió szerint újraértékeli a
`rand` követelményeit.

Sokkal több mondanivaló van még a [Cargóról][doccargo]<!-- ignore --> és [az
ökoszisztémájáról][doccratesio]<!-- ignore -->, amit a 14. fejezetben
tárgyalunk, de egyelőre ennyit kell tudnod. A Cargo nagyon megkönnyíti a
könyvtárak újrafelhasználását, így a rustaceanek kisebb projekteket tudnak
írni, amelyeket számos csomagból állítanak össze.

### Véletlen szám generálása {#generating-a-random-number}

Kezdjük el használni a `rand`-ot, hogy generáljunk egy kitalálandó számot. A
következő lépés a _src/main.rs_ frissítése, ahogy a 2-3. listában látható.

<Listing number="2-3" file-name="src/main.rs" caption="Kód hozzáadása véletlen szám generálásához">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Először hozzáadjuk a `use rand::prelude::*;` sort. A `prelude` modul a `rand`
crate leggyakrabban használt részeit tartalmazza, a `use` pedig elérhetővé teszi
ezeket az elemeket a programunk hatókörében.

Ezután két sort adunk hozzá középen. Az első sorban meghívjuk a `rand::rng`
függvényt, amely megadja nekünk azt a bizonyos véletlenszám-generátort, amelyet
használni fogunk: egy olyat, amely az aktuális végrehajtási szálhoz lokális, és
amelynek a magját az operációs rendszer adja. Ezután meghívjuk a
véletlenszám-generátoron a `random_range` metódust. Ezt a metódust az `RngExt`
trait definiálja, amely a `rand::prelude` modul része, és amelyet a `use
rand::prelude::*;` utasítással hoztunk a hatókörbe. A `random_range` metódus
argumentumként egy tartománykifejezést vár, és a tartományon belül generál egy
véletlen számot. Az itt használt tartománykifejezés `start..=end` alakú, és
alulról is, felülről is zárt, ezért az `1..=100` alakot kell megadnunk, hogy 1
és 100 közötti számot kérjünk.

> Megjegyzés: Nem fogod csak úgy tudni, hogy mit kell egy crate-ből a hatókörbe
> hozni, és mely metódusait, illetve függvényeit kell meghívni, ezért minden
> crate-hez tartozik dokumentáció, amely leírja a használatát. A Cargo egy
> másik ügyes képessége, hogy a `cargo doc --open` parancs futtatása lokálisan
> felépíti az összes függőséged által biztosított dokumentációt, és megnyitja
> azt a böngésződben. Ha például a `rand` crate egyéb funkcionalitása is
> érdekel, futtasd a `cargo doc --open` parancsot, és kattints a bal oldali
> oldalsávban a `rand`-ra.

A második új sor kiírja a titkos számot. Ez a program fejlesztése közben
hasznos, mert így tesztelni tudjuk, de a végleges változatból törölni fogjuk.
Nem sok játék az, ha a program azonnal kiírja a választ, amint elindul!

Próbáld meg néhányszor lefuttatni a programot:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Különböző véletlen számokat kell kapnod, és mindegyiknek 1 és 100 közötti
számnak kell lennie. Ha figyelmeztetéseket kapsz, azokat nyugodtan figyelmen
kívül hagyhatod. Ha hibákat kapsz, ellenőrizd, hogy a *Cargo.toml* fájlodban
`rand = "0.10.1"` szerepel-e, mivel a `rand` későbbi verzióinak más lehet az
API-ja, de a `0.10` sorozat bármely verziójának működnie kell az ebben a
fejezetben szereplő kóddal.

## A tipp összehasonlítása a titkos számmal {#comparing-the-guess-to-the-secret-number}

Most, hogy van felhasználói bemenetünk és egy véletlen számunk,
összehasonlíthatjuk őket. Ezt a lépést a 2-4. lista mutatja. Vedd észre, hogy
ez a kód még nem fordul le, ahogy azt mindjárt elmagyarázzuk.

<Listing number="2-4" file-name="src/main.rs" caption="Két szám összehasonlításának lehetséges visszatérési értékeit kezelő kód">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Először hozzáadunk egy újabb `use` utasítást, amely a standard könyvtárból a
`std::cmp::Ordering` nevű típust hozza a hatókörbe. Az `Ordering` típus egy
másik enum, és `Less`, `Greater`, illetve `Equal` variánsai vannak. Ez az a
három kimenetel, amely két érték összehasonlításakor lehetséges.

Ezután öt új sort adunk hozzá alul, amelyek az `Ordering` típust használják. A
`cmp` metódus két értéket hasonlít össze, és bármin meghívható, ami
összehasonlítható. Referenciát vár arra, amivel össze akarod hasonlítani: itt a
`guess`-t hasonlítja a `secret_number`-höz. Ezután visszaadja az `Ordering`
enum egy variánsát, amelyet a `use` utasítással hoztunk a hatókörbe. Egy
[`match`][match]<!-- ignore --> kifejezést használunk annak eldöntésére, hogy
mit tegyünk ezután, attól függően, hogy az `Ordering` melyik variánsát adta
vissza a `cmp` hívása a `guess` és a `secret_number` értékekkel.

A `match` kifejezés _ágakból_ áll. Egy ág egy _mintából_ áll, amelyre
illeszteni kell, és abból a kódból, amelynek le kell futnia, ha a `match`-nek
átadott érték illeszkedik az adott ág mintájára. A Rust fogja a `match`-nek
átadott értéket, és sorban végignézi az egyes ágak mintáit. A minták és a
`match` szerkezet a Rust erőteljes nyelvi elemei: lehetővé teszik, hogy sokféle
helyzetet fejezz ki, amellyel a kódod találkozhat, és gondoskodnak arról, hogy
mindegyiket kezeld is. Ezeket a nyelvi elemeket részletesen a 6., illetve a 19.
fejezetben tárgyaljuk.

Nézzünk végig egy példát az itt használt `match` kifejezéssel. Tegyük fel, hogy
a felhasználó 50-re tippelt, a véletlenszerűen generált titkos szám pedig
ezúttal 38.

Amikor a kód összehasonlítja az 50-et a 38-cal, a `cmp` metódus
`Ordering::Greater`-t ad vissza, mert 50 nagyobb, mint 38. A `match` kifejezés
megkapja az `Ordering::Greater` értéket, és elkezdi ellenőrizni az egyes ágak
mintáit. Megnézi az első ág mintáját, az `Ordering::Less`-t, és látja, hogy az
`Ordering::Greater` érték nem illeszkedik az `Ordering::Less`-re, ezért
figyelmen kívül hagyja az abban az ágban lévő kódot, és továbblép a következő
ágra. A következő ág mintája az `Ordering::Greater`, ami _illeszkedik_ az
`Ordering::Greater`-re! Az ahhoz az ághoz tartozó kód lefut, és kiírja a
képernyőre, hogy `Too big!`. A `match` kifejezés az első sikeres illeszkedés
után véget ér, így ebben az esetben már nem nézi meg az utolsó ágat.

A 2-4. listában szereplő kód azonban még nem fordul le. Próbáljuk ki:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

A hiba lényege az, hogy _mismatched types_, azaz eltérnek a típusok. A Rustnak
erős, statikus típusrendszere van. Ugyanakkor típuskikövetkeztetése is van.
Amikor azt írtuk, hogy `let mut guess = String::new()`, a Rust ki tudta
következtetni, hogy a `guess` egy `String` kell legyen, és nem kellett kiírnunk
a típust. A `secret_number` viszont egy számtípus. A Rust számtípusai közül
többnek is lehet 1 és 100 közötti értéke: az `i32`, ami egy 32 bites szám; az
`u32`, ami egy előjel nélküli 32 bites szám; az `i64`, ami egy 64 bites szám;
és mások is. Hacsak másképp nem adjuk meg, a Rust alapértelmezésben `i32`-t
használ, és ez a `secret_number` típusa is, hacsak nem adsz hozzá máshol olyan
típusinformációt, amely miatt a Rust más numerikus típust következtetne ki. A
hiba oka az, hogy a Rust nem tud összehasonlítani egy sztringet és egy
számtípust.

Végső soron azt szeretnénk, hogy a program a bemenetként beolvasott `String`-et
számtípussá alakítsa, hogy numerikusan össze tudjuk hasonlítani a titkos
számmal. Ezt úgy tesszük meg, hogy hozzáadjuk ezt a sort a `main` függvény
törzséhez:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

A sor a következő:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Létrehozunk egy `guess` nevű változót. De várjunk csak, nincs már a programnak
egy `guess` nevű változója? De van, csakhogy a Rust szerencsére megengedi, hogy
a `guess` korábbi értékét egy újjal árnyékoljuk. A _shadowing_ lehetővé teszi,
hogy újrahasználjuk a `guess` változónevet, ahelyett hogy két külön változót
kellene létrehoznunk, például `guess_str`-t és `guess`-t. Ezt részletesebben a
[3. fejezetben][shadowing]<!-- ignore --> tárgyaljuk, de egyelőre elég annyit
tudni, hogy ezt a képességet gyakran használják, amikor egy értéket az egyik
típusból egy másikba akarsz konvertálni.

Ezt az új változót a `guess.trim().parse()` kifejezéshez kötjük. A kifejezésben
szereplő `guess` az eredeti `guess` változóra utal, amely a bemenetet
sztringként tartalmazta. A `String` példány `trim` metódusa eltávolít minden
whitespace-t az elejéről és a végéről, amit meg kell tennünk, mielőtt a
sztringet `u32`-vé alakíthatnánk, mert az csak numerikus adatot tartalmazhat. A
felhasználónak meg kell nyomnia az <kbd>enter</kbd> billentyűt ahhoz, hogy a
`read_line` teljesüljön és beírja a tippjét, ez pedig egy újsor karaktert ad a
sztringhez. Ha például a felhasználó beírja az <kbd>5</kbd>-öt és megnyomja az
<kbd>enter</kbd>-t, a `guess` így néz ki: `5\n`. A `\n` az „újsort” jelöli.
(Windowson az <kbd>enter</kbd> megnyomása kocsivissza és újsor karaktert
eredményez: `\r\n`.) A `trim` metódus eltávolítja a `\n`-t vagy a `\r\n`-t, így
csak az `5` marad.

A [sztringek `parse` metódusa][parse]<!-- ignore --> egy sztringet egy másik
típussá alakít. Itt arra használjuk, hogy sztringből számot csináljunk. Meg
kell mondanunk a Rustnak, pontosan milyen számtípust akarunk, ezt a
`let guess: u32` alakkal tesszük. A `guess` utáni kettőspont (`:`) azt mondja a
Rustnak, hogy meg fogjuk adni a változó típusát. A Rustnak van néhány beépített
számtípusa; az itt látható `u32` egy előjel nélküli, 32 bites egész szám. Jó
alapértelmezett választás egy kis pozitív számhoz. Más számtípusokról a
[3. fejezetben][integers]<!-- ignore --> tanulsz majd.

Ráadásul az `u32` típusjelölés ebben a példaprogramban és a `secret_number`-rel
való összehasonlítás azt jelenti, hogy a Rust ki fogja következtetni: a
`secret_number` is `u32` kell legyen. Így most már két azonos típusú érték
között történik az összehasonlítás!

A `parse` metódus csak olyan karakterekkel működik, amelyek logikusan számmá
alakíthatók, ezért könnyen okozhat hibát. Ha például a sztring az `A👍%`-ot
tartalmazná, azt sehogy sem lehetne számmá alakítani. Mivel meghiúsulhat, a
`parse` metódus `Result` típust ad vissza, ahogy a `read_line` metódus is
(erről korábban a [„Lehetséges hibák kezelése a `Result`
típussal”](#handling-potential-failure-with-result)<!-- ignore --> szakaszban
volt szó). Ezt a `Result`-ot ugyanúgy kezeljük: ismét az `expect` metódust
használjuk. Ha a `parse` az `Err` `Result`-variánst adja vissza, mert nem
tudott számot előállítani a sztringből, az `expect` hívás összeomlasztja a
játékot, és kiírja az általunk megadott üzenetet. Ha a `parse` sikeresen át
tudja alakítani a sztringet számmá, akkor a `Result` `Ok` variánsát adja
vissza, és az `expect` visszaadja azt a számot, amelyet szeretnénk, az `Ok`
értékből.

Futtassuk most a programot:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Szuper! Bár a tipp elé szóközöket írtunk, a program mégis rájött, hogy a
felhasználó 76-ra tippelt. Futtasd le a programot néhányszor, hogy ellenőrizd a
különböző bemenetekkel járó eltérő viselkedést: találd el pontosan a számot,
tippelj túl nagy számra, és tippelj túl kicsire is.

A játék nagy része már működik, de a felhasználó csak egyetlen tippet adhat.
Változtassunk ezen egy ciklus hozzáadásával!

## Több tipp engedélyezése ciklussal

A `loop` kulcsszó végtelen ciklust hoz létre. Hozzáadunk egy ciklust, hogy a
felhasználóknak több esélyük legyen kitalálni a számot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Ahogy látod, mindent a tippet bekérő felszólítástól kezdve beletettünk egy
ciklusba. Ügyelj arra, hogy a cikluson belüli sorokat még négy szóközzel
beljebb húzd, majd futtasd le újra a programot. A program most már örökké újabb
tippet fog kérni, ami valójában új problémát vet fel. Úgy tűnik, a felhasználó
nem tud kilépni!

A felhasználó bármikor megszakíthatná a programot a
<kbd>ctrl</kbd>-<kbd>C</kbd> billentyűkombinációval. De van másik módja is
annak, hogy megmeneküljünk ettől a telhetetlen szörnyetegtől, ahogy azt a
`parse` tárgyalásánál említettük [„A tipp összehasonlítása a titkos
számmal”](#comparing-the-guess-to-the-secret-number)<!-- ignore --> című
részben: ha a felhasználó nem szám választ ad meg, a program összeomlik. Ezt
kihasználhatjuk, hogy a felhasználó ki tudjon lépni, ahogy itt látható:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

A `quit` beírása kilép a játékból, de ahogy észre fogod venni, ugyanezt teszi
bármilyen más, nem szám bemenet is. Ez enyhén szólva nem optimális; azt
szeretnénk, hogy a játék akkor is álljon meg, ha eltalálták a helyes számot.

### Kilépés a helyes tipp után {#quitting-after-a-correct-guess}

Programozzuk úgy a játékot, hogy kilépjen, amikor a felhasználó nyer: adjunk
hozzá egy `break` utasítást:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

A `break` sor hozzáadása a `You win!` után azt eredményezi, hogy a program
kilép a ciklusból, amikor a felhasználó helyesen tippeli meg a titkos számot. A
ciklusból való kilépés a programból való kilépést is jelenti, mert a ciklus a
`main` utolsó része.

### Érvénytelen bemenet kezelése

Hogy tovább finomítsuk a játék viselkedését, ahelyett hogy összeomlana a
program, amikor a felhasználó nem számot ír be, tegyük úgy, hogy a játék
figyelmen kívül hagyja a nem szám bemenetet, így a felhasználó folytathatja a
tippelést. Ezt úgy érhetjük el, hogy módosítjuk azt a sort, ahol a `guess`
`String`-ből `u32`-vé alakul, ahogy a 2-5. listában látható.

<Listing number="2-5" file-name="src/main.rs" caption="Nem szám tipp figyelmen kívül hagyása és újabb tipp kérése a program összeomlasztása helyett">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Az `expect` hívásról egy `match` kifejezésre váltunk, hogy a hibán való
összeomlás helyett kezeljük a hibát. Ne feledd, hogy a `parse` `Result` típust
ad vissza, a `Result` pedig egy enum, amelynek `Ok` és `Err` variánsai vannak.
Itt `match` kifejezést használunk, ahogy azt a `cmp` metódus `Ordering`
eredményénél is tettük.

Ha a `parse` sikeresen számmá tudja alakítani a sztringet, egy `Ok` értéket ad
vissza, amely az eredményül kapott számot tartalmazza. Ez az `Ok` érték
illeszkedni fog az első ág mintájára, és a `match` kifejezés egyszerűen
visszaadja azt a `num` értéket, amelyet a `parse` előállított és az `Ok` értékbe
tett. Ez a szám pontosan ott köt ki, ahol szeretnénk: az új `guess` változóban,
amelyet létrehozunk.

Ha a `parse` _nem_ tudja számmá alakítani a sztringet, egy `Err` értéket ad
vissza, amely több információt tartalmaz a hibáról. Az `Err` érték nem
illeszkedik az első `match`-ág `Ok(num)` mintájára, de illeszkedik a második ág
`Err(_)` mintájára. Az aláhúzásjel, `_`, egy mindent elkapó érték; ebben a
példában azt mondjuk, hogy minden `Err` értékre illeszkedni akarunk,
függetlenül attól, milyen információt tartalmaznak. Így a program a második ág
kódját fogja végrehajtani, a `continue`-t, ami azt mondja a programnak, hogy
lépjen a `loop` következő iterációjára, és kérjen újabb tippet. Vagyis
gyakorlatilag a program minden olyan hibát figyelmen kívül hagy, amellyel a
`parse` találkozhat!

Most már mindennek úgy kell működnie a programban, ahogy elvárjuk. Próbáljuk
ki:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Nagyszerű! Egyetlen apró utolsó igazítással befejezzük a kitalálós játékot.
Emlékezz vissza, hogy a program még mindig kiírja a titkos számot. Ez
teszteléshez jól jött, de tönkreteszi a játékot. Töröljük azt a `println!`-t,
amely kiírja a titkos számot. A 2-6. lista mutatja a végleges kódot.

<Listing number="2-6" file-name="src/main.rs" caption="A kitalálós játék teljes kódja">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Ezen a ponton sikeresen megépítetted a kitalálós játékot. Gratulálunk!

## Összefoglalás

Ez a projekt gyakorlati módja volt annak, hogy sok új Rust-fogalmat megismerj:
a `let`-et, a `match`-et, a függvényeket, a külső crate-ek használatát és még
sok mást. A következő néhány fejezetben ezekről a fogalmakról részletesebben is
tanulsz majd. A 3. fejezet olyan fogalmakat tárgyal, amelyek a legtöbb
programozási nyelvben megvannak, például a változókat, az adattípusokat és a
függvényeket, és megmutatja, hogyan használd őket a Rustban. A 4. fejezet az
ownershipet járja körül, azt a képességet, amely a Rustot különbözővé teszi a
többi nyelvtől. Az 5. fejezet a structokat és a metódusszintaxist tárgyalja, a
6. fejezet pedig azt magyarázza el, hogyan működnek az enumok.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
