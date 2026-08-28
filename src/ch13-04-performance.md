<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Teljesítmény: ciklusok kontra iterátorok

Ahhoz, hogy eldöntsd, ciklusokat vagy iterátorokat használj-e, tudnod kell,
melyik implementáció a gyorsabb: a `search` függvény explicit `for` ciklust
használó változata, vagy az iterátorokat használó.

Futtattunk egy benchmarkot, amelyben Sir Arthur Conan Doyle _The Adventures of
Sherlock Holmes_ című művének teljes tartalmát betöltöttük egy `String`-be, és
a _the_ szót kerestük a tartalomban. Íme a benchmark eredményei a `search`
függvény `for` ciklust használó és az iterátorokat használó változatára:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

A két implementáció teljesítménye hasonló! A benchmark kódját itt nem
magyarázzuk el, mert nem az a cél, hogy bebizonyítsuk a két változat
egyenértékűségét, hanem hogy általános képet kapjunk arról, hogyan viszonyul
egymáshoz a két implementáció teljesítmény szempontjából.

Egy átfogóbb benchmarkhoz különböző méretű szövegeket kellene `contents`-ként
kipróbálnod, különböző és eltérő hosszúságú szavakat `query`-ként, és mindenféle
egyéb variációt. A lényeg viszont ez: az iterátorok — bár magas szintű
absztrakciót jelentenek — nagyjából ugyanarra a kódra fordulnak le, mintha te
magad írtad volna meg az alacsonyabb szintű kódot. Az iterátorok a Rust
_zero-cost absztrakcióinak_ egyike; ezen azt értjük, hogy az absztrakció
használata nem jár semmilyen többlet futásidejű költséggel. Ez analóg azzal,
ahogyan Bjarne Stroustrup, a C++ eredeti megtervezője és implementálója
definiálja a nulla többletköltséget a 2012-es ETAPS-en tartott „Foundations of
C++” című előadásában:

> Általánosságban a C++ implementációk betartják a nulla többletköltség elvét:
> amit nem használsz, azért nem fizetsz. Sőt: amit használsz, azt kézzel sem
> tudnád jobban megírni.

Sok esetben az iterátorokat használó Rust-kód ugyanarra az assemblyre fordul,
amit kézzel írnál. Az olyan optimalizációk, mint a ciklusok kigöngyölítése és a
tömbindexelés határellenőrzésének elhagyása, itt is érvényesülnek, és rendkívül
hatékonnyá teszik az eredményül kapott kódot. Most, hogy ezt tudod,
félelem nélkül használhatsz iterátorokat és closure-öket! Ezektől a kód
magasabb szintűnek tűnik, de nem járnak futásidejű teljesítménybüntetéssel.

## Összefoglalás

A closure-ök és az iterátorok a Rust olyan nyelvi elemei, amelyeket a
funkcionális programozási nyelvek ötletei ihlettek. Hozzájárulnak ahhoz, hogy a
Rust képes legyen magas szintű gondolatokat világosan kifejezni alacsony szintű
teljesítmény mellett. A closure-ök és az iterátorok implementációja olyan, hogy
a futásidejű teljesítményt nem befolyásolja. Ez része annak a Rust-célnak, hogy
zero-cost absztrakciókat igyekszik nyújtani.

Most, hogy javítottuk az I/O-projektünk kifejezőerejét, nézzük meg a `cargo`
néhány további képességét, amelyek segítenek megosztani a projektet a
világgal.
