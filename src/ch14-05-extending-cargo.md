## A Cargo kiterjesztése egyedi parancsokkal

A Cargót úgy tervezték, hogy új alparancsokkal bővíthesd anélkül, hogy magát a
Cargót módosítanod kellene. Ha a `$PATH` változódban van egy `cargo-valami` nevű
bináris, akkor a `cargo valami` paranccsal úgy futtathatod, mintha Cargo-alparancs
volna. Az ilyen egyedi parancsok a `cargo --list` futtatásakor is megjelennek a
listában. A Cargo felépítésének rendkívül kényelmes előnye, hogy a `cargo
install` paranccsal telepíthetsz kiterjesztéseket, majd ugyanúgy futtathatod
őket, mint a beépített Cargo-eszközöket!

## Összefoglalás

A kódmegosztás a Cargóval és a [crates.io](https://crates.io/)<!-- ignore -->
oldallal része annak, ami a Rust ökoszisztémáját sokféle feladatra hasznossá
teszi. A Rust standard könyvtára kicsi és stabil, a crate-eket viszont könnyű
megosztani, használni és a nyelvétől eltérő ütemben továbbfejleszteni. Ne
szégyellj megosztani a [crates.io](https://crates.io/)<!-- ignore
--> oldalon olyan kódot, amelyet hasznosnak találsz; jó eséllyel másnak is
hasznos lesz!
