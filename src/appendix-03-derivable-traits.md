## C függelék: Származtatható trait-ek

A könyv több pontján is szó volt a `derive` attribútumról, amelyet egy struct-
vagy enum-definícióra alkalmazhatsz. A `derive` attribútum olyan kódot generál,
amely a saját alapértelmezett implementációjával implementál egy trait-et azon a
típuson, amelyet a `derive` szintaxissal annotáltál.

Ebben a függelékben azoknak a standard könyvtárbeli trait-eknek a referenciáját
adjuk meg, amelyeket a `derive`-val használhatsz. Minden szakasz kitér a
következőkre:

- Milyen operátorokat és metódusokat tesz elérhetővé a trait származtatása
- Mit csinál a trait `derive` által biztosított implementációja
- Mit jelent a típusra nézve a trait implementálása
- Milyen feltételek mellett szabad, illetve nem szabad implementálnod a trait-et
- Példák olyan műveletekre, amelyekhez szükség van a trait-re

Ha a `derive` attribútum által biztosítottól eltérő viselkedést szeretnél, nézd
meg az egyes trait-ek [standard könyvtárbeli dokumentációját](../std/index.html)<!-- ignore -->,
ahol a kézi implementálásuk részleteit is megtalálod.

Az itt felsorolt trait-ek az egyetlenek a standard könyvtárban definiáltak
közül, amelyeket `derive` segítségével implementálhatsz a saját típusaidon. A
standard könyvtárban definiált többi trait-nek nincs ésszerű alapértelmezett
viselkedése, így rajtad múlik, hogy úgy implementáld őket, ahogy az a céljaid
szempontjából értelmes.

Egy példa olyan trait-re, amelyet nem lehet származtatni, a `Display`, amely a
végfelhasználók számára történő formázást intézi. Mindig gondold át, hogyan
helyes egy típust megjeleníteni a végfelhasználónak. Mely részeit láthatja a
típusnak a végfelhasználó? Mely részeket találná relevánsnak? Az adat melyik
formátuma lenne számára a legrelevánsabb? A Rust fordítónak nincs meg ez a
rálátása, így nem tud helyetted megfelelő alapértelmezett viselkedést nyújtani.

A függelékben felsorolt származtatható trait-ek listája nem teljes körű: a
könyvtárak a saját trait-jeikhez is implementálhatják a `derive`-ot, így azoknak
a trait-eknek a listája, amelyekkel a `derive`-ot használhatod, valójában nyitott.
A `derive` implementálásához procedurális makróra van szükség, amelyről a 20.
fejezet [„Egyedi `derive` makrók”][custom-derive-macros]<!-- ignore --> című
szakaszában esik szó.

### `Debug` a programozói kimenethez

A `Debug` trait teszi lehetővé a debug formázást a formátumsztringekben, amit a
`{}` helyőrzőkön belüli `:?` hozzáadásával jelzel.

A `Debug` trait lehetővé teszi, hogy hibakeresési céllal kiírd egy típus
példányait, így te és a típusodat használó más programozók megvizsgálhattok egy
példányt a program végrehajtásának adott pontján.

A `Debug` trait szükséges például az `assert_eq!` makró használatához. Ez a makró
kiírja az argumentumként megadott példányok értékeit, ha az egyenlőségi állítás
nem teljesül, hogy a programozók láthassák, miért nem volt egyenlő a két
példány.

### `PartialEq` és `Eq` az egyenlőség-összehasonlításokhoz

A `PartialEq` trait lehetővé teszi, hogy egy típus példányait egyenlőségre
vizsgálva összehasonlítsd, és elérhetővé teszi a `==` és a `!=` operátor
használatát.

A `PartialEq` származtatása az `eq` metódust implementálja. Amikor a `PartialEq`-t
struct-okon származtatjuk, két példány csak akkor egyenlő, ha _minden_ mező
egyenlő, és nem egyenlők, ha _bármelyik_ mező nem egyenlő. Enumokon
származtatva minden variáns egyenlő önmagával, és nem egyenlő a többi
variánssal.

A `PartialEq` trait szükséges például az `assert_eq!` makró használatához,
amelynek képesnek kell lennie egy típus két példányát egyenlőségre
összehasonlítani.

Az `Eq` trait-nek nincsenek metódusai. Az a célja, hogy jelezze: az annotált
típus minden értéke egyenlő önmagával. Az `Eq` trait csak olyan típusokra
alkalmazható, amelyek a `PartialEq`-t is implementálják, bár nem minden
`PartialEq`-t implementáló típus tudja implementálni az `Eq`-t. Erre példa a
lebegőpontos számtípusok esete: a lebegőpontos számok implementációja kimondja,
hogy a nem szám (`NaN`) érték két példánya nem egyenlő egymással.

Az `Eq`-ra például akkor van szükség, amikor egy `HashMap<K, V>` kulcsairól van
szó, hogy a `HashMap<K, V>` meg tudja mondani, két kulcs azonos-e.

### `PartialOrd` és `Ord` a rendezési összehasonlításokhoz

A `PartialOrd` trait lehetővé teszi, hogy egy típus példányait rendezési céllal
hasonlítsd össze. A `PartialOrd`-ot implementáló típus használható a `<`, a `>`,
a `<=` és a `>=` operátorral. A `PartialOrd` trait-et csak olyan típusokra
alkalmazhatod, amelyek a `PartialEq`-t is implementálják.

A `PartialOrd` származtatása a `partial_cmp` metódust implementálja, amely egy
`Option<Ordering>`-et ad vissza; ez `None` lesz, ha a megadott értékek nem
állíthatók sorrendbe. Példa olyan értékre, amely nem eredményez rendezést, noha
az adott típus legtöbb értéke összehasonlítható: a `NaN` lebegőpontos érték. A
`partial_cmp` hívása bármely lebegőpontos számmal és a `NaN` lebegőpontos
értékkel `None`-t ad vissza.

Struct-okon származtatva a `PartialOrd` úgy hasonlít össze két példányt, hogy az
egyes mezők értékeit abban a sorrendben veti össze, ahogy a mezők a
struct-definícióban szerepelnek. Enumokon származtatva az enum-definícióban
korábban deklarált variánsok kisebbnek számítanak a később felsoroltaknál.

A `PartialOrd` trait szükséges például a `rand` crate `gen_range` metódusához,
amely egy tartománykifejezéssel megadott tartományban generál véletlen értéket.

Az `Ord` trait révén tudhatod, hogy az annotált típus bármely két értéke között
létezik érvényes rendezés. Az `Ord` trait a `cmp` metódust implementálja, amely
`Option<Ordering>` helyett `Ordering`-et ad vissza, mert érvényes rendezés
mindig lehetséges. Az `Ord` trait-et csak olyan típusokra alkalmazhatod, amelyek
a `PartialOrd`-ot és az `Eq`-t is implementálják (az `Eq` pedig megköveteli a
`PartialEq`-t). Struct-okon és enumokon származtatva a `cmp` ugyanúgy viselkedik,
ahogy a `partial_cmp` származtatott implementációja a `PartialOrd` esetén.

Az `Ord`-ra például akkor van szükség, amikor értékeket tárolunk egy
`BTreeSet<T>`-ben, egy olyan adatszerkezetben, amely az értékek rendezési
sorrendje alapján tárolja az adatokat.

### `Clone` és `Copy` az értékek duplikálásához

A `Clone` trait lehetővé teszi, hogy explicit módon mélymásolatot készíts egy
értékről, és a duplikálási folyamat tetszőleges kód futtatásával, valamint a
heapen lévő adatok másolásával járhat. A `Clone`-ról bővebben a 4. fejezet
[„Változók és adatok kölcsönhatása:
clone”][variables-and-data-interacting-with-clone]<!-- ignore --> című
szakaszában olvashatsz.

A `Clone` származtatása a `clone` metódust implementálja, amely – ha a teljes
típusra van implementálva – meghívja a `clone`-t a típus minden részére. Ez azt
jelenti, hogy a `Clone` származtatásához a típus minden mezőjének vagy értékének
implementálnia kell a `Clone`-t.

A `Clone`-ra például akkor van szükség, amikor egy slice-on meghívjuk a `to_vec`
metódust. A slice nem birtokolja az általa tartalmazott típuspéldányokat, de a
`to_vec` által visszaadott vektornak birtokolnia kell a saját példányait, ezért
a `to_vec` minden elemen meghívja a `clone`-t. Így a slice-ban tárolt típusnak
implementálnia kell a `Clone`-t.

A `Copy` trait lehetővé teszi, hogy egy értéket pusztán a stacken tárolt bitek
másolásával duplikálj; nincs szükség tetszőleges kódra. A `Copy`-ról bővebben a
4. fejezet [„Csak a stack-en lévő adat: `Copy`”][stack-only-data-copy]<!-- ignore -->
című szakaszában olvashatsz.

A `Copy` trait nem definiál metódusokat, hogy a programozók ne tudják
túlterhelni azokat, és ezzel megsérteni azt a feltevést, hogy nem fut
tetszőleges kód. Így minden programozó feltételezheti, hogy egy érték másolása
nagyon gyors lesz.

A `Copy`-t bármely olyan típuson származtathatod, amelynek minden része
implementálja a `Copy`-t. Egy `Copy`-t implementáló típusnak a `Clone`-t is
implementálnia kell, mert egy `Copy`-t implementáló típusnak triviális `Clone`
implementációja van, amely ugyanazt a feladatot végzi, mint a `Copy`.

A `Copy` trait-re ritkán van szükség; a `Copy`-t implementáló típusokhoz
optimalizációk állnak rendelkezésre, vagyis nem kell meghívnod a `clone`-t, ami
tömörebbé teszi a kódot.

Mindent, ami a `Copy`-val lehetséges, a `Clone`-nal is elérhetsz, de a kód
lassabb lehet, vagy helyenként a `clone`-t kell használnia.

### `Hash` egy érték fix méretű értékké képezéséhez

A `Hash` trait lehetővé teszi, hogy egy tetszőleges méretű típus egy példányát
egy hash függvény segítségével fix méretű értékké képezd le. A `Hash`
származtatása a `hash` metódust implementálja. A `hash` metódus származtatott
implementációja egyesíti a típus egyes részein meghívott `hash` eredményét, ami
azt jelenti, hogy a `Hash` származtatásához minden mezőnek vagy értéknek
implementálnia kell a `Hash`-t.

A `Hash`-re például akkor van szükség, amikor kulcsokat tárolunk egy
`HashMap<K, V>`-ben az adatok hatékony tárolása érdekében.

### `Default` az alapértelmezett értékekhez

A `Default` trait lehetővé teszi, hogy alapértelmezett értéket hozz létre egy
típushoz. A `Default` származtatása a `default` függvényt implementálja. A
`default` függvény származtatott implementációja meghívja a `default` függvényt a
típus minden részén, ami azt jelenti, hogy a `Default` származtatásához a típus
minden mezőjének vagy értékének implementálnia kell a `Default`-ot.

A `Default::default` függvényt gyakran a struct-frissítő szintaxissal együtt
használják, amelyről az 5. fejezet [„Példányok létrehozása struct-frissítő
szintaxissal”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> című szakaszában volt szó. Egy struct néhány mezőjét testre szabhatod,
a többi mezőhöz pedig a `..Default::default()` használatával alapértelmezett
értéket állíthatsz be és használhatsz.

A `Default` trait-re például akkor van szükség, amikor az `unwrap_or_default`
metódust használod `Option<T>` példányokon. Ha az `Option<T>` értéke `None`, az
`unwrap_or_default` metódus az `Option<T>`-ben tárolt `T` típushoz tartozó
`Default::default` eredményét adja vissza.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
