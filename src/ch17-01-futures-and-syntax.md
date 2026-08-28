## A future-ök és az async szintaxis

A Rust aszinkron programozásának kulcselemei a _future_-ök, valamint a Rust
`async` és `await` kulcsszavai.

A _future_ olyan érték, amely most még nincs kész, de a jövő valamely pontján
készen fog állni. (Ugyanez a fogalom sok nyelvben felbukkan, néha más néven,
például _task_ vagy _promise_ néven.) A Rust építőelemként biztosít egy
`Future` trait-et, hogy a különböző aszinkron műveleteket eltérő
adatszerkezetekkel, de közös interfésszel lehessen implementálni. A Rustban a
future-ök olyan típusok, amelyek implementálják a `Future` trait-et. Minden
future maga tartja számon, mennyit haladt előre, és hogy mit jelent nála a
„kész” állapot.

Az `async` kulcsszót blokkokra és függvényekre alkalmazhatod, jelezve, hogy azok
megszakíthatók és folytathatók. Egy async blokkon vagy async függvényen belül
az `await` kulcsszóval _bevárhatsz egy future-t_ (vagyis megvárhatod, amíg
készen áll). Minden pont, ahol egy async blokkon vagy függvényen belül bevársz
egy future-t, lehetséges hely arra, hogy az adott blokk vagy függvény
szüneteljen, majd folytatódjon. Azt a folyamatot, amelynek során rákérdezünk egy
future-re, hogy elérhető-e már az értéke, _polling_-nak nevezzük.

Néhány más nyelv, például a C# és a JavaScript szintén `async` és `await`
kulcsszavakat használ az aszinkron programozáshoz. Ha ismered ezeket a
nyelveket, feltűnhetnek jelentős különbségek abban, ahogyan a Rust kezeli a
szintaxist. Ennek jó oka van, ahogy látni fogjuk!

Amikor async Rust kódot írunk, legtöbbször az `async` és az `await` kulcsszót
használjuk. A Rust ezeket a `Future` trait-et használó, ezzel egyenértékű kódra
fordítja, nagyjából úgy, ahogy a `for` ciklusokat az `Iterator` trait-et
használó, egyenértékű kódra fordítja. Mivel azonban a Rust biztosítja a
`Future` trait-et, szükség esetén a saját adattípusaidra is implementálhatod.
A fejezetben látott függvények közül sok olyan típussal tér vissza, amelynek
saját `Future` implementációja van. A fejezet végén visszatérünk a trait
definíciójához, és mélyebben is beleássuk magunkat a működésébe, de egyelőre
ennyi részlet elég ahhoz, hogy továbbhaladjunk.

Mindez talán kissé elvontnak tűnik, ezért írjuk meg az első async
programunkat: egy kis webscrapert. Két URL-t adunk át neki a parancssorból,
mindkettőt konkurensen letöltjük, és annak az eredményét adjuk vissza, amelyik
előbb elkészül. Ebben a példában elég sok új szintaxis lesz, de ne aggódj –
menet közben mindent elmagyarázunk, amit tudnod kell.

## Az első async programunk {#our-first-async-program}

Hogy a fejezet fókuszában az async tanulása maradjon, és ne az ökoszisztéma
darabjainak zsonglőrködése, létrehoztuk a `trpl` crate-et (a `trpl` a „The Rust
Programming Language” rövidítése). Ez újraexportálja az összes típust, trait-et
és függvényt, amelyre szükséged lesz, elsősorban a
[`futures`][futures-crate]<!-- ignore --> és a [`tokio`][tokio]<!-- ignore -->
crate-ekből. A `futures` crate a Rust async kóddal kapcsolatos kísérleteinek
hivatalos otthona, és valójában itt tervezték meg eredetileg a `Future`
trait-et. A Tokio ma a legszélesebb körben használt async runtime a Rustban,
különösen a webalkalmazások területén. Léteznek más kiváló runtime-ok is,
amelyek adott esetben jobban illenek a céljaidhoz. A `trpl` a motorháztető
alatt a `tokio` crate-et használja, mert az jól tesztelt és széles körben
elterjedt.

Bizonyos esetekben a `trpl` át is nevezi vagy becsomagolja az eredeti API-kat,
hogy a fejezet szempontjából lényeges részleteknél maradhass. Ha meg szeretnéd
érteni, mit csinál a crate, javasoljuk, hogy nézd meg a
[forráskódját][crate-source]. Látni fogod, melyik újraexportálás melyik
crate-ből jön, és bőséges kommentekkel magyaráztuk el, mit csinál a crate.

Hozz létre egy `hello-async` nevű új binary projektet, és vedd fel a `trpl`
crate-et függőségként:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Most már a `trpl` által nyújtott különféle darabokkal megírhatjuk az első async
programunkat. Egy kis parancssori eszközt fogunk építeni, amely letölt két
weboldalt, mindkettőből kinyeri a `<title>` elemet, és kiírja annak az oldalnak
a címét, amelyik ezt az egész folyamatot előbb befejezi.

### A page_title függvény definiálása

Kezdjük egy olyan függvény megírásával, amely paraméterként egy oldal URL-jét
kapja, kérést intéz hozzá, és visszaadja a `<title>` elem szövegét (lásd a
17-1. listát).

<Listing number="17-1" file-name="src/main.rs" caption="Async függvény definiálása egy HTML-oldal title elemének lekérésére">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Először definiálunk egy `page_title` nevű függvényt, és megjelöljük az `async`
kulcsszóval. Ezután a `trpl::get` függvénnyel letöltjük a kapott URL-t, és az
`await` kulcsszóval bevárjuk a választ. Hogy megkapjuk a `response` szövegét,
meghívjuk a `text` metódusát, és ismét bevárjuk az `await` kulcsszóval.
Mindkét lépés aszinkron. A `get` függvénynél meg kell várnunk, amíg a szerver
visszaküldi a válasza első részét, amely a HTTP-fejléceket, a sütiket és így
tovább tartalmazza, és a válasz törzsétől külön is megérkezhet. Különösen akkor
tarthat egy ideig, amíg minden megérkezik, ha a törzs nagyon nagy. Mivel meg
kell várnunk a válasz _egészének_ megérkezését, a `text` metódus is async.

Mindkét future-t kifejezetten be kell várnunk, mert a Rustban a future-ök
_lusták_: addig nem csinálnak semmit, amíg az `await` kulcsszóval erre meg nem
kéred őket. (Sőt, a Rust fordítói figyelmeztetést ad, ha nem használsz fel egy
future-t.) Ez emlékeztethet a 13. fejezet [„Elemsorozatok feldolgozása
iterátorokkal”][iterators-lazy]<!-- ignore --> szakaszában az iterátorokról
folytatott beszélgetésre. Az iterátorok sem csinálnak semmit, amíg meg nem
hívod a `next` metódusukat – akár közvetlenül, akár `for` ciklusokon vagy olyan
metódusokon keresztül, mint a `map`, amelyek a motorháztető alatt a `next`-et
használják. Hasonlóképpen a future-ök sem csinálnak semmit, amíg kifejezetten
meg nem kéred őket. Ez a lustaság teszi lehetővé, hogy a Rust elkerülje az
async kód futtatását addig, amíg arra ténylegesen szükség nincs.

> Megjegyzés: ez eltér attól a viselkedéstől, amelyet a 16. fejezet [„Új szál
> létrehozása a spawn segítségével”][thread-spawn]<!-- ignore --> szakaszában a
> `thread::spawn` használatakor láttunk, ahol a másik szálnak átadott closure
> azonnal futni kezdett. Attól is eltér, ahogyan sok más nyelv közelíti meg az
> asyncet. A Rustnak viszont fontos, hogy a teljesítménygaranciáit tudja
> nyújtani, éppúgy, mint az iterátorok esetében.

Ha már megvan a `response_text`, az `Html::parse` segítségével feldolgozhatjuk
a `Html` típus egy példányává. Nyers sztring helyett most már olyan adattípusunk
van, amellyel gazdagabb adatszerkezetként dolgozhatunk a HTML-lel. Használhatjuk
például a `select_first` metódust, hogy megkeressük egy adott CSS-szelektor
első előfordulását. A `"title"` sztringet átadva megkapjuk a dokumentum első
`<title>` elemét, ha van ilyen. Mivel előfordulhat, hogy nincs illeszkedő elem,
a `select_first` egy `Option<ElementRef>` értékkel tér vissza. Végül az
`Option::map` metódust használjuk, amellyel dolgozhatunk az `Option` elemével,
ha jelen van, és nem csinálunk semmit, ha nincs. (Használhatnánk itt egy
`match` kifejezést is, de a `map` idiomatikusabb.) A `map`-nek átadott függvény
törzsében meghívjuk a `title`-ön az `inner_html`-t, hogy megkapjuk a tartalmát,
ami egy `String`. A végeredmény tehát egy `Option<String>`.

Figyeld meg, hogy a Rust `await` kulcsszava a bevárt kifejezés _után_ áll, nem
pedig előtte. Vagyis _postfix_ kulcsszó. Ez eltérhet attól, amit megszoktál, ha
más nyelvekben használtál már `async`-ot, de a Rustban ettől sokkal
kényelmesebb dolgozni a metódusláncokkal. Ennek eredményeként a `page_title`
törzsét átírhatjuk úgy, hogy a `trpl::get` és a `text` függvényhívásokat
láncba fűzzük, közéjük téve az `await`-et, ahogy a 17-2. lista mutatja.

<Listing number="17-2" file-name="src/main.rs" caption="Láncolás az `await` kulcsszóval">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Ezzel sikeresen megírtuk az első async függvényünket! Mielőtt kódot írnánk a
`main`-be a meghívásához, beszéljünk még egy kicsit arról, mit is írtunk, és mit
jelent.

Amikor a Rust `async` kulcsszóval megjelölt _blokkot_ lát, azt egy egyedi,
névtelen adattípussá fordítja, amely implementálja a `Future` trait-et. Amikor
a Rust `async`-kal megjelölt _függvényt_ lát, azt egy nem async függvénnyé
fordítja, amelynek a törzse egy async blokk. Egy async függvény visszatérési
típusa az a névtelen adattípus, amelyet a fordító az adott async blokkhoz
létrehoz.

Így az `async fn` írása egyenértékű egy olyan függvény írásával, amely a
visszatérési típus _future_-jével tér vissza. A fordító számára egy olyan
függvénydefiníció, mint a 17-1. listában szereplő `async fn page_title`,
nagyjából egyenértékű az alábbi, nem async függvénnyel:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Nézzük végig az átalakított változat egyes részeit:

- Az `impl Trait` szintaxist használja, amelyet még a 10. fejezet
  [„Trait-ek paraméterként”][impl-trait]<!-- ignore --> szakaszában tárgyaltunk.
- A visszaadott érték implementálja a `Future` trait-et, amelynek `Output`
  asszociált típusa van. Figyeld meg, hogy az `Output` típus `Option<String>`,
  ugyanaz, mint a `page_title` `async fn` változatának eredeti visszatérési
  típusa.
- Az eredeti függvény törzsében meghívott összes kód egy `async move` blokkba
  van csomagolva. Emlékezz, hogy a blokkok kifejezések. Ez az egész blokk az a
  kifejezés, amellyel a függvény visszatér.
- Ez az async blokk `Option<String>` típusú értéket állít elő, ahogy az imént
  leírtuk. Ez az érték megfelel a visszatérési típusban szereplő `Output`
  típusnak. Éppen úgy, mint a többi blokknál, amelyeket eddig láttál.
- Az új függvénytörzs `async move` blokk amiatt, ahogyan az `url` paramétert
  használja. (Az `async` és az `async move` közti különbségről sokkal bővebben
  is szó lesz később a fejezetben.)

Most már meghívhatjuk a `page_title`-t a `main`-ben.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Async függvény végrehajtása runtime segítségével

Kezdésként egyetlen oldal címét kérjük le, ahogy a 17-3. lista mutatja. Sajnos
ez a kód még nem fordul le.

<Listing number="17-3" file-name="src/main.rs" caption="A `page_title` függvény meghívása a `main`-ből, felhasználó által megadott argumentummal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Ugyanazt a mintát követjük, amelyet a parancssori argumentumok lekérésére
használtunk a 12. fejezet [„Parancssori argumentumok
fogadása”][cli-args]<!-- ignore --> szakaszában. Ezután átadjuk az URL
argumentumot a `page_title`-nek, és bevárjuk az eredményt. Mivel a future által
előállított érték egy `Option<String>`, egy `match` kifejezéssel különböző
üzeneteket írunk ki attól függően, hogy az oldalnak volt-e `<title>` eleme.

Az `await` kulcsszót csak async függvényekben vagy blokkokban használhatjuk, a
Rust pedig nem engedi, hogy a speciális `main` függvényt `async`-ként jelöljük
meg.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

A `main` azért nem jelölhető meg `async`-ként, mert az async kódnak _runtime_-ra
van szüksége: egy olyan Rust crate-re, amely az aszinkron kód végrehajtásának
részleteit kezeli. Egy program `main` függvénye _elindíthat_ egy runtime-ot, de
_maga_ nem runtime. (Nemsokára többet is látunk arról, miért van ez így.)
Minden olyan Rust programban, amely async kódot hajt végre, van legalább egy
hely, ahol beállít egy runtime-ot a future-ök végrehajtásához.

Az asyncet támogató nyelvek többsége runtime-mal együtt érkezik, a Rust
azonban nem. Ehelyett sok különböző async runtime érhető el, és mindegyik más
kompromisszumokat köt, a célzott felhasználási esetnek megfelelően. Egy nagy
áteresztőképességű, sok CPU-maggal és rengeteg RAM-mal rendelkező webszervernek
például egészen más igényei vannak, mint egy egymagos, kevés RAM-mal
rendelkező, heap-lefoglalásra képtelen mikrokontrollernek. Az ilyen runtime-okat
biztosító crate-ek gyakran a gyakori funkcionalitások – például a fájl- vagy
hálózati I/O – async változatait is nyújtják.

Itt és a fejezet további részében a `trpl` crate `block_on` függvényét
használjuk, amely argumentumként egy future-t vár, és blokkolja az aktuális
szálat, amíg ez a future be nem fejeződik. A színfalak mögött a `block_on`
hívása a `tokio` crate segítségével beállít egy runtime-ot, amely a kapott
future futtatására szolgál (a `trpl` crate `block_on` viselkedése hasonló más
runtime crate-ek `block_on` függvényeihez). Amint a future befejeződik, a
`block_on` visszaadja azt az értéket, amelyet a future előállított.

A `page_title` által visszaadott future-t közvetlenül is átadhatnánk a
`block_on`-nak, majd amikor befejeződik, mintaillesztést végezhetnénk a kapott
`Option<String>`-en, ahogy a 17-3. listában is próbáltuk. A fejezet legtöbb
példájában (és a való világ legtöbb async kódjában) azonban egynél több async
függvényhívásunk lesz, ezért inkább egy `async` blokkot adunk át, és
kifejezetten bevárjuk a `page_title` hívás eredményét, ahogy a 17-4. listában.

<Listing number="17-4" caption="Async blokk bevárása a `trpl::block_on` segítségével" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Amikor lefuttatjuk ezt a kódot, azt a viselkedést kapjuk, amelyet eredetileg
vártunk:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Hűha – végre van működő async kódunk! Mielőtt azonban megírnánk a kódot, amely
két oldalt versenyeztet egymással, fordítsuk vissza röviden a figyelmünket
arra, hogyan működnek a future-ök.

Minden _await pont_ – vagyis minden hely, ahol a kód az `await` kulcsszót
használja – olyan pontot jelöl, ahol a vezérlés visszakerül a runtime-hoz.
Ahhoz, hogy ez működjön, a Rustnak nyilván kell tartania az async blokkban
szereplő állapotot, hogy a runtime elindíthasson valamilyen más munkát, majd
visszatérhessen, amikor készen áll arra, hogy megpróbálja továbbléptetni az
elsőt. Ez egy láthatatlan állapotgép, mintha egy ilyen enumot írtál volna, hogy
minden await pontnál elmentsd az aktuális állapotot:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Az egyes állapotok közti átmeneteket kezelő kód kézzel való megírása azonban
fárasztó és hibalehetőségekkel teli lenne, különösen amikor később további
funkcionalitást és további állapotokat kell hozzáadnod a kódhoz. Szerencsére a
Rust fordító automatikusan létrehozza és kezeli az async kód állapotgépének
adatszerkezeteit. Az adatszerkezetekre vonatkozó szokásos borrowing- és
ownership-szabályok továbbra is érvényesek, és örömünkre a fordító ezek
ellenőrzését is elvégzi helyettünk, ráadásul hasznos hibaüzeneteket ad. Ezek
közül néhányon később a fejezetben végig fogunk menni.

Végső soron valaminek végre kell hajtania ezt az állapotgépet, és ez a valami
a runtime. (Ezért találkozhatsz az _executor_-ok említésével, amikor a
runtime-okat nézegeted: az executor a runtime azon része, amely az async kód
végrehajtásáért felel.)

Most már érted, miért akadályozott meg minket a fordító abban, hogy a `main`-t
magát async függvénnyé tegyük a 17-3. listában. Ha a `main` async függvény
lenne, valami másnak kellene kezelnie annak a future-nek az állapotgépét,
amellyel a `main` visszatér – csakhogy a `main` a program kiindulópontja!
Ehelyett a `main`-ben meghívtuk a `trpl::block_on` függvényt, hogy beállítsunk
egy runtime-ot, és lefuttassuk az `async` blokk által visszaadott future-t,
amíg el nem készül.

> Megjegyzés: néhány runtime makrókat kínál, hogy _tudj_ async `main`
> függvényt írni. Ezek a makrók átírják az `async fn main() { ... }`-t normál
> `fn main`-né, amely ugyanazt csinálja, amit mi kézzel csináltunk a 17-4.
> listában: meghív egy függvényt, amely a `trpl::block_on`-hoz hasonlóan
> végigfuttat egy future-t.

Most rakjuk össze ezeket a darabokat, és nézzük meg, hogyan írhatunk konkurens
kódot.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Két URL konkurens versenyeztetése egymással

A 17-5. listában a `page_title`-t két különböző, parancssorból kapott URL-lel
hívjuk meg, és versenyeztetjük őket úgy, hogy kiválasztjuk azt a future-t,
amelyik előbb befejeződik.

<Listing number="17-5" caption="A `page_title` meghívása két URL-re, hogy lássuk, melyik tér vissza előbb" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Azzal kezdjük, hogy meghívjuk a `page_title`-t a felhasználó által megadott
URL-ek mindegyikére. A kapott future-öket `title_fut_1` és `title_fut_2` néven
mentjük el. Ne feledd, ezek még nem csinálnak semmit, mert a future-ök lusták,
és még nem vártuk be őket. Ezután átadjuk a future-öket a `trpl::select`-nek,
amely egy olyan értékkel tér vissza, amely jelzi, hogy a neki átadott future-ök
közül melyik fejeződött be előbb.

> Megjegyzés: a motorháztető alatt a `trpl::select` egy általánosabb, a
> `futures` crate-ben definiált `select` függvényre épül. A `futures` crate
> `select` függvénye rengeteg olyasmire képes, amire a `trpl::select` nem, de
> jár vele némi további bonyolultság is, amelyet egyelőre átugorhatunk.

Bármelyik future „nyerhet” jogosan, így nincs értelme `Result`-tal visszatérni.
Ehelyett a `trpl::select` egy olyan típussal tér vissza, amellyel eddig nem
találkoztunk: a `trpl::Either`-rel. Az `Either` típus némiképp hasonlít a
`Result`-ra abban, hogy két esete van. A `Result`-tal ellentétben viszont az
`Either`-be nincs beleépítve a siker vagy a kudarc fogalma. Ehelyett a `Left`
és a `Right` jelöli az „egyiket vagy a másikat”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

A `select` függvény `Left`-tel és az adott future kimenetével tér vissza, ha az
első argumentum nyer, illetve `Right`-tal és a második future argumentum
kimenetével, ha _az_ nyer. Ez megfelel annak a sorrendnek, amelyben az
argumentumok a függvény hívásakor megjelennek: az első argumentum a második
argumentumtól balra áll.

A `page_title`-t is módosítjuk, hogy visszaadja a neki átadott URL-t is. Így ha
az előbb visszatérő oldalnak nincs feloldható `<title>` eleme, akkor is ki
tudunk írni értelmes üzenetet. Ezzel az információval a kezünkben úgy zárjuk a
munkát, hogy frissítjük a `println!` kimenetét, hogy jelezze, melyik URL
fejeződött be előbb, és hogy mi az adott URL-en található weboldal `<title>`-je,
ha van ilyen.

Ezzel most már építettél egy kicsi, működő webscrapert! Válassz ki néhány
URL-t, és futtasd a parancssori eszközt. Felfedezheted, hogy egyes oldalak
következetesen gyorsabbak másoknál, míg más esetekben futásról futásra változik,
melyik oldal a gyorsabb. Ami még fontosabb: megtanultad a future-ökkel való
munka alapjait, így most már mélyebbre áshatunk abban, mi mindent tehetünk az
asynckel.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
