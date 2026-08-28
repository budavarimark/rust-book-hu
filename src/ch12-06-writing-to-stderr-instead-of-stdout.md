<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Hibák átirányítása a standard hibakimenetre

Pillanatnyilag a `println!` makróval írjuk ki az összes kimenetünket a
terminálra. A legtöbb terminálban kétféle kimenet van: a _standard kimenet_
(`stdout`) az általános információknak, és a _standard hibakimenet_ (`stderr`)
a hibaüzeneteknek. Ez a megkülönböztetés lehetővé teszi, hogy a felhasználók
egy program sikeres kimenetét fájlba irányítsák, a hibaüzeneteket viszont
továbbra is a képernyőn lássák.

A `println!` makró csak a standard kimenetre tud írni, ezért valami mást kell
használnunk, ha a standard hibakimenetre akarunk írni.

### Annak ellenőrzése, hová íródnak a hibák

Először figyeljük meg, hogy a `minigrep` által kiírt tartalom jelenleg a
standard kimenetre íródik, beleértve azokat a hibaüzeneteket is, amelyeket
inkább a standard hibakimenetre szeretnénk írni. Ezt úgy tesszük meg, hogy a
standard kimenet streamjét egy fájlba irányítjuk, miközben szándékosan hibát
okozunk. A standard hibakimenet streamjét nem irányítjuk át, így a standard
hibakimenetre küldött tartalom továbbra is a képernyőn jelenik meg.

A parancssori programoktól elvárás, hogy a hibaüzeneteket a standard
hibakimenet streamjére küldjék, hogy a hibaüzeneteket akkor is lássuk a
képernyőn, ha a standard kimenet streamjét fájlba irányítjuk. A programunk
jelenleg nem viselkedik jól: mindjárt látni fogjuk, hogy a hibaüzenet kimenetét
is a fájlba menti!

Ennek a viselkedésnek a bemutatásához a programot a `>` jellel és azzal a
fájlútvonallal futtatjuk, amelyre a standard kimenet streamjét irányítani
akarjuk: _output.txt_. Nem adunk át semmilyen argumentumot, ami hibát kell hogy
okozzon:

```console
$ cargo run > output.txt
```

A `>` szintaxis azt mondja a shellnek, hogy a standard kimenet tartalmát a
képernyő helyett az _output.txt_ fájlba írja. A várt hibaüzenetet nem láttuk a
képernyőn, ami azt jelenti, hogy a fájlban kellett kikötnie. Ez az, amit az
_output.txt_ tartalmaz:

```text
Problem parsing arguments: not enough arguments
```

Bizony, a hibaüzenetünk a standard kimenetre íródik. Az ilyen hibaüzenetek
sokkal hasznosabbak, ha a standard hibakimenetre íródnak, hogy a fájlban csak a
sikeres futás adatai kössenek ki. Ezen fogunk változtatni.

### Hibák kiírása a standard hibakimenetre

A 12-24. listában szereplő kóddal változtatjuk meg a hibaüzenetek kiírásának
módját. A fejezet korábbi részében elvégzett refaktorálásnak köszönhetően
minden hibaüzenetet kiíró kód egyetlen függvényben, a `main`-ben van. A
standard könyvtár biztosítja az `eprintln!` makrót, amely a standard hibakimenet
streamjére ír, úgyhogy változtassuk meg azt a két helyet, ahol a hibák
kiírásához `println!`-t hívtunk, hogy helyette `eprintln!`-t használjanak.

<Listing number="12-24" file-name="src/main.rs" caption="Hibaüzenetek írása a standard hibakimenetre a standard kimenet helyett az `eprintln!` makróval">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Most futtassuk le újra a programot ugyanígy, argumentumok nélkül, a standard
kimenetet pedig a `>` jellel átirányítva:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Most már látjuk a hibát a képernyőn, és az _output.txt_ semmit nem tartalmaz;
ez az a viselkedés, amit a parancssori programoktól elvárunk.

Futtassuk le újra a programot olyan argumentumokkal, amelyek nem okoznak hibát,
de a standard kimenetet továbbra is fájlba irányítjuk, így:

```console
$ cargo run -- to poem.txt > output.txt
```

Semmilyen kimenetet nem fogunk látni a terminálon, az _output.txt_ pedig az
eredményeinket fogja tartalmazni:

<span class="filename">Fájlnév: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Ez azt mutatja, hogy mostantól a standard kimenetet a sikeres kimenetre, a
standard hibakimenetet pedig a hibakimenetre használjuk, ahogy illik.

## Összefoglalás

Ez a fejezet felelevenített néhányat az eddig tanult fontosabb fogalmak közül,
és bemutatta, hogyan lehet gyakori I/O-műveleteket végezni Rustban. A
parancssori argumentumok, a fájlok, a környezeti változók és a hibák kiírására
szolgáló `eprintln!` makró használatával mostantól felkészült vagy parancssori
alkalmazások írására. A korábbi fejezetek fogalmaival kombinálva a kódod jól
szervezett lesz, hatékonyan tárolja majd az adatokat a megfelelő
adatszerkezetekben, szépen kezeli a hibákat, és jól tesztelt lesz.

Ezután megismerünk néhány olyan Rust-képességet, amelyre a funkcionális nyelvek
hatottak: a closure-öket és az iterátorokat.
