# Aquascope-ábrák a magyar Rust könyvben

Ez az ág az [Aquascope][aquascope] segítségével egészíti ki a könyvet
interaktív ábrákkal, a [Brown Egyetem Cognitive Engineering Lab][cel]
[rust-book forkjának][brown] mintájára. A forkban lévő kvízek **nem** részei
ennek az ágnak, csak az ábrák.

Maga a dokumentum nem része a könyvnek.

[aquascope]: https://cognitive-engineering-lab.github.io/aquascope/
[cel]: https://cel.cs.brown.edu/
[brown]: https://github.com/cognitive-engineering-lab/rust-book

## Mit ad hozzá az Aquascope?

Kétféle ábrát:

- **futásidejű (`interpreter`)** – a stack és a heap állapota a kód `L1`, `L2`, …
  megfigyelési pontjain; jól mutatja a move-ot, a `clone`-t, a `drop`-ot és a
  függvényhívások kereteit;
- **fordítási idejű (`permissions`)** – a borrow checker által nyilvántartott
  R/W/O jogosultságok soronként; jól mutatja, mit tilt és mit enged a borrowing.

Az ábrák olvasását maga a könyv is elmagyarázza a [4. fejezet
bevezetőjében](src/ch04-00-understanding-ownership.md).

## Fordítás helyben

```bash
./ci/aquascope-setup.sh
export PATH="$PWD/bin:$PATH"
export LD_LIBRARY_PATH="$(rustc +nightly-2026-05-01 --print target-libdir)"
mdbook build
```

A `ci/aquascope-setup.sh` letölti az `aquascope` release binárisait a `bin/`
könyvtárba, és telepíti azt a nightly toolchaint, amelyre az `aquascope-driver`
épül. Mindkettő verziója a szkript elején állítható.

Az `mdbook test` az Aquascope nélkül is lefut: a `book.toml`-ban a
preprocesszor `renderers = ["html"]` beállítással csak a HTML kimenethez fut.

## Ellenőrzés

Egy-egy fejezet ábráit az egész könyv újrafordítása nélkül is ellenőrizheted:

```bash
python3 tools/check_aquascope.py src/ch04-02-references-and-borrowing.md
```

A szkript minden `aquascope` blokkot egy eldobható mdbook-projektbe másol, és
megmondja, melyik nem elemezhető.

## A blokkok szintaxisa

Az ábrát sima kódblokk hordozza, `aquascope` nyelvcímkével és vesszővel
elválasztott kapcsolókkal:

````markdown
```aquascope,interpreter,horizontal
fn main() {
    let s = String::from("hello");`[]`
}
```
````

Kapcsolók:

| kapcsoló | jelentés |
| --- | --- |
| `interpreter` | futásidejű memóriaábra |
| `permissions` | fordítási idejű jogosultságok |
| `boundaries` | a jogosultsági határok kirajzolása a sorok mellé |
| `stepper` | soronkénti jogosultságváltozások |
| `horizontal` | a pillanatképek egymás mellett, nem egymás alatt |
| `shouldFail` | a kód szándékosan nem fordul le |
| `concreteTypes` | a generikus típusok helyett a konkrét típusok |
| `hideCode` | csak az ábra jelenik meg, a kód nem |

A `` `[]` `` jelölés a kódban egy megfigyelési pontot vesz fel (`L1`, `L2`, …).
A `#`-tel kezdődő sorok az ábrán nem jelennek meg, de a fordításban részt
vesznek – ugyanúgy, ahogy a szokásos Rust kódblokkokban.

## Konvenciók ebben a könyvben

- Az ábrák **kiegészítik** a meglévő listákat, nem helyettesítik őket. Ezért a
  blokkban általában csak a lényeges sorok láthatók, a többit `#` rejti el.
- Az ábrák előtt egy-két mondatos magyar bevezető mondja meg, mit érdemes
  megfigyelni rajtuk.
- Az ábrák kódja – mint a könyv minden más kódja – angol marad.
