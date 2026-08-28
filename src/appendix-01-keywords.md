## A függelék: Kulcsszavak

Az alábbi listák azokat a kulcsszavakat tartalmazzák, amelyeket a Rust nyelv
jelenlegi vagy jövőbeli használatra fenntart. Ezért nem használhatók
azonosítóként (kivéve nyers azonosítóként, ahogy azt a [„Nyers
azonosítók”][raw-identifiers]<!-- ignore --> szakaszban tárgyaljuk). Az
_azonosítók_ függvények, változók, paraméterek, struct-mezők, modulok, crate-ek,
konstansok, makrók, statikus értékek, attribútumok, típusok, trait-ek vagy
lifetime-ok nevei.

[raw-identifiers]: #raw-identifiers

### Jelenleg használatban lévő kulcsszavak

Az alábbi lista a jelenleg használatban lévő kulcsszavakat sorolja fel, a
funkciójuk leírásával együtt.

- **`as`**: Primitív típuskonverzió végrehajtása, az adott elemet tartalmazó
  konkrét trait egyértelműsítése, vagy elemek átnevezése `use` utasításokban.
- **`async`**: `Future`-t ad vissza ahelyett, hogy blokkolná az aktuális szálat.
- **`await`**: Felfüggeszti a végrehajtást, amíg egy `Future` eredménye el nem
  készül.
- **`break`**: Azonnali kilépés egy ciklusból.
- **`const`**: Konstans elemek vagy konstans nyers pointerek definiálása.
- **`continue`**: Továbblépés a következő ciklusiterációra.
- **`crate`**: Modulútvonalban a crate gyökerére hivatkozik.
- **`dyn`**: Dinamikus dispatch egy trait objecthez.
- **`else`**: Tartalék ág az `if` és az `if let` vezérlési szerkezetekhez.
- **`enum`**: Felsorolás definiálása.
- **`extern`**: Külső függvény vagy változó linkelése.
- **`false`**: Logikai hamis literál.
- **`fn`**: Függvény vagy függvénypointer-típus definiálása.
- **`for`**: Iteráció egy iterátor elemein, trait implementálása, vagy magasabb
  rendű lifetime megadása.
- **`if`**: Elágazás egy feltételes kifejezés eredménye alapján.
- **`impl`**: Inherens vagy trait-funkcionalitás implementálása.
- **`in`**: A `for` ciklus szintaxisának része.
- **`let`**: Változó kötése.
- **`loop`**: Feltétel nélküli ciklus.
- **`match`**: Egy érték illesztése mintákra.
- **`mod`**: Modul definiálása.
- **`move`**: Ráveszi a closure-t, hogy vegye át az összes elkapott érték
  ownership-jét.
- **`mut`**: Módosíthatóságot jelöl referenciákban, nyers pointerekben vagy
  mintakötésekben.
- **`pub`**: Publikus láthatóságot jelöl struct-mezőkben, `impl` blokkokban vagy
  modulokban.
- **`ref`**: Kötés referencia szerint.
- **`return`**: Visszatérés függvényből.
- **`Self`**: Típusalias az éppen definiált vagy implementált típusra.
- **`self`**: A metódus alanya vagy az aktuális modul.
- **`static`**: Globális változó vagy a teljes programfutás alatt tartó
  lifetime.
- **`struct`**: Struktúra definiálása.
- **`super`**: Az aktuális modul szülőmodulja.
- **`trait`**: Trait definiálása.
- **`true`**: Logikai igaz literál.
- **`type`**: Típusalias vagy asszociált típus definiálása.
- **`union`**: [Union][union]<!-- ignore --> definiálása; csak union-deklarációban
  használva kulcsszó.
- **`unsafe`**: Unsafe kódot, függvényeket, trait-eket vagy implementációkat
  jelöl.
- **`use`**: Szimbólumok behozatala a hatókörbe.
- **`where`**: Egy típust megszorító kikötéseket jelöl.
- **`while`**: Feltételes ciklus egy kifejezés eredménye alapján.

[union]: ../reference/items/unions.html

### Jövőbeli használatra fenntartott kulcsszavak

Az alábbi kulcsszavaknak még nincs semmilyen funkciójuk, de a Rust fenntartja
őket lehetséges jövőbeli használatra:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Nyers azonosítók {#raw-identifiers}

A _nyers azonosítók_ (raw identifiers) azt a szintaxist jelentik, amellyel olyan
helyeken is használhatsz kulcsszavakat, ahol azok általában nem lennének
megengedettek. Nyers azonosítót úgy használsz, hogy a kulcsszó elé `r#`-t
írsz.

Például a `match` kulcsszó. Ha megpróbálod lefordítani az alábbi függvényt,
amely a `match`-et használja névként:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

ezt a hibát kapod:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

A hiba azt mutatja, hogy a `match` kulcsszót nem használhatod
függvényazonosítóként. Ahhoz, hogy a `match`-et függvénynévként használd, a nyers
azonosító szintaxisára van szükséged, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Ez a kód hibák nélkül lefordul. Figyeld meg az `r#` előtagot a függvény nevén
mind a definíciójában, mind ott, ahol a `main`-ben meghívjuk a függvényt.

A nyers azonosítók lehetővé teszik, hogy bármely általad választott szót
azonosítóként használj, még akkor is, ha az a szó éppen egy fenntartott
kulcsszó. Ez nagyobb szabadságot ad az azonosítónevek megválasztásában, és
lehetővé teszi olyan nyelveken írt programokkal való integrációt is, ahol ezek a
szavak nem kulcsszavak. Ráadásul a nyers azonosítókkal olyan könyvtárakat is
használhatsz, amelyek más Rust editionben íródtak, mint amit a te crate-ed
használ. Például a `try` nem kulcsszó a 2015-ös editionben, viszont az a 2018-as,
a 2021-es és a 2024-es editionben. Ha egy olyan könyvtártól függsz, amely a
2015-ös editionnel készült, és van benne egy `try` függvény, a nyers azonosító
szintaxisát – ebben az esetben az `r#try`-t – kell használnod ahhoz, hogy a
későbbi editionöket használó kódodból meghívd azt a függvényt. Az editionökről
bővebben az [E függelékben][appendix-e]<!-- ignore --> olvashatsz.

[appendix-e]: appendix-05-editions.html
