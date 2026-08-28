## Értéklisták tárolása vektorokkal

Az első kollekciótípus, amelyet megnézünk, a `Vec<T>`, más néven vektor.
A vektorokban egyetlen adatszerkezetben több értéket is tárolhatsz, méghozzá
úgy, hogy az összes érték egymás mellé kerül a memóriában. Egy vektor csak
azonos típusú értékeket tud tárolni. Akkor hasznosak, ha van egy listányi
elemed, például egy fájl szövegsorai vagy egy bevásárlókosár tételeinek árai.

### Új vektor létrehozása

Új, üres vektort a `Vec::new` függvény hívásával hozunk létre, ahogy a 8-1.
listában látható.

<Listing number="8-1" caption="Új, üres vektor létrehozása `i32` típusú értékek tárolására">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy itt típusannotációt adtunk meg. Mivel nem szúrunk be
értékeket ebbe a vektorba, a Rust nem tudja, milyen elemeket szándékozunk
tárolni. Ez fontos szempont. A vektorok generikusok segítségével vannak
megvalósítva; azt, hogy hogyan használj generikusokat a saját típusaidhoz,
a 10. fejezetben vesszük végig. Egyelőre elég annyit tudni, hogy a standard
könyvtár által biztosított `Vec<T>` típus bármilyen típust képes tárolni.
Amikor egy adott típus tárolására hozunk létre vektort, a típust csúcsos
zárójelek között adhatjuk meg. A 8-1. listában megmondtuk a Rustnak, hogy a
`v`-ben lévő `Vec<T>` `i32` típusú elemeket fog tárolni.

Gyakoribb, hogy kezdőértékekkel hozol létre egy `Vec<T>`-t, a Rust pedig
kikövetkezteti a tárolni kívánt érték típusát, így ritkán van szükség erre a
típusannotációra. A Rust kényelmes módon biztosítja a `vec!` makrót, amely új
vektort hoz létre a megadott értékekkel. A 8-2. lista egy új `Vec<i32>`-t hoz
létre, amely az `1`, `2` és `3` értékeket tartalmazza. Az egész szám típusa
`i32`, mert ez az alapértelmezett egész típus, ahogy azt a 3. fejezet
[„Adattípusok”][data-types]<!-- ignore --> című szakaszában tárgyaltuk.

<Listing number="8-2" caption="Értékeket tartalmazó új vektor létrehozása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Mivel kezdő `i32` értékeket adtunk meg, a Rust ki tudja következtetni, hogy a
`v` típusa `Vec<i32>`, így a típusannotációra nincs szükség. Következőnek
nézzük meg, hogyan módosíthatunk egy vektort.

### Vektor módosítása

Ha létre akarunk hozni egy vektort, majd elemeket akarunk hozzáadni, a `push`
metódust használhatjuk, ahogy a 8-3. listában látható.

<Listing number="8-3" caption="A `push` metódus használata értékek hozzáadására egy vektorhoz">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Mint minden változónál, ha meg akarjuk tudni változtatni az értékét, a `mut`
kulcsszóval módosíthatóvá kell tennünk, ahogy azt a 3. fejezetben tárgyaltuk.
A belé helyezett számok mind `i32` típusúak, és ezt a Rust kikövetkezteti az
adatokból, így nincs szükségünk a `Vec<i32>` annotációra.

### Vektorelemek olvasása

Kétféleképpen hivatkozhatunk egy vektorban tárolt értékre: indexeléssel vagy a
`get` metódussal. A következő példákban az extra érthetőség kedvéért
annotáltuk azoknak az értékeknek a típusát, amelyeket ezek a függvények
visszaadnak.

A 8-4. lista bemutatja az érték elérésének mindkét módját egy vektorban:
az indexelő szintaxist és a `get` metódust.

<Listing number="8-4" caption="Indexelő szintaxis és a `get` metódus használata egy vektorbeli elem eléréséhez">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Figyelj meg néhány részletet. A harmadik elem megszerzéséhez a `2` indexértéket
használjuk, mert a vektorokat számokkal indexeljük, nullától kezdve. Az `&` és
a `[]` használatával referenciát kapunk az adott indexen lévő elemre. Amikor a
`get` metódust használjuk úgy, hogy az indexet argumentumként adjuk át, egy
`Option<&T>`-t kapunk, amelyet a `match`-csel használhatunk.

A Rust azért biztosít kétféle módot egy elem hivatkozására, hogy megválaszthasd,
hogyan viselkedjen a program, amikor a meglévő elemek tartományán kívüli
indexértéket próbálsz használni. Példaként nézzük meg, mi történik, ha van egy
ötelemű vektorunk, és mindkét technikával megpróbáljuk elérni a 100. indexen
lévő elemet, ahogy a 8-5. listában látható.

<Listing number="8-5" caption="Kísérlet a 100. indexen lévő elem elérésére egy ötelemű vektorban">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Amikor ezt a kódot futtatjuk, az első, `[]`-t használó módszer panicot vált ki
a programban, mert egy nem létező elemre hivatkozik. Ezt a módszert akkor
érdemes használni, ha azt szeretnéd, hogy a programod összeomoljon, ha valaki
a vektor végén túli elemet próbál elérni.

Amikor a `get` metódusnak a vektoron kívüli indexet adunk át, `None`-t ad
vissza anélkül, hogy panicot váltana ki. Akkor használd ezt a módszert, ha
normál körülmények között is előfordulhat alkalmanként, hogy a vektor
tartományán kívüli elemet érünk el. A kódodban ekkor lesz logika arra, hogy
kezelje a `Some(&element)` vagy a `None` esetet, ahogy azt a 6. fejezetben
tárgyaltuk. Az index például egy számot beíró embertől érkezhet. Ha véletlenül
túl nagy számot ad meg, és a program `None` értéket kap, megmondhatnád a
felhasználónak, hány elem van az aktuális vektorban, és adhatnál neki egy újabb
esélyt érvényes érték megadására. Ez sokkal felhasználóbarátabb lenne, mint egy
elgépelés miatt összeomlasztani a programot!

Amikor a program érvényes referenciával rendelkezik, a borrow checker
kikényszeríti az ownership- és borrowing-szabályokat (amelyeket a 4. fejezetben
vettünk át), hogy ez a referencia és a vektor tartalmára mutató bármely további
referencia érvényes maradjon. Emlékezz a szabályra, amely kimondja, hogy nem
lehet egyszerre módosítható és nem módosítható referenciád ugyanabban a
hatókörben. Ez a szabály érvényes a 8-6. listában is, ahol nem módosítható
referenciát tartunk egy vektor első elemére, és megpróbálunk egy elemet
hozzáadni a végéhez. Ez a program nem fog működni, ha később a függvényben is
hivatkozni próbálunk arra az elemre.

<Listing number="8-6" caption="Kísérlet elem hozzáadására egy vektorhoz, miközben egy elemre mutató referenciát tartunk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Ennek a kódnak a fordítása a következő hibát eredményezi:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

A 8-6. lista kódja úgy tűnhet, mintha működnie kellene: miért érdekelné az első
elemre mutató referenciát, hogy mi változik a vektor végén? Ez a hiba abból
fakad, ahogyan a vektorok működnek: mivel a vektorok az értékeket egymás mellé
helyezik a memóriában, egy új elem hozzáadása a vektor végéhez új memória
lefoglalását és a régi elemek új helyre másolását igényelheti, ha nincs elég
hely az összes elem egymás melletti elhelyezésére ott, ahol a vektor jelenleg
tárolva van. Ebben az esetben az első elemre mutató referencia felszabadított
memóriára mutatna. A borrowing-szabályok megakadályozzák, hogy a programok
ilyen helyzetbe kerüljenek.

> Megjegyzés: A `Vec<T>` típus implementációs részleteiről bővebben lásd a
> [„The Rustonomicon”][nomicon] című írást.

### Iterálás egy vektor értékein

Ha sorban el akarjuk érni egy vektor minden elemét, inkább végigiterálunk az
összes elemen, ahelyett hogy indexekkel érnénk el őket egyesével. A 8-7. lista
bemutatja, hogyan használjunk `for` ciklust ahhoz, hogy nem módosítható
referenciákat kapjunk egy `i32` értékeket tartalmazó vektor minden elemére, és
kiírjuk őket.

<Listing number="8-7" caption="Egy vektor minden elemének kiírása az elemeken `for` ciklussal végigiterálva">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Egy módosítható vektor minden elemére mutató módosítható referenciákon is
végigiterálhatunk, hogy megváltoztassuk az összes elemet. A 8-8. listában lévő
`for` ciklus `50`-et ad hozzá minden elemhez.

<Listing number="8-8" caption="Iterálás egy vektor elemeire mutató módosítható referenciákon">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Ahhoz, hogy megváltoztassuk azt az értéket, amelyre a módosítható referencia
hivatkozik, a `*` dereferáló operátort kell használnunk, hogy eljussunk az `i`
mögötti értékhez, mielőtt a `+=` operátort használhatnánk. A dereferáló
operátorról bővebben a 15. fejezet [„A referenciát követve az
értékig”][deref]<!-- ignore --> című szakaszában beszélünk.

Egy vektoron végigiterálni, akár nem módosítható, akár módosítható módon,
biztonságos a borrow checker szabályai miatt. Ha megpróbálnánk elemeket
beszúrni vagy eltávolítani a 8-7. és a 8-8. lista `for` ciklusainak
törzsében, olyan fordítási hibát kapnánk, mint amilyet a 8-6. lista kódjánál
kaptunk. A vektorra mutató referencia, amelyet a `for` ciklus tart,
megakadályozza az egész vektor egyidejű módosítását.

### Enum használata többféle típus tárolására

Egy vektor csak azonos típusú értékeket tud tárolni. Ez kényelmetlen lehet;
biztosan vannak olyan felhasználási esetek, amikor különböző típusú elemek
listáját kell tárolni. Szerencsére egy enum variánsai ugyanazon enum típus alatt
vannak definiálva, így amikor egyetlen típusra van szükségünk különböző típusú
elemek reprezentálásához, definiálhatunk és használhatunk egy enumot!

Tegyük fel például, hogy egy táblázatkezelő egyik sorából szeretnénk értékeket
kinyerni, ahol a sor egyes oszlopai egész számokat, mások lebegőpontos számokat,
megint mások pedig sztringeket tartalmaznak. Definiálhatunk egy enumot, amelynek
variánsai a különböző értéktípusokat tárolják, és az enum összes variánsa
ugyanolyan típusúnak fog számítani: az enum típusának. Ezután létrehozhatunk egy
vektort, amely ezt az enumot tárolja, és így végső soron különböző típusokat
tárol. Ezt mutatjuk be a 8-9. listában.

<Listing number="8-9" caption="Enum definiálása különböző típusú értékek egyetlen vektorban való tárolásához">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

A Rustnak fordítási időben tudnia kell, milyen típusok lesznek a vektorban,
hogy pontosan tudja, mennyi memóriára lesz szükség a heapen az egyes elemek
tárolásához. Emellett kifejezetten meg kell adnunk, milyen típusok
megengedettek ebben a vektorban. Ha a Rust megengedné, hogy egy vektor
bármilyen típust tároljon, fennállna az esélye, hogy egy vagy több típus hibát
okozna a vektor elemein végzett műveletek során. Egy enum és egy `match`
kifejezés együttes használata azt jelenti, hogy a Rust fordítási időben
biztosítja minden lehetséges eset kezelését, ahogy azt a 6. fejezetben
tárgyaltuk.

Ha nem ismered azoknak a típusoknak a teljes körét, amelyeket a program
futásidőben kap majd, hogy vektorban tárolja őket, az enumos technika nem fog
működni. Helyette használhatsz trait objectet, amelyet a 18. fejezetben veszünk
át.

Most, hogy megbeszéltük a vektorok néhány leggyakoribb felhasználási módját,
mindenképp nézd át [az API dokumentációját][vec-api]<!-- ignore --> a standard
könyvtár által a `Vec<T>`-n definiált rengeteg hasznos metódusért. Például a
`push` mellett a `pop` metódus eltávolítja és visszaadja az utolsó elemet.

### Egy vektor eldobása az elemeit is eldobja

Mint bármely más `struct`, a vektor is felszabadul, amikor kikerül a
hatóköréből, ahogy azt a 8-10. listában jelöltük.

<Listing number="8-10" caption="Annak bemutatása, hol dobódik el a vektor és az elemei">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Amikor a vektor eldobódik, az összes tartalma is eldobódik, ami azt jelenti,
hogy az általa tárolt egész számok felszabadulnak. A borrow checker biztosítja,
hogy a vektor tartalmára mutató bármely referenciát csak addig használjuk, amíg
maga a vektor érvényes.

Térjünk át a következő kollekciótípusra: a `String`-re!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
