# Haladó nyelvi elemek

Mostanra megismerted a Rust programozási nyelv leggyakrabban használt részeit.
Mielőtt a 21. fejezetben belevágnánk még egy projektbe, nézzünk meg néhány
olyan aspektusát a nyelvnek, amellyel időnként találkozhatsz, de valószínűleg
nem használod mindennap. Ezt a fejezetet referenciaként használhatod, amikor
valami ismeretlenbe ütközöl. Az itt bemutatott képességek nagyon konkrét
helyzetekben hasznosak. Bár lehet, hogy nem nyúlsz hozzájuk gyakran, szeretnénk
biztosra menni, hogy a Rust minden képességét átlátod.

Ebben a fejezetben a következőket vesszük sorra:

- Unsafe Rust: hogyan mondhatsz le a Rust egyes garanciáiról, és hogyan
  vállalhatod magadra a felelősséget azok kézi betartásáért
- Haladó trait-ek: asszociált típusok, alapértelmezett típusparaméterek,
  teljesen minősített szintaxis, supertrait-ek és a newtype minta a trait-ekhez
  kapcsolódóan
- Haladó típusok: még több a newtype mintáról, típusaliasok, a never típus és a
  dinamikusan méretezett típusok
- Haladó függvények és closure-ök: függvénypointerek és closure-ök visszaadása
- Makrók: módszerek olyan kód definiálására, amely fordítási időben további
  kódot definiál

Ez a Rust képességeinek olyan tárháza, amelyben mindenki talál valamit! Vágjunk
bele!
