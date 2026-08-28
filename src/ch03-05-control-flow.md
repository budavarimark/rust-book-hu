## Vezérlési szerkezetek {#control-flow}

Az a lehetőség, hogy egy kódrészletet csak akkor futtatunk, ha egy feltétel
`true`, illetve hogy egy kódrészletet ismételten futtatunk, amíg egy feltétel
`true`, a legtöbb programozási nyelv alapvető építőköve. A Rust-kód
végrehajtásának irányítására a leggyakrabban használt szerkezetek az `if`
kifejezések és a ciklusok.

### `if` kifejezések

Az `if` kifejezéssel feltételektől függően ágaztathatod el a kódodat. Megadsz
egy feltételt, majd kijelented: „Ha ez a feltétel teljesül, futtasd ezt a
kódblokkot. Ha a feltétel nem teljesül, ne futtasd ezt a kódblokkot.”

Hozz létre egy _branches_ nevű új projektet a _projects_ könyvtáradban, hogy
kipróbálhassuk az `if` kifejezést. A _src/main.rs_ fájlba írd be a következőket:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Minden `if` kifejezés az `if` kulcsszóval kezdődik, amelyet egy feltétel követ.
Ebben az esetben a feltétel azt vizsgálja, hogy a `number` változó értéke
kisebb-e 5-nél. A feltétel teljesülése esetén végrehajtandó kódblokkot
közvetlenül a feltétel után, kapcsos zárójelek közé helyezzük. Az `if`
kifejezések feltételeihez tartozó kódblokkokat néha _ágaknak_ (arm) nevezzük,
akárcsak a `match` kifejezések ágait, amelyekről a 2. fejezet
[„A tipp összehasonlítása a titkos
számmal”][comparing-the-guess-to-the-secret-number]<!-- ignore --> című
szakaszában volt szó.

Ha szeretnénk, egy `else` kifejezést is megadhatunk – itt éppen ezt tettük –,
hogy a program alternatív kódblokkot futtasson arra az esetre, ha a feltétel
`false` értékre értékelődik ki. Ha nem adsz meg `else` kifejezést, és a feltétel
`false`, a program egyszerűen kihagyja az `if` blokkot, és a következő
kódrészletre lép.

Próbáld meg futtatni ezt a kódot; a következő kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Próbáljuk meg a `number` értékét olyanra változtatni, amitől a feltétel `false`
lesz, és nézzük meg, mi történik:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Futtasd újra a programot, és nézd meg a kimenetet:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Érdemes azt is megjegyezni, hogy a feltételnek ebben a kódban _kötelezően_
`bool` típusúnak kell lennie. Ha a feltétel nem `bool`, hibát kapunk. Próbáld
meg például futtatni a következő kódot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Az `if` feltétele ezúttal a `3` értékre értékelődik ki, és a Rust hibát dob:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

A hiba azt jelzi, hogy a Rust `bool` típust várt, de egész számot kapott. A
Ruby-hoz vagy a JavaScripthez hasonló nyelvekkel ellentétben a Rust nem próbálja
meg automatikusan logikai értékké alakítani a nem logikai típusokat. Explicitnek
kell lenned, és az `if` feltételeként mindig logikai értéket kell megadnod. Ha
például azt szeretnénk, hogy az `if` kódblokk csak akkor fusson le, ha egy szám
nem egyenlő `0`-val, a következőképpen módosíthatjuk az `if` kifejezést:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Ennek a kódnak a futtatása a `number was something other than zero` szöveget
írja ki.

#### Több feltétel kezelése `else if` segítségével

Több feltételt is használhatsz, ha az `if` és az `else` szerkezetet egy `else
if` kifejezésben kombinálod. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Ennek a programnak négy lehetséges útvonala van. A futtatása után a következő
kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

A program végrehajtásakor sorban megvizsgálja az egyes `if` kifejezéseket, és az
első olyan törzset hajtja végre, amelynek a feltétele `true` értékre értékelődik
ki. Vedd észre, hogy bár a 6 osztható 2-vel, nem látjuk a `number is divisible
by 2` kimenetet, és az `else` blokk `number is not divisible by 4, 3, or 2`
szövegét sem. Ez azért van, mert a Rust csak az első `true` feltételhez tartozó
blokkot hajtja végre, és amint talál egyet, a többit már meg sem nézi.

A túl sok `else if` kifejezés használata áttekinthetetlenné teheti a kódot,
ezért ha egynél többet használsz, érdemes lehet átalakítanod a kódodat. A 6.
fejezet ezekre az esetekre egy nagy erejű Rust-elágaztató szerkezetet mutat be,
amelynek neve `match`.

#### Az `if` használata `let` utasításban

Mivel az `if` kifejezés, használhatjuk egy `let` utasítás jobb oldalán, hogy az
eredményt egy változóhoz rendeljük, ahogy a 3-2. listában látható.

<Listing number="3-2" file-name="src/main.rs" caption="Egy `if` kifejezés eredményének változóhoz rendelése">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

A `number` változóhoz az `if` kifejezés eredményétől függő érték kötődik.
Futtasd le a kódot, hogy lásd, mi történik:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Ne feledd, hogy a kódblokkok a bennük szereplő utolsó kifejezésre értékelődnek
ki, és a számok önmagukban szintén kifejezések. Ebben az esetben a teljes `if`
kifejezés értéke attól függ, melyik kódblokk fut le. Ez azt jelenti, hogy az
`if` egyes ágaiból eredményként adódó lehetséges értékeknek azonos típusúaknak
kell lenniük; a 3-2. listában mind az `if`, mind az `else` ág eredménye `i32`
egész szám volt. Ha a típusok nem egyeznek, mint a következő példában, hibát
kapunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Amikor megpróbáljuk lefordítani ezt a kódot, hibát kapunk. Az `if` és az `else`
ág értékeinek típusai nem összeegyeztethetők, és a Rust pontosan megmutatja, hol
keressük a problémát a programban:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Az `if` blokkban lévő kifejezés egész számra értékelődik ki, az `else` blokkban
lévő pedig sztringre. Ez nem működik, mert a változóknak egyetlen típusuk lehet,
és a Rustnak már fordítási időben egyértelműen tudnia kell, milyen típusú a
`number` változó. A `number` típusának ismerete lehetővé teszi a fordítónak,
hogy mindenütt ellenőrizze a típus érvényességét, ahol a `number` változót
használjuk. A Rust erre nem lenne képes, ha a `number` típusa csak futásidőben
dőlne el; a fordító bonyolultabb lenne, és kevesebb garanciát tudna nyújtani a
kódra nézve, ha bármely változóhoz több feltételezett típust kellene
nyilvántartania.

### Ismétlés ciklusokkal

Gyakran hasznos egy kódblokkot többször végrehajtani. Erre a feladatra a Rust
többféle _ciklust_ (loop) kínál, amelyek a ciklustörzsben lévő kódot
végigfuttatják a végéig, majd azonnal újrakezdik az elejéről. Hozzunk létre egy
_loops_ nevű új projektet, hogy kísérletezhessünk a ciklusokkal.

A Rustban háromféle ciklus van: `loop`, `while` és `for`. Próbáljuk ki mindet.

#### Kód ismétlése a `loop` szerkezettel

A `loop` kulcsszó azt mondja a Rustnak, hogy egy kódblokkot újra és újra
futtasson, vagy örökké, vagy amíg kifejezetten nem szólsz neki, hogy álljon le.

Példaként módosítsd a _loops_ könyvtáradban lévő _src/main.rs_ fájlt így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Amikor futtatjuk ezt a programot, azt látjuk, hogy az `again!` szöveg
folyamatosan újra és újra kiíródik, amíg kézzel le nem állítjuk a programot. A
legtöbb terminál támogatja a <kbd>ctrl</kbd>-<kbd>C</kbd> billentyűkombinációt,
amellyel megszakítható egy végtelen ciklusban ragadt program. Próbáld ki:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

A `^C` szimbólum azt jelöli, hol nyomtad meg a <kbd>ctrl</kbd>-<kbd>C</kbd>
kombinációt.

Lehet, hogy látod az `again!` szót a `^C` után, lehet, hogy nem, attól függően,
hogy a kód épp hol tartott a ciklusban, amikor megkapta a megszakítási jelzést.

Szerencsére a Rust kóddal is lehetőséget ad a ciklusból való kilépésre. A
`break` kulcsszót elhelyezheted a cikluson belül, hogy megmondd a programnak,
mikor hagyja abba a ciklus végrehajtását. Emlékezz vissza, hogy ezt tettük a
kitalálós játékban a 2. fejezet [„Kilépés helyes
tipp után”][quitting-after-a-correct-guess]<!-- ignore --> című szakaszában,
hogy kilépjünk a programból, amikor a felhasználó a helyes szám kitalálásával
megnyerte a játékot.

A kitalálós játékban a `continue` kulcsszót is használtuk, amely egy ciklusban
azt mondja a programnak, hogy hagyja ki a ciklus adott iterációjának hátralévő
kódját, és lépjen a következő iterációra.

#### Értékek visszaadása ciklusokból

A `loop` egyik felhasználási módja egy olyan művelet újrapróbálása, amelyről
tudod, hogy meghiúsulhat, például annak ellenőrzése, hogy egy szál befejezte-e a
munkáját. Előfordulhat az is, hogy a művelet eredményét ki kell juttatnod a
ciklusból a kód többi részéhez. Ehhez a `break` kifejezés után, amellyel a
ciklust leállítod, megadhatod a visszaadni kívánt értéket; ez az érték kikerül a
ciklusból, hogy használhasd, ahogy itt látható:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

A ciklus előtt deklarálunk egy `counter` nevű változót, és `0`-ra
inicializáljuk. Ezután deklarálunk egy `result` nevű változót, amely a ciklusból
visszaadott értéket tárolja majd. A ciklus minden iterációjában `1`-et adunk a
`counter` változóhoz, majd megnézzük, hogy a `counter` egyenlő-e `10`-zel.
Amikor igen, a `break` kulcsszót a `counter * 2` értékkel használjuk. A ciklus
után pontosvesszővel zárjuk le az utasítást, amely az értéket a `result`
változóhoz rendeli. Végül kiírjuk a `result` értékét, ami ebben az esetben `20`.

Egy cikluson belülről `return`-ölhetsz is. Míg a `break` csak az aktuális
ciklusból lép ki, a `return` mindig az aktuális függvényből lép ki.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Egyértelműsítés cikluscímkékkel

Ha ciklusokon belüli ciklusaid vannak, a `break` és a `continue` az adott ponton
a legbelső ciklusra vonatkozik. Egy cikluson megadhatsz egy _cikluscímkét_ (loop
label), amelyet aztán a `break` vagy a `continue` mellett használhatsz annak
jelzésére, hogy ezek a kulcsszavak a legbelső ciklus helyett a megcímkézett
ciklusra vonatkozzanak. A cikluscímkéknek egyetlen aposztróffal kell kezdődniük.
Íme egy példa két egymásba ágyazott ciklussal:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

A külső ciklus címkéje `'counting_up`, és 0-tól 2-ig számol felfelé. A címke
nélküli belső ciklus 10-től 9-ig számol visszafelé. Az első `break`, amely nem
ad meg címkét, csak a belső ciklusból lép ki. A `break 'counting_up;` utasítás a
külső ciklusból lép ki. Ez a kód a következőt írja ki:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Feltételes ciklusok egyszerűsítése a while szerkezettel

Egy programnak gyakran ki kell értékelnie egy feltételt egy cikluson belül. Amíg
a feltétel `true`, a ciklus fut. Amikor a feltétel már nem `true`, a program
meghívja a `break`-et, leállítva a ciklust. Az ilyen viselkedés megvalósítható a
`loop`, az `if`, az `else` és a `break` kombinációjával; ha kedved van, most ki
is próbálhatod egy programban. Ez a minta azonban annyira gyakori, hogy a
Rustban van rá beépített nyelvi szerkezet, amelynek neve `while` ciklus. A 3-3.
listában a `while` szerkezettel háromszor futtatjuk le a programot, minden
alkalommal visszafelé számolva, majd a ciklus után kiírunk egy üzenetet, és
kilépünk.

<Listing number="3-3" file-name="src/main.rs" caption="`while` ciklus használata kód futtatására, amíg egy feltétel `true` értékre értékelődik ki">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Ez a szerkezet rengeteg egymásba ágyazást szüntet meg, amely a `loop`, az `if`,
az `else` és a `break` használata esetén szükséges lenne, és áttekinthetőbb is.
Amíg a feltétel `true` értékre értékelődik ki, a kód fut; egyébként kilép a
ciklusból.

#### Végighaladás egy kollekción a `for` szerkezettel {#looping-through-a-collection-with-for}

Használhatod a `while` szerkezetet arra, hogy végighaladj egy kollekció, például
egy tömb elemein. A 3-4. listában szereplő ciklus például kiírja az `a` tömb
minden elemét.

<Listing number="3-4" file-name="src/main.rs" caption="Egy kollekció minden elemén való végighaladás `while` ciklussal">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Itt a kód felfelé haladva végigszámol a tömb elemein. A `0` indexnél kezd, és
addig ismétel, amíg el nem éri a tömb utolsó indexét (vagyis amíg az `index <
5` már nem `true`). Ennek a kódnak a futtatása a tömb minden elemét kiírja:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Mind az öt tömbérték megjelenik a terminálban, ahogy vártuk. Bár az `index` egy
ponton eléri az `5` értéket, a ciklus leáll, mielőtt megpróbálná kiolvasni a
hatodik értéket a tömbből.

Ez a megközelítés azonban hibalehetőségeket rejt; a program panicot válthat ki,
ha az indexérték vagy a vizsgálati feltétel hibás. Ha például az `a` tömb
definícióját négyeleműre módosítanád, de elfelejtenéd a feltételt `while index
< 4`-re frissíteni, a kód panicot váltana ki. Lassú is, mert a fordító
futásidejű kódot ad hozzá, amely a ciklus minden iterációjában elvégzi a
feltételes ellenőrzést, hogy az index a tömb határain belül van-e.

Tömörebb alternatívaként `for` ciklust használhatsz, és egy kollekció minden
eleméhez lefuttathatsz valamilyen kódot. Egy `for` ciklus a 3-5. listában
látható kódhoz hasonlóan néz ki.

<Listing number="3-5" file-name="src/main.rs" caption="Egy kollekció minden elemén való végighaladás `for` ciklussal">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Amikor futtatjuk ezt a kódot, ugyanazt a kimenetet látjuk, mint a 3-4. listánál.
Ami még fontosabb: most már növeltük a kód biztonságát, és kiküszöböltük azoknak
a hibáknak a lehetőségét, amelyek abból eredhetnek, hogy túlmegyünk a tömb
végén, vagy nem jutunk el elég messzire, és kihagyunk néhány elemet. A `for`
ciklusokból generált gépi kód hatékonyabb is lehet, mert az indexet nem kell
minden iterációban a tömb hosszához hasonlítani.

A `for` ciklus használatával nem kell arra emlékezned, hogy bármilyen más kódot
módosíts, ha megváltoztatod a tömbben lévő értékek számát – szemben a 3-4.
listában használt módszerrel.

A `for` ciklusok biztonságossága és tömörsége miatt ezek a Rustban a
leggyakrabban használt ciklusszerkezetek. Még olyan helyzetekben is, amikor egy
kódrészletet meghatározott számban szeretnél lefuttatni – mint a 3-3. listában
szereplő, `while` ciklust használó visszaszámláló példában –, a legtöbb
rusztacea `for` ciklust használna. Ezt úgy lehetne megoldani, hogy a standard
könyvtár által biztosított `Range` típust használjuk, amely sorban legenerálja
az összes számot egy adott számtól kezdve egy másik szám előttig.

Így nézne ki a visszaszámlálás egy `for` ciklussal és egy másik, eddig még nem
tárgyalt metódussal, a `rev` metódussal, amely megfordítja a tartományt:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Ez a kód valamivel szebb, nem igaz?

## Összefoglalás

Sikerült! Ez terjedelmes fejezet volt: tanultál a változókról, a skalár és
összetett adattípusokról, a függvényekről, a kommentekről, az `if`
kifejezésekről és a ciklusokról! Hogy gyakorold a fejezetben tárgyalt
fogalmakat, próbálj meg olyan programokat írni, amelyek a következőket teszik:

- Hőmérsékletet váltanak át Fahrenheit és Celsius között.
- Kiszámítják az *n*-edik Fibonacci-számot.
- Kiírják a „The Twelve Days of Christmas” című karácsonyi ének szövegét,
  kihasználva a dalban lévő ismétlődést.

Ha készen állsz a továbblépésre, egy olyan Rust-fogalomról fogunk beszélni,
amely _nem_ létezik általánosan más programozási nyelvekben: az ownershipről.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
