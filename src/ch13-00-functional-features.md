# Funkcionális nyelvi elemek: iterátorok és closure-ök

A Rust tervezése sok létező nyelvből és technikából merített ihletet, és az
egyik jelentős hatás a _funkcionális programozás_. A funkcionális stílusú
programozásban gyakran előfordul, hogy a függvényeket értékként használjuk:
argumentumban adjuk át őket, más függvényekből adjuk vissza őket, változókhoz
rendeljük őket későbbi végrehajtás céljából, és így tovább.

Ebben a fejezetben nem vitatkozunk azon, mi funkcionális programozás és mi nem,
hanem inkább a Rust néhány olyan képességét beszéljük meg, amelyek hasonlítanak
sok, gyakran funkcionálisnak nevezett nyelv képességeihez.

Pontosabban a következőket vesszük végig:

- A _closure_-ök, azaz a függvényszerű konstrukciók, amelyeket változóban
  tárolhatsz
- Az _iterátorok_, azaz elemek sorozatának feldolgozási módja
- Hogyan használhatók a closure-ök és az iterátorok a 12. fejezetbeli
  I/O-projekt javítására
- A closure-ök és az iterátorok teljesítménye (spoiler: gyorsabbak, mint
  gondolnád!)

Már szó volt a Rust néhány más képességéről is – például a mintaillesztésről és
az enumokról –, amelyekre szintén hatott a funkcionális stílus. Mivel a
closure-ök és az iterátorok elsajátítása fontos része a gyors, idiomatikus
Rust-kód írásának, ezt az egész fejezetet nekik szenteljük.
