# Generikus típusok, trait-ek és lifetime-ok

Minden programozási nyelvben vannak eszközök a fogalmak ismétlődésének hatékony
kezelésére. A Rustban az egyik ilyen eszköz a _generikusok_: absztrakt
helyettesítők konkrét típusok vagy más tulajdonságok helyett. Ki tudjuk fejezni
a generikusok viselkedését, illetve azt, hogyan viszonyulnak más
generikusokhoz, anélkül hogy tudnánk, mi kerül a helyükre a kód fordításakor és
futtatásakor.

A függvények valamilyen generikus típusú paramétert is átvehetnek olyan konkrét
típus helyett, mint az `i32` vagy a `String`, ugyanúgy, ahogy ismeretlen értékű
paramétereket vesznek át, hogy ugyanazt a kódot több konkrét értéken
futtathassák. Valójában már használtunk generikusokat: a 6. fejezetben az
`Option<T>`-vel, a 8. fejezetben a `Vec<T>`-vel és a `HashMap<K, V>`-vel, a 9.
fejezetben pedig a `Result<T, E>`-vel. Ebben a fejezetben azt fedezed fel,
hogyan definiálhatsz saját típusokat, függvényeket és metódusokat
generikusokkal!

Először átnézzük, hogyan emelhetünk ki egy függvényt a kódismétlés
csökkentésére. Ezután ugyanezzel a technikával generikus függvényt készítünk két
olyan függvényből, amelyek csak a paramétereik típusában különböznek.
Elmagyarázzuk azt is, hogyan használhatunk generikus típusokat struct- és
enum-definíciókban.

Utána megtanulod, hogyan definiálhatsz viselkedést generikus módon a trait-ek
segítségével. A trait-eket kombinálhatod generikus típusokkal, hogy egy
generikus típust úgy szoríts meg, hogy csak azokat a típusokat fogadja el,
amelyek egy adott viselkedéssel rendelkeznek, ne pedig bármelyik típust.

Végül a _lifetime_-okról lesz szó: ezek a generikusok egy fajtája, amely
információt ad a fordítónak arról, hogyan viszonyulnak egymáshoz a referenciák.
A lifetime-ok segítségével elég információt adhatunk a fordítónak a
kölcsönvett értékekről ahhoz, hogy több helyzetben is biztosítani tudja a
referenciák érvényességét, mint a segítségünk nélkül.

## Ismétlődés megszüntetése függvény kiemelésével

A generikusok révén a konkrét típusokat olyan helykitöltővel válthatjuk ki,
amely több típust képvisel, így megszüntethetjük a kódismétlést. Mielőtt
belevágnánk a generikusok szintaxisába, nézzük meg először, hogyan lehet
generikus típusok nélkül megszüntetni az ismétlődést: kiemelünk egy függvényt,
amely a konkrét értékeket olyan helykitöltővel váltja ki, amely több értéket
képvisel. Utána ugyanezt a technikát alkalmazzuk egy generikus függvény
kiemelésére! Ha látod, hogyan ismerheted fel a függvénybe kiemelhető ismétlődő
kódot, kezded majd felismerni azt az ismétlődő kódot is, amely generikusokat
használhat.

Kezdjük a 10-1. listázás rövid programjával, amely megkeresi a legnagyobb
számot egy listában.

<Listing number="10-1" file-name="src/main.rs" caption="A legnagyobb szám megkeresése egy számlistában">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Egész számok listáját tároljuk a `number_list` változóban, a lista első számára
mutató referenciát pedig egy `largest` nevű változóba tesszük. Ezután
végigmegyünk a lista összes számán, és ha az aktuális szám nagyobb, mint a
`largest`-ben tárolt szám, kicseréljük a referenciát abban a változóban. Ha
viszont az aktuális szám kisebb vagy egyenlő az eddig látott legnagyobb
számnál, a változó nem változik, és a kód továbblép a lista következő számára.
Miután a lista összes számát megvizsgáltuk, a `largest` a legnagyobb számra
hivatkozik, ami ebben az esetben a 100.

Most azt a feladatot kaptuk, hogy két különböző számlistában keressük meg a
legnagyobb számot. Ehhez választhatjuk azt, hogy megismételjük a 10-1. listázás
kódját, és a program két különböző pontján ugyanazt a logikát használjuk, ahogy
a 10-2. listázás mutatja.

<Listing number="10-2" file-name="src/main.rs" caption="Kód a legnagyobb szám megkeresésére *két* számlistában">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Bár ez a kód működik, a kód ismétlése fárasztó és hibalehetőségeket rejt.
Ráadásul több helyen is emlékeznünk kell a kód frissítésére, ha meg akarjuk
változtatni.

Az ismétlődés kiküszöbölésére absztrakciót hozunk létre: definiálunk egy
függvényt, amely bármely, paraméterként átadott egészszám-listán működik. Ettől
a megoldástól a kódunk világosabb lesz, és absztrakt módon fejezhetjük ki egy
listában a legnagyobb szám megkeresésének fogalmát.

A 10-3. listázásban a legnagyobb számot megkereső kódot kiemeljük egy `largest`
nevű függvénybe. Ezután meghívjuk a függvényt, hogy megtaláljuk a legnagyobb
számot a 10-2. listázás két listájában. A függvényt bármely más, `i32`
értékekből álló listán is használhatnánk, ami a jövőben a kezünkbe kerül.

<Listing number="10-3" file-name="src/main.rs" caption="Absztrahált kód a legnagyobb szám megkeresésére két listában">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

A `largest` függvénynek van egy `list` nevű paramétere, amely bármely konkrét
`i32` értékekből álló slice-ot képvisel, amit átadhatunk a függvénynek. Ennek
eredményeként, amikor meghívjuk a függvényt, a kód azokon a konkrét értékeken
fut le, amelyeket átadunk neki.

Összefoglalva, ezeket a lépéseket tettük meg, hogy a 10-2. listázás kódját a
10-3. listázás kódjává alakítsuk:

1. Azonosítottuk az ismétlődő kódot.
1. Kiemeltük az ismétlődő kódot a függvény törzsébe, és a függvény
   szignatúrájában megadtuk a kód bemeneteit és visszatérési értékeit.
1. Az ismétlődő kód két előfordulását átírtuk úgy, hogy helyette a függvényt
   hívja meg.

Ezután ugyanezeket a lépéseket használjuk generikusokkal a kódismétlés
csökkentésére. Ahogyan a függvény törzse konkrét értékek helyett egy absztrakt
`list`-en tud működni, úgy a generikusok révén a kód absztrakt típusokon tud
működni.

Tegyük fel például, hogy volna két függvényünk: az egyik `i32` értékek
slice-ában keresi meg a legnagyobb elemet, a másik pedig `char` értékek
slice-ában. Hogyan szüntetnénk meg ezt az ismétlődést? Derítsük ki!
