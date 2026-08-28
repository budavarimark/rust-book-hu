## Metódusok {#methods}

A metódusok hasonlítanak a függvényekhez: az `fn` kulcsszóval és egy névvel
deklaráljuk őket, lehetnek paramétereik és visszatérési értékük, és tartalmaznak
valamennyi kódot, amely lefut, amikor a metódust máshonnan meghívják. A
függvényekkel ellentétben a metódusokat egy struct (vagy egy enum, illetve egy
trait object, amelyekről a [6. fejezetben][enums]<!-- ignore -->, illetve a
[18. fejezetben][trait-objects]<!-- ignore --> lesz szó) kontextusán belül
definiáljuk, és az első paraméterük mindig a `self`, amely azt a
struct-példányt jelöli, amelyen a metódust meghívják.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Metódusszintaxis {#method-syntax}

Alakítsuk át az `area` függvényt, amelynek paramétere egy `Rectangle` példány,
és készítsünk helyette egy `Rectangle` struct-on definiált `area` metódust,
ahogy az 5-13. listában látható.

<Listing number="5-13" file-name="src/main.rs" caption="Egy `area` metódus definiálása a `Rectangle` struct-on">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Ahhoz, hogy a függvényt a `Rectangle` kontextusán belül definiáljuk, nyitunk
egy `impl` (implementation) blokkot a `Rectangle`-höz. Minden, ami ebben az
`impl` blokkban van, a `Rectangle` típushoz fog tartozni. Ezután áthelyezzük az
`area` függvényt az `impl` kapcsos zárójelei közé, és az első (ebben az esetben
egyetlen) paramétert `self`-re cseréljük a szignatúrában és a törzsben
mindenütt. A `main`-ben, ahol korábban az `area` függvényt hívtuk meg a `rect1`
argumentummal, most _metódusszintaxist_ használhatunk, hogy meghívjuk az `area`
metódust a `Rectangle` példányunkon. A metódusszintaxis a példány után
következik: egy pontot írunk, azt követi a metódus neve, a zárójelek és az
esetleges argumentumok.

Az `area` szignatúrájában a `rectangle: &Rectangle` helyett `&self` szerepel. A
`&self` valójában a `self: &Self` rövidítése. Egy `impl` blokkon belül a `Self`
típus annak a típusnak az aliasa, amelyhez az `impl` blokk tartozik. A
metódusok első paramétere kötelezően egy `Self` típusú, `self` nevű paraméter,
ezért a Rust megengedi, hogy ezt az első paraméterhelyen pusztán a `self` névvel
rövidítsd. Vedd észre, hogy a `self` rövidítés elé továbbra is ki kell tennünk a
`&`-t, jelezve, hogy ez a metódus borrow-olja a `Self` példányt, ahogy a
`rectangle: &Rectangle` esetében is tettük. A metódusok átvehetik a `self`
ownershipjét, borrow-olhatják a `self`-et nem módosíthatóan – ahogy itt tettük
–, vagy borrow-olhatják módosíthatóan, akárcsak bármely más paramétert.

A metódushívás semmit nem másol le: a `rect1.area()` valójában a
`Rectangle::area(&rect1)` hívás, ezért az `area` keretében a `self` csak egy
pointer. Az `L2` pontban két keret van a stack-en – a `main` és az `area` –, és
a `self` a `main`-ben élő `rect1`-re mutat; az `L3` pontban az `area` kerete
már eltűnt, a `rect1` viszont változatlanul él:

```aquascope,interpreter
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {
    fn area(&self) -> u32 {
        `[]`self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };`[]`
    let area = rect1.area();`[]`
}
```

Itt ugyanazért választottuk a `&self`-et, amiért a függvényes változatban a
`&Rectangle`-t használtuk: nem akarjuk átvenni az ownershipet, csak olvasni
akarjuk a struct adatait, nem írni. Ha a metódus feladatának részeként meg
akarnánk változtatni azt a példányt, amelyen a metódust meghívtuk, akkor
`&mut self` lenne az első paraméter. Ritka az olyan metódus, amely a puszta
`self` első paraméterrel átveszi a példány ownershipjét; ezt a technikát
általában akkor használják, amikor a metódus a `self`-et valami mássá alakítja
át, és meg akarod akadályozni, hogy a hívó az átalakítás után is használja az
eredeti példányt.

A három forma közötti különbség a jogosultsági ábrákon látszik a legjobban.
Tegyük fel, hogy a `Rectangle`-höz az `area(&self)` mellett egy
`set_width(&mut self, width: u32)` és egy `max(self, other: Rectangle)`
metódust is definiálunk. Egy nem módosítható `rect` változónak **R** és **O**
jogosultsága van, ezért az `area` (`&self`) és a `max` (`self`) hívása is
megengedett:

```aquascope,permissions,boundaries,stepper
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {
#    fn area(&self) -> u32 {
#        self.width * self.height
#    }
#
#    fn set_width(&mut self, width: u32) {
#        self.width = width;
#    }
#
#    fn max(self, other: Rectangle) -> Rectangle {
#        Rectangle {
#            width: self.width.max(other.width),
#            height: self.height.max(other.height),
#        }
#    }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0,
};
println!("{}", rect.area());

let other_rect = Rectangle { width: 1, height: 1 };
let max_rect = rect.max(other_rect);
#}
```

A `set_width` viszont **W** jogosultságot kíván a `rect`-en, mert a `&mut self`
paraméter módosítható borrow-t igényel. Ez a jogosultság a `mut` nélkül
deklarált `rect`-nek nincs meg, ezért a fordító elutasítja a hívást:

```aquascope,permissions,boundaries,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {
#    fn area(&self) -> u32 {
#        self.width * self.height
#    }
#
#    fn set_width(&mut self, width: u32) {
#        self.width = width;
#    }
#
#    fn max(self, other: Rectangle) -> Rectangle {
#        Rectangle {
#            width: self.width.max(other.width),
#            height: self.height.max(other.height),
#        }
#    }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0,
};
rect.set_width(0);
#}
```

A puszta `self` első paraméter ezzel szemben elmozgatja a példányt: a
`rect.max(...)` hívás elhasználja a `rect` **O** jogosultságát, és utána a
`rect` minden jogosultságát elveszíti, ezért a rá következő `rect.area()` már
nem fordul le:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {
#    fn area(&self) -> u32 {
#        self.width * self.height
#    }
#
#    fn set_width(&mut self, width: u32) {
#        self.width = width;
#    }
#
#    fn max(self, other: Rectangle) -> Rectangle {
#        Rectangle {
#            width: self.width.max(other.width),
#            height: self.height.max(other.height),
#        }
#    }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0,
};
let other_rect = Rectangle {
    width: 1,
    height: 1,
};
let max_rect = rect.max(other_rect);
println!("{}", rect.area());
#}
```

A metódusok függvények helyett való használatának fő oka – azon túl, hogy
metódusszintaxist kapunk, és nem kell minden metódus szignatúrájában
megismételni a `self` típusát – a rendezettség. Egy adott típus példányaival
végezhető összes műveletet egyetlen `impl` blokkba tettük, ahelyett hogy a
kódunk jövőbeli használóinak a `Rectangle` képességeit az általunk nyújtott
könyvtár különböző helyein kellene keresgélniük.

Vedd észre, hogy egy metódusnak adhatjuk ugyanazt a nevet, mint a struct
valamelyik mezőjének. Például definiálhatunk a `Rectangle`-ön egy szintén
`width` nevű metódust:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Itt úgy döntünk, hogy a `width` metódus `true` értéket ad vissza, ha a példány
`width` mezőjének értéke nagyobb `0`-nál, és `false`-ot, ha az érték `0`:
bármilyen célra használhatunk egy mezőt az azonos nevű metóduson belül. A
`main`-ben, amikor a `rect1.width` után zárójeleket írunk, a Rust tudja, hogy a
`width` metódusra gondolunk. Ha nem használunk zárójeleket, a Rust tudja, hogy
a `width` mezőre gondolunk.

Gyakran – de nem mindig – amikor egy metódusnak ugyanazt a nevet adjuk, mint egy
mezőnek, azt szeretnénk, hogy csak a mező értékét adja vissza, és semmi mást ne
csináljon. Az ilyen metódusokat _getter_-eknek nevezzük, és a Rust nem
implementálja őket automatikusan a struct mezőihez, ahogy néhány más nyelv
teszi. A getterek azért hasznosak, mert a mezőt priváttá teheted, a metódust
viszont publikussá, és így csak olvasható hozzáférést engedélyezhetsz ahhoz a
mezőhöz a típus publikus API-jának részeként. Arról, hogy mit jelent a publikus
és a privát, és hogyan jelölhető egy mező vagy metódus publikusnak, illetve
privátnak, a [7. fejezetben][public]<!-- ignore --> lesz szó.

> ### Hol van a `->` operátor? {#wheres-the---operator}
>
> A C-ben és a C++-ban két különböző operátort használnak metódushívásra: a
> `.`-ot akkor, ha közvetlenül az objektumon hívsz meg egy metódust, és a
> `->`-t akkor, ha az objektumra mutató pointeren hívod meg a metódust, és
> előbb dereferálnod kell a pointert. Más szóval, ha az `object` egy pointer,
> akkor az `object->something()` hasonló a `(*object).something()`-hoz.
>
> A Rustban nincs a `->` operátornak megfelelő operátor; helyette a Rustnak van
> egy _automatikus referenciaképzés és dereferálás_ nevű képessége. A
> metódushívás azon kevés helyek egyike a Rustban, ahol ez a viselkedés
> érvényesül.
>
> Így működik: amikor egy metódust az `object.something()` alakban hívsz meg, a
> Rust automatikusan hozzáadja a `&`, `&mut` vagy `*` jelet, hogy az `object`
> illeszkedjen a metódus szignatúrájához. Más szóval a következők azonosak:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> Az első sokkal tisztább. Ez az automatikus referenciaképzés azért működik,
> mert a metódusoknak egyértelmű a fogadójuk – a `self` típusa. A fogadó és a
> metódus neve alapján a Rust egyértelműen el tudja dönteni, hogy a metódus
> olvas (`&self`), módosít (`&mut self`) vagy felemészti az értéket (`self`).
> Az, hogy a Rust a metódusfogadóknál implicitté teszi a borrowingot, nagyban
> hozzájárul ahhoz, hogy az ownership a gyakorlatban kényelmesen használható
> legyen.

### Több paraméterrel rendelkező metódusok

Gyakoroljuk a metódusok használatát azzal, hogy egy második metódust is
implementálunk a `Rectangle` struct-on. Ezúttal azt szeretnénk, hogy egy
`Rectangle` példány átvegyen egy másik `Rectangle` példányt, és `true`-t adjon
vissza, ha a második `Rectangle` teljes egészében belefér a `self`-be (az első
`Rectangle`-be); egyébként `false`-ot kell visszaadnia. Vagyis ha egyszer
definiáltuk a `can_hold` metódust, szeretnénk meg tudni írni az 5-14.
listában látható programot.

<Listing number="5-14" file-name="src/main.rs" caption="A még meg nem írt `can_hold` metódus használata">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

A várt kimenet a következőképpen nézne ki, mivel a `rect2` mindkét mérete
kisebb a `rect1` méreteinél, a `rect3` viszont szélesebb a `rect1`-nél:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Tudjuk, hogy metódust akarunk definiálni, tehát az `impl Rectangle` blokkon
belül lesz. A metódus neve `can_hold` lesz, és paraméterként egy másik
`Rectangle` nem módosítható borrow-ját veszi át. Hogy mi lesz a paraméter
típusa, azt a metódust hívó kódból tudhatjuk meg: a `rect1.can_hold(&rect2)` a
`&rect2`-t adja át, ami a `rect2`, egy `Rectangle` példány nem módosítható
borrow-ja. Ennek van értelme, hiszen csak olvasnunk kell a `rect2`-t (nem
írnunk, ami módosítható borrow-ot igényelne), és azt szeretnénk, hogy a `main`
megtartsa a `rect2` ownershipjét, hogy a `can_hold` metódus hívása után is
használhassuk. A `can_hold` visszatérési értéke logikai érték lesz, az
implementáció pedig azt ellenőrzi, hogy a `self` szélessége és magassága
nagyobb-e a másik `Rectangle` szélességénél, illetve magasságánál. Adjuk hozzá
az új `can_hold` metódust az 5-13. lista `impl` blokkjához, ahogy az 5-15.
listában látható.

<Listing number="5-15" file-name="src/main.rs" caption="A `can_hold` metódus implementálása a `Rectangle`-ön, amely paraméterként egy másik `Rectangle` példányt vesz át">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Ha ezt a kódot az 5-14. lista `main` függvényével futtatjuk, megkapjuk a kívánt
kimenetet. A metódusoknak több paraméterük is lehet, amelyeket a `self`
paraméter után adunk hozzá a szignatúrához, és ezek a paraméterek pontosan úgy
működnek, mint a függvények paraméterei.

A `can_hold` keretében jól látszik, hogy egyik téglalap sem másolódik le: az
`L2` pontban a `self` és az `other` is a `main` keretében élő `Rectangle`
példányokra mutató pointer. Ezért marad a `rect1` és a `rect2` is használható a
hívás után, az `L3` pontban:

```aquascope,interpreter
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        `[]`self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    let rect2 = Rectangle {
        width: 10,
        height: 40,
    };`[]`
    let fits = rect1.can_hold(&rect2);`[]`
}
```

### Asszociált függvények

Az `impl` blokkon belül definiált összes függvényt _asszociált függvénynek_
nevezzük, mert ahhoz a típushoz vannak társítva, amelynek a neve az `impl` után
áll. Definiálhatunk olyan asszociált függvényeket is, amelyeknek nem a `self` az
első paraméterük (és így nem metódusok), mert nincs szükségük a típus egy
példányára a működésükhöz. Egy ilyen függvényt már használtunk is: a `String`
típuson definiált `String::from` függvényt.

A nem metódus asszociált függvényeket gyakran használják konstruktorként,
amelyek a struct egy új példányát adják vissza. Ezeket sokszor `new`-nak
nevezik, de a `new` nem különleges név, és nincs beépítve a nyelvbe. Például
dönthetünk úgy, hogy egy `square` nevű asszociált függvényt biztosítunk,
amelynek egyetlen mérete van paraméterként, és ezt használja szélességként és
magasságként is, így könnyebbé téve egy négyzet alakú `Rectangle`
létrehozását, mintha kétszer kellene megadni ugyanazt az értéket:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

A visszatérési típusban és a függvény törzsében szereplő `Self` kulcsszavak
annak a típusnak az aliasai, amely az `impl` kulcsszó után áll, ami ebben az
esetben a `Rectangle`.

Ennek az asszociált függvénynek a hívásához a `::` szintaxist használjuk a
struct nevével; erre példa a `let sq = Rectangle::square(3);`. Ezt a függvényt
a struct névtérbe zárja: a `::` szintaxist mind az asszociált függvényekhez,
mind a modulok által létrehozott névterekhez használjuk. A modulokról a
[7. fejezetben][modules]<!-- ignore --> lesz szó.

### Több `impl` blokk

Minden struct-hoz több `impl` blokk is tartozhat. Például az 5-15. lista
egyenértékű az 5-16. listában látható kóddal, amelyben minden metódus a saját
`impl` blokkjában van.

<Listing number="5-16" caption="Az 5-15. lista újraírása több `impl` blokkal">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Itt semmi okunk nincs több `impl` blokkra szétosztani ezeket a metódusokat, de
ez érvényes szintaxis. A 10. fejezetben, ahol a generikus típusokról és a
trait-ekről lesz szó, látunk majd olyan esetet, amelyben a több `impl` blokk
hasznos.

## Összefoglalás

A struct-okkal olyan saját típusokat hozhatsz létre, amelyeknek a te
szakterületeden van jelentésük. A struct-ok segítségével az összetartozó
adatdarabokat összekapcsolva tarthatod, és mindegyiket elnevezheted, hogy
világos legyen a kódod. Az `impl` blokkokban a típusodhoz társított
függvényeket definiálhatsz, a metódusok pedig az asszociált függvények olyan
fajtája, amellyel megadhatod, hogyan viselkednek a struct-jaid példányai.

De a struct-ok nem az egyetlen módja saját típusok létrehozásának: forduljunk a
Rust enumjaihoz, hogy egy újabb eszközzel bővítsük az eszköztáradat.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
