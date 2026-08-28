<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closure-ök

A Rust closure-jei névtelen függvények, amelyeket változóban tárolhatsz vagy
argumentumként átadhatsz más függvényeknek. A closure-t létrehozhatod az egyik
helyen, majd máshol meghívhatod, hogy egy másik kontextusban értékelődjön ki. A
függvényekkel ellentétben a closure-ök képesek értékeket elkapni abból a
hatókörből, amelyben definiálva vannak. Bemutatjuk, hogyan teszik lehetővé a
closure-ök ezen képességei a kód újrafelhasználását és a viselkedés testreszabását.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### A környezet elkapása

Először azt vizsgáljuk meg, hogyan használhatunk closure-öket arra, hogy
értékeket kapjunk el a környezetből, amelyben definiálva vannak, későbbi
felhasználásra. A helyzet a következő: a pólócégünk időről időre elajándékoz
egy exkluzív, limitált kiadású pólót valakinek a levelezőlistánkról,
promócióként. A levelezőlistán szereplők tetszés szerint megadhatják a
kedvenc színüket a profiljukban. Ha az ingyenes pólóra kiválasztott személynek
be van állítva a kedvenc színe, olyan színű pólót kap. Ha az illető nem adott
meg kedvenc színt, akkor abból a színből kap, amelyikből a cégnek jelenleg a
legtöbb van.

Ezt sokféleképpen meg lehet valósítani. Ebben a példában egy `ShirtColor` nevű
enumot fogunk használni, amelynek `Red` és `Blue` variánsai vannak (az
egyszerűség kedvéért korlátozzuk az elérhető színek számát). A cég készletét
egy `Inventory` structtal ábrázoljuk, amelynek van egy `shirts` nevű mezője,
és ez egy `Vec<ShirtColor>` értéket tartalmaz, amely a jelenleg raktáron lévő
pólószíneket adja meg. Az `Inventory`-n definiált `giveaway` metódus megkapja az
ingyenpóló nyertesének esetleges pólószín-preferenciáját, és visszaadja azt a
pólószínt, amelyet az illető kapni fog. Ezt a felállást mutatja a 13-1. lista.

<Listing number="13-1" file-name="src/main.rs" caption="A pólócég ajándékozási helyzete">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

A `main`-ben definiált `store`-ban két kék és egy piros póló maradt, amelyeket
ebben a limitált kiadású promócióban szét lehet osztani. Meghívjuk a `giveaway`
metódust egy piros pólót preferáló felhasználóra és egy olyanra, akinek nincs
preferenciája.

Ismét: ezt a kódot sokféleképpen meg lehetne írni, és itt, hogy a closure-ökre
összpontosítsunk, olyan fogalmakhoz ragaszkodtunk, amelyeket már megtanultál,
kivéve a `giveaway` metódus törzsét, amely closure-t használ. A `giveaway`
metódusban `Option<ShirtColor>` típusú paraméterként kapjuk meg a felhasználó
preferenciáját, és meghívjuk az `unwrap_or_else` metódust a `user_preference`-en.
Az [`Option<T>` `unwrap_or_else` metódusát][unwrap-or-else]<!-- ignore --> a
standard könyvtár definiálja. Egyetlen argumentumot vár: egy argumentum nélküli
closure-t, amely `T` típusú értéket ad vissza (ugyanazt a típust, amelyet az
`Option<T>` `Some` variánsa tárol, ebben az esetben `ShirtColor`-t). Ha az
`Option<T>` a `Some` variáns, az `unwrap_or_else` a `Some`-on belüli értéket
adja vissza. Ha az `Option<T>` a `None` variáns, az `unwrap_or_else` meghívja a
closure-t, és a closure által visszaadott értéket adja vissza.

A `|| self.most_stocked()` closure-kifejezést adjuk meg az `unwrap_or_else`
argumentumaként. Ez egy olyan closure, amelynek magának nincsenek paraméterei
(ha a closure-nek lennének paraméterei, azok a két függőleges vonal között
jelennének meg). A closure törzse a `self.most_stocked()` hívást tartalmazza. A
closure-t itt definiáljuk, az `unwrap_or_else` implementációja pedig később
értékeli ki, ha szükség van az eredményre.

Ezt a kódot futtatva a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Az egyik érdekes szempont itt az, hogy olyan closure-t adtunk át, amely az
aktuális `Inventory` példányon hívja meg a `self.most_stocked()`-ot. A standard
könyvtárnak semmit nem kellett tudnia az általunk definiált `Inventory` vagy
`ShirtColor` típusokról, sem arról a logikáról, amelyet ebben a helyzetben
használni akarunk. A closure elkap egy nem módosítható referenciát a `self`
`Inventory` példányra, és az általunk megadott kóddal együtt átadja az
`unwrap_or_else` metódusnak. A függvények ezzel szemben nem képesek ilyen módon
elkapni a környezetüket.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Closure-típusok kikövetkeztetése és annotálása

További különbségek is vannak a függvények és a closure-ök között. A closure-ök
általában nem követelik meg, hogy annotáld a paraméterek vagy a visszatérési
érték típusait, ahogy azt az `fn` függvényeknél kell. A függvényeknél azért
kötelezők a típusannotációk, mert a típusok egy explicit interfész részei,
amelyet a felhasználóid felé teszel közzé. Ennek az interfésznek a szigorú
meghatározása fontos annak biztosításához, hogy mindenki egyetértsen abban,
milyen típusú értékeket használ és ad vissza egy függvény. A closure-ök ezzel
szemben nem ilyen közzétett interfészben szerepelnek: változókban tároljuk őket,
és úgy használjuk őket, hogy nem nevezzük el és nem tesszük közzé őket a
könyvtárunk felhasználói felé.

A closure-ök jellemzően rövidek, és csak egy szűk kontextusban relevánsak, nem
pedig tetszőleges helyzetekben. Ezekben a korlátozott kontextusokban a fordító
ki tudja következtetni a paraméterek típusait és a visszatérési típust, hasonlóan
ahhoz, ahogy a legtöbb változó típusát is ki tudja következtetni (ritkán
előfordul, hogy a fordítónak closure-típusannotációkra is szüksége van).

A változókhoz hasonlóan hozzáadhatunk típusannotációkat, ha növelni akarjuk az
explicitséget és az érthetőséget, cserébe azért, hogy a szükségesnél
bőbeszédűbbek leszünk. Egy closure típusainak annotálása úgy nézne ki, ahogy a
13-2. listában látható definíció. Ebben a példában úgy definiálunk egy
closure-t, hogy változóban tároljuk, ahelyett hogy ott definiálnánk, ahol
argumentumként átadjuk, mint a 13-1. listában.

<Listing number="13-2" file-name="src/main.rs" caption="A paraméter- és a visszatérésitípus opcionális típusannotációinak hozzáadása a closure-höz">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

A típusannotációk hozzáadásával a closure-ök szintaxisa jobban hasonlít a
függvények szintaxisára. Itt összehasonlításképpen definiálunk egy függvényt,
amely 1-et ad a paraméteréhez, és egy closure-t, amely ugyanígy viselkedik.
Néhány szóközt is beszúrtunk, hogy a megfelelő részek egy vonalba kerüljenek. Ez
jól szemlélteti, mennyire hasonlít a closure-szintaxis a függvényszintaxisra,
eltekintve a függőleges vonalak használatától és attól, hogy mennyi szintaxis
opcionális:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Az első sor egy függvénydefiníciót mutat, a második egy teljesen annotált
closure-definíciót. A harmadik sorban elhagyjuk a típusannotációkat a
closure-definícióból. A negyedik sorban elhagyjuk a kapcsos zárójeleket,
amelyek opcionálisak, mert a closure törzse csak egyetlen kifejezésből áll.
Ezek mind érvényes definíciók, és meghívva ugyanazt a viselkedést produkálják.
Az `add_one_v3` és az `add_one_v4` sorokhoz ki kell értékelni a closure-öket
ahhoz, hogy le tudjanak fordulni, mert a típusok a használatukból következnek
ki. Ez hasonló ahhoz, ahogy a `let v = Vec::new();` esetében is szükség van
típusannotációkra vagy arra, hogy valamilyen típusú értékeket szúrjunk be a
`Vec`-be, hogy a Rust ki tudja következtetni a típust.

A closure-definíciók esetében a fordító minden paraméterükhöz és a
visszatérési értékükhöz egy konkrét típust következtet ki. Például a 13-3. lista
egy rövid closure definícióját mutatja, amely egyszerűen visszaadja a
paraméterként kapott értéket. Ez a closure ezen a példán kívül nem túl hasznos.
Figyeld meg, hogy nem adtunk típusannotációkat a definícióhoz. Mivel nincsenek
típusannotációk, bármilyen típussal meghívhatjuk a closure-t, amit itt először
`String`-gel meg is tettünk. Ha ezután megpróbáljuk az `example_closure`-t egy
egésszel meghívni, hibát kapunk.

<Listing number="13-3" file-name="src/main.rs" caption="Kísérlet egy kikövetkeztetett típusú closure meghívására két különböző típussal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

A fordító ezt a hibát adja:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Amikor először hívjuk meg az `example_closure`-t a `String` értékkel, a fordító
`String`-nek következteti ki az `x` típusát és a closure visszatérési típusát.
Ezek a típusok ezután rögzülnek az `example_closure`-ben lévő closure-ben, és
típushibát kapunk, amikor legközelebb más típussal próbáljuk használni ugyanazt
a closure-t.

### Referenciák elkapása vagy az ownership átvétele {#capturing-references-or-moving-ownership}

A closure-ök háromféleképpen kaphatnak el értékeket a környezetükből, ami
közvetlenül megfeleltethető annak a háromféle módnak, ahogy egy függvény
paramétert vehet át: nem módosítható borrowing, módosítható borrowing és az
ownership átvétele. A closure aszerint dönti el, melyiket használja, hogy a
törzse mit csinál az elkapott értékekkel.

A 13-4. listában olyan closure-t definiálunk, amely nem módosítható
referenciát kap el a `list` nevű vektorra, mert az érték kiírásához csak nem
módosítható referenciára van szüksége.

<Listing number="13-4" file-name="src/main.rs" caption="Nem módosítható referenciát elkapó closure definiálása és meghívása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Ez a példa azt is szemlélteti, hogy egy változó closure-definícióhoz köthető, és
később a változónevet és zárójeleket használva meghívhatjuk a closure-t, mintha
a változónév egy függvénynév lenne.

Mivel egyszerre több nem módosítható referenciánk is lehet a `list`-re, a `list`
továbbra is elérhető a closure-definíció előtti kódból, a closure-definíció
után, de a closure meghívása előtt, valamint a closure meghívása után is. Ez a
kód lefordul, lefut, és a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Ezután a 13-5. listában úgy módosítjuk a closure törzsét, hogy egy elemet
adjon hozzá a `list` vektorhoz. A closure most már módosítható referenciát kap
el.

<Listing number="13-5" file-name="src/main.rs" caption="Módosítható referenciát elkapó closure definiálása és meghívása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Ez a kód lefordul, lefut, és a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Figyeld meg, hogy már nincs `println!` a `borrows_mutably` closure definíciója
és meghívása között: amikor a `borrows_mutably` definiálódik, módosítható
referenciát kap el a `list`-re. A closure meghívása után nem használjuk többé a
closure-t, így a módosítható borrow véget ér. A closure-definíció és a
closure-hívás között nem megengedett egy nem módosítható borrow a kiíráshoz,
mert amíg van egy módosítható borrow, addig semmilyen más borrow nem
megengedett. Próbálj meg odaírni egy `println!`-t, és nézd meg, milyen
hibaüzenetet kapsz!

Ha rá akarod kényszeríteni a closure-t, hogy vegye át a környezetben használt
értékek ownershipjét, még akkor is, ha a closure törzsének szigorúan véve nincs
szüksége az ownershipre, a `move` kulcsszót használhatod a paraméterlista előtt.

Ez a technika elsősorban akkor hasznos, amikor egy closure-t adunk át egy új
szálnak, hogy az adatokat átmozgassuk, és így az új szál birtokolja őket. A
szálakról és arról, miért érdemes használni őket, a 16. fejezetben, a
konkurencia tárgyalásakor lesz részletesen szó, de most nézzük meg röviden, hogyan
indíthatunk új szálat egy olyan closure-rel, amelynek szüksége van a `move`
kulcsszóra. A 13-6. lista a 13-4. listát mutatja úgy módosítva, hogy a vektort
egy új szálban írja ki, ne pedig a fő szálban.

<Listing number="13-6" file-name="src/main.rs" caption="A `move` használata arra, hogy a szálhoz tartozó closure átvegye a `list` ownershipjét">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Új szálat indítunk, és argumentumként átadunk a szálnak egy closure-t, amelyet
futtatnia kell. A closure törzse kiírja a listát. A 13-4. listában a closure
csak nem módosítható referenciával kapta el a `list`-et, mert a kiírásához ez a
legkisebb szükséges hozzáférés a `list`-hez. Ebben a példában, noha a closure
törzsének továbbra is csak nem módosítható referenciára van szüksége, meg kell
adnunk, hogy a `list`-et a closure-be kell mozgatni; ezt úgy tesszük, hogy a
closure-definíció elejére kitesszük a `move` kulcsszót. Ha a fő szál további
műveleteket végezne, mielőtt meghívná a `join`-t az új szálon, akkor az új szál
befejeződhetne a fő szál hátralévő részének befejeződése előtt, vagy a fő szál
fejeződhetne be előbb. Ha a fő szál megtartaná a `list` ownershipjét, de az új
szál előtt befejeződne, és eldobná a `list`-et, akkor a szálban lévő nem
módosítható referencia érvénytelen lenne. Ezért a fordító megköveteli, hogy a
`list`-et az új szálnak átadott closure-be mozgassuk, hogy a referencia
érvényes legyen. Próbáld meg eltávolítani a `move` kulcsszót, vagy használni a
`list`-et a fő szálban a closure definiálása után, és nézd meg, milyen fordítási
hibákat kapsz!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Elkapott értékek kimozgatása a closure-ökből {#moving-captured-values-out-of-closures}

Miután egy closure elkapott egy referenciát vagy átvette egy érték ownershipjét
abból a környezetből, ahol a closure definiálva van (ezzel meghatározva, hogy mi
– ha egyáltalán bármi – mozog _bele_ a closure-be), a closure törzsében lévő kód
határozza meg, mi történik ezekkel a referenciákkal vagy értékekkel, amikor a
closure később kiértékelődik (ezzel meghatározva, hogy mi – ha egyáltalán bármi
– mozog _ki_ a closure-ből).

Egy closure törzse a következők bármelyikét teheti: kimozgathat egy elkapott
értéket a closure-ből, módosíthatja az elkapott értéket, se nem mozgatja, se
nem módosítja az értéket, vagy eleve semmit nem kap el a környezetből.

Az, ahogyan egy closure elkapja és kezeli a környezetéből származó értékeket,
befolyásolja, mely trait-eket implementálja a closure, a trait-ek pedig azt a
módot jelentik, ahogyan a függvények és a structok megadhatják, milyen fajta
closure-öket tudnak használni. A closure-ök automatikusan implementálják ezen
`Fn` trait-ek közül az egyiket, kettőt vagy mindhármat, egymásra épülő módon,
attól függően, hogyan kezeli a closure törzse az értékeket:

* Az `FnOnce` azokra a closure-ökre vonatkozik, amelyeket egyszer lehet
  meghívni. Minden closure implementálja legalább ezt a trait-et, mert minden
  closure meghívható. Az a closure, amely elkapott értékeket mozgat ki a
  törzséből, csak az `FnOnce`-t implementálja, a többi `Fn` trait-et nem, mert
  csak egyszer hívható meg.
* Az `FnMut` azokra a closure-ökre vonatkozik, amelyek nem mozgatnak ki
  elkapott értékeket a törzsükből, de módosíthatják az elkapott értékeket.
  Ezek a closure-ök egynél többször is meghívhatók.
* Az `Fn` azokra a closure-ökre vonatkozik, amelyek nem mozgatnak ki elkapott
  értékeket a törzsükből és nem is módosítják az elkapott értékeket, valamint
  azokra, amelyek semmit nem kapnak el a környezetükből. Ezek a closure-ök
  egynél többször is meghívhatók anélkül, hogy módosítanák a környezetüket, ami
  fontos például akkor, amikor egy closure-t többször, konkurensen hívunk meg.

Nézzük meg az `Option<T>` `unwrap_or_else` metódusának definícióját, amelyet a
13-1. listában használtunk:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Emlékezz rá, hogy a `T` az a generikus típus, amely az `Option` `Some`
variánsában lévő érték típusát képviseli. Ez a `T` típus egyben az
`unwrap_or_else` függvény visszatérési típusa is: az a kód például, amely egy
`Option<String>`-en hívja meg az `unwrap_or_else`-t, `String`-et fog kapni.

Ezután figyeld meg, hogy az `unwrap_or_else` függvénynek van egy további
generikus típusparamétere, az `F`. Az `F` típus az `f` nevű paraméter típusa,
vagyis azé a closure-é, amelyet az `unwrap_or_else` hívásakor megadunk.

Az `F` generikus típusra megadott trait bound az `FnOnce() -> T`, ami azt
jelenti, hogy az `F`-nek egyszer meghívhatónak kell lennie, nem vehet át
argumentumot, és `T`-t kell visszaadnia. Az `FnOnce` használata a trait
boundban azt a megkötést fejezi ki, hogy az `unwrap_or_else` legfeljebb egyszer
hívja meg az `f`-et. Az `unwrap_or_else` törzsében látható, hogy ha az `Option`
`Some`, az `f` nem hívódik meg. Ha az `Option` `None`, az `f` egyszer hívódik
meg. Mivel minden closure implementálja az `FnOnce`-t, az `unwrap_or_else`
mindhárom fajta closure-t elfogadja, és a lehető legrugalmasabb.

> Megjegyzés: Ha az, amit tenni akarunk, nem igényli érték elkapását a
> környezetből, akkor closure helyett egy függvény nevét is használhatjuk ott,
> ahol valami olyasmire van szükségünk, ami implementálja valamelyik `Fn`
> trait-et. Például egy `Option<Vec<T>>` értéken meghívhatjuk az
> `unwrap_or_else(Vec::new)`-t, hogy új, üres vektort kapjunk, ha az érték
> `None`. A fordító egy függvénydefinícióhoz automatikusan implementálja azt az
> `Fn` trait-et, amelyik alkalmazható rá.

Most nézzük meg a standard könyvtár slice-okon definiált `sort_by_key`
metódusát, hogy lássuk, miben tér el az `unwrap_or_else`-től, és miért az
`FnMut`-ot használja a `sort_by_key` az `FnOnce` helyett a trait boundban. A
closure egyetlen argumentumot kap, egy referenciát a slice éppen vizsgált
aktuális elemére, és egy `K` típusú, rendezhető értéket ad vissza. Ez a függvény
akkor hasznos, ha egy slice-ot az elemek valamelyik attribútuma szerint akarsz
rendezni. A 13-7. listában van egy `Rectangle` példányokból álló listánk, és a
`sort_by_key`-t használjuk, hogy a `width` attribútumuk szerint, növekvő
sorrendbe rendezzük őket.

<Listing number="13-7" file-name="src/main.rs" caption="A `sort_by_key` használata a téglalapok szélesség szerinti rendezéséhez">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Ez a kód a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

A `sort_by_key` azért `FnMut` closure-t vár, mert többször hívja meg a
closure-t: egyszer a slice minden elemére. A `|r| r.width` closure semmit nem
kap el, nem módosít és nem mozgat ki a környezetéből, így megfelel a trait bound
követelményeinek.

Ezzel szemben a 13-8. lista egy olyan closure-re mutat példát, amely csak az
`FnOnce` trait-et implementálja, mert kimozgat egy értéket a környezetből. A
fordító nem engedi, hogy ezt a closure-t a `sort_by_key`-jel használjuk.

<Listing number="13-8" file-name="src/main.rs" caption="Kísérlet egy `FnOnce` closure használatára a `sort_by_key`-jel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Ez egy mesterkélt, körülményes (és nem működő) módja annak, hogy megpróbáljuk
megszámolni, hányszor hívja meg a `sort_by_key` a closure-t a `list` rendezése
közben. A kód úgy próbál számolni, hogy a `value`-t – egy `String`-et a closure
környezetéből – betolja a `sort_operations` vektorba. A closure elkapja a
`value`-t, majd kimozgatja a `value`-t a closure-ből azzal, hogy átadja a
`value` ownershipjét a `sort_operations` vektornak. Ez a closure egyszer hívható
meg; ha másodszor is meg akarnánk hívni, az nem működne, mert a `value` már nem
lenne a környezetben ahhoz, hogy újra betolhassuk a `sort_operations`-be! Ezért
ez a closure csak az `FnOnce`-t implementálja. Amikor megpróbáljuk lefordítani
ezt a kódot, ezt a hibát kapjuk, miszerint a `value` nem mozgatható ki a
closure-ből, mert a closure-nek implementálnia kell az `FnMut`-ot:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

A hiba a closure törzsének arra a sorára mutat, amely kimozgatja a `value`-t a
környezetből. Ennek javításához úgy kell megváltoztatnunk a closure törzsét,
hogy ne mozgasson ki értékeket a környezetből. Ha a környezetben tartunk egy
számlálót, és a closure törzsében növeljük az értékét, az sokkal egyszerűbb
módja annak, hogy megszámoljuk, hányszor hívódik meg a closure. A 13-9. listában
szereplő closure működik a `sort_by_key`-jel, mert csak egy módosítható
referenciát kap el a `num_sort_operations` számlálóra, és így egynél többször is
meghívható.

<Listing number="13-9" file-name="src/main.rs" caption="Az `FnMut` closure használata a `sort_by_key`-jel megengedett.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

Az `Fn` trait-ek fontosak, amikor closure-öket használó függvényeket vagy
típusokat definiálunk vagy használunk. A következő szakaszban az iterátorokról
lesz szó. Sok iterátormetódus vár closure-argumentumot, ezért tartsd észben
ezeket a closure-részleteket, ahogy továbbhaladunk!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else
