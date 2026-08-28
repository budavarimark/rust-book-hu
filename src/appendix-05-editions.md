## E függelék: Editionök

Az 1. fejezetben láttad, hogy a `cargo new` egy kevés metaadatot ad a
_Cargo.toml_ fájlodhoz egy editionről. Ez a függelék arról szól, mit is jelent
ez!

A Rust nyelvnek és fordítónak hathetes kiadási ciklusa van, vagyis a
felhasználók folyamatosan kapják az új nyelvi elemeket. Más programozási nyelvek
nagyobb változásokat adnak ki ritkábban; a Rust kisebb frissítéseket ad ki
gyakrabban. Egy idő után ezek az apró változások összeadódnak. Kiadásról
kiadásra azonban nehéz visszatekinteni és azt mondani: „Nahát, a Rust 1.10 és a
Rust 1.31 között a Rust sokat változott!”

Nagyjából háromévente a Rust csapata új Rust _editiont_ állít elő. Minden
edition egy áttekinthető csomagba fogja össze a beérkezett újításokat, teljesen
frissített dokumentációval és eszközkészlettel. Az új editionök a szokásos
hathetes kiadási folyamat részeként érkeznek.

Az editionök különböző emberek számára különböző célt szolgálnak:

- Az aktív Rust-felhasználók számára az új edition könnyen érthető csomagba
  gyűjti az apránként érkező változásokat.
- Azok számára, akik nem használják a nyelvet, az új edition azt jelzi, hogy
  jelentős előrelépések történtek, ami miatt érdemes lehet újra megnézni a
  Rustot.
- Azok számára, akik a Rustot fejlesztik, az új edition gyülekezőpontot ad az
  egész projekt számára.

E sorok írásakor négy Rust edition érhető el: a Rust 2015, a Rust 2018, a Rust
2021 és a Rust 2024. Ez a könyv a Rust 2024 edition idiómáit használva íródott.

A _Cargo.toml_ fájlban az `edition` kulcs jelzi, hogy a fordító melyik editiont
használja a kódodhoz. Ha a kulcs nem létezik, a Rust visszafelé kompatibilitási
okokból a `2015`-öt használja edition értékként.

Minden projekt dönthet úgy, hogy az alapértelmezett 2015-ös editiontől eltérőt
használ. Az editionök tartalmazhatnak inkompatibilis változásokat, például egy
olyan új kulcsszót, amely ütközik a kódban lévő azonosítókkal. Hacsak nem
választod kifejezetten ezeket a változásokat, a kódod továbbra is lefordul akkor
is, amikor frissíted az általad használt Rust fordító verzióját.

Minden Rust fordítóverzió támogatja az összes olyan editiont, amely a fordító
kiadása előtt létezett, és képes bármely támogatott edition crate-jeit
összelinkelni. Az edition változásai csak azt befolyásolják, ahogy a fordító
kezdetben elemzi a kódot. Ezért ha te a Rust 2015-öt használod, és az egyik
függőséged a Rust 2018-at, a projekted lefordul, és használni tudja azt a
függőséget. A fordított helyzet is működik, amikor a projekted a Rust 2018-at, a
függőség pedig a Rust 2015-öt használja.

Hogy világos legyen: a legtöbb nyelvi elem minden editionben elérhető lesz.
Bármelyik Rust editiont használó fejlesztők továbbra is látni fogják a
fejlesztéseket, ahogy az új stabil kiadások megjelennek. Bizonyos esetekben
azonban – főként amikor új kulcsszavak kerülnek be – néhány új képesség csak a
későbbi editionökben lesz elérhető. Editiont kell váltanod, ha ki akarod
használni az ilyen újításokat.

További részletekért lásd a [_The Rust Edition Guide_][edition-guide] című
kiadványt. Ez egy teljes könyv, amely számba veszi az editionök közti
különbségeket, és elmagyarázza, hogyan frissítheted automatikusan a kódodat egy
új editionre a `cargo fix` segítségével.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
