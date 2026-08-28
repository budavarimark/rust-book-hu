# Egy I/O-projekt: parancssori program készítése

Ez a fejezet összefoglalja az eddig megtanult készségeket, és bemutat néhány
további képességet a standard könyvtárból. Készítünk egy parancssori eszközt,
amely fájlokkal és a parancssori be- és kimenettel dolgozik, hogy gyakoroljuk
azokat a Rust-fogalmakat, amelyek már a birtokodban vannak.

A Rust sebessége, biztonságossága, az egyetlen binárisból álló kimenete és a
platformfüggetlen támogatása ideális nyelvvé teszi parancssori eszközök
készítéséhez, ezért a projektünkben elkészítjük a klasszikus `grep` parancssori
keresőeszköz saját változatát (**g**lobally search a **r**egular **e**xpression
and **p**rint, azaz „keress globálisan egy reguláris kifejezést, és írasd ki”).
A legegyszerűbb használati esetben a `grep` egy megadott karakterláncot keres
egy megadott fájlban. Ehhez a `grep` egy fájlútvonalat és egy karakterláncot vár
argumentumként. Ezután beolvassa a fájlt, megkeresi benne azokat a sorokat,
amelyek tartalmazzák a karakterlánc-argumentumot, és kiírja ezeket a sorokat.

Közben megmutatjuk, hogyan használhatja a parancssori eszközünk azokat a
terminálképességeket, amelyeket sok más parancssori eszköz is használ.
Beolvassuk egy környezeti változó értékét, hogy a felhasználó beállíthassa az
eszközünk viselkedését. A hibaüzeneteket pedig a szabványos hibakimenetre
(`stderr`) írjuk ki a szabványos kimenet (`stdout`) helyett, hogy a felhasználó
például egy fájlba irányíthassa át a sikeres kimenetet, miközben a
hibaüzeneteket továbbra is látja a képernyőn.

A Rust közösségének egyik tagja, Andrew Gallant már elkészítette a `grep` teljes
értékű, nagyon gyors változatát `ripgrep` néven. Ehhez képest a mi változatunk
meglehetősen egyszerű lesz, de ez a fejezet megadja azt a háttértudást, amelyre
szükséged van egy olyan valós projekt megértéséhez, mint a `ripgrep`.

A `grep`-projektünk számos olyan fogalmat kapcsol össze, amelyet eddig
megtanultál:

- A kód szervezése ([7. fejezet][ch7]<!-- ignore -->)
- Vektorok és karakterláncok használata ([8. fejezet][ch8]<!-- ignore -->)
- Hibakezelés ([9. fejezet][ch9]<!-- ignore -->)
- Trait-ek és lifetime-ok használata ott, ahol helyénvaló ([10. fejezet][ch10]<!-- ignore -->)
- Tesztek írása ([11. fejezet][ch11]<!-- ignore -->)

Röviden bemutatjuk a closure-öket, az iterátorokat és a trait objecteket is,
amelyeket a [13. fejezet][ch13]<!-- ignore --> és a [18.
fejezet][ch18]<!-- ignore --> tárgyal majd részletesen.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
