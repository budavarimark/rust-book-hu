## A slice típus {#the-slice-type}

A _slice_-ok segítségével egy [kollekció](ch08-00-common-collections.md)<!--
ignore --> összefüggő elemsorozatára hivatkozhatsz. A slice a referencia egy
fajtája, ezért nincs ownershipje.

Íme egy kis programozási feladat: írj egy függvényt, amely egy szóközökkel
elválasztott szavakból álló sztringet kap, és visszaadja az első szót, amit
talál benne. Ha a függvény nem talál szóközt a sztringben, akkor az egész
sztring egyetlen szó, tehát a teljes sztringet kell visszaadni.

> Megjegyzés: A slice-ok bemutatásának kedvéért ebben a szakaszban csak ASCII
> karaktereket feltételezünk; az UTF-8 kezelésének alaposabb tárgyalása a 8.
> fejezet [„UTF-8 kódolású szöveg tárolása sztringekkel”][strings]<!-- ignore
> --> című szakaszában található.

Nézzük végig, hogyan írnánk meg ennek a függvénynek a szignatúráját slice-ok
nélkül, hogy megértsük, milyen problémát oldanak majd meg a slice-ok:

```rust,ignore
fn first_word(s: &String) -> ?
```

A `first_word` függvénynek egy `&String` típusú paramétere van. Ownershipre
nincs szükségünk, tehát ez így rendben van. (Az idiomatikus Rustban a
függvények nem veszik át az argumentumaik ownershipjét, hacsak nincs rá
szükségük; ennek okai a továbbiakban válnak majd világossá.) De mit adjunk
vissza? Igazából nincs módunk arra, hogy egy sztring egy *részéről* beszéljünk.
Visszaadhatjuk viszont a szó végének indexét, amelyet egy szóköz jelez.
Próbáljuk ki ezt, ahogy a 4-7. lista mutatja.

<Listing number="4-7" file-name="src/main.rs" caption="A `first_word` függvény, amely egy bájtindexet ad vissza a `String` paraméterbe">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

Mivel elemenként végig kell mennünk a `String`-en, és meg kell néznünk, hogy
egy érték szóköz-e, az `as_bytes` metódussal bájttömbbé alakítjuk a
`String`-ünket.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Ezután az `iter` metódussal iterátort készítünk a bájttömb fölé:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Az iterátorokat részletesebben a [13. fejezetben][ch13]<!-- ignore -->
tárgyaljuk. Egyelőre elég annyi, hogy az `iter` egy olyan metódus, amely egy
kollekció minden elemét visszaadja, az `enumerate` pedig becsomagolja az `iter`
eredményét, és minden elemet egy tuple részeként ad vissza. Az `enumerate`
által visszaadott tuple első eleme az index, a második eleme pedig egy
referencia az elemre. Ez kicsit kényelmesebb, mintha magunk számolnánk ki az
indexet.

Mivel az `enumerate` metódus tuple-t ad vissza, mintákkal szétbonthatjuk ezt a
tuple-t. A mintákról bővebben a [6. fejezetben][ch6]<!-- ignore --> lesz szó. A
`for` ciklusban olyan mintát adunk meg, amelyben `i` áll a tuple indexére és
`&item` a tuple-ben lévő egyetlen bájtra. Mivel az `.iter().enumerate()`
hívástól egy referenciát kapunk az elemre, `&` jelet használunk a mintában.

A `for` cikluson belül a bájtliterál-szintaxis segítségével keressük a szóközt
jelentő bájtot. Ha találunk szóközt, visszaadjuk a pozícióját. Egyébként az
`s.len()` hívással a sztring hosszát adjuk vissza.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Most már meg tudjuk állapítani a sztringben lévő első szó végének indexét, de
van egy probléma. Egy önmagában álló `usize` értéket adunk vissza, amely
azonban csak a `&String` kontextusában jelent valamit. Más szóval: mivel a
`String`-től különálló érték, semmi nem garantálja, hogy a jövőben is érvényes
marad. Nézd meg a 4-8. listában szereplő programot, amely a 4-7. listából
származó `first_word` függvényt használja.

<Listing number="4-8" file-name="src/main.rs" caption="A `first_word` függvény hívási eredményének eltárolása, majd a `String` tartalmának megváltoztatása">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

Ez a program hiba nélkül lefordul, és akkor is lefordulna, ha az `s.clear()`
hívása után használnánk a `word`-öt. Mivel a `word` egyáltalán nincs
kapcsolatban az `s` állapotával, a `word` továbbra is az `5` értéket
tartalmazza. Ezt az `5` értéket felhasználhatnánk az `s` változóval együtt,
hogy kinyerjük az első szót, ez azonban hiba lenne, mert az `s` tartalma
megváltozott azóta, hogy elmentettük az `5`-öt a `word`-be.

Az alábbi ábra megmutatja, miért hallgat a fordító: a `first_word(&s)` hívás
csak a hívás idejére kölcsönzi az `s`-t, a visszaadott `usize` pedig már
semmilyen módon nem hivatkozik a `String` tartalmára. Ezért `s` a hívás után
visszakapja a **W** és **O** jogosultságát, és az `s.clear()` megengedett:

```aquascope,permissions,stepper,boundaries
#fn first_word(s: &String) -> usize {
#    let bytes = s.as_bytes();
#    for (i, &item) in bytes.iter().enumerate() {
#        if item == b' ' {
#            return i;
#        }
#    }
#    s.len()
#}
fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);
    s.clear();
}
```

Fárasztó és hibára hajlamos, ha folyton azon kell aggódnunk, hogy a `word`-ben
tárolt index kicsúszik az `s`-ben lévő adattal való szinkronból! Ezeknek az
indexeknek a kezelése még törékenyebb, ha írunk egy `second_word` függvényt is.
A szignatúrájának így kellene kinéznie:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Most már egy kezdő- _és_ egy végindexet is nyilvántartunk, és még több olyan
értékünk van, amelyet egy adott állapotú adatból számoltunk ki, de amely
semmilyen módon nincs hozzákötve ehhez az állapothoz. Három egymástól
független változó lebeg körülöttünk, amelyeket szinkronban kell tartani.

Szerencsére a Rustnak van megoldása erre a problémára: a string slice-ok.

### String slice-ok {#string-slices}

A _string slice_ egy `String` összefüggő elemsorozatára mutató referencia, és
így néz ki:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

A `hello` nem a teljes `String`-re mutató referencia, hanem a `String` egy
részére, amelyet a plusz `[0..5]` rész jelöl ki. A slice-okat szögletes
zárójelben megadott tartománnyal hozzuk létre, `[kezdő_index..vég_index]`
formában, ahol a _`kezdő_index`_ a slice első pozíciója, a _`vég_index`_ pedig
eggyel több a slice utolsó pozíciójánál. Belül a slice adatszerkezete a
kezdőpozíciót és a slice hosszát tárolja, amely a _`vég_index`_ mínusz a
_`kezdő_index`_ értékkel egyenlő. Tehát a `let world = &s[6..11];` esetében a
`world` egy olyan slice lenne, amely az `s` 6-os indexű bájtjára mutató
pointert és az `5` hosszértéket tartalmazza.

A 4-7. ábra ezt szemlélteti.

<img alt="Három táblázat: az egyik az s stacken tárolt adatait ábrázolja, amely
a heapen lévő &quot;hello world&quot; sztringadat táblázatának 0-s indexű
bájtjára mutat. A harmadik táblázat a world slice stacken tárolt adatait
ábrázolja, amelynek hosszértéke 5, és a heapadat-táblázat 6-os bájtjára mutat."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">4-7. ábra: Egy string slice, amely egy `String` egy
részére hivatkozik</span>

Ugyanez futás közben: az alábbi ábrán a nyilak mutatják, hova mutatnak az egyes
referenciák. A `hello` és a `world` a heap-en lévő sztringadat egy-egy
szakaszára hivatkozik, míg az összehasonlításként felvett `s2` – amely nem
slice – magára a `String`-re:

```aquascope,interpreter
#fn main() {
let s = String::from("hello world");

let hello: &str = &s[0..5];
let world: &str = &s[6..11];
let s2: &String = &s;`[]`
#}
```

A slice-ok azért különleges referenciák, mert „kövér” pointerek: a címen kívül
metaadatot, jelen esetben a hosszt is tárolják. Ha a Rust adatszerkezeteinek a
belsejébe nézünk, ez láthatóvá válik – figyeld meg, hogy a `hello` és a `world`
is egy `ptr` és egy `len` mezőből áll, és hogy a `String` valójában egy
bájtvektor (`Vec<u8>`), amely egy `len` hosszt és egy `buf` puffert tartalmaz:

```aquascope,interpreter,concreteTypes,hideCode
fn main() {
    let s = String::from("hello world");

    let hello: &str = &s[0..5];
    let world: &str = &s[6..11];
    let s2: &String = &s;
    `[]`
}
```

A Rust `..` tartomány-szintaxisában, ha a 0-s indexnél akarsz kezdeni,
elhagyhatod a két pont előtti értéket. Más szóval ezek egyenértékűek:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

Ugyanígy, ha a slice tartalmazza a `String` utolsó bájtját is, elhagyhatod a
záró számot. Vagyis ezek egyenértékűek:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Mindkét értéket is elhagyhatod, ha a teljes sztringről akarsz slice-ot venni.
Tehát ezek egyenértékűek:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Megjegyzés: A string slice tartományindexeinek érvényes UTF-8
> karakterhatárokra kell esniük. Ha egy többbájtos karakter közepén próbálsz
> string slice-ot létrehozni, a programod hibával fog kilépni.

Mivel a slice referencia, a jogosultságokra is ugyanúgy hat, mint bármelyik
másik referencia. Az alábbi ábrán jól látszik: amint a `hello` slice létrejön,
`s` elveszíti a **W** és **O** jogosultságát, és csak a `hello` utolsó
használata után kapja vissza őket – ezért engedélyezett az `s.push_str` hívás:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut s = String::from("hello");
    let hello: &str = &s[0..5];
    println!("{hello}");
    s.push_str(" world");
}
```

Mindezek ismeretében írjuk át a `first_word` függvényt úgy, hogy slice-ot adjon
vissza. A „string slice” típust `&str` alakban írjuk:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

A szó végének indexét ugyanúgy kapjuk meg, mint a 4-7. listában: az első
szóköz előfordulását keressük. Amikor megtaláljuk a szóközt, egy string
slice-ot adunk vissza, amelynek kezdő- és végindexe a sztring eleje, illetve a
szóköz indexe.

Így amikor meghívjuk a `first_word` függvényt, egyetlen olyan értéket kapunk
vissza, amely hozzá van kötve a mögöttes adathoz. Az érték a slice
kezdőpontjára mutató referenciából és a slice elemszámából áll.

Egy `second_word` függvénynél is működne a slice visszaadása:

```rust,ignore
fn second_word(s: &String) -> &str {
```

Így egy egyszerű API-t kapunk, amelyet sokkal nehezebb elrontani, mert a
fordító gondoskodik róla, hogy a `String`-be mutató referenciák érvényesek
maradjanak. Emlékszel a 4-8. listában szereplő program hibájára, amikor
megkaptuk az első szó végének indexét, aztán kiürítettük a sztringet, így az
indexünk érvénytelenné vált? Az a kód logikailag hibás volt, de nem jelzett
azonnal semmilyen hibát. A problémák később bukkantak volna fel, ha
továbbra is használni próbáljuk az első szó indexét egy kiürített sztringgel.
A slice-ok lehetetlenné teszik ezt a hibát, és sokkal hamarabb tudtunkra
adják, hogy baj van a kódunkkal. A `first_word` slice-os változata fordítási
idejű hibát vált ki:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

Az ábrán most az látszik, ami a 4-8. listában még nem: a `first_word(&s)` hívás
után `s` **nem** kapja vissza a **W** jogosultságát, mert a visszaadott slice
továbbra is az `s`-re hivatkozik. Az `s.clear()` sorhoz így hiányzik a szükséges
jogosultság, amit az ábra pirossal jelez:

```aquascope,permissions,boundaries,stepper,shouldFail
#fn first_word(s: &String) -> &str {
#    let bytes = s.as_bytes();
#    for (i, &item) in bytes.iter().enumerate() {
#        if item == b' ' {
#            return &s[0..i];
#        }
#    }
#    &s[..]
#}
fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);
    s.clear();
    println!("the first word is: {word}");
}
```

Íme a fordítói hiba:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Emlékezz vissza a borrowing szabályaira: ha van egy nem módosítható
referenciánk valamire, akkor nem vehetünk fel rá módosítható referenciát is.
Mivel a `clear` metódusnak meg kell rövidítenie a `String`-et, módosítható
referenciát kell szereznie. A `clear` hívása utáni `println!` a `word`-ben lévő
referenciát használja, tehát a nem módosítható referenciának azon a ponton még
aktívnak kell lennie. A Rust nem engedi, hogy a `clear`-beli módosítható
referencia és a `word`-beli nem módosítható referencia egyszerre létezzen, így
a fordítás meghiúsul. A Rust nemcsak könnyebben használhatóvá tette az
API-nkat, hanem a hibák egy egész osztályát is kiküszöbölte fordítási időben!

<!-- Old headings. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### Sztringliterálok mint slice-ok

Emlékezz vissza: azt mondtuk, hogy a sztringliterálok a binárison belül
tárolódnak. Most, hogy ismerjük a slice-okat, végre rendesen megérthetjük a
sztringliterálokat:

```rust
let s = "Hello, world!";
```

Az `s` típusa itt `&str`: egy slice, amely a bináris adott pontjára mutat. Ez
egyben az oka annak is, hogy a sztringliterálok nem módosíthatók; az `&str`
ugyanis nem módosítható referencia.

#### String slice-ok paraméterként {#string-slices-as-parameters}

Ha tudjuk, hogy literálokból és `String` értékekből egyaránt vehetünk
slice-okat, az elvezet minket a `first_word` egy újabb javításához, mégpedig a
szignatúrájához:

```rust,ignore
fn first_word(s: &String) -> &str {
```

Egy tapasztaltabb rustacean helyette a 4-9. listában látható szignatúrát írná,
mert így ugyanazt a függvényt használhatjuk `&String` és `&str` értékekre is.

<Listing number="4-9" caption="A `first_word` függvény javítása azzal, hogy az `s` paraméter típusához string slice-ot használunk">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

Ha string slice-unk van, azt közvetlenül átadhatjuk. Ha `String`-ünk van,
átadhatjuk a `String` egy slice-át vagy egy referenciát a `String`-re. Ez a
rugalmasság a deref coercionöket használja ki, amely képességet a 15. fejezet
[„Deref coercionök használata függvényekben és metódusokban”][deref-coercions]<!--
ignore --> című szakaszában tárgyalunk.

Ha egy függvényt úgy definiálunk, hogy egy `String`-re mutató referencia
helyett string slice-ot vegyen át, azzal általánosabbá és hasznosabbá tesszük
az API-nkat anélkül, hogy bármilyen funkcionalitást elveszítenénk:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### Egyéb slice-ok

A string slice-ok, ahogy sejthető, kifejezetten sztringekhez valók. Létezik
azonban egy általánosabb slice típus is. Nézd meg ezt a tömböt:

```rust
let a = [1, 2, 3, 4, 5];
```

Ahogy egy sztring egy részére szeretnénk hivatkozni, úgy egy tömb egy részére
is hivatkozhatunk. Ezt így tennénk:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

Ennek a slice-nak a típusa `&[i32]`. Ugyanúgy működik, mint a string slice-ok:
az első elemre mutató referenciát és egy hosszt tárol. Ezt a fajta slice-ot
mindenféle más kollekcióhoz is használni fogod. Ezekről a kollekciókról
részletesen a 8. fejezetben, a vektorok kapcsán lesz szó.

Ez a slice is kölcsönveszi a tömböt: amíg él, `a` elveszíti a **W** és **O**
jogosultságát, ahogy az alábbi ábrán látható:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut a = [1, 2, 3, 4, 5];
    let slice = &a[1..3];
    println!("{slice:?}");
    a[0] = 10;
}
```

A felépítése is ugyanaz, mint a string slice-oké. Egy vektor szeletének a
belsejébe nézve látszik, hogy a `slice` itt is egy `ptr` és egy `len` mezőből
áll, és a `ptr` a kollekció második elemére mutat:

```aquascope,interpreter,concreteTypes
#fn main() {
let a = vec![1, 2, 3, 4, 5];
let slice = &a[1..3];`[]`
#}
```

## Összefoglalás

Az ownership, a borrowing és a slice-ok fogalmai fordítási időben biztosítják a
memóriabiztonságot a Rust-programokban. A Rust nyelv ugyanúgy kezedbe adja a
memóriahasználat feletti irányítást, mint a többi rendszerprogramozási nyelv.
Az viszont, hogy az adat ownere automatikusan feltakarít az adat után, amikor
kikerül a hatóköréből, azt jelenti, hogy nem kell külön kódot írnod és
hibakeresned ehhez az irányításhoz.

Az ownership a Rust sok más részének a működésére is hatással van, ezért ezekről
a fogalmakról a könyv hátralévő részében is beszélni fogunk. Lépjünk tovább az
5. fejezetre, és nézzük meg, hogyan csoportosíthatunk adatdarabkákat egy
`struct`-ba.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#using-deref-coercions-in-functions-and-methods
