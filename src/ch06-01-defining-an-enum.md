## Enum definiálása

Míg a struct-ok arra adnak módot, hogy összetartozó mezőket és adatokat fogj
egybe – például egy `Rectangle`-t a `width` és `height` mezőjével –, az enumok
arra, hogy kimondd: egy érték a lehetséges értékek egy halmazának valamelyik
eleme. Például mondhatjuk, hogy a `Rectangle` a lehetséges alakzatok egyike,
amelyek közé a `Circle` és a `Triangle` is tartozik. Ehhez a Rust lehetővé
teszi, hogy ezeket a lehetőségeket enumként kódoljuk.

Nézzünk meg egy olyan helyzetet, amelyet kódban szeretnénk kifejezni, és lássuk,
miért hasznosak az enumok, és miért illenek ide jobban a struct-oknál. Tegyük
fel, hogy IP-címekkel kell dolgoznunk. Jelenleg két fő szabvány használatos az
IP-címekre: a négyes és a hatos verzió. Mivel a programunk számára ez az összes
lehetőség egy IP-cím esetén, _felsorolhatjuk_ az összes lehetséges változatot –
innen kapta a nevét a felsorolt típus.

Bármely IP-cím lehet négyes vagy hatos verziójú cím, de nem lehet egyszerre
mindkettő. Az IP-címeknek ez a tulajdonsága teszi megfelelővé az enum
adatszerkezetet, mert egy enum értéke csak az egyik változata lehet. A négyes és
a hatos verziójú címek egyaránt alapvetően IP-címek, ezért ugyanolyan típusként
kell kezelni őket, amikor a kód bármilyen IP-címre vonatkozó helyzeteket kezel.

Ezt a fogalmat kódban úgy fejezhetjük ki, hogy definiálunk egy `IpAddrKind`
felsorolt típust, és felsoroljuk, milyen fajta lehet egy IP-cím: `V4` és `V6`.
Ezek az enum változatai:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

Az `IpAddrKind` mostantól egy saját adattípus, amelyet a kódunk más részein is
használhatunk.

### Enum értékek {#enum-values}

Az `IpAddrKind` két változatának példányait így hozhatjuk létre:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Vedd észre, hogy az enum változatai az enum azonosítója alatti névtérben
vannak, és a kettőt kettős kettőspont választja el. Ez azért hasznos, mert így
az `IpAddrKind::V4` és az `IpAddrKind::V6` érték egyaránt ugyanolyan típusú:
`IpAddrKind`. Ezután például definiálhatunk egy függvényt, amely bármilyen
`IpAddrKind`-ot átvesz:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

És ezt a függvényt bármelyik változattal meghívhatjuk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Az enumok használatának még több előnye van. Ha jobban belegondolunk az
IP-cím-típusunkba, jelenleg nincs módunk tárolni a tényleges IP-cím _adatot_;
csak azt tudjuk, milyen _fajtájú_. Mivel az imént tanultál a struct-okról az 5.
fejezetben, talán kísértést éreznél, hogy struct-okkal old meg ezt a problémát,
ahogy a 6-1. listában látható.

<Listing number="6-1" caption="Egy IP-cím adatának és `IpAddrKind` változatának tárolása `struct` segítségével">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Itt definiáltunk egy `IpAddr` struct-ot, amelynek két mezője van: egy
`IpAddrKind` típusú `kind` mező (a korábban definiált enum) és egy `String`
típusú `address` mező. Ebből a struct-ból két példányunk van. Az első a `home`,
amelynek `kind` mezője az `IpAddrKind::V4` értéket veszi fel, a hozzá tartozó
címadat pedig `127.0.0.1`. A második példány a `loopback`. Ennek `kind` értéke
az `IpAddrKind` másik változata, a `V6`, a hozzá tartozó cím pedig `::1`. A
struct-tal fogtuk össze a `kind` és az `address` értéket, így a változat most
már az értékhez tartozik.

Az alábbi ábra megmutatja, hogyan néz ki ez a memóriában. Mindkét példány a
stack-en tárolja a `kind` mező változatát és az `address` mező `String`
fejét, a cím szövege pedig a heap-en van:

```aquascope,interpreter
#fn main() {
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

let home = IpAddr {
    kind: IpAddrKind::V4,
    address: String::from("127.0.0.1"),
};

let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
};`[]`
#}
```

Ugyanezt a fogalmat azonban tömörebben fejezhetjük ki pusztán egy enummal: a
struct-ba ágyazott enum helyett az adatokat közvetlenül az egyes enum
változatokba tehetjük. Az `IpAddr` enum új definíciója azt mondja ki, hogy a
`V4` és a `V6` változathoz egyaránt `String` érték tartozik:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Az adatot közvetlenül az enum egyes változataihoz kapcsoljuk, így nincs szükség
külön struct-ra. Itt egy másik részlet is jobban látszik abból, hogyan működnek
az enumok: minden általunk definiált enum változat neve egyben olyan függvény
is lesz, amely az enum egy példányát állítja elő. Vagyis az `IpAddr::V4()` egy
függvényhívás, amely egy `String` argumentumot vesz át, és az `IpAddr` típus
egy példányát adja vissza. Ezt a konstruktorfüggvényt automatikusan megkapjuk
az enum definiálásának eredményeként.

Vesd össze a memóriaképet az előzővel: a külön struct eltűnt, a `String`
közvetlenül az enum változatában ül, a heap-en lévő adat viszont ugyanaz
maradt:

```aquascope,interpreter
#fn main() {
enum IpAddr {
    V4(String),
    V6(String),
}

let home = IpAddr::V4(String::from("127.0.0.1"));

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}
```

Az enum struct helyetti használatának van még egy előnye: minden változathoz
eltérő típusú és mennyiségű adat tartozhat. A négyes verziójú IP-címek mindig
négy számkomponensből állnak, amelyek értéke 0 és 255 közötti. Ha a `V4`
címeket négy `u8` értékként akarnánk tárolni, de a `V6` címeket továbbra is egy
`String` értékként kifejezni, ezt struct-tal nem tudnánk megtenni. Az enumok
könnyedén kezelik ezt az esetet:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Az ábrán jól látszik, hogy a két változat egészen mást tárol: a `V4` négy `u8`
értéket tart közvetlenül magában, a `V6` pedig egy `String`-et, amelynek a
tartalma a heap-re kerül:

```aquascope,interpreter
#fn main() {
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}
```

Többféle módot is bemutattunk arra, hogyan definiálhatunk adatszerkezeteket a
négyes és hatos verziójú IP-címek tárolására. Mint kiderül, azonban annyira
gyakori igény az IP-címek tárolása és annak jelzése, hogy melyik fajtáról van
szó, hogy [a standard könyvtárban van egy definíció, amelyet
használhatunk!][IpAddr]<!-- ignore --> Nézzük meg, hogyan definiálja a standard
könyvtár az `IpAddr`-t. Pontosan azt az enumot és azokat a változatokat
tartalmazza, amelyeket mi is definiáltunk és használtunk, de a címadatot két
különböző struct formájában ágyazza a változatokba, amelyeket változatonként
eltérően definiál:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Ez a kód azt szemlélteti, hogy bármilyen adatot betehetsz egy enum változatba:
például sztringeket, numerikus típusokat vagy struct-okat. Akár egy másik
enumot is beletehetsz! Ráadásul a standard könyvtár típusai gyakran nem sokkal
bonyolultabbak annál, mint amit magad is kitalálnál.

Vedd észre, hogy bár a standard könyvtár tartalmaz egy `IpAddr` definíciót,
ütközés nélkül létrehozhatjuk és használhatjuk a sajátunkat, mert nem hoztuk be
a standard könyvtár definícióját a hatókörünkbe. A típusok hatókörbe hozásáról
bővebben a 7. fejezetben lesz szó.

Nézzünk meg egy másik enum példát a 6-2. listában: ennek a változataiba
sokféle típus van beágyazva.

<Listing number="6-2" caption="Egy `Message` enum, amelynek változatai eltérő mennyiségű és típusú értéket tárolnak">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Ennek az enumnak négy változata van, különböző típusokkal:

- `Quit`: egyáltalán nem tartozik hozzá adat
- `Move`: névvel ellátott mezői vannak, akárcsak egy struct-nak
- `Write`: egyetlen `String`-et tartalmaz
- `ChangeColor`: három `i32` értéket tartalmaz

Az alábbi ábrán mind a négy változatból létrehozunk egy-egy értéket. Mindegyik
`Message` típusú, a memóriában viszont más és más adatot hordoznak: csak a
`Write` változat sztringjének tartalma kerül a heap-re:

```aquascope,interpreter
#fn main() {
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

let quit = Message::Quit;
let movement = Message::Move { x: 1, y: 2 };
let write = Message::Write(String::from("hello"));
let color = Message::ChangeColor(0, 160, 255);`[]`
#}
```

Egy olyan enum definiálása, amelynek a 6-2. listában láthatókhoz hasonló
változatai vannak, hasonlít különféle struct-definíciók megadásához, azzal a
különbséggel, hogy az enum nem használja a `struct` kulcsszót, és az összes
változat egyetlen `Message` típus alá van csoportosítva. A következő struct-ok
ugyanazokat az adatokat tárolhatnák, mint a fenti enum változatai:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Ha viszont a különböző struct-okat használnánk, amelyek mindegyike saját
típusú, nem tudnánk olyan könnyen definiálni egy függvényt, amely bármelyik
fajta üzenetet átveszi, mint a 6-2. listában definiált `Message` enummal, amely
egyetlen típus.

Van még egy hasonlóság az enumok és a struct-ok között: ahogy `impl`
segítségével metódusokat definiálhatunk struct-okon, ugyanúgy definiálhatunk
metódusokat enumokon is. Íme egy `call` nevű metódus, amelyet a `Message`
enumunkon definiálhatnánk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

A metódus törzse a `self`-fel érné el azt az értéket, amelyen a metódust
meghívtuk. Ebben a példában létrehoztunk egy `m` változót, amelynek értéke
`Message::Write(String::from("hello"))`, és ez lesz a `self` a `call` metódus
törzsében, amikor az `m.call()` lefut.

Nézzünk meg egy másik, nagyon gyakori és hasznos enumot a standard könyvtárból:
az `Option`-t.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Az `Option` enum

Ez a szakasz az `Option` esettanulmányát járja körül, amely egy másik, a
standard könyvtár által definiált enum. Az `Option` típus azt a nagyon gyakori
helyzetet kódolja, amikor egy érték lehet valami, de lehet semmi is.

Ha például egy nem üres lista első elemét kéred le, kapsz egy értéket. Ha egy
üres lista első elemét kéred le, semmit sem kapsz. Ha ezt a fogalmat a
típusrendszer nyelvén fejezzük ki, a fordító ellenőrizni tudja, hogy minden
kezelendő esetet lekezeltél-e; ez a képesség megelőzhet olyan hibákat, amelyek
más programozási nyelvekben rendkívül gyakoriak.

A programozási nyelvek tervezéséről gyakran abban a keretben gondolkodunk, hogy
milyen képességeket veszünk bele, pedig a kihagyott képességek is fontosak. A
Rustban nincs meg a null, amely sok más nyelvben megvan. A _null_ olyan érték,
amely azt jelenti, hogy nincs ott érték. A nullt ismerő nyelvekben a változók
mindig két állapot egyikében vannak: null vagy nem null.

Tony Hoare, a null feltalálója 2009-es „Null References: The Billion Dollar
Mistake” című előadásában ezt mondta:

> Milliárd dolláros hibámnak nevezem. Akkoriban az első átfogó típusrendszert
> terveztem referenciákhoz egy objektumorientált nyelvben. A célom az volt, hogy
> a referenciák minden használata teljesen biztonságos legyen, és az
> ellenőrzést a fordító automatikusan végezze el. De nem tudtam ellenállni a
> kísértésnek, hogy bevezessem a null referenciát, egyszerűen azért, mert olyan
> könnyű volt implementálni. Ez megszámlálhatatlan hibához, sebezhetőséghez és
> rendszerösszeomláshoz vezetett, ami az elmúlt negyven évben valószínűleg
> milliárd dollárnyi fájdalmat és kárt okozott.

A null értékekkel az a baj, hogy ha egy null értéket nem null értékként
próbálsz használni, valamilyen hibát kapsz. Mivel ez a null vagy nem null
tulajdonság mindent áthat, rendkívül könnyű elkövetni ezt a fajta hibát.

Az a fogalom azonban, amelyet a null kifejezni próbál, továbbra is hasznos: a
null olyan érték, amely valamilyen okból jelenleg érvénytelen vagy hiányzik.

A probléma valójában nem a fogalommal van, hanem az adott implementációval. A
Rustban ezért nincs null, viszont van egy enum, amely képes kódolni azt a
fogalmat, hogy egy érték jelen van-e vagy hiányzik. Ez az enum az `Option<T>`,
és a [standard könyvtár így definiálja][option]<!-- ignore -->:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Az `Option<T>` enum annyira hasznos, hogy még a prelude része is; nem kell
kifejezetten hatókörbe hoznod. A változatai is részei a prelude-nak: a `Some`-ot
és a `None`-t közvetlenül, az `Option::` előtag nélkül használhatod. Az
`Option<T>` ettől még ugyanolyan hétköznapi enum, a `Some(T)` és a `None` pedig
továbbra is az `Option<T>` típus változatai.

A `<T>` szintaxis a Rust olyan képessége, amelyről még nem beszéltünk. Ez egy
generikus típusparaméter, a generikusokkal pedig részletesebben a 10.
fejezetben foglalkozunk. Egyelőre csak annyit kell tudnod, hogy a `<T>` azt
jelenti: az `Option` enum `Some` változata egyetlen, tetszőleges típusú
adatdarabot tarthat, és minden konkrét típus, amely a `T` helyére kerül, más és
más `Option<T>` típust eredményez. Íme néhány példa arra, hogyan tárolhatunk
`Option` értékekkel számtípusokat és `char` típusokat:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Az ábra megmutatja, mi kerül ilyenkor a memóriába: a `Some` változat magában
hordozza a benne tárolt értéket, az `absent_number` `None` változatához pedig
egyáltalán nem tartozik adat:

```aquascope,interpreter
#fn main() {
let some_number = Some(5);
let some_char = Some('e');

let absent_number: Option<i32> = None;`[]`
#}
```

A `some_number` típusa `Option<i32>`. A `some_char` típusa `Option<char>`, ami
másik típus. A Rust ki tudja következtetni ezeket a típusokat, mert a `Some`
változaton belül megadtunk egy értéket. Az `absent_number` esetében a Rust
megköveteli, hogy megadjuk a teljes `Option` típust: a fordító pusztán egy
`None` értéket nézve nem tudja kikövetkeztetni, milyen típust tartana a
megfelelő `Some` változat. Itt megmondjuk a Rustnak, hogy az `absent_number`
típusa `Option<i32>` legyen.

Ha van egy `Some` értékünk, tudjuk, hogy van érték, és az érték a `Some`-on
belül van. Ha `None` értékünk van, az bizonyos értelemben ugyanazt jelenti, mint
a null: nincs érvényes értékünk. Miért jobb akkor az `Option<T>`, mint a null?

Röviden azért, mert az `Option<T>` és a `T` (ahol a `T` bármilyen típus lehet)
különböző típusok, ezért a fordító nem engedi, hogy egy `Option<T>` értéket úgy
használjunk, mintha biztosan érvényes érték lenne. Például ez a kód nem fordul
le, mert egy `i8`-at próbál hozzáadni egy `Option<i8>`-hoz:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Ha lefuttatjuk ezt a kódot, ehhez hasonló hibaüzenetet kapunk:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Kemény! Ez a hibaüzenet lényegében azt jelenti, hogy a Rust nem tudja, hogyan
adjon össze egy `i8`-at és egy `Option<i8>`-at, mert különböző típusok. Amikor
a Rustban van egy `i8`-hoz hasonló típusú értékünk, a fordító biztosítja, hogy
mindig érvényes értékünk legyen. Magabiztosan haladhatunk tovább anélkül, hogy
az érték használata előtt nullra kellene ellenőriznünk. Csak akkor kell
aggódnunk amiatt, hogy esetleg nincs értékünk, ha `Option<i8>` (vagy bármilyen
más olyan típusú) értékkel dolgozunk, és a fordító gondoskodik róla, hogy az
érték használata előtt lekezeljük ezt az esetet.

Más szóval egy `Option<T>`-t `T`-vé kell alakítanod, mielőtt `T`-műveleteket
végezhetnél vele. Ez általában segít elkapni a null egyik leggyakoribb
problémáját: azt a feltételezést, hogy valami nem null, pedig valójában az.

Ha kiiktatjuk annak kockázatát, hogy tévesen nem null értéket feltételezünk,
magabiztosabbak lehetünk a kódunkban. Ahhoz, hogy egy érték esetleg null
lehessen, kifejezetten kérned kell ezt azzal, hogy az érték típusa `Option<T>`
lesz. Ezután, amikor használod azt az értéket, kötelező kifejezetten lekezelned
azt az esetet, amikor az érték null. Minden olyan helyen, ahol egy érték típusa
nem `Option<T>`, nyugodtan feltételezheted, hogy az érték nem null. Ez a Rust
tudatos tervezési döntése volt, hogy korlátozza a null mindent átható jelenlétét
és növelje a Rust kód biztonságát.

Hogyan szedjük ki tehát a `T` értéket egy `Some` változatból, ha `Option<T>`
típusú értékünk van, hogy használhassuk azt az értéket? Az `Option<T>` enumnak
rengeteg metódusa van, amelyek sokféle helyzetben hasznosak; ezeket [a
dokumentációjában][docs]<!-- ignore --> nézheted meg. Ha megismerkedsz az
`Option<T>` metódusaival, az rendkívül hasznos lesz a Rusttal töltött utad
során.

Általánosságban egy `Option<T>` érték használatához olyan kódra van szükség,
amely minden változatot lekezel. Kell valamennyi kód, amely csak akkor fut le,
ha `Some(T)` értékünk van, és ez a kód használhatja a benne lévő `T`-t. Kell
egy másik kódrészlet, amely csak akkor fut le, ha `None` értékünk van, és ennek
a kódnak nem áll rendelkezésére `T` érték. A `match` kifejezés olyan
vezérlésiszerkezet-elem, amely enumokkal használva pontosan ezt teszi: attól
függően futtat különböző kódot, hogy az enum melyik változata van nála, és ez a
kód használhatja az illeszkedő értékben lévő adatokat.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
