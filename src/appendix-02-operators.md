## B függelék: Operátorok és szimbólumok

Ez a függelék a Rust szintaxisának szótárát tartalmazza, beleértve az
operátorokat és azokat az egyéb szimbólumokat, amelyek önmagukban, illetve
útvonalak, generikusok, trait boundok, makrók, attribútumok, kommentek, tuple-ök
és zárójelek környezetében fordulnak elő.

### Operátorok

A B-1. táblázat a Rust operátorait tartalmazza, egy példát arra, hogyan jelenik
meg az operátor a kódban, egy rövid magyarázatot, valamint azt, hogy az adott
operátor túlterhelhető-e. Ha egy operátor túlterhelhető, a táblázat felsorolja a
túlterheléshez használandó trait-et.

<span class="caption">B-1. táblázat: Operátorok</span>

| Operátor                  | Példa                                                   | Magyarázat                                                                        | Túlterhelhető? |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Makrókifejtés                                                                     |                |
| `!`                       | `!expr`                                                 | Bitenkénti vagy logikai komplemens                                                | `Not`          |
| `!=`                      | `expr != expr`                                          | Nem egyenlő összehasonlítás                                                       | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Aritmetikai maradék                                                               | `Rem`          |
| `%=`                      | `var %= expr`                                           | Aritmetikai maradék és értékadás                                                  | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Borrow                                                                            |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Borrow-olt pointertípus                                                           |                |
| `&`                       | `expr & expr`                                           | Bitenkénti ÉS                                                                     | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bitenkénti ÉS és értékadás                                                        | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Rövidzáras logikai ÉS                                                             |                |
| `*`                       | `expr * expr`                                           | Aritmetikai szorzás                                                               | `Mul`          |
| `*=`                      | `var *= expr`                                           | Aritmetikai szorzás és értékadás                                                  | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereferálás                                                                       | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Nyers pointer                                                                     |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Összetett típusmegszorítás                                                        |                |
| `+`                       | `expr + expr`                                           | Aritmetikai összeadás                                                             | `Add`          |
| `+=`                      | `var += expr`                                           | Aritmetikai összeadás és értékadás                                                | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Argumentum- és elemelválasztó                                                     |                |
| `-`                       | `- expr`                                                | Aritmetikai negálás                                                               | `Neg`          |
| `-`                       | `expr - expr`                                           | Aritmetikai kivonás                                                               | `Sub`          |
| `-=`                      | `var -= expr`                                           | Aritmetikai kivonás és értékadás                                                  | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Függvény és closure visszatérési típusa                                           |                |
| `.`                       | `expr.ident`                                            | Mezőhozzáférés                                                                    |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Metódushívás                                                                      |                |
| `.`                       | `expr.0`, `expr.1` és így tovább                        | Tuple-indexelés                                                                   |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Jobbról kizáró tartományliterál                                                   | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Jobbról záró tartományliterál                                                     | `PartialOrd`   |
| `..`                      | `..expr`                                                | Struct-literál frissítő szintaxisa                                                |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | „És a többi” mintakötés                                                           |                |
| `...`                     | `expr...expr`                                           | (Elavult, helyette `..=` használandó) Mintában: záró tartományminta                |                |
| `/`                       | `expr / expr`                                           | Aritmetikai osztás                                                                | `Div`          |
| `/=`                      | `var /= expr`                                           | Aritmetikai osztás és értékadás                                                   | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Megszorítások                                                                     |                |
| `:`                       | `ident: expr`                                           | Struct-mező inicializálása                                                        |                |
| `:`                       | `'a: loop {...}`                                        | Cikluscímke                                                                       |                |
| `;`                       | `expr;`                                                 | Utasítás- és elemlezáró                                                           |                |
| `;`                       | `[...; len]`                                            | A fix méretű tömb szintaxisának része                                             |                |
| `<<`                      | `expr << expr`                                          | Balra léptetés                                                                    | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Balra léptetés és értékadás                                                       | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Kisebb mint összehasonlítás                                                       | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Kisebb vagy egyenlő összehasonlítás                                               | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Értékadás/ekvivalencia                                                            |                |
| `==`                      | `expr == expr`                                          | Egyenlőség-összehasonlítás                                                        | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | A `match`-ág szintaxisának része                                                  |                |
| `>`                       | `expr > expr`                                           | Nagyobb mint összehasonlítás                                                      | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Nagyobb vagy egyenlő összehasonlítás                                              | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Jobbra léptetés                                                                   | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Jobbra léptetés és értékadás                                                      | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Mintakötés                                                                        |                |
| `^`                       | `expr ^ expr`                                           | Bitenkénti kizáró VAGY                                                            | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitenkénti kizáró VAGY és értékadás                                               | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Mintaalternatívák                                                                 |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitenkénti VAGY                                                                   | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitenkénti VAGY és értékadás                                                      | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Rövidzáras logikai VAGY                                                           |                |
| `?`                       | `expr?`                                                 | Hibaterjesztés                                                                    |                |

### Nem operátor szimbólumok

Az alábbi táblázatok az összes olyan szimbólumot tartalmazzák, amely nem
operátorként működik; vagyis nem úgy viselkedik, mint egy függvény- vagy
metódushívás.

A B-2. táblázat azokat a szimbólumokat mutatja, amelyek önmagukban jelennek meg,
és sokféle helyen érvényesek.

<span class="caption">B-2. táblázat: Önálló szintaxis</span>

| Szimbólum                                                                       | Magyarázat                                                                          |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `'ident`                                                                        | Nevesített lifetime vagy cikluscímke                                                |
| Számjegyek, amelyeket közvetlenül `u8`, `i32`, `f64`, `usize` és így tovább követ | Adott típusú numerikus literál                                                       |
| `"..."`                                                                         | String literál                                                                      |
| `r"..."`, `r#"..."#`, `r##"..."##` és így tovább                                | Nyers string literál; az escape-karakterek nincsenek feldolgozva                     |
| `b"..."`                                                                        | Bájtstring literál; string helyett bájtokból álló tömböt hoz létre                    |
| `br"..."`, `br#"..."#`, `br##"..."##` és így tovább                             | Nyers bájtstring literál; a nyers és a bájtstring literál kombinációja                |
| `'...'`                                                                         | Karakterliterál                                                                      |
| `b'...'`                                                                        | ASCII bájtliterál                                                                    |
| <code>&vert;...&vert; expr</code>                                               | Closure                                                                              |
| `!`                                                                             | Mindig üres alsó típus (bottom type) a divergáló függvényekhez                        |
| `_`                                                                             | „Figyelmen kívül hagyott” mintakötés; egészliterálok olvashatóbbá tételére is szolgál |

A B-3. táblázat azokat a szimbólumokat mutatja, amelyek a modulhierarchián
keresztül egy elemhez vezető útvonal környezetében jelennek meg.

<span class="caption">B-3. táblázat: Útvonalakhoz kapcsolódó szintaxis</span>

| Szimbólum                               | Magyarázat                                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Névtér-útvonal                                                                                                    |
| `::path`                                | A crate gyökeréhez képesti útvonal (vagyis explicit módon abszolút útvonal)                                       |
| `self::path`                            | Az aktuális modulhoz képesti útvonal (vagyis explicit módon relatív útvonal)                                      |
| `super::path`                           | Az aktuális modul szülőjéhez képesti útvonal                                                                      |
| `type::ident`, `<type as trait>::ident` | Asszociált konstansok, függvények és típusok                                                                      |
| `<type>::...`                           | Asszociált elem olyan típushoz, amelyet nem lehet közvetlenül megnevezni (például `<&T>::...`, `<[T]>::...` stb.) |
| `trait::method(...)`                    | Metódushívás egyértelműsítése az azt definiáló trait megnevezésével                                               |
| `type::method(...)`                     | Metódushívás egyértelműsítése annak a típusnak a megnevezésével, amelyre definiálva van                           |
| `<type as trait>::method(...)`          | Metódushívás egyértelműsítése a trait és a típus megnevezésével                                                   |

A B-4. táblázat azokat a szimbólumokat mutatja, amelyek a generikus
típusparaméterek használatának környezetében jelennek meg.

<span class="caption">B-4. táblázat: Generikusok</span>

| Szimbólum                      | Magyarázat                                                                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `path<...>`                    | Egy típuson belüli generikus típus paramétereit adja meg (például `Vec<u8>`)                                                                                |
| `path::<...>`, `method::<...>` | Egy kifejezésben adja meg egy generikus típus, függvény vagy metódus paramétereit; gyakran _turbofish_ néven emlegetik (például `"42".parse::<i32>()`)       |
| `fn ident<...> ...`            | Generikus függvény definiálása                                                                                                                              |
| `struct ident<...> ...`        | Generikus struktúra definiálása                                                                                                                             |
| `enum ident<...> ...`          | Generikus felsorolás definiálása                                                                                                                            |
| `impl<...> ...`                | Generikus implementáció definiálása                                                                                                                         |
| `for<...> type`                | Magasabb rendű lifetime boundok                                                                                                                             |
| `type<ident=type>`             | Olyan generikus típus, amelyben egy vagy több asszociált típus konkrét értéket kap (például `Iterator<Item=T>`)                                              |

A B-5. táblázat azokat a szimbólumokat mutatja, amelyek a generikus
típusparaméterek trait boundokkal való megszorítása környezetében jelennek meg.

<span class="caption">B-5. táblázat: Trait bound megszorítások</span>

| Szimbólum                     | Magyarázat                                                                                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `T: U`                        | A `T` generikus paraméter olyan típusokra van megszorítva, amelyek implementálják az `U`-t                                                         |
| `T: 'a`                       | A `T` generikus típusnak túl kell élnie az `'a` lifetime-ot (vagyis a típus tranzitívan nem tartalmazhat `'a`-nál rövidebb lifetime-ú referenciát) |
| `T: 'static`                  | A `T` generikus típus a `'static`-okon kívül nem tartalmaz borrow-olt referenciát                                                                  |
| `'b: 'a`                      | A `'b` generikus lifetime-nak túl kell élnie az `'a` lifetime-ot                                                                                   |
| `T: ?Sized`                   | Megengedi, hogy a generikus típusparaméter dinamikusan méretezett típus legyen                                                                     |
| `'a + trait`, `trait + trait` | Összetett típusmegszorítás                                                                                                                        |

A B-6. táblázat azokat a szimbólumokat mutatja, amelyek makrók hívása vagy
definiálása, illetve egy elem attribútumainak megadása környezetében jelennek
meg.

<span class="caption">B-6. táblázat: Makrók és attribútumok</span>

| Szimbólum                                   | Magyarázat          |
| ------------------------------------------- | ------------------- |
| `#[meta]`                                   | Külső attribútum    |
| `#![meta]`                                  | Belső attribútum    |
| `$ident`                                    | Makróhelyettesítés  |
| `$ident:kind`                               | Makró-metaváltozó   |
| `$(...)...`                                 | Makróismétlés       |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Makróhívás          |

A B-7. táblázat a kommenteket létrehozó szimbólumokat mutatja.

<span class="caption">B-7. táblázat: Kommentek</span>

| Szimbólum  | Magyarázat                            |
| ---------- | ------------------------------------- |
| `//`       | Soros komment                         |
| `//!`      | Belső soros dokumentációs komment      |
| `///`      | Külső soros dokumentációs komment      |
| `/*...*/`  | Blokk-komment                          |
| `/*!...*/` | Belső blokk dokumentációs komment       |
| `/**...*/` | Külső blokk dokumentációs komment       |

A B-8. táblázat azokat a környezeteket mutatja, amelyekben kerek zárójelet
használunk.

<span class="caption">B-8. táblázat: Kerek zárójelek</span>

| Szimbólum                | Magyarázat                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------- |
| `()`                     | Üres tuple (más néven unit), literálként és típusként egyaránt                                          |
| `(expr)`                 | Zárójelezett kifejezés                                                                                  |
| `(expr,)`                | Egyelemű tuple-kifejezés                                                                                |
| `(type,)`                | Egyelemű tuple-típus                                                                                    |
| `(expr, ...)`            | Tuple-kifejezés                                                                                         |
| `(type, ...)`            | Tuple-típus                                                                                             |
| `expr(expr, ...)`        | Függvényhívás-kifejezés; tuple `struct`-ok és tuple `enum` variánsok inicializálására is használatos    |

A B-9. táblázat azokat a környezeteket mutatja, amelyekben kapcsos zárójelet
használunk.

<span class="caption">B-9. táblázat: Kapcsos zárójelek</span>

| Környezet    | Magyarázat        |
| ------------ | ----------------- |
| `{...}`      | Blokk-kifejezés   |
| `Type {...}` | Struct-literál    |

A B-10. táblázat azokat a környezeteket mutatja, amelyekben szögletes zárójelet
használunk.

<span class="caption">B-10. táblázat: Szögletes zárójelek</span>

| Környezet                                          | Magyarázat                                                                                                                                         |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Tömbliterál                                                                                                                                        |
| `[expr; len]`                                      | Tömbliterál, amely az `expr` `len` darab másolatát tartalmazza                                                                                     |
| `[type; len]`                                      | Tömbtípus, amely a `type` `len` darab példányát tartalmazza                                                                                        |
| `expr[expr]`                                       | Kollekció indexelése; túlterhelhető (`Index`, `IndexMut`)                                                                                          |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Kollekció indexelése, amely kollekció-slice-olásnak álcázza magát, „indexként” a `Range`, `RangeFrom`, `RangeTo` vagy `RangeFull` használatával    |
