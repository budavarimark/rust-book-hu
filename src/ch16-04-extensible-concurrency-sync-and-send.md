<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Bővíthető konkurencia a `Send` és `Sync` trait-ekkel

Érdekes módon szinte minden konkurenciával kapcsolatos képesség, amiről eddig
ebben a fejezetben szó volt, a standard könyvtár része, nem a nyelvé. A
konkurencia kezelésére nem korlátoznak téged a nyelv vagy a standard könyvtár
lehetőségei; írhatsz saját konkurenciaeszközöket, vagy használhatod a mások által
írtakat.

A kulcsfontosságú konkurenciafogalmak közül azonban a nyelvbe – és nem a
standard könyvtárba – van beépítve a `std::marker` `Send` és `Sync` trait-je.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Ownership átadása szálak között

A `Send` jelölő trait azt jelzi, hogy a `Send`-et implementáló típus értékeinek
ownershipje átadható szálak között. Szinte minden Rust típus implementálja a
`Send`-et, de van néhány kivétel, például az `Rc<T>`: ez nem implementálhatja a
`Send`-et, mert ha klónoznál egy `Rc<T>` értéket, és megpróbálnád a klón
ownershipjét egy másik szálnak átadni, mindkét szál egyszerre frissíthetné a
referenciaszámlálót. Ezért az `Rc<T>` egyszálú helyzetekben való használatra
készült, ahol nem akarod megfizetni a szálbiztonság teljesítménybeli árát.

Ezért a Rust típusrendszere és a trait bound-ok gondoskodnak arról, hogy soha ne
küldhess véletlenül egy `Rc<T>` értéket nem biztonságos módon szálak között.
Amikor a 16-14. listában ezzel próbálkoztunk, ezt a hibát kaptuk: `` the trait
`Send` is not implemented for `Rc<Mutex<i32>>` ``. Amikor átváltottunk az
`Arc<T>`-re, amely implementálja a `Send`-et, a kód lefordult.

Minden olyan típus, amely teljes egészében `Send` típusokból áll, automatikusan
szintén `Send`-nek minősül. Szinte minden primitív típus `Send`, kivéve a nyers
pointereket, amelyekről a 20. fejezetben lesz szó.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Hozzáférés több szálról

A `Sync` jelölő trait azt jelzi, hogy a `Sync`-et implementáló típusra
biztonságos több szálról is hivatkozni. Más szóval bármely `T` típus
implementálja a `Sync`-et, ha a `&T` (egy `T`-re mutató nem módosítható
referencia) implementálja a `Send`-et, vagyis ha a referenciát biztonságosan el
lehet küldeni egy másik szálnak. A `Send`-hez hasonlóan a primitív típusok mind
implementálják a `Sync`-et, és azok a típusok is implementálják, amelyek teljes
egészében `Sync`-et implementáló típusokból állnak.

Az `Rc<T>` smart pointer ugyanazokból az okokból nem implementálja a `Sync`-et
sem, amiért a `Send`-et sem. A `RefCell<T>` típus (amelyről a 15. fejezetben
volt szó) és a hozzá kapcsolódó `Cell<T>` típuscsalád szintén nem implementálja
a `Sync`-et. A borrow checking azon implementációja, amelyet a `RefCell<T>`
futásidőben végez, nem szálbiztos. A `Mutex<T>` smart pointer implementálja a
`Sync`-et, és használható arra, hogy több szállal osszunk meg hozzáférést,
ahogy azt az [„Osztott hozzáférés a `Mutex<T>`-hez”][shared-access]<!-- ignore
--> részben láttad.

### A `Send` és `Sync` kézi implementálása unsafe

Mivel azok a típusok, amelyek teljes egészében a `Send` és `Sync` trait-eket
implementáló más típusokból állnak, automatikusan szintén implementálják a
`Send`-et és a `Sync`-et, ezeket a trait-eket nem kell kézzel implementálnunk.
Jelölő trait-ek lévén még metódusaik sincsenek, amelyeket implementálni kellene.
Egyszerűen csak hasznosak a konkurenciával kapcsolatos invariánsok
betartatásában.

Ezen trait-ek kézi implementálása unsafe Rust kód írásával jár. Az unsafe Rust
kód használatáról a 20. fejezetben lesz szó; egyelőre az a fontos információ,
hogy olyan új konkurens típusok építése, amelyek nem `Send` és `Sync` részekből
állnak, alapos átgondolást igényel a biztonsági garanciák betartásához. [„The
Rustonomicon”][nomicon] további információt tartalmaz ezekről a garanciákról és
arról, hogyan tarthatók be.

## Összefoglalás

Nem ez az utolsó alkalom, hogy konkurenciával találkozol ebben a könyvben: a
következő fejezet az async programozásra összpontosít, a 21. fejezet projektje
pedig az itt tárgyalt kisebb példáknál valósághűbb helyzetben használja majd az
ebben a fejezetben megismert fogalmakat.

Ahogy korábban említettük, mivel a Rust konkurenciakezeléséből nagyon kevés
része a nyelvnek, sok konkurenciamegoldás crate-ként van implementálva. Ezek
gyorsabban fejlődnek, mint a standard könyvtár, ezért mindenképpen keress rá az
interneten a legfrissebb, korszerű crate-ekre, amelyeket többszálú helyzetekben
használhatsz.

A Rust standard könyvtára csatornákat kínál az üzenetküldéshez, valamint olyan
smart pointer típusokat, mint a `Mutex<T>` és az `Arc<T>`, amelyek konkurens
környezetben is biztonságosan használhatók. A típusrendszer és a borrow checker
gondoskodik arról, hogy az ezeket a megoldásokat használó kódban ne alakuljanak
ki adatversenyek vagy érvénytelen referenciák. Ha egyszer sikerül lefordítanod a
kódodat, nyugodt lehetsz afelől, hogy vidáman fog futni több szálon anélkül,
hogy a más nyelvekben megszokott, nehezen felderíthető hibák jelentkeznének. A
konkurens programozás többé nem olyan fogalom, amelytől félni kell: rajta, tedd
a programjaidat konkurenssé, félelem nélkül!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html
