# Enumok és mintaillesztés

Ebben a fejezetben a felsorolt típusokat vesszük szemügyre, amelyeket _enum_-nak
is neveznek. Az enumok lehetővé teszik, hogy egy típust a lehetséges
változatainak felsorolásával definiálj. Először definiálunk és használunk egy
enumot, hogy megmutassuk, hogyan képes az enum az adatok mellett jelentést is
hordozni. Ezután megismerkedünk egy különösen hasznos enummal, az `Option`-nel,
amely azt fejezi ki, hogy egy érték lehet valami, de lehet semmi is. Utána
megnézzük, hogyan teszi könnyűvé a `match` kifejezésben végzett mintaillesztés,
hogy egy enum különböző értékeire különböző kód fusson. Végül szó lesz arról,
hogy az `if let` szerkezet egy másik kényelmes és tömör idióma, amellyel
enumokat kezelhetsz a kódodban.
