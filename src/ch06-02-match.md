<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## A `match` vezérlési szerkezet {#the-match-control-flow-construct}

A Rustnak van egy rendkívül erős vezérlési szerkezete, a `match`, amellyel egy
értéket minták sorozatához hasonlíthatsz, majd annak alapján futtathatsz kódot,
hogy melyik minta illeszkedik. A minták állhatnak literál értékekből,
változónevekből, helyettesítő szimbólumokból és sok minden másból; a [19.
fejezet][ch19-00-patterns]<!-- ignore --> az összes mintafajtát és azok
működését bemutatja. A `match` ereje a minták kifejezőerejéből fakad, valamint
abból, hogy a fordító ellenőrzi: minden lehetséges esetet kezelsz.

Gondolj a `match` kifejezésre úgy, mint egy pénzérme-válogató gépre: az érmék
egy sínen csúsznak lefelé, amelyen különböző méretű lyukak sorakoznak, és
minden érme az első olyan lyukon esik át, amelybe belefér. Ugyanígy az értékek
is végighaladnak a `match` mintáin, és az első olyan mintánál, amelybe az érték
„belefér”, az érték beleesik a hozzá tartozó kódblokkba, amely a végrehajtás
során felhasználja.

Ha már az érméknél tartunk, használjuk őket példaként a `match` bemutatására!
Írhatunk egy függvényt, amely egy ismeretlen amerikai érmét kap, és a
számlálógéphez hasonló módon eldönti, melyik érméről van szó, majd visszaadja
az értékét centben, ahogy a 6-3. listában látható.

<Listing number="6-3" caption="Egy enum és egy `match` kifejezés, amelynek mintái az enum variánsai">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Vegyük szemügyre a `value_in_cents` függvényben lévő `match`-et. Először
kiírjuk a `match` kulcsszót, utána pedig egy kifejezést, amely ebben az esetben
a `coin` érték. Ez nagyon hasonlít az `if`-nél használt feltételes
kifejezéshez, van azonban egy nagy különbség: az `if`-nél a feltételnek logikai
értéket kell adnia, itt viszont bármilyen típus lehet. A `coin` típusa ebben a
példában a `Coin` enum, amelyet az első sorban definiáltunk.

Ezután következnek a `match`-ágak. Egy ág két részből áll: egy mintából és
valamennyi kódból. Az itteni első ág mintája a `Coin::Penny` érték, ezt követi
a `=>` operátor, amely elválasztja a mintát a futtatandó kódtól. A kód ebben az
esetben csupán az `1` érték. Az egyes ágakat vessző választja el a
következőtől.

Amikor a `match` kifejezés lefut, a kapott értéket sorban összehasonlítja
minden ág mintájával. Ha egy minta illeszkedik az értékre, a mintához tartozó
kód lefut. Ha az adott minta nem illeszkedik az értékre, a végrehajtás a
következő ággal folytatódik, nagyjából úgy, mint az érmeválogató gépben.
Annyi águnk lehet, amennyire szükségünk van: a 6-3. listában a `match`-ünknek
négy ága van.

Az egyes ágakhoz tartozó kód egy kifejezés, és az illeszkedő ágban lévő
kifejezés eredménye lesz az az érték, amelyet az egész `match` kifejezés
visszaad.

Általában nem használunk kapcsos zárójeleket, ha a `match`-ág kódja rövid,
ahogy a 6-3. listában is, ahol minden ág csupán egy értéket ad vissza. Ha több
sornyi kódot szeretnél futtatni egy `match`-ágban, kapcsos zárójeleket kell
használnod, és az ágat követő vessző ilyenkor elhagyható. Például a következő
kód minden alkalommal kiírja, hogy „Lucky penny!”, amikor a metódust egy
`Coin::Penny` értékkel hívjuk meg, de továbbra is a blokk utolsó értékét, az
`1`-et adja vissza:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Értékekhez kötő minták {#patterns-that-bind-to-values}

A `match`-ágak másik hasznos tulajdonsága, hogy hozzá tudnak kötődni a mintára
illeszkedő értékek részeihez. Így tudunk értékeket kinyerni az enum
variánsaiból.

Példaként változtassuk meg az egyik enum-variánsunkat úgy, hogy adatot
tároljon. 1999 és 2008 között az Egyesült Államok olyan negyeddollárosokat
vert, amelyek egyik oldalán mind az 50 államnak külön mintázata volt. Más
érmék nem kaptak állammintákat, így csak a negyeddollárosoknak van ez a
többletértékük. Ezt az információt úgy adhatjuk hozzá az `enum`-unkhoz, hogy a
`Quarter` variánst kiegészítjük egy benne tárolt `UsState` értékkel; ezt
tettük meg a 6-4. listában.

<Listing number="6-4" caption="Egy `Coin` enum, amelyben a `Quarter` variáns egy `UsState` értéket is tárol">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Képzeljük el, hogy egy barátunk mind az 50 állam negyeddollárosát gyűjti.
Miközben érmetípus szerint válogatjuk az aprópénzünket, minden negyeddolláros
esetén hangosan bemondjuk a hozzá tartozó állam nevét is, hogy ha éppen olyan
akad a kezünkbe, amelyik a barátunknak még nincs meg, hozzátehesse a
gyűjteményéhez.

Ennek a kódnak a `match` kifejezésében egy `state` nevű változót adunk ahhoz a
mintához, amely a `Coin::Quarter` variáns értékeire illeszkedik. Amikor egy
`Coin::Quarter` illeszkedik, a `state` változó hozzákötődik az adott
negyeddolláros államának értékéhez. Ezután az adott ág kódjában használhatjuk a
`state` változót, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Ha meghívnánk a `value_in_cents(Coin::Quarter(UsState::Alaska))` függvényt, a
`coin` értéke `Coin::Quarter(UsState::Alaska)` lenne. Amikor ezt az értéket
összehasonlítjuk az egyes `match`-ágakkal, egyik sem illeszkedik, amíg el nem
érünk a `Coin::Quarter(state)` ágig. Ezen a ponton a `state` kötése az
`UsState::Alaska` érték lesz. Ezt a kötést ezután felhasználhatjuk a
`println!` kifejezésben, így kinyerve a belső állam értékét a `Coin` enum
`Quarter` variánsából.

A jogosultsági ábra megmutatja, mit tesz ez a `match` a `coin` értékkel. A
`coin`-t tulajdonba kapjuk, ezért a `Coin::Quarter(state)` ág egyszerűen
kimozgatja belőle az `UsState` értéket: a `state` megkapja az **R** és az **O**
jogosultságot, a `coin` pedig elveszíti mindkettőt:

```aquascope,permissions,stepper,boundaries
##[derive(Debug)]
#enum UsState {
#    Alabama,
#    Alaska,
#}
#enum Coin {
#    Penny,
#    Nickel,
#    Dime,
#    Quarter(UsState),
#}
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {state:?}!");
            25
        }
    }
}
#fn main() {
#    value_in_cents(Coin::Quarter(UsState::Alaska));
#}
```

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Az `Option<T>` illesztése `match`-csel


Az előző szakaszban a `Some` esetből akartuk kinyerni a belső `T` értéket az
`Option<T>` használatakor; az `Option<T>`-t `match` segítségével is kezelhetjük,
ahogyan a `Coin` enummal tettük! Érmék helyett most az `Option<T>` variánsait
hasonlítjuk össze, de a `match` kifejezés működése ugyanaz marad.

Tegyük fel, hogy egy olyan függvényt szeretnénk írni, amely egy `Option<i32>`
értéket kap, és ha van benne érték, hozzáad 1-et. Ha nincs benne érték, a
függvény adja vissza a `None` értéket, és ne próbáljon meg semmilyen műveletet
végrehajtani.

Ezt a függvényt a `match`-nek köszönhetően nagyon könnyű megírni, és a 6-5.
listában láthatóhoz hasonlóan fog kinézni.

<Listing number="6-5" caption="Egy függvény, amely `match` kifejezést használ egy `Option<i32>` értéken">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Vizsgáljuk meg részletesebben a `plus_one` első végrehajtását. Amikor meghívjuk
a `plus_one(five)` függvényt, a `plus_one` törzsében lévő `x` változó értéke
`Some(5)` lesz. Ezt hasonlítjuk össze ezután minden egyes `match`-ággal:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

A `Some(5)` érték nem illeszkedik a `None` mintára, ezért továbblépünk a
következő ágra:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Illeszkedik a `Some(5)` a `Some(i)` mintára? Igen! Ugyanarról a variánsról van
szó. Az `i` hozzákötődik a `Some`-ban tárolt értékhez, tehát az `i` felveszi az
`5` értéket. Ezután lefut a `match`-ág kódja, vagyis hozzáadunk 1-et az `i`
értékéhez, és létrehozunk egy új `Some` értéket, amelyben a `6` összegünk van.

Most nézzük meg a `plus_one` második hívását a 6-5. listában, ahol az `x`
értéke `None`. Belépünk a `match`-be, és összehasonlítjuk az első ággal:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Illeszkedik! Nincs érték, amihez hozzáadhatnánk, ezért a program megáll, és a
`=>` jobb oldalán álló `None` értéket adja vissza. Mivel az első ág
illeszkedett, a további ágakkal már nem történik összehasonlítás.

A `match` és az enumok együttes használata sok helyzetben hasznos. Ezt a mintát
gyakran fogod látni Rust-kódban: `match`-elünk egy enumra, hozzákötünk egy
változót a benne lévő adathoz, majd ez alapján futtatunk kódot. Elsőre kicsit
trükkös, de ha egyszer megszokod, azt fogod kívánni, bárcsak minden nyelvben
lenne ilyen. Rendre a felhasználók egyik kedvence.

Ha az enumban nem másolható adat van – például egy `String` –, érdemes
megfigyelni, hogy a `match` mozgatja-e vagy csak kölcsönveszi ezt az adatot. Az
alábbi programban a `Some(_)` minta nem köt hozzá változót a `String`-hez, ezért
semmi nem mozdul: az `opt` a `match` után is megtartja az **R** és az **O**
jogosultságát, így a `println!` olvashatja:

```aquascope,permissions,stepper,boundaries
#fn main() {
let opt: Option<String> = Some(String::from("Hello world"));

match opt {
    Some(_) => println!("Some!"),
    None => println!("None!"),
}

println!("{opt:?}");
#}
```

Ha a helykitöltő `_` helyére változónevet írunk, megváltozik a kép. Az `opt`
típusa `Option<String>`, nem pedig `&Option<String>`, ezért a `Some(s)` minta
kimozgatja belőle a `String`-et: az `opt` már az illesztésnél elveszíti az **R**
és az **O** jogosultságát, a `println!` pedig nem fordul le:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let opt: Option<String> = Some(String::from("Hello world"));

match opt {
    Some(s) => println!("Some: {s}"),
    None => println!("None!"),
}

println!("{opt:?}");`{}`
#}
```

Ha csak bele akarunk nézni az `opt`-ba anélkül, hogy a tartalmát elmozgatnánk,
referenciára illesztünk. Ilyenkor a Rust „lefelé tolja” a referenciát a külső
enumról a benne lévő mezőre – az `s` típusa `&String` lesz –, ezért az `opt`
csak az **O** jogosultságát adja kölcsön a `match` idejére, az **R**-t végig
megtartja, és az illesztés után is használható:

```aquascope,permissions,stepper,boundaries
#fn main() {
let opt: Option<String> = Some(String::from("Hello world"));

match &opt {
    Some(s) => println!("Some: {s}"),
    None => println!("None!"),
}

println!("{opt:?}");
#}
```

### A `match`-ek kimerítőek

Van a `match`-nek még egy tulajdonsága, amelyet meg kell beszélnünk: az ágak
mintáinak minden lehetőséget le kell fedniük. Nézd meg a `plus_one`
függvényünk következő változatát, amelyben van egy hiba, és nem fordul le:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Nem kezeltük a `None` esetet, így ez a kód hibát fog okozni. Szerencsére olyan
hibáról van szó, amelyet a Rust észre tud venni. Ha megpróbáljuk lefordítani
ezt a kódot, a következő hibát kapjuk:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

A Rust tudja, hogy nem fedtük le az összes lehetséges esetet, sőt azt is tudja,
melyik mintát felejtettük el! A `match`-ek a Rustban _kimerítőek_: az utolsó
lehetőségig ki kell merítenünk az eseteket ahhoz, hogy a kód érvényes legyen.
Különösen az `Option<T>` esetében, amikor a Rust megakadályozza, hogy
elfelejtsük kifejezetten kezelni a `None` esetet, ez megóv attól, hogy értéket
feltételezzünk ott, ahol esetleg null van, és ezzel lehetetlenné teszi a
korábban tárgyalt milliárd dolláros hibát.

### Mindent elkapó minták és a `_` helykitöltő

Az enumok segítségével néhány konkrét értékre külön műveletet végezhetünk,
minden más értékre pedig egyetlen alapértelmezett műveletet. Képzeld el, hogy
egy játékot implementálunk, amelyben ha 3-at dobsz a kockával, a játékosod nem
lép, hanem kap egy elegáns új kalapot. Ha 7-est dobsz, a játékosod elveszít egy
elegáns kalapot. Minden más érték esetén a játékosod annyi mezőt lép a
játéktáblán. Íme egy `match`, amely ezt a logikát valósítja meg úgy, hogy a
kockadobás eredménye véletlen érték helyett rögzítve van, a többi logikát pedig
törzs nélküli függvények képviselik, mert a tényleges implementálásuk kívül
esik ennek a példának a keretein:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Az első két ágban a minták a `3` és a `7` literál értékek. Az utolsó ágban,
amely minden más lehetséges értéket lefed, a minta az a változó, amelyet az
`other` névre kereszteltünk. Az `other` ághoz tartozó kód úgy használja ezt a
változót, hogy átadja a `move_player` függvénynek.

Ez a kód lefordul, pedig nem soroltuk fel az összes lehetséges értéket, amelyet
egy `u8` felvehet, mert az utolsó minta minden kifejezetten fel nem sorolt
értékre illeszkedik. Ez a mindent elkapó minta teljesíti azt a követelményt,
hogy a `match`-nek kimerítőnek kell lennie. Vedd észre, hogy a mindent elkapó
ágat a végére kell tennünk, mert a minták kiértékelése sorrendben történik. Ha
korábbra tettük volna a mindent elkapó ágat, a többi ág soha nem futna le,
ezért a Rust figyelmeztet minket, ha egy mindent elkapó ág után további ágakat
veszünk fel!

A Rustnak van egy olyan mintája is, amelyet akkor használhatunk, ha mindent el
akarunk kapni, de nem akarjuk _használni_ az értéket a mindent elkapó mintában:
a `_` egy speciális minta, amely bármilyen értékre illeszkedik, és nem kötődik
hozzá az értékhez. Ez azt jelzi a Rustnak, hogy nem fogjuk használni az
értéket, így a Rust nem figyelmeztet minket nem használt változóra.

Változtassuk meg a játék szabályait: mostantól, ha 3-tól és 7-től eltérő
bármit dobsz, újra kell dobnod. Már nincs szükségünk a mindent elkapó érték
használatára, ezért a kódunkat átírhatjuk úgy, hogy az `other` nevű változó
helyett `_`-t használjon:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Ez a példa szintén teljesíti a kimerítőségi követelményt, mert az utolsó ágban
kifejezetten figyelmen kívül hagyunk minden más értéket; nem felejtettünk el
semmit.

Végül még egyszer megváltoztatjuk a játék szabályait úgy, hogy semmi más ne
történjen a körödben, ha 3-tól és 7-től eltérő bármit dobsz. Ezt úgy
fejezhetjük ki, hogy a `_` ághoz tartozó kódként a unit értéket (a [„A tuple
típus”][tuples]<!-- ignore --> szakaszban említett üres tuple típust)
használjuk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Itt kifejezetten megmondjuk a Rustnak, hogy nem fogunk használni semmilyen más
értéket, amely nem illeszkedik egy korábbi ág mintájára, és ebben az esetben
nem akarunk kódot futtatni.

A mintákról és az illesztésről még sok mindent elmondunk a [19.
fejezetben][ch19-00-patterns]<!-- ignore -->. Egyelőre továbblépünk az `if let`
szintaxisra, amely olyan helyzetekben lehet hasznos, ahol a `match` kifejezés
kissé bőbeszédű.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
