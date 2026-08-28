## Makrók {#macros}

A könyv során végig használtunk makrókat, például a `println!`-t, de még nem
jártuk körül teljesen, mi is az a makró, és hogyan működik. A _makró_ kifejezés
a Rust képességeinek egy egész családjára utal: a `macro_rules!` segítségével
írt deklaratív makrókra és a procedurális makrók három fajtájára:

- Egyedi `#[derive]` makrók, amelyek megadják a structokon és enumokon
  használt `derive` attribútummal hozzáadott kódot
- Attribútumszerű makrók, amelyek bármely elemen használható egyedi
  attribútumokat definiálnak
- Függvényszerű makrók, amelyek függvényhívásnak látszanak, de az
  argumentumukként megadott tokeneken dolgoznak

Ezek mindegyikéről sorra beszélünk, de előbb nézzük meg, minek is kellenek
egyáltalán makrók, ha már vannak függvényeink.

### A makrók és a függvények közötti különbség

A makrók alapvetően olyan kódírási módot jelentenek, amelyben a kód másik kódot
ír; ezt _metaprogramozásnak_ nevezzük. A C függelékben a `derive` attribútumról
lesz szó, amely különféle trait-ek implementációját generálja neked.
Használtuk emellett a könyv során a `println!` és a `vec!` makrót is. Ezek a
makrók mind _kifejtődnek_, és több kódot állítanak elő, mint amennyit kézzel
írtál.

A metaprogramozás azért hasznos, mert csökkenti a megírandó és karbantartandó
kód mennyiségét — ez a függvények egyik szerepe is. A makróknak azonban van
néhány további képességük, amellyel a függvények nem rendelkeznek.

Egy függvényszignatúrának deklarálnia kell, hány és milyen típusú paramétere
van a függvénynek. A makrók ezzel szemben változó számú paramétert fogadhatnak:
meghívhatjuk a `println!("hello")`-t egyetlen argumentummal, vagy a
`println!("hello {}", name)`-et kettővel. Ráadásul a makrók még azelőtt
kifejtődnek, hogy a fordító értelmezné a kód jelentését, így egy makró például
implementálhat egy trait-et egy adott típusra. Egy függvény ezt nem teheti meg,
mert futásidőben hívódik meg, a trait-eket viszont fordítási időben kell
implementálni.

A makró — függvény helyett történő — implementálásának hátránya, hogy a
makródefiníciók összetettebbek a függvénydefinícióknál, hiszen olyan Rust-kódot
írsz, amely Rust-kódot ír. E közvetettség miatt a makródefiníciókat általában
nehezebb olvasni, megérteni és karbantartani, mint a függvénydefiníciókat.

A makrók és a függvények közötti másik fontos különbség, hogy a makrókat egy
fájlban _azelőtt_ kell definiálnod vagy hatókörbe hoznod, hogy meghívnád őket,
míg a függvényeket bárhol definiálhatod és bárhol meghívhatod.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Deklaratív makrók az általános metaprogramozáshoz

A Rustban a makrók legelterjedtebb formája a _deklaratív makró_. Ezeket néha
„példa alapú makróknak” (macros by example), „`macro_rules!` makróknak” vagy
egyszerűen csak „makróknak” nevezik. A deklaratív makrók lényegében azt teszik
lehetővé, hogy a Rust `match` kifejezéseihez hasonló dolgot írj. Ahogy a 6.
fejezetben szó volt róla, a `match` kifejezések olyan vezérlési szerkezetek,
amelyek fogadnak egy kifejezést, összehasonlítják a kifejezés eredményül kapott
értékét mintákkal, majd lefuttatják az illeszkedő mintához tartozó kódot. A
makrók szintén egy értéket hasonlítanak össze bizonyos kódhoz tartozó mintákkal:
ebben az esetben az érték a makrónak átadott, szó szerinti Rust forráskód; a
mintákat ennek a forráskódnak a szerkezetével vetik össze; az egyes mintákhoz
tartozó kód pedig illeszkedés esetén a makrónak átadott kód helyébe lép. Mindez
a fordítás során történik.

Makró definiálásához a `macro_rules!` szerkezetet használod. Nézzük meg a
`macro_rules!` használatát azon keresztül, hogyan van definiálva a `vec!`
makró. A 8. fejezet foglalkozott azzal, hogyan hozhatunk létre a `vec!`
makróval új vektort adott értékekkel. Például az alábbi makró egy három egész
számot tartalmazó új vektort hoz létre:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Használhatnánk a `vec!` makrót két egész számból álló vektor vagy öt string
slice-ból álló vektor létrehozására is. Függvénnyel ugyanezt nem tudnánk
megtenni, mert előre nem ismernénk az értékek számát és típusát.

A 20-35. lista a `vec!` makró definíciójának kissé egyszerűsített változatát
mutatja.

<Listing number="20-35" file-name="src/lib.rs" caption="A `vec!` makró definíciójának egyszerűsített változata">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Megjegyzés: a `vec!` makró tényleges definíciója a standard könyvtárban olyan
> kódot is tartalmaz, amely előre lefoglalja a megfelelő mennyiségű memóriát. Ez
> a kód egy optimalizáció, amelyet itt nem szerepeltetünk, hogy a példa
> egyszerűbb legyen.

A `#[macro_export]` annotáció azt jelzi, hogy ennek a makrónak elérhetőnek kell
lennie, valahányszor az őt definiáló crate-et hatókörbe hozzák. Enélkül az
annotáció nélkül a makrót nem lehet hatókörbe hozni.

Ezután a makródefiníciót a `macro_rules!`-lal és a definiálandó makró nevével
kezdjük, felkiáltójel _nélkül_. A nevet — ez esetben a `vec`-et — kapcsos
zárójelek követik, amelyek a makródefiníció törzsét jelölik.

A `vec!` törzsében lévő szerkezet a `match` kifejezés szerkezetéhez hasonlít.
Egyetlen águnk van, a `( $( $x:expr ),* )` mintával, amelyet a `=>` és az ehhez
a mintához tartozó kódblokk követ. Ha a minta illeszkedik, a hozzá tartozó
kódblokk kerül kibocsátásra. Mivel ez az egyetlen minta ebben a makróban, csak
egyféleképpen lehet illeszkedni; bármilyen más minta hibát eredményez. Az
összetettebb makróknak több águk is lesz.

A makródefiníciókban érvényes mintaszintaxis eltér a 19. fejezetben tárgyalt
mintaszintaxistól, mert a makróknál a mintákat nem értékekkel, hanem a
Rust-kód szerkezetével vetjük össze. Nézzük végig, mit jelentenek a minta egyes
darabjai a 20-29. listában; a teljes makró-mintaszintaxist a [Rust
referenciában][ref] találod.

Először is egy zárójelpárral fogjuk körül az egész mintát. Dollárjellel (`$`)
deklarálunk a makrórendszerben egy változót, amely a mintára illeszkedő
Rust-kódot fogja tartalmazni. A dollárjel egyértelművé teszi, hogy ez
makróváltozó, nem közönséges Rust-változó. Ezután következik egy újabb
zárójelpár, amely a benne lévő mintára illeszkedő értékeket fogja be a
helyettesítő kódban való felhasználásra. A `$()` belsejében a `$x:expr` áll,
amely bármely Rust-kifejezésre illeszkedik, és a `$x` nevet adja a
kifejezésnek.

A `$()`-t követő vessző azt jelzi, hogy a `$()`-ben lévő kódra illeszkedő
kódrészletek egyes példányai között szó szerinti vessző elválasztókaraktert
kell írni. A `*` azt adja meg, hogy a minta nullaszor vagy többször illeszkedik
arra, ami a `*` előtt áll.

Amikor ezt a makrót a `vec![1, 2, 3];` alakban hívjuk meg, a `$x` minta
háromszor illeszkedik, az `1`, a `2` és a `3` kifejezésekre.

Most nézzük az ehhez az ághoz tartozó kód törzsében lévő mintát: a `$()*`-on
belüli `temp_vec.push()` minden olyan részhez legenerálódik, amely a mintában
lévő `$()`-re illeszkedik, nullaszor vagy többször, attól függően, hányszor
illeszkedik a minta. A `$x` helyére minden illeszkedő kifejezés bekerül. Amikor
ezt a makrót a `vec![1, 2, 3];` alakban hívjuk meg, a makróhívás helyébe lépő
generált kód a következő lesz:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Olyan makrót definiáltunk, amely tetszőleges számú, tetszőleges típusú
argumentumot fogadhat, és olyan kódot tud generálni, amely a megadott elemeket
tartalmazó vektort hoz létre.

Ha többet szeretnél megtudni a makróírásról, olvasd el az online
dokumentációt vagy más forrásokat, például a Daniel Keep által elindított és
Lukas Wirth által folytatott [„The Little Book of Rust Macros”][tlborm] című
könyvet.

### Procedurális makrók kódgenerálásra attribútumokból

A makrók második formája a procedurális makró, amely inkább függvényként
viselkedik (és egyfajta eljárás). A _procedurális makrók_ valamilyen kódot
kapnak bemenetként, műveleteket végeznek rajta, és kódot állítanak elő
kimenetként — ahelyett, hogy mintákra illesztenének, és a kódot másik kóddal
helyettesítenék, ahogy a deklaratív makrók teszik. A procedurális makrók három
fajtája az egyedi `derive`, az attribútumszerű és a függvényszerű makró, és
mindegyik hasonlóan működik.

Procedurális makrók készítésekor a definícióknak saját, speciális crate-típusú
crate-ben kell lenniük. Ennek bonyolult technikai okai vannak, amelyeket
reményeink szerint a jövőben meg tudunk szüntetni. A 20-36. listában
megmutatjuk, hogyan definiálhatunk procedurális makrót; a `some_attribute` egy
konkrét makrófajta használatának helyőrzője.

<Listing number="20-36" file-name="src/lib.rs" caption="Példa procedurális makró definiálására">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

A procedurális makrót definiáló függvény bemenetként egy `TokenStream`-et kap,
és kimenetként `TokenStream`-et állít elő. A `TokenStream` típust a Rusttal
együtt szállított `proc_macro` crate definiálja, és tokenek sorozatát
reprezentálja. Ez a makró lényege: az a forráskód, amellyel a makró dolgozik,
alkotja a bemeneti `TokenStream`-et, a makró által előállított kód pedig a
kimeneti `TokenStream`. A függvényhez emellett egy attribútum is tartozik,
amely megadja, milyen fajta procedurális makrót készítünk. Ugyanabban a
crate-ben többféle procedurális makrónk is lehet.

Nézzük meg a procedurális makrók különböző fajtáit. Egy egyedi `derive`
makróval kezdjük, majd elmagyarázzuk azokat az apró eltéréseket, amelyek a
többi formát megkülönböztetik.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Egyedi `derive` makrók {#custom-derive-macros}

Hozzunk létre egy `hello_macro` nevű crate-et, amely definiál egy `HelloMacro`
nevű trait-et egyetlen, `hello_macro` nevű asszociált függvénnyel. Ahelyett,
hogy a felhasználóinkkal implementáltatnánk a `HelloMacro` trait-et minden
egyes típusukra, biztosítunk egy procedurális makrót, hogy a felhasználók a
`#[derive(HelloMacro)]` annotációval ellássák a típusukat, és így megkapják a
`hello_macro` függvény alapértelmezett implementációját. Az alapértelmezett
implementáció a `Hello, Macro! My name is TypeName!` szöveget írja ki, ahol a
`TypeName` annak a típusnak a neve, amelyre ezt a trait-et definiálták. Más
szóval olyan crate-et írunk, amely lehetővé teszi, hogy egy másik programozó a
crate-ünket használva a 20-37. listához hasonló kódot írjon.

<Listing number="20-37" file-name="src/main.rs" caption="A kód, amelyet a crate-ünk felhasználója írhat majd a procedurális makrónkkal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Ez a kód a `Hello, Macro! My name is Pancakes!` szöveget fogja kiírni, ha
elkészültünk. Az első lépés egy új library crate létrehozása, így:

```console
$ cargo new hello_macro --lib
```

Ezután a 20-38. listában definiáljuk a `HelloMacro` trait-et és az asszociált
függvényét.

<Listing file-name="src/lib.rs" number="20-38" caption="Egyszerű trait, amelyet a `derive` makróval fogunk használni">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Megvan a trait és a függvénye. Ezen a ponton a crate-ünk felhasználója
implementálhatná a trait-et a kívánt működés eléréséhez, ahogy a 20-39.
listában látható.

<Listing number="20-39" file-name="src/main.rs" caption="Így nézne ki, ha a felhasználók kézzel implementálnák a `HelloMacro` trait-et">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Ehhez azonban minden olyan típushoz meg kellene írniuk az implementációs
blokkot, amelyet a `hello_macro`-val akarnak használni; mi szeretnénk
megkímélni őket ettől a munkától.

Ráadásul egyelőre nem tudjuk a `hello_macro` függvényt olyan alapértelmezett
implementációval ellátni, amely kiírja annak a típusnak a nevét, amelyre a
trait implementálva van: a Rustban nincs reflexió, így futásidőben nem tudja
megnézni a típus nevét. Makróra van szükségünk, amely fordítási időben generál
kódot.

A következő lépés a procedurális makró definiálása. Jelen sorok írásakor a
procedurális makróknak saját crate-ben kell lenniük. Ez a megkötés idővel
talán megszűnik. A crate-ek és a makró-crate-ek elnevezésének konvenciója a
következő: egy `foo` nevű crate-hez az egyedi `derive` procedurális makró
crate neve `foo_derive`. Hozzunk létre egy `hello_macro_derive` nevű új
crate-et a `hello_macro` projektünkön belül:

```console
$ cargo new hello_macro_derive --lib
```

A két crate-ünk szorosan összefügg, ezért a procedurális makró crate-jét a
`hello_macro` crate könyvtárán belül hozzuk létre. Ha megváltoztatjuk a
trait-definíciót a `hello_macro`-ban, a `hello_macro_derive` procedurális
makrójának implementációját is módosítanunk kell. A két crate-et külön kell
majd publikálni, és az ezeket használó programozóknak mindkettőt fel kell
venniük függőségként, és mindkettőt hatókörbe kell hozniuk. Megtehetnénk azt
is, hogy a `hello_macro` crate függőségként használja a `hello_macro_derive`-t,
és újraexportálja a procedurális makró kódját. A projekt általunk választott
felépítése viszont lehetővé teszi, hogy a programozók akkor is használhassák a
`hello_macro`-t, ha nem kérnek a `derive` funkcionalitásból.

Deklarálnunk kell, hogy a `hello_macro_derive` crate procedurális makró crate.
Szükségünk lesz emellett a `syn` és a `quote` crate képességeire is, ahogy azt
mindjárt látni fogod, ezért ezeket fel kell vennünk függőségként. Add hozzá a
következőt a `hello_macro_derive` _Cargo.toml_ fájljához:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

A procedurális makró definiálásának megkezdéséhez másold a 20-40. lista kódját
a `hello_macro_derive` crate _src/lib.rs_ fájljába. Vedd figyelembe, hogy ez a
kód addig nem fordul le, amíg meg nem adjuk az `impl_hello_macro` függvény
definícióját.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Kód, amelyre a legtöbb procedurális makró crate-nek szüksége lesz a Rust-kód feldolgozásához">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Vedd észre, hogy két részre osztottuk a kódot: a `hello_macro_derive`
függvényre, amely a `TokenStream` értelmezéséért felel, és az
`impl_hello_macro` függvényre, amely a szintaxisfa átalakításáért — ez
kényelmesebbé teszi a procedurális makró írását. A külső függvényben (itt a
`hello_macro_derive`-ban) lévő kód szinte minden procedurális makró crate-ben
ugyanaz lesz, amelyet valaha látsz vagy készítesz. A belső függvény (itt az
`impl_hello_macro`) törzsében megadott kód viszont a procedurális makród
céljától függően más és más lesz.

Három új crate-et vezettünk be: a `proc_macro`-t, a [`syn`][syn]<!-- ignore -->
crate-et és a [`quote`][quote]<!-- ignore --> crate-et. A `proc_macro` crate a
Rusttal együtt érkezik, ezért nem kellett felvennünk a _Cargo.toml_
függőségei közé. A `proc_macro` crate a fordító API-ja, amely lehetővé teszi,
hogy a kódunkból olvassuk és manipuláljuk a Rust-kódot.

A `syn` crate egy sztringből álló Rust-kódot olyan adatszerkezetté alakít,
amelyen műveleteket végezhetünk. A `quote` crate a `syn` adatszerkezeteit
alakítja vissza Rust-kóddá. Ezek a crate-ek sokkal egyszerűbbé teszik bármilyen
kezelni kívánt Rust-kód értelmezését: a Rust-kódhoz teljes értékű elemzőt írni
nem kis feladat.

A `hello_macro_derive` függvény akkor hívódik meg, amikor a könyvtárunk egy
felhasználója `#[derive(HelloMacro)]`-t ír egy típusra. Ez azért lehetséges,
mert itt a `hello_macro_derive` függvényt a `proc_macro_derive` annotációval
láttuk el, és megadtuk a `HelloMacro` nevet, amely megegyezik a trait-ünk
nevével; ezt a konvenciót követi a legtöbb procedurális makró.

A `hello_macro_derive` függvény először átalakítja az `input`-ot
`TokenStream`-ből olyan adatszerkezetté, amelyet aztán értelmezhetünk, és
amelyen műveleteket végezhetünk. Itt lép színre a `syn`. A `syn` `parse`
függvénye egy `TokenStream`-et vesz át, és egy `DeriveInput` structot ad
vissza, amely az értelmezett Rust-kódot reprezentálja. A 20-41. lista annak a
`DeriveInput` structnak a lényeges részeit mutatja, amelyet a `struct
Pancakes;` sztring értelmezésekor kapunk.

<Listing number="20-41" caption="A `DeriveInput` példány, amelyet a 20-37. listában a makró attribútumával ellátott kód értelmezésekor kapunk">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Ennek a structnak a mezői azt mutatják, hogy az általunk értelmezett Rust-kód
egy unit struct, amelynek `ident`-je (_azonosítója_, vagyis a neve)
`Pancakes`. Ennek a structnak további mezői is vannak mindenféle Rust-kód
leírására; további információért nézd meg a [`syn` dokumentációját a
`DeriveInput`-ról][syn-docs].

Hamarosan definiáljuk az `impl_hello_macro` függvényt, amelyben felépítjük a
beilleszteni kívánt új Rust-kódot. Előtte azonban vedd észre, hogy a `derive`
makrónk kimenete is `TokenStream`. A visszaadott `TokenStream` hozzáadódik
ahhoz a kódhoz, amelyet a crate-ünk felhasználói írnak, így amikor lefordítják
a crate-jüket, megkapják azt az extra funkcionalitást, amelyet a módosított
`TokenStream`-ben biztosítunk.

Talán észrevetted, hogy `unwrap`-et hívunk, hogy a `hello_macro_derive`
függvény panicot váltson ki, ha a `syn::parse` függvény hívása itt meghiúsul. A
procedurális makrónknak azért kell hibák esetén panicot kiváltania, mert a
`proc_macro_derive` függvényeknek `Result` helyett `TokenStream`-et kell
visszaadniuk, hogy megfeleljenek a procedurális makrók API-jának. Ezt a példát
az `unwrap` használatával egyszerűsítettük le; éles kódban a `panic!` vagy az
`expect` használatával konkrétabb hibaüzeneteket kell adnod arról, mi ment
félre.

Most, hogy megvan a kód, amely az annotált Rust-kódot `TokenStream`-ből
`DeriveInput` példánnyá alakítja, generáljuk le azt a kódot, amely az annotált
típusra implementálja a `HelloMacro` trait-et, ahogy a 20-42. listában látható.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="A `HelloMacro` trait implementálása az értelmezett Rust-kód alapján">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Az `ast.ident` segítségével egy `Ident` struct példányt kapunk, amely az
annotált típus nevét (azonosítóját) tartalmazza. A 20-41. listában lévő struct
mutatja, hogy amikor az `impl_hello_macro` függvényt a 20-37. lista kódján
futtatjuk, a kapott `ident` `ident` mezőjének értéke `"Pancakes"` lesz. Így a
20-42. listában a `name` változó olyan `Ident` struct példányt fog
tartalmazni, amely kiírva a `"Pancakes"` sztring lesz — a 20-37. listában
szereplő struct neve.

A `quote!` makró lehetővé teszi, hogy megadjuk a visszaadni kívánt Rust-kódot.
A fordító nem pontosan azt várja, ami a `quote!` makró futtatásának közvetlen
eredménye, ezért `TokenStream`-mé kell alakítanunk. Ezt az `into` metódus
hívásával tesszük meg, amely felemészti ezt a köztes reprezentációt, és a
megkövetelt `TokenStream` típusú értéket adja vissza.

A `quote!` makró néhány nagyon menő sablonozási lehetőséget is biztosít:
beírhatjuk, hogy `#name`, és a `quote!` behelyettesíti a `name` változóban lévő
értéket. Még ismétlést is végezhetsz vele, hasonlóan ahhoz, ahogyan a
közönséges makrók működnek. Alapos bevezetésért nézd meg [a `quote` crate
dokumentációját][quote-docs].

Azt szeretnénk, hogy a procedurális makrónk generálja le a `HelloMacro`
trait-ünk implementációját arra a típusra, amelyet a felhasználó annotált; ezt
a `#name`-mel érhetjük el. A trait-implementációban egyetlen függvény van, a
`hello_macro`, amelynek törzse tartalmazza a biztosítani kívánt működést: a
`Hello, Macro! My name is` szöveg, majd az annotált típus nevének kiírását.

Az itt használt `stringify!` makró a Rust beépített makrója. Egy Rust
kifejezést vesz át, például az `1 + 2`-t, és fordítási időben sztringliterállá
alakítja, például `"1 + 2"`-vé. Ez különbözik a `format!`-tól és a
`println!`-től, amelyek kiértékelik a kifejezést, majd az eredményt `String`-gé
alakítják. Elképzelhető, hogy a `#name` bemenet olyan kifejezés, amelyet szó
szerint kell kiírni, ezért használjuk a `stringify!`-t. A `stringify!`
használata ráadásul megspórol egy memóriafoglalást is azzal, hogy a `#name`-et
fordítási időben sztringliterállá alakítja.

Ezen a ponton a `cargo build`-nek sikeresen le kell futnia mind a
`hello_macro`, mind a `hello_macro_derive` esetében. Kössük össze ezeket a
crate-eket a 20-37. lista kódjával, hogy működés közben lássuk a procedurális
makrót! Hozz létre egy új binary projektet a _projects_ könyvtáradban a
`cargo new pancakes` paranccsal. Fel kell vennünk a `hello_macro`-t és a
`hello_macro_derive`-t függőségként a `pancakes` crate _Cargo.toml_ fájljába.
Ha a `hello_macro` és a `hello_macro_derive` saját verzióidat publikálod a
[crates.io](https://crates.io/)<!-- ignore --> oldalra, akkor közönséges
függőségek lennének; ha nem, `path` függőségként adhatod meg őket az alábbi
módon:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Másold a 20-37. lista kódját a _src/main.rs_ fájlba, és futtasd a `cargo run`
parancsot: a `Hello, Macro! My name is Pancakes!` szöveget kell kiírnia. A
`HelloMacro` trait implementációja a procedurális makróból került be anélkül,
hogy a `pancakes` crate-nek implementálnia kellett volna; a
`#[derive(HelloMacro)]` adta hozzá a trait-implementációt.

Ezután nézzük meg, miben különböznek a procedurális makrók többi fajtái az
egyedi `derive` makróktól.

### Attribútumszerű makrók

Az attribútumszerű makrók hasonlítanak az egyedi `derive` makrókra, de ahelyett,
hogy a `derive` attribútumhoz generálnának kódot, új attribútumok
létrehozását teszik lehetővé. Rugalmasabbak is: a `derive` csak structoknál és
enumoknál működik, az attribútumok viszont más elemekre, például függvényekre
is alkalmazhatók. Íme egy példa attribútumszerű makró használatára. Tegyük fel,
hogy van egy `route` nevű attribútumod, amely egy webalkalmazás-keretrendszer
használatakor függvényeket annotál:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Ezt a `#[route]` attribútumot a keretrendszer definiálná procedurális
makróként. A makródefiníciós függvény szignatúrája így nézne ki:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Itt két `TokenStream` típusú paraméterünk van. Az első az attribútum
tartalmáért felel: ez a `GET, "/"` rész. A második annak az elemnek a törzse,
amelyhez az attribútum tartozik: ebben az esetben az `fn index() {}` és a
függvény törzsének többi része.

Ezen túl az attribútumszerű makrók ugyanúgy működnek, mint az egyedi `derive`
makrók: létrehozol egy `proc-macro` crate-típusú crate-et, és implementálsz egy
függvényt, amely legenerálja a kívánt kódot!

### Függvényszerű makrók

A függvényszerű makrók olyan makrókat definiálnak, amelyek függvényhívásnak
látszanak. A `macro_rules!` makrókhoz hasonlóan rugalmasabbak a függvényeknél;
például előre nem ismert számú argumentumot fogadhatnak. A `macro_rules!`
makrókat viszont csak a korábbi [„Deklaratív makrók az általános
metaprogramozáshoz”][decl]<!-- ignore --> című szakaszban tárgyalt,
`match`-szerű szintaxissal lehet definiálni. A függvényszerű makrók egy
`TokenStream` paramétert kapnak, és a definíciójuk Rust-kóddal manipulálja ezt
a `TokenStream`-et, ahogy a procedurális makrók másik két fajtája is teszi.
Függvényszerű makróra példa egy `sql!` makró, amelyet így lehetne meghívni:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Ez a makró értelmezné a benne lévő SQL-utasítást, és ellenőrizné, hogy
szintaktikailag helyes-e; ez sokkal összetettebb feldolgozás annál, mint amire
egy `macro_rules!` makró képes. Az `sql!` makrót így definiálnánk:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Ez a definíció hasonlít az egyedi `derive` makró szignatúrájára: megkapjuk a
zárójelek között lévő tokeneket, és visszaadjuk azt a kódot, amelyet
generálni akartunk.

## Összefoglalás

Hűha! Most már van néhány olyan Rust-képesség az eszköztáradban, amelyet
valószínűleg nem fogsz gyakran használni, de tudni fogod, hogy nagyon
sajátos helyzetekben rendelkezésre állnak. Több összetett témát is bemutattunk,
hogy amikor hibaüzenetek javaslataiban vagy mások kódjában találkozol velük,
felismerd ezeket a fogalmakat és szintaktikai elemeket. Használd ezt a
fejezetet referenciaként, amely elvezet a megoldásokhoz.

Következőnek mindazt, amiről a könyv során szó volt, a gyakorlatba ültetjük, és
készítünk még egy projektet!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
