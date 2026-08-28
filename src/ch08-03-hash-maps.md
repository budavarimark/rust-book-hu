## Kulcsok és hozzájuk tartozó értékek tárolása hash mapekben

Gyakori kollekcióink közül az utolsó a hash map. A `HashMap<K, V>` típus `K`
típusú kulcsok `V` típusú értékekre való leképezését tárolja egy _hash függvény_
segítségével, amely meghatározza, hogyan helyezi el ezeket a kulcsokat és
értékeket a memóriában. Sok programozási nyelv támogatja ezt a fajta
adatszerkezetet, de gyakran más néven, például _hash_, _map_, _object_, _hash
table_, _dictionary_ vagy _asszociatív tömb_ néven, hogy csak néhányat
említsünk.

A hash mapek akkor hasznosak, ha nem index alapján akarsz adatot kikeresni –
ahogy azt a vektoroknál teheted –, hanem egy tetszőleges típusú kulcs alapján.
Egy játékban például egy hash mapben tarthatnád nyilván az egyes csapatok
pontszámát, ahol minden kulcs egy csapat neve, az értékek pedig az egyes
csapatok pontszámai. Egy csapatnév alapján lekérdezheted a pontszámát.

Ebben a szakaszban a hash mapek alapvető API-ját vesszük végig, de sokkal több
finomság rejtőzik a standard könyvtár által a `HashMap<K, V>`-n definiált
függvényekben. Mint mindig, további információért nézd meg a standard könyvtár
dokumentációját.

### Új hash map létrehozása

Üres hash mapet létrehozni például a `new` használatával lehet, elemeket pedig
az `insert`tel adhatunk hozzá. A 8-20. listában két csapat pontszámát tartjuk
nyilván, a csapatok neve _Blue_ és _Yellow_. A Blue csapat 10 ponttal indul, a
Yellow csapat pedig 50-nel.

<Listing number="8-20" caption="Új hash map létrehozása és néhány kulcs-érték pár beszúrása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy először `use`-olnunk kell a `HashMap`-et a standard könyvtár
kollekciókat tartalmazó részéből. Három gyakori kollekciónk közül ezt használják
a legritkábban, ezért nincs benne azokban a nyelvi elemekben, amelyeket a prelude
automatikusan behoz a hatókörbe. A hash mapek kevesebb támogatást is kapnak a
standard könyvtártól; például nincs beépített makró a létrehozásukra.

A vektorokhoz hasonlóan a hash mapek is a heapen tárolják az adataikat. Ennek a
`HashMap`-nek `String` típusú kulcsai és `i32` típusú értékei vannak. A
vektorokhoz hasonlóan a hash mapek is homogének: minden kulcsnak azonos típusúnak
kell lennie, és minden értéknek is azonos típusúnak kell lennie.

### Értékek elérése egy hash mapben {#accessing-values-in-a-hash-map}

Egy értéket úgy kaphatunk meg a hash mapből, hogy a kulcsát átadjuk a `get`
metódusnak, ahogy a 8-21. listában látható.

<Listing number="8-21" caption="A hash mapben tárolt Blue csapat pontszámának elérése">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Itt a `score` a Blue csapathoz társított értéket fogja tartalmazni, az eredmény
pedig `10` lesz. A `get` metódus egy `Option<&V>`-t ad vissza; ha az adott
kulcshoz nincs érték a hash mapben, a `get` `None`-t ad vissza. Ez a program úgy
kezeli az `Option`-t, hogy meghívja a `copied` metódust, hogy `Option<&i32>`
helyett `Option<i32>`-t kapjon, majd az `unwrap_or`-t, hogy a `score` nulla
legyen, ha a `scores`-ban nincs bejegyzés a kulcshoz.

Egy hash map minden kulcs-érték párján hasonló módon iterálhatunk végig, mint a
vektoroknál, egy `for` ciklussal:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Ez a kód tetszőleges sorrendben írja ki a párokat:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Az ownership kezelése hash mapekben

Azoknál a típusoknál, amelyek implementálják a `Copy` traitet – például az
`i32`-nél –, az értékek bemásolódnak a hash mapbe. A tulajdonolt értékek, mint a
`String`, bemozdulnak, és a hash map lesz ezeknek az értékeknek az ownere, ahogy
azt a 8-22. lista bemutatja.

<Listing number="8-22" caption="Annak bemutatása, hogy a kulcsok és az értékek beszúrás után a hash map tulajdonába kerülnek">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

A `field_name` és a `field_value` változókat nem tudjuk használni azután, hogy
az `insert` hívásával bemozdultak a hash mapbe.

Ha értékekre mutató referenciákat szúrunk be a hash mapbe, az értékek nem
mozdulnak be a hash mapbe. Azoknak az értékeknek, amelyekre a referenciák
mutatnak, legalább addig érvényesnek kell maradniuk, amíg a hash map érvényes.
Ezekről a kérdésekről bővebben a 10. fejezet [„Referenciák érvényesítése
lifetime-okkal”][validating-references-with-lifetimes]<!-- ignore --> című
szakaszában beszélünk.

### Egy hash map módosítása

Bár a kulcs-érték párok száma növelhető, minden egyedi kulcshoz egyszerre csak
egy érték tartozhat (fordítva viszont nem: például a Blue csapathoz és a Yellow
csapathoz is tartozhat a `10` érték a `scores` hash mapben).

Amikor meg akarod változtatni egy hash map adatait, el kell döntened, hogyan
kezeled azt az esetet, amikor egy kulcshoz már tartozik érték. Lecserélheted a
régi értéket az újra, teljesen figyelmen kívül hagyva a régit. Megtarthatod a
régi értéket, és figyelmen kívül hagyhatod az újat, csak akkor adva hozzá az új
értéket, ha a kulcshoz _még nem_ tartozik érték. Vagy kombinálhatod a régi és az
új értéket. Nézzük meg, hogyan csináljuk mindezt!

#### Egy érték felülírása

Ha beszúrunk egy kulcsot és egy értéket egy hash mapbe, majd ugyanazt a kulcsot
egy másik értékkel szúrjuk be, az adott kulcshoz tartozó érték lecserélődik.
Bár a 8-23. lista kódja kétszer hívja meg az `insert`et, a hash map csak egy
kulcs-érték párt fog tartalmazni, mert mindkétszer a Blue csapat kulcsához
tartozó értéket szúrjuk be.

<Listing number="8-23" caption="Adott kulccsal tárolt érték lecserélése">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Ez a kód a `{"Blue": 25}` értéket írja ki. Az eredeti `10` érték felülíródott.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Kulcs és érték hozzáadása csak akkor, ha a kulcs még nincs jelen

Gyakori, hogy megnézzük, létezik-e már egy adott kulcs értékkel a hash mapben,
majd a következőképpen járunk el: ha a kulcs létezik a hash mapben, a meglévő
érték maradjon úgy, ahogy van; ha a kulcs nem létezik, szúrjuk be a kulcsot és
egy hozzá tartozó értéket.

A hash mapeknek van erre egy speciális API-juk, az `entry`, amely paraméterként
azt a kulcsot várja, amelyet ellenőrizni szeretnél. Az `entry` metódus
visszatérési értéke egy `Entry` nevű enum, amely egy olyan értéket reprezentál,
amely létezhet, de az is lehet, hogy nem. Tegyük fel, hogy meg akarjuk nézni,
tartozik-e érték a Yellow csapat kulcsához. Ha nem, be akarjuk szúrni az `50`
értéket, és ugyanezt szeretnénk a Blue csapatnál is. Az `entry` API-t használva
a kód a 8-24. listában láthatóan alakul.

<Listing number="8-24" caption="Az `entry` metódus használata, hogy csak akkor szúrjunk be, ha a kulcshoz még nem tartozik érték">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Az `Entry` `or_insert` metódusa úgy van definiálva, hogy módosítható referenciát
adjon vissza a megfelelő `Entry`-kulcshoz tartozó értékre, ha az a kulcs létezik,
ha pedig nem, akkor a paramétert szúrja be az adott kulcs új értékeként, és
módosítható referenciát ad vissza az új értékre. Ez a technika sokkal tisztább,
mintha magunk írnánk meg a logikát, ráadásul jobban kijön a borrow checkerrel is.

A 8-24. lista kódjának futtatása a `{"Yellow": 50, "Blue": 10}` értéket írja ki.
Az `entry` első hívása beszúrja a Yellow csapat kulcsát az `50` értékkel, mert a
Yellow csapatnak még nincs értéke. Az `entry` második hívása nem változtatja meg
a hash mapet, mert a Blue csapatnak már van `10` értéke.

#### Egy érték frissítése a régi érték alapján

A hash mapek másik gyakori felhasználási módja, hogy kikeressük egy kulcs
értékét, majd a régi érték alapján frissítjük. A 8-25. lista például olyan kódot
mutat, amely megszámolja, hányszor fordul elő az egyes szó egy szövegben. Egy
hash mapet használunk, amelyben a szavak a kulcsok, és növeljük az értéket, hogy
nyilvántartsuk, hányszor láttuk az adott szót. Ha először látunk egy szót, előbb
beszúrjuk a `0` értéket.

<Listing number="8-25" caption="Szavak előfordulásainak számolása szavakat és darabszámokat tároló hash map segítségével">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Ez a kód a `{"world": 2, "hello": 1, "wonderful": 1}` értéket írja ki.
Előfordulhat, hogy ugyanazok a kulcs-érték párok más sorrendben jelennek meg:
emlékezz vissza az [„Értékek elérése egy hash mapben”][access]<!-- ignore -->
szakaszra, amely szerint egy hash mapen tetszőleges sorrendben iterálunk végig.

A `split_whitespace` metódus egy iterátort ad vissza a `text` értékének
whitespace-ekkel elválasztott részszeletein. Az `or_insert` metódus módosítható
referenciát (`&mut V`) ad vissza a megadott kulcshoz tartozó értékre. Itt ezt a
módosítható referenciát a `count` változóban tároljuk, így ahhoz, hogy értéket
adjunk neki, előbb dereferálnunk kell a `count`-ot a csillag (`*`) segítségével.
A módosítható referencia a `for` ciklus végén kikerül a hatóköréből, így ezek a
változtatások mind biztonságosak, és a borrowing-szabályok megengedik őket.

### Hash függvények

Alapértelmezés szerint a `HashMap` egy _SipHash_ nevű hash függvényt használ,
amely ellenállást nyújt a hash táblákat érintő szolgáltatásmegtagadási (DoS)
támadásokkal szemben[^siphash]<!-- ignore -->. Ez nem a leggyorsabb elérhető
hash algoritmus, de a teljesítménycsökkenésért cserébe kapott jobb biztonság
megéri. Ha profilozod a kódodat, és azt látod, hogy az alapértelmezett hash
függvény túl lassú a céljaidhoz, átválthatsz egy másik függvényre egy másik
hasher megadásával. A _hasher_ olyan típus, amely implementálja a `BuildHasher`
traitet. A traitekről és arról, hogyan implementáljuk őket, a [10.
fejezetben][traits]<!-- ignore --> beszélünk. Nem feltétlenül kell a nulláról
megírnod a saját hasheredet; a [crates.io](https://crates.io/)<!-- ignore -->
oldalon más Rust-felhasználók által megosztott könyvtárak érhetők el, amelyek sok
elterjedt hash algoritmust megvalósító hashereket biztosítanak.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Összefoglalás

A vektorok, a sztringek és a hash mapek nagyon sok olyan funkcionalitást
biztosítanak, amelyre a programokban szükség van, amikor adatokat kell tárolni,
elérni és módosítani. Íme néhány gyakorlat, amelyek megoldásához most már meg
kell lennie az eszközeidnek:

1. Egy egész számokból álló lista esetén használj vektort, és add vissza a lista
   mediánját (rendezés után a középső pozícióban lévő érték) és móduszát (a
   leggyakrabban előforduló érték; ehhez egy hash map lesz hasznos).
1. Alakítsd át a sztringeket Pig Latinre. Minden szó első mássalhangzója a szó
   végére kerül, és hozzáadjuk az _ay_ végződést, így a _first_ szóból
   _irst-fay_ lesz. A magánhangzóval kezdődő szavak helyett a _hay_ végződést
   kapják a végükre (az _apple_ szóból _apple-hay_ lesz). Ne feledkezz meg az
   UTF-8 kódolás részleteiről!
1. Egy hash map és vektorok segítségével készíts szöveges felületet, amely
   lehetővé teszi a felhasználónak, hogy alkalmazottak nevét adja hozzá egy
   vállalat valamelyik részlegéhez; például „Add Sally to Engineering” vagy „Add
   Amir to Sales”. Ezután engedd, hogy a felhasználó lekérje egy részleg összes
   emberének listáját vagy a vállalat összes emberét részlegek szerint, ábécé
   sorrendbe rendezve.

A standard könyvtár API-dokumentációja leírja azokat a metódusokat, amelyekkel a
vektorok, a sztringek és a hash mapek rendelkeznek, és amelyek hasznosak lesznek
ezekhez a gyakorlatokhoz!

Egyre összetettebb programok felé haladunk, amelyekben a műveletek meghiúsulhatnak,
így ez tökéletes alkalom arra, hogy a hibakezelésről beszéljünk. Ez lesz a
következő téma!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
