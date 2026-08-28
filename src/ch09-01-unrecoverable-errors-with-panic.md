## Helyrehozhatatlan hibák a `panic!` makróval

Néha rossz dolgok történnek a kódodban, és nem tehetsz ellenük semmit. Ezekre az
esetekre való a Rust `panic!` makrója. A gyakorlatban kétféleképpen válthatsz ki
panicot: olyan műveletet hajtasz végre, amelytől a kódunk panicot vált ki
(például egy tömb végén túlra hivatkozol), vagy közvetlenül meghívod a `panic!`
makrót. Mindkét esetben panicot idézünk elő a programunkban. Alapértelmezés
szerint ezek a panicok kiírnak egy hibaüzenetet, visszabontják és feltakarítják
a stacket, majd kilépnek. Egy környezeti változó segítségével azt is elérheted,
hogy a Rust panic esetén megjelenítse a hívási vermet, így könnyebben
visszakeresheted a panic forrását.

> ### A stack visszabontása vagy megszakítás panic esetén
>
> Alapértelmezés szerint panic esetén a program elkezdi a _visszabontást_
> (unwinding), ami azt jelenti, hogy a Rust visszafelé végigjárja a stacket, és
> feltakarítja az adatokat minden függvényből, amellyel találkozik. A visszafelé
> haladás és a takarítás azonban rengeteg munka. A Rust ezért lehetővé teszi,
> hogy ehelyett az azonnali _megszakítást_ (abort) válaszd, amely takarítás
> nélkül fejezi be a programot.
>
> A program által használt memóriát ilyenkor az operációs rendszernek kell
> felszabadítania. Ha a projektedben a lehető legkisebbre kell szorítanod a
> keletkező binárist, akkor a visszabontásról átválthatsz megszakításra úgy,
> hogy a `panic = 'abort'` sort hozzáadod a _Cargo.toml_ fájlod megfelelő
> `[profile]` szakaszaihoz. Ha például release módban szeretnél megszakítást
> panic esetén, ezt add hozzá:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Próbáljuk meg meghívni a `panic!` makrót egy egyszerű programban:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Amikor futtatod a programot, valami ilyesmit fogsz látni:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

A `panic!` hívása okozza az utolsó két sorban látható hibaüzenetet. Az első sor
a panic üzenetünket mutatja, valamint a forráskódnak azt a helyét, ahol a panic
bekövetkezett: a _src/main.rs:2:5_ azt jelzi, hogy a _src/main.rs_ fájlunk
második sorának ötödik karakteréről van szó.

Ebben az esetben a megjelölt sor a saját kódunk része, és ha odalapozunk, ott
látjuk a `panic!` makró hívását. Más esetekben a `panic!` hívása olyan kódban
lehet, amelyet a mi kódunk hív meg, és a hibaüzenetben jelentett fájlnév és
sorszám valaki más kódjára fog mutatni, ahol a `panic!` makrót meghívják – nem
pedig a mi kódunk azon sorára, amely végül a `panic!` hívásához vezetett.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Annak a kiderítésére, hogy kódunk melyik része okozza a problémát, használhatjuk
azoknak a függvényeknek a backtrace-ét, amelyekből a `panic!` hívás származik.
Ahhoz, hogy megértsük, hogyan használjunk egy `panic!` backtrace-t, nézzünk meg
egy másik példát, és lássuk, milyen az, amikor a `panic!` hívás nem a saját
kódunk közvetlen makróhívásából, hanem egy könyvtárból érkezik a kódunkban lévő
hiba miatt. A 9-1. listában olyan kód szerepel, amely egy vektor érvényes
indextartományán túli indexhez próbál hozzáférni.

<Listing number="9-1" file-name="src/main.rs" caption="Kísérlet egy vektor végén túli elem elérésére, ami `panic!` hívást fog okozni">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Itt a vektorunk 100. eleméhez próbálunk hozzáférni (ez a 99-es indexen van,
mivel az indexelés nullától indul), a vektornak azonban csak három eleme van.
Ebben a helyzetben a Rust panicot vált ki. A `[]` használatától azt várnánk,
hogy egy elemet ad vissza, de ha érvénytelen indexet adsz át, nincs olyan elem,
amelyet a Rust helyesen visszaadhatna.

C-ben egy adatszerkezet végén túli olvasás nem definiált viselkedés. Bármit
megkaphatsz, ami a memóriának azon a helyén van, amely az adatszerkezet adott
elemének felelne meg, még akkor is, ha az a memória nem tartozik a
szerkezethez. Ezt _buffer overread_-nek nevezik, és biztonsági sebezhetőségekhez
vezethet, ha egy támadó úgy tudja manipulálni az indexet, hogy az adatszerkezet
után tárolt, számára nem engedélyezett adatokat olvasson ki.

Hogy megvédje a programodat az ilyesfajta sebezhetőségtől, a Rust leállítja a
végrehajtást és megtagadja a folytatást, ha egy nem létező indexen álló elemet
próbálsz kiolvasni. Próbáljuk ki, és lássuk:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Ez a hiba a _main.rs_ 4. sorára mutat, ahol a `v`-ben lévő vektor 99-es
indexéhez próbálunk hozzáférni.

A `note:` sor elárulja, hogy beállíthatjuk a `RUST_BACKTRACE` környezeti
változót, hogy pontos backtrace-t kapjunk arról, mi vezetett a hibához. A
_backtrace_ az összes olyan függvény listája, amelyet meghívtak, hogy eljussunk
eddig a pontig. A backtrace-ek a Rustban ugyanúgy működnek, mint más nyelvekben:
az olvasásuk kulcsa, hogy felülről indulj, és addig olvasd, amíg meg nem látod
az általad írt fájlokat. Ott ered a probléma. Az e fölötti sorok olyan kódok,
amelyeket a te kódod hívott meg; az alattuk lévő sorok pedig olyan kódok,
amelyek a te kódodat hívták. Ezek az előtte és utána álló sorok tartalmazhatnak
Rust-alapkódot, standard könyvtárbeli kódot vagy az általad használt crate-eket.
Próbáljunk meg backtrace-t kérni úgy, hogy a `RUST_BACKTRACE` környezeti
változót `0`-tól különböző értékre állítjuk. A 9-2. lista az általad is látható
kimenethez hasonlót mutat.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="A `panic!` hívása által generált backtrace, amely a `RUST_BACKTRACE` környezeti változó beállításakor jelenik meg">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Ez rengeteg kimenet! A pontosan látható kimenet eltérhet az operációs
rendszeredtől és a Rust verziójától függően. Ahhoz, hogy ilyen információt
tartalmazó backtrace-eket kapj, engedélyezni kell a debug szimbólumokat. A debug
szimbólumok alapértelmezés szerint engedélyezve vannak, ha a `cargo build` vagy
a `cargo run` parancsot a `--release` kapcsoló nélkül használod, ahogy itt is
tettük.

A 9-2. lista kimenetében a backtrace 6. sora a projektünkben arra a sorra mutat,
amely a problémát okozza: a _src/main.rs_ 4. sorára. Ha nem szeretnénk, hogy a
programunk panicot váltson ki, a vizsgálódást annál a helynél kell kezdenünk,
amelyre az első olyan sor mutat, amely egy általunk írt fájlt említ. A 9-1.
listában, ahol szándékosan írtunk panicot okozó kódot, a panic javításának módja
az, hogy ne kérjünk a vektor indextartományán túli elemet. Amikor a jövőben a
kódod panicot vált ki, ki kell derítened, hogy a kód milyen művelettel és milyen
értékekkel okozza a panicot, és mit kellene helyette tennie.

A `panic!` makróra és arra, hogy mikor érdemes és mikor nem érdemes a `panic!`
makróval kezelni a hibás helyzeteket, ebben a fejezetben később, a [„`panic!`
vagy ne `panic!`”][to-panic-or-not-to-panic]<!-- ignore --> szakaszban térünk
vissza. Ezután megnézzük, hogyan lehet egy hibából felépülni a `Result`
segítségével.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic
