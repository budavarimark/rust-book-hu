<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Hatókör és láthatóság szabályozása modulokkal

Ebben a szakaszban a modulokról és a modulrendszer további részeiről lesz szó,
nevezetesen az _útvonalakról_, amelyekkel elemeket nevezhetsz meg; a `use`
kulcsszóról, amely egy útvonalat behoz a hatókörbe; valamint a `pub`
kulcsszóról, amellyel nyilvánossá tehetsz elemeket. Szó lesz még az `as`
kulcsszóról, a külső csomagokról és a glob operátorról.

### Modulok – gyorstalpaló

Mielőtt belemennénk a modulok és az útvonalak részleteibe, itt adunk egy gyors
összefoglalót arról, hogyan működnek a modulok, az útvonalak, a `use` és a
`pub` kulcsszó a fordítóban, és hogy a fejlesztők többsége hogyan szervezi a
kódját. Mindegyik szabályra hozunk példákat a fejezet során, de ez a rész
kiválóan használható emlékeztetőként arról, hogyan működnek a modulok.

- **Indulj a crate rootból**: Egy crate fordításakor a fordító először a crate
  root fájlban (ez általában library crate esetén az _src/lib.rs_, binary crate
  esetén az _src/main.rs_) keresi a lefordítandó kódot.
- **Modulok deklarálása**: A crate root fájlban új modulokat deklarálhatsz;
  tegyük fel, hogy a `mod garden;` sorral deklarálsz egy „garden” modult. A
  fordító a következő helyeken keresi a modul kódját:
  - Beágyazva, azokban a kapcsos zárójelekben, amelyek a `mod garden` utáni
    pontosvesszőt helyettesítik
  - Az _src/garden.rs_ fájlban
  - Az _src/garden/mod.rs_ fájlban
- **Almodulok deklarálása**: A crate rooton kívüli bármelyik fájlban
  deklarálhatsz almodulokat. Például az _src/garden.rs_ fájlban deklarálhatod a
  `mod vegetables;` sort. A fordító a szülőmodulról elnevezett könyvtáron belül
  a következő helyeken keresi az almodul kódját:
  - Beágyazva, közvetlenül a `mod vegetables` után, pontosvessző helyett
    kapcsos zárójelek között
  - Az _src/garden/vegetables.rs_ fájlban
  - Az _src/garden/vegetables/mod.rs_ fájlban
- **Modulokban lévő kód útvonalai**: Amint egy modul a crate-ed része lett, a
  benne lévő kódra ugyanazon a crate-en belül bárhonnan hivatkozhatsz a kódhoz
  vezető útvonallal, amennyiben a láthatósági szabályok ezt megengedik. Például
  a garden vegetables modulban lévő `Asparagus` típus a
  `crate::garden::vegetables::Asparagus` útvonalon található meg.
- **Privát kontra nyilvános**: A modulon belüli kód alapértelmezés szerint
  privát a szülőmoduljaihoz képest. Ha nyilvánossá akarsz tenni egy modult, a
  `mod` helyett a `pub mod` szerkezettel deklaráld. Ha egy nyilvános modulon
  belüli elemeket is nyilvánossá akarod tenni, írj `pub` kulcsszót a
  deklarációik elé.
- **A `use` kulcsszó**: Egy hatókörön belül a `use` kulcsszó rövidítéseket hoz
  létre elemekhez, hogy csökkentse a hosszú útvonalak ismétlődését. Bármelyik
  olyan hatókörben, amely hivatkozhat a
  `crate::garden::vegetables::Asparagus` útvonalra, létrehozhatsz egy
  rövidítést a `use crate::garden::vegetables::Asparagus;` sorral, és onnantól
  kezdve elég csak `Asparagus`-t írnod, ha az adott hatókörben használni
  szeretnéd ezt a típust.

Itt létrehozunk egy `backyard` nevű binary crate-et, amely szemlélteti ezeket a
szabályokat. A crate könyvtára, amelynek szintén _backyard_ a neve, a következő
fájlokat és könyvtárakat tartalmazza:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

A crate root fájl ebben az esetben az _src/main.rs_, és a következőt
tartalmazza:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

A `pub mod garden;` sor azt mondja a fordítónak, hogy vegye bele azt a kódot,
amelyet az _src/garden.rs_ fájlban talál, ez pedig a következő:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Itt a `pub mod vegetables;` azt jelenti, hogy az _src/garden/vegetables.rs_
fájlban lévő kód is bekerül. Ez a kód a következő:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Most pedig nézzük meg ezeknek a szabályoknak a részleteit, és lássuk őket
működés közben!

### Összetartozó kód csoportosítása modulokban

A _modulok_ lehetővé teszik, hogy a crate-en belül úgy szervezzük a kódot, hogy
az olvasható és könnyen újrafelhasználható legyen. A modulokkal az elemek
_láthatóságát_ is szabályozhatjuk, mert a modulon belüli kód alapértelmezés
szerint privát. A privát elemek olyan belső implementációs részletek, amelyek
kívülről nem használhatók. Dönthetünk úgy, hogy nyilvánossá tesszük a modulokat
és a bennük lévő elemeket, amivel közzétesszük őket, hogy külső kód is
használhassa őket, és függhessen tőlük.

Példaként írjunk egy library crate-et, amely egy étterem működését valósítja
meg. A függvények szignatúráit definiáljuk, de a törzsüket üresen hagyjuk, hogy
a kód szervezésére koncentrálhassunk az étterem tényleges implementációja
helyett.

Az éttermi szakmában az étterem egyes részeit „front of house”-nak, másokat
„back of house”-nak neveznek. A _front of house_ (vendégtér) az, ahol a
vendégek vannak; ide tartozik, ahol a hostessek leültetik a vendégeket, ahol a
felszolgálók felveszik a rendelést és a fizetést intézik, és ahol a pultosok
elkészítik az italokat. A _back of house_ (hátsó rész) az, ahol a séfek és a
szakácsok dolgoznak a konyhában, ahol a mosogatók takarítanak, és ahol a
vezetők az adminisztratív munkát végzik.

Ahhoz, hogy így strukturáljuk a crate-ünket, egymásba ágyazott modulokba
szervezhetjük a függvényeit. Hozz létre egy `restaurant` nevű új könyvtárat a
`cargo new restaurant --lib` parancs futtatásával. Ezután írd be a 7-1. lista
kódját az _src/lib.rs_ fájlba, hogy definiálj néhány modult és
függvényszignatúrát; ez a kód a front of house rész.

<Listing number="7-1" file-name="src/lib.rs" caption="Egy `front_of_house` modul, amely további modulokat tartalmaz, azok pedig függvényeket">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Egy modult a `mod` kulcsszóval definiálunk, amelyet a modul neve követ (ebben
az esetben `front_of_house`). A modul törzse ezután kapcsos zárójelek közé
kerül. A modulokba további modulokat helyezhetünk, ahogy ebben az esetben a
`hosting` és a `serving` modult. A modulok más elemek definícióit is
tartalmazhatják, például struct-okét, enumokét, konstansokét, trait-ekét, és
ahogy a 7-1. listában, függvényekét.

A modulok használatával az összetartozó definíciókat egy csoportba foghatjuk,
és megnevezhetjük, miért tartoznak össze. Az ezt a kódot használó programozók a
csoportok alapján tájékozódhatnak a kódban ahelyett, hogy az összes definíciót
végig kellene olvasniuk, így könnyebben megtalálják a számukra fontos
definíciókat. Azok a programozók, akik új funkcionalitást adnak ehhez a kódhoz,
tudni fogják, hová tegyék a kódot, hogy a program szervezett maradjon.

Korábban említettük, hogy az _src/main.rs_ és az _src/lib.rs_ neve _crate
root_. Az elnevezés oka az, hogy e két fájl bármelyikének a tartalma egy
`crate` nevű modult alkot a crate modulszerkezetének gyökerében; ezt a
szerkezetet _modulfának_ nevezzük.

A 7-2. lista a 7-1. listában lévő szerkezet modulfáját mutatja.

<Listing number="7-2" caption="A 7-1. lista kódjának modulfája">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Ez a fa megmutatja, hogyan ágyazódnak egyes modulok más modulokba; például a
`hosting` a `front_of_house` modulba ágyazódik. A fából az is látszik, hogy egyes
modulok _testvérek_, vagyis ugyanabban a modulban vannak definiálva; a
`hosting` és a `serving` testvérek, amelyeket a `front_of_house` modulon belül
definiáltunk. Ha az A modul a B modulon belül van, azt mondjuk, hogy az A modul
a B modul _gyereke_, a B modul pedig az A modul _szülője_. Vedd észre, hogy az
egész modulfa a `crate` nevű implicit modul alatt gyökerezik.

A modulfa a számítógépeden lévő fájlrendszer könyvtárfájára emlékeztethet; ez
nagyon találó összehasonlítás! Ahogyan a fájlrendszerben a könyvtárakat, úgy
használod a modulokat a kódod szervezésére. És ahogyan a könyvtárban lévő
fájlokat, úgy a moduljainkat is meg kell tudnunk találni valahogyan.
