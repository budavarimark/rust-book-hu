
<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### A vezérlés visszaadása a runtime-nak

Az [„Az első async programunk”][async-program]<!-- ignore --> szakaszból
emlékezhetsz rá, hogy minden await pontnál a Rust lehetőséget ad a runtime-nak
arra, hogy szüneteltesse a taskot, és átváltson egy másikra, ha a bevárt future
még nem áll készen. Ennek a fordítottja is igaz: a Rust _kizárólag_ await
pontnál szünetelteti az async blokkokat, és adja vissza a vezérlést a
runtime-nak. Az await pontok között minden szinkron módon fut.

Ez azt jelenti, hogy ha egy async blokkban await pont nélkül végzel el egy
csomó munkát, az a future megakadályozza a többi future előrehaladását. Erre
néha úgy hivatkoznak, hogy az egyik future _kiéhezteti_ a többit. Bizonyos
esetekben ez nem nagy baj. Ha viszont valamilyen költséges előkészítést vagy
hosszan futó munkát végzel, esetleg van egy future-öd, amely a végtelenségig
folytat egy adott feladatot, át kell gondolnod, mikor és hol adod vissza a
vezérlést a runtime-nak.

Szimuláljunk egy hosszan futó műveletet, hogy szemléltessük a kiéheztetés
problémáját, aztán nézzük meg, hogyan oldható meg. A 17-14. listában bemutatunk
egy `slow` függvényt.

<Listing number="17-14" caption="A `thread::sleep` használata lassú műveletek szimulálására" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Ez a kód a `trpl::sleep` helyett a `std::thread::sleep` függvényt használja,
így a `slow` hívása néhány ezredmásodpercre blokkolja az aktuális szálat. A
`slow` így olyan valós műveleteket helyettesíthet, amelyek egyszerre hosszan
futók és blokkolók.

A 17-15. listában a `slow` segítségével két future-ben szimulálunk ilyen
CPU-igényes munkát.

<Listing number="17-15" caption="A `slow` függvény hívása lassú műveletek szimulálására" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Mindkét future csak _azután_ adja vissza a vezérlést a runtime-nak, hogy
elvégzett egy csomó lassú műveletet. Ha lefuttatod ezt a kódot, a következő
kimenetet fogod látni:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Ahogy a 17-5. listában, ahol a `trpl::select` hívással versenyeztettünk két
URL-t letöltő future-t, a `select` most is azonnal befejeződik, amint az `a`
elkészül. A két future `slow` hívásai között viszont nincs átlapolódás. Az `a`
future elvégzi az összes munkáját addig, amíg be nem várja a `trpl::sleep`
hívást, ezután a `b` future végzi el az összes munkáját a saját `trpl::sleep`
hívásának bevárásáig, végül pedig az `a` future fejeződik be. Ahhoz, hogy a két
future a lassú feladatai között is haladni tudjon, await pontokra van
szükségünk, hogy visszaadhassuk a vezérlést a runtime-nak. Vagyis kell valami,
amit bevárhatunk!

Ezt a fajta átadást már a 17-15. listában is látjuk: ha eltávolítanánk az `a`
future végéről a `trpl::sleep` hívást, akkor úgy fejeződne be, hogy a `b`
future _egyáltalán_ nem futna. Próbáljuk meg kiindulásként a `trpl::sleep`
függvényt használni arra, hogy a műveletek felváltva haladhassanak, ahogy azt a
17-16. lista mutatja.

<Listing number="17-16" caption="A `trpl::sleep` használata, hogy a műveletek felváltva haladhassanak" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Minden `slow` hívás közé beszúrtunk egy await ponttal rendelkező
`trpl::sleep` hívást. A két future munkája így már átlapolódik:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

Az `a` future még mindig fut egy darabig, mielőtt átadná a vezérlést a `b`-nek,
mert a `slow`-ot hívja meg előbb, és csak utána a `trpl::sleep`-et, de ezután a
future-ök oda-vissza váltogatják egymást minden alkalommal, amikor valamelyikük
await ponthoz ér. Most ezt minden `slow` hívás után megtettük, de a munkát
bárhogyan feldarabolhatnánk, ahogy nekünk a leginkább értelmes.

Valójában azonban nem _aludni_ szeretnénk itt: a lehető leggyorsabban akarunk
haladni. Csupán vissza kell adnunk a vezérlést a runtime-nak. Ezt közvetlenül
is megtehetjük a `trpl::yield_now` függvénnyel. A 17-17. listában az összes
`trpl::sleep` hívást `trpl::yield_now`-ra cseréljük.

<Listing number="17-17" caption="A `yield_now` használata, hogy a műveletek felváltva haladhassanak" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Ez a kód egyszerre világosabban fejezi ki a valódi szándékot, és jelentősen
gyorsabb is lehet, mint a `sleep` használata, mert az olyan időzítőknek, mint
amilyet a `sleep` használ, gyakran korlátozott a felbontásuk. Az általunk
használt `sleep` verzió például mindig legalább egy ezredmásodpercig alszik,
még akkor is, ha egy nanoszekundumos `Duration` értéket adunk át neki. Ne
feledd, a modern számítógépek _gyorsak_: egy ezredmásodperc alatt is sok
mindent el tudnak végezni!

Ez azt jelenti, hogy az async még számításigényes feladatoknál is hasznos
lehet, attól függően, mi mást csinál a programod, mert hasznos eszközt ad a
program különböző részei közötti kapcsolatok strukturálásához (cserébe viszont
ott van az async állapotgép többletköltsége). Ez a _kooperatív multitaszking_
egy formája, amelyben minden future maga dönti el, mikor adja át a vezérlést az
await pontokon keresztül. Ezért minden future felelőssége az is, hogy ne
blokkoljon túl sokáig. Néhány Rust-alapú beágyazott operációs rendszerben ez a
multitaszking _egyetlen_ formája!

A valós kódban persze általában nem fogsz minden egyes sorban függvényhívásokat
és await pontokat váltogatni. Bár a vezérlés ilyen módon való átadása
viszonylag olcsó, nem ingyenes. Sok esetben egy számításigényes feladat
feldarabolása jelentősen lassabbá teheti azt, így néha az _összteljesítmény_
szempontjából jobb, ha hagyjuk, hogy egy művelet rövid ideig blokkoljon. Mindig
mérj, hogy kiderüljön, valójában hol vannak a kódod teljesítménybeli szűk
keresztmetszetei. Az alapul szolgáló működést viszont fontos szem előtt
tartani, ha azt tapasztalod, hogy sok minden sorosan fut, amiről azt hitted,
konkurensen fog!

### Saját async absztrakciók építése {#building-our-own-async-abstractions}

A future-öket egymással kombinálva új mintákat is létrehozhatunk. Például
felépíthetünk egy `timeout` függvényt a már meglévő async építőelemekből. Ha
elkészülünk, az eredmény maga is egy újabb építőelem lesz, amellyel további
async absztrakciókat hozhatunk létre.

A 17-18. lista mutatja, hogyan várnánk el ennek a `timeout`-nak a működését egy
lassú future-rel.

<Listing number="17-18" caption="Az elképzelt `timeout` használata egy lassú művelet időkorlátos futtatására" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Implementáljuk hát! Kezdésként gondoljuk át a `timeout` API-ját:

- Magának is async függvénynek kell lennie, hogy bevárhassuk.
- Az első paramétere a futtatandó future legyen. Generikussá tehetjük, hogy
  bármilyen future-rel működjön.
- A második paramétere a maximális várakozási idő lesz. Ha `Duration` típust
  használunk, azt könnyen továbbadhatjuk a `trpl::sleep`-nek.
- `Result` értékkel kell visszatérnie. Ha a future sikeresen befejeződik, a
  `Result` egy `Ok` lesz, benne a future által előállított értékkel. Ha előbb
  telik le az időkorlát, a `Result` egy `Err` lesz, benne azzal az
  időtartammal, ameddig az időkorlát várt.

A 17-19. lista mutatja ezt a deklarációt.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="A `timeout` szignatúrájának definiálása" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Ez kielégíti a típusokkal kapcsolatos céljainkat. Most gondoljuk át a szükséges
_viselkedést_: versenyeztetni akarjuk a kapott future-t az időtartammal. A
`trpl::sleep` segítségével időzítő future-t készíthetünk az időtartamból, a
`trpl::select` hívással pedig futtathatjuk ezt az időzítőt a hívó által átadott
future-rel együtt.

A 17-20. listában úgy implementáljuk a `timeout`-ot, hogy mintaillesztést
végzünk a `trpl::select` bevárásának eredményén.

<Listing number="17-20" caption="A `timeout` definiálása a `select` és a `sleep` segítségével" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

A `trpl::select` implementációja nem fair: az argumentumokat mindig abban a
sorrendben pollozza, ahogyan átadták őket (más `select` implementációk
véletlenszerűen választják ki, melyik argumentumot pollozzák először). Ezért a
`future_to_try`-t adjuk át elsőként a `select`-nek, hogy akkor is legyen esélye
befejeződni, ha a `max_time` nagyon rövid időtartam. Ha a `future_to_try`
fejeződik be előbb, a `select` egy `Left` értéket ad vissza a `future_to_try`
kimenetével. Ha az időzítő fejeződik be előbb, a `select` egy `Right` értéket
ad vissza az időzítő `()` kimenetével.

Ha a `future_to_try` sikerrel jár, és `Left(output)` értéket kapunk,
`Ok(output)` értékkel térünk vissza. Ha ehelyett az alvási időzítő jár le, és
`Right(())` értéket kapunk, akkor a `()` értéket figyelmen kívül hagyjuk egy
`_` mintával, és `Err(max_time)` értékkel térünk vissza.

Ezzel készen is van egy működő `timeout`, amelyet két másik async segédelemből
építettünk fel. Ha lefuttatjuk a kódunkat, az időkorlát letelte után kiírja a
hibaágat:

```text
Failed after 2 seconds
```

Mivel a future-ök kombinálhatók más future-ökkel, kisebb async építőelemekből
igazán erőteljes eszközöket állíthatsz össze. Ugyanezzel a megközelítéssel
kombinálhatod például az időkorlátokat az újrapróbálkozásokkal, azokat pedig
olyan műveletekkel, mint a hálózati hívások (például a 17-5. listában látottak).

A gyakorlatban általában közvetlenül az `async` és az `await` kulcsszavakkal
fogsz dolgozni, másodsorban pedig olyan függvényekkel, mint a `select`, és
olyan makrókkal, mint a `join!`, hogy szabályozd a legkülső future-ök
futtatását.

Már számos módot láttunk arra, hogyan dolgozhatunk több future-rel egyszerre. A
következőkben azt nézzük meg, hogyan dolgozhatunk időben egymás után következő
future-ök sorozatával a _stream_-ek segítségével.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
