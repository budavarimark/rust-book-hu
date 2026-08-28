## Crate publikálása a Crates.io-ra

Használtunk már a [crates.io](https://crates.io/)<!-- ignore --> oldalról
származó csomagokat a projektünk függőségeiként, de a saját csomagjaid
publikálásával te is megoszthatod a kódodat másokkal. A
[crates.io](https://crates.io/)<!-- ignore --> crate-regiszter a csomagjaid
forráskódját terjeszti, ezért elsősorban nyílt forráskódú kódnak ad otthont.

A Rustnak és a Cargónak vannak olyan képességei, amelyekkel a publikált
csomagodat könnyebben megtalálják és használják mások. Ezek közül tárgyalunk
néhányat, majd elmagyarázzuk, hogyan kell publikálni egy csomagot.

### Hasznos dokumentációs kommentek írása

Ha pontosan dokumentálod a csomagjaidat, azzal segítesz a többi
felhasználónak megtudni, hogyan és mikor használják őket, ezért érdemes időt
fektetni a dokumentáció megírásába. A 3. fejezetben megbeszéltük, hogyan
kommentelhető a Rust-kód két perjellel, `//`. A Rustnak van egy sajátos
kommentfajtája is a dokumentációhoz, amelyet találóan _dokumentációs
kommentnek_ nevezünk, és amelyből HTML-dokumentáció generálódik. A HTML a
publikus API-elemek dokumentációs kommentjeinek tartalmát jeleníti meg azoknak
a programozóknak, akiket az érdekel, hogyan _használják_ a crate-edet, nem
pedig az, hogyan van a crate-ed _implementálva_.

A dokumentációs kommentek kettő helyett három perjelet használnak, `///`, és
Markdown-jelölést támogatnak a szöveg formázásához. A dokumentációs
kommenteket közvetlenül az általuk dokumentált elem elé kell tenni. A 14-1.
lista egy `my_crate` nevű crate-ben lévő `add_one` függvény dokumentációs
kommentjeit mutatja be.

<Listing number="14-1" file-name="src/lib.rs" caption="Egy függvény dokumentációs kommentje">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Itt leírjuk, mit csinál az `add_one` függvény, elkezdünk egy `Examples` című
szakaszt, majd olyan kódot adunk meg, amely bemutatja az `add_one` függvény
használatát. A HTML-dokumentációt ebből a dokumentációs kommentből a `cargo
doc` futtatásával generálhatjuk. Ez a parancs a Rusttal együtt terjesztett
`rustdoc` eszközt futtatja, és a generált HTML-dokumentációt a _target/doc_
könyvtárba teszi.

A kényelem kedvéért a `cargo doc --open` futtatása felépíti az aktuális
crate-ed dokumentációjának HTML-jét (és a crate összes függőségének
dokumentációját is), majd megnyitja az eredményt egy webböngészőben. Navigálj
az `add_one` függvényhez, és látni fogod, hogyan jelenik meg a dokumentációs
kommentek szövege, ahogy a 14-1. ábra mutatja.

<img alt="A `my_crate` `add_one` függvényének megjelenített HTML-dokumentációja" src="img/trpl14-01.png" class="center" />

<span class="caption">14-1. ábra: Az `add_one` függvény
HTML-dokumentációja</span>

#### Gyakran használt szakaszok

A 14-1. listában az `# Examples` Markdown-címsort használtuk, hogy létrehozzunk
egy „Examples” című szakaszt a HTML-ben. Íme néhány további szakasz, amelyet a
crate-ek szerzői gyakran használnak a dokumentációjukban:

- **Panics**: Azok a helyzetek, amelyekben a dokumentált függvény panicot
  válthat ki. A függvény hívóinak, akik nem szeretnék, hogy a programjuk
  leálljon egy panickel, ügyelniük kell arra, hogy ezekben a helyzetekben ne
  hívják meg a függvényt.
- **Errors**: Ha a függvény `Result` értéket ad vissza, akkor a lehetséges
  hibafajták és az azokat kiváltó körülmények leírása hasznos lehet a hívóknak,
  hogy olyan kódot írhassanak, amely a különböző hibafajtákat különbözőképpen
  kezeli.
- **Safety**: Ha a függvény meghívása `unsafe` (a nem biztonságos kódról a 20.
  fejezetben lesz szó), akkor legyen egy szakasz, amely elmagyarázza, miért nem
  biztonságos a függvény, és bemutatja azokat az invariánsokat, amelyek
  betartását a függvény elvárja a hívóktól.

A legtöbb dokumentációs kommentnek nincs szüksége mindegyik szakaszra, de ez jó
ellenőrzőlista, amely emlékeztet arra, mely szempontok érdekelhetik a kódod
felhasználóit.

#### Dokumentációs kommentek tesztként {#documentation-comments-as-tests}

Ha példakódblokkokat teszel a dokumentációs kommentjeidbe, azzal segíthetsz
bemutatni a könyvtárad használatát, és van egy további előnye is: a `cargo
test` futtatása tesztként lefuttatja a dokumentációdban lévő
kódpéldákat! Semmi sem jobb egy példákkal ellátott dokumentációnál. De semmi
sem rosszabb az olyan példáknál, amelyek nem működnek, mert a kód megváltozott
a dokumentáció megírása óta. Ha a `cargo test` parancsot a 14-1. listából
származó `add_one` függvény dokumentációjával futtatjuk, a tesztek
eredményében ehhez hasonló szakaszt fogunk látni:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Ha most megváltoztatjuk akár a függvényt, akár a példát úgy, hogy a példában
lévő `assert_eq!` panicot váltson ki, és újra lefuttatjuk a `cargo test`
parancsot, látni fogjuk, hogy a doktesztek észreveszik: a példa és a kód
kiestek egymással a szinkronból!

<!-- Old headings. Do not remove or links may break. -->

<a id="commenting-contained-items"></a>

#### A tartalmazó elem kommentjei

A `//!` stílusú dokumentációs komment ahhoz az elemhez fűz dokumentációt, amely
*tartalmazza* a kommenteket, nem pedig a kommenteket *követő* elemekhez.
Ezeket a dokumentációs kommenteket jellemzően a crate gyökérfájljában
(megállapodás szerint _src/lib.rs_) vagy egy modulon belül használjuk, hogy a
crate-et vagy a modult mint egészet dokumentáljuk.

Ha például olyan dokumentációt szeretnénk hozzáadni, amely leírja az `add_one`
függvényt tartalmazó `my_crate` crate célját, akkor `//!` kezdetű dokumentációs
kommenteket teszünk a _src/lib.rs_ fájl elejére, ahogy a 14-2. lista mutatja.

<Listing number="14-2" file-name="src/lib.rs" caption="A `my_crate` crate egészének dokumentációja">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Vedd észre, hogy a `//!` jellel kezdődő utolsó sor után nincs semmilyen kód.
Mivel a kommenteket `///` helyett `//!` jellel kezdtük, azt az elemet
dokumentáljuk, amely tartalmazza ezt a kommentet, nem pedig a kommentet követő
elemet. Ebben az esetben ez az elem a _src/lib.rs_ fájl, amely a crate gyökere.
Ezek a kommentek az egész crate-et írják le.

Amikor lefuttatjuk a `cargo doc --open` parancsot, ezek a kommentek a
`my_crate` dokumentációjának címoldalán, a crate publikus elemeinek listája
fölött jelennek meg, ahogy a 14-2. ábra mutatja.

Az elemeken belüli dokumentációs kommentek különösen crate-ek és modulok
leírásához hasznosak. Használd őket arra, hogy elmagyarázd a tartalmazó egység
átfogó célját, ezzel segítve a felhasználóidat a crate szerkezetének
megértésében.

<img alt="Megjelenített HTML-dokumentáció a crate egészét leíró kommenttel" src="img/trpl14-02.png" class="center" />

<span class="caption">14-2. ábra: A `my_crate` megjelenített dokumentációja, a
crate egészét leíró kommenttel együtt</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

### Kényelmes publikus API exportálása {#exporting-a-convenient-public-api}

A publikus API-d szerkezete fontos szempont egy crate publikálásakor. Azok,
akik a crate-edet használják, kevésbé ismerik a szerkezetét, mint te, és nehezen
találhatják meg a használni kívánt darabokat, ha a crate-ednek nagy a
modulhierarchiája.

A 7. fejezetben szó volt arról, hogyan tehetünk elemeket publikussá a `pub`
kulcsszóval, és hogyan hozhatunk be elemeket egy hatókörbe a `use` kulcsszóval.
Az a szerkezet azonban, amely neked logikusnak tűnik a crate fejlesztése
közben, nem feltétlenül kényelmes a felhasználóid számára. Lehet, hogy a
structjaidat több szintből álló hierarchiába szeretnéd szervezni, de akkor
azoknak, akik a hierarchia mélyén definiált típusaid egyikét szeretnék
használni, gondot okozhat egyáltalán rájönni, hogy az a típus létezik. Az is
bosszanthatja őket, hogy a `use my_crate::UsefulType;` helyett a `use
my_crate::some_module::another_module::UsefulType;` sort kell beírniuk.

A jó hír az, hogy ha a szerkezet _nem_ kényelmes mások számára egy másik
könyvtárból való használatra, akkor sem kell átrendezned a belső felépítésedet:
ehelyett újraexportálhatod az elemeket, hogy a privát szerkezetedtől eltérő
publikus szerkezetet alakíts ki, a `pub use` segítségével. Az *újraexportálás*
fog egy adott helyen publikus elemet, és publikussá teszi egy másik helyen is,
mintha ott lenne definiálva.

Tegyük fel például, hogy készítettünk egy `art` nevű könyvtárat művészeti
fogalmak modellezésére. Ebben a könyvtárban két modul van: egy `kinds` modul,
amely két enumot tartalmaz `PrimaryColor` és `SecondaryColor` néven, valamint
egy `utils` modul, amely egy `mix` nevű függvényt tartalmaz, ahogy a 14-3.
lista mutatja.

<Listing number="14-3" file-name="src/lib.rs" caption="Egy `art` könyvtár, amelynek elemei `kinds` és `utils` modulokba vannak szervezve">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

A 14-3. ábra azt mutatja, hogyan nézne ki ennek a crate-nek a `cargo doc` által
generált dokumentációjának címoldala.

<img alt="Az `art` crate megjelenített dokumentációja, amely felsorolja a `kinds` és `utils` modulokat" src="img/trpl14-03.png" class="center" />

<span class="caption">14-3. ábra: Az `art` dokumentációjának címoldala, amely a
`kinds` és `utils` modulokat sorolja fel</span>

Figyeld meg, hogy sem a `PrimaryColor` és `SecondaryColor` típusok, sem a `mix`
függvény nincs felsorolva a címoldalon. A `kinds` és a `utils` elemre kell
kattintanunk, hogy lássuk őket.

Egy másik crate-nek, amely ettől a könyvtártól függ, olyan `use` utasításokra
lenne szüksége, amelyek behozzák az `art` elemeit a hatókörbe, megadva a
jelenleg definiált modulszerkezetet. A 14-4. lista egy olyan crate példáját
mutatja, amely az `art` crate `PrimaryColor` és `mix` elemeit használja.

<Listing number="14-4" file-name="src/main.rs" caption="Egy crate, amely az `art` crate elemeit használja annak belső szerkezetével exportálva">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

A 14-4. lista kódjának szerzőjének, aki az `art` crate-et használja, ki kellett
derítenie, hogy a `PrimaryColor` a `kinds` modulban, a `mix` pedig a `utils`
modulban van. Az `art` crate modulszerkezete inkább az `art` crate-en dolgozó
fejlesztők szempontjából érdekes, mint azok szempontjából, akik használják. A
belső szerkezet semmilyen hasznos információt nem tartalmaz annak, aki azt
próbálja megérteni, hogyan használja az `art` crate-et; sőt zavart okoz, mert
az azt használó fejlesztőknek ki kell találniuk, hol keressenek, és meg kell
adniuk a modulneveket a `use` utasításokban.

Hogy eltávolítsuk a belső felépítést a publikus API-ból, módosíthatjuk a 14-3.
listában lévő `art` crate kódját úgy, hogy `pub use` utasításokat adunk hozzá,
és a legfelső szinten újraexportáljuk az elemeket, ahogy a 14-5. lista mutatja.

<Listing number="14-5" file-name="src/lib.rs" caption="`pub use` utasítások hozzáadása az elemek újraexportálásához">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

A `cargo doc` által ehhez a crate-hez generált API-dokumentáció mostantól
felsorolja és linkeli az újraexportokat a címoldalon, ahogy a 14-4. ábra
mutatja, így a `PrimaryColor` és `SecondaryColor` típusok, valamint a `mix`
függvény könnyebben megtalálható.

<img alt="Az `art` crate megjelenített dokumentációja az újraexportokkal a címoldalon" src="img/trpl14-04.png" class="center" />

<span class="caption">14-4. ábra: Az `art` dokumentációjának címoldala, amely
felsorolja az újraexportokat</span>

Az `art` crate felhasználói továbbra is látják és használhatják a 14-3. listából
származó belső szerkezetet, ahogy azt a 14-4. lista bemutatja, vagy
használhatják a 14-5. listában lévő kényelmesebb szerkezetet, ahogy a 14-6.
lista mutatja.

<Listing number="14-6" file-name="src/main.rs" caption="Egy program, amely az `art` crate újraexportált elemeit használja">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Olyan esetekben, amikor sok egymásba ágyazott modul van, a típusok legfelső
szintű újraexportálása a `pub use` segítségével jelentős különbséget jelenthet
a crate-et használók élményében. A `pub use` egy másik gyakori alkalmazása az,
hogy egy függőség definícióit újraexportáljuk az aktuális crate-ben, hogy az
adott crate definíciói a te crate-ed publikus API-jának részévé váljanak.

Egy hasznos publikus API-szerkezet kialakítása inkább művészet, mint tudomány,
és iterálhatsz, amíg meg nem találod a felhasználóid számára legjobban működő
API-t. A `pub use` választása rugalmasságot ad abban, hogyan strukturálod
belülről a crate-edet, és leválasztja ezt a belső szerkezetet arról, amit a
felhasználóidnak mutatsz. Nézd meg néhány telepített crate kódját, és
figyeld meg, eltér-e a belső szerkezetük a publikus API-juktól.

### Crates.io-fiók létrehozása

Mielőtt bármilyen crate-et publikálhatnál, létre kell hoznod egy fiókot a
[crates.io](https://crates.io/)<!-- ignore --> oldalon, és szerezned kell egy
API-tokent. Ehhez látogass el a [crates.io](https://crates.io/)<!-- ignore -->
kezdőlapjára, és jelentkezz be egy GitHub-fiókkal. (A GitHub-fiók jelenleg
követelmény, de az oldal a jövőben más módokat is támogathat a
fiókregisztrációra.) Miután bejelentkeztél, látogasd meg a fiókbeállításaidat a
[https://crates.io/me/](https://crates.io/me/)<!-- ignore --> címen, és szerezd
meg az API-kulcsodat. Ezután futtasd a `cargo login` parancsot, és illeszd be
az API-kulcsodat, amikor a program kéri, így:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

Ez a parancs tudatja a Cargóval az API-tokenedet, és helyben tárolja a
_~/.cargo/credentials.toml_ fájlban. Vedd figyelembe, hogy ez a token titok: ne
oszd meg senki mással. Ha bármilyen okból mégis megosztod valakivel, vissza kell
vonnod, és új tokent kell generálnod a [crates.io](https://crates.io/)<!-- ignore
--> oldalon.

### Metaadatok hozzáadása egy új crate-hez

Tegyük fel, hogy van egy crate-ed, amelyet publikálni szeretnél. A publikálás
előtt hozzá kell adnod néhány metaadatot a crate _Cargo.toml_ fájljának
`[package]` szakaszához.

A crate-ednek egyedi névre lesz szüksége. Amíg helyben dolgozol egy crate-en,
bárhogyan elnevezheted. A [crates.io](https://crates.io/)<!-- ignore --> oldalon
azonban a crate-neveket az érkezési sorrend elve alapján osztják ki. Ha egy
crate-nevet már lefoglaltak, senki más nem publikálhat crate-et azzal a névvel.
Mielőtt megpróbálnál publikálni egy crate-et, keress rá a használni kívánt
névre. Ha a nevet már használják, másik nevet kell találnod, és a _Cargo.toml_
fájl `[package]` szakaszában a `name` mezőt az új névre kell szerkesztened a
publikáláshoz, így:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Még ha egyedi nevet választottál is, amikor ezen a ponton lefuttatod a `cargo
publish` parancsot a crate publikálásához, előbb egy figyelmeztetést, majd egy
hibát kapsz:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

Ez azért eredményez hibát, mert hiányzik néhány létfontosságú információ: leírás
és licenc szükséges ahhoz, hogy az emberek tudják, mit csinál a crate-ed, és
milyen feltételek mellett használhatják. A _Cargo.toml_ fájlban adj hozzá egy
mindössze egy-két mondatos leírást, mert ez a crate-eddel együtt fog megjelenni
a keresési találatok között. A `license` mezőhöz meg kell adnod egy
_licencazonosító-értéket_. A
[Linux Foundation Software Package Data Exchange (SPDX)][spdx] felsorolja
azokat az azonosítókat, amelyeket ehhez az értékhez használhatsz. Ha például
azt szeretnéd megadni, hogy a crate-edet az MIT-licenc alatt licenceled, add
hozzá az `MIT` azonosítót:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Ha olyan licencet szeretnél használni, amely nem szerepel az SPDX-ben, akkor az
adott licenc szövegét egy fájlba kell tenned, a fájlt bele kell foglalnod a
projektedbe, majd a `license` kulcs helyett a `license-file` kulccsal kell
megadnod annak a fájlnak a nevét.

Az arról szóló útmutatás, hogy melyik licenc megfelelő a projektedhez,
túlmutat e könyv keretein. A Rust-közösségben sokan ugyanúgy licencelik a
projektjeiket, mint magát a Rustot: az `MIT OR Apache-2.0` kettős licenccel. Ez
a gyakorlat egyben azt is bemutatja, hogy több, `OR` jellel elválasztott
licencazonosítót is megadhatsz, hogy a projektednek több licence legyen.

Egy egyedi névvel, a verzióval, a leírásoddal és a hozzáadott licenccel a
publikálásra kész projekt _Cargo.toml_ fájlja így nézhet ki:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[A Cargo dokumentációja](https://doc.rust-lang.org/cargo/) további metaadatokat
ír le, amelyeket megadhatsz, hogy mások könnyebben felfedezhessék és
használhassák a crate-edet.

### Publikálás a Crates.io-ra

Most, hogy létrehoztál egy fiókot, elmentetted az API-tokenedet, nevet
választottál a crate-ednek, és megadtad a szükséges metaadatokat, készen állsz
a publikálásra! Egy crate publikálásakor egy adott verzió töltődik fel a
[crates.io](https://crates.io/)<!-- ignore --> oldalra, hogy mások
használhassák.

Légy óvatos, mert a publikálás _végleges_. A verziót soha nem lehet felülírni,
és a kódot bizonyos körülményeket leszámítva nem lehet törölni. A Crates.io
egyik fő célja az, hogy a kód állandó archívumaként szolgáljon, hogy a
[crates.io](https://crates.io/)<!-- ignore --> crate-jeitől függő összes
projekt buildjei továbbra is működjenek. A verziók törlésének engedélyezése
lehetetlenné tenné e cél teljesítését. Nincs azonban korlátozva, hány
crate-verziót publikálhatsz.

Futtasd le újra a `cargo publish` parancsot. Most már sikerrel kell járnia:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

Gratulálunk! Most már megosztottad a kódodat a Rust-közösséggel, és bárki
könnyen felveheti a crate-edet a projektje függőségei közé.

### Egy meglévő crate új verziójának publikálása

Amikor módosítottad a crate-edet, és készen állsz egy új verzió kiadására,
megváltoztatod a _Cargo.toml_ fájlodban megadott `version` értéket, és újra
publikálsz. A [szemantikus verziózás szabályai][semver] alapján döntsd el, mi a
megfelelő következő verziószám az általad elvégzett változtatások fajtájától
függően. Ezután futtasd a `cargo publish` parancsot az új verzió feltöltéséhez.

<!-- Old headings. Do not remove or links may break. -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>
<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### Verziók elavulttá nyilvánítása a Crates.io-n

Bár egy crate korábbi verzióit nem távolíthatod el, megakadályozhatod, hogy
bármilyen jövőbeli projekt új függőségként vegye fel őket. Ez akkor hasznos, ha
egy crate-verzió valamilyen okból hibás. Ilyen helyzetekre a Cargo támogatja
egy crate-verzió visszahúzását (yank).

Egy verzió _visszahúzása_ (yank) megakadályozza, hogy új projektek attól a
verziótól függjenek, miközben minden olyan meglévő projekt, amely tőle függ,
tovább működhet. Lényegében a yank azt jelenti, hogy egyetlen _Cargo.lock_
fájllal rendelkező projekt sem törik el, és a jövőben generált _Cargo.lock_
fájlok egyike sem fogja használni a visszahúzott verziót.

Egy crate-verzió visszahúzásához a korábban publikált crate könyvtárában
futtasd a `cargo yank` parancsot, és add meg, melyik verziót szeretnéd
visszahúzni. Ha például publikáltunk egy `guessing_game` nevű crate-et 1.0.1
verzióval, és vissza akarjuk húzni, akkor a `guessing_game` projektkönyvtárában
a következőt futtatnánk:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

Ha a parancshoz hozzáadod az `--undo` kapcsolót, vissza is vonhatsz egy
visszahúzást, és megengedheted, hogy a projektek újra függjenek egy verziótól:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

A yank _nem_ töröl semmilyen kódot. Nem tud például véletlenül feltöltött
titkokat törölni. Ha ez megtörténik, azonnal újra kell állítanod azokat a
titkokat.

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/
