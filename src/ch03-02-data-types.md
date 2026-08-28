## Adattípusok {#data-types}

Rustban minden érték egy bizonyos _adattípusba_ tartozik, ami megmondja a
Rustnak, milyen fajta adatról van szó, hogy tudja, hogyan kell dolgoznia vele.
Az adattípusok két részhalmazát nézzük meg: a skalár és az összetett típusokat.

Ne feledd, hogy a Rust _statikusan típusos_ nyelv, ami azt jelenti, hogy
fordítási időben ismernie kell minden változó típusát. A fordító általában ki
tudja következtetni, melyik típust akarjuk használni, az érték és annak
felhasználási módja alapján. Azokban az esetekben, amikor sokféle típus
lehetséges – például amikor a 2. fejezet [„A tipp összehasonlítása a titkos
számmal”][comparing-the-guess-to-the-secret-number]<!-- ignore --> című
részében a `parse` segítségével egy `String`-et számtípussá alakítottunk –,
típusannotációt kell hozzáadnunk, így:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Ha nem adjuk hozzá a fenti kódban látható `: u32` típusannotációt, a Rust a
következő hibát írja ki, ami azt jelenti, hogy a fordítónak több információra
van szüksége tőlünk ahhoz, hogy tudja, melyik típust akarjuk használni:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Más adattípusoknál másféle típusannotációkat fogsz látni.

### Skalár típusok

A _skalár_ típusok egyetlen értéket képviselnek. A Rustnak négy elsődleges
skalár típusa van: egész számok, lebegőpontos számok, logikai értékek és
karakterek. Ezeket más programozási nyelvekből is ismerheted. Nézzük meg,
hogyan működnek Rustban.

#### Egész típusok {#integer-types}

Az _egész szám_ olyan szám, amelynek nincs tört része. A 2. fejezetben már
használtunk egy egész típust, az `u32`-t. Ez a típusdeklaráció azt jelzi, hogy
a hozzá tartozó érték előjel nélküli egész szám (az előjeles egész típusok `u`
helyett `i`-vel kezdődnek), amely 32 bitnyi helyet foglal el. A 3-1. táblázat a
Rust beépített egész típusait mutatja. Bármelyik változatot használhatjuk egy
egész érték típusának megadására.

<span class="caption">3-1. táblázat: Egész típusok Rustban</span>

| Hossz  | Előjeles  | Előjel nélküli |
| ------- | ------- | -------- |
| 8 bites   | `i8`    | `u8`     |
| 16 bites  | `i16`   | `u16`    |
| 32 bites  | `i32`   | `u32`    |
| 64 bites  | `i64`   | `u64`    |
| 128 bites | `i128`  | `u128`   |
| Architektúrafüggő | `isize` | `usize`  |

Minden változat lehet előjeles vagy előjel nélküli, és explicit mérete van. Az
_előjeles_ és az _előjel nélküli_ arra utal, hogy a szám lehet-e negatív –
másképp fogalmazva, hogy kell-e a számhoz előjel (előjeles), vagy mindig csak
pozitív lesz, és ezért előjel nélkül is ábrázolható (előjel nélküli). Olyan ez,
mint amikor papírra írunk számokat: ha az előjel számít, a számot plusz- vagy
mínuszjellel írjuk le; ha viszont nyugodtan feltételezhetjük, hogy a szám
pozitív, előjel nélkül írjuk. Az előjeles számokat [kettes komplemens][twos-complement]<!-- ignore
--> ábrázolással tároljuk.

Minden előjeles változat a −(2<sup>n − 1</sup>) és a 2<sup>n −
1</sup> − 1 közötti számokat tudja tárolni (a határokat is beleértve), ahol _n_
az adott változat által használt bitek száma. Egy `i8` tehát a
−(2<sup>7</sup>) és a 2<sup>7</sup> − 1 közötti számokat tárolhatja, ami
−128-tól 127-ig terjed. Az előjel nélküli változatok a 0 és a 2<sup>n</sup> − 1
közötti számokat tárolhatják, így egy `u8` a 0 és a 2<sup>8</sup> − 1 közötti,
azaz a 0 és 255 közötti számokat tudja tárolni.

Ezenkívül az `isize` és a `usize` típus annak a számítógépnek az
architektúrájától függ, amelyen a programod fut: 64 bites, ha 64 bites
architektúrán vagy, és 32 bites, ha 32 bites architektúrán.

Az egész literálokat a 3-2. táblázatban látható formák bármelyikében írhatod.
Vedd észre, hogy azok a számliterálok, amelyek többféle számtípusúak is
lehetnek, típusutótagot is kaphatnak – például `57u8` –, amivel megadható a
típus. A számliterálokban a `_` is használható vizuális elválasztóként, hogy a
szám könnyebben olvasható legyen, például `1_000`, amelynek ugyanaz az értéke,
mintha `1000`-t írtál volna.

<span class="caption">3-2. táblázat: Egész literálok Rustban</span>

| Számliterálok  | Példa       |
| ---------------- | ------------- |
| Decimális          | `98_222`      |
| Hexadecimális              | `0xff`        |
| Oktális            | `0o77`        |
| Bináris           | `0b1111_0000` |
| Bájt (csak `u8`) | `b'A'`        |

Honnan tudod hát, melyik egész típust használd? Ha bizonytalan vagy, a Rust
alapértelmezései általában jó kiindulópontot jelentenek: az egész típusok
alapértelmezése az `i32`. Az `isize` vagy a `usize` elsősorban akkor jön szóba,
amikor valamilyen kollekciót indexelsz.

> ##### Egész szám túlcsordulás
>
> Tegyük fel, hogy van egy `u8` típusú változód, amely a 0 és 255 közötti
> értékeket tudja tárolni. Ha a változót ezen a tartományon kívüli értékre –
> például 256-ra – próbálod állítani, _egész szám túlcsordulás_ történik, aminek
> kétféle következménye lehet. Ha debug módban fordítasz, a Rust beépít egész
> szám túlcsordulás elleni ellenőrzéseket, amelyek hatására a programod
> futásidőben _panicot vált ki_, ha ez a helyzet előáll. A Rust a _panicking_
> kifejezést használja arra, amikor egy program hibával lép ki; a panicokról
> részletesebben a 9. fejezet [„Helyrehozhatatlan hibák a
> `panic!`-kal”][unrecoverable-errors-with-panic]<!-- ignore --> című részében
> lesz szó.
>
> Ha release módban, a `--release` kapcsolóval fordítasz, a Rust _nem_ épít be
> olyan túlcsordulás-ellenőrzéseket, amelyek panicot okoznának. Ehelyett, ha
> túlcsordulás történik, a Rust _kettes komplemens körbefordulást_ végez.
> Röviden: a típus által tárolható legnagyobb értéknél nagyobb értékek
> „körbefordulnak” a típus által tárolható legkisebb értékre. Egy `u8` esetén a
> 256-ból 0 lesz, a 257-ből 1, és így tovább. A program nem vált ki panicot, de
> a változóban valószínűleg nem az az érték lesz, amit vártál. Az egész szám
> túlcsordulás körbefordulós viselkedésére támaszkodni hibának számít.
>
> Ha explicit módon akarod kezelni a túlcsordulás lehetőségét, a standard
> könyvtár által a primitív számtípusokhoz biztosított alábbi metóduscsaládokat
> használhatod:
>
> - Körbefordulás minden fordítási módban a `wrapping_*` metódusokkal, például a
>   `wrapping_add`-del.
> - A `None` érték visszaadása túlcsordulás esetén a `checked_*` metódusokkal.
> - Az érték és egy logikai érték visszaadása, amely jelzi, volt-e túlcsordulás,
>   az `overflowing_*` metódusokkal.
> - Telítődés a típus minimum- vagy maximumértékénél a `saturating_*`
>   metódusokkal.

#### Lebegőpontos típusok

A Rustnak két primitív típusa is van a _lebegőpontos számokhoz_, vagyis a
tizedes törtekhez. A Rust lebegőpontos típusai az `f32` és az `f64`, amelyek 32,
illetve 64 bit méretűek. Az alapértelmezett típus az `f64`, mert a modern CPU-kon
nagyjából ugyanolyan gyors, mint az `f32`, de nagyobb pontosságra képes. Minden
lebegőpontos típus előjeles.

Íme egy példa, amely lebegőpontos számokat mutat működés közben:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

A lebegőpontos számok ábrázolása az IEEE-754 szabvány szerint történik.

#### Számműveletek

A Rust minden számtípushoz támogatja az elvárt alapvető matematikai
műveleteket: összeadás, kivonás, szorzás, osztás és maradékképzés. Az
egészosztás nulla felé csonkol a legközelebbi egész számra. Az alábbi kód
megmutatja, hogyan használnád az egyes számműveleteket egy `let` utasításban:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Ezekben az utasításokban minden kifejezés egy matematikai operátort használ, és
egyetlen értékké értékelődik ki, amely aztán egy változóhoz kötődik. A [B
függelék][appendix_b]<!-- ignore --> tartalmazza a Rust összes operátorának
listáját.

#### A logikai típus

Ahogy a legtöbb más programozási nyelvben, Rustban is két lehetséges értéke van
a logikai típusnak: `true` és `false`. A logikai értékek mérete egy bájt. A
logikai típust Rustban a `bool` szóval adjuk meg. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

A logikai értékeket leginkább feltételes szerkezetekben használjuk, például egy
`if` kifejezésben. Azt, hogy az `if` kifejezések hogyan működnek Rustban, a
[„Vezérlési szerkezetek”][control-flow]<!-- ignore --> című részben tárgyaljuk.

#### A karakter típus

A Rust `char` típusa a nyelv legalapvetőbb betűtípusa. Íme néhány példa `char`
értékek deklarálására:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Vedd észre, hogy a `char` literálokat egyszeres idézőjellel adjuk meg,
szemben a string literálokkal, amelyek kettős idézőjelet használnak. A Rust
`char` típusa 4 bájt méretű, és egy Unicode skalárértéket képvisel, ami azt
jelenti, hogy sokkal többet tud ábrázolni, mint pusztán az ASCII. Az ékezetes
betűk; a kínai, japán és koreai karakterek; az emojik; és a nulla szélességű
szóközök mind érvényes `char` értékek Rustban. A Unicode skalárértékek az
`U+0000`–`U+D7FF` és az `U+E000`–`U+10FFFF` tartományba esnek (a határokat is
beleértve). A „karakter” azonban valójában nem is fogalom a Unicode-ban, így
az, amit emberként „karakternek” gondolsz, nem feltétlenül esik egybe azzal,
ami Rustban egy `char`. Erről a témáról részletesen a 8. fejezet [„UTF-8
kódolású szöveg tárolása stringekben”][strings]<!-- ignore --> című részében
lesz szó.

### Összetett típusok

Az _összetett típusok_ több értéket foghatnak össze egyetlen típusba. A Rustnak
két primitív összetett típusa van: a tuple és a tömb.

#### A tuple típus {#the-tuple-type}

A _tuple_ általános módja annak, hogy több, különböző típusú értéket
csoportosítsunk egyetlen összetett típusba. A tuple-öknek rögzített a hosszuk:
ha egyszer deklaráltuk őket, a méretük nem nőhet és nem csökkenhet.

Tuple-t úgy hozunk létre, hogy zárójelek között vesszővel elválasztott
értéklistát írunk. A tuple minden pozíciójának van típusa, és a tuple-ben lévő
különböző értékek típusának nem kell megegyeznie. Ebben a példában opcionális
típusannotációkat is hozzáadtunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

A `tup` változó az egész tuple-höz kötődik, mert a tuple egyetlen összetett
elemnek számít. Ahhoz, hogy kinyerjük az egyes értékeket egy tuple-ből,
mintaillesztéssel destrukturálhatunk egy tuple-értéket, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Ez a program először létrehoz egy tuple-t, és hozzáköti a `tup` változóhoz.
Ezután egy mintát használ a `let`-tel, hogy a `tup`-ot három külön változóra –
`x`, `y` és `z` – bontsa. Ezt _destrukturálásnak_ nevezzük, mert az egyetlen
tuple-t három részre bontja. Végül a program kiírja az `y` értékét, ami `6.4`.

Egy tuple elemét közvetlenül is elérhetjük: egy pontot (`.`) írunk, majd utána
annak az értéknek az indexét, amelyet el akarunk érni. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Ez a program létrehozza az `x` tuple-t, majd a megfelelő indexek segítségével
eléri a tuple minden elemét. Ahogy a legtöbb programozási nyelvben, a tuple
első indexe a 0.

Az érték nélküli tuple-nek külön neve van: _unit_. Ezt az értéket és a hozzá
tartozó típust is `()`-ként írjuk, és üres értéket vagy üres visszatérési
típust jelöl. A kifejezések implicit módon a unit értékkel térnek vissza, ha
nem adnak vissza semmilyen más értéket.

#### A tömb típus

Több érték kollekcióját másképp is megkaphatjuk: _tömbbel_. A tuple-lel
ellentétben egy tömb minden elemének azonos típusúnak kell lennie. Néhány más
nyelv tömbjeivel ellentétben a Rust tömbjeinek rögzített a hosszuk.

Egy tömb értékeit szögletes zárójelek között, vesszővel elválasztott listaként
írjuk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

A tömbök akkor hasznosak, ha azt szeretnéd, hogy az adataid a stacken
foglalódjanak le – ahogy az eddig látott többi típus esetében is –, ne pedig a
heapen (a stackről és a heapről bővebben a [4. fejezetben][stack-and-heap]<!--
ignore --> lesz szó), vagy amikor biztosítani akarod, hogy mindig rögzített
számú elemed legyen. A tömb azonban nem olyan rugalmas, mint a vektor típus. A
vektor a standard könyvtár által biztosított hasonló kollekciótípus, amelynek a
mérete _viszont_ nőhet és csökkenhet, mert a tartalma a heapen él. Ha nem vagy
biztos benne, hogy tömböt vagy vektort használj, jó eséllyel vektort érdemes. A
[8. fejezet][vectors]<!-- ignore --> részletesebben tárgyalja a vektorokat.

A tömbök viszont hasznosabbak, ha tudod, hogy az elemek számának nem kell majd
változnia. Ha például a hónapok neveit használnád egy programban,
valószínűleg tömböt választanál vektor helyett, mert tudod, hogy mindig 12
elemet fog tartalmazni:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Egy tömb típusát szögletes zárójelekkel írod le: benne az egyes elemek típusa,
egy pontosvessző, majd a tömb elemeinek száma, így:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Itt az `i32` az egyes elemek típusa. A pontosvessző után az `5` szám azt
jelzi, hogy a tömb öt elemet tartalmaz.

Egy tömböt úgy is inicializálhatsz, hogy minden eleme ugyanazt az értéket
tartalmazza: megadod a kezdőértéket, utána egy pontosvesszőt, majd szögletes
zárójelben a tömb hosszát, ahogy itt látható:

```rust
let a = [3; 5];
```

Az `a` nevű tömb `5` elemet fog tartalmazni, amelyek kezdetben mind a `3`
értékre lesznek beállítva. Ez ugyanaz, mintha a `let a = [3, 3, 3, 3, 3];`
sort írnád, csak tömörebb módon.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Tömbelemek elérése

A tömb egyetlen, ismert és rögzített méretű memóriadarab, amely a stacken
foglalható le. A tömb elemeit indexeléssel érheted el, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Ebben a példában a `first` nevű változó az `1` értéket kapja, mert ez az érték
található a tömb `[0]` indexén. A `second` nevű változó a `2` értéket kapja a
tömb `[1]` indexéről.

#### Érvénytelen tömbelem elérése

Nézzük meg, mi történik, ha a tömb végén túli elemet próbálsz elérni. Tegyük
fel, hogy lefuttatod ezt a – a 2. fejezet kitalálós játékához hasonló – kódot,
hogy egy tömbindexet kérj be a felhasználótól:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Ez a kód sikeresen lefordul. Ha a `cargo run` paranccsal futtatod, és `0`-t,
`1`-et, `2`-t, `3`-at vagy `4`-et adsz meg, a program kiírja a tömb megfelelő
indexén található értéket. Ha viszont a tömb végén túli számot adsz meg,
például `10`-et, ehhez hasonló kimenetet fogsz látni:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

A program futásidejű hibát eredményezett azon a ponton, ahol érvénytelen
értéket használt az indexelési műveletben. A program hibaüzenettel lépett ki, és
nem hajtotta végre az utolsó `println!` utasítást. Amikor indexeléssel próbálsz
elérni egy elemet, a Rust ellenőrzi, hogy a megadott index kisebb-e a tömb
hosszánál. Ha az index nagyobb vagy egyenlő a hossznál, a Rust panicot vált ki.
Ennek az ellenőrzésnek futásidőben kell megtörténnie, különösen ebben az
esetben, mert a fordító sehogy sem tudhatja, milyen értéket ad majd meg a
felhasználó, amikor később futtatja a kódot.

Ez egy példa a Rust memóriabiztonsági elveinek működésére. Sok alacsony szintű
nyelvben nem történik meg ez az ellenőrzés, és ha hibás indexet adsz meg,
érvénytelen memóriaterület válik elérhetővé. A Rust úgy véd meg az ilyen
hibáktól, hogy azonnal kilép, ahelyett hogy engedélyezné a memóriahozzáférést és
folytatná a futást. A 9. fejezet többet foglalkozik a Rust hibakezelésével, és
azzal, hogyan írhatsz olvasható, biztonságos kódot, amely sem panicot nem vált
ki, sem érvénytelen memóriahozzáférést nem enged meg.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
