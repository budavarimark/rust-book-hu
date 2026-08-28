# Smart pointerek

A pointer általános fogalom egy olyan változóra, amely egy memóriacímet
tartalmaz. Ez a cím valamilyen más adatra hivatkozik, azaz „rámutat”. A Rustban
a leggyakoribb pointerfajta a referencia, amelyről a 4. fejezetben tanultál. A
referenciákat a `&` jel jelöli, és borrowolják azt az értéket, amelyre mutatnak.
Az adatokra való hivatkozáson kívül semmilyen különleges képességük nincs, és
nem járnak többletköltséggel.

A _smart pointerek_ ezzel szemben olyan adatszerkezetek, amelyek pointerként
viselkednek, de emellett további metaadatokkal és képességekkel is
rendelkeznek. A smart pointerek fogalma nem a Rust sajátja: a smart pointerek a
C++-ból erednek, és más nyelvekben is léteznek. A Rust standard könyvtárában
sokféle smart pointer található, amelyek a referenciákon túlmutató
funkcionalitást nyújtanak. Az általános fogalom feltérképezéséhez több
különböző példát is megnézünk smart pointerekre, köztük egy _referenciaszámláló_
smart pointer típust. Ez a pointer lehetővé teszi, hogy egy adatnak több ownere
legyen: nyilvántartja az ownerek számát, és amikor egy owner sem marad,
felszabadítja az adatot.

A Rustban, ahol az ownership és a borrowing fogalma is jelen van, van még egy
különbség a referenciák és a smart pointerek között: míg a referenciák csak
borrowolják az adatot, a smart pointerek sok esetben _birtokolják_ azt az
adatot, amelyre mutatnak.

A smart pointereket általában structokkal implementálják. A hétköznapi
structokkal ellentétben a smart pointerek implementálják a `Deref` és a `Drop`
trait-et. A `Deref` trait lehetővé teszi, hogy a smart pointer struct egy
példánya referenciaként viselkedjen, így a kódodat úgy írhatod meg, hogy
referenciákkal és smart pointerekkel egyaránt működjön. A `Drop` trait
segítségével testre szabhatod azt a kódot, amely akkor fut le, amikor a smart
pointer egy példánya kilép a hatóköréből. Ebben a fejezetben mindkét trait-ről
szó lesz, és bemutatjuk, miért fontosak a smart pointerek szempontjából.

Mivel a smart pointer minta egy általános, a Rustban gyakran használt
tervezési minta, ez a fejezet nem tud minden létező smart pointerre kitérni.
Sok könyvtárnak megvan a saját smart pointere, sőt, te magad is írhatsz ilyet.
A standard könyvtár leggyakoribb smart pointereivel foglalkozunk:

- `Box<T>`, értékek lefoglalásához a heapen
- `Rc<T>`, egy referenciaszámláló típus, amely többszörös ownershipet tesz
  lehetővé
- `Ref<T>` és `RefMut<T>`, amelyeket a `RefCell<T>` típuson keresztül érünk el,
  és amely a borrowing szabályait futásidőben érvényesíti fordítási idő helyett

Ezenfelül szó lesz az _interior mutability_ mintáról, ahol egy nem módosítható
típus olyan API-t tesz elérhetővé, amellyel egy belső érték módosítható.
Kitérünk a referenciaciklusokra is: hogyan okozhatnak memóriaszivárgást, és
hogyan előzhetők meg.

Vágjunk bele!
