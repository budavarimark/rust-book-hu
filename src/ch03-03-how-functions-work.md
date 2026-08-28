## Függvények

A függvények mindenütt jelen vannak a Rust kódban. A nyelv egyik legfontosabb
függvényét már láttad: a `main` függvényt, amely sok program belépési pontja.
Találkoztál már az `fn` kulcsszóval is, amellyel új függvényeket deklarálhatsz.

A Rust kód a _snake case_ stílust használja konvencióként a függvény- és
változónevekhez, amelyben minden betű kisbetű, a szavakat pedig alulvonás
választja el. Íme egy program, amely egy példa függvénydefiníciót tartalmaz:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Rustban úgy definiálunk függvényt, hogy beírjuk az `fn`-t, majd a függvény
nevét és egy zárójelpárt. A kapcsos zárójelek megmondják a fordítónak, hol
kezdődik és hol ér véget a függvény törzse.

Bármelyik általunk definiált függvényt meghívhatjuk úgy, hogy beírjuk a nevét,
majd egy zárójelpárt. Mivel az `another_function` definiálva van a programban,
meghívható a `main` függvényen belülről. Vedd észre, hogy az
`another_function`-t a forráskódban a `main` függvény _után_ definiáltuk;
definiálhattuk volna előtte is. A Rustot nem érdekli, hol definiálod a
függvényeidet, csak az, hogy valahol egy olyan hatókörben legyenek
definiálva, amelyet a hívó lát.

Kezdjünk el egy _functions_ nevű új binary projektet, hogy tovább vizsgáljuk a
függvényeket. Tedd az `another_function` példát a _src/main.rs_ fájlba, és
futtasd. A következő kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

A sorok abban a sorrendben hajtódnak végre, ahogyan a `main` függvényben
szerepelnek. Először a „Hello, world!” üzenet íródik ki, majd meghívódik az
`another_function`, és kiíródik az ő üzenete.

### Paraméterek

A függvényeket úgy is definiálhatjuk, hogy _paramétereik_ legyenek; ezek
speciális változók, amelyek a függvény szignatúrájának részei. Ha egy
függvénynek vannak paraméterei, konkrét értékeket adhatsz meg hozzájuk.
Technikailag ezeket a konkrét értékeket _argumentumoknak_ nevezzük, de a
hétköznapi beszédben az emberek hajlamosak a _paraméter_ és az _argumentum_
szót felcserélhetően használni akár a függvény definíciójában szereplő
változókra, akár a függvény hívásakor átadott konkrét értékekre.

Az `another_function` ebben a változatában hozzáadunk egy paramétert:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Próbáld ki ezt a programot; a következő kimenetet kell kapnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Az `another_function` deklarációjában egy `x` nevű paraméter szerepel. Az `x`
típusa `i32`-ként van megadva. Amikor `5`-öt adunk át az `another_function`-nek,
a `println!` makró `5`-öt tesz oda, ahol a formátumstringben az `x`-et
tartalmazó kapcsoszárójel-pár állt.

A függvényszignatúrákban _kötelező_ deklarálnod minden paraméter típusát. Ez
tudatos döntés a Rust tervezésében: a függvénydefiníciókban megkövetelt
típusannotációk miatt a fordítónak szinte sosem kell máshol is használnod őket
a kódban ahhoz, hogy kiderüljön, melyik típusra gondolsz. A fordító
hasznosabb hibaüzeneteket is tud adni, ha tudja, milyen típusokat vár a
függvény.

Ha több paramétert definiálsz, vesszővel válaszd el a paraméterdeklarációkat,
így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Ez a példa létrehoz egy `print_labeled_measurement` nevű függvényt két
paraméterrel. Az első paraméter neve `value`, típusa `i32`. A második neve
`unit_label`, típusa `char`. A függvény ezután olyan szöveget ír ki, amely
tartalmazza a `value`-t és a `unit_label`-t is.

Próbáljuk ki ezt a kódot. Cseréld le a _functions_ projekted _src/main.rs_
fájljában jelenleg lévő programot a fenti példára, és futtasd a `cargo run`
paranccsal:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Mivel a függvényt `5`-tel hívtuk meg a `value` értékeként és `'h'`-val a
`unit_label` értékeként, a program kimenete ezeket az értékeket tartalmazza.

### Utasítások és kifejezések

A függvénytörzsek utasítások sorozatából állnak, amelyet opcionálisan egy
kifejezés zár le. Az eddig tárgyalt függvényekben nem szerepelt lezáró
kifejezés, de kifejezést már láttál egy utasítás részeként. Mivel a Rust
kifejezésalapú nyelv, ezt a különbséget fontos megérteni. Más nyelvek nem
tesznek hasonló megkülönböztetéseket, úgyhogy nézzük meg, mik az utasítások és
a kifejezések, és a köztük lévő különbségek hogyan hatnak a függvények
törzsére.

- Az _utasítások_ olyan instrukciók, amelyek végrehajtanak valamilyen műveletet,
  és nem adnak vissza értéket.
- A _kifejezések_ egy eredményértékké értékelődnek ki.

Nézzünk néhány példát.

Valójában már használtunk utasításokat és kifejezéseket is. Egy változó
létrehozása és érték hozzárendelése a `let` kulcsszóval utasítás. A 3-1.
listában a `let y = 6;` egy utasítás.

<Listing number="3-1" file-name="src/main.rs" caption="Egy `main` függvénydeklaráció, amely egyetlen utasítást tartalmaz">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

A függvénydefiníciók szintén utasítások; a teljes fenti példa önmagában egy
utasítás. (Ahogy hamarosan látni fogjuk, egy függvény meghívása viszont nem
utasítás.)

Az utasítások nem adnak vissza értéket. Ezért nem rendelhetsz egy `let`
utasítást egy másik változóhoz, ahogy azt az alábbi kód megpróbálja; hibát
fogsz kapni:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Amikor futtatod ezt a programot, a kapott hiba így néz ki:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

A `let y = 6` utasítás nem ad vissza értéket, így nincs semmi, amihez az `x`
kötődhetne. Ez különbözik attól, ami más nyelvekben – például a C-ben és a
Rubyban – történik, ahol az értékadás visszaadja az értékadás értékét. Azokban
a nyelvekben leírhatod, hogy `x = y = 6`, és mind az `x`, mind az `y` értéke
`6` lesz; Rustban ez nincs így.

A kifejezések egy értékké értékelődnek ki, és a Rustban írt kódod nagy részét
ők teszik ki. Vegyünk egy matematikai műveletet, például az `5 + 6`-ot: ez egy
kifejezés, amely a `11` értékké értékelődik ki. A kifejezések lehetnek
utasítások részei: a 3-1. listában a `let y = 6;` utasításban lévő `6` egy
kifejezés, amely a `6` értékké értékelődik ki. Egy függvény meghívása
kifejezés. Egy makró meghívása kifejezés. A kapcsos zárójelekkel létrehozott új
hatókörblokk is kifejezés, például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Ez a kifejezés:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

egy blokk, amely ebben az esetben `4`-gyé értékelődik ki. Ez az érték a `let`
utasítás részeként az `y`-hoz kötődik. Figyeld meg, hogy az `x + 1` sor végén
nincs pontosvessző, ellentétben a legtöbb eddig látott sorral. A kifejezések
nem tartalmaznak lezáró pontosvesszőt. Ha pontosvesszőt teszel egy kifejezés
végére, utasítássá alakítod, és akkor már nem ad vissza értéket. Tartsd ezt
észben, ahogy a következőkben a függvények visszatérési értékeit és a
kifejezéseket vizsgáljuk.

### Visszatérési értékkel rendelkező függvények

A függvények értéket adhatnak vissza az őket hívó kódnak. A visszatérési
értékeket nem nevezzük el, de a típusukat egy nyíl (`->`) után deklarálnunk
kell. Rustban a függvény visszatérési értéke azonos a függvénytörzs blokkjában
lévő utolsó kifejezés értékével. A `return` kulcsszóval és egy érték
megadásával korábban is kiléphetsz egy függvényből, de a legtöbb függvény
implicit módon az utolsó kifejezést adja vissza. Íme egy példa egy értéket
visszaadó függvényre:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

A `five` függvényben nincsenek függvényhívások, makrók, de még `let` utasítások
sem – csupán maga az `5` szám. Ez Rustban tökéletesen érvényes függvény. Vedd
észre, hogy a függvény visszatérési típusa is meg van adva: `-> i32`. Próbáld
ki ezt a kódot; a kimenetnek így kell kinéznie:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

A `five`-ban lévő `5` a függvény visszatérési értéke, ezért a visszatérési
típus `i32`. Nézzük meg ezt részletesebben. Két fontos dolog van: Először is, a
`let x = five();` sor azt mutatja, hogy egy függvény visszatérési értékét
használjuk egy változó inicializálására. Mivel a `five` függvény `5`-öt ad
vissza, ez a sor ugyanaz, mint a következő:

```rust
let x = 5;
```

Másodszor, a `five` függvénynek nincsenek paraméterei, és definiálja a
visszatérési érték típusát, a függvény törzse viszont egy magányos `5`
pontosvessző nélkül, mert ez egy kifejezés, amelynek az értékét vissza akarjuk
adni.

Nézzünk egy másik példát:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Ha lefuttatod ezt a kódot, a `The value of x is: 6` szöveget írja ki. De mi
történik, ha pontosvesszőt teszünk az `x + 1`-et tartalmazó sor végére, és így
kifejezésből utasítássá alakítjuk?

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Ennek a kódnak a fordítása hibát eredményez, az alábbiak szerint:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

A fő hibaüzenet, a `mismatched types`, felfedi a kód alapvető problémáját. A
`plus_one` függvény definíciója azt mondja, hogy `i32`-t fog visszaadni, de az
utasítások nem értékelődnek ki értékké, amit a `()`, vagyis a unit típus fejez
ki. Ezért semmi sem kerül visszaadásra, ami ellentmond a függvénydefiníciónak,
és hibát eredményez. Ebben a kimenetben a Rust ad egy üzenetet, amely
segíthet a probléma orvoslásában: azt javasolja, hogy távolítsd el a
pontosvesszőt, ami megszüntetné a hibát.
