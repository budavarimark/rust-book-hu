# A Rust könyv magyar fordítása – fordítói útmutató

Ez a dokumentum a `src/` mappában található könyvszöveg magyar fordításának
szabályait rögzíti. Maga a dokumentum nem része a könyvnek.

## Alapelvek

1. **A kód nem fordítandó.** A ```` ``` ```` kódblokkok tartalma, a bennük lévő
   kommentek és kimenetek, valamint a soron belüli `kód` részek változatlanok
   maradnak.
2. **A Rust szakkifejezései angolul maradnak.** Lásd a szótárat lentebb.
3. **A szerkezet nem változik.** A fájlnevek, a sorok sorrendje, a
   `{{#include}}` / `{{#rustdoc_include}}` direktívák, a `<Listing>` elemek
   `number` és `file-name` attribútumai, a link-URL-ek és a
   link-referencia-címkék (`[cimke]: ...`) érintetlenek maradnak.
4. **Megszólítás:** tegező forma („ha ezt írod”), a közös haladást pedig T/1
   fejezi ki („nézzük meg”, „hozzuk létre”).
5. **Sortörés:** a szöveg 80 karakternél törik, ahogy az eredetiben.

## Mit fordítunk, mit nem

| Elem | Teendő |
| --- | --- |
| Bekezdések, felsorolások, címsorok | fordítandó |
| `<Listing caption="...">` | **csak** a `caption` fordítandó |
| `<Listing number="..." file-name="...">` | változatlan |
| ```` ``` ```` kódblokk (kód, komment, kimenet) | változatlan |
| Soron belüli `kód`, típusnevek, metódusnevek | változatlan |
| `{{#include}}`, `{{#rustdoc_include}}` | változatlan |
| `[szöveg](url)` | csak a `szöveg` fordítandó |
| `[cimke]: url` sorok | teljesen változatlanok |
| `<!-- ... -->` HTML-kommentek | változatlanok |
| Címsor végén álló `{#horgony}` | **változatlanul megtartandó** |
| `<img src=... alt="...">` | csak az `alt` és a képaláírás fordítandó |
| `<span class="caption">...</span>` | a szövege fordítandó |
| Fájlnevek (`src/main.rs`, `Cargo.toml`), parancsok | változatlanok |

## Terminológiai szótár

### Angolul maradó kifejezések

Ezeket **nem fordítjuk**. Ragozáskor kötőjellel kapcsoljuk a toldalékot:
`trait-ek`, `crate-ben`, `lifetime-ot`, `ownership-et`, `closure-ök`.

| Angol | Magyar használat |
| --- | --- |
| ownership | ownership |
| owner | owner |
| borrowing, borrow | borrowing, borrow |
| borrow checker | borrow checker |
| move (ownership-átadás) | move |
| lifetime | lifetime |
| lifetime elision | lifetime elision |
| trait | trait |
| trait bound | trait bound |
| trait object | trait object |
| supertrait | supertrait |
| blanket implementation | blanket implementáció |
| associated type | asszociált típus |
| crate | crate |
| binary crate / library crate | binary crate / library crate |
| workspace | workspace |
| closure | closure |
| slice, string slice | slice, string slice |
| struct | struct |
| enum | enum |
| match (kulcsszó) | `match` |
| stack | stack |
| heap | heap |
| smart pointer | smart pointer |
| deref coercion | deref coercion |
| interior mutability | interior mutability |
| shadowing | shadowing |
| panic | panic |
| unsafe Rust | unsafe Rust |
| future | future |
| stream | stream |
| task (async) | task |
| executor, runtime (async futtatókörnyezet) | executor, runtime |
| poll | poll |
| thread pool | thread pool |
| state pattern | state pattern |
| newtype pattern | newtype minta |
| dispatch (static/dynamic) | statikus/dinamikus dispatch |
| Cargo, crates.io, rustup, rustc, rustfmt, Clippy | változatlan |

### Fordítandó kifejezések

| Angol | Magyar |
| --- | --- |
| variable | változó |
| mutable / immutable | módosítható / nem módosítható |
| constant | konstans |
| function | függvény |
| method | metódus |
| associated function | asszociált függvény |
| parameter / argument | paraméter / argumentum |
| return value | visszatérési érték |
| type | típus |
| generic | generikus |
| generic type parameter | generikus típusparaméter |
| monomorphization | monomorfizáció |
| reference | referencia |
| dangling reference | dangling referencia |
| pointer / raw pointer | pointer / nyers pointer |
| scope | hatókör |
| module | modul |
| package | csomag |
| path | útvonal |
| statement / expression | utasítás / kifejezés |
| loop | ciklus |
| compiler | fordító |
| to compile | fordítani |
| compile time / runtime | fordítási idő / futásidő |
| error | hiba |
| error handling | hibakezelés |
| recoverable / unrecoverable | helyrehozható / helyrehozhatatlan |
| test, unit test, integration test | teszt, egységteszt, integrációs teszt |
| assertion | állítás |
| macro | makró |
| declarative / procedural macro | deklaratív / procedurális makró |
| collection | kollekció |
| vector | vektor |
| hash map | hash map |
| iterator | iterátor |
| pattern matching | mintaillesztés |
| pattern | minta |
| refutable / irrefutable | cáfolható / cáfolhatatlan |
| arm (match arm) | ág (`match`-ág) |
| implementation, to implement | implementáció, implementálni |
| encapsulation | egységbezárás |
| inheritance | öröklődés |
| polymorphism | polimorfizmus |
| thread | szál |
| concurrency | konkurencia |
| parallelism | párhuzamosság |
| channel | csatorna |
| message passing | üzenetküldés |
| shared state | osztott állapot |
| race condition | versenyhelyzet |
| deadlock | holtpont |
| reference cycle | referenciaciklus |
| memory leak | memóriaszivárgás |
| allocate | lefoglal |
| operator overloading | operátor-túlterhelés |
| graceful shutdown | szabályos leállítás |
| documentation comment | dokumentációs komment |
| release profile | release profil |
| feature (nyelvi jellemző) | nyelvi elem, képesség |
| standard library | standard könyvtár |

## Stílus

- Idézőjel: magyar „…” idézőjel a prózában; a kódban maradnak az eredeti jelek.
- Az `_ownership_` típusú, dőlt betűs fogalombevezetéseket megtartjuk; az
  angolul maradó szakszó dőlt marad, a lefordított fogalom dőlten kapja meg a
  magyar alakot, első előfordulásnál zárójelben az angol eredetivel, ha ez
  segíti az érthetőséget.
- A `panic` igei használatát érdemes körülírni: „a program panickel” helyett
  „a program panicot vált ki” vagy „a program leáll egy panickel”.
- Kerüljük a szó szerinti, magyartalan tükörfordítást; a mondatok legyenek
  természetes magyar mondatok, de tartalmilag pontosak.
