# Az ownership megértése

Az ownership a Rust legegyedibb képessége, és mélyen kihat a nyelv többi részére
is. Ez teszi lehetővé, hogy a Rust memóriabiztonsági garanciákat nyújtson
garbage collector nélkül, ezért fontos megérteni, hogyan működik az ownership.
Ebben a fejezetben az ownershipről és több kapcsolódó képességről lesz szó: a
borrowing-ról, a slice-okról, valamint arról, hogyan helyezi el a Rust az
adatokat a memóriában.

## Az interaktív ábrákról {#az-interaktiv-abrakrol}

Ebben a fejezetben – és a könyv néhány későbbi részében – olyan interaktív
ábrákkal találkozol, amelyeket az [Aquascope][aquascope] nevű eszköz készít. Az
Aquascope-ot a Brown Egyetem Cognitive Engineering Lab kutatói fejlesztették ki,
és a Rust működését két nézőpontból mutatja meg. Érdemes néhány percet szánni
arra, hogy megismerd az ábrák jelöléseit, mert utána sokkal gyorsabban
megérthetők.

### Futásidejű ábrák: mi van a memóriában?

Az első fajta ábra a program **futás közbeni** memóriaállapotát mutatja. A kód
mellett `L1`, `L2`, … jelölések állnak: ezek megfigyelési pontok. Minden
ponthoz tartozik egy pillanatkép, amelyen a `Stack` a függvények keretét és a
bennük élő változókat, a `Heap` pedig a futásidőben lefoglalt adatot mutatja. A
pointereket nyilak jelzik.

```aquascope,interpreter,horizontal
fn main() {
    let n = 5;`[]`
    make_and_drop();`[]`
}

fn make_and_drop() {
    let s = String::from("hello");`[]`
}
```

Az `L2` pontban két keret van a stack-en: a `main` és az általa hívott
`make_and_drop`. Utóbbiban él az `s` változó, amely a heap-en lévő `"hello"`
sztringre mutat. Amikor a függvény visszatér, `s` kilép a hatóköréből, ezért az
`L3` pontban a heap már üres.

Ha egy változó kiszürkülve, áthúzva jelenik meg, az azt jelenti, hogy az értékét
elmozgatták (move), így a változó már nem használható.

### Fordítási idejű ábrák: mit enged meg a fordító?

A második fajta ábra azt mutatja, hogy a fordító **fordítási időben** milyen
jogosultságokat tart nyilván az egyes helyeken. Három jogosultság van:

- **R** (_read_): az adat olvasható.
- **W** (_write_): az adat módosítható.
- **O** (_own_): az adat elmozgatható vagy eldobható.

Ezek nem a nyelv részei, hanem a borrow checker működésének szemléltetésére
szolgálnak. A sorok mellett megjelenő táblázatokban a `+` jel azt jelzi, hogy a
változó megkapta az adott jogosultságot, az áthúzott betű pedig azt, hogy
elvesztette:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut v = vec![1, 2, 3];
    let n = &v[0];
    println!("{n}");
    v.push(4);
}
```

Amikor a `&v[0]` létrehoz egy referenciát, `v` elveszíti a **W** és **O**
jogosultságát: amíg `n` él, `v` nem módosítható. Miután `n` utoljára használva
lett a `println!`-ben, `v` visszakapja a jogosultságait, ezért a `v.push(4)`
már megengedett.

Ott, ahol a kódnak nincs meg a szükséges jogosultsága, az ábra pirossal jelzi a
hiányt, és a blokk alatt megjelenik a rák jelzés, hogy a kód nem fordul le:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
    let mut v = vec![1, 2, 3];
    let n = &v[0];
    v.push(4);
    println!("{n}");
}
```

[aquascope]: https://cognitive-engineering-lab.github.io/aquascope/
