## Egyszálú webszerver építése

Kezdjük azzal, hogy működésre bírunk egy egyszálú webszervert. Mielőtt
belefognánk, nézzünk egy gyors áttekintést a webszerverek építésében szerepet
játszó protokollokról. E protokollok részletei túlmutatnak a könyv keretein, de
egy rövid áttekintés megadja a szükséges információkat.

A webszerverekben szerepet játszó két fő protokoll a _Hypertext Transfer
Protocol_ _(HTTP)_ és a _Transmission Control Protocol_ _(TCP)_. Mindkettő
_kérés-válasz_ (request-response) protokoll, vagyis egy _kliens_ kéréseket
kezdeményez, a _szerver_ pedig figyeli a kéréseket, és választ ad a kliensnek.
E kérések és válaszok tartalmát a protokollok határozzák meg.

A TCP az alacsonyabb szintű protokoll, amely leírja, hogyan jut el az
információ az egyik szerverről a másikra, de azt nem határozza meg, hogy mi ez
az információ. A HTTP a TCP-re épül, és a kérések és válaszok tartalmát
definiálja. Technikailag lehetséges a HTTP-t más protokollokkal is használni,
de az esetek túlnyomó többségében a HTTP TCP-n keresztül küldi az adatait. Mi a
TCP- és HTTP-kérések és -válaszok nyers bájtjaival fogunk dolgozni.

### A TCP-kapcsolat figyelése

A webszerverünknek figyelnie kell egy TCP-kapcsolatot, tehát ezzel a résszel
kezdjük. A standard könyvtár erre a `std::net` modult kínálja. Hozzunk létre a
szokásos módon egy új projektet:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Most kezdésként írd be a 21-1. listában látható kódot a _src/main.rs_ fájlba.
Ez a kód a helyi `127.0.0.1:7878` címen figyeli a beérkező TCP-stream-eket. Ha
beérkező streamet kap, kiírja a `Connection established!` üzenetet.

<Listing number="21-1" file-name="src/main.rs" caption="Beérkező stream-ek figyelése és üzenet kiírása, amikor streamet kapunk">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

A `TcpListener` segítségével a `127.0.0.1:7878` címen tudjuk figyelni a
TCP-kapcsolatokat. A címben a kettőspont előtti rész egy IP-cím, amely a saját
gépedet jelöli (ez minden gépen ugyanaz, és nem konkrétan a szerzők gépét
jelenti), a `7878` pedig a port. Ezt a portot két okból választottuk: a HTTP-t
általában nem ezen a porton fogadják, így a szerverünk vélhetően nem ütközik
más, a gépeden esetleg futó webszerverrel, ráadásul a 7878 a _rust_ szó
begépelve egy telefonon.

A `bind` függvény ebben a helyzetben úgy működik, mint a `new` függvény: új
`TcpListener` példányt ad vissza. A függvény neve azért `bind`, mert a
hálózatkezelésben azt, hogy egy porthoz kapcsolódunk figyelés céljából,
„porthoz kötésnek” (binding to a port) nevezik.

A `bind` függvény `Result<T, E>` értéket ad vissza, ami jelzi, hogy a kötés
meghiúsulhat, például ha a programunk két példányát futtatnánk, és így két
program figyelné ugyanazt a portot. Mivel csak tanulási célból írunk egy
egyszerű szervert, most nem foglalkozunk az ilyen hibák kezelésével; helyette
`unwrap`-pel állítjuk le a programot, ha hiba történik.

A `TcpListener` `incoming` metódusa olyan iterátort ad vissza, amely stream-ek
sorozatát adja nekünk (pontosabban `TcpStream` típusú stream-eket). Egyetlen
_stream_ egy nyitott kapcsolatot jelöl a kliens és a szerver között. A
_kapcsolat_ (connection) a teljes kérés-válasz folyamat neve, amelyben a kliens
csatlakozik a szerverhez, a szerver választ állít elő, majd lezárja a
kapcsolatot. Ennek megfelelően a `TcpStream`-ből olvassuk ki, mit küldött a
kliens, majd a válaszunkat a streambe írjuk, hogy adatot küldjünk vissza a
kliensnek. Összességében ez a `for` ciklus egymás után dolgozza fel a
kapcsolatokat, és stream-ek sorozatát adja a kezünkbe.

Egyelőre a stream kezelése annyiból áll, hogy `unwrap`-et hívunk, ami leállítja
a programunkat, ha a streamnek bármilyen hibája van; ha nincs hiba, a program
kiír egy üzenetet. A sikeres esethez a következő listában adunk további
funkcionalitást. Azért kaphatunk hibát az `incoming` metódustól, amikor egy
kliens csatlakozik a szerverhez, mert valójában nem kapcsolatokon iterálunk,
hanem _kapcsolódási kísérleteken_. A kapcsolat több okból is meghiúsulhat, és
ezek közül sok operációs rendszer specifikus. Sok operációs rendszerben például
korlátozott az egyszerre nyitva tartható kapcsolatok száma; az ezen felüli új
kapcsolódási kísérletek hibát okoznak, amíg néhány nyitott kapcsolat le nem
zárul.

Próbáljuk ki ezt a kódot! Add ki a `cargo run` parancsot a terminálban, majd
töltsd be a _127.0.0.1:7878_ címet egy böngészőben. A böngészőnek valamilyen
hibaüzenetet kell mutatnia, például „Connection reset”, mert a szerver
pillanatnyilag semmilyen adatot nem küld vissza. Ha viszont a terminálra nézel,
több üzenetet is látnod kell, amelyek akkor íródtak ki, amikor a böngésző
csatlakozott a szerverhez!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Néha egyetlen böngészőkérésre több üzenet is kiíródik; ennek oka lehet, hogy a
böngésző az oldalra vonatkozó kérés mellett más erőforrásokat is kér, például a
böngészőfülön megjelenő _favicon.ico_ ikont.

Az is előfordulhat, hogy a böngésző többször próbál csatlakozni a szerverhez,
mert a szerver nem válaszol semmilyen adattal. Amikor a `stream` kikerül a
hatóköréből, és a ciklus végén eldobódik, a kapcsolat a `drop` implementáció
részeként lezárul. A böngészők a lezárt kapcsolatokat néha újrapróbálkozással
kezelik, mert a probléma átmeneti is lehet.

A böngészők időnként több kapcsolatot is nyitnak a szerverhez anélkül, hogy
kéréseket küldenének, hogy ha *tényleg* küldenek később kéréseket, azok
gyorsabban mehessenek végbe. Ilyenkor a szerverünk minden kapcsolatot lát,
függetlenül attól, hogy érkezik-e kérés azon a kapcsolaton. Sok Chrome-alapú
böngésző verziója csinálja ezt például; ezt az optimalizációt privát böngészési
móddal vagy másik böngésző használatával kapcsolhatod ki.

A lényeg az, hogy sikeresen hozzájutottunk egy TCP-kapcsolat kezelőjéhez!

Ne feledd leállítani a programot a <kbd>ctrl</kbd>-<kbd>C</kbd> lenyomásával,
amikor végeztél a kód egy adott változatának futtatásával. Ezután a `cargo run`
paranccsal indítsd újra a programot minden kódmódosítás után, hogy biztosan a
legfrissebb kód fusson.

### A kérés beolvasása

Implementáljuk azt a funkciót, amely beolvassa a böngésző kérését! Hogy
szétválasszuk a kapcsolat felvételét attól, hogy utána kezdünk is valamit a
kapcsolattal, új függvényt indítunk a kapcsolatok feldolgozására. Ebben az új
`handle_connection` függvényben adatot olvasunk a TCP streamből, és kiírjuk,
hogy lássuk, mit küld a böngésző. Módosítsd a kódot úgy, hogy a 21-2. listára
hasonlítson.

<Listing number="21-2" file-name="src/main.rs" caption="Olvasás a `TcpStream`-ből és az adat kiírása">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Behozzuk a hatókörbe a `std::io::BufReader` és a `std::io::prelude` elemeit,
hogy hozzáférjünk azokhoz a trait-ekhez és típusokhoz, amelyekkel olvasni és
írni tudunk a streamből, illetve a streambe. A `main` függvény `for`
ciklusában ahelyett, hogy kiírnánk egy üzenetet a kapcsolat létrejöttéről, most
meghívjuk az új `handle_connection` függvényt, és átadjuk neki a `stream`-et.

A `handle_connection` függvényben létrehozunk egy új `BufReader` példányt,
amely a `stream`-re mutató referenciát csomagolja be. A `BufReader`
pufferelést ad hozzá azzal, hogy helyettünk kezeli a `std::io::Read` trait
metódusainak hívásait.

Létrehozunk egy `http_request` nevű változót, amelybe összegyűjtjük a
böngészőtől a szerverünkhöz érkező kérés sorait. A `Vec<_>` típusannotációval
jelezzük, hogy ezeket a sorokat egy vektorba szeretnénk gyűjteni.

A `BufReader` implementálja a `std::io::BufRead` trait-et, amely a `lines`
metódust nyújtja. A `lines` metódus `Result<String, std::io::Error>` értékek
iterátorát adja vissza úgy, hogy minden újsor bájtnál felosztja az adatfolyamot.
Ahhoz, hogy megkapjuk az egyes `String`-eket, `map`-eljük és `unwrap`-eljük az
egyes `Result`-okat. A `Result` hibát is tartalmazhat, ha az adat nem érvényes
UTF-8, vagy ha probléma adódott a streamből való olvasás során. Egy éles
programnak megint csak elegánsabban kellene kezelnie ezeket a hibákat, mi
viszont az egyszerűség kedvéért a hiba esetén leállítjuk a programot.

A böngésző két egymást követő újsorkarakterrel jelzi a HTTP-kérés végét, ezért
hogy egy kérést kapjunk a streamből, addig vesszük ki a sorokat, amíg üres
sztringet nem kapunk. Miután a sorokat összegyűjtöttük a vektorba, szépített
debug formázással kiírjuk őket, hogy megnézhessük, milyen utasításokat küld a
böngésző a szerverünknek.

Próbáljuk ki ezt a kódot! Indítsd el a programot, és küldj újra egy kérést a
böngészőből. Vedd észre, hogy a böngészőben továbbra is hibaoldalt kapunk, de a
programunk kimenete a terminálban most már valahogy így fog kinézni:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

A böngésződtől függően kicsit eltérő kimenetet kaphatsz. Most, hogy kiírjuk a
kérés adatait, a kérés első sorában a `GET` utáni útvonalat megnézve azt is
láthatjuk, miért kapunk egyetlen böngészőkérésből több kapcsolatot. Ha az
ismétlődő kapcsolatok mind a _/_ útvonalat kérik, akkor tudjuk, hogy a böngésző
azért próbálja újra és újra lekérni a _/_ címet, mert nem kap választ a
programunktól.

Bontsuk szét ezeket a kérésadatokat, hogy megértsük, mit kér a böngésző a
programunktól.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Nézzük meg közelebbről a HTTP-kérést

A HTTP szöveges alapú protokoll, és egy kérés a következő formátumú:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Az első sor a _kéréssor_ (request line), amely azt tartalmazza, hogy mit kér a
kliens. A kéréssor első része a használt metódust jelöli, például `GET` vagy
`POST`, amely leírja, hogyan intézi a kliens a kérést. A mi kliensünk `GET`
kérést használt, ami azt jelenti, hogy információt kér.

A kéréssor következő része a _/_, amely azt az _uniform resource identifier_
_(URI)_ értéket adja meg, amelyet a kliens kér: az URI majdnem, de nem
teljesen ugyanaz, mint az _uniform resource locator_ _(URL)_. Az URI-k és az
URL-ek közti különbség ebben a fejezetben nem számít nekünk, de a HTTP
specifikáció az _URI_ kifejezést használja, így itt gondolatban nyugodtan
behelyettesíthetjük az _URL_-t az _URI_ helyére.

Az utolsó rész a kliens által használt HTTP-verzió, majd a kéréssor egy CRLF
szekvenciával zárul. (A _CRLF_ a _carriage return_ és a _line feed_
rövidítése, ezek még az írógépek korából származó kifejezések!) A CRLF
szekvencia `\r\n` alakban is írható, ahol a `\r` a kocsivissza, a `\n` pedig a
soremelés. A _CRLF szekvencia_ választja el a kéréssort a kérés többi
adatától. Vedd észre, hogy amikor a CRLF kiíródik, `\r\n` helyett egy új sor
kezdetét látjuk.

Ha megnézzük a kéréssor adatait, amelyeket a programunk eddigi futtatásából
kaptunk, azt látjuk, hogy a metódus a `GET`, a kért URI a _/_, a verzió pedig a
`HTTP/1.1`.

A kéréssor után a `Host:`-tól kezdődő további sorok fejlécek. A `GET`
kéréseknek nincs törzsük.

Próbálj kérést küldeni egy másik böngészőből, vagy kérj le egy másik címet,
például a _127.0.0.1:7878/test_ címet, hogy lásd, hogyan változnak a kérés
adatai.

Most, hogy tudjuk, mit kér a böngésző, küldjünk vissza némi adatot!

### Válasz írása

Most azt implementáljuk, hogy adatot küldjünk válaszul a kliens kérésére. A
válaszok formátuma a következő:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Az első sor az _állapotsor_ (status line), amely a válaszban használt
HTTP-verziót, a kérés eredményét összefoglaló numerikus állapotkódot, valamint
egy indoklást tartalmaz, amely szövegesen írja le az állapotkódot. A CRLF
szekvencia után jönnek az esetleges fejlécek, majd egy újabb CRLF szekvencia és
a válasz törzse.

Íme egy példa válasz, amely az 1.1-es HTTP-verziót használja, állapotkódja 200,
az indoklása OK, nincsenek fejlécei és nincs törzse:

```text
HTTP/1.1 200 OK\r\n\r\n
```

A 200-as állapotkód a szabványos sikerválasz. Ez a szöveg egy pici sikeres
HTTP-válasz. Írjuk ki ezt a streambe a sikeres kérésre adott válaszunkként! A
`handle_connection` függvényből távolítsd el a `println!`-t, amely a kérés
adatait írta ki, és cseréld le a 21-3. listában látható kódra.

<Listing number="21-3" file-name="src/main.rs" caption="Pici sikeres HTTP-válasz írása a streambe">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Az első új sor definiálja a `response` változót, amely a sikerüzenet adatait
tartalmazza. Ezután `as_bytes`-t hívunk a `response`-on, hogy a sztringadatokat
bájtokká alakítsuk. A `stream` `write_all` metódusa `&[u8]` értéket vár, és
ezeket a bájtokat közvetlenül a kapcsolatba küldi. Mivel a `write_all` művelet
meghiúsulhat, mint korábban, `unwrap`-et használunk bármilyen hibaeredményre.
Egy valódi alkalmazásban itt megint csak hibakezelést kellene beépítened.

Ezekkel a változtatásokkal futtassuk a kódunkat, és küldjünk egy kérést. Már
nem írunk ki adatot a terminálra, így a Cargo kimenetén kívül semmilyen
kimenetet nem fogunk látni. Ha betöltöd a _127.0.0.1:7878_ címet egy
böngészőben, hibaüzenet helyett üres oldalt kell kapnod. Épp most kódoltad le
kézzel egy HTTP-kérés fogadását és egy válasz elküldését!

### Valódi HTML visszaadása

Implementáljuk azt a funkciót, hogy ne csak egy üres oldalt adjunk vissza. Hozd
létre az új _hello.html_ fájlt a projektkönyvtárad gyökerében, ne a _src_
könyvtárban. Bármilyen HTML-t megadhatsz benne; a 21-4. lista egy lehetséges
változatot mutat.

<Listing number="21-4" file-name="hello.html" caption="Példa HTML-fájl, amelyet válaszként adunk vissza">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Ez egy minimális HTML5 dokumentum egy címsorral és némi szöveggel. Ahhoz, hogy
a szerver ezt adja vissza, amikor kérés érkezik, a 21-5. listában látható módon
módosítjuk a `handle_connection` függvényt, hogy beolvassa a HTML-fájlt,
hozzáadja a válasz törzseként, és elküldje.

<Listing number="21-5" file-name="src/main.rs" caption="A *hello.html* tartalmának elküldése a válasz törzseként">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

A `use` utasításhoz hozzáadtuk az `fs`-t, hogy a standard könyvtár
fájlrendszer-modulját behozzuk a hatókörbe. Egy fájl tartalmának sztringbe
olvasásának kódja ismerős lehet; ezt használtuk, amikor az I/O projektünkben
beolvastuk egy fájl tartalmát a 12-4. listában.

Ezután a `format!` makróval a fájl tartalmát a sikerválasz törzseként adjuk
hozzá. Az érvényes HTTP-válasz érdekében hozzáadjuk a `Content-Length`
fejlécet, amelynek értéke a válasz törzsének mérete – ebben az esetben a
`hello.html` mérete.

Futtasd ezt a kódot `cargo run` paranccsal, és töltsd be a _127.0.0.1:7878_
címet a böngésződben; látnod kell a megjelenített HTML-t!

Jelenleg figyelmen kívül hagyjuk a kérés `http_request`-ben lévő adatait, és
feltétel nélkül visszaküldjük a HTML-fájl tartalmát. Ez azt jelenti, hogy ha a
böngésződben a _127.0.0.1:7878/valami-mas_ címet kéred le, ugyanezt a
HTML-választ kapod vissza. A szerverünk pillanatnyilag nagyon korlátozott, és
nem azt csinálja, amit a legtöbb webszerver. Azt szeretnénk, hogy a válaszaink
a kéréstől függjenek, és csak a _/_ útvonalra irányuló, jól formált kérésre
küldjük vissza a HTML-fájlt.

### A kérés ellenőrzése és szelektív válasz

Jelenleg a webszerverünk visszaadja a fájlban lévő HTML-t, akármit is kért a
kliens. Építsük be azt a funkciót, hogy a HTML-fájl visszaadása előtt
ellenőrizzük, hogy a böngésző a _/_ útvonalat kéri-e, és hibát adjunk vissza,
ha a böngésző bármi mást kér. Ehhez módosítanunk kell a `handle_connection`
függvényt a 21-6. listában látható módon. Ez az új kód összeveti a kapott kérés
tartalmát azzal, amiről tudjuk, hogyan néz ki egy _/_ útvonalra irányuló kérés,
és `if`, illetve `else` blokkokat ad hozzá, hogy különbözőképpen kezelje a
kéréseket.

<Listing number="21-6" file-name="src/main.rs" caption="A */* útvonalra irányuló kérések eltérő kezelése a többi kéréstől">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Csak a HTTP-kérés első sorát fogjuk megnézni, ezért ahelyett, hogy a teljes
kérést beolvasnánk egy vektorba, a `next`-et hívjuk meg, hogy megkapjuk az
iterátor első elemét. Az első `unwrap` az `Option`-t kezeli, és leállítja a
programot, ha az iterátornak nincs eleme. A második `unwrap` a `Result`-ot
kezeli, és ugyanaz a hatása, mint a 21-2. listában a `map`-be tett `unwrap`-nek.

Ezután megnézzük a `request_line`-t, hogy megegyezik-e a _/_ útvonalra irányuló
GET kérés kéréssorával. Ha igen, az `if` blokk visszaadja a HTML-fájlunk
tartalmát.

Ha a `request_line` _nem_ egyezik meg a _/_ útvonalra irányuló GET kéréssel,
akkor valamilyen más kérést kaptunk. Az `else` blokkba hamarosan kódot adunk,
hogy az összes többi kérésre is válaszoljunk.

Futtasd most ezt a kódot, és kérd le a _127.0.0.1:7878_ címet; a
_hello.html_-ben lévő HTML-t kell kapnod. Bármilyen más kérés, például a
_127.0.0.1:7878/valami-mas_ esetén olyan kapcsolathibát kapsz, amilyeneket a
21-1. és a 21-2. lista kódjának futtatásakor láttál.

Most adjuk hozzá az `else` blokkhoz a 21-7. listában látható kódot, hogy 404-es
állapotkóddal térjünk vissza, ami azt jelzi, hogy a kéréshez tartozó tartalom
nem található. Visszaadunk némi HTML-t is egy oldalhoz, amelyet a böngésző
megjelenít, és amely a végfelhasználó számára jelzi a választ.

<Listing number="21-7" file-name="src/main.rs" caption="Válasz 404-es állapotkóddal és hibaoldallal, ha bármi mást kértek, mint a */*">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Itt a válaszunk állapotsora 404-es állapotkódot és a `NOT FOUND` indoklást
tartalmazza. A válasz törzse a _404.html_ fájlban lévő HTML lesz. A
hibaoldalhoz létre kell hoznod egy _404.html_ fájlt a _hello.html_ mellett;
megint csak nyugodtan használj bármilyen HTML-t, vagy vedd át a 21-8. listában
szereplő példa HTML-t.

<Listing number="21-8" file-name="404.html" caption="Példatartalom ahhoz az oldalhoz, amelyet bármely 404-es válasszal visszaküldünk">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Ezekkel a változtatásokkal futtasd újra a szervert. A _127.0.0.1:7878_
lekérésének a _hello.html_ tartalmát kell visszaadnia, minden más kérésnek,
például a _127.0.0.1:7878/foo_ címnek pedig a _404.html_-ben lévő hiba-HTML-t.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refaktorálás

Pillanatnyilag az `if` és az `else` blokkban sok az ismétlés: mindkettő fájlt
olvas be, és a fájlok tartalmát írja a streambe. Az egyetlen különbség az
állapotsor és a fájlnév. Tegyük tömörebbé a kódot azzal, hogy ezeket a
különbségeket külön `if` és `else` sorokba emeljük ki, amelyek az állapotsor és
a fájlnév értékét változókhoz rendelik; ezután ezeket a változókat feltétel
nélkül használhatjuk a kódban a fájl beolvasásához és a válasz kiírásához. A
21-9. lista mutatja az eredményül kapott kódot, miután lecseréltük a nagy `if`
és `else` blokkokat.

<Listing number="21-9" file-name="src/main.rs" caption="Az `if` és `else` blokkok refaktorálása úgy, hogy csak a két eset közti eltérő kódot tartalmazzák">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Most az `if` és az `else` blokk csak a megfelelő állapotsor- és fájlnévértéket
adja vissza egy tuple-ben; ezt a két értéket ezután destrukturálással rendeljük
a `status_line` és a `filename` változókhoz, a `let` utasításban használt
mintával, ahogy azt a 19. fejezetben tárgyaltuk.

A korábban duplikált kód most már az `if` és `else` blokkokon kívül van, és a
`status_line`, illetve `filename` változókat használja. Így könnyebb látni a
két eset közti különbséget, és csak egy helyen kell módosítanunk a kódot, ha
változtatni akarunk a fájlbeolvasás és a válaszírás működésén. A 21-9. lista
kódjának viselkedése megegyezik a 21-7. listáéval.

Nagyszerű! Most van egy egyszerű webszerverünk nagyjából 40 sor Rust kódból,
amely az egyik kérésre egy tartalmas oldallal, az összes többire pedig 404-es
válasszal felel.

Jelenleg a szerverünk egyetlen szálon fut, vagyis egyszerre csak egy kérést tud
kiszolgálni. Nézzük meg, miért lehet ez probléma: szimuláljunk néhány lassú
kérést. Ezután kijavítjuk, hogy a szerverünk egyszerre több kérést is kezelni
tudjon.
