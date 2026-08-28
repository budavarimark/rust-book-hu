<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Stream-ek: future-ök sorozatban

Emlékezz vissza, hogyan használtuk a fejezet korábbi részében, az
[„Üzenetküldés”][17-02-messages]<!-- ignore --> szakaszban az async csatornánk
fogadó oldalát. Az async `recv` metódus idővel elemek sorozatát állítja elő. Ez
egy sokkal általánosabb minta egy példája, amelyet _stream_-nek nevezünk. Sok
fogalom természetes módon írható le stream-ként: egy sorban elérhetővé váló
elemek, a fájlrendszerből fokozatosan beolvasott adatdarabok, amikor a teljes
adathalmaz túl nagy a számítógép memóriájához, vagy a hálózaton át idővel
megérkező adatok. Mivel a stream-ek future-ök, bármilyen más future-rel együtt
használhatjuk és érdekes módokon kombinálhatjuk őket. Kötegelhetjük például az
eseményeket, hogy ne indítsunk túl sok hálózati hívást, időkorlátot szabhatunk
hosszan futó műveletek sorozatára, vagy visszafoghatjuk a felhasználói felület
eseményeit, hogy ne végezzünk fölösleges munkát.

Elemek sorozatával már a 13. fejezetben is találkoztunk, amikor az
[„Az `Iterator` trait és a `next` metódus”][iterator-trait]<!-- ignore -->
szakaszban az Iterator trait-et néztük meg, de két különbség is van az
iterátorok és az async csatorna fogadó oldala között. Az első különbség az idő:
az iterátorok szinkronok, a csatorna fogadó oldala viszont aszinkron. A második
különbség az API. Ha közvetlenül az `Iterator`-ral dolgozunk, a szinkron `next`
metódusát hívjuk meg. Konkrétan a `trpl::Receiver` stream esetében ehelyett egy
aszinkron `recv` metódust hívtunk. Ettől eltekintve ezek az API-k nagyon
hasonlónak érződnek, és ez a hasonlóság nem véletlen. A stream olyan, mint az
iteráció aszinkron formája. Míg azonban a `trpl::Receiver` kifejezetten
üzenetek fogadására vár, az általános célú stream API sokkal tágabb: a
következő elemet adja, ahogy az `Iterator` teszi, csak éppen aszinkron módon.

Az iterátorok és a stream-ek közötti hasonlóság a Rustban azt jelenti, hogy
bármilyen iterátorból készíthetünk stream-et. Az iterátorokhoz hasonlóan úgy
dolgozhatunk egy stream-mel, hogy meghívjuk a `next` metódusát, majd bevárjuk a
kimenetét, ahogy a 17-21. listában, amely még nem fordul le.

<Listing number="17-21" caption="Stream létrehozása egy iterátorból és az értékeinek kiírása" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Egy számokból álló tömbbel indulunk, amelyet iterátorrá alakítunk, majd `map`
hívással megduplázzuk az összes értéket. Ezután a `trpl::stream_from_iter`
függvénnyel stream-mé alakítjuk az iterátort. Végül egy `while let` ciklussal
végigmegyünk a stream elemein, ahogy azok megérkeznek.

Sajnos amikor megpróbáljuk lefuttatni a kódot, nem fordul le, hanem azt jelzi,
hogy nincs elérhető `next` metódus:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Ahogy ez a kimenet elmagyarázza, a fordítási hiba oka az, hogy a `next` metódus
használatához a megfelelő trait-nek hatókörben kell lennie. Az eddigiek alapján
joggal gondolhatnád, hogy ez a trait a `Stream`, de valójában a `StreamExt`.
Az `Ext` az _extension_ (kiterjesztés) rövidítése, és a Rust közösségben bevett
minta arra, hogy egy trait-et egy másikkal egészítsünk ki.

A `Stream` trait egy alacsony szintű interfészt definiál, amely lényegében az
`Iterator` és a `Future` trait-eket ötvözi. A `StreamExt` a `Stream` tetejére
épülő, magasabb szintű API-készletet nyújt, benne a `next` metódussal, valamint
más segédmetódusokkal, amelyek hasonlítanak az `Iterator` trait által
biztosítottakhoz. A `Stream` és a `StreamExt` egyelőre nem része a Rust
standard könyvtárának, de az ökoszisztéma legtöbb crate-je hasonló
definíciókat használ.

A fordítási hiba javításához fel kell vennünk egy `use` utasítást a
`trpl::StreamExt`-hez, ahogy a 17-22. listában látható.

<Listing number="17-22" caption="Iterátor sikeres használata stream alapjaként" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Ha mindezeket a darabokat összerakjuk, a kód úgy működik, ahogy szeretnénk!
Ráadásul most, hogy a `StreamExt` hatókörben van, az összes segédmetódusát
használhatjuk, ugyanúgy, mint az iterátoroknál.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
