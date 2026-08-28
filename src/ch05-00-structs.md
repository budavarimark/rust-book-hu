# Struktok használata összetartozó adatok strukturálására

A _struct_ – vagyis _struktúra_ – egy olyan egyéni adattípus, amellyel több
összetartozó, egy értelmes csoportot alkotó értéket csomagolhatsz össze és
nevezhetsz el. Ha ismersz valamilyen objektumorientált nyelvet, a struct
nagyjából olyan, mint egy objektum adatattribútumai. Ebben a fejezetben
összehasonlítjuk a tuple-öket és a structokat, hogy építsünk arra, amit már
tudsz, és megmutassuk, mikor jobb módja a structok használata az adatok
csoportosításának.

Bemutatjuk, hogyan definiálhatsz és példányosíthatsz structokat. Szó lesz
arról, hogyan definiálhatunk asszociált függvényeket – különösen a _metódusok_
nevű asszociált függvényeket –, amelyekkel egy struct típushoz kapcsolódó
viselkedést adhatunk meg. A structok és az enumok (amelyekről a 6. fejezetben
lesz szó) az alapkövei annak, hogy a programod fogalomkörében új típusokat hozz
létre, és teljes mértékben kihasználd a Rust fordítási idejű
típusellenőrzését.
