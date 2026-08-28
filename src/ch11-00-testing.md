# Automatizált tesztek írása

Edsger W. Dijkstra 1972-es „The Humble Programmer” című esszéjében azt írta,
hogy „a programok tesztelése nagyon hatékony módja lehet annak, hogy kimutassuk
a hibák jelenlétét, de reménytelenül alkalmatlan a hiányuk bizonyítására”. Ez
nem azt jelenti, hogy ne próbálnánk meg annyit tesztelni, amennyit csak tudunk!

A programjaink _helyessége_ azt fejezi ki, hogy a kódunk mennyire azt csinálja,
amit szántunk neki. A Rustot a programok helyessége iránti nagyfokú
elkötelezettséggel tervezték, de a helyesség összetett dolog, és nem könnyű
bizonyítani. A Rust típusrendszere ennek a tehernek nagy részét leveszi a
vállunkról, de a típusrendszer nem tud mindent elkapni. Ezért a Rust
támogatást nyújt automatizált szoftvertesztek írásához.

Tegyük fel, hogy írunk egy `add_two` függvényt, amely 2-t ad hozzá bármely
számhoz, amit átadunk neki. Ennek a függvénynek a szignatúrája egy egész számot
vár paraméterként, és egy egész számot ad vissza eredményként. Amikor
implementáljuk és lefordítjuk ezt a függvényt, a Rust elvégzi az összes
típusellenőrzést és borrow-ellenőrzést, amit eddig megismertél, hogy
biztosítsa például, hogy nem adunk át `String` értéket vagy érvénytelen
referenciát ennek a függvénynek. De a Rust _nem_ tudja ellenőrizni, hogy ez a
függvény pontosan azt fogja-e csinálni, amit szánunk neki, vagyis a paraméter
plusz 2-t adja-e vissza, és nem mondjuk a paraméter plusz 10-et vagy a
paraméter mínusz 50-et! Itt jönnek képbe a tesztek.

Írhatunk olyan teszteket, amelyek például azt állítják, hogy amikor `3`-at
adunk át az `add_two` függvénynek, a visszakapott érték `5`. Ezeket a teszteket
lefuttathatjuk minden alkalommal, amikor módosítjuk a kódunkat, hogy
megbizonyosodjunk róla: a már meglévő helyes viselkedés nem változott meg.

A tesztelés összetett készség: bár egyetlen fejezetben nem tudunk kitérni a jó
tesztek írásának minden részletére, ebben a fejezetben a Rust tesztelési
eszközeinek működését tárgyaljuk. Szó lesz azokról az annotációkról és
makrókról, amelyek a tesztek írásakor rendelkezésedre állnak, a tesztek
futtatásának alapértelmezett viselkedéséről és a hozzá tartozó opciókról,
valamint arról, hogyan szervezzük a teszteket egységtesztekbe és integrációs
tesztekbe.
