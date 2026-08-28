## Hogyan írjunk teszteket {#how-to-write-tests}

A _tesztek_ olyan Rust-függvények, amelyek ellenőrzik, hogy a nem teszt jellegű
kód az elvárt módon működik-e. A tesztfüggvények törzse jellemzően a következő
három műveletet végzi el:

- Előkészíti a szükséges adatokat vagy állapotot.
- Lefuttatja a tesztelni kívánt kódot.
- Állítást fogalmaz meg arról, hogy az eredmények megfelelnek az elvárásnak.

Nézzük meg, milyen eszközöket ad a Rust kifejezetten az ilyen műveleteket végző
tesztek írásához: ilyen a `test` attribútum, néhány makró és a `should_panic`
attribútum.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Tesztfüggvények felépítése

A legegyszerűbb esetben egy teszt a Rustban nem más, mint egy `test`
attribútummal ellátott függvény. Az attribútumok metaadatok a Rust-kód egyes
darabjairól; egy példa erre a `derive` attribútum, amelyet az 5. fejezetben
struct-okkal használtunk. Ahhoz, hogy egy függvényből tesztfüggvény legyen,
írd a `#[test]` sort az `fn` elé. Amikor a `cargo test` paranccsal futtatod a
tesztjeidet, a Rust felépít egy tesztfuttató binárist, amely lefuttatja az
annotált függvényeket, és jelenti, hogy az egyes tesztfüggvények sikeresek
vagy sikertelenek voltak-e.

Valahányszor új library projektet hozunk létre a Cargóval, automatikusan
generálódik egy teszt modul benne egy tesztfüggvénnyel. Ez a modul mintát ad a
tesztek írásához, így nem kell minden új projekt kezdetén utánanézned a pontos
szerkezetnek és szintaxisnak. Annyi további tesztfüggvényt és annyi teszt
modult adhatsz hozzá, amennyit csak akarsz!

A tesztek működésének néhány aspektusát a minta teszttel kísérletezve fogjuk
felfedezni, mielőtt bármilyen valódi kódot tesztelnénk. Utána írunk néhány
életszerű tesztet, amelyek az általunk írt kódot hívják meg, és állítást
fogalmaznak meg a helyes viselkedéséről.

Hozzunk létre egy új, `adder` nevű library projektet, amely két számot ad
össze:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Az `adder` library _src/lib.rs_ fájljának tartalma a 11-1. listához hasonlóan
néz ki.

<Listing number="11-1" file-name="src/lib.rs" caption="A `cargo new` által automatikusan generált kód">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

A fájl egy példa `add` függvénnyel kezdődik, hogy legyen mit tesztelnünk.

Egyelőre összpontosítsunk kizárólag az `it_works` függvényre. Figyeld meg a
`#[test]` annotációt: ez az attribútum jelzi, hogy ez egy tesztfüggvény, így a
tesztfuttató tudja, hogy tesztként kell kezelnie. A `tests` modulban lehetnek
nem teszt jellegű függvények is, amelyek gyakori helyzetek előkészítésében vagy
gyakori műveletek elvégzésében segítenek, ezért mindig jeleznünk kell, mely
függvények a tesztek.

A példafüggvény törzse az `assert_eq!` makrót használja annak állítására, hogy
a `result`, amely az `add` 2-vel és 2-vel való meghívásának eredményét
tartalmazza, egyenlő 4-gyel. Ez az állítás egy tipikus teszt formáját mutatja
be példaként. Futtassuk le, hogy lássuk: a teszt sikeres.

A `cargo test` parancs lefuttatja a projektünk összes tesztjét, ahogy a 11-2.
listán látható.

<Listing number="11-2" caption="Az automatikusan generált teszt futtatásának kimenete">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

A Cargo lefordította és lefuttatta a tesztet. Látjuk a `running 1 test` sort. A
következő sor a generált tesztfüggvény nevét mutatja, amely `tests::it_works`,
és azt, hogy a teszt futtatásának eredménye `ok`. Az összegző `test result:
ok.` azt jelenti, hogy minden teszt sikeres volt, a `1 passed; 0 failed` rész
pedig összesíti a sikeres, illetve sikertelen tesztek számát.

Egy tesztet meg lehet jelölni figyelmen kívül hagyottként, hogy adott esetben
ne fusson le; erről az [„Tesztek kihagyása, hacsak nem kérjük őket
kifejezetten”][ignoring]<!-- ignore --> szakaszban lesz szó a fejezet későbbi
részében. Mivel ezt itt nem tettük meg, az összegzés `0 ignored` értéket mutat.
A `cargo test` parancsnak argumentumot is átadhatunk, hogy csak azokat a
teszteket futtassa, amelyek neve illeszkedik egy adott karakterláncra; ezt
_szűrésnek_ nevezzük, és a [„Tesztek egy részhalmazának futtatása név
alapján”][subset]<!-- ignore --> szakaszban tárgyaljuk. Itt nem szűrtük a
lefuttatott teszteket, ezért az összegzés végén `0 filtered out` szerepel.

A `0 measured` statisztika a teljesítményt mérő benchmark tesztekre vonatkozik.
A benchmark tesztek e sorok írásakor csak a nightly Rustban érhetők el.
További információért lásd [a benchmark tesztekről szóló
dokumentációt][bench].

A teszt kimenetének következő része, amely a `Doc-tests adder` sorral kezdődik,
az esetleges dokumentációs tesztek eredményeit tartalmazza. Egyelőre nincsenek
dokumentációs tesztjeink, de a Rust le tudja fordítani az API-dokumentációnkban
megjelenő kódpéldákat. Ez a képesség segít szinkronban tartani a dokumentációt
és a kódot! A dokumentációs tesztek írásáról a 14. fejezet [„Dokumentációs
kommentek tesztként”][doc-comments]<!-- ignore --> szakaszában lesz szó.
Egyelőre figyelmen kívül hagyjuk a `Doc-tests` kimenetet.

Kezdjük el a tesztet a saját igényeinkhez igazítani. Először nevezd át az
`it_works` függvényt valami másra, például `exploration`-re, így:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Ezután futtasd újra a `cargo test` parancsot. A kimenet most már `it_works`
helyett `exploration`-t mutat:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Most hozzáadunk még egy tesztet, de ezúttal olyat, amely megbukik! A tesztek
akkor buknak meg, ha a tesztfüggvényben valami panicot vált ki. Minden teszt
külön szálon fut, és amikor a fő szál látja, hogy egy tesztszál elhalálozott, a
tesztet sikertelennek jelöli. A 9. fejezetben szó volt róla, hogy a panic
kiváltásának legegyszerűbb módja a `panic!` makró meghívása. Vidd be az új
tesztet `another` nevű függvényként, hogy a _src/lib.rs_ fájlod a 11-3. listához
hasonlóan nézzen ki.

<Listing number="11-3" file-name="src/lib.rs" caption="Egy második teszt hozzáadása, amely megbukik, mert meghívjuk a `panic!` makrót">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Futtasd le újra a teszteket a `cargo test` paranccsal. A kimenetnek a 11-4.
listához hasonlóan kell kinéznie, amely azt mutatja, hogy az `exploration`
tesztünk sikeres volt, az `another` pedig megbukott.

<Listing number="11-4" caption="Teszteredmények, amikor az egyik teszt sikeres, a másik megbukik">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Az `ok` helyett a `test tests::another` sorban `FAILED` áll. Két új szakasz
jelenik meg az egyes eredmények és az összegzés között: az első az egyes
tesztbukások részletes okát mutatja. Ebben az esetben azt a részletet kapjuk,
hogy a `tests::another` azért bukott meg, mert panicot váltott ki a `Make this
test fail` üzenettel a _src/lib.rs_ fájl 17. sorában. A következő szakasz csak
az összes megbukott teszt nevét sorolja fel, ami akkor hasznos, ha sok teszt
van és sok részletes bukási kimenet. Egy megbukott teszt nevét felhasználhatjuk
arra, hogy csak azt az egy tesztet futtassuk le, és könnyebben hibakeressünk;
a tesztek futtatásának módjairól bővebben a [„A tesztek futtatásának
szabályozása”][controlling-how-tests-are-run]<!-- ignore --> szakaszban lesz
szó.

Az összegző sor a végén jelenik meg: összességében a teszteredményünk `FAILED`.
Egy teszt sikeres volt, egy pedig megbukott.

Most, hogy láttad, hogyan néznek ki a teszteredmények különböző helyzetekben,
nézzünk meg néhány `panic!`-on kívüli makrót, amelyek hasznosak a tesztekben.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Eredmények ellenőrzése az `assert!` makróval

A standard könyvtár által biztosított `assert!` makró akkor hasznos, ha meg
akarsz bizonyosodni arról, hogy egy tesztben valamilyen feltétel `true`
értékűre értékelődik ki. Az `assert!` makrónak olyan argumentumot adunk, amely
logikai értékre értékelődik ki. Ha az érték `true`, semmi sem történik, és a
teszt sikeres. Ha az érték `false`, az `assert!` makró meghívja a `panic!`
makrót, amivel a teszt megbukik. Az `assert!` makró használata segít
ellenőrizni, hogy a kódunk a szándékunknak megfelelően működik-e.

Az 5. fejezet 5-15. listáján egy `Rectangle` struct-ot és egy `can_hold`
metódust használtunk, amelyeket itt megismétlünk a 11-5. listán. Tegyük ezt a
kódot a _src/lib.rs_ fájlba, majd írjunk hozzá néhány tesztet az `assert!`
makróval.

<Listing number="11-5" file-name="src/lib.rs" caption="A `Rectangle` struct és a `can_hold` metódusa az 5. fejezetből">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

A `can_hold` metódus logikai értéket ad vissza, ami azt jelenti, hogy tökéletes
felhasználási eset az `assert!` makró számára. A 11-6. listán olyan tesztet
írunk, amely úgy próbálja ki a `can_hold` metódust, hogy létrehoz egy 8
szélességű és 7 magasságú `Rectangle` példányt, és azt állítja, hogy ez képes
befogadni egy másik, 5 szélességű és 1 magasságú `Rectangle` példányt.

<Listing number="11-6" file-name="src/lib.rs" caption="Egy teszt a `can_hold`-hoz, amely azt ellenőrzi, hogy egy nagyobb téglalap valóban be tud-e fogadni egy kisebbet">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Figyeld meg a `use super::*;` sort a `tests` modulon belül. A `tests` modul
egy szokásos modul, amely a 7. fejezet [„Útvonalak elemekre való hivatkozáshoz
a modulfában”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->
szakaszában tárgyalt szokásos láthatósági szabályokat követi. Mivel a `tests`
modul belső modul, a külső modulban lévő, tesztelendő kódot be kell hoznunk a
belső modul hatókörébe. Itt glob-ot használunk, így minden, amit a külső
modulban definiálunk, elérhető ebben a `tests` modulban.

A tesztünket `larger_can_hold_smaller`-nek neveztük el, és létrehoztuk a két
szükséges `Rectangle` példányt. Ezután meghívtuk az `assert!` makrót, és átadtuk
neki a `larger.can_hold(&smaller)` hívás eredményét. Ennek a kifejezésnek
`true` értéket kell adnia, tehát a tesztünknek sikeresnek kell lennie.
Nézzük meg!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Valóban sikeres! Adjunk hozzá egy másik tesztet, ezúttal azt állítva, hogy egy
kisebb téglalap nem tud befogadni egy nagyobbat:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Mivel a `can_hold` függvény helyes eredménye ebben az esetben `false`, ezt az
eredményt negálnunk kell, mielőtt átadjuk az `assert!` makrónak. Ennek
eredményeként a tesztünk akkor lesz sikeres, ha a `can_hold` `false` értéket ad
vissza:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Két sikeres teszt! Most nézzük meg, mi történik a teszteredményeinkkel, ha hibát
viszünk a kódunkba. Módosítjuk a `can_hold` metódus implementációját úgy, hogy a
nagyobb-mint jelet (`>`) kisebb-mint jelre (`<`) cseréljük a szélességek
összehasonlításakor:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

A tesztek futtatása most a következőt eredményezi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

A tesztjeink elkapták a hibát! Mivel a `larger.width` értéke `8`, a
`smaller.width` értéke pedig `5`, a szélességek összehasonlítása a `can_hold`
metódusban most `false` értéket ad: a 8 nem kisebb, mint az 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Egyenlőség tesztelése az `assert_eq!` és `assert_ne!` makróval

A működés ellenőrzésének gyakori módja, hogy egyenlőséget tesztelünk a
tesztelendő kód eredménye és a kódtól várt érték között. Ezt megtehetnéd úgy is,
hogy az `assert!` makrót használod, és egy `==` operátort tartalmazó kifejezést
adsz át neki. Ez azonban olyan gyakori teszt, hogy a standard könyvtár egy
makrópárt – az `assert_eq!` és `assert_ne!` makrót – biztosít ennek a tesztnek a
kényelmesebb elvégzésére. Ezek a makrók két argumentumot hasonlítanak össze
egyenlőség, illetve egyenlőtlenség szempontjából. Ráadásul ki is írják a két
értéket, ha az állítás nem teljesül, ami megkönnyíti annak megállapítását, hogy
_miért_ bukott meg a teszt; ezzel szemben az `assert!` makró csak azt jelzi,
hogy `false` értéket kapott az `==` kifejezésre, anélkül hogy kiírná azokat az
értékeket, amelyek a `false` értékhez vezettek.

A 11-7. listán írunk egy `add_two` nevű függvényt, amely `2`-t ad a
paraméteréhez, majd az `assert_eq!` makróval teszteljük ezt a függvényt.

<Listing number="11-7" file-name="src/lib.rs" caption="Az `add_two` függvény tesztelése az `assert_eq!` makróval">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Ellenőrizzük, hogy sikeres-e!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Létrehozunk egy `result` nevű változót, amely az `add_two(2)` hívás eredményét
tartalmazza. Ezután a `result` és a `4` értéket adjuk át argumentumként az
`assert_eq!` makrónak. Ennek a tesztnek a kimeneti sora `test tests::it_adds_two
... ok`, és az `ok` szöveg jelzi, hogy a tesztünk sikeres volt!

Vigyünk hibát a kódunkba, hogy lássuk, hogyan néz ki az `assert_eq!`, amikor
megbukik. Módosítsd az `add_two` függvény implementációját úgy, hogy `3`-at
adjon hozzá:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Futtasd le újra a teszteket:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

A tesztünk elkapta a hibát! A `tests::it_adds_two` teszt megbukott, és az
üzenet elárulja, hogy a `left == right` állítás nem teljesült, valamint azt is,
mi a `left` és a `right` értéke. Ez az üzenet segít elindulni a hibakeresésben:
a `left` argumentum, ahol az `add_two(2)` hívás eredménye volt, `5` lett, a
`right` argumentum viszont `4`. Elképzelheted, hogy ez különösen hasznos, amikor
sok tesztünk fut egyszerre.

Vedd figyelembe, hogy egyes nyelvekben és tesztelési keretrendszerekben az
egyenlőséget vizsgáló állításfüggvények paramétereit `expected` és `actual`
néven hívják, és számít, milyen sorrendben adjuk meg az argumentumokat. A
Rustban azonban `left` és `right` a nevük, és nem számít, milyen sorrendben
adjuk meg az elvárt értéket és a kód által előállított értéket. Ebben a
tesztben az állítást `assert_eq!(4, result)` alakban is írhattuk volna, ami
ugyanazt a bukási üzenetet eredményezte volna, amely az
`` assertion `left == right` failed `` szöveget jeleníti meg.

Az `assert_ne!` makró akkor sikeres, ha a két megadott érték nem egyenlő, és
akkor bukik meg, ha egyenlők. Ez a makró leginkább azokban az esetekben
hasznos, amikor nem tudjuk biztosan, mi _lesz_ egy érték, de tudjuk, minek
biztosan _nem_ szabad lennie. Ha például egy olyan függvényt tesztelünk,
amelyről garantált, hogy valamilyen módon megváltoztatja a bemenetét, de a
változtatás módja attól függ, a hét melyik napján futtatjuk a tesztjeinket,
akkor a legjobb, amit állíthatunk, az lehet, hogy a függvény kimenete nem
egyenlő a bemenetével.

A felszín alatt az `assert_eq!` és `assert_ne!` makró a `==`, illetve a `!=`
operátort használja. Amikor az állítások nem teljesülnek, ezek a makrók debug
formázással írják ki az argumentumaikat, ami azt jelenti, hogy az
összehasonlított értékeknek implementálniuk kell a `PartialEq` és `Debug`
trait-et. Minden primitív típus és a standard könyvtár típusainak nagy része
implementálja ezeket a trait-eket. Az általad definiált struct-oknál és
enumoknál implementálnod kell a `PartialEq`-et, hogy egyenlőséget állíthass
ezekre a típusokra. A `Debug`-ot is implementálnod kell, hogy az értékek
kiíródjanak, amikor az állítás nem teljesül. Mivel mindkét trait
származtatható, ahogy az 5. fejezet 5-12. listájánál említettük, ez általában
annyira egyszerű, mint hozzáadni a `#[derive(PartialEq, Debug)]` annotációt a
struct- vagy enum-definíciódhoz. További részletekért ezekről és más
származtatható trait-ekről lásd a C függeléket, [„Származtatható
trait-ek”][derivable-traits]<!-- ignore -->.

### Egyedi hibaüzenetek hozzáadása

Az `assert!`, `assert_eq!` és `assert_ne!` makróknak opcionális argumentumként
egyedi üzenetet is átadhatsz, amely a bukási üzenettel együtt kiíródik. A
kötelező argumentumok után megadott bármely argumentum továbbadódik a `format!`
makrónak (amelyről a 8. fejezet [„Összefűzés a `+` operátorral vagy a `format!`
makróval”][concatenating]<!--
ignore --> szakaszában volt szó), így átadhatsz egy `{}` helyőrzőket tartalmazó
formázósztringet és a helyőrzőkbe kerülő értékeket. Az egyedi üzenetek
hasznosak annak dokumentálására, hogy egy állítás mit jelent; amikor egy teszt
megbukik, jobban átlátod, mi a baj a kóddal.

Tegyük fel például, hogy van egy függvényünk, amely név szerint köszönti az
embereket, és tesztelni akarjuk, hogy a függvénynek átadott név megjelenik-e a
kimenetben:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Ennek a programnak a követelményeiről még nem született megállapodás, és eléggé
biztosak vagyunk benne, hogy a köszöntés elején álló `Hello` szöveg meg fog
változni. Úgy döntöttünk, hogy nem akarjuk frissíteni a tesztet, valahányszor a
követelmények változnak, ezért ahelyett, hogy a `greeting` függvény által
visszaadott értékkel való pontos egyezést ellenőriznénk, csak azt állítjuk,
hogy a kimenet tartalmazza a bemeneti paraméter szövegét.

Most vigyünk hibát ebbe a kódba úgy, hogy a `greeting` függvényből kihagyjuk a
`name`-et, és nézzük meg, hogyan néz ki az alapértelmezett tesztbukás:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Ennek a tesztnek a futtatása a következőt eredményezi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Ez az eredmény csak azt jelzi, hogy az állítás nem teljesült, és azt, hogy
melyik sorban van az állítás. Egy hasznosabb bukási üzenet kiírná a `greeting`
függvénytől kapott értéket. Adjunk hozzá egy egyedi bukási üzenetet, amely egy
formázósztringből áll, benne egy helyőrzővel, amelyet a `greeting` függvénytől
ténylegesen kapott érték tölt ki:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Most, amikor lefuttatjuk a tesztet, informatívabb hibaüzenetet kapunk:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

A teszt kimenetében látjuk a ténylegesen kapott értéket, ami segít
felderíteni, mi történt ahelyett, aminek történnie kellett volna.

### Panicok ellenőrzése a `should_panic` attribútummal

A visszatérési értékek ellenőrzésén túl fontos ellenőrizni azt is, hogy a
kódunk az elvárásainknak megfelelően kezeli-e a hibahelyzeteket. Vegyük például
a `Guess` típust, amelyet a 9. fejezet 9-13. listáján hoztunk létre. A `Guess`-t
használó többi kód arra a garanciára támaszkodik, hogy a `Guess` példányok csak
1 és 100 közötti értékeket tartalmaznak. Írhatunk olyan tesztet, amely
biztosítja, hogy egy ezen a tartományon kívüli értékkel létrehozott `Guess`
példány létrehozásának kísérlete panicot vált ki.

Ezt úgy tesszük meg, hogy hozzáadjuk a `should_panic` attribútumot a
tesztfüggvényünkhöz. A teszt akkor sikeres, ha a függvényen belüli kód panicot
vált ki; a teszt megbukik, ha a függvényen belüli kód nem vált ki panicot.

A 11-8. lista olyan tesztet mutat, amely azt ellenőrzi, hogy a `Guess::new`
hibahelyzetei akkor következnek-e be, amikor várjuk őket.

<Listing number="11-8" file-name="src/lib.rs" caption="Annak tesztelése, hogy egy feltétel `panic!`-ot okoz">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

A `#[should_panic]` attribútumot a `#[test]` attribútum után és az általa
érintett tesztfüggvény elé helyezzük. Nézzük meg az eredményt, amikor ez a
teszt sikeres:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Jól néz ki! Most vigyünk hibát a kódunkba úgy, hogy eltávolítjuk azt a
feltételt, amely miatt a `new` függvény panicot vált ki, ha az érték nagyobb,
mint 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Amikor lefuttatjuk a 11-8. lista tesztjét, meg fog bukni:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Ebben az esetben nem kapunk túl sok segítséget az üzenetből, de ha megnézzük a
tesztfüggvényt, látjuk, hogy `#[should_panic]` annotációval van ellátva. A
kapott bukás azt jelenti, hogy a tesztfüggvényben lévő kód nem okozott panicot.

A `should_panic` attribútumot használó tesztek pontatlanok lehetnek. Egy
`should_panic` teszt akkor is sikeres lenne, ha a teszt a vártól eltérő okból
váltana ki panicot. Ahhoz, hogy a `should_panic` teszteket pontosabbá tegyük,
hozzáadhatunk egy opcionális `expected` paramétert a `should_panic`
attribútumhoz. A tesztkeretrendszer megbizonyosodik róla, hogy a bukási üzenet
tartalmazza a megadott szöveget. Vegyük például a `Guess` módosított kódját a
11-9. listán, ahol a `new` függvény attól függően más-más üzenettel vált ki
panicot, hogy az érték túl kicsi vagy túl nagy.

<Listing number="11-9" file-name="src/lib.rs" caption="Egy `panic!` tesztelése olyan panicüzenettel, amely egy megadott részsztringet tartalmaz">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Ez a teszt sikeres lesz, mert a `should_panic` attribútum `expected`
paraméterébe írt érték részsztringje annak az üzenetnek, amellyel a
`Guess::new` függvény panicot vált ki. Megadhattuk volna a teljes elvárt
panicüzenetet is, ami ebben az esetben `Guess value must be less than or equal
to 100, got 200` lenne. Az, hogy mit adsz meg, attól függ, mennyire egyedi vagy
dinamikus a panicüzenet, és mennyire szeretnéd pontossá tenni a tesztedet.
Ebben az esetben a panicüzenet egy részsztringje is elegendő annak
biztosítására, hogy a tesztfüggvényben lévő kód az `else if value > 100` ágat
futtassa le.

Hogy lássuk, mi történik, amikor egy `expected` üzenettel ellátott
`should_panic` teszt megbukik, vigyünk ismét hibát a kódunkba úgy, hogy
felcseréljük az `if value < 1` és az `else if value > 100` blokkok törzsét:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Ezúttal, amikor lefuttatjuk a `should_panic` tesztet, meg fog bukni:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

A bukási üzenet jelzi, hogy ez a teszt valóban kiváltott panicot, ahogy vártuk,
de a panicüzenet nem tartalmazta az elvárt `less than or equal to 100`
sztringet. A ténylegesen kapott panicüzenet ebben az esetben `Guess value must
be greater than or equal to 1, got 200` volt. Most már elkezdhetjük kideríteni,
hol van a hibánk!

### `Result<T, E>` használata a tesztekben

Az eddigi tesztjeink mind panicot váltanak ki, amikor megbuknak. Írhatunk
olyan teszteket is, amelyek a `Result<T, E>` típust használják! Íme a 11-1.
lista tesztje átírva úgy, hogy `Result<T, E>` típust használjon, és panic
helyett `Err` értéket adjon vissza:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Az `it_works` függvény visszatérési típusa most `Result<(), String>`. A
függvény törzsében az `assert_eq!` makró meghívása helyett `Ok(())` értéket
adunk vissza, ha a teszt sikeres, és egy `String`-et tartalmazó `Err` értéket,
ha a teszt megbukik.

Ha úgy írod meg a teszteket, hogy `Result<T, E>` értéket adjanak vissza, akkor
használhatod a kérdőjel operátort a tesztek törzsében, ami kényelmes módja
lehet olyan tesztek írásának, amelyeknek meg kell bukniuk, ha bármely bennük
lévő művelet `Err` variánst ad vissza.

A `#[should_panic]` annotációt nem használhatod olyan teszteken, amelyek
`Result<T, E>` típust használnak. Ahhoz, hogy azt állítsd, egy művelet `Err`
variánst ad vissza, _ne_ használd a kérdőjel operátort a `Result<T, E>`
értéken. Ehelyett használd az `assert!(value.is_err())` alakot.

Most, hogy már többféle módot ismersz a tesztek írására, nézzük meg, mi
történik a tesztjeink futtatásakor, és fedezzük fel a `cargo test` parancshoz
használható különböző opciókat.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
