# Gyakori kollekciók

A Rust standard könyvtára számos nagyon hasznos adatszerkezetet tartalmaz,
ezeket _kollekcióknak_ nevezzük. A legtöbb más adattípus egyetlen konkrét
értéket képvisel, a kollekciók viszont több értéket is tárolhatnak. A beépített
tömb- és tuple-típusokkal ellentétben az adatok, amelyekre ezek a kollekciók
mutatnak, a heap-en tárolódnak, ami azt jelenti, hogy az adatok mennyiségének
nem kell fordítási időben ismertnek lennie, és a program futása közben nőhet
vagy csökkenhet. Minden kollekciófajtának más a képessége és más a költsége, és
az adott helyzethez illő kiválasztása olyan készség, amelyet idővel sajátítasz
el. Ebben a fejezetben három olyan kollekciót tárgyalunk, amelyeket nagyon
gyakran használnak a Rust-programokban:

- A _vektor_ változó számú érték egymás melletti tárolását teszi lehetővé.
- A _string_ karakterek kollekciója. A `String` típust korábban már említettük,
  de ebben a fejezetben részletesen is szó lesz róla.
- A _hash map_ segítségével egy értéket egy adott kulcshoz társíthatsz. Ez az
  általánosabb, _map_ nevű adatszerkezet egy konkrét implementációja.

A standard könyvtár által kínált többi kollekciófajtáról
[a dokumentációban][collections] olvashatsz.

Megnézzük, hogyan hozhatunk létre és frissíthetünk vektorokat, stringeket és
hash mapeket, és azt is, mi teszi különlegessé mindegyiket.

[collections]: ../std/collections/index.html
