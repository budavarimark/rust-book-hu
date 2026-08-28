## Referenciák és borrowing {#references-and-borrowing}

A 4-5. listában szereplő tuple-ös kóddal az a baj, hogy vissza kell adnunk a
`String`-et a hívó függvénynek ahhoz, hogy a `calculate_length` hívása után is
használhassuk a `String`-et, hiszen a `String` bemozgott a `calculate_length`
függvénybe. Ehelyett átadhatunk egy referenciát a `String` értékre.
A referencia abban hasonlít a pointerhez, hogy egy cím, amelyet követve
hozzáférünk az adott címen tárolt adathoz; azt az adatot valamelyik másik
változó birtokolja. A pointerrel ellentétben a referenciáról garantált, hogy a
saját élettartama alatt végig egy adott típus érvényes értékére mutat.

Így definiálnál és használnál egy olyan `calculate_length` függvényt, amely
paraméterként egy objektumra mutató referenciát kap, ahelyett hogy átvenné az
érték ownershipjét:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

Először is figyeld meg, hogy a változódeklarációból és a függvény visszatérési
értékéből eltűnt az összes tuple-ös kód. Másodszor vedd észre, hogy `&s1`-et
adunk át a `calculate_length` függvénynek, a definíciójában pedig `String`
helyett `&String` szerepel. Ezek az és-jelek jelölik a referenciákat, és
lehetővé teszik, hogy úgy hivatkozz egy értékre, hogy közben nem veszed át az
ownershipjét. A 4-6. ábra ezt a fogalmat szemlélteti.

<img alt="Három táblázat: az s táblázata csak egy pointert tartalmaz az s1
táblázatára. Az s1 táblázata az s1 stacken tárolt adatait tartalmazza, és a
heapen lévő sztringadatokra mutat." src="img/trpl04-06.svg" class="center" />

<span class="caption">4-6. ábra: Egy `&String` típusú `s`, amely a `String`
típusú `s1`-re mutat</span>

> Megjegyzés: A `&` jellel történő referenciaképzés ellentéte a
> _dereferencelés_, amelyet a dereferencia-operátorral, a `*` jellel végzünk.
> A dereferencia-operátor néhány használatát a 8. fejezetben látjuk majd, a
> dereferencelés részleteit pedig a 15. fejezetben tárgyaljuk.

Nézzük meg közelebbről az itteni függvényhívást:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

Az `&s1` szintaxissal olyan referenciát hozunk létre, amely _hivatkozik_ az
`s1` értékére, de nem birtokolja azt. Mivel a referencia nem birtokolja az
értéket, a mutatott érték nem kerül eldobásra akkor, amikor a referencia
használata véget ér.

Az alábbi futásidejű ábrán az látszik, mit jelent ez a memóriában. Az `L2`
pontban két lépésen át jutunk el a heap-en lévő `"hello"` adatig: az `s`
referencia a stack-en lévő `s1`-re mutat, `s1` pedig a heap-en tárolt
sztringtartalomra. Mivel `s` nem birtokolja az adatot, a `calculate_length`
visszatérése után (`L3`) a heap-en semmi nem szabadul fel, csak a függvény
stack-kerete tűnik el:

```aquascope,interpreter,horizontal
fn main() {
    let s1 = String::from("hello");`[]`
    let len = calculate_length(&s1);`[]`
    println!("The length of '{s1}' is {len}.");
}

fn calculate_length(s: &String) -> usize {
    `[]`s.len()
}
```

Hasonlóképpen a függvény szignatúrája is `&` jellel jelzi, hogy az `s`
paraméter típusa referencia. Tegyünk hozzá néhány magyarázó megjegyzést:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

Az a hatókör, amelyben az `s` változó érvényes, ugyanaz, mint bármely más
függvényparaméteré, de a referencia által mutatott érték nem kerül eldobásra
akkor, amikor az `s` használata véget ér, mert az `s`-nek nincs ownershipje.
Ha a függvények a tényleges értékek helyett referenciákat kapnak paraméterként,
nem kell visszaadnunk az értékeket ahhoz, hogy visszaadjuk az ownershipet,
hiszen soha nem is volt ownershipünk.

A referenciakészítés műveletét _borrowing_-nak nevezzük. Ahogy a való életben
is: ha valaki birtokol valamit, kölcsönkérheted tőle. Amikor végeztél, vissza
kell adnod. Nem a tiéd.

A fordítási idejű ábra megmutatja, mibe kerül ez a kölcsönzés. Mivel `s1` nem
`mut`, eleve csak **R** és **O** jogosultsága van; a `&s1` borrow idejére
elveszíti az **O**-t, tehát amíg az `s` referencia él, `s1` nem mozgatható el és
nem dobható el – olvasni viszont továbbra is lehet. Az `s` utolsó használata
(a `calculate_length(s)` hívás) után `s1` visszakapja az **O** jogosultságát is:

```aquascope,permissions,stepper,boundaries
#fn main() {
let s1 = String::from("hello");
let s: &String = &s1;
let len = calculate_length(s);
println!("The length of '{s1}' is {len}.");
#}
#fn calculate_length(s: &String) -> usize {
#    s.len()
#}
```

Mi történik hát, ha megpróbálunk módosítani valamit, amit épp kölcsönvettünk?
Próbáld ki a 4-6. listában szereplő kódot. Előre szólunk: nem fog működni!

<Listing number="4-6" file-name="src/main.rs" caption="Kísérlet egy kölcsönvett érték módosítására">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

Íme a hiba:

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

Ahogy a változók alapértelmezés szerint nem módosíthatók, úgy a referenciák
sem. Nem módosíthatunk olyasmit, amire csak referenciánk van.

Az ábra a jogosultságok nyelvén is megmutatja a hibát: a `change` függvényben a
`*some_string` hely csak **R** jogosultságot kap, a `push_str` viszont **R**-t
és **W**-t vár, ezért a hiányzó **W** üresen marad, és a kód nem fordul le:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
    let s = String::from("hello");
    change(&s);
}

fn change(some_string: &String) {
    some_string.push_str(", world");
}
```

### Módosítható referenciák

A 4-6. listában szereplő kódot néhány apró módosítással kijavíthatjuk úgy, hogy
megváltoztathassunk egy kölcsönvett értéket; ehhez _módosítható referenciát_
(mutable reference) használunk:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

Először `mut`-tá tesszük az `s`-t. Utána a `change` függvény hívásának helyén
`&mut s` formában létrehozunk egy módosítható referenciát, a függvény
szignatúráját pedig úgy alakítjuk, hogy a `some_string: &mut String`
paraméterrel módosítható referenciát fogadjon. Ez nagyon világossá teszi, hogy
a `change` függvény meg fogja változtatni a kölcsönvett értéket.

Az alábbi ábrán a `&mut s` referenciát külön változóba (`r`) tettük, hogy több
soron át lássuk a hatását. Amikor `r` létrejön, `s` mind a három jogosultságát
(**R**, **W**, **O**) elveszíti: amíg `r` él, `s`-hez semmilyen módon nem lehet
hozzáférni. Cserébe a `*some_string` hely a `change` belsejében megkapja a
**W**-t, így a `push_str` módosíthat rajta. Az `r` utolsó használata után `s`
visszakapja a jogosultságait, ezért a `println!` újra olvashatja:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut s = String::from("hello");
    let r = &mut s;
    change(r);
    println!("{s}");
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

A módosítható referenciáknak egy nagy megkötésük van: ha van egy módosítható
referenciád egy értékre, akkor semmilyen más referenciád nem lehet ugyanarra az
értékre. Ez a kód, amely két módosítható referenciát próbál létrehozni az
`s`-re, hibát okoz:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

Íme a hiba:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

A hiba azt mondja, hogy a kód érvénytelen, mert az `s`-t egyszerre többször nem
kölcsönözhetjük módosíthatóként. Az első módosítható borrow az `r1`-ben van, és
addig kell tartania, amíg a `println!`-ben fel nem használjuk, ám e módosítható
referencia létrehozása és felhasználása között megpróbáltunk létrehozni egy
másik módosítható referenciát `r2`-ben, amely ugyanazt az adatot kölcsönzi,
mint az `r1`.

Az ábrán is jól látszik a tiltás: az `r1` létrehozása után `s`-nek egyetlen
jogosultsága sem marad, ezért amikor a következő sor `&mut s` alakban újra
kölcsönözné, a művelethez elvárt **R** és **W** üresen – vagyis hiányzóként –
jelenik meg mellette:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s;
println!("{r1}, {r2}");
#}
```

Az a megkötés, amely megakadályozza, hogy egyszerre több módosítható referencia
mutasson ugyanarra az adatra, megengedi ugyan a módosítást, de csak nagyon
kontrollált módon. Az új rustaceanoknak sokszor nehézséget okoz, mert a legtöbb
nyelvben akkor módosíthatsz, amikor csak akarsz. Ennek a megkötésnek az az
előnye, hogy a Rust fordítási időben meg tudja előzni az adatversenyeket. Az
_adatverseny_ (data race) hasonlít a versenyhelyzetre, és akkor lép fel, ha az
alábbi három dolog együtt fennáll:

- Két vagy több pointer egyszerre fér hozzá ugyanahhoz az adathoz.
- A pointerek közül legalább egyet írásra használnak.
- Nincs semmilyen mechanizmus, amely szinkronizálná az adathoz való
  hozzáférést.

Az adatversenyek nemdefiniált viselkedést okoznak, és nehéz lehet őket
felderíteni és javítani, ha futásidőben próbálod kinyomozni őket; a Rust úgy
előzi meg ezt a problémát, hogy egyszerűen nem fordítja le az adatversenyt
tartalmazó kódot!

Mint mindig, kapcsos zárójelekkel most is létrehozhatunk egy új hatókört, ami
lehetővé teszi több módosítható referencia használatát – csak épp nem
_egyidejűleg_:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

A Rust hasonló szabályt érvényesít a módosítható és a nem módosítható
referenciák kombinálására. Ez a kód hibát eredményez:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

Íme a hiba:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

Hoppá! _Az sem_ lehet, hogy módosítható referenciánk legyen ugyanarra az
értékre, amelyre nem módosítható referenciánk is van.

Az ábrán végigkövetheted, miért más ez az eset: az `r1` és `r2` nem módosítható
borrow-jai csak a **W** és az **O** jogosultságot veszik el `s`-től, az **R**-t
nem, ezért fér meg egymás mellett a két olvasó referencia. Az `r3` sorában
viszont a `&mut s` **W**-t is elvárna, azt pedig `s` már nem tudja megadni:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
let r3 = &mut s;
println!("{r1}, {r2}, and {r3}");
#}
```

A nem módosítható referencia használói nem számítanak arra, hogy az érték
hirtelen megváltozik a kezük alatt! Több nem módosítható referencia viszont
megengedett, mert aki csak olvassa az adatot, az nem tudja befolyásolni senki
más olvasását.

Vedd észre, hogy egy referencia hatóköre ott kezdődik, ahol bevezetjük, és a
referencia utolsó használatáig tart. Például ez a kód lefordul, mert a nem
módosítható referenciák utolsó használata a `println!`-ben van, még a
módosítható referencia bevezetése előtt:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

Az `r1` és `r2` nem módosítható referenciák hatóköre a `println!` után véget
ér, ahol utoljára használjuk őket, és ez még az `r3` módosítható referencia
létrehozása előtt van. Ezek a hatókörök nem fedik át egymást, így a kód
megengedett: a fordító látja, hogy a referenciát a hatókör vége előtti
valamelyik ponttól kezdve már nem használjuk.

Az ábra lépésenként mutatja ugyanezt: a `println!` sora után `r1` és `r2` minden
jogosultságát elveszíti, mert ott ér véget az élettartamuk, `s` pedig ugyanitt
visszakapja a **W** és **O** jogosultságát – így a következő sorban már
létrejöhet az `r3` módosítható referencia:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{r1} and {r2}");
let r3 = &mut s;
println!("{r3}");
#}
```

Bár a borrowinggal kapcsolatos hibák időnként bosszantóak lehetnek, ne feledd:
a Rust fordítója korán (futásidő helyett fordítási időben) mutat rá egy
lehetséges hibára, és pontosan megmutatja, hol a probléma. Így neked nem kell
utólag kinyomoznod, miért nem az van az adataidban, amit gondoltál.

### Dangling referenciák {#dangling-references}

A pointereket használó nyelvekben könnyű véletlenül létrehozni egy _dangling
pointert_ – vagyis olyan pointert, amely a memória egy olyan területére
hivatkozik, amelyet közben esetleg már másnak adtak oda –: elég felszabadítani
valamennyi memóriát úgy, hogy közben megőrizzük az arra mutató pointert. A
Rustban ezzel szemben a fordító garantálja, hogy a referenciák soha nem lesznek
dangling referenciák: ha van egy referenciád valamilyen adatra, a fordító
gondoskodik róla, hogy az adat ne kerüljön ki a hatóköréből előbb, mint a rá
mutató referencia.

Az alábbi ábrán pontosan ez a helyzet áll elő: a `drop(s)` felszabadítaná a
`String`-et, miközben az `s_ref` referencia még él. A `&s` borrow elveszi
`s`-től az **O** jogosultságot, a `drop` viszont épp **O**-t várna – ezért a
`drop(s)` sorában hiányzóként jelenik meg, és a kód nem fordul le:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let s = String::from("hello");
let s_ref = &s;
drop(s);
println!("{s_ref}");
#}
```

Próbáljunk meg létrehozni egy dangling referenciát, hogy lássuk, a Rust hogyan
akadályozza meg őket egy fordítási idejű hibával:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

Íme a hiba:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

Ez a hibaüzenet egy olyan képességre hivatkozik, amelyet még nem tárgyaltunk:
a lifetime-okra. A lifetime-okról részletesen a 10. fejezetben lesz szó. De ha
figyelmen kívül hagyod a lifetime-okra vonatkozó részeket, az üzenet mégis
tartalmazza a kulcsot ahhoz, miért problémás ez a kód:

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

Nézzük meg közelebbről, pontosan mi történik a `dangle` kódunk egyes
szakaszaiban:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

Mivel az `s` a `dangle` belsejében jön létre, a `dangle` kódjának végeztével az
`s` felszabadul. Mi viszont megpróbáltunk visszaadni rá egy referenciát. Ez azt
jelentené, hogy a referencia egy érvénytelen `String`-re mutatna. Ez így nem
jó! A Rust nem engedi, hogy ezt tegyük.

A megoldás itt az, hogy közvetlenül a `String`-et adjuk vissza:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

Ez minden gond nélkül működik. Az ownership kifelé mozog, és semmi nem
szabadul fel.

### A referenciák szabályai

Foglaljuk össze, mit beszéltünk meg a referenciákról:

- Bármely adott pillanatban _vagy_ egy módosítható referenciád lehet, _vagy_
  tetszőleges számú nem módosítható referenciád.
- A referenciáknak mindig érvényesnek kell lenniük.

Következőnek egy másfajta referenciát nézünk meg: a slice-okat.
