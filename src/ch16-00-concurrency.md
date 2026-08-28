# Félelem nélküli konkurencia

A konkurens programozás biztonságos és hatékony kezelése a Rust másik fő
célkitűzése. A _konkurens programozás_, amelyben egy program különböző részei
egymástól függetlenül futnak, és a _párhuzamos programozás_, amelyben egy
program különböző részei egyszerre futnak, egyre fontosabbá válnak, ahogy egyre
több számítógép használja ki a több processzorát. Történelmileg az ilyen
környezetekben való programozás nehéz volt és könnyen vezetett hibákhoz. A Rust
ezen szeretne változtatni.

Kezdetben a Rust csapata azt gondolta, hogy a memóriabiztonság garantálása és a
konkurenciából fakadó problémák megelőzése két különálló kihívás, amelyeket
eltérő módszerekkel kell megoldani. Idővel a csapat rájött, hogy az ownership-
és a típusrendszer együtt hatékony eszközkészletet ad a memóriabiztonság _és_ a
konkurencia problémáinak kezeléséhez! Az ownership és a típusellenőrzés
kihasználásával a Rustban sok konkurenciahiba fordítási idejű hibává válik
futásidejű hiba helyett. Így ahelyett, hogy rengeteg időt töltenél azoknak a
pontos körülményeknek a reprodukálásával, amelyek között egy futásidejű
konkurenciahiba előjön, a hibás kódot a fordító egyszerűen nem fogja lefordítani,
és a problémát elmagyarázó hibaüzenetet ad. Ennek eredményeként a kódot még
munka közben javíthatod, nem pedig azután, hogy már élesbe került. Ezt a
tulajdonságát a Rustnak elneveztük _félelem nélküli konkurenciának_. A félelem
nélküli konkurencia lehetővé teszi, hogy olyan kódot írj, amely mentes a rejtett
hibáktól, és könnyen refaktorálható anélkül, hogy új hibákat vinnél bele.

> Megjegyzés: az egyszerűség kedvéért sok problémára egyszerűen
> _konkurensként_ hivatkozunk, ahelyett hogy a pontosabb _konkurens és/vagy
> párhuzamos_ megfogalmazást használnánk. Ebben a fejezetben gondolatban
> helyettesítsd be a _konkurens és/vagy párhuzamos_ kifejezést mindenütt, ahol
> azt írjuk, hogy _konkurens_. A következő fejezetben, ahol a különbség
> fontosabb, pontosabban fogalmazunk majd.

Sok nyelv dogmatikus abban, milyen megoldásokat kínál a konkurens problémák
kezelésére. Az Erlangnak például elegáns eszközei vannak az üzenetküldésen
alapuló konkurenciához, viszont csak nehézkes módjai vannak az állapot szálak
közötti megosztására. A lehetséges megoldásoknak csak egy részhalmazát
támogatni észszerű stratégia a magasabb szintű nyelvek esetében, mert egy
magasabb szintű nyelv azzal kecsegtet, hogy némi kontrollról lemondva
absztrakciókat nyerünk. Az alacsonyabb szintű nyelvektől viszont elvárjuk, hogy
minden helyzetben a legjobb teljesítményt nyújtó megoldást adják, és kevesebb
absztrakciót tegyenek a hardver fölé. Ezért a Rust sokféle eszközt kínál a
problémák modellezésére, azon a módon, amely a te helyzetedhez és
követelményeidhez illik.

Ebben a fejezetben a következő témákat járjuk körül:

- Hogyan hozhatunk létre szálakat több kódrészlet egyidejű futtatásához
- Az _üzenetküldésen_ alapuló konkurencia, ahol csatornák küldenek üzeneteket a
  szálak között
- Az _osztott állapotú_ konkurencia, ahol több szál is hozzáfér ugyanahhoz az
  adathoz
- A `Sync` és `Send` trait-ek, amelyek a Rust konkurenciagaranciáit kiterjesztik
  a felhasználó által definiált típusokra is, nem csak a standard könyvtár
  típusaira
