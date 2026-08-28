## Szabályos leállítás és takarítás

A 21-20. listában szereplő kód a szándékunknak megfelelően, egy thread pool
segítségével, aszinkron módon válaszol a kérésekre. Kapunk néhány
figyelmeztetést a `workers`, az `id` és a `thread` mezőkről, amelyeket nem
használunk közvetlenül; ez arra emlékeztet minket, hogy semmit nem takarítunk
el. Amikor a kevésbé elegáns
<kbd>ctrl</kbd>-<kbd>C</kbd> módszerrel állítjuk le a fő szálat, azonnal minden
más szál is leáll, még akkor is, ha éppen egy kérés kiszolgálásának közepén
tartanak.

Ezután tehát implementáljuk a `Drop` trait-et, hogy a pool minden szálán
meghívjuk a `join`-t, így azok befejezhetik a folyamatban lévő kéréseket a
bezárás előtt. Utána megvalósítunk egy módot arra, hogy szóljunk a szálaknak: ne
fogadjanak több új kérést, és álljanak le. Hogy működés közben is lássuk ezt a
kódot, úgy módosítjuk a szerverünket, hogy csak két kérést fogadjon, mielőtt
szabályosan leállítja a thread poolt.

Egy dolgot érdemes menet közben észrevenni: mindez nem érinti a kódnak azokat a
részeit, amelyek a closure-ök végrehajtását intézik, tehát minden ugyanígy nézne
ki akkor is, ha egy async runtime-hoz használnánk a thread poolt.

### A `Drop` trait implementálása a `ThreadPool`-on

Kezdjük azzal, hogy implementáljuk a `Drop`-ot a thread poolunkon. Amikor a pool
dropolódik, minden szálunknak join-olnia kell, hogy biztosan befejezzék a
munkájukat. A 21-22. lista egy első próbálkozást mutat a `Drop`
implementációra; ez a kód még nem egészen fog működni.

<Listing number="21-22" file-name="src/lib.rs" caption="Az egyes szálak join-olása, amikor a thread pool kikerül a hatókörből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Először végigmegyünk a thread pool `workers` elemein. A `&mut`-ot azért
használjuk, mert a `self` egy módosítható referencia, és a `worker`-t is
módosítani akarjuk. Minden `worker` esetén kiírunk egy üzenetet arról, hogy az
adott `Worker` példány leáll, majd meghívjuk a `join`-t az adott `Worker`
példány szálán. Ha a `join` hívása sikertelen, az `unwrap`-pel panicot váltunk
ki a Rustban, és nem szabályos leállásba megyünk át.

Íme a hiba, amit a kód fordításakor kapunk:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

A hiba azt mondja, hogy nem hívhatjuk meg a `join`-t, mert csak egy módosítható
borrow-unk van az egyes `worker`-ekre, a `join` viszont átveszi az argumentuma
ownershipjét. A probléma megoldásához ki kell mozgatnunk a szálat abból a
`Worker` példányból, amely a `thread`-et birtokolja, hogy a `join` fel tudja
használni a szálat. Ennek egyik módja ugyanaz a megközelítés, amit a 18-15.
listában alkalmaztunk. Ha a `Worker` egy `Option<thread::JoinHandle<()>>`-t
tartalmazna, meghívhatnánk a `take` metódust az `Option`-ön, hogy kimozgassuk az
értéket a `Some` variánsból, és a helyére egy `None` variánst tegyünk. Más
szóval: egy futó `Worker`-nek `Some` variáns lenne a `thread` mezőjében, és
amikor ki akarnánk takarítani egy `Worker`-t, a `Some`-ot `None`-ra cserélnénk,
hogy a `Worker`-nek ne legyen futtatható szála.

Ez azonban _csak_ a `Worker` dropolásakor kerülne elő. Cserébe egy
`Option<thread::JoinHandle<()>>`-vel kellene bajlódnunk mindenhol, ahol a
`worker.thread`-hez hozzáférünk. Az idiomatikus Rust elég gyakran használ
`Option`-t, de ha azon kapod magad, hogy kerülő megoldásként egy `Option`-be
csomagolsz valamit, amiről tudod, hogy mindig jelen lesz, jó ötlet más
megközelítéseket keresni, amelyekkel tisztább és kevésbé hibalehetőséges lesz a
kódod.

Ebben az esetben létezik jobb alternatíva: a `Vec::drain` metódus. Ez egy
tartományparamétert fogad, amely megadja, mely elemeket távolítsa el a
vektorból, és ezeknek az elemeknek egy iterátorát adja vissza. A `..` tartomány
szintaxisának átadásával *minden* értéket eltávolítunk a vektorból.

A `ThreadPool` `drop` implementációját tehát így kell frissítenünk:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Ez megoldja a fordítási hibát, és semmilyen más változtatást nem igényel a
kódunkban. Vedd figyelembe, hogy mivel a drop meghívódhat panic közben is, az
unwrap szintén panicot válthat ki, ami dupla panicot okoz; az pedig azonnal
összeomlasztja a programot, és megszakítja a folyamatban lévő takarítást. Egy
példaprogramnál ez rendben van, de éles kódban nem ajánlott.

### Jelzés a szálaknak, hogy hagyják abba a munkák figyelését

Az összes eddigi változtatással a kódunk figyelmeztetések nélkül fordul. A rossz
hír azonban az, hogy ez a kód még nem úgy működik, ahogy szeretnénk. A kulcs a
`Worker` példányok szálai által futtatott closure-ök logikájában van: jelenleg
meghívjuk a `join`-t, de az nem állítja le a szálakat, mert azok végtelen
`loop`-ban keresnek munkát. Ha a `drop` jelenlegi implementációjával
megpróbálnánk dropolni a `ThreadPool`-t, a fő szál örökre blokkolódna, miközben
az első szál befejezésére vár.

A probléma megoldásához változtatnunk kell a `ThreadPool` `drop`
implementációján, majd a `Worker` ciklusán is.

Először a `ThreadPool` `drop` implementációját változtatjuk meg úgy, hogy
explicit módon dropolja a `sender`-t, mielőtt megvárná a szálak befejeződését. A
21-23. lista a `ThreadPool` változtatásait mutatja a `sender` explicit
dropolásához. A szállal ellentétben itt _valóban_ szükségünk van egy
`Option`-re, hogy az `Option::take`-kel ki tudjuk mozgatni a `sender`-t a
`ThreadPool`-ból.

<Listing number="21-23" file-name="src/lib.rs" caption="A `sender` explicit dropolása a `Worker` szálak join-olása előtt">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

A `sender` dropolása lezárja a csatornát, ami azt jelzi, hogy több üzenet nem
lesz elküldve. Amikor ez megtörténik, a `Worker` példányok végtelen ciklusában
lévő összes `recv` hívás hibát ad vissza. A 21-24. listában úgy módosítjuk a
`Worker` ciklusát, hogy ilyenkor szabályosan kilépjen a ciklusból; ez azt
jelenti, hogy a szálak befejeződnek, amikor a `ThreadPool` `drop`
implementációja meghívja rajtuk a `join`-t.

<Listing number="21-24" file-name="src/lib.rs" caption="Explicit kilépés a ciklusból, amikor a `recv` hibát ad vissza">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Hogy működés közben lássuk ezt a kódot, módosítsuk a `main`-t úgy, hogy csak két
kérést fogadjon el, mielőtt szabályosan leállítja a szervert, ahogy a 21-25.
lista mutatja.

<Listing number="21-25" file-name="src/main.rs" caption="A szerver leállítása két kérés kiszolgálása után, a ciklusból kilépve">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Egy valós webszervernél nem szeretnéd, ha mindössze két kérés kiszolgálása után
leállna. Ez a kód csak azt demonstrálja, hogy a szabályos leállítás és takarítás
rendben működik.

A `take` metódus az `Iterator` trait-ben van definiálva, és legfeljebb az első
két elemre korlátozza az iterációt. A `ThreadPool` a `main` végén kikerül a
hatókörből, és lefut a `drop` implementáció.

Indítsd el a szervert a `cargo run` paranccsal, és küldj három kérést. A
harmadik kérésnek hibára kell futnia, a terminálodban pedig valami ehhez hasonló
kimenetet kell látnod:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Lehet, hogy a `Worker` azonosítók és az üzenetek más sorrendben jelennek meg. Az
üzenetekből látszik, hogyan működik ez a kód: a 0-s és a 3-as `Worker` példány
kapta meg az első két kérést. A szerver a második kapcsolat után nem fogadott
több kapcsolatot, és a `ThreadPool`-on lévő `Drop` implementáció még azelőtt
elkezdett futni, hogy a `Worker 3` egyáltalán belekezdett volna a munkájába. A
`sender` dropolása lekapcsolja az összes `Worker` példányt, és jelzi nekik, hogy
álljanak le. Minden `Worker` példány kiír egy üzenetet, amikor lekapcsolódik,
majd a thread pool meghívja a `join`-t, hogy megvárja az egyes `Worker` szálak
befejeződését.

Vegyünk észre egy érdekes részletet ebben a konkrét futásban: a `ThreadPool`
dropolta a `sender`-t, és még mielőtt bármelyik `Worker` hibát kapott volna,
megpróbáltuk join-olni a `Worker 0`-t. A `Worker 0` még nem kapott hibát a
`recv`-től, így a fő szál blokkolódott, és megvárta, hogy a `Worker 0`
befejeződjön. Közben a `Worker 3` kapott egy munkát, majd minden szál hibát
kapott. Amikor a `Worker 0` befejeződött, a fő szál megvárta a többi `Worker`
példány befejeződését is. Addigra mindegyik kilépett a ciklusából, és leállt.

Gratulálunk! Ezzel elkészültünk a projektünkkel: van egy alap webszerverünk,
amely thread poolt használ az aszinkron válaszadáshoz. Képesek vagyunk a szerver
szabályos leállítására, ami kitakarítja a pool összes szálát.

Íme a teljes kód referenciaként:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Itt még többet is tehetnénk! Ha tovább szeretnéd fejleszteni ezt a projektet,
íme néhány ötlet:

- Írj több dokumentációt a `ThreadPool`-hoz és a publikus metódusaihoz.
- Írj teszteket a könyvtár funkcionalitásához.
- Cseréld le az `unwrap` hívásokat robusztusabb hibakezelésre.
- Használd a `ThreadPool`-t webes kérések kiszolgálásán kívüli feladatra is.
- Keress egy thread pool crate-et a [crates.io](https://crates.io/) oldalon, és
  implementálj egy hasonló webszervert a saját megoldásunk helyett azzal a
  crate-tel. Utána hasonlítsd össze az API-ját és a robusztusságát az általunk
  implementált thread poolével.

## Összefoglalás

Szép munka! Eljutottál a könyv végére! Köszönjük, hogy velünk tartottál ezen a
Rust-körutazáson. Most már készen állsz arra, hogy megvalósítsd a saját Rust
projektjeidet, és segíts mások projektjeiben. Ne feledd: van egy befogadó
közösség a többi Rustaceanből, akik szívesen segítenek bármilyen kihívásban,
amivel a Rust-utad során találkozol.
