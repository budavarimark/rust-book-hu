<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Osztott viselkedés definiálása trait-ekkel

A _trait_ azt írja le, milyen funkcionalitással rendelkezik egy adott típus, és
mit oszthat meg más típusokkal. A trait-ek segítségével absztrakt módon
definiálhatunk osztott viselkedést. A _trait bound_-okkal pedig megadhatjuk,
hogy egy generikus típus bármilyen olyan típus lehet, amely egy bizonyos
viselkedéssel rendelkezik.

> Megjegyzés: A trait-ek hasonlítanak arra, amit más nyelvekben gyakran
> _interfésznek_ neveznek, bár akadnak eltérések.

### Trait definiálása

Egy típus viselkedését azok a metódusok alkotják, amelyeket meghívhatunk az
adott típuson. Különböző típusok akkor osztoznak ugyanazon a viselkedésen, ha
mindegyiken meghívhatjuk ugyanazokat a metódusokat. A trait-definíciók arra
valók, hogy metódus-szignatúrákat csoportosítsunk, és így definiáljuk azt a
viselkedéshalmazt, amely egy adott cél eléréséhez szükséges.

Tegyük fel például, hogy több struct-unk van, amelyek különféle fajtájú és
mennyiségű szöveget tárolnak: egy `NewsArticle` struct, amely egy adott helyen
készült hírt tárol, és egy `SocialPost`, amely legfeljebb 280 karaktert
tartalmazhat, valamint metaadatokat arról, hogy új bejegyzésről, egy másik
bejegyzés megosztásáról vagy egy bejegyzésre adott válaszról van-e szó.

Szeretnénk készíteni egy `aggregator` nevű médiaaggregátor library crate-et,
amely meg tudja jeleníteni a `NewsArticle` vagy `SocialPost` példányokban
esetleg tárolt adatok összefoglalóit. Ehhez minden típustól kérnünk kell egy
összefoglalót, mégpedig úgy, hogy meghívjuk a példányon a `summarize` metódust.
A 10-12. lista a publikus `Summary` trait definícióját mutatja, amely ezt a
viselkedést fejezi ki.

<Listing number="10-12" file-name="src/lib.rs" caption="Egy `Summary` trait, amely a `summarize` metódus által nyújtott viselkedésből áll">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Itt a `trait` kulcsszóval deklarálunk egy trait-et, majd megadjuk a trait
nevét, ami ebben az esetben `Summary`. A trait-et `pub`-ként is deklaráljuk,
hogy az ettől a crate-től függő crate-ek szintén használhassák, amint azt
néhány példában látni fogjuk. A kapcsos zárójelek között deklaráljuk azokat a
metódus-szignatúrákat, amelyek a trait-et implementáló típusok viselkedését
írják le; ez ebben az esetben az `fn summarize(&self) -> String`.

A metódus-szignatúra után nem kapcsos zárójelben adunk meg egy implementációt,
hanem pontosvesszőt teszünk. Minden típusnak, amely ezt a trait-et
implementálja, saját, egyedi viselkedést kell adnia a metódus törzsének. A
fordító kikényszeríti, hogy minden olyan típuson, amely rendelkezik a `Summary`
trait-tel, pontosan ezzel a szignatúrával legyen definiálva a `summarize`
metódus.

Egy trait törzsében több metódus is lehet: a metódus-szignatúrák soronként egy
darab szerepelnek, és minden sor pontosvesszővel zárul.

### Trait implementálása egy típuson {#implementing-a-trait-on-a-type}

Most, hogy definiáltuk a `Summary` trait metódusainak kívánt szignatúráit,
implementálhatjuk a trait-et a médiaaggregátorunk típusain. A 10-13. lista a
`Summary` trait implementációját mutatja a `NewsArticle` structon, amely a
címet, a szerzőt és a helyszínt használja a `summarize` visszatérési értékének
összeállításához. A `SocialPost` struct esetében a `summarize` metódust úgy
definiáljuk, hogy a felhasználónevet adja vissza, utána pedig a bejegyzés
teljes szövegét, feltételezve, hogy a bejegyzés tartalma már eleve 280
karakterre van korlátozva.

<Listing number="10-13" file-name="src/lib.rs" caption="A `Summary` trait implementálása a `NewsArticle` és a `SocialPost` típuson">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Egy trait implementálása egy típuson hasonlít a szokásos metódusok
implementálásához. A különbség az, hogy az `impl` után az implementálandó trait
nevét írjuk, majd a `for` kulcsszót használjuk, végül megadjuk annak a típusnak
a nevét, amelyre a trait-et implementálni akarjuk. Az `impl` blokkon belül
azokat a metódus-szignatúrákat írjuk le, amelyeket a trait-definíció megadott.
A szignatúrák után nem pontosvesszőt teszünk, hanem kapcsos zárójeleket, és a
metódus törzsét kitöltjük azzal a konkrét viselkedéssel, amelyet a trait
metódusaitól az adott típus esetében elvárunk.

Most, hogy a library implementálta a `Summary` trait-et a `NewsArticle` és a
`SocialPost` típuson, a crate felhasználói ugyanúgy hívhatják meg a trait
metódusait a `NewsArticle` és a `SocialPost` példányain, ahogyan a szokásos
metódusokat hívjuk. Az egyetlen különbség, hogy a felhasználónak a típusok
mellett magát a trait-et is be kell hoznia a hatókörbe. Íme egy példa arra,
hogyan használhatná egy binary crate az `aggregator` library crate-ünket:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Ez a kód a következőt írja ki: `1 new post: horse_ebooks: of course, as you
probably already know, people`.

Más crate-ek, amelyek az `aggregator` crate-től függenek, szintén behozhatják a
hatókörbe a `Summary` trait-et, hogy implementálják a `Summary`-t a saját
típusaikon. Egy fontos megkötés, hogy egy trait-et csak akkor implementálhatunk
egy típuson, ha vagy a trait, vagy a típus, vagy mindkettő lokális a
crate-ünkhöz. Például implementálhatunk standard könyvtárbeli trait-eket, mint
a `Display`, egy saját típuson, mint a `SocialPost`, az `aggregator` crate-ünk
funkcionalitásának részeként, mert a `SocialPost` típus lokális az `aggregator`
crate-ünkhöz. A `Summary` trait-et is implementálhatjuk a `Vec<T>` típuson az
`aggregator` crate-ünkben, mert a `Summary` trait lokális az `aggregator`
crate-ünkhöz.

Külső trait-eket viszont nem implementálhatunk külső típusokon. Például nem
implementálhatjuk a `Display` trait-et a `Vec<T>` típuson az `aggregator`
crate-ünkben, mert a `Display` és a `Vec<T>` egyaránt a standard könyvtárban
van definiálva, és egyik sem lokális az `aggregator` crate-ünkhöz. Ez a
megkötés a _koherencia_ nevű tulajdonság része, pontosabban az _orphan rule_
(árva szabály), amely onnan kapta a nevét, hogy a szülőtípus nincs jelen. Ez a
szabály biztosítja, hogy mások kódja ne törhesse el a tiédet, és fordítva. A
szabály nélkül két crate is implementálhatná ugyanazt a trait-et ugyanarra a
típusra, és a Rust nem tudná, melyik implementációt használja.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Alapértelmezett implementációk használata

Néha hasznos, ha egy trait néhány metódusának vagy az összesnek van
alapértelmezett viselkedése, ahelyett hogy minden típuson minden metódushoz
implementációt követelnénk meg. Ezután, amikor a trait-et egy adott típuson
implementáljuk, minden metódus alapértelmezett viselkedését megtarthatjuk vagy
felülírhatjuk.

A 10-14. listában a `Summary` trait `summarize` metódusához alapértelmezett
stringet adunk meg, ahelyett hogy csak a metódus-szignatúrát definiálnánk, mint
a 10-12. listában.

<Listing number="10-14" file-name="src/lib.rs" caption="Egy `Summary` trait definiálása a `summarize` metódus alapértelmezett implementációjával">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Ahhoz, hogy a `NewsArticle` példányainak összefoglalásához az alapértelmezett
implementációt használjuk, egy üres `impl` blokkot adunk meg így:
`impl Summary for NewsArticle {}`.

Bár már nem definiáljuk közvetlenül a `summarize` metódust a `NewsArticle`
típuson, adtunk egy alapértelmezett implementációt, és megadtuk, hogy a
`NewsArticle` implementálja a `Summary` trait-et. Ennek eredményeként továbbra
is meghívhatjuk a `summarize` metódust egy `NewsArticle` példányon, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Ez a kód a következőt írja ki: `New article available! (Read more...)`.

Az alapértelmezett implementáció létrehozása nem teszi szükségessé, hogy
bármit megváltoztassunk a `Summary` `SocialPost`-on való implementációján a
10-13. listában. Ennek az az oka, hogy egy alapértelmezett implementáció
felülírásának szintaxisa megegyezik annak a trait-metódusnak az implementálási
szintaxisával, amelynek nincs alapértelmezett implementációja.

Az alapértelmezett implementációk meghívhatják ugyanannak a trait-nek más
metódusait is, még akkor is, ha azoknak a metódusoknak nincs alapértelmezett
implementációjuk. Így egy trait sok hasznos funkcionalitást nyújthat, miközben
az implementálóktól csak egy kis részt követel meg. Definiálhatnánk például a
`Summary` trait-et úgy, hogy legyen egy `summarize_author` metódusa, amelynek
az implementációja kötelező, majd definiálhatnánk egy `summarize` metódust,
amelynek alapértelmezett implementációja meghívja a `summarize_author`
metódust:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

A `Summary` ezen változatának használatához csak a `summarize_author` metódust
kell definiálnunk, amikor a trait-et egy típuson implementáljuk:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Miután definiáltuk a `summarize_author` metódust, meghívhatjuk a `summarize`
metódust a `SocialPost` struct példányain, és a `summarize` alapértelmezett
implementációja meg fogja hívni a `summarize_author` általunk megadott
definícióját. Mivel implementáltuk a `summarize_author` metódust, a `Summary`
trait a `summarize` metódus viselkedését anélkül adta meg nekünk, hogy több
kódot kellett volna írnunk. Így néz ki mindez:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Ez a kód a következőt írja ki:
`1 new post: (Read more from @horse_ebooks...)`.

Fontos megjegyezni, hogy ugyanannak a metódusnak a felülíró implementációjából
nem lehet meghívni az alapértelmezett implementációt.

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Trait-ek használata paraméterként

Most, hogy tudod, hogyan definiálj és implementálj trait-eket, nézzük meg,
hogyan használhatók a trait-ek olyan függvények definiálására, amelyek sokféle
különböző típust fogadnak el. A 10-13. listában a `NewsArticle` és a
`SocialPost` típuson implementált `Summary` trait-et fogjuk használni egy
`notify` függvény definiálásához, amely meghívja a `summarize` metódust az
`item` paraméterén; ez a paraméter olyan típusú, amely implementálja a
`Summary` trait-et. Ehhez az `impl Trait` szintaxist használjuk, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Az `item` paraméterhez nem konkrét típust adunk meg, hanem az `impl` kulcsszót
és a trait nevét. Ez a paraméter bármilyen olyan típust elfogad, amely
implementálja a megadott trait-et. A `notify` törzsében az `item`-en meghívhatunk
bármilyen metódust, amely a `Summary` trait-től származik, például a
`summarize` metódust. A `notify` függvényt meghívhatjuk, és átadhatjuk neki a
`NewsArticle` vagy a `SocialPost` bármelyik példányát. Az a kód, amely bármely
más típussal hívja meg a függvényt, például egy `String`-gel vagy egy `i32`-vel,
nem fordul le, mert azok a típusok nem implementálják a `Summary` trait-et.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### A trait bound szintaxisa

Az `impl Trait` szintaxis egyszerű esetekben jól működik, valójában azonban
szintaktikai cukorka egy hosszabb alakra, amelyet _trait bound_-nak nevezünk;
az így néz ki:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Ez a hosszabb alak egyenértékű az előző szakasz példájával, csak bőbeszédűbb. A
trait bound-okat a generikus típusparaméter deklarációjához írjuk, egy
kettőspont után, csúcsos zárójeleken belül.

Az `impl Trait` szintaxis kényelmes, és egyszerű esetekben tömörebb kódot
eredményez, míg a teljesebb trait bound szintaxis más esetekben bonyolultabb
dolgokat is ki tud fejezni. Lehet például két olyan paraméterünk, amely
implementálja a `Summary` trait-et. Az `impl Trait` szintaxissal ez így néz ki:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Az `impl Trait` használata akkor helyénvaló, ha azt szeretnénk, hogy a függvény
megengedje az `item1` és az `item2` eltérő típusát (feltéve, hogy mindkét típus
implementálja a `Summary` trait-et). Ha viszont azt akarjuk kikényszeríteni,
hogy mindkét paraméter ugyanolyan típusú legyen, akkor trait bound-ot kell
használnunk, így:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Az `item1` és az `item2` paraméter típusaként megadott `T` generikus típus úgy
korlátozza a függvényt, hogy az `item1` és az `item2` argumentumaként átadott
érték konkrét típusának meg kell egyeznie.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Több trait bound a `+` szintaxissal

Egynél több trait bound-ot is megadhatunk. Tegyük fel, hogy azt szeretnénk, ha
a `notify` az `item`-en a `summarize` mellett a megjelenítéshez való formázást
is használhatná: a `notify` definíciójában megadjuk, hogy az `item`-nek a
`Display` és a `Summary` trait-et is implementálnia kell. Ezt a `+`
szintaxissal tehetjük meg:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

A `+` szintaxis generikus típusokon lévő trait bound-okkal is használható:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

A két trait bound megadásával a `notify` törzse meghívhatja a `summarize`
metódust, és a `{}` segítségével formázhatja az `item`-et.

#### Átláthatóbb trait bound-ok `where` klózokkal

A túl sok trait bound használatának megvannak a hátrányai. Minden generikusnak
saját trait bound-jai vannak, így a több generikus típusparaméterrel rendelkező
függvényeknél rengeteg trait bound információ zsúfolódhat a függvény neve és a
paraméterlistája közé, amitől a függvényszignatúrát nehéz lesz olvasni. Ezért a
Rustban van egy másik szintaxis is a trait bound-ok megadására: egy `where`
klóz a függvényszignatúra után. Vagyis ahelyett, hogy ezt írnánk:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

használhatunk egy `where` klózt, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Ennek a függvénynek a szignatúrája kevésbé zsúfolt: a függvény neve, a
paraméterlista és a visszatérési típus közel van egymáshoz, hasonlóan egy olyan
függvényhez, amelynek nincs sok trait bound-ja.

### Trait-eket implementáló típusok visszaadása

Az `impl Trait` szintaxist a visszatérési érték helyén is használhatjuk, hogy
egy trait-et implementáló valamilyen típusú értéket adjunk vissza, ahogy itt
látható:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Azzal, hogy visszatérési típusként az `impl Summary`-t használjuk, azt adjuk
meg, hogy a `returns_summarizable` függvény valamilyen olyan típust ad vissza,
amely implementálja a `Summary` trait-et, anélkül hogy megneveznénk a konkrét
típust. Ebben az esetben a `returns_summarizable` egy `SocialPost`-ot ad
vissza, de a függvényt hívó kódnak erről nem kell tudnia.

Az a lehetőség, hogy a visszatérési típust csak az általa implementált trait
alapján adjuk meg, különösen hasznos a closure-ök és az iterátorok
kontextusában, amelyekkel a 13. fejezetben foglalkozunk. A closure-ök és az
iterátorok olyan típusokat hoznak létre, amelyeket csak a fordító ismer, vagy
amelyeket nagyon hosszú lenne leírni. Az `impl Trait` szintaxis lehetővé teszi,
hogy tömören megadd: egy függvény olyan típust ad vissza, amely implementálja
az `Iterator` trait-et, anélkül hogy egy nagyon hosszú típust kellene kiírnod.

Az `impl Trait` azonban csak akkor használható, ha egyetlen típust adsz vissza.
Például ez a kód, amely vagy egy `NewsArticle`-t, vagy egy `SocialPost`-ot ad
vissza `impl Summary` visszatérési típussal, nem működne:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Az, hogy vagy egy `NewsArticle`-t, vagy egy `SocialPost`-ot adjunk vissza, nem
megengedett, mert az `impl Trait` szintaxis fordítóbeli megvalósítása bizonyos
korlátokkal jár. Azt, hogyan írhatunk ilyen viselkedésű függvényt, a 18. fejezet
[„Trait objectek használata osztott viselkedés absztrahálására”][trait-objects]<!-- ignore -->
című szakaszában tárgyaljuk.

### Metódusok feltételes implementálása trait bound-okkal

Ha egy generikus típusparamétereket használó `impl` blokkban trait bound-ot
alkalmazunk, feltételesen implementálhatunk metódusokat azokra a típusokra,
amelyek a megadott trait-eket implementálják. Például a 10-15. listában
szereplő `Pair<T>` típus mindig implementálja a `new` függvényt, amely egy új
`Pair<T>` példányt ad vissza (idézd fel az 5. fejezet
[„Metódusszintaxis”][methods]<!-- ignore --> című szakaszából, hogy a `Self`
egy típusalias az `impl` blokk típusára, ami ebben az esetben a `Pair<T>`). A
következő `impl` blokkban viszont a `Pair<T>` csak akkor implementálja a
`cmp_display` metódust, ha a belső `T` típusa implementálja az
összehasonlítást lehetővé tevő `PartialOrd` trait-et _és_ a kiírást lehetővé
tevő `Display` trait-et.

<Listing number="10-15" file-name="src/lib.rs" caption="Metódusok feltételes implementálása egy generikus típuson trait bound-októl függően">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Egy trait-et is implementálhatunk feltételesen bármely olyan típusra, amely egy
másik trait-et implementál. Az olyan implementációkat, amelyek egy trait-et
minden olyan típusra megvalósítanak, amely kielégíti a trait bound-okat,
_blanket implementációnak_ nevezzük, és széles körben használják őket a Rust
standard könyvtárában. A standard könyvtár például minden olyan típusra
implementálja a `ToString` trait-et, amely implementálja a `Display` trait-et.
A standard könyvtár `impl` blokkja nagyjából így néz ki:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Mivel a standard könyvtárban megvan ez a blanket implementáció, a `ToString`
trait által definiált `to_string` metódust minden olyan típuson meghívhatjuk,
amely implementálja a `Display` trait-et. Az egész számokat például azért
alakíthatjuk így a nekik megfelelő `String` értékekké, mert az egész számok
implementálják a `Display` trait-et:

```rust
let s = 3.to_string();
```

A blanket implementációk a trait dokumentációjában az „Implementors” szakaszban
jelennek meg.

A trait-ek és a trait bound-ok lehetővé teszik, hogy olyan kódot írjunk, amely
generikus típusparaméterekkel csökkenti a duplikációt, ugyanakkor megadja a
fordítónak, hogy a generikus típustól egy bizonyos viselkedést várunk el. A
fordító ezután a trait bound információ alapján ellenőrizni tudja, hogy a
kódunkkal használt összes konkrét típus nyújtja-e a megfelelő viselkedést. A
dinamikusan típusos nyelvekben futásidőben kapnánk hibát, ha olyan metódust
hívnánk meg egy típuson, amely nem definiálja azt a metódust. A Rust viszont
ezeket a hibákat fordítási időre helyezi át, így kénytelenek vagyunk még azelőtt
kijavítani a problémákat, hogy a kódunk egyáltalán futni tudna. Ráadásul nem
kell olyan kódot írnunk, amely futásidőben ellenőrzi a viselkedést, hiszen már
fordítási időben ellenőriztük. Ezzel javul a teljesítmény anélkül, hogy le
kellene mondanunk a generikusok rugalmasságáról.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
