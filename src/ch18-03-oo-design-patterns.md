## Egy objektumorientált tervezési minta megvalósítása

A _state pattern_ egy objektumorientált tervezési minta. A minta lényege, hogy
definiáljuk azoknak az állapotoknak a halmazát, amelyekben egy érték belsőleg
lehet. Az állapotokat _állapotobjektumok_ egy halmaza képviseli, és az érték
viselkedése az állapotától függően változik. Végig fogunk dolgozni egy
példát: egy blogbejegyzés-structot, amelynek van egy mezője az állapota
tárolására, ez pedig a „piszkozat”, „lektorálás alatt” vagy „publikált”
halmazból származó állapotobjektum lesz.

Az állapotobjektumok közös funkcionalitáson osztoznak: a Rustban természetesen
structokat és traiteket használunk objektumok és öröklődés helyett. Minden
állapotobjektum a saját viselkedéséért felel, és azért, hogy megszabja, mikor
kell másik állapotba váltania. Az az érték, amely az állapotobjektumot tartja,
semmit nem tud az egyes állapotok eltérő viselkedéséről, sem arról, mikor kell
állapotot váltani.

A state pattern használatának előnye, hogy amikor a program üzleti
követelményei megváltoznak, nem kell megváltoztatnunk sem az állapotot tartó
érték kódját, sem az értéket használó kódot. Csak az egyik állapotobjektumon
belüli kódot kell frissítenünk, hogy megváltoztassuk a szabályait, vagy esetleg
további állapotobjektumokat kell felvennünk.

Először hagyományosabb, objektumorientált módon valósítjuk meg a state
patternt. Ezután olyan megközelítést használunk, amely a Rustban valamivel
természetesebb. Vágjunk bele, és lépésről lépésre valósítsunk meg egy
blogbejegyzés-munkafolyamatot a state pattern segítségével.

A végleges működés így fog kinézni:

1. Egy blogbejegyzés üres piszkozatként indul.
1. Amikor a piszkozat elkészül, kérünk rá egy lektorálást.
1. Amikor a bejegyzést jóváhagyják, publikálásra kerül.
1. Csak a publikált blogbejegyzések adnak vissza kinyomtatandó tartalmat, hogy
   a jóvá nem hagyott bejegyzések ne kerülhessenek véletlenül publikálásra.

Minden más, egy bejegyzésen megkísérelt változtatásnak hatástalannak kell
lennie. Ha például megpróbálunk jóváhagyni egy piszkozat állapotú
blogbejegyzést, mielőtt lektorálást kértünk volna rá, a bejegyzésnek
publikálatlan piszkozatnak kell maradnia.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Kísérlet a hagyományos objektumorientált stílusra

Végtelen sokféleképpen strukturálhatjuk a kódot ugyanannak a problémának a
megoldására, és mindegyik mód más kompromisszumokkal jár. Ennek a szakasznak az
implementációja inkább hagyományos objektumorientált stílusú; Rustban is meg
lehet így írni, de nem használja ki a Rust néhány erősségét. Később egy másik
megoldást is bemutatunk, amely szintén az objektumorientált tervezési mintát
használja, de úgy van felépítve, hogy az objektumorientált tapasztalattal
rendelkező programozók számára talán kevésbé ismerősnek tűnik. Összehasonlítjuk
majd a két megoldást, hogy megtapasztaljuk, milyen kompromisszumokkal jár, ha a
Rust-kódot másképp tervezzük meg, mint a más nyelveken írt kódot.

A 18-11. lista kód formájában mutatja be ezt a munkafolyamatot: ez egy
példahasználata annak az API-nak, amelyet egy `blog` nevű library crate-ben
fogunk megvalósítani. Ez egyelőre nem fordul le, mert még nem implementáltuk a
`blog` crate-et.

<Listing number="18-11" file-name="src/main.rs" caption="Kód, amely bemutatja, milyen viselkedést szeretnénk a `blog` crate-ünktől">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Azt szeretnénk, hogy a felhasználó a `Post::new` segítségével új, piszkozat
állapotú blogbejegyzést hozhasson létre. Azt is szeretnénk, hogy szöveget
lehessen hozzáadni a blogbejegyzéshez. Ha azonnal, még a jóváhagyás előtt
próbáljuk lekérdezni a bejegyzés tartalmát, nem kaphatunk szöveget, mert a
bejegyzés még piszkozat. Bemutatási céllal `assert_eq!` hívásokat tettünk a
kódba. Kiváló egységteszt lenne ehhez az az állítás, hogy egy piszkozat
állapotú blogbejegyzés `content` metódusa üres sztringet ad vissza, de ehhez a
példához nem írunk teszteket.

Ezután azt szeretnénk lehetővé tenni, hogy lektorálást lehessen kérni a
bejegyzésre, és azt szeretnénk, hogy a `content` üres sztringet adjon vissza,
amíg a lektorálásra várunk. Amikor a bejegyzés megkapja a jóváhagyást,
publikálásra kell kerülnie, vagyis a `content` hívásakor a bejegyzés szövegét
kell visszakapnunk.

Vedd észre, hogy a crate-ből egyedül a `Post` típussal lépünk kapcsolatba. Ez a
típus fogja használni a state patternt, és olyan értéket tart majd, amely a
három állapotobjektum egyike lesz, ezek pedig a bejegyzés lehetséges
állapotait – piszkozat, lektorálás alatt vagy publikált – képviselik. Az egyik
állapotból a másikba való átmenetet a `Post` típus belsőleg kezeli. Az
állapotok azokra a metódushívásokra válaszul változnak, amelyeket a
könyvtárunk használói a `Post` példányon hívnak meg, de nekik nem kell
közvetlenül kezelniük az állapotváltásokat. Ráadásul a felhasználók nem is
hibázhatnak az állapotokkal, például nem publikálhatnak egy bejegyzést, mielőtt
azt lektorálták volna.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### A `Post` definiálása és új példány létrehozása

Vágjunk bele a könyvtár implementációjába! Tudjuk, hogy szükségünk van egy
publikus `Post` structra, amely valamilyen tartalmat tárol, ezért a struct
definíciójával és egy hozzá tartozó publikus `new` függvénnyel kezdjük, amely
`Post` példányt hoz létre, ahogy a 18-12. listában látható. Készítünk egy
privát `State` traitet is, amely azt a viselkedést definiálja, amellyel a
`Post` minden állapotobjektumának rendelkeznie kell.

Ezután a `Post` egy `Box<dyn State>` trait objectet fog tartani egy `Option<T>`
belsejében, egy `state` nevű privát mezőben, hogy tárolja az
állapotobjektumot. Mindjárt látni fogod, miért van szükség az `Option<T>`-re.

<Listing number="18-12" file-name="src/lib.rs" caption="Egy `Post` struct és egy `new` függvény definíciója, amely új `Post` példányt hoz létre, valamint egy `State` trait és egy `Draft` struct">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

A `State` trait a bejegyzés különböző állapotai által megosztott viselkedést
definiálja. Az állapotobjektumok a `Draft`, a `PendingReview` és a `Published`,
és mindegyik implementálni fogja a `State` traitet. Egyelőre a traitnek nincs
egyetlen metódusa sem, és azzal kezdjük, hogy csak a `Draft` állapotot
definiáljuk, mert azt szeretnénk, hogy a bejegyzés ebben az állapotban induljon.

Amikor új `Post`-ot hozunk létre, a `state` mezőjét egy `Some` értékre
állítjuk, amely egy `Box`-ot tart. Ez a `Box` a `Draft` struct egy új
példányára mutat. Ez biztosítja, hogy valahányszor új `Post` példányt hozunk
létre, az piszkozatként induljon. Mivel a `Post` `state` mezője privát, nincs
mód arra, hogy más állapotban hozzunk létre `Post`-ot! A `Post::new`
függvényben a `content` mezőt egy új, üres `String`-re állítjuk.

#### A bejegyzés tartalmának tárolása

A 18-11. listában láttuk, hogy szeretnénk meghívni egy `add_text` nevű
metódust, és átadni neki egy `&str`-t, amely aztán a blogbejegyzés
szövegtartalmához adódik. Ezt metódusként valósítjuk meg ahelyett, hogy a
`content` mezőt `pub`-ként tennénk elérhetővé, hogy később olyan metódust
implementálhassunk, amely szabályozza, hogyan olvasható a `content` mező adata.
Az `add_text` metódus meglehetősen egyszerű, úgyhogy adjuk hozzá a 18-13.
listában látható implementációt az `impl Post` blokkhoz.

<Listing number="18-13" file-name="src/lib.rs" caption="Az `add_text` metódus implementálása, amely szöveget ad a bejegyzés `content` mezőjéhez">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Az `add_text` metódus módosítható referenciát vesz át a `self`-re, mert
megváltoztatjuk azt a `Post` példányt, amelyen az `add_text`-et meghívjuk.
Ezután meghívjuk a `push_str`-t a `content`-ben lévő `String`-en, és átadjuk a
`text` argumentumot, hogy hozzáadódjon az elmentett `content`-hez. Ez a
viselkedés nem függ attól, milyen állapotban van a bejegyzés, ezért nem része a
state patternnek. Az `add_text` metódus egyáltalán nem lép kapcsolatba a
`state` mezővel, de része annak a viselkedésnek, amelyet támogatni szeretnénk.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Annak biztosítása, hogy egy piszkozat bejegyzés tartalma üres legyen

Még azután is, hogy meghívtuk az `add_text`-et, és tartalmat adtunk a
bejegyzésünkhöz, azt szeretnénk, hogy a `content` metódus üres string slice-ot
adjon vissza, mert a bejegyzés még mindig piszkozat állapotban van, ahogy azt a
18-11. lista első `assert_eq!` hívása mutatja. Egyelőre implementáljuk a
`content` metódust a lehető legegyszerűbb módon, amely kielégíti ezt a
követelményt: mindig üres string slice-ot adunk vissza. Ezt később
megváltoztatjuk, miután megvalósítottuk a bejegyzés állapotának
megváltoztatását, hogy publikálható legyen. Egyelőre a bejegyzések csak
piszkozat állapotban lehetnek, tehát a bejegyzés tartalmának mindig üresnek
kell lennie. A 18-14. lista mutatja ezt az ideiglenes implementációt.

<Listing number="18-14" file-name="src/lib.rs" caption="Ideiglenes implementáció hozzáadása a `Post` `content` metódusához, amely mindig üres string slice-ot ad vissza">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Ezzel a hozzáadott `content` metódussal a 18-11. listában minden a szándékunk
szerint működik az első `assert_eq!` hívásig bezárólag.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Lektorálás kérése, amely megváltoztatja a bejegyzés állapotát

Ezután olyan funkciót kell hozzáadnunk, amellyel lektorálást lehet kérni egy
bejegyzésre, és amelynek `Draft`-ról `PendingReview`-ra kell változtatnia az
állapotát. A 18-15. lista mutatja ezt a kódot.

<Listing number="18-15" file-name="src/lib.rs" caption="A `request_review` metódusok implementálása a `Post`-on és a `State` traiten">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

A `Post`-nak adunk egy `request_review` nevű publikus metódust, amely
módosítható referenciát vesz át a `self`-re. Ezután meghívunk egy belső
`request_review` metódust a `Post` aktuális állapotán, és ez a második
`request_review` metódus felemészti az aktuális állapotot, és új állapotot ad
vissza.

A `request_review` metódust hozzáadjuk a `State` traithez; a traitet
implementáló minden típusnak mostantól implementálnia kell a `request_review`
metódust. Vedd észre, hogy a metódus első paramétereként nem `self`, `&self`
vagy `&mut self` szerepel, hanem `self: Box<Self>`. Ez a szintaxis azt jelenti,
hogy a metódus csak akkor érvényes, ha az adott típust tartó `Box`-on hívjuk
meg. Ez a szintaxis átveszi a `Box<Self>` ownershipjét, érvénytelenítve a régi
állapotot, hogy a `Post` állapotértéke új állapottá alakulhasson.

Ahhoz, hogy felemészthesse a régi állapotot, a `request_review` metódusnak át
kell vennie az állapotérték ownershipjét. Itt jön a képbe a `Post` `state`
mezőjében lévő `Option`: meghívjuk a `take` metódust, hogy kivegyük a `Some`
értéket a `state` mezőből, és `None`-t hagyjunk a helyén, mert a Rust nem
engedi meg, hogy a structjainkban feltöltetlen mezők legyenek. Ez lehetővé
teszi, hogy a `state` értéket kimozgassuk a `Post`-ból, ahelyett hogy csak
kölcsönvennénk. Ezután a bejegyzés `state` értékét a művelet eredményére
állítjuk.

A `state` mezőt átmenetileg `None`-ra kell állítanunk, ahelyett hogy
közvetlenül olyan kóddal állítanánk be, mint a `self.state =
self.state.request_review();`, hogy megkapjuk a `state` érték ownershipjét. Ez
biztosítja, hogy a `Post` ne használhassa a régi `state` értéket azután, hogy
azt új állapottá alakítottuk.

A `Draft` `request_review` metódusa egy új `PendingReview` struct új, boxolt
példányát adja vissza, amely azt az állapotot képviseli, amikor a bejegyzés
lektorálásra vár. A `PendingReview` struct is implementálja a `request_review`
metódust, de nem végez semmilyen átalakítást. Ehelyett önmagát adja vissza,
mert ha egy már `PendingReview` állapotban lévő bejegyzésre kérünk
lektorálást, annak `PendingReview` állapotban kell maradnia.

Most már kezdhetjük látni a state pattern előnyeit: a `Post` `request_review`
metódusa ugyanaz, függetlenül attól, mi a `state` értéke. Minden állapot a
saját szabályaiért felel.

A `Post` `content` metódusát így hagyjuk, üres string slice-ot ad vissza. Most
már a `Draft` állapot mellett `PendingReview` állapotban is lehet egy `Post`,
de ugyanazt a viselkedést szeretnénk `PendingReview` állapotban is. A 18-11.
lista mostantól a második `assert_eq!` hívásig működik!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Az `approve` hozzáadása a `content` viselkedésének megváltoztatásához

Az `approve` metódus hasonló lesz a `request_review` metódushoz: a `state`
mezőt arra az értékre állítja, amelyet az aktuális állapot szerint az adott
állapot jóváhagyásakor fel kell vennie, ahogy a 18-16. listában látható.

<Listing number="18-16" file-name="src/lib.rs" caption="Az `approve` metódus implementálása a `Post`-on és a `State` traiten">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Hozzáadjuk az `approve` metódust a `State` traithez, és felveszünk egy új
structot, amely implementálja a `State`-et: a `Published` állapotot.

Ahhoz hasonlóan, ahogy a `PendingReview` `request_review` metódusa működik, ha
az `approve` metódust egy `Draft`-on hívjuk meg, annak nem lesz hatása, mert az
`approve` a `self`-et adja vissza. Amikor az `approve`-ot a `PendingReview`-n
hívjuk meg, az a `Published` struct új, boxolt példányát adja vissza. A
`Published` struct implementálja a `State` traitet, és mind a `request_review`,
mind az `approve` metódus esetében önmagát adja vissza, mert ezekben az
esetekben a bejegyzésnek `Published` állapotban kell maradnia.

Most frissítenünk kell a `Post` `content` metódusát. Azt szeretnénk, hogy a
`content` által visszaadott érték a `Post` aktuális állapotától függjön, ezért
a `Post`-tal a `state` értékén definiált `content` metódusra delegáltatjuk a
feladatot, ahogy a 18-17. listában látható.

<Listing number="18-17" file-name="src/lib.rs" caption="A `Post` `content` metódusának frissítése, hogy a `State` `content` metódusára delegáljon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Mivel az a cél, hogy mindezek a szabályok a `State`-et implementáló structokon
belül maradjanak, meghívunk egy `content` metódust a `state`-ben lévő értéken,
és argumentumként átadjuk a bejegyzés példányát (vagyis a `self`-et). Ezután
visszaadjuk azt az értéket, amelyet a `state` értéken meghívott `content`
metódus adott vissza.

Az `Option`-on meghívjuk az `as_ref` metódust, mert az `Option`-ben lévő
értékre referenciát szeretnénk kapni, nem pedig az érték ownershipjét. Mivel a
`state` típusa `Option<Box<dyn State>>`, az `as_ref` hívásakor egy
`Option<&Box<dyn State>>` értéket kapunk vissza. Ha nem hívnánk meg az
`as_ref`-et, hibát kapnánk, mert nem tudjuk kimozgatni a `state`-et a
függvényparaméter kölcsönvett `&self`-jéből.

Ezután meghívjuk az `unwrap` metódust, amelyről tudjuk, hogy soha nem fog
panicot kiváltani, mert tudjuk, hogy a `Post` metódusai gondoskodnak arról,
hogy a `state` mindig `Some` értéket tartalmazzon, amikor ezek a metódusok
lefutottak. Ez egyike azoknak az eseteknek, amelyekről a 9. fejezet [„Amikor
több információd van, mint a fordítónak”][more-info-than-rustc]<!-- ignore -->
című szakaszában beszéltünk, amikor tudjuk, hogy a `None` érték soha nem
fordulhat elő, még ha a fordító ezt nem is képes belátni.

Ezen a ponton, amikor a `&Box<dyn State>` értéken meghívjuk a `content`-et, a
deref coercion lép működésbe a `&`-en és a `Box`-on, így a `content` metódus
végül a `State` traitet implementáló típuson hívódik meg. Ez azt jelenti, hogy
a `content`-et fel kell vennünk a `State` trait definíciójába, és ott fogjuk
elhelyezni azt a logikát, amely megmondja, milyen tartalmat adjunk vissza az
adott állapottól függően, ahogy a 18-18. listában látható.

<Listing number="18-18" file-name="src/lib.rs" caption="A `content` metódus hozzáadása a `State` traithez">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Alapértelmezett implementációt adunk a `content` metódushoz, amely üres string
slice-ot ad vissza. Ez azt jelenti, hogy a `Draft` és a `PendingReview`
structon nem kell implementálnunk a `content`-et. A `Published` struct
felülírja a `content` metódust, és a `post.content` értékét adja vissza. Bár ez
kényelmes, az, hogy a `State` `content` metódusa dönti el a `Post` tartalmát,
elmossa a határt a `State` és a `Post` felelőssége között.

Vedd észre, hogy ehhez a metódushoz lifetime-annotációkra van szükségünk, ahogy
azt a 10. fejezetben megbeszéltük. Argumentumként egy `post`-ra vett
referenciát veszünk át, és e `post` egy részére vett referenciát adunk vissza,
így a visszaadott referencia lifetime-ja a `post` argumentum lifetime-jához
kapcsolódik.

És készen is vagyunk – a 18-11. lista most már teljes egészében működik!
Megvalósítottuk a state patternt a blogbejegyzés-munkafolyamat szabályaival. A
szabályokhoz kapcsolódó logika az állapotobjektumokban él, ahelyett hogy szét
lenne szórva a `Post`-ban.

> ### Miért nem enummal?
>
> Talán elgondolkodtál azon, miért nem használtunk olyan enumot, amelynek a
> variánsai a bejegyzés lehetséges állapotai. Ez mindenképpen járható megoldás;
> próbáld ki, és hasonlítsd össze a végeredményeket, hogy lásd, melyiket
> szereted jobban! Az enum használatának egyik hátránya, hogy minden helyen,
> ahol az enum értékét vizsgáljuk, `match` kifejezésre vagy hasonlóra lesz
> szükség az összes lehetséges variáns kezeléséhez. Ez ismétlődőbb lehet, mint
> ez a trait objectes megoldás.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### A state pattern értékelése

Megmutattuk, hogy a Rust képes megvalósítani az objektumorientált state
patternt, hogy egységbe zárja a bejegyzés különböző állapotaihoz tartozó
eltérő viselkedéseket. A `Post` metódusai semmit nem tudnak ezekről a
viselkedésekről. A kód szervezésének módja miatt csak egyetlen helyre kell
néznünk ahhoz, hogy megtudjuk, egy publikált bejegyzés hogyan viselkedhet: a
`State` trait `Published` structon lévő implementációjához.

Ha olyan alternatív implementációt készítenénk, amely nem használja a state
patternt, akkor helyette valószínűleg `match` kifejezéseket alkalmaznánk a
`Post` metódusaiban, vagy akár a `main` kódjában, amely megvizsgálja a
bejegyzés állapotát, és ezeken a helyeken változtat a viselkedésen. Ez azt
jelentené, hogy több helyre kellene néznünk ahhoz, hogy megértsük, mi mindennel
jár, ha egy bejegyzés publikált állapotban van.

A state patternnel a `Post` metódusaiban és azokon a helyeken, ahol a `Post`-ot
használjuk, nincs szükség `match` kifejezésekre, új állapot felvételéhez pedig
csak egy új structot kellene hozzáadnunk, és egyetlen helyen, azon az egyetlen
structon implementálnunk a trait metódusait.

A state patternt használó implementációt könnyű további funkciókkal bővíteni.
Hogy lásd, mennyire egyszerű a state patternt használó kód karbantartása,
próbálj ki néhányat az alábbi javaslatok közül:

- Adj hozzá egy `reject` metódust, amely a bejegyzés állapotát
  `PendingReview`-ról visszaállítja `Draft`-ra.
- Írd elő, hogy két `approve` hívásra legyen szükség, mielőtt az állapot
  `Published`-ra változhat.
- Csak akkor engedd, hogy a felhasználók szöveges tartalmat adjanak hozzá, ha a
  bejegyzés `Draft` állapotban van. Tipp: az állapotobjektum feleljen azért,
  ami a tartalommal kapcsolatban változhat, de ne feleljen a `Post`
  módosításáért.

A state pattern egyik hátránya, hogy mivel az állapotok valósítják meg az
állapotok közötti átmeneteket, egyes állapotok összekapcsolódnak egymással. Ha
a `PendingReview` és a `Published` közé felveszünk egy újabb állapotot, például
a `Scheduled`-t, akkor a `PendingReview` kódját kellene megváltoztatnunk, hogy
helyette a `Scheduled`-be váltson át. Kevesebb munka lenne, ha a
`PendingReview`-t nem kellene megváltoztatni egy új állapot felvételekor, de ez
azt jelentené, hogy másik tervezési mintára kellene váltanunk.

Egy másik hátrány, hogy némi logikát megkettőztünk. Az ismétlődés egy részének
kiküszöbölésére megpróbálhatnánk alapértelmezett implementációkat készíteni a
`State` trait `request_review` és `approve` metódusaihoz, amelyek a `self`-et
adják vissza. Ez azonban nem működne: amikor a `State`-et trait objectként
használjuk, a trait nem tudja, pontosan mi lesz a konkrét `self`, így a
visszatérési típus fordítási időben nem ismert. (Ez egyike a korábban említett
dyn kompatibilitási szabályoknak.)

További ismétlődés a `Post` `request_review` és `approve` metódusainak hasonló
implementációja. Mindkét metódus az `Option::take`-et használja a `Post`
`state` mezőjén, és ha a `state` értéke `Some`, akkor a becsomagolt érték
ugyanezen metódusának implementációjára delegálnak, majd a `state` mező új
értékét az eredményre állítják. Ha a `Post`-on sok ilyen mintát követő
metódusunk lenne, elgondolkodhatnánk azon, hogy makrót definiálunk az ismétlés
kiküszöbölésére (lásd a 20. fejezet [„Makrók”][macros]<!-- ignore --> című
szakaszát).

Azzal, hogy a state patternt pontosan úgy valósítjuk meg, ahogy azt az
objektumorientált nyelvekre definiálták, nem használjuk ki olyan teljes
mértékben a Rust erősségeit, ahogy tehetnénk. Nézzünk meg néhány olyan
változtatást a `blog` crate-en, amelyekkel az érvénytelen állapotok és
átmenetek fordítási idejű hibává tehetők.

### Az állapotok és a viselkedés típusokként való kódolása {#encoding-states-and-behavior-as-types}

Megmutatjuk, hogyan gondolhatod újra a state patternt, hogy más
kompromisszumokat kapj. Ahelyett, hogy az állapotokat és az átmeneteket
teljesen egységbe zárnánk úgy, hogy a külső kód semmit se tudjon róluk, az
állapotokat különböző típusokba kódoljuk. Ennek következtében a Rust
típusellenőrző rendszere fordítói hibával akadályozza meg azokat a
kísérleteket, amelyek piszkozat bejegyzéseket használnának ott, ahol csak
publikált bejegyzések megengedettek.

Nézzük meg a `main` első részét a 18-11. listából:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Továbbra is lehetővé tesszük, hogy a `Post::new` segítségével piszkozat
állapotú új bejegyzéseket hozzunk létre, és hogy szöveget adhassunk a bejegyzés
tartalmához. Ahelyett azonban, hogy a piszkozat bejegyzésnek lenne egy üres
sztringet visszaadó `content` metódusa, azt fogjuk elérni, hogy a piszkozat
bejegyzéseknek egyáltalán ne legyen `content` metódusuk. Így ha megpróbáljuk
lekérdezni egy piszkozat bejegyzés tartalmát, fordítói hibát kapunk, amely
közli, hogy a metódus nem létezik. Ennek eredményeként lehetetlen lesz, hogy
véletlenül megjelenítsük egy piszkozat bejegyzés tartalmát az éles
környezetben, mert az a kód le sem fordul. A 18-19. lista mutatja egy `Post`
struct és egy `DraftPost` struct definícióját, valamint a rajtuk lévő
metódusokat.

<Listing number="18-19" file-name="src/lib.rs" caption="Egy `Post` `content` metódussal és egy `DraftPost` `content` metódus nélkül">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Mind a `Post`, mind a `DraftPost` structnak van egy privát `content` mezője,
amely a blogbejegyzés szövegét tárolja. A structoknak már nincs `state`
mezőjük, mert az állapot kódolását áthelyezzük a structok típusaiba. A `Post`
struct a publikált bejegyzést fogja képviselni, és van egy `content` metódusa,
amely visszaadja a `content` mezőt.

Továbbra is van egy `Post::new` függvényünk, de ez `Post` példány helyett
`DraftPost` példányt ad vissza. Mivel a `content` privát, és nincs olyan
függvény, amely `Post`-ot adna vissza, jelenleg nem lehet `Post` példányt
létrehozni.

A `DraftPost` structnak van egy `add_text` metódusa, így a korábbiakhoz
hasonlóan hozzáadhatunk szöveget a `content`-hez, de vedd észre, hogy a
`DraftPost`-on nincs definiálva `content` metódus! A program mostantól tehát
biztosítja, hogy minden bejegyzés piszkozatként induljon, és hogy a piszkozat
bejegyzések tartalma ne legyen elérhető megjelenítésre. Minden kísérlet arra,
hogy ezeket a megkötéseket megkerüljük, fordítói hibát eredményez.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Hogyan jutunk hát publikált bejegyzéshez? Azt a szabályt szeretnénk
kikényszeríteni, hogy egy piszkozat bejegyzést le kell lektorálni és jóvá kell
hagyni, mielőtt publikálható lenne. A lektorálásra váró állapotban lévő
bejegyzésnek továbbra sem szabad tartalmat megjelenítenie. Valósítsuk meg ezeket
a megkötéseket egy újabb struct, a `PendingReviewPost` hozzáadásával: a
`DraftPost`-on definiálunk egy `request_review` metódust, amely
`PendingReviewPost`-ot ad vissza, a `PendingReviewPost`-on pedig egy `approve`
metódust, amely `Post`-ot ad vissza, ahogy a 18-20. listában látható.

<Listing number="18-20" file-name="src/lib.rs" caption="Egy `PendingReviewPost`, amely a `DraftPost` `request_review` metódusának meghívásával jön létre, és egy `approve` metódus, amely a `PendingReviewPost`-ot publikált `Post`-tá alakítja">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

A `request_review` és az `approve` metódus átveszi a `self` ownershipjét, így
felemészti a `DraftPost`, illetve a `PendingReviewPost` példányt, és
`PendingReviewPost`-tá, illetve publikált `Post`-tá alakítja őket. Ily módon
nem maradnak ottfelejtett `DraftPost` példányaink azután, hogy meghívtuk rajtuk
a `request_review`-t, és így tovább. A `PendingReviewPost` structon nincs
definiálva `content` metódus, ezért a tartalmának olvasására tett kísérlet
fordítói hibát eredményez, akárcsak a `DraftPost` esetében. Mivel az egyetlen
mód arra, hogy olyan publikált `Post` példányhoz jussunk, amelyen van
definiálva `content` metódus, az `approve` metódus meghívása egy
`PendingReviewPost`-on, `PendingReviewPost`-hoz pedig kizárólag a `DraftPost`
`request_review` metódusának meghívásával juthatunk, ezzel a
blogbejegyzés-munkafolyamatot bekódoltuk a típusrendszerbe.

Néhány apró változtatást azonban a `main`-en is el kell végeznünk. A
`request_review` és az `approve` metódus új példányokat ad vissza, ahelyett
hogy módosítaná azt a structot, amelyen meghívjuk őket, ezért további `let post
=` shadowing értékadásokat kell felvennünk a visszakapott példányok
elmentéséhez. Azok az állítások sem szerepelhetnek már, amelyek szerint a
piszkozat és a lektorálásra váró bejegyzések tartalma üres sztring, és nincs is
rájuk szükségünk: már le sem tudjuk fordítani azt a kódot, amely az ilyen
állapotban lévő bejegyzések tartalmát próbálná használni. A frissített `main`
kódot a 18-21. lista mutatja.

<Listing number="18-21" file-name="src/main.rs" caption="A `main` módosításai, hogy a blogbejegyzés-munkafolyamat új implementációját használja">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Azok a változtatások, amelyeket a `main`-en el kellett végeznünk a `post`
újbóli értékadásához, azt jelentik, hogy ez az implementáció már nem egészen
követi az objektumorientált state patternt: az állapotok közötti átalakulások
már nincsenek teljes egészében a `Post` implementációjába zárva. Cserébe
viszont azt nyerjük, hogy az érvénytelen állapotok immár lehetetlenek a
típusrendszernek és a fordítási időben történő típusellenőrzésnek
köszönhetően! Ez biztosítja, hogy bizonyos hibák – például egy publikálatlan
bejegyzés tartalmának megjelenítése – kiderüljenek, mielőtt éles környezetbe
kerülnének.

Próbáld ki a szakasz elején javasolt feladatokat a `blog` crate-en abban az
állapotában, ahogy a 18-21. lista után áll, és nézd meg, mit gondolsz a kód
ezen változatának a felépítéséről. Vedd észre, hogy néhány feladat ebben a
kialakításban talán már eleve teljesül.

Láttuk, hogy bár a Rust képes megvalósítani objektumorientált tervezési
mintákat, más minták is rendelkezésre állnak benne, például az, hogy az
állapotot a típusrendszerbe kódoljuk. Ezek a minták más-más
kompromisszumokkal járnak. Bár lehet, hogy nagyon jól ismered az
objektumorientált mintákat, ha a Rust képességeit kihasználva újragondolod a
problémát, az előnyökkel járhat: például bizonyos hibák már fordítási időben
kiszűrhetők. Az objektumorientált minták nem mindig lesznek a legjobb megoldás
Rustban, mert vannak olyan képességek – például az ownership –, amelyekkel az
objektumorientált nyelvek nem rendelkeznek.

## Összefoglalás

Függetlenül attól, hogy e fejezet elolvasása után objektumorientált nyelvnek
tartod-e a Rustot, most már tudod, hogy trait objectek használatával
megkaphatsz néhány objektumorientált képességet a Rustban. A dinamikus dispatch
egy kis futásidejű teljesítmény árán rugalmasságot adhat a kódodnak. Ezt a
rugalmasságot olyan objektumorientált minták megvalósítására használhatod,
amelyek javíthatják a kódod karbantarthatóságát. A Rustnak vannak más
képességei is, például az ownership, amelyekkel az objektumorientált nyelvek
nem rendelkeznek. Egy objektumorientált minta nem mindig lesz a legjobb mód a
Rust erősségeinek kihasználására, de rendelkezésre álló lehetőség.

A következőkben a mintákat vesszük szemügyre, amelyek a Rust egy másik olyan
képességét jelentik, amely nagy rugalmasságot tesz lehetővé. A könyv során már
röviden találkoztunk velük, de a teljes képességüket még nem láttuk. Vágjunk
bele!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
