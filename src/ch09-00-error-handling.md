# Hibakezelés

A hibák a szoftverfejlesztés velejárói, ezért a Rust számos képességgel
rendelkezik a hibás helyzetek kezelésére. A Rust sok esetben megköveteli, hogy
elismerd egy hiba lehetőségét, és tegyél is valamit ellene, mielőtt a kódod
lefordulna. Ez a követelmény robusztusabbá teszi a programodat azáltal, hogy
biztosítja: még azelőtt felfedezed és megfelelően kezeled a hibákat, hogy éles
környezetbe telepítenéd a kódot!

A Rust két nagy kategóriába sorolja a hibákat: helyrehozható és helyrehozhatatlan
hibákra. Egy _helyrehozható hiba_ (recoverable error) esetén – ilyen például a
_fájl nem található_ hiba – jó eséllyel csak jelenteni akarjuk a problémát a
felhasználónak, és újra megpróbálni a műveletet. A _helyrehozhatatlan hibák_
(unrecoverable errors) mindig hibás kódra utalnak, mint például egy tömb végén
túli helyre való hivatkozás, ezért ilyenkor azonnal le akarjuk állítani a
programot.

A legtöbb nyelv nem tesz különbséget a hibák e két fajtája között, és mindkettőt
ugyanúgy kezeli, például kivételekkel. A Rustban nincsenek kivételek. Helyettük a
`Result<T, E>` típus áll rendelkezésre a helyrehozható hibákhoz, valamint a
`panic!` makró, amely leállítja a végrehajtást, ha a program helyrehozhatatlan
hibába ütközik. Ebben a fejezetben előbb a `panic!` hívásáról lesz szó, majd a
`Result<T, E>` értékek visszaadásáról. Emellett megvizsgáljuk azokat a
szempontokat is, amelyek alapján eldöntheted, hogy megpróbálkozz-e egy hibából
való felépüléssel, vagy inkább állítsd le a végrehajtást.
