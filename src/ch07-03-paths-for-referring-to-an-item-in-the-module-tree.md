## Útvonalak a modulfa elemeire való hivatkozáshoz

Ahhoz, hogy megmutassuk a Rustnak, hol találja meg egy elemet a modulfában,
útvonalat használunk, ugyanúgy, ahogy egy fájlrendszerben való navigáláskor is
útvonalat használunk. Egy függvény hívásához ismernünk kell az útvonalát.

Egy útvonal kétféle alakot ölthet:

- Az _abszolút útvonal_ a teljes útvonal, amely egy crate gyökeréből indul;
  külső crate-ből származó kód esetén az abszolút útvonal a crate nevével
  kezdődik, az aktuális crate kódja esetén pedig a szó szerinti `crate`
  kulcsszóval.
- A _relatív útvonal_ az aktuális modulból indul, és a `self`, a `super` vagy
  egy, az aktuális modulban lévő azonosító áll az elején.

Az abszolút és a relatív útvonalakat egyaránt kettős kettősponttal (`::`)
elválasztott azonosítók követik.

Térjünk vissza a 7-1. listához, és tegyük fel, hogy meg akarjuk hívni az
`add_to_waitlist` függvényt. Ez ugyanaz a kérdés, mint hogy: mi az
`add_to_waitlist` függvény útvonala? A 7-3. lista a 7-1. listát tartalmazza,
néhány modult és függvényt elhagyva belőle.

Két módot mutatunk be arra, hogyan hívható meg az `add_to_waitlist` függvény egy
új, a crate gyökerében definiált `eat_at_restaurant` függvényből. Ezek az
útvonalak helyesek, de van még egy másik probléma, amely megakadályozza, hogy ez
a példa így, ahogy van, lefordulhasson. Kicsit később elmagyarázzuk, miért.

Az `eat_at_restaurant` függvény a library crate-ünk nyilvános API-jának része,
ezért a `pub` kulcsszóval jelöljük meg. A [„Útvonalak közzététele a `pub`
kulcsszóval”][pub]<!-- ignore --> című szakaszban részletesebben is szó lesz a
`pub`-ról.

<Listing number="7-3" file-name="src/lib.rs" caption="Az `add_to_waitlist` függvény hívása abszolút és relatív útvonallal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Amikor először hívjuk meg az `add_to_waitlist` függvényt az
`eat_at_restaurant`-ban, abszolút útvonalat használunk. Az `add_to_waitlist`
függvény ugyanabban a crate-ben van definiálva, mint az `eat_at_restaurant`, ami
azt jelenti, hogy az abszolút útvonalat a `crate` kulcsszóval kezdhetjük. Ezután
felsoroljuk az egymást követő modulokat, amíg el nem jutunk az
`add_to_waitlist`-ig. Képzelj el egy ugyanilyen szerkezetű fájlrendszert: az
`add_to_waitlist` program futtatásához a
`/front_of_house/hosting/add_to_waitlist` útvonalat adnánk meg; a `crate` névvel
a crate gyökeréből indulni olyan, mint a shellben `/`-rel a fájlrendszer
gyökeréből indulni.

Amikor másodszor hívjuk meg az `add_to_waitlist` függvényt az
`eat_at_restaurant`-ban, relatív útvonalat használunk. Az útvonal a
`front_of_house`-zal kezdődik, annak a modulnak a nevével, amely a modulfa
ugyanazon szintjén van definiálva, mint az `eat_at_restaurant`. A fájlrendszeres
megfelelője itt a `front_of_house/hosting/add_to_waitlist` útvonal használata
lenne. Ha az útvonal egy modul nevével kezdődik, az azt jelenti, hogy relatív.

Az, hogy relatív vagy abszolút útvonalat használsz-e, olyan döntés, amelyet a
projekted alapján hozol meg, és attól függ, hogy valószínűbb-e, hogy az elemet
definiáló kódot az elemet használó kódtól külön vagy azzal együtt mozgatod. Ha
például a `front_of_house` modult és az `eat_at_restaurant` függvényt egy
`customer_experience` nevű modulba mozgatnánk, frissítenünk kellene az
`add_to_waitlist`-hez vezető abszolút útvonalat, a relatív útvonal viszont
továbbra is érvényes maradna. Ha viszont csak az `eat_at_restaurant` függvényt
mozgatnánk külön egy `dining` nevű modulba, az `add_to_waitlist` hívásához
vezető abszolút útvonal változatlan maradna, a relatív útvonalat viszont
frissíteni kellene. Általában az abszolút útvonalak megadását részesítjük
előnyben, mert valószínűbb, hogy a kóddefiníciókat és az elemek hívásait
egymástól függetlenül akarjuk mozgatni.

Próbáljuk meg lefordítani a 7-3. listát, és derítsük ki, miért nem fordul le
egyelőre! A kapott hibákat a 7-4. lista mutatja.

<Listing number="7-4" caption="A 7-3. listában szereplő kód fordításakor kapott fordítói hibák">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

A hibaüzenetek azt mondják, hogy a `hosting` modul privát. Más szóval a
`hosting` modulhoz és az `add_to_waitlist` függvényhez vezető útvonalaink
helyesek, de a Rust nem engedi őket használni, mert nincs hozzáférése a privát
részekhez. A Rustban minden elem (függvény, metódus, struct, enum, modul és
konstans) alapértelmezés szerint privát a szülőmodulok felé. Ha egy elemet,
például egy függvényt vagy egy structot priváttá akarsz tenni, tedd egy modulba.

Egy szülőmodul elemei nem használhatják a gyermekmodulokon belüli privát
elemeket, a gyermekmodulok elemei viszont használhatják az őseik moduljaiban
lévő elemeket. Ez azért van, mert a gyermekmodulok becsomagolják és elrejtik az
implementációs részleteiket, a gyermekmodulok viszont látják azt a környezetet,
amelyben definiálva vannak. Hogy folytassuk a hasonlatunkat: gondolj a
privátsági szabályokra úgy, mint egy étterem hátsó irodájára: ami ott bent
történik, az az étterem vendégei elől el van zárva, az irodavezetők viszont
mindent látnak és mindent megtehetnek abban az étteremben, amelyet üzemeltetnek.

A Rust azért választotta ezt a működést a modulrendszer számára, hogy a belső
implementációs részletek elrejtése legyen az alapértelmezés. Így tudod, a belső
kód mely részeit változtathatod meg anélkül, hogy a külső kód elromlana. A Rust
azonban lehetőséget ad arra, hogy a gyermekmodulok kódjának belső részeit a
külső ősmodulok számára is elérhetővé tedd: ehhez a `pub` kulcsszóval kell
nyilvánossá tenned az adott elemet.

### Útvonalak közzététele a `pub` kulcsszóval {#exposing-paths-with-the-pub-keyword}

Térjünk vissza a 7-4. listában látott hibához, amely azt mondta, hogy a
`hosting` modul privát. Azt szeretnénk, hogy a szülőmodulban lévő
`eat_at_restaurant` függvény hozzáférjen a gyermekmodulban lévő
`add_to_waitlist` függvényhez, ezért a `hosting` modult a `pub` kulcsszóval
jelöljük meg, ahogy a 7-5. lista mutatja.

<Listing number="7-5" file-name="src/lib.rs" caption="A `hosting` modul `pub`-ként való deklarálása, hogy használhassuk az `eat_at_restaurant`-ból">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Sajnos a 7-5. listában szereplő kód továbbra is fordítási hibákat eredményez,
ahogy azt a 7-6. lista mutatja.

<Listing number="7-6" caption="A 7-5. listában szereplő kód fordításakor kapott fordítói hibák">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Mi történt? A `pub` kulcsszó hozzáadása a `mod hosting` elé nyilvánossá teszi a
modult. Ezzel a változtatással, ha hozzáférünk a `front_of_house`-hoz, akkor
hozzáférünk a `hosting`-hoz is. A `hosting` _tartalma_ azonban továbbra is
privát: attól, hogy a modult nyilvánossá tesszük, még nem lesz nyilvános a
tartalma. Egy modulon a `pub` kulcsszó csak azt engedi meg, hogy az ősmoduljai
kódja hivatkozzon rá, azt nem, hogy hozzáférjen a belső kódjához. Mivel a
modulok tárolók, nem sokra megyünk azzal, ha csak magát a modult tesszük
nyilvánossá; tovább kell lépnünk, és a modulon belüli elemek közül is
nyilvánossá kell tennünk egyet vagy többet.

A 7-6. listában látható hibák azt mondják, hogy az `add_to_waitlist` függvény
privát. A privátsági szabályok a structokra, az enumokra, a függvényekre és a
metódusokra ugyanúgy vonatkoznak, mint a modulokra.

Tegyük nyilvánossá az `add_to_waitlist` függvényt is a `pub` kulcsszónak a
definíciója elé írásával, ahogy a 7-7. listában látható.

<Listing number="7-7" file-name="src/lib.rs" caption="A `pub` kulcsszó hozzáadása a `mod hosting`-hoz és az `fn add_to_waitlist`-hez lehetővé teszi, hogy meghívjuk a függvényt az `eat_at_restaurant`-ból.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Most már le fog fordulni a kód! Hogy lássuk, a `pub` kulcsszó hozzáadása miért
teszi lehetővé ezeknek az útvonalaknak a használatát az `eat_at_restaurant`-ban
a privátsági szabályok fényében, nézzük meg az abszolút és a relatív útvonalat.

Az abszolút útvonalban a `crate`-tel kezdünk, a crate-ünk modulfájának
gyökerével. A `front_of_house` modul a crate gyökerében van definiálva. Bár a
`front_of_house` nem nyilvános, mégis hivatkozhatunk rá az
`eat_at_restaurant`-ból, mert az `eat_at_restaurant` függvény ugyanabban a
modulban van definiálva, mint a `front_of_house` (azaz az `eat_at_restaurant` és
a `front_of_house` testvérek). Ezt követi a `pub`-bal megjelölt `hosting` modul.
A `hosting` szülőmodulját elérjük, tehát a `hosting`-ot is elérjük. Végül az
`add_to_waitlist` függvény `pub`-bal van megjelölve, a szülőmodulját pedig
elérjük, így ez a függvényhívás működik!

A relatív útvonalban a logika ugyanaz, mint az abszolút útvonal esetében, csak
az első lépés más: az útvonal nem a crate gyökeréből indul, hanem a
`front_of_house`-ból. A `front_of_house` modul ugyanabban a modulban van
definiálva, mint az `eat_at_restaurant`, így az abból a modulból induló relatív
útvonal működik, amelyben az `eat_at_restaurant` definiálva van. Ezután, mivel a
`hosting` és az `add_to_waitlist` `pub`-bal van megjelölve, az útvonal többi
része is működik, és ez a függvényhívás érvényes!

Ha azt tervezed, hogy megosztod a library crate-edet, hogy más projektek is
használhassák a kódodat, akkor a nyilvános API-d az a szerződés a crate-ed
felhasználóival, amely meghatározza, hogyan léphetnek kapcsolatba a kódoddal. A
nyilvános API változásainak kezelése körül sok megfontolandó szempont van, hogy
az emberek könnyebben építhessenek a crate-edre. Ezek a szempontok kívül esnek e
könyv keretein; ha érdekel a téma, nézd meg
[a Rust API-irányelveket][api-guidelines].

> #### Bevált gyakorlatok binary és library crate-et is tartalmazó csomagokhoz
>
> Említettük, hogy egy csomag tartalmazhat egy _src/main.rs_ binary crate
> gyökeret és egy _src/lib.rs_ library crate gyökeret is, és alapértelmezés
> szerint mindkét crate a csomag nevét viseli. Az ilyen, library és binary
> crate-et is tartalmazó mintát követő csomagokban a binary crate jellemzően
> épp csak annyi kódot tartalmaz, amennyi elindít egy futtatható programot,
> amely a library crate-ben definiált kódot hívja meg. Így más projektek is
> élvezhetik a csomag által nyújtott funkcionalitás legnagyobb részét, mert a
> library crate kódja megosztható.
>
> A modulfát a _src/lib.rs_ fájlban érdemes definiálni. Ezután bármely
> nyilvános elem használható a binary crate-ben, ha az útvonalakat a csomag
> nevével kezded. A binary crate a library crate felhasználójává válik, éppen
> úgy, ahogy egy teljesen külső crate használná a library crate-et: kizárólag a
> nyilvános API-t használhatja. Ez segít jó API-t tervezni; nemcsak a szerzője
> vagy, hanem az ügyfele is!
>
> A [12. fejezetben][ch12]<!-- ignore --> ezt a szervezési gyakorlatot egy
> parancssori programmal mutatjuk be, amely binary és library crate-et is
> tartalmaz majd.

### Relatív útvonalak indítása a `super` kulcsszóval

Olyan relatív útvonalakat is fel tudunk építeni, amelyek nem az aktuális
modulból vagy a crate gyökeréből, hanem a szülőmodulból indulnak: ehhez a
`super`-t kell az útvonal elejére írni. Ez olyan, mint amikor egy
fájlrendszerbeli útvonalat a `..` szintaxissal kezdünk, ami a szülőkönyvtárba
lépést jelenti. A `super` használatával olyan elemre hivatkozhatunk, amelyről
tudjuk, hogy a szülőmodulban van, és ez megkönnyítheti a modulfa átrendezését,
amikor a modul szorosan kapcsolódik a szülőjéhez, a szülő viszont egy nap
esetleg máshová kerül a modulfában.

Nézd meg a 7-8. listában szereplő kódot, amely azt a helyzetet modellezi,
amikor egy szakács kijavít egy hibás rendelést, és személyesen viszi ki a
vendégnek. A `back_of_house` modulban definiált `fix_incorrect_order` függvény
meghívja a szülőmodulban definiált `deliver_order` függvényt úgy, hogy megadja a
`deliver_order`-höz vezető, `super`-rel kezdődő útvonalat.

<Listing number="7-8" file-name="src/lib.rs" caption="Függvény hívása `super`-rel kezdődő relatív útvonalon">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

A `fix_incorrect_order` függvény a `back_of_house` modulban van, így a `super`
segítségével a `back_of_house` szülőmoduljába léphetünk, ami ebben az esetben a
gyökér, azaz a `crate`. Innen keressük a `deliver_order`-t, és meg is találjuk.
Siker! Úgy gondoljuk, hogy a `back_of_house` modul és a `deliver_order` függvény
valószínűleg ugyanebben a viszonyban marad egymással, és együtt kerülnek majd
máshová, ha úgy döntenénk, hogy átszervezzük a crate modulfáját. Ezért
használtuk a `super`-t: így kevesebb helyen kell majd frissítenünk a kódot a
jövőben, ha ez a kód egy másik modulba kerül.

### Structok és enumok nyilvánossá tétele

A `pub` kulcsszóval structokat és enumokat is nyilvánossá nyilváníthatunk, de a
`pub` structokkal és enumokkal való használatának van néhány további részlete.
Ha a `pub`-ot egy structdefiníció elé írjuk, a struct nyilvános lesz, a struct
mezői viszont továbbra is priváték maradnak. Minden egyes mezőről külön-külön
eldönthetjük, hogy nyilvános legyen-e. A 7-9. listában egy nyilvános
`back_of_house::Breakfast` structot definiáltunk, amelynek a `toast` mezője
nyilvános, a `seasonal_fruit` mezője viszont privát. Ez azt az esetet
modellezi, amikor egy étteremben a vendég kiválaszthatja, milyen kenyér jár az
ételhez, azt viszont a szakács dönti el, milyen gyümölcs kerül mellé, aszerint,
hogy mi van szezonban és készleten. Az elérhető gyümölcs gyorsan változik, így a
vendégek nem választhatják ki a gyümölcsöt, sőt azt sem láthatják, melyiket
kapják majd.

<Listing number="7-9" file-name="src/lib.rs" caption="Struct néhány nyilvános és néhány privát mezővel">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Mivel a `back_of_house::Breakfast` struct `toast` mezője nyilvános, az
`eat_at_restaurant`-ban pontjelöléssel írhatunk a `toast` mezőbe, és
olvashatunk belőle. Vedd észre, hogy a `seasonal_fruit` mezőt nem használhatjuk
az `eat_at_restaurant`-ban, mert a `seasonal_fruit` privát. Próbáld meg
kikommentezni azt a sort, amely a `seasonal_fruit` mező értékét módosítja, és
nézd meg, milyen hibát kapsz!

Azt is vedd figyelembe, hogy mivel a `back_of_house::Breakfast`-nek van egy
privát mezője, a structnak nyilvános asszociált függvényt kell biztosítania,
amely `Breakfast`-példányt hoz létre (itt `summer`-nek neveztük el). Ha a
`Breakfast`-nek nem lenne ilyen függvénye, nem tudnánk `Breakfast`-példányt
létrehozni az `eat_at_restaurant`-ban, mert nem tudnánk beállítani a privát
`seasonal_fruit` mező értékét az `eat_at_restaurant`-ban.

Ezzel szemben ha egy enumot teszünk nyilvánossá, akkor annak az összes variánsa
nyilvános lesz. Csak a `pub`-ot kell az `enum` kulcsszó elé írnunk, ahogy azt a
7-10. lista mutatja.

<Listing number="7-10" file-name="src/lib.rs" caption="Ha egy enumot nyilvánossá nyilvánítunk, az összes variánsa nyilvános lesz.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Mivel az `Appetizer` enumot nyilvánossá tettük, a `Soup` és a `Salad`
variánsokat használhatjuk az `eat_at_restaurant`-ban.

Az enumok nem túl hasznosak, ha a variánsaik nem nyilvánosak; bosszantó lenne,
ha minden enumvariánst `pub`-bal kellene megjelölni minden esetben, ezért az
enumvariánsok alapértelmezés szerint nyilvánosak. A structok gyakran akkor is
hasznosak, ha a mezőik nem nyilvánosak, ezért a struct mezői az általános
szabályt követik: alapértelmezés szerint minden privát, hacsak nincs `pub`-bal
megjelölve.

Van még egy `pub`-bal kapcsolatos helyzet, amelyet nem tárgyaltunk, és ez az
utolsó modulrendszerbeli képesség: a `use` kulcsszó. Először magával a
`use`-zal foglalkozunk, majd megmutatjuk, hogyan lehet a `pub`-ot és a `use`-t
kombinálni.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
