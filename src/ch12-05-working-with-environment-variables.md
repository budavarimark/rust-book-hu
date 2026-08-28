## Munka környezeti változókkal

A `minigrep` binárisunkat egy extra képességgel javítjuk fel: a
kis- és nagybetűt nem megkülönböztető kereséssel, amelyet a felhasználó egy
környezeti változóval kapcsolhat be. Ezt a képességet parancssori opcióként is
megvalósíthatnánk, és megkövetelhetnénk, hogy a felhasználók minden alkalommal
megadják, amikor élni akarnak vele, de ha inkább környezeti változót
csinálunk belőle, akkor a felhasználóink egyszer beállíthatják a környezeti
változót, és abban a terminál-munkamenetben az összes keresésük kis- és
nagybetűt nem megkülönböztető lesz.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Elbukó teszt írása a kis- és nagybetűt nem megkülönböztető kereséshez

Először egy új `search_case_insensitive` függvényt adunk a `minigrep`
könyvtárhoz, amelyet akkor hívunk meg, ha a környezeti változónak van értéke.
Továbbra is a TDD-folyamatot követjük, tehát az első lépés ismét egy elbukó
teszt megírása. Új tesztet veszünk fel az új `search_case_insensitive`
függvényhez, a régi tesztünket pedig `one_result`-ról `case_sensitive`-re
nevezzük át, hogy világosabb legyen a két teszt közötti különbség, ahogy a
12-20. listában látható.

<Listing number="12-20" file-name="src/lib.rs" caption="Új, elbukó teszt hozzáadása a kis- és nagybetűt nem megkülönböztető függvényhez, amelyet mindjárt felveszünk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Figyeld meg, hogy a régi teszt `contents` értékét is átírtuk. Felvettünk egy új
sort a `"Duct tape."` szöveggel, nagy _D_ betűvel, amely nem illeszkedhet a
`"duct"` lekérdezésre, amikor kis- és nagybetűt megkülönböztető módon
keresünk. A régi teszt ilyen módosítása segít biztosítani, hogy véletlenül se
rontsuk el a már implementált, kis- és nagybetűt megkülönböztető keresést.
Ennek a tesztnek most át kell mennie, és a kis- és nagybetűt nem
megkülönböztető kereséssel való munka során is át kell mennie.

A kis- és nagybetűt _nem_ megkülönböztető kereséshez tartozó új teszt a
`"rUsT"` lekérdezést használja. A `search_case_insensitive` függvényben,
amelyet mindjárt felveszünk, a `"rUsT"` lekérdezésnek illeszkednie kell a
nagy _R_ betűs `"Rust:"` szöveget tartalmazó sorra és a `"Trust me."` sorra is,
noha mindkettőnek más a kis- és nagybetűzése, mint a lekérdezésnek. Ez a mi
elbukó tesztünk, és fordítási hibával fog elbukni, mert még nem definiáltuk a
`search_case_insensitive` függvényt. Nyugodtan vegyél fel egy vázimplementációt,
amely mindig üres vektort ad vissza, hasonlóan ahhoz, ahogy a `search`
függvénnyel tettük a 12-16. listában, hogy lásd a teszt lefordulását és
elbukását.

### A `search_case_insensitive` függvény implementálása

A 12-21. listában látható `search_case_insensitive` függvény szinte teljesen
ugyanaz lesz, mint a `search` függvény. Az egyetlen különbség az, hogy kisbetűssé
alakítjuk a `query`-t és minden `line`-t, hogy a bemeneti argumentumok kis- és
nagybetűzésétől függetlenül ugyanolyan betűalakúak legyenek, amikor
ellenőrizzük, hogy a sor tartalmazza-e a lekérdezést.

<Listing number="12-21" file-name="src/lib.rs" caption="A `search_case_insensitive` függvény definiálása úgy, hogy összehasonlítás előtt kisbetűssé alakítja a lekérdezést és a sort">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Először kisbetűssé alakítjuk a `query` szöveget, és egy azonos nevű új
változóban tároljuk el, ezzel shadowingoljuk az eredeti `query`-t. A
`to_lowercase` meghívása a lekérdezésen azért szükséges, hogy akár `"rust"`,
akár `"RUST"`, `"Rust"` vagy `"rUsT"` a felhasználó lekérdezése, úgy kezeljük,
mintha `"rust"` lenne, és ne különböztessük meg a kis- és nagybetűket. Bár a
`to_lowercase` kezeli az alapvető Unicode-ot, nem lesz 100 százalékig pontos.
Ha valódi alkalmazást írnánk, itt egy kicsit több munkát szeretnénk elvégezni,
de ez a szakasz a környezeti változókról szól, nem a Unicode-ról, ezért itt
ennyiben hagyjuk.

Figyeld meg, hogy a `query` most `String`, nem pedig string slice, mert a
`to_lowercase` hívása új adatot hoz létre, nem pedig meglévő adatra hivatkozik.
Tegyük fel például, hogy a lekérdezés `"rUsT"`: ez a string slice nem tartalmaz
kisbetűs `u`-t vagy `t`-t, amelyet felhasználhatnánk, ezért egy új, `"rust"`-ot
tartalmazó `String`-et kell lefoglalnunk. Amikor most a `query`-t argumentumként
átadjuk a `contains` metódusnak, egy és-jelet is ki kell tennünk, mert a
`contains` szignatúrája string slice-ot vár.

Ezután felvesszük a `to_lowercase` hívását minden `line`-on, hogy minden
karaktert kisbetűssé alakítsunk. Most, hogy a `line`-t és a `query`-t is
kisbetűssé alakítottuk, a lekérdezés betűalakjától függetlenül megtaláljuk a
találatokat.

Nézzük meg, hogy ez az implementáció átmegy-e a teszteken:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Nagyszerű! Átmentek. Most hívjuk meg az új `search_case_insensitive` függvényt
a `run` függvényből. Először felveszünk egy konfigurációs opciót a `Config`
structba, amellyel váltani lehet a kis- és nagybetűt megkülönböztető, illetve
nem megkülönböztető keresés között. Ennek a mezőnek a hozzáadása fordítási
hibákat okoz, mert még sehol nem inicializáljuk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Felvettük az `ignore_case` mezőt, amely egy logikai értéket tárol. Ezután azt
akarjuk, hogy a `run` függvény ellenőrizze az `ignore_case` mező értékét, és
ennek alapján döntse el, hogy a `search` vagy a `search_case_insensitive`
függvényt hívja-e meg, ahogy a 12-22. listában látható. Ez még mindig nem
fordul le.

<Listing number="12-22" file-name="src/main.rs" caption="A `search` vagy a `search_case_insensitive` meghívása a `config.ignore_case` értéke alapján">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Végül ellenőriznünk kell a környezeti változót. A környezeti változókkal való
munkához szükséges függvények a standard könyvtár `env` moduljában találhatók,
amely a _src/main.rs_ tetején már hatókörben van. Az `env` modul `var`
függvényével fogjuk megnézni, hogy be van-e állítva bármilyen érték az
`IGNORE_CASE` nevű környezeti változóhoz, ahogy a 12-23. listában látható.

<Listing number="12-23" file-name="src/main.rs" caption="Az `IGNORE_CASE` nevű környezeti változó bármilyen értékének ellenőrzése">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Itt létrehozunk egy új változót, `ignore_case` néven. Az értékének
beállításához meghívjuk az `env::var` függvényt, és átadjuk neki az
`IGNORE_CASE` környezeti változó nevét. Az `env::var` függvény egy `Result`-ot
ad vissza, amely a sikeres `Ok` variáns lesz, és a környezeti változó értékét
tartalmazza, ha a környezeti változó bármilyen értékre be van állítva. Az `Err`
variánst adja vissza, ha a környezeti változó nincs beállítva.

A `Result`-on az `is_ok` metódust használjuk annak ellenőrzésére, hogy a
környezeti változó be van-e állítva, ami azt jelenti, hogy a programnak kis- és
nagybetűt nem megkülönböztető keresést kell végeznie. Ha az `IGNORE_CASE`
környezeti változó nincs semmire beállítva, az `is_ok` `false`-ot ad vissza, és
a program kis- és nagybetűt megkülönböztető keresést hajt végre. Nem érdekel
minket a környezeti változó _értéke_, csak az, hogy be van-e állítva vagy sem,
ezért az `is_ok`-ot használjuk, nem pedig az `unwrap`-et, az `expect`-et vagy a
`Result` bármely más, korábban látott metódusát.

Az `ignore_case` változóban lévő értéket átadjuk a `Config` példánynak, hogy a
`run` függvény kiolvashassa ezt az értéket, és eldönthesse, hogy a
`search_case_insensitive` vagy a `search` függvényt hívja-e meg, ahogy azt a
12-22. listában implementáltuk.

Próbáljuk ki! Először a környezeti változó beállítása nélkül futtatjuk a
programunkat, a `to` lekérdezéssel, amelynek minden olyan sorra illeszkednie
kell, amely csupa kisbetűvel tartalmazza a _to_ szót:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Úgy tűnik, ez továbbra is működik! Most futtassuk a programot úgy, hogy az
`IGNORE_CASE` `1`-re van állítva, de ugyanazzal a `to` lekérdezéssel:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Ha PowerShellt használsz, külön parancsként kell beállítanod a környezeti
változót és futtatnod a programot:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Ettől az `IGNORE_CASE` a shell-munkameneted hátralévő részére megmarad. A
`Remove-Item` cmdlettel lehet törölni:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Olyan sorokat kell kapnunk, amelyek tartalmazzák a _to_ szót, akár nagybetűkkel
is:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Kiváló, a _To_ szót tartalmazó sorokat is megkaptuk! A `minigrep` programunk
mostantól képes környezeti változóval vezérelt, kis- és nagybetűt nem
megkülönböztető keresésre. Most már tudod, hogyan kezeld a parancssori
argumentumokkal vagy környezeti változókkal beállított opciókat.

Egyes programok ugyanahhoz a beállításhoz argumentumokat _és_ környezeti
változókat is megengednek. Ilyen esetekben a programok eldöntik, hogy melyik
élvez elsőbbséget. Önálló gyakorlásként próbáld meg a kis- és nagybetű
megkülönböztetését parancssori argumentummal vagy környezeti változóval is
vezérelhetővé tenni. Döntsd el, hogy a parancssori argumentum vagy a környezeti
változó élvezzen-e elsőbbséget, ha a programot úgy futtatják, hogy az egyik a
kis- és nagybetűk megkülönböztetésére, a másik pedig azok figyelmen kívül
hagyására van beállítva.

A `std::env` modul még sok más hasznos képességet tartalmaz a környezeti
változók kezeléséhez: nézd meg a dokumentációját, hogy lásd, mi érhető el.
