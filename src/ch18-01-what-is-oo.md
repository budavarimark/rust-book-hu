## Az objektumorientált nyelvek jellemzői

A programozói közösségben nincs egyetértés arról, milyen képességekkel kell
rendelkeznie egy nyelvnek ahhoz, hogy objektumorientáltnak számítson. A Rustra
számos programozási paradigma hatott, köztük az OOP is; a 13. fejezetben
például a funkcionális programozásból érkező elemeket vizsgáltuk meg. Azt
mondhatjuk, hogy az OOP-nyelvekben van néhány közös jellemző – nevezetesen az
objektumok, az egységbezárás és az öröklődés. Nézzük meg, mit jelentenek ezek a
jellemzők, és hogy a Rust támogatja-e őket.

### Az objektumok adatot és viselkedést tartalmaznak

A _Design Patterns: Elements of Reusable Object-Oriented Software_ című könyv,
amelyet Erich Gamma, Richard Helm, Ralph Johnson és John Vlissides írt
(Addison-Wesley, 1994), és amelyet közkeletűen csak _a Gang of Four_
könyveként emlegetnek, az objektumorientált tervezési minták katalógusa. Az
OOP-t így definiálja:

> Az objektumorientált programok objektumokból épülnek fel. Egy **objektum**
> egybecsomagolja az adatokat és az azokon műveleteket végző eljárásokat. Az
> eljárásokat jellemzően **metódusoknak** vagy **műveleteknek** nevezzük.

E definíció szerint a Rust objektumorientált: a structoknak és az enumoknak van
adatuk, az `impl` blokkok pedig metódusokat biztosítanak a structokhoz és az
enumokhoz. Bár a metódusokkal rendelkező structokat és enumokat nem _hívjuk_
objektumnak, a Gang of Four objektumdefiníciója szerint ugyanazt a
funkcionalitást nyújtják.

### Az implementációs részleteket elrejtő egységbezárás {#encapsulation-that-hides-implementation-details}

Az OOP-hez általában társított másik szempont az _egységbezárás_
(encapsulation) gondolata, ami azt jelenti, hogy egy objektum implementációs
részletei nem érhetők el az objektumot használó kód számára. Ezért az
objektummal kizárólag a publikus API-ján keresztül lehet kapcsolatba lépni; az
objektumot használó kód nem nyúlhat bele az objektum belsejébe, és nem
változtathatja meg közvetlenül az adatait vagy a viselkedését. Ez lehetővé
teszi, hogy a programozó úgy módosítsa és refaktorálja az objektum belsejét,
hogy közben nem kell megváltoztatnia az objektumot használó kódot.

A 7. fejezetben megbeszéltük, hogyan szabályozhatjuk az egységbezárást: a `pub`
kulcsszóval eldönthetjük, hogy a kódunkban mely modulok, típusok, függvények és
metódusok legyenek publikusak, és alapértelmezés szerint minden más privát.
Definiálhatunk például egy `AveragedCollection` structot, amelynek van egy
mezője, amely `i32` értékek vektorát tartalmazza. A structnak lehet egy másik
mezője is, amely a vektorban lévő értékek átlagát tárolja, vagyis az átlagot
nem kell mindig kiszámolni, amikor valakinek szüksége van rá. Más szóval az
`AveragedCollection` gyorsítótárazza helyettünk a kiszámolt átlagot. A 18-1.
listában látható az `AveragedCollection` struct definíciója.

<Listing number="18-1" file-name="src/lib.rs" caption="Egy `AveragedCollection` struct, amely egész számok listáját és a kollekció elemeinek átlagát tartja karban">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

A struct `pub` jelölést kapott, hogy más kód is használhassa, de a structon
belüli mezők privátak maradnak. Ez ebben az esetben azért fontos, mert
biztosítani szeretnénk, hogy valahányszor egy érték bekerül a listába vagy
kikerül belőle, az átlag is frissüljön. Ezt úgy érjük el, hogy `add`, `remove`
és `average` metódusokat implementálunk a structon, ahogy a 18-2. listában
látható.

<Listing number="18-2" file-name="src/lib.rs" caption="Az `AveragedCollection` publikus `add`, `remove` és `average` metódusainak implementációi">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

A publikus `add`, `remove` és `average` metódusok az egyetlen módok arra, hogy
egy `AveragedCollection` példány adatait elérjük vagy módosítsuk. Amikor az
`add` metódussal elemet adunk a `list` mezőhöz, vagy a `remove` metódussal
eltávolítunk belőle egyet, mindkettő implementációja meghívja a privát
`update_average` metódust, amely az `average` mező frissítéséről is
gondoskodik.

A `list` és az `average` mezőt privátnak hagyjuk, hogy a külső kód semmiképp se
adhasson hozzá elemet közvetlenül a `list` mezőhöz, és ne is vehessen ki
belőle; különben az `average` mező kicsúszhatna a szinkronból, amikor a `list`
megváltozik. Az `average` metódus visszaadja az `average` mezőben lévő értéket,
így a külső kód olvashatja az `average` értékét, de nem módosíthatja.

Mivel az `AveragedCollection` struct implementációs részleteit egységbe zártuk,
a jövőben könnyen megváltoztathatunk bizonyos dolgokat, például az adott
adatszerkezetet. Használhatnánk mondjuk `HashSet<i32>` típust `Vec<i32>`
helyett a `list` mezőhöz. Amíg a publikus `add`, `remove` és `average`
metódusok szignatúrája változatlan marad, az `AveragedCollection`-t használó
kódot nem kell módosítani. Ha ehelyett a `list` mezőt tettük volna publikussá,
ez nem feltétlenül lenne igaz: a `HashSet<i32>` és a `Vec<i32>` más metódusokat
kínál az elemek hozzáadására és eltávolítására, így a külső kódot
valószínűleg módosítani kellene, ha közvetlenül a `list` mezőt változtatná.

Ha az egységbezárás elengedhetetlen ahhoz, hogy egy nyelvet
objektumorientáltnak tekintsünk, akkor a Rust megfelel ennek a
követelménynek. Az a lehetőség, hogy a kód különböző részeinél használjuk-e a
`pub` kulcsszót vagy sem, lehetővé teszi az implementációs részletek
egységbezárását.

### Az öröklődés mint típusrendszerbeli eszköz és mint kódmegosztás

Az _öröklődés_ olyan mechanizmus, amelynek révén egy objektum elemeket örökölhet
egy másik objektum definíciójából, és így megkapja a szülőobjektum adatait és
viselkedését anélkül, hogy neked újra definiálnod kellene őket.

Ha egy nyelvnek öröklődéssel kell rendelkeznie ahhoz, hogy objektumorientált
legyen, akkor a Rust nem ilyen nyelv. Nincs mód arra, hogy makró használata
nélkül olyan structot definiálj, amely örökli a szülőstruct mezőit és
metódusimplementációit.

Ha azonban hozzászoktál ahhoz, hogy az öröklődés is ott van a programozói
eszköztáradban, a Rustban más megoldásokat használhatsz attól függően, hogy
eredetileg miért nyúltál volna az öröklődéshez.

Két fő okból választanád az öröklődést. Az egyik a kód újrafelhasználása:
megvalósíthatsz egy adott viselkedést az egyik típusra, és az öröklődés
lehetővé teszi, hogy ugyanezt az implementációt egy másik típusnál is
felhasználd. Rust-kódban ezt korlátozott mértékben megteheted az alapértelmezett
trait-metódusimplementációkkal, amelyeket a 10-14. listában láttál, amikor
alapértelmezett implementációt adtunk a `Summary` trait `summarize`
metódusához. Minden olyan típusnak, amely implementálja a `Summary` trait-et,
minden további kód nélkül rendelkezésére áll a `summarize` metódus. Ez ahhoz
hasonlít, mint amikor egy szülőosztály tartalmazza egy metódus
implementációját, és az örökítő gyermekosztály is rendelkezik a metódus
implementációjával. Ráadásul felül is írhatjuk a `summarize` metódus
alapértelmezett implementációját, amikor implementáljuk a `Summary` trait-et,
ami hasonló ahhoz, mint amikor egy gyermekosztály felülírja egy
szülőosztálytól örökölt metódus implementációját.

Az öröklődés használatának másik oka a típusrendszerhez kapcsolódik: ahhoz,
hogy egy gyermektípust ugyanazokon a helyeken lehessen használni, ahol a
szülőtípust. Ezt _polimorfizmusnak_ is nevezik, ami azt jelenti, hogy több
objektum futásidőben behelyettesíthető egymással, ha bizonyos közös
jellemzőkkel bírnak.

> ### Polimorfizmus
>
> Sokak számára a polimorfizmus egyet jelent az öröklődéssel. Valójában
> azonban ez általánosabb fogalom, amely olyan kódra utal, amely többféle típusú
> adattal is képes dolgozni. Az öröklődés esetén ezek a típusok többnyire
> alosztályok.
>
> A Rust ehelyett generikusokat használ arra, hogy elvonatkoztasson a
> lehetséges típusoktól, és trait boundokat arra, hogy megszabja, mit kell
> nyújtaniuk ezeknek a típusoknak. Ezt néha _korlátozott parametrikus
> polimorfizmusnak_ nevezik.

A Rust más kompromisszumokat választott azzal, hogy nem kínál öröklődést. Az
öröklődésnél gyakran fennáll a veszélye, hogy a szükségesnél több kódot
osztunk meg. Az alosztályoknak nem mindig kellene a szülőosztályuk összes
jellemzőjén osztozniuk, de az öröklődéssel mégis így lesz. Ez rugalmatlanabbá
teheti a program felépítését. Ráadásul megnyitja a lehetőséget arra, hogy az
alosztályokon olyan metódusokat hívjunk meg, amelyeknek nincs értelmük, vagy
hibát okoznak, mert nem alkalmazhatók az adott alosztályra. Emellett néhány
nyelv csak az _egyszeres öröklődést_ engedi meg (vagyis egy alosztály csak egy
osztálytól örökölhet), tovább korlátozva a program felépítésének rugalmasságát.

Ezen okok miatt a Rust más megközelítést választ: az öröklődés helyett trait
objecteket használ, hogy futásidőben polimorfizmust érjen el. Nézzük meg,
hogyan működnek a trait objectek.
