## Változók és módosíthatóság {#variables-and-mutability}

Ahogy azt az [„Értékek tárolása
változókban”][storing-values-with-variables]<!-- ignore --> című részben
említettük, a változók alapértelmezés szerint nem módosíthatók. Ez egyike a
Rust számos finom ösztönzésének arra, hogy úgy írd a kódodat, hogy kihasználd
az általa nyújtott biztonságot és a könnyű konkurenciát. Ugyanakkor továbbra is
lehetőséged van módosíthatóvá tenni a változóidat. Nézzük meg, hogyan és miért
bátorít a Rust arra, hogy a módosíthatatlanságot részesítsd előnyben, és miért
akarhatsz mégis néha eltérni ettől.

Ha egy változó nem módosítható, akkor amint egy érték hozzákötődik egy névhez,
azt az értéket többé nem tudod megváltoztatni. Ennek szemléltetéséhez hozz
létre egy _variables_ nevű új projektet a _projects_ könyvtáradban a `cargo new
variables` paranccsal.

Ezután az új _variables_ könyvtáradban nyisd meg a _src/main.rs_ fájlt, és
cseréld le a kódját az alábbira, amely egyelőre nem fordul le:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Mentsd el, és futtasd a programot a `cargo run` paranccsal. Egy
módosíthatatlansági hibáról szóló hibaüzenetet kell kapnod, ahogy az alábbi
kimenetben látszik:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Ez a példa megmutatja, hogyan segít a fordító megtalálni a hibákat a
programjaidban. A fordítói hibák bosszantóak lehetnek, de valójában csak azt
jelentik, hogy a programod még nem biztonságosan azt csinálja, amit szeretnél;
_nem_ azt jelentik, hogy rossz programozó vagy! A tapasztalt rustaceanök is
kapnak fordítói hibákat.

Azért kaptad a `` cannot assign twice to immutable variable `x` `` hibaüzenetet, mert egy második értéket próbáltál adni a nem módosítható `x` változónak.

Fontos, hogy fordítási idejű hibát kapjunk, amikor egy módosíthatatlannak
jelölt értéket próbálunk megváltoztatni, mert éppen az ilyen helyzetek
vezethetnek bugokhoz. Ha a kódunk egyik része arra a feltevésre épül, hogy egy
érték sohasem változik meg, egy másik része viszont megváltoztatja azt, akkor
könnyen előfordulhat, hogy az első rész nem azt teszi, amire terveztük. Az
ilyen bugok okát utólag nehéz lehet felderíteni, különösen akkor, ha a második
kódrészlet csak _néha_ változtatja meg az értéket. A Rust fordítója garantálja,
hogy ha kijelented, hogy egy érték nem fog változni, akkor az tényleg nem fog
változni, így neked nem kell ezt fejben tartanod. A kódodról ezáltal könnyebb
gondolkodni.

A módosíthatóság azonban nagyon hasznos lehet, és kényelmesebbé teheti a kód
írását. Bár a változók alapértelmezés szerint nem módosíthatók, módosíthatóvá
teheted őket, ha a változó neve elé írod a `mut` kulcsszót, ahogy a [2.
fejezetben][storing-values-with-variables]<!-- ignore --> tetted. A `mut`
hozzáadása egyben a szándékot is közvetíti a kód későbbi olvasói felé, jelezve,
hogy a kód más részei meg fogják változtatni ennek a változónak az értékét.

Módosítsuk például a _src/main.rs_ fájlt a következőre:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Ha most futtatjuk a programot, ezt kapjuk:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

A `mut` használatával megengedett, hogy az `x`-hez kötött értéket `5`-ről
`6`-ra változtassuk. Végső soron rajtad múlik, hogy használsz-e
módosíthatóságot, és attól függ, hogy az adott helyzetben mit tartasz a
legvilágosabbnak.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Konstansok deklarálása {#declaring-constants}

A módosíthatatlan változókhoz hasonlóan a _konstansok_ is olyan értékek,
amelyek egy névhez vannak kötve, és nem változhatnak meg, de van néhány
különbség a konstansok és a változók között.

Először is, a konstansoknál nem használhatsz `mut`-ot. A konstansok nem
egyszerűen alapértelmezés szerint módosíthatatlanok – mindig azok. A
konstansokat a `let` kulcsszó helyett a `const` kulcsszóval deklarálod, és az
érték típusát _kötelező_ megadni. A típusokkal és a típusannotációkkal a
következő részben, az [„Adattípusok”][data-types]<!-- ignore --> címűben
foglalkozunk, úgyhogy a részletek miatt egyelőre ne aggódj. Egyelőre elég
annyi, hogy a típust mindig meg kell adnod.

Konstansokat bármelyik hatókörben deklarálhatsz, a globális hatókörben is, ami
hasznossá teszi őket olyan értékekhez, amelyekről a kód sok részének tudnia
kell.

Az utolsó különbség az, hogy a konstansok értéke csak konstans kifejezés lehet,
nem pedig olyan érték eredménye, amelyet csak futásidőben lehetne kiszámítani.

Íme egy példa egy konstans deklarációjára:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

A konstans neve `THREE_HOURS_IN_SECONDS`, az értéke pedig 60 (az egy percben
lévő másodpercek száma) szorozva 60-nal (az egy órában lévő percek száma)
szorozva 3-mal (ahány órát ebben a programban számolni akarunk). A Rust
elnevezési konvenciója szerint a konstansok neve csupa nagybetűs, a szavak
között alulvonással. A fordító képes bizonyos műveletek szűk körét fordítási
időben kiértékelni, ami lehetővé teszi, hogy ezt az értéket a 10 800 helyett
egy könnyebben érthető és ellenőrizhető módon írjuk le. Arról, hogy konstansok
deklarálásakor milyen műveletek használhatók, a [Rust Reference konstans
kiértékelésről szóló részében][const-eval] találsz további információt.

A konstansok a program teljes futása alatt érvényesek, azon a hatókörön belül,
amelyben deklarálták őket. Ez a tulajdonság hasznossá teszi a konstansokat
olyan, az alkalmazási területedhez tartozó értékekhez, amelyekről a program
több részének is tudnia kell, például hogy egy játék játékosa legfeljebb hány
pontot szerezhet, vagy hogy mekkora a fény sebessége.

Hasznos, ha a programban végig használt, bedrótozott értékeket konstansként
nevezzük el, mert így közvetítjük az érték jelentését a kód későbbi
karbantartóinak. Abban is segít, hogy a kódnak csak egyetlen olyan pontja
legyen, amelyet módosítani kell, ha a bedrótozott értéket a jövőben frissíteni
kellene.

### Shadowing {#shadowing}

Ahogy a [2. fejezet][comparing-the-guess-to-the-secret-number]<!-- ignore -->
kitalálós játékos oktatóanyagában láttad, deklarálhatsz egy új változót
ugyanazzal a névvel, mint egy korábbi változóé. A rustaceanök azt mondják, hogy
az első változót _shadowingolja_ (árnyékolja) a második, ami azt jelenti, hogy
a fordító a második változót fogja látni, amikor a változó nevét használod.
Gyakorlatilag a második változó beárnyékolja az elsőt, és magára veszi a
változónév minden használatát egészen addig, amíg őt magát nem árnyékolják, vagy
a hatókör véget nem ér. Egy változót úgy tudunk shadowingolni, hogy ugyanazt a
változónevet használjuk, és megismételjük a `let` kulcsszó használatát, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Ez a program először az `x`-et köti az `5` értékhez. Ezután a `let x =`
megismétlésével létrehoz egy új `x` változót: veszi az eredeti értéket, és
hozzáad `1`-et, így az `x` értéke `6` lesz. Ezután a kapcsos zárójelekkel
létrehozott belső hatókörben a harmadik `let` utasítás szintén shadowingolja az
`x`-et, és új változót hoz létre: az előző értéket megszorozza `2`-vel, így az
`x` értéke `12` lesz. Amikor ez a hatókör véget ér, a belső shadowing is
megszűnik, és az `x` visszatér a `6` értékhez. Ha futtatjuk ezt a programot, a
következőt írja ki:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

A shadowing más, mint egy változó `mut`-tal való megjelölése, mert fordítási
idejű hibát kapunk, ha véletlenül a `let` kulcsszó nélkül próbálunk új értéket
adni ennek a változónak. A `let` használatával elvégezhetünk néhány
átalakítást egy értéken, de az átalakítások befejeztével a változó
módosíthatatlan lesz.

A másik különbség a `mut` és a shadowing között az, hogy mivel a `let` kulcsszó
újbóli használatakor gyakorlatilag egy új változót hozunk létre,
megváltoztathatjuk az érték típusát, miközben ugyanazt a nevet használjuk újra.
Tegyük fel például, hogy a programunk megkéri a felhasználót, hogy szóköz
karakterek beírásával adja meg, hány szóközt szeretne valamilyen szöveg között,
majd ezt a bemenetet számként akarjuk tárolni:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Az első `spaces` változó string típusú, a második `spaces` változó pedig szám
típusú. A shadowing tehát megkímél minket attól, hogy különböző neveket kelljen
kitalálnunk, például `spaces_str`-t és `spaces_num`-ot; ehelyett újra
használhatjuk az egyszerűbb `spaces` nevet. Ha viszont `mut`-ot próbálunk erre
használni, ahogy itt látható, fordítási idejű hibát kapunk:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

A hiba azt mondja, hogy nem változtathatjuk meg egy változó típusát:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Most, hogy megnéztük, hogyan működnek a változók, vegyük szemügyre a további
adattípusokat, amelyeket felvehetnek.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html
