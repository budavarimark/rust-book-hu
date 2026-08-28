## Minden hely, ahol mintákat használhatunk

A minták a Rustban számos helyen felbukkannak, és te már eddig is sokat
használtad őket anélkül, hogy tudtál volna róla! Ez a szakasz azokat a helyeket
veszi sorra, ahol a minták érvényesek.

### `match`-ágak

Ahogy a 6. fejezetben szó volt róla, a `match` kifejezések ágaiban mintákat
használunk. Formálisan a `match` kifejezés a `match` kulcsszóból, egy
illesztendő értékből, valamint egy vagy több `match`-ágból áll; egy ág egy
mintából és egy kifejezésből tevődik össze, amely akkor fut le, ha az érték
illeszkedik az ág mintájára – így:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Például itt van a 6-5. listából származó `match` kifejezés, amely az `x`
változóban lévő `Option<i32>` értékre illeszt:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Ebben a `match` kifejezésben a minták a nyilaktól balra álló `None` és
`Some(i)`.

A `match` kifejezésekkel szemben az egyik követelmény, hogy kimerítők legyenek,
vagyis a `match` kifejezésben szereplő érték minden lehetőségét le kell fedniük.
Az egyik módja annak, hogy minden lehetőséget lefedj, ha az utolsó ágban egy
mindent elkapó mintát használsz: például egy bármilyen értékre illeszkedő
változónév soha nem hiúsulhat meg, így lefedi az összes megmaradt esetet.

A `_` minta bármire illeszkedik, de soha nem köt hozzá változót, ezért gyakran
az utolsó `match`-ágban szerepel. A `_` minta például akkor hasznos, ha minden
nem részletezett értéket figyelmen kívül szeretnél hagyni. A `_` mintával
részletesebben az [„Értékek figyelmen kívül hagyása egy
mintában”][ignoring-values-in-a-pattern]<!-- ignore --> szakaszban foglalkozunk
a fejezet későbbi részében.

### `let` utasítások

E fejezet előtt csak a `match` és az `if let` melletti mintahasználatról esett
kifejezetten szó, valójában azonban máshol is használtunk mintákat, például a
`let` utasításokban. Nézd meg például ezt az egyszerű értékadást `let`-tel:

```rust
let x = 5;
```

Minden alkalommal, amikor egy ilyen `let` utasítást írtál, mintát használtál,
még ha nem is tudatosult benned! Formálisabban a `let` utasítás így néz ki:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Az olyan utasításokban, mint a `let x = 5;`, ahol a PATTERN helyén egy
változónév áll, a változónév csupán a minta egy különösen egyszerű formája. A
Rust összeveti a kifejezést a mintával, és értéket ad a benne talált neveknek. A
`let x = 5;` példában tehát az `x` egy olyan minta, amelynek jelentése: „kösd az
`x` változóhoz azt, ami ide illeszkedik”. Mivel az `x` név maga a teljes minta,
ez a minta gyakorlatilag azt jelenti: „kösd az `x` változóhoz az egészet, bármi
legyen is az érték”.

Hogy a `let` mintaillesztő természete jobban látsszon, nézzük meg a 19-1.
listát, amely egy mintát használ a `let`-tel egy tuple destrukturálására.


<Listing number="19-1" caption="Minta használata egy tuple destrukturálására és három változó egyidejű létrehozására">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Itt egy tuple-t illesztünk egy mintára. A Rust összeveti az `(1, 2, 3)` értéket
az `(x, y, z)` mintával, és látja, hogy az érték illeszkedik a mintára – vagyis
azt látja, hogy az elemek száma mindkettőben ugyanannyi –, ezért az `1`-et az
`x`-hez, a `2`-t az `y`-hoz, a `3`-at pedig a `z`-hez köti. Ezt a tuple-mintát
úgy is felfoghatod, mint amely három különálló változómintát ágyaz be magába.

Ha a mintában lévő elemek száma nem egyezik meg a tuple elemeinek számával, a
teljes típus nem fog illeszkedni, és fordítási hibát kapunk. A 19-2. lista
például azt mutatja be, hogyan próbálunk meg egy háromelemű tuple-t két
változóba destrukturálni – ez nem működik.

<Listing number="19-2" caption="Hibásan megalkotott minta, amelynek változói nem felelnek meg a tuple elemszámának">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Ha megpróbáljuk lefordítani ezt a kódot, a következő típushibát kapjuk:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

A hiba javításához a tuple egy vagy több értékét figyelmen kívül hagyhatnánk a
`_` vagy a `..` használatával, ahogy azt az [„Értékek figyelmen kívül
hagyása egy mintában”][ignoring-values-in-a-pattern]<!-- ignore -->
szakaszban látni fogod.
Ha a gond az, hogy túl sok változó van a mintában, a megoldás az, hogy a típusok
összeillesztéséhez változókat távolítunk el, amíg a változók száma meg nem
egyezik a tuple elemeinek számával.

### Feltételes `if let` kifejezések

A 6. fejezetben arról volt szó, hogyan használhatjuk az `if let` kifejezéseket
elsősorban egy olyan `match` rövidebb leírására, amely csak egyetlen esetre
illeszt. Az `if let` mellé opcionálisan `else` ág is kerülhet, amely olyan kódot
tartalmaz, ami akkor fut le, ha az `if let`-ben lévő minta nem illeszkedik.

A 19-3. lista azt mutatja, hogy az `if let`, az `else if` és az `else if let`
kifejezéseket tetszés szerint vegyíthetjük is. Ez nagyobb rugalmasságot ad, mint
egy `match` kifejezés, amelyben csak egyetlen értéket adhatunk meg a mintákkal
való összevetésre. Ráadásul a Rust nem követeli meg, hogy az egymást követő `if
let`, `else if` és `else if let` ágak feltételei bármilyen kapcsolatban legyenek
egymással.

A 19-3. listában szereplő kód több feltétel ellenőrzése alapján dönti el, milyen
színű legyen a háttér. Ebben a példában olyan változókat hoztunk létre, amelyek
beégetett értékeket tartalmaznak; egy valódi program ezeket a felhasználótól
kapná meg.

<Listing number="19-3" file-name="src/main.rs" caption="Az `if let`, `else if`, `else if let` és `else` vegyítése">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Ha a felhasználó megad egy kedvenc színt, azt használjuk háttérszínként. Ha
nincs megadva kedvenc szín, és ma kedd van, a háttérszín zöld lesz. Egyébként ha
a felhasználó szövegként adja meg az életkorát, és azt sikerül számmá
alakítanunk, a szín a szám értékétől függően lila vagy narancssárga lesz. Ha e
feltételek egyike sem teljesül, a háttérszín kék lesz.

Ez a feltételes szerkezet lehetővé teszi, hogy összetett követelményeket
támogassunk. Az itt szereplő beégetett értékekkel ez a példa a `Using purple as
the background color` szöveget írja ki.

Láthatod, hogy az `if let` is bevezethet olyan új változókat, amelyek
árnyékolják (shadowing) a meglévőket, ugyanúgy, ahogy a `match`-ágak: az `if let
Ok(age) = age` sor egy új `age` változót vezet be, amely az `Ok` variánsban lévő
értéket tartalmazza, és shadowingolja a meglévő `age` változót. Ez azt jelenti,
hogy az
`if age > 30` feltételt ezen a blokkon belülre kell tennünk: nem vonhatjuk össze
ezt a két feltételt `if let Ok(age) = age && age > 30` alakba. Az új `age`,
amelyet a 30-hoz akarunk hasonlítani, csak akkor válik érvényessé, amikor a
kapcsos zárójellel elkezdődik az új hatókör.

Az `if let` kifejezések hátránya, hogy a fordító nem ellenőrzi a kimerítőséget,
míg a `match` kifejezéseknél igen. Ha elhagynánk az utolsó `else` blokkot, és
ezzel néhány esetet kezeletlenül hagynánk, a fordító nem figyelmeztetne minket a
lehetséges logikai hibára.

### `while let` feltételes ciklusok

Az `if let`-hez hasonló felépítésű `while let` feltételes ciklus lehetővé teszi,
hogy egy `while` ciklus addig fusson, amíg egy minta illeszkedik. A 19-4.
listában egy olyan `while let` ciklust mutatunk be, amely szálak között küldött
üzenetekre vár, de ezúttal `Option` helyett `Result` értéket vizsgál.

<Listing number="19-4" caption="`while let` ciklus használata értékek kiírására mindaddig, amíg az `rx.recv()` `Ok` értéket ad vissza">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Ez a példa az `1`, `2`, majd a `3` értéket írja ki. A `recv` metódus kiveszi az
első üzenetet a csatorna fogadó oldaláról, és egy `Ok(value)` értéket ad vissza.
Amikor a 16. fejezetben először találkoztunk a `recv` metódussal, közvetlenül
kicsomagoltuk a hibát, vagy iterátorként dolgoztunk vele egy `for` ciklusban.
Ahogy azonban a 19-4. lista mutatja, `while let`-et is használhatunk, mert a
`recv` metódus minden beérkező üzenetnél `Ok` értéket ad vissza, amíg a küldő
létezik, majd `Err` értéket ad, ha a küldő oldal lecsatlakozott.

### `for` ciklusok

Egy `for` ciklusban a `for` kulcsszót közvetlenül követő érték egy minta. A `for
x in y` esetében például az `x` a minta. A 19-5. lista azt mutatja be, hogyan
használhatunk mintát egy `for` ciklusban egy tuple destrukturálására, vagyis
szétbontására a `for` ciklus részeként.


<Listing number="19-5" caption="Minta használata egy `for` ciklusban egy tuple destrukturálására">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

A 19-5. listában szereplő kód a következőt írja ki:


```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Az `enumerate` metódussal alakítjuk át az iterátort úgy, hogy az egy értéket és
az érték indexét adja vissza egy tuple-be csomagolva. Az első előállított érték
a
`(0, 'a')` tuple. Amikor ezt az értéket az `(index, value)` mintára illesztjük,
az index `0` lesz, a value pedig `'a'`, és ez adja a kimenet első sorát.


### Függvényparaméterek

A függvényparaméterek is lehetnek minták. A 19-6. listában szereplő kód, amely
egy `foo` nevű függvényt deklarál egyetlen `i32` típusú, `x` nevű paraméterrel,
mostanra már ismerősnek tűnik.

<Listing number="19-6" caption="Mintákat használó függvényszignatúra a paraméterekben">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Az `x` rész egy minta! Ahogy a `let`-nél tettük, a függvény argumentumaiban is
illeszthetnénk egy tuple-t a mintára. A 19-7. lista egy tuple értékeit bontja
szét, miközben átadjuk azt egy függvénynek.

<Listing number="19-7" file-name="src/main.rs" caption="Függvény, amelynek paraméterei destrukturálnak egy tuple-t">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Ez a kód a `Current location: (3, 5)` szöveget írja ki. A `&(3, 5)` érték
illeszkedik a `&(x, y)` mintára, így az `x` a `3` érték, az `y` pedig az `5`
lesz.

Closure-ök paraméterlistájában ugyanúgy használhatunk mintákat, mint a
függvények paraméterlistájában, hiszen a closure-ök hasonlítanak a
függvényekre, ahogy azt a 13. fejezetben tárgyaltuk.

Ezen a ponton már többféle mintahasználatot láttál, de a minták nem mindenütt
működnek egyformán. Bizonyos helyeken a mintáknak cáfolhatatlannak kell lenniük;
más körülmények között lehetnek cáfolhatók is. A következőkben ezt a két
fogalmat tárgyaljuk.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
