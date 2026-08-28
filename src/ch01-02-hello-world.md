## Hello, World!

Most, hogy telepítetted a Rustot, itt az ideje megírni az első Rust-programodat.
Új nyelv tanulásakor hagyomány egy olyan kis programot írni, amely a `Hello,
world!` szöveget írja ki a képernyőre, úgyhogy mi is ezt tesszük!

> Megjegyzés: Ez a könyv feltételezi a parancssor alapszintű ismeretét. A Rust
> nem támaszt konkrét elvárásokat a szerkesztőddel, az eszközeiddel vagy a kódod
> helyével szemben, így ha a parancssor helyett inkább IDE-t használnál,
> nyugodtan használd a kedvenc IDE-det. Sok IDE ma már valamilyen szinten
> támogatja a Rustot; a részletekért nézd meg az IDE dokumentációját. A Rust
> csapata arra összpontosít, hogy a `rust-analyzer` révén kiváló IDE-támogatás
> legyen elérhető. További részletekért lásd a [D függeléket][devtools]<!--
> ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### A projektkönyvtár beállítása

Kezdd azzal, hogy létrehozol egy könyvtárat a Rust-kódod tárolására. A Rust
számára mindegy, hol van a kódod, de a könyv gyakorlataihoz és projektjeihez
azt javasoljuk, hogy hozz létre egy _projects_ könyvtárat a saját home
könyvtáradban, és ott tartsd az összes projektedet.

Nyiss meg egy terminált, és add ki a következő parancsokat, hogy létrehozz egy
_projects_ könyvtárat, azon belül pedig egy könyvtárat a „Hello, world!”
projektnek.

Linuxon, macOS-en és a Windows PowerShellben ezt írd be:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Windows CMD-ben ezt írd be:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### A Rust-programok alapjai {#rust-program-basics}

Ezután hozz létre egy új forrásfájlt _main.rs_ néven. A Rust-fájlok mindig
_.rs_ kiterjesztésűek. Ha több szóból áll a fájlnév, a konvenció szerint
alulvonással válaszd el őket. Például a _helloworld.rs_ helyett használd a
_hello_world.rs_ nevet.

Most nyisd meg az imént létrehozott _main.rs_ fájlt, és írd be az 1-1.
listában szereplő kódot.

<Listing number="1-1" file-name="main.rs" caption="Program, amely kiírja, hogy `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Mentsd el a fájlt, és térj vissza a terminálablakhoz a
_~/projects/hello_world_ könyvtárban. Linuxon vagy macOS-en a következő
parancsokkal fordíthatod le és futtathatod a fájlt:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Windowson a `./main` helyett a `.\main` parancsot add ki:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Az operációs rendszertől függetlenül a `Hello, world!` sztringnek kell
megjelennie a terminálban. Ha nem látod ezt a kimenetet, lapozz vissza a
telepítési szakasz [„Hibaelhárítás”][troubleshooting]<!-- ignore --> részéhez,
ahol megtudhatod, hogyan kérhetsz segítséget.

Ha a `Hello, world!` mégis megjelent, gratulálunk! Hivatalosan is írtál egy
Rust-programot. Ezzel Rust-programozó lettél – üdvözlünk!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Egy Rust-program anatómiája

Nézzük át részletesen ezt a „Hello, world!” programot. Íme a kirakós első
darabja:

```rust
fn main() {

}
```

Ezek a sorok egy `main` nevű függvényt definiálnak. A `main` függvény
különleges: minden futtatható Rust-programban ez az első kód, amely lefut. Az
első sor itt egy `main` nevű függvényt deklarál, amelynek nincs paramétere, és
nem ad vissza semmit. Ha lennének paraméterei, azok a zárójelek (`()`) között
szerepelnének.

A függvény törzsét `{}` fogja közre. A Rust minden függvénytörzs köré kapcsos
zárójeleket követel meg. Jó stílus a nyitó kapcsos zárójelet a
függvénydeklarációval azonos sorba tenni, egy szóközzel elválasztva.

> Megjegyzés: Ha a Rust-projektek között egységes, szabványos stílushoz
> szeretnéd tartani magad, használhatod a `rustfmt` nevű automatikus
> formázóeszközt, amely egy adott stílusra formázza a kódodat (a `rustfmt`-ről
> bővebben a [D függelékben][devtools]<!-- ignore --> olvashatsz). A Rust
> csapata ezt az eszközt a szokásos Rust-disztribúció részévé tette, akárcsak a
> `rustc`-t, tehát valószínűleg már telepítve van a gépeden!

A `main` függvény törzsében a következő kód szerepel:

```rust
println!("Hello, world!");
```

Ez a sor végzi el az összes munkát ebben a kis programban: szöveget ír ki a
képernyőre. Három fontos részletet érdemes itt észrevenni.

Először is, a `println!` egy Rust-makrót hív meg. Ha helyette függvényt hívna,
akkor `println` alakban (a `!` nélkül) írnánk. A Rust makrói arra szolgálnak,
hogy olyan kódot írjunk, amely kódot generál, kiterjesztve ezzel a Rust
szintaxisát; részletesebben a [20. fejezetben][ch20-macros]<!-- ignore -->
tárgyaljuk őket. Egyelőre csak annyit kell tudnod, hogy a `!` használata azt
jelenti: makrót hívsz meg egy közönséges függvény helyett, és hogy a makrók nem
mindig ugyanazokat a szabályokat követik, mint a függvények.

Másodszor, itt van a `"Hello, world!"` sztring. Ezt a sztringet argumentumként
adjuk át a `println!`-nak, és a sztring megjelenik a képernyőn.

Harmadszor, pontosvesszővel (`;`) zárjuk a sort, ami azt jelzi, hogy ez a
kifejezés véget ért, és a következő kezdődhet. A Rust-kód legtöbb sora
pontosvesszővel végződik.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Fordítás és futtatás

Épp most futtattál egy frissen létrehozott programot, nézzük hát meg a folyamat
minden lépését.

A Rust-programot futtatás előtt le kell fordítanod a Rust fordítójával: add ki
a `rustc` parancsot, és add át neki a forrásfájlod nevét, így:

```console
$ rustc main.rs
```

Ha van C vagy C++ hátered, észreveheted, hogy ez hasonlít a `gcc`-re vagy a
`clang`-ra. A sikeres fordítás után a Rust egy bináris futtatható állományt
állít elő.

Linuxon, macOS-en és a Windows PowerShellben az `ls` parancs kiadásával láthatod
a futtatható állományt a shellben:

```console
$ ls
main  main.rs
```

Linuxon és macOS-en két fájlt látsz. A Windows PowerShellben ugyanazt a három
fájlt látod, mint a CMD-ben. A Windows CMD-ben a következőt írnád be:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Ez megmutatja a _.rs_ kiterjesztésű forráskódfájlt, a futtatható állományt
(Windowson _main.exe_, minden más platformon _main_), Windows esetén pedig egy
_.pdb_ kiterjesztésű fájlt, amely hibakeresési információkat tartalmaz. Innen a
_main_ vagy a _main.exe_ fájlt futtatod, így:

```console
$ ./main # or .\main on Windows
```

Ha a _main.rs_ fájlod a „Hello, world!” programod, ez a sor a `Hello, world!`
szöveget írja ki a termináladra.

Ha valamelyik dinamikus nyelvet, például a Rubyt, a Pythont vagy a JavaScriptet
ismered jobban, talán szokatlan, hogy a fordítás és a futtatás külön lépés. A
Rust _előre fordított (ahead-of-time compiled)_ nyelv, ami azt jelenti, hogy
lefordíthatsz egy programot, odaadhatod a futtatható állományt valaki másnak,
és ő anélkül is futtathatja, hogy telepítve lenne nála a Rust. Ha viszont egy
_.rb_, _.py_ vagy _.js_ fájlt adsz oda valakinek, akkor neki (értelemszerűen)
telepített Ruby-, Python- vagy JavaScript-implementációra van szüksége. Azokban
a nyelvekben viszont egyetlen parancs is elég a program lefordításához és
futtatásához. A nyelvtervezésben minden kompromisszum kérdése.

Egyszerű programoknál a puszta `rustc`-vel való fordítás megfelel, de ahogy a
projekted növekszik, kezelni akarod majd az összes beállítást, és könnyen
megoszthatóvá szeretnéd tenni a kódodat. Ezután bemutatjuk a Cargo eszközt,
amely a valós Rust-programok írásában lesz a segítségedre.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
