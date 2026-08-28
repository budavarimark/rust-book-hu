## UTF-8 kódolású szöveg tárolása sztringekkel {#storing-utf-8-encoded-text-with-strings}

A 4. fejezetben már beszéltünk a sztringekről, most azonban alaposabban is
megnézzük őket. A kezdő Rust-programozók gyakran akadnak el a sztringeknél,
három ok együttes hatására: a Rust hajlamos felszínre hozni a lehetséges
hibákat, a sztringek bonyolultabb adatszerkezetek, mint azt sok programozó
gondolná, és ott van még az UTF-8 is. Ezek a tényezők úgy adódnak össze, hogy
más programozási nyelvek felől érkezve nehéznek tűnhetnek.

A sztringeket a kollekciók kontextusában tárgyaljuk, mert a sztringek bájtok
kollekciójaként vannak megvalósítva, kiegészítve néhány metódussal, amelyek
hasznos funkcionalitást nyújtanak, amikor ezeket a bájtokat szövegként
értelmezzük. Ebben a szakaszban a `String` azon műveleteiről beszélünk, amelyek
minden kollekciótípusnál megvannak, például a létrehozásról, a módosításról és
az olvasásról. Szóba kerül az is, miben különbözik a `String` a többi
kollekciótól, nevezetesen hogy a `String` indexelését mennyire bonyolítja az,
hogy az emberek és a számítógépek eltérően értelmezik a `String` adatait.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### A sztringek meghatározása

Először határozzuk meg, mit értünk a _sztring_ kifejezés alatt. A Rustnak a
nyelv magjában csak egyetlen sztringtípusa van, ez a string slice `str`,
amelyet általában a kölcsönzött, `&str` alakjában látunk. A 4. fejezetben már
beszéltünk a string slice-okról, amelyek valahol máshol tárolt, UTF-8 kódolású
sztringadatokra mutató referenciák. A sztringliterálok például a program
binárisában tárolódnak, ezért string slice-ok.

A `String` típus, amelyet nem a nyelv magja tartalmaz, hanem a Rust standard
könyvtára biztosít, egy növelhető, módosítható, tulajdonolt, UTF-8 kódolású
sztringtípus. Amikor a Rust-programozók a Rustban „sztringekről” beszélnek,
akár a `String`, akár a string slice `&str` típusra gondolhatnak, nem csupán az
egyikre. Bár ez a szakasz nagyrészt a `String`-ről szól, mindkét típust
erőteljesen használja a Rust standard könyvtára, és mind a `String`, mind a
string slice-ok UTF-8 kódolásúak.

### Új `String` létrehozása

A `Vec<T>`-nél elérhető műveletek közül sok a `String`-nél is elérhető, mert a
`String` valójában egy bájtvektor köré épülő burkolóként van megvalósítva,
néhány további garanciával, megkötéssel és képességgel. Olyan függvényre példa,
amely ugyanúgy működik a `Vec<T>` és a `String` esetében, a példány
létrehozására szolgáló `new` függvény, amelyet a 8-11. lista mutat be.

<Listing number="8-11" caption="Új, üres `String` létrehozása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Ez a sor egy új, üres, `s` nevű sztringet hoz létre, amelybe aztán adatokat
tölthetünk. Gyakran van valamilyen kezdeti adatunk, amellyel indítani
szeretnénk a sztringet. Ehhez a `to_string` metódust használjuk, amely minden
olyan típuson elérhető, amely implementálja a `Display` traitet – ahogy a
sztringliterálok is teszik. A 8-12. lista két példát mutat.

<Listing number="8-12" caption="A `to_string` metódus használata `String` létrehozására sztringliterálból">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Ez a kód egy `initial contents` tartalmú sztringet hoz létre.

Használhatjuk a `String::from` függvényt is arra, hogy sztringliterálból
`String`-et hozzunk létre. A 8-13. lista kódja egyenértékű a 8-12. lista
`to_string`-et használó kódjával.

<Listing number="8-13" caption="A `String::from` függvény használata `String` létrehozására sztringliterálból">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Mivel a sztringeket rengeteg mindenre használjuk, sokféle generikus API áll
rendelkezésünkre hozzájuk, ami sok lehetőséget ad. Némelyikük feleslegesnek
tűnhet, de mindegyiknek megvan a maga helye! Ebben az esetben a `String::from`
és a `to_string` ugyanazt csinálja, így hogy melyiket választod, stílus és
olvashatóság kérdése.

Ne feledd, hogy a sztringek UTF-8 kódolásúak, így bármilyen helyesen kódolt
adatot elhelyezhetünk bennük, ahogy a 8-14. listában látható.

<Listing number="8-14" caption="Különböző nyelvű üdvözlések tárolása sztringekben">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Ezek mind érvényes `String` értékek.

### Egy `String` módosítása

Egy `String` mérete növekedhet, és a tartalma megváltozhat, akárcsak egy
`Vec<T>` tartalma, ha további adatokat teszel bele. Ezenkívül kényelmesen
használhatod a `+` operátort vagy a `format!` makrót `String` értékek
összefűzésére.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Hozzáfűzés a `push_str` vagy a `push` segítségével

Egy `String`-et úgy tudunk növelni, hogy a `push_str` metódussal string slice-ot
fűzünk hozzá, ahogy a 8-15. listában látható.

<Listing number="8-15" caption="String slice hozzáfűzése egy `String`-hez a `push_str` metódussal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

E két sor után az `s` a `foobar` értéket fogja tartalmazni. A `push_str`
metódus string slice-ot vár, mert nem feltétlenül akarjuk átvenni a paraméter
ownershipjét. A 8-16. lista kódjában például azt szeretnénk, hogy az `s2` az
után is használható legyen, hogy a tartalmát hozzáfűztük az `s1`-hez.

<Listing number="8-16" caption="String slice használata azután, hogy a tartalmát hozzáfűztük egy `String`-hez">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Ha a `push_str` metódus átvenné az `s2` ownershipjét, nem tudnánk kiírni az
értékét az utolsó sorban. Így azonban ez a kód pontosan úgy működik, ahogy
elvárnánk!

A `push` metódus egyetlen karaktert vár paraméterként, és hozzáadja a
`String`-hez. A 8-17. lista az _l_ betűt adja hozzá egy `String`-hez a `push`
metódussal.

<Listing number="8-17" caption="Egyetlen karakter hozzáadása egy `String` értékhez a `push` segítségével">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Ennek eredményeként az `s` a `lol` értéket fogja tartalmazni.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Összefűzés a `+` vagy a `format!` segítségével {#concatenating-with--or-format}

Gyakran szeretnél két meglévő sztringet egyesíteni. Ennek egyik módja a `+`
operátor használata, ahogy a 8-18. listában látható.

<Listing number="8-18" caption="A `+` operátor használata két `String` érték egyesítésére egy új `String` értékké">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Az `s3` sztring a `Hello, world!` értéket fogja tartalmazni. Hogy az `s1` miért
nem érvényes többé az összeadás után, és hogy miért az `s2`-re mutató
referenciát használtuk, annak a `+` operátor használatakor meghívott metódus
szignatúrájához van köze. A `+` operátor az `add` metódust használja, amelynek
a szignatúrája nagyjából így néz ki:

```rust,ignore
fn add(self, s: &str) -> String {
```

A standard könyvtárban az `add`-et generikusokkal és asszociált típusokkal
definiálva látod majd. Itt konkrét típusokat helyettesítettünk be, ez történik
ugyanis, amikor ezt a metódust `String` értékekkel hívjuk meg. A generikusokat
a 10. fejezetben tárgyaljuk. Ez a szignatúra megadja azokat a támpontokat,
amelyekre szükségünk van a `+` operátor trükkös részleteinek megértéséhez.

Először is, az `s2` előtt `&` áll, ami azt jelenti, hogy a második sztring egy
referenciáját adjuk hozzá az első sztringhez. Ez az `add` függvény `s`
paramétere miatt van: csak string slice-ot adhatunk hozzá egy `String`-hez;
két `String` értéket nem adhatunk össze. De várjunk csak – az `&s2` típusa
`&String`, nem `&str`, ahogy azt az `add` második paraméterénél megadták. Akkor
miért fordul le a 8-18. lista?

Azért tudjuk az `&s2`-t használni az `add` hívásában, mert a fordító képes az
`&String` argumentumot `&str`-ré alakítani. Amikor meghívjuk az `add` metódust,
a Rust deref coercion-t alkalmaz, ami itt az `&s2`-t `&s2[..]`-vé alakítja. A
deref coercionről részletesebben a 15. fejezetben lesz szó. Mivel az `add` nem
veszi át az `s` paraméter ownershipjét, az `s2` a művelet után is érvényes
`String` marad.

Másodszor, a szignatúrából látszik, hogy az `add` átveszi a `self`
ownershipjét, mert a `self` előtt _nem_ áll `&`. Ez azt jelenti, hogy a 8-18.
listában az `s1` bemozdul az `add` hívásába, és utána már nem lesz érvényes.
Tehát bár a `let s3 = s1 + &s2;` úgy néz ki, mintha mindkét sztringet lemásolná
és egy újat hozna létre, ez az utasítás valójában átveszi az `s1` ownershipjét,
hozzáfűzi az `s2` tartalmának egy másolatát, majd visszaadja az eredmény
ownershipjét. Más szóval: úgy néz ki, mintha rengeteget másolna, pedig nem; az
implementáció hatékonyabb a másolásnál.

Ha több sztringet kell összefűznünk, a `+` operátor viselkedése nehézkessé
válik:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Ezen a ponton az `s` a `tic-tac-toe` lesz. A sok `+` és `"` karakter miatt
nehéz látni, mi történik. Sztringek bonyolultabb módon való egyesítéséhez
inkább a `format!` makrót használhatjuk:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Ez a kód is a `tic-tac-toe` értéket állítja be az `s`-nek. A `format!` makró
úgy működik, mint a `println!`, csakhogy a kimenetet nem a képernyőre írja,
hanem egy `String`-et ad vissza a tartalommal. A kód `format!`-et használó
változata sokkal könnyebben olvasható, és a `format!` makró által generált kód
referenciákat használ, így ez a hívás egyik paraméterének ownershipjét sem
veszi át.

### Sztringek indexelése

Sok más programozási nyelvben érvényes és gyakori művelet, hogy egy sztring
egyes karaktereit index szerinti hivatkozással érjük el. Ha azonban a Rustban
indexelő szintaxissal próbálod elérni egy `String` részeit, hibát fogsz kapni.
Nézd meg a 8-19. lista érvénytelen kódját.

<Listing number="8-19" caption="Kísérlet indexelő szintaxis használatára egy `String`-gel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Ez a kód a következő hibát eredményezi:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

A hibaüzenet elárulja a lényeget: a Rust sztringjei nem támogatják az
indexelést. De miért nem? A kérdés megválaszolásához meg kell beszélnünk,
hogyan tárolja a Rust a sztringeket a memóriában.

#### Belső reprezentáció

A `String` egy `Vec<u8>` köré épülő burkoló. Nézzük meg a 8-14. lista néhány
helyesen kódolt UTF-8 példasztringjét. Először ezt:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Ebben az esetben a `len` értéke `4` lesz, ami azt jelenti, hogy a `"Hola"`
sztringet tároló vektor 4 bájt hosszú. Ezek a betűk UTF-8-ban kódolva egyenként
1 bájtot foglalnak. A következő sor viszont meglepetést okozhat (figyeld meg,
hogy ez a sztring a nagy cirill _Ze_ betűvel kezdődik, nem a 3-as számmal):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Ha megkérdeznék tőled, milyen hosszú ez a sztring, talán azt mondanád, hogy 12.
Valójában a Rust válasza 24: ennyi bájtra van szükség a „Здравствуйте” UTF-8
kódolásához, mert az ebben a sztringben lévő Unicode-skalárértékek egyenként 2
bájtnyi helyet foglalnak. Ezért a sztring bájtjaiba mutató index nem mindig
felel meg egy érvényes Unicode-skalárértéknek. Szemléltetésképp nézd meg ezt az
érvénytelen Rust-kódot:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Már tudod, hogy az `answer` nem a `З` lesz, az első betű. UTF-8-ban kódolva a
`З` első bájtja `208`, a második pedig `151`, így úgy tűnhet, hogy az `answer`
valójában `208` kellene, hogy legyen – de a `208` önmagában nem érvényes
karakter. A `208` visszaadása valószínűleg nem az, amit a felhasználó szeretne,
ha ennek a sztringnek az első betűjét kéri; ugyanakkor a Rustnak csak ez az
adata van a 0. bájtindexen. A felhasználók általában nem a bájtértéket akarják
visszakapni, még akkor sem, ha a sztring csak latin betűket tartalmaz: ha az
`&"hi"[0]` érvényes kód lenne, és a bájtértéket adná vissza, `104`-et adna
vissza, nem `h`-t.

A válasz tehát az, hogy a váratlan érték visszaadásának és az esetleg nem
azonnal felfedezett hibáknak az elkerülése érdekében a Rust ezt a kódot le sem
fordítja, így a fejlesztési folyamat korai szakaszában megelőzi a
félreértéseket.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Bájtok, skalárértékek és grafémaklaszterek

Az UTF-8-cal kapcsolatban egy másik szempont, hogy a Rust nézőpontjából
valójában háromféle releváns módon lehet a sztringekre tekinteni: bájtokként,
skalárértékekként és grafémaklaszterekként (ez utóbbi áll a legközelebb ahhoz,
amit _betűnek_ neveznénk).

Ha megnézzük a dévanágari írással írt „नमस्ते” hindi szót, az `u8` értékek olyan
vektoraként tárolódik, amely így néz ki:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Ez 18 bájt, és végső soron így tárolják a számítógépek ezt az adatot. Ha
Unicode-skalárértékekként nézzük őket – és a Rust `char` típusa éppen ez –,
azok a bájtok így festenek:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Itt hat `char` érték van, de a negyedik és a hatodik nem betű: ezek olyan
diakritikus jelek, amelyeknek önmagukban nincs értelmük. Végül, ha
grafémaklaszterekként nézzük őket, azt kapjuk, amit egy ember a hindi szót
alkotó négy betűnek nevezne:

```text
["न", "म", "स्", "ते"]
```

A Rust különböző módokat kínál a számítógépek által tárolt nyers sztringadatok
értelmezésére, hogy minden program azt az értelmezést választhassa, amelyre
szüksége van, függetlenül attól, milyen emberi nyelven van az adat.

Az utolsó ok, amiért a Rust nem engedi, hogy egy `String`-et indexeljünk egy
karakter megszerzéséhez, az, hogy az indexelő műveletektől elvárjuk, hogy
mindig konstans idő alatt fussanak le (O(1)). Ezt a teljesítményt azonban egy
`String` esetében nem lehet garantálni, mert a Rustnak végig kellene járnia a
tartalmat az elejétől az indexig, hogy megállapítsa, hány érvényes karakter
volt benne.

### Sztringek szeletelése

Egy sztring indexelése gyakran rossz ötlet, mert nem egyértelmű, minek kellene
lennie a sztringindexelő művelet visszatérési típusának: bájtértéknek,
karakternek, grafémaklaszternek vagy string slice-nak. Ezért, ha tényleg
indexeket kell használnod string slice-ok létrehozásához, a Rust arra kér, hogy
légy pontosabb.

Ahelyett, hogy a `[]`-t egyetlen számmal használnád, használhatod a `[]`-t egy
tartománnyal, hogy adott bájtokat tartalmazó string slice-ot hozz létre:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Itt az `s` egy `&str` lesz, amely a sztring első 4 bájtját tartalmazza. Korábban
említettük, hogy ezek a karakterek egyenként 2 bájtosak, ami azt jelenti, hogy
az `s` a `Зд` lesz.

Ha csak egy karakter bájtjainak egy részét próbálnánk kiszeletelni, mondjuk az
`&hello[0..1]`-gyel, a Rust futásidőben panicot váltana ki, ugyanúgy, mintha
egy vektorban érvénytelen indexet érnénk el:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Óvatosan kell eljárnod, amikor tartományokkal hozol létre string slice-okat,
mert ezzel összeomlaszthatod a programodat.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Iterálás sztringeken

A legjobb módja annak, hogy sztringek részein dolgozzunk, ha egyértelműen
megmondjuk, karaktereket vagy bájtokat akarunk-e. Az egyes
Unicode-skalárértékekhez használd a `chars` metódust. A `chars` meghívása a
„Зд”-n két `char` típusú értéket különít el és ad vissza, az eredményen pedig
végigiterálhatsz, hogy minden elemet elérj:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Ez a kód a következőt írja ki:

```text
З
д
```

Alternatívaként a `bytes` metódus minden nyers bájtot visszaad, ami a te
területeden megfelelő lehet:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Ez a kód azt a 4 bájtot írja ki, amelyekből ez a sztring áll:

```text
208
151
208
180
```

De ne feledd: az érvényes Unicode-skalárértékek 1 bájtnál többől is állhatnak.

Grafémaklasztereket kinyerni a sztringekből – ahogy a dévanágari írásnál is –
összetett feladat, ezért ezt a funkcionalitást a standard könyvtár nem
biztosítja. Ha erre a funkcionalitásra van szükséged, a
[crates.io](https://crates.io/)<!-- ignore --> oldalon elérhetők crate-ek.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### A sztringek bonyolultságának kezelése

Összefoglalva: a sztringek bonyolultak. A különböző programozási nyelvek
másképp döntenek arról, hogyan mutatják be ezt a bonyolultságot a
programozónak. A Rust úgy döntött, hogy a `String` adatok helyes kezelését
teszi az alapértelmezett viselkedéssé minden Rust-program számára, ami azt
jelenti, hogy a programozóknak már az elején több gondolatot kell fordítaniuk
az UTF-8 adatok kezelésére. Ez a kompromisszum a sztringek bonyolultságából
többet tár fel, mint ami más programozási nyelvekben látszik, cserébe viszont
megkíméli attól, hogy a fejlesztési életciklus későbbi szakaszában kelljen a
nem ASCII karakterekkel kapcsolatos hibákkal foglalkoznod.

A jó hír az, hogy a standard könyvtár rengeteg olyan funkcionalitást kínál a
`String` és a `&str` típusokra építve, amelyek segítenek ezeket az összetett
helyzeteket helyesen kezelni. Mindenképp nézd meg a dokumentációt az olyan
hasznos metódusokért, mint a `contains` a sztringben való kereséshez vagy a
`replace` a sztring egyes részeinek másik sztringre cseréléséhez.

Váltsunk valami kicsit kevésbé bonyolultra: a hash mapekre!
