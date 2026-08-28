<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Közelebbi pillantás az async trait-jeire

A fejezet során többféle módon használtuk a `Future`, a `Stream` és a
`StreamExt` trait-et. Eddig viszont kerültük, hogy túl mélyen belemenjünk abba,
hogyan működnek, vagy hogyan illeszkednek egymáshoz – ez a mindennapi Rust
munkádhoz általában bőven elég is. Néha azonban olyan helyzetekbe kerülsz,
amikor meg kell értened ezeknek a trait-eknek néhány további részletét,
valamint a `Pin` típust és az `Unpin` trait-et. Ebben a szakaszban épp csak
annyira ásunk bele, hogy ezekben az esetekben segítsen; a _valóban_ mély
merülést más dokumentációra hagyjuk.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### A `Future` trait

Kezdjük azzal, hogy közelebbről megnézzük, hogyan működik a `Future` trait. Így
definiálja a Rust:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Ez a trait-definíció egy csomó új típust és néhány olyan szintaxist is
tartalmaz, amelyet még nem láttunk, úgyhogy nézzük végig darabonként.

Először is, a `Future` `Output` asszociált típusa mondja meg, mivé oldódik fel a
future. Ez a `Item` asszociált típus megfelelője az `Iterator` trait-nél.
Másodszor, a `Future`-nek van egy `poll` metódusa, amely a `self` paraméteréhez
egy speciális `Pin` referenciát vár, továbbá egy módosítható referenciát egy
`Context` típusra, és egy `Poll<Self::Output>` értékkel tér vissza. A `Pin`-ről
és a `Context`-ről mindjárt bővebben is beszélünk. Egyelőre koncentráljunk arra,
amivel a metódus visszatér, a `Poll` típusra:

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Ez a `Poll` típus hasonlít az `Option`-höz. Van egy változata, amely értéket
tartalmaz, a `Ready(T)`, és egy, amely nem, a `Pending`. A `Poll` jelentése
azonban egészen más, mint az `Option`-é! A `Pending` változat azt jelzi, hogy a
future-nek még van tennivalója, tehát a hívónak később újra ellenőriznie kell.
A `Ready` változat azt jelzi, hogy a `Future` befejezte a munkáját, és a `T`
érték elérhető.

> Megjegyzés: Ritkán van szükség arra, hogy közvetlenül hívd a `poll`-t, de ha
> mégis, tartsd észben, hogy a legtöbb future-nél a hívónak nem szabad újra
> meghívnia a `poll`-t azután, hogy a future `Ready` értéket adott vissza. Sok
> future panicot vált ki, ha a készre válása után újra pollozzák. Azok a
> future-ök, amelyeknél biztonságos az újbóli poll, ezt kifejezetten jelzik a
> dokumentációjukban. Ez hasonlít az `Iterator::next` viselkedéséhez.

Amikor `await`-et használó kódot látsz, a Rust a motorháztető alatt olyan kódra
fordítja, amely a `poll`-t hívja. Ha visszalapozol a 17-4. listához, ahol egy
URL oldalcímét írtuk ki, miután feloldódott, a Rust nagyjából (bár nem
pontosan) ilyesmire fordítja:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```

Mit tegyünk, ha a future még `Pending`? Kell valami mód arra, hogy újra és újra
és újra megpróbáljuk, amíg a future végül készen nem áll. Más szóval egy
ciklusra van szükségünk:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```

Ha viszont a Rust pontosan erre a kódra fordítaná, akkor minden `await`
blokkolna – vagyis pont az ellenkezője történne annak, amit szerettünk volna!
Ehelyett a Rust gondoskodik arról, hogy a ciklus át tudja adni a vezérlést
valaminek, ami szüneteltetheti az ezen a future-ön végzett munkát, hogy más
future-ökkel foglalkozzon, majd később újra ellenőrizze ezt. Ahogy láttuk, ez a
„valami” egy async runtime, és ez az ütemezési és koordinációs munka az egyik fő
feladata.

Az [„Adatküldés két task között üzenetküldéssel”][message-passing]<!-- ignore -->
szakaszban leírtuk az `rx.recv` bevárását. A `recv` hívás egy future-t ad
vissza, és a future bevárása pollozza azt. Megjegyeztük, hogy a runtime
szünetelteti a future-t, amíg az készen nem áll vagy egy `Some(message)`
értékkel, vagy `None`-nal, ha a csatorna bezárul. Most, hogy mélyebben értjük a
`Future` trait-et, és azon belül a `Future::poll`-t, láthatjuk, hogyan működik
ez. A runtime tudja, hogy a future nem áll készen, ha az `Poll::Pending`
értékkel tér vissza. Fordítva, a runtime tudja, hogy a future _készen_ áll, és
tovább is lépteti, ha a `poll` `Poll::Ready(Some(message))` vagy
`Poll::Ready(None)` értékkel tér vissza.

Annak pontos részletei, hogy egy runtime ezt hogyan csinálja, túlmutatnak a
könyv keretein, de a lényeg, hogy lásd a future-ök alapvető működését: a runtime
_pollozza_ minden future-t, amelyért felel, és visszaalusztatja azt, amelyik még
nem áll készen.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### A `Pin` típus és az `Unpin` trait

A 17-13. listában a `trpl::join!` makróval vártunk be három future-t. Gyakori
azonban, hogy van egy kollekciónk – például egy vektorunk –, amely annyi
future-t tartalmaz, amennyi csak futásidőben derül ki. Alakítsuk át a 17-13.
listát a 17-23. lista kódjává, amely a három future-t egy vektorba teszi, és
ehelyett a `trpl::join_all` függvényt hívja; ez még nem fog lefordulni.

<Listing number="17-23" caption="Kollekcióban lévő future-ök bevárása"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Minden future-t egy `Box`-ba teszünk, hogy _trait objektumokká_ tegyük őket,
ahogy azt a 12. fejezet „Hibák visszaadása a `run`-ból” szakaszában is tettük.
(A trait objektumokkal részletesen a 18. fejezetben foglalkozunk.) A trait
objektumok használatával az ezek a típusok által előállított névtelen future-ök
mindegyikét azonos típusúként kezelhetjük, mivel mindegyik implementálja a
`Future` trait-et.

Ez talán meglepő. Végtére is egyik async blokk sem ad vissza semmit, tehát
mindegyik `Future<Output = ()>` típust állít elő. Ne feledd azonban, hogy a
`Future` egy trait, és hogy a fordító minden async blokkhoz külön, egyedi enumot
hoz létre, még akkor is, ha azonos a kimeneti típusuk. Ahogy két különböző,
kézzel írt structot sem tehetsz egyetlen `Vec`-be, a fordító által generált
enumokat sem keverheted.

Ezután átadjuk a future-ök kollekcióját a `trpl::join_all` függvénynek, és
bevárjuk az eredményt. Ez azonban nem fordul le; itt a hibaüzenetek lényeges
része.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

A hibaüzenet megjegyzése elárulja, hogy a `pin!` makróval kellene _pinelnünk_
az értékeket, ami azt jelenti, hogy beletesszük őket a `Pin` típusba, amely
garantálja, hogy az értékek nem mozdulnak el a memóriában. A hibaüzenet szerint
a pinelés azért szükséges, mert a `dyn Future<Output = ()>` típusnak
implementálnia kellene az `Unpin` trait-et, jelenleg viszont nem teszi.

A `trpl::join_all` függvény egy `JoinAll` nevű structtal tér vissza. Ez a
struct generikus egy `F` típusra nézve, amelyre az a megkötés vonatkozik, hogy
implementálja a `Future` trait-et. Ha egy future-t közvetlenül `await`-tel
várunk be, az implicit módon pineli a future-t. Ezért nem kell mindenhol a
`pin!` makrót használnunk, ahol future-öket akarunk bevárni.

Itt azonban nem közvetlenül várunk be egy future-t. Ehelyett egy új future-t, a
JoinAll-t hozzuk létre azzal, hogy a future-ök egy kollekcióját átadjuk a
`join_all` függvénynek. A `join_all` szignatúrája megköveteli, hogy a
kollekcióban lévő elemek típusai mind implementálják a `Future` trait-et, a
`Box<T>` pedig csak akkor implementálja a `Future`-t, ha a becsomagolt `T` olyan
future, amely implementálja az `Unpin` trait-et.

Ez elég sok mindent kell megemészteni! Hogy igazán megértsük, ássunk bele még
kicsit mélyebben abba, hogyan is működik a `Future` trait, különösen a pinelés
körül. Nézd meg újra a `Future` trait definícióját:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

A `cx` paraméter és annak `Context` típusa a kulcsa annak, hogy egy runtime
valójában honnan tudja, mikor ellenőrizzen egy adott future-t, miközben
lusta marad. Ismét: ennek részletei túlmutatnak a fejezet keretein, és
általában csak akkor kell ezzel foglalkoznod, ha saját `Future` implementációt
írsz. Helyette a `self` típusára koncentrálunk, mivel most látunk először olyan
metódust, ahol a `self` típusannotációt kap. A `self` típusannotációja úgy
működik, mint a többi függvényparaméter típusannotációja, két lényeges
különbséggel:

- Megmondja a Rustnak, milyen típusúnak kell lennie a `self`-nek ahhoz, hogy a
  metódus meghívható legyen.
- Nem lehet akármilyen típus. Csak az a típus lehet, amelyre a metódus
  implementálva van, egy arra a típusra mutató referencia vagy smart pointer,
  vagy egy `Pin`, amely egy arra a típusra mutató referenciát csomagol be.

Erről a szintaxisról a [18. fejezetben][ch-18]<!-- ignore --> lesz szó
bővebben. Egyelőre elég annyit tudni, hogy ha pollozni akarunk egy future-t
annak ellenőrzésére, hogy `Pending` vagy `Ready(Output)` állapotban van-e,
akkor egy `Pin`-be csomagolt módosítható referenciára van szükségünk az adott
típusra.

A `Pin` egy burkoló a pointerszerű típusok, például az `&`, `&mut`, `Box` és
`Rc` számára. (Szigorúan véve a `Pin` azokkal a típusokkal működik, amelyek
implementálják a `Deref` vagy a `DerefMut` trait-et, de ez gyakorlatilag
egyenértékű azzal, hogy csak referenciákkal és smart pointerekkel dolgozik.) A
`Pin` maga nem pointer, és nincs saját viselkedése, mint például az `Rc`-nek és
az `Arc`-nak a referenciaszámlálás; tisztán olyan eszköz, amellyel a fordító
megkötéseket kényszeríthet ki a pointerek használatára.

Ha felidézzük, hogy az `await` a `poll` hívásaira épül, kezd magyarázatot kapni
a korábban látott hibaüzenet – az viszont az `Unpin`-ről szólt, nem a
`Pin`-ről. Hogyan is viszonyul tehát a `Pin` az `Unpin`-hoz, és miért van
szüksége a `Future`-nek arra, hogy a `self` egy `Pin` típusban legyen a `poll`
hívásához?

Emlékezz vissza a fejezet korábbi részéből, hogy egy future-ben lévő await
pontok sorozata állapotgéppé fordul, és a fordító gondoskodik róla, hogy ez az
állapotgép betartsa a Rust összes szokásos biztonsági szabályát, beleértve a
borrowingot és az ownershipet. Ehhez a Rust megnézi, milyen adatokra van
szükség az egyik await pont és a következő await pont vagy az async blokk vége
között. Ezután létrehoz egy ennek megfelelő változatot a lefordított
állapotgépben. Minden változat megkapja a szükséges hozzáférést azokhoz az
adatokhoz, amelyeket a forráskód adott szakaszában használni fog – vagy úgy,
hogy átveszi az adott adat ownershipjét, vagy úgy, hogy módosítható, illetve
nem módosítható referenciát kap rá.

Eddig rendben is vagyunk: ha bármit elrontunk egy adott async blokk
ownershipjével vagy referenciáival kapcsolatban, a borrow checker szólni fog.
Amikor viszont mozgatni akarjuk az adott blokkhoz tartozó future-t – például
egy `Vec`-be helyezve, hogy átadjuk a `join_all`-nak –, a dolgok bonyolultabbá
válnak.

Amikor mozgatunk egy future-t – akár úgy, hogy betoljuk egy adatszerkezetbe,
hogy iterátorként használjuk a `join_all`-lal, akár úgy, hogy visszaadjuk egy
függvényből –, az valójában azt jelenti, hogy a Rust által számunkra létrehozott
állapotgépet mozgatjuk. És a Rust legtöbb más típusától eltérően az async
blokkokhoz létrehozott future-ök végül önmagukra mutató referenciákat is
tartalmazhatnak egy-egy változat mezőiben, ahogy azt a 17-4. ábra
egyszerűsített szemléltetése mutatja.

<figure>

<img alt="Egyoszlopos, háromsoros táblázat, amely egy fut1 nevű future-t ábrázol; az első két sorában a 0 és az 1 adatérték szerepel, a harmadik sorból pedig egy nyíl mutat vissza a második sorra, ami a future-ön belüli belső referenciát jelképezi." src="img/trpl17-04.svg" class="center" />

<figcaption>17-4. ábra: Önmagára hivatkozó adattípus</figcaption>

</figure>

Alapesetben viszont minden olyan objektum, amelynek van önmagára mutató
referenciája, biztonságosan nem mozgatható, mert a referenciák mindig annak a
tényleges memóriacímére mutatnak, amire hivatkoznak (lásd a 17-5. ábrát). Ha
magát az adatszerkezetet elmozgatod, ezek a belső referenciák továbbra is a régi
helyre fognak mutatni. Az a memóriahely viszont már érvénytelen. Egyrészt az ott
lévő érték nem frissül, amikor módosítod az adatszerkezetet. Másrészt – és ez a
fontosabb – a számítógép mostantól szabadon felhasználhatja azt a memóriát más
célokra! Így később akár teljesen független adatokat is olvashatnál onnan.

<figure>

<img alt="Két táblázat, amelyek két future-t, a fut1-et és a fut2-t ábrázolják; mindkettőnek egy oszlopa és három sora van, és azt az eredményt mutatják, ahogy egy future-t kimozgattunk a fut1-ből a fut2-be. Az első, a fut1 szürkére van halványítva, minden indexében kérdőjel áll, ami ismeretlen memóriát jelöl. A másodikban, a fut2-ben az első és a második sorban 0 és 1 áll, a harmadik sorából pedig egy nyíl mutat vissza a fut1 második sorára; ez az a pointer, amely a future mozgatás előtti régi memóriahelyére hivatkozik." src="img/trpl17-05.svg" class="center" />

<figcaption>17-5. ábra: Önmagára hivatkozó adattípus mozgatásának nem biztonságos eredménye</figcaption>

</figure>

Elméletileg a Rust fordítója megpróbálhatná frissíteni az objektumra mutató
összes referenciát, valahányszor azt elmozgatják, de ez sok teljesítménybeli
többletköltséggel járhatna, különösen, ha referenciák egész hálóját kellene
frissíteni. Ha ehelyett biztosítani tudnánk, hogy a szóban forgó adatszerkezet
_ne mozduljon el a memóriában_, akkor semmilyen referenciát nem kellene
frissítenünk. Pontosan erre való a Rust borrow checkere: a biztonságos kódban
megakadályozza, hogy elmozgass olyan elemet, amelyre aktív referencia mutat.

A `Pin` erre épít, és pontosan azt a garanciát adja meg, amire szükségünk van.
Amikor egy értéket _pinelünk_ azzal, hogy egy rá mutató pointert `Pin`-be
csomagolunk, az többé nem mozdulhat el. Így ha `Pin<Box<SomeType>>` értéked van,
valójában a `SomeType` értéket pineled, _nem_ a `Box` pointert. A 17-6. ábra
szemlélteti ezt a folyamatot.

<figure>

<img alt="Három egymás mellé helyezett doboz. Az elsőn a „Pin”, a másodikon a „b1”, a harmadikon a „pinned” felirat. A „pinned” dobozban egy „fut” feliratú, egyoszlopos táblázat van; ez egy future-t ábrázol, amelynek minden cellája az adatszerkezet egy-egy részének felel meg. Az első cellájában a „0” érték áll, a másodikból egy nyíl indul ki, amely a negyedik, egyben utolsó cellára mutat, amelyben az „1” érték szerepel, a harmadik cellában pedig szaggatott vonalak és pontok jelzik, hogy az adatszerkezetnek lehetnek további részei is. Együttesen a „fut” táblázat egy önmagára hivatkozó future-t ábrázol. A „Pin” feliratú dobozból nyíl indul ki, áthalad a „b1” feliratú dobozon, és a „pinned” dobozon belül, a „fut” táblázatnál végződik." src="img/trpl17-06.svg" class="center" />

<figcaption>17-6. ábra: Egy önmagára hivatkozó future-típusra mutató `Box` pinelése</figcaption>

</figure>

Valójában a `Box` pointer továbbra is szabadon mozoghat. Ne feledd: az számít,
hogy a végső soron hivatkozott adat a helyén maradjon. Ha egy pointer
elmozdul, _de az általa mutatott adat_ ugyanott marad, ahogy a 17-7. ábrán,
akkor nincs lehetséges probléma. (Önálló gyakorlásként nézd meg a típusok, és a
`std::pin` modul dokumentációját, és próbáld kitalálni, hogyan csinálnád ezt egy
`Box`-ot becsomagoló `Pin`-nel.) A lényeg az, hogy maga az önmagára hivatkozó
típus nem mozdulhat el, mert továbbra is pinelve van.

<figure>

<img alt="Négy doboz, nagyjából három oszlopban elrendezve; az előző ábrával azonos, csak a második oszlop változott. Most két doboz van a második oszlopban, „b1” és „b2” felirattal, a „b1” szürkére van halványítva, és a „Pin”-ből induló nyíl a „b1” helyett a „b2”-n halad át; ez azt jelzi, hogy a pointer a „b1”-ből a „b2”-be került, a „pinned” dobozban lévő adat viszont nem mozdult el." src="img/trpl17-07.svg" class="center" />

<figcaption>17-7. ábra: Egy önmagára hivatkozó future-típusra mutató `Box` mozgatása</figcaption>

</figure>

A legtöbb típus azonban teljesen biztonságosan mozgatható, még akkor is, ha
történetesen egy `Pin` pointer mögött van. A pineléssel csak akkor kell
foglalkoznunk, ha az elemeknek belső referenciáik vannak. Az olyan primitív
értékek, mint a számok és a logikai értékek, biztonságosak, mert
nyilvánvalóan nincsenek belső referenciáik. Ahogy a legtöbb típusnak sincsenek,
amellyel a Rustban általában dolgozol. Egy `Vec`-et például aggodalom nélkül
mozgathatsz. Az eddigiek alapján, ha `Pin<Vec<String>>` értéked lenne, mindent a
`Pin` által nyújtott biztonságos, de korlátozó API-kon keresztül kellene
elvégezned, holott egy `Vec<String>` mindig biztonságosan mozgatható, ha nincs
rá más referencia. Kell tehát egy mód arra, hogy megmondjuk a fordítónak: az
ilyen esetekben nyugodtan mozgathatók az elemek – és itt lép színre az `Unpin`.

Az `Unpin` egy jelölő trait, hasonlóan a 16. fejezetben látott `Send` és `Sync`
trait-ekhez, így nincs saját funkcionalitása. A jelölő trait-ek csak arra
szolgálnak, hogy közöljék a fordítóval: biztonságos az adott trait-et
implementáló típust egy bizonyos kontextusban használni. Az `Unpin` azt jelzi a
fordítónak, hogy egy adott típusnak _nem_ kell semmilyen garanciát fenntartania
azzal kapcsolatban, hogy a szóban forgó érték biztonságosan mozgatható-e.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Ahogy a `Send` és a `Sync` esetében, a fordító automatikusan implementálja az
`Unpin`-t minden olyan típusra, amelyről be tudja bizonyítani, hogy
biztonságos. Speciális eset – megint csak a `Send`-hez és a `Sync`-hez
hasonlóan –, amikor az `Unpin` _nincs_ implementálva egy típusra. Ennek a
jelölése <code>impl !Unpin for <em>SomeType</em></code>, ahol a
<code><em>SomeType</em></code> egy olyan típus neve, amelynek _muszáj_
fenntartania ezeket a garanciákat, hogy biztonságos legyen, valahányszor egy rá
mutató pointert `Pin`-ben használnak.

Más szóval két dolgot érdemes észben tartani a `Pin` és az `Unpin`
kapcsolatáról. Először is, az `Unpin` a „normális” eset, a `!Unpin` pedig a
különleges. Másodszor, az, hogy egy típus `Unpin`-t vagy `!Unpin`-t
implementál-e, _csak_ akkor számít, ha az adott típusra mutató pinelt pointert
használsz, például <code>Pin<&mut <em>SomeType</em>></code> alakban.

Hogy kézzelfoghatóbb legyen, gondolj egy `String`-re: van egy hossza, és vannak
az őt alkotó Unicode karakterek. Egy `String`-et becsomagolhatunk `Pin`-be,
ahogy azt a 17-8. ábra mutatja. A `String` azonban automatikusan implementálja
az `Unpin`-t, mint a Rust legtöbb más típusa is.

<figure>

<img alt="Bal oldalon egy „Pin” feliratú doboz, belőle nyíl indul a jobb oldalon lévő „String” feliratú dobozhoz. A „String” doboz tartalmazza az 5usize adatot, amely a sztring hosszát jelöli, valamint a „h”, „e”, „l”, „l” és „o” betűket, amelyek az ebben a String példányban tárolt „hello” sztring karaktereit jelentik. Egy pontozott téglalap veszi körül a „String” dobozt és a feliratát, a „Pin” dobozt viszont nem." src="img/trpl17-08.svg" class="center" />

<figcaption>17-8. ábra: Egy `String` pinelése; a pontozott vonal azt jelzi, hogy a `String` implementálja az `Unpin` trait-et, ezért valójában nincs pinelve</figcaption>

</figure>

Ennek eredményeként olyasmiket is megtehetünk, amelyek tilosak lennének, ha a
`String` ehelyett `!Unpin`-t implementálna – például kicserélhetjük az egyik
sztringet egy másikra pontosan ugyanazon a memóriahelyen, ahogy a 17-9. ábrán
látható. Ez nem sérti a `Pin` szerződését, mert a `String`-nek nincsenek olyan
belső referenciái, amelyek miatt a mozgatása nem lenne biztonságos. Pontosan
ezért implementál `Unpin`-t a `!Unpin` helyett.

<figure>

<img alt="Ugyanaz a „hello” sztringadat, mint az előző példában, most „s1” felirattal és szürkére halványítva. Az előző példa „Pin” doboza most egy másik String példányra mutat, amelynek felirata „s2”, amely érvényes, a hossza 7usize, és a „goodbye” sztring karaktereit tartalmazza. Az s2-t pontozott téglalap veszi körül, mert ő is implementálja az Unpin trait-et." src="img/trpl17-09.svg" class="center" />

<figcaption>17-9. ábra: A `String` lecserélése a memóriában egy teljesen másik `String`-re</figcaption>

</figure>

Most már eleget tudunk ahhoz, hogy megértsük a korábbi, 17-23. listabeli
`join_all` hívásra kapott hibákat. Eredetileg az async blokkok által előállított
future-öket akartuk egy `Vec<Box<dyn Future<Output = ()>>>` típusba mozgatni, de
ahogy láttuk, ezeknek a future-öknek lehetnek belső referenciáik, ezért nem
implementálják automatikusan az `Unpin`-t. Ha egyszer pineltük őket, a kapott
`Pin` típust már betehetjük a `Vec`-be, abban a biztos tudatban, hogy a
future-ökben lévő adatok _nem_ fognak elmozdulni. A 17-24. lista mutatja, hogyan
javíthatjuk a kódot: meghívjuk a `pin!` makrót ott, ahol a három future-t
definiáljuk, és igazítunk a trait objektum típusán.

<Listing number="17-24" caption="A future-ök pinelése, hogy bemozgathatók legyenek a vektorba">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Ez a példa most már lefordul és lefut, és futásidőben hozzáadhatnánk vagy
eltávolíthatnánk future-öket a vektorból, majd az összeset összefűzhetnénk a
join-nal.

A `Pin` és az `Unpin` főként alacsonyabb szintű könyvtárak építésénél fontos,
vagy amikor magát a runtime-ot építed, nem pedig a mindennapi Rust kódban.
Amikor viszont ezekkel a trait-ekkel találkozol hibaüzenetekben, mostantól
jobban tudod, hogyan javítsd a kódodat!

> Megjegyzés: A `Pin` és az `Unpin` együttese teszi lehetővé, hogy a Rustban
> biztonságosan implementálható legyen az összetett típusok egész osztálya,
> amely egyébként nehézséget okozna, mert önmagára hivatkozó. A `Pin`-t igénylő
> típusok ma leginkább az async Rustban bukkannak fel, de időnként más
> kontextusban is találkozhatsz velük.
>
> Annak részleteit, hogy a `Pin` és az `Unpin` hogyan működik, és milyen
> szabályokat kell fenntartaniuk, a `std::pin` API-dokumentációja részletesen
> tárgyalja, így ha többet szeretnél megtudni, ez remek kiindulópont.
>
> Ha még részletesebben szeretnéd megérteni, mi zajlik a motorháztető alatt,
> nézd meg az [_Asynchronous Programming in Rust_][async-book] című könyv
> [2.][under-the-hood]<!-- ignore --> és [4.][pinning]<!-- ignore -->
> fejezetét.

### A `Stream` trait

Most, hogy mélyebben érted a `Future`, a `Pin` és az `Unpin` trait-eket,
fordíthatjuk a figyelmünket a `Stream` trait-re. Ahogy a fejezet korábbi
részéből megtudtad, a stream-ek az aszinkron iterátorokhoz hasonlítanak. Az
`Iterator`-tól és a `Future`-től eltérően azonban a `Stream`-nek e sorok
írásakor nincs definíciója a standard könyvtárban, de _létezik_ a `futures`
crate egy nagyon elterjedt definíciója, amelyet az egész ökoszisztémában
használnak.

Tekintsük át az `Iterator` és a `Future` trait definícióját, mielőtt
megnéznénk, hogyan olvaszthatná őket össze egy `Stream` trait. Az
`Iterator`-tól a sorozat gondolatát kapjuk: a `next` metódusa egy
`Option<Self::Item>` értéket ad. A `Future`-től az idővel bekövetkező készenlét
gondolatát kapjuk: a `poll` metódusa egy `Poll<Self::Output>` értéket ad. Ahhoz,
hogy időben egymás után készre váló elemek sorozatát tudjuk ábrázolni, olyan
`Stream` trait-et definiálunk, amely ezeket a képességeket egyesíti:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

A `Stream` trait definiál egy `Item` nevű asszociált típust a stream által
előállított elemek típusához. Ez hasonlít az `Iterator`-hoz, ahol nulla vagy
több elem lehet, és eltér a `Future`-től, ahol mindig egyetlen `Output` van, még
akkor is, ha az a unit típus, a `()`.

A `Stream` egy metódust is definiál ezeknek az elemeknek a lekérésére. Ezt
`poll_next`-nek hívjuk, hogy világos legyen: ugyanúgy pollozik, ahogy a
`Future::poll`, és ugyanúgy elemek sorozatát állítja elő, ahogy az
`Iterator::next`. A visszatérési típusa a `Poll`-t és az `Option`-t ötvözi. A
külső típus a `Poll`, mert a készenlétét ellenőrizni kell, akárcsak egy
future-nél. A belső típus az `Option`, mert jeleznie kell, van-e még további
üzenet, akárcsak egy iterátornál.

Valami nagyon hasonló ehhez a definícióhoz valószínűleg végül a Rust standard
könyvtárának is része lesz. Addig is a legtöbb runtime eszköztárának része,
tehát számíthatsz rá, és általánosságban minden érvényes lesz, amit a
következőkben tárgyalunk!

A [„Stream-ek: future-ök sorozatban”][streams]<!-- ignore --> szakaszban látott
példákban azonban nem a `poll_next`-et _vagy_ a `Stream`-et használtuk, hanem a
`next`-et és a `StreamExt`-et. Persze dolgozhatnánk közvetlenül a `poll_next`
API-val is, kézzel megírva a saját `Stream` állapotgépeinket, ahogy a
future-ökkel is dolgozhatnánk közvetlenül a `poll` metódusukon keresztül. Az
`await` használata viszont sokkal kellemesebb, és a `StreamExt` trait éppen a
`next` metódust adja hozzá, hogy ezt megtehessük:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Megjegyzés: A fejezet korábbi részében ténylegesen használt definíció kissé
> eltér ettől, mert olyan Rust-verziókat is támogat, amelyek még nem tették
> lehetővé az async függvények használatát trait-ekben. Ennek eredményeként így
> néz ki:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> Ez a `Next` típus egy `struct`, amely implementálja a `Future`-t, és lehetővé
> teszi, hogy a `self`-re mutató referencia lifetime-ját megnevezzük a
> `Next<'_, Self>` alakkal, így az `await` működni tud ezzel a metódussal.

A `StreamExt` trait ad otthont az összes érdekes metódusnak is, amely a
stream-ekkel használható. A `StreamExt` automatikusan implementálva van minden
olyan típusra, amely implementálja a `Stream`-et, de ezek a trait-ek külön
vannak definiálva, hogy a közösség fejleszthesse a kényelmi API-kat anélkül,
hogy ez érintené az alapvető trait-et.

A `StreamExt` `trpl` crate-ben használt verziójában a trait nemcsak a `next`
metódust definiálja, hanem alapértelmezett implementációt is ad hozzá, amely
helyesen kezeli a `Stream::poll_next` hívásának részleteit. Ez azt jelenti, hogy
még ha saját stream jellegű adattípust kell is írnod, _csak_ a `Stream`-et kell
implementálnod, és onnantól bárki, aki használja az adattípusodat,
automatikusan használhatja hozzá a `StreamExt`-et és annak metódusait.

Ennyit szerettünk volna elmondani ezeknek a trait-eknek az alacsonyabb szintű
részleteiről. Zárásként nézzük meg, hogyan illeszkednek egymáshoz a future-ök
(beleértve a stream-eket), a taskok és a szálak!

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html
