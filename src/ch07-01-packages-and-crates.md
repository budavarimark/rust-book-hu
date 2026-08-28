## Csomagok és crate-ek

A modulrendszer első részei, amelyeket áttekintünk, a csomagok és a crate-ek.

A _crate_ a legkisebb kódmennyiség, amelyet a Rust fordító egyszerre figyelembe
vesz. Még ha a `cargo` helyett a `rustc`-t futtatod, és egyetlen forrásfájlt
adsz át neki (ahogy még az 1. fejezet [„A Rust-programok alapjai”][basics]<!--
ignore --> szakaszában tettük), a fordító azt a fájlt is crate-nek tekinti. A
crate-ek modulokat tartalmazhatnak, a modulok pedig definiálhatók más
fájlokban is, amelyek a crate-tel együtt fordulnak le, ahogy a következő
szakaszokban látni fogjuk.

Egy crate kétféle alakban létezhet: binary crate vagy library crate. A _binary
crate_-ek olyan programok, amelyeket futtatható állománnyá fordíthatsz és
futtathatsz, például parancssori program vagy szerver. Mindegyiknek
rendelkeznie kell egy `main` nevű függvénnyel, amely megadja, mi történjen a
futtatható állomány indításakor. Az eddig létrehozott crate-jeink mind binary
crate-ek voltak.

A _library crate_-eknek nincs `main` függvényük, és nem fordulnak futtatható
állománnyá. Ehelyett olyan funkcionalitást definiálnak, amelyet több projekt
között szánnak megosztásra. Például a [2. fejezetben][rand]<!-- ignore -->
használt `rand` crate véletlen számok előállítására szolgáló funkcionalitást
nyújt. A rustaceanek legtöbbször library crate-re gondolnak, amikor azt
mondják, „crate”, és a „crate” szót a „könyvtár” általános programozási
fogalmával felváltva használják.

A _crate root_ az a forrásfájl, amelyből a Rust fordító kiindul, és amely a
crate-ed gyökérmodulját alkotja (a modulokat részletesen a [„Hatókör és
láthatóság szabályozása modulokkal”][modules]<!-- ignore --> szakaszban
mutatjuk be).

A _csomag_ egy vagy több crate-ből álló köteg, amely funkcionalitások egy
halmazát nyújtja. Egy csomag tartalmaz egy _Cargo.toml_ fájlt, amely leírja,
hogyan kell felépíteni ezeket a crate-eket. A Cargo valójában maga is egy csomag, amely
annak a parancssori eszköznek a binary crate-jét tartalmazza, amelyet a kódod
építéséhez használsz. A Cargo csomag egy library crate-et is tartalmaz, amelytől
a binary crate függ. Más projektek is függhetnek a Cargo library crate-jétől,
ha ugyanazt a logikát akarják használni, mint amit a Cargo parancssori eszköze
használ.

Egy csomag tetszőleges számú binary crate-et tartalmazhat, de legfeljebb egy
library crate-et. Egy csomagnak legalább egy crate-et tartalmaznia kell,
mindegy, hogy az library vagy binary crate.

Nézzük végig, mi történik, amikor létrehozunk egy csomagot. Először beírjuk a
`cargo new my-project` parancsot:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Miután lefuttattuk a `cargo new my-project` parancsot, az `ls` paranccsal
megnézzük, mit hoz létre a Cargo. A _my-project_ könyvtárban van egy
_Cargo.toml_ fájl, amely csomaggá teszi. Van egy _src_ könyvtár is, amely a
_main.rs_ fájlt tartalmazza. Nyisd meg a _Cargo.toml_ fájlt a
szövegszerkesztődben, és vedd észre, hogy sehol nem esik szó az _src/main.rs_
fájlról. A Cargo azt a konvenciót követi, hogy az _src/main.rs_ annak a binary
crate-nek a crate rootja, amelynek neve megegyezik a csomagéval. Hasonlóképpen
a Cargo tudja, hogy ha a csomag könyvtára tartalmaz _src/lib.rs_ fájlt, akkor a
csomag tartalmaz egy, a csomaggal azonos nevű library crate-et, és az
_src/lib.rs_ annak a crate rootja. A Cargo átadja a crate root fájlokat a
`rustc`-nek, hogy felépítse a könyvtárat vagy a binary állományt.

Itt egy olyan csomagunk van, amely csak az _src/main.rs_ fájlt tartalmazza,
vagyis csak egy `my-project` nevű binary crate-et. Ha egy csomag tartalmaz
_src/main.rs_ és _src/lib.rs_ fájlt is, akkor két crate-je van: egy binary és
egy library crate, mindkettő a csomaggal azonos néven. Egy csomagnak több
binary crate-je is lehet, ha fájlokat helyezel az _src/bin_ könyvtárba: minden
fájl külön binary crate lesz.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
