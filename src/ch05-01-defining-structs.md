## Structok definiálása és példányosítása

A structok hasonlítanak a tuple-ökre, amelyekről a [„A tuple típus”][tuples]<!--
ignore --> szakaszban volt szó, hiszen mindkettő több összetartozó értéket
tárol. A tuple-ökhöz hasonlóan a struct darabjai is különböző típusúak
lehetnek. A tuple-öktől eltérően viszont a structban minden adatdarabot
elnevezel, így világos, hogy az értékek mit jelentenek. Ezektől a nevektől a
structok rugalmasabbak a tuple-öknél: nem kell az adatok sorrendjére
hagyatkoznod ahhoz, hogy megadd vagy elérd egy példány értékeit.

Egy struct definiálásához beírjuk a `struct` kulcsszót, és nevet adunk az egész
structnak. A struct nevének le kell írnia, mi a jelentősége az együvé
csoportosított adatdaraboknak. Ezután kapcsos zárójelek között definiáljuk az
adatdarabok nevét és típusát; ezeket _mezőknek_ nevezzük. Az 5-1. lista például
egy olyan structot mutat, amely egy felhasználói fiók adatait tárolja.

<Listing number="5-1" file-name="src/main.rs" caption="A `User` struct definíciója">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Ahhoz, hogy a definiálás után használjuk a structot, létrehozzuk a struct egy
_példányát_ úgy, hogy minden mezőhöz konkrét értéket adunk meg. A példányt úgy
hozzuk létre, hogy leírjuk a struct nevét, majd kapcsos zárójelek között
felsoroljuk a _`kulcs: érték`_ párokat, ahol a kulcsok a mezők nevei, az értékek
pedig azok az adatok, amelyeket ezekben a mezőkben tárolni akarunk. A mezőket
nem kell ugyanabban a sorrendben megadnunk, ahogy a structban deklaráltuk őket.
Más szóval a struct definíciója olyan, mint a típus általános sablonja, a
példányok pedig konkrét adatokkal töltik ki ezt a sablont, így hozva létre a
típus értékeit. Egy konkrét felhasználót például az 5-2. listában látható módon
deklarálhatunk.

<Listing number="5-2" file-name="src/main.rs" caption="A `User` struct egy példányának létrehozása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Ha egy konkrét értéket akarunk kiolvasni egy structból, pontjelöléssel tesszük.
Ennek a felhasználónak az e-mail-címét például a `user1.email` kifejezéssel
érjük el. Ha a példány módosítható, akkor a pontjelöléssel és egy adott mezőbe
való értékadással meg is változtathatunk egy értéket. Az 5-3. lista azt
mutatja, hogyan változtatható meg egy módosítható `User` példány `email`
mezőjének értéke.

<Listing number="5-3" file-name="src/main.rs" caption="Egy `User` példány `email` mezőjében lévő érték megváltoztatása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Vedd észre, hogy a teljes példánynak módosíthatónak kell lennie; a Rust nem
engedi, hogy csak bizonyos mezőket jelöljünk módosíthatónak. Mint bármely más
kifejezést, a struct új példányának létrehozását is megtehetjük a függvénytörzs
utolsó kifejezéseként, hogy implicit módon visszaadjuk ezt az új példányt.

Az 5-4. lista egy `build_user` függvényt mutat, amely a megadott e-mail-címmel
és felhasználónévvel tér vissza egy `User` példánnyal. Az `active` mező a `true`
értéket kapja, a `sign_in_count` pedig az `1` értéket.

<Listing number="5-4" file-name="src/main.rs" caption="Egy `build_user` függvény, amely egy e-mail-címet és egy felhasználónevet kap, és egy `User` példányt ad vissza">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Van értelme a függvény paramétereit ugyanazokkal a nevekkel elnevezni, mint a
struct mezőit, de kicsit fárasztó újra és újra leírni az `email` és a
`username` mezőneveket és változókat. Ha a structnak több mezője lenne, az
egyes nevek ismételgetése még bosszantóbb lenne. Szerencsére van rá egy
kényelmes rövidítés!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### A mezőinicializáló rövidítés használata

Mivel az 5-4. listában a paraméternevek és a struct mezőnevei pontosan
megegyeznek, a _mezőinicializáló rövidítés_ (field init shorthand)
szintaxisával úgy írhatjuk át a `build_user` függvényt, hogy pontosan
ugyanúgy viselkedjen, de ne ismételgesse a `username`-et és az `email`-t – ezt
mutatja az 5-5. lista.

<Listing number="5-5" file-name="src/main.rs" caption="Egy `build_user` függvény, amely mezőinicializáló rövidítést használ, mert a `username` és az `email` paraméterek neve megegyezik a struct mezőinek nevével">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Itt a `User` struct egy új példányát hozzuk létre, amelynek van egy `email` nevű
mezője. Az `email` mező értékét a `build_user` függvény `email` paraméterében
lévő értékre akarjuk beállítani. Mivel az `email` mező és az `email` paraméter
neve azonos, elég csak `email`-t írnunk az `email: email` helyett.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Példányok létrehozása struct-frissítő szintaxissal

Gyakran hasznos, ha úgy hozzuk létre egy struct új példányát, hogy az
ugyanazon típus egy másik példányának értékeit veszi át nagyrészt, de
némelyiket megváltoztatja. Ezt a struct-frissítő szintaxissal tehetjük meg.

Először az 5-6. listában megmutatjuk, hogyan hozunk létre a szokásos módon, a
frissítő szintaxis nélkül egy új `User` példányt a `user2`-ben. Az `email`-nek
új értéket adunk, egyébként pedig ugyanazokat az értékeket használjuk, amelyeket
az 5-2. listában létrehozott `user1` tartalmaz.

<Listing number="5-6" file-name="src/main.rs" caption="Egy új `User` példány létrehozása a `user1` egy kivétellel az összes értékének felhasználásával">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

A struct-frissítő szintaxissal ugyanezt kevesebb kóddal érhetjük el, ahogy azt
az 5-7. lista mutatja. A `..` szintaxis azt jelöli, hogy a többi, kifejezetten
be nem állított mező ugyanazt az értéket kapja, mint a megadott példány mezői.

<Listing number="5-7" file-name="src/main.rs" caption="Struct-frissítő szintaxis használata: új `email` érték beállítása egy `User` példányhoz, a többi érték átvétele a `user1`-től">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Az 5-7. listában szereplő kód is olyan példányt hoz létre a `user2`-ben, amely
más `email` értékkel rendelkezik, de a `username`, `active` és `sign_in_count`
mezőkben ugyanazokat az értékeket tartalmazza, mint a `user1`. A `..user1`
résznek utolsóként kell állnia, hogy jelezze: minden fennmaradó mező a `user1`
megfelelő mezőiből kapja az értékét, egyébként viszont tetszőleges számú
mezőhöz megadhatunk értéket, tetszőleges sorrendben, függetlenül a mezők
sorrendjétől a struct definíciójában.

Vedd észre, hogy a struct-frissítő szintaxis az `=` jelet értékadásként
használja; ez azért van, mert mozgatja az adatot, ahogy azt a [„Változók és
adatok kölcsönhatása: move”][move]<!-- ignore --> szakaszban láttuk. Ebben a
példában a `user2` létrehozása után már nem használhatjuk a `user1`-et, mert a
`user1` `username` mezőjében lévő `String` bemozgott a `user2`-be. Ha az
`email`-hez és a `username`-hez is új `String` értékeket adtunk volna a
`user2`-nek, és így csak az `active` és a `sign_in_count` értékeket vettük
volna át a `user1`-től, akkor a `user1` a `user2` létrehozása után is érvényes
maradna. Az `active` és a `sign_in_count` egyaránt olyan típusú, amely
implementálja a `Copy` trait-et, tehát a [„Csak a stacken lévő adatok:
Copy”][copy]<!-- ignore --> szakaszban tárgyalt viselkedés érvényesülne. A `user1.email` értéket egyébként
ebben a példában is használhatjuk továbbra is, mert az értéke nem mozgott ki a
`user1`-ből.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Különböző típusok létrehozása tuple structokkal {#creating-different-types-with-tuple-structs}

A Rust olyan structokat is támogat, amelyek a tuple-ökre hasonlítanak; ezek a
_tuple structok_. A tuple structoknak megvan az a többletjelentésük, amit a
struct neve ad, de a mezőikhez nem tartoznak nevek; csak a mezők típusait
tartalmazzák. A tuple structok akkor hasznosak, ha az egész tuple-nek nevet
akarsz adni, és a tuple-t más tuple-öktől eltérő típussá akarod tenni, illetve
amikor a mezők elnevezése – ahogy egy közönséges structban tennénk – terjengős
vagy fölösleges lenne.

Egy tuple struct definiálásához kezdd a `struct` kulcsszóval és a struct
nevével, majd sorold fel a tuple-ben szereplő típusokat. Például itt két tuple
structot definiálunk és használunk, `Color` és `Point` néven:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Vedd észre, hogy a `black` és az `origin` érték különböző típusú, mert
különböző tuple structok példányai. Minden struct, amelyet definiálsz, önálló
típus, még akkor is, ha a structon belüli mezők típusai megegyeznek. Egy olyan
függvény például, amely `Color` típusú paramétert vár, nem fogadhat el `Point`
típusú argumentumot, pedig mindkét típus három `i32` értékből áll. Ettől
eltekintve a tuple struct példányok hasonlítanak a tuple-ökre: szét lehet
bontani őket az egyes darabjaikra, és egy `.` jellel, majd az indexszel
elérheted az egyes értékeket. A tuple-öktől eltérően a tuple structok szétbontásakor meg
kell nevezned a struct típusát. Például a `let Point(x, y, z) = origin;`
kifejezést írnánk ahhoz, hogy az `origin` pont értékeit `x`, `y` és `z` nevű
változókba bontsuk szét.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Unit-szerű structok definiálása

Olyan structokat is definiálhatsz, amelyeknek egyetlen mezőjük sincs! Ezeket
_unit-szerű structoknak_ nevezzük, mert hasonlóan viselkednek a `()`
unit típushoz, amelyet a [„A tuple típus”][tuples]<!-- ignore --> szakaszban
említettünk. A unit-szerű structok akkor lehetnek hasznosak, ha valamilyen
típusra implementálnod kell egy trait-et, de nincs olyan adat, amelyet magában a
típusban akarnál tárolni. A trait-ekről a 10. fejezetben lesz szó. Íme egy példa
egy `AlwaysEqual` nevű unit struct deklarálására és példányosítására:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Az `AlwaysEqual` definiálásához a `struct` kulcsszót, a kívánt nevet, majd egy
pontosvesszőt használunk. Nincs szükség kapcsos zárójelekre vagy
zárójelpárokra! Ezután hasonló módon kaphatunk egy `AlwaysEqual` példányt a
`subject` változóba: az általunk definiált nevet írjuk le, mindenféle kapcsos
zárójel és zárójelpár nélkül. Képzeld el, hogy később olyan viselkedést
implementálunk ehhez a típushoz, amely szerint az `AlwaysEqual` minden példánya
mindig egyenlő bármely más típus minden példányával – például azért, hogy
tesztelési célokra ismert eredményünk legyen. Ennek a viselkedésnek az
implementálásához semmilyen adatra nem lenne szükségünk! A 10. fejezetben
látni fogod, hogyan definiálhatsz trait-eket, és hogyan implementálhatod őket
bármilyen típusra, köztük a unit-szerű structokra is.

> ### A struct adatainak ownershipje
>
> Az 5-1. listában szereplő `User` struct definíciójában a birtokolt `String`
> típust használtuk az `&str` string slice típus helyett. Ez tudatos döntés,
> mert azt akarjuk, hogy a struct minden példánya birtokolja az összes
> adatát, és hogy ez az adat mindaddig érvényes legyen, amíg a teljes struct
> érvényes.
>
> Lehetséges az is, hogy egy struct valami máshoz tartozó adatra mutató
> referenciákat tároljon, ehhez azonban _lifetime_-okat kell használni, ami a
> Rust egy olyan képessége, amelyről a 10. fejezetben lesz szó. A lifetime-ok
> biztosítják, hogy a struct által hivatkozott adat legalább addig érvényes
> legyen, mint maga a struct. Tegyük fel, hogy megpróbálsz egy referenciát
> tárolni egy structban lifetime-ok megadása nélkül, ahogy az alábbi kód teszi
> a *src/main.rs* fájlban; ez nem fog működni:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> A fordító panaszkodni fog, hogy lifetime-megadókra van szüksége:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> A 10. fejezetben megbeszéljük, hogyan javíthatók ezek a hibák, hogy
> referenciákat tárolhass structokban, egyelőre azonban az ilyen hibákat úgy
> javítjuk, hogy az `&str`-hez hasonló referenciák helyett a `String`-hez
> hasonló birtokolt típusokat használunk.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
