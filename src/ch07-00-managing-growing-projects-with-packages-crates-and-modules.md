<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Csomagok, crate-ek és modulok

Ahogy nagyobb programokat írsz, a kódod szervezése egyre fontosabbá válik. Ha
az összetartozó funkciókat csoportosítod, és a különálló feladatokat ellátó
kódrészeket elkülöníted, világossá teszed, hol található egy adott képességet
megvalósító kód, és hová kell menned, ha meg akarod változtatni, hogyan
működik.

Az eddig írt programjaink egyetlen fájlban, egyetlen modulban voltak. Ahogy egy
projekt növekszik, érdemes úgy szervezned a kódot, hogy több modulra, majd több
fájlra bontod. Egy csomag több binary crate-et és opcionálisan egy library
crate-et tartalmazhat. Ahogy a csomag nő, egyes részeit külön crate-ekbe
emelheted ki, amelyek külső függőségekké válnak. Ez a fejezet mindezeket a
technikákat bemutatja. Nagyon nagy projektekhez, amelyek együtt fejlődő,
egymással összefüggő csomagok halmazából állnak, a Cargo workspace-eket kínál;
ezekkel a 14. fejezet [„Cargo-workspace-ek”][workspaces]<!-- ignore --> című
szakaszában foglalkozunk.

Szó lesz az implementációs részletek egységbezárásáról is, amely lehetővé teszi
a kód magasabb szintű újrafelhasználását: ha egyszer implementáltál egy
műveletet, más kód meghívhatja a kódodat a nyilvános felületén keresztül
anélkül, hogy tudnia kellene, hogyan működik az implementáció. Az, ahogyan a
kódot megírod, meghatározza, mely részei nyilvánosak más kód számára, és mely
részei olyan privát implementációs részletek, amelyek megváltoztatásának jogát
fenntartod magadnak. Ez egy újabb módja annak, hogy csökkentsd a fejben
tartandó részletek mennyiségét.

Egy kapcsolódó fogalom a hatókör: az a beágyazott környezet, amelyben a kódot
írod, rendelkezik nevek egy halmazával, amelyek „a hatókörben vannak”. Kód
olvasásakor, írásakor és fordításakor a programozóknak és a fordítóknak tudniuk
kell, hogy egy adott helyen egy adott név változóra, függvényre, struct-ra,
enumra, modulra, konstansra vagy más elemre utal-e, és hogy mit jelent az adott
elem. Létrehozhatsz hatóköröket, és megváltoztathatod, mely nevek vannak a
hatókörben, és melyek nincsenek. Ugyanabban a hatókörben nem lehet két azonos
nevű elemed; a névütközések feloldására vannak eszközök.

A Rustnak számos képessége van, amelyekkel kezelheted a kódod szervezését,
beleértve azt, hogy mely részletek nyilvánosak, mely részletek privátak, és
milyen nevek vannak az egyes hatókörökben a programjaidban. Ezek a képességek,
amelyeket néha együtt _modulrendszernek_ neveznek, a következők:

* **Csomagok**: A Cargo képessége, amellyel crate-eket építhetsz, tesztelhetsz
és oszthatsz meg
* **Crate-ek**: Modulok fája, amely könyvtárat vagy futtatható állományt hoz
létre
* **Modulok és a use**: Lehetővé teszik az útvonalak szervezésének,
hatókörének és láthatóságának szabályozását
* **Útvonalak**: Egy elem – például egy struct, függvény vagy modul –
megnevezésének módja

Ebben a fejezetben mindezeket a képességeket áttekintjük, megbeszéljük, hogyan
hatnak egymásra, és elmagyarázzuk, hogyan használd őket a hatókörök kezelésére.
A végére alaposan meg kell értened a modulrendszert, és profi módjára kell
tudnod bánni a hatókörökkel!

[workspaces]: ch14-03-cargo-workspaces.html
