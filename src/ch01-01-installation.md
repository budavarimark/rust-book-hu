## Telepítés {#installation}

Az első lépés a Rust telepítése. A Rustot a `rustup` segítségével töltjük le,
amely a Rust-verziók és a hozzájuk tartozó eszközök kezelésére szolgáló
parancssori eszköz. A letöltéshez internetkapcsolatra lesz szükséged.

> Megjegyzés: Ha valamilyen okból inkább nem szeretnéd a `rustup`-ot használni,
> nézd meg a [Rust egyéb telepítési módjait ismertető oldalt][otherinstall],
> ahol további lehetőségeket találsz.

Az alábbi lépések a Rust fordítójának legutóbbi stabil verzióját telepítik. A
Rust stabilitási garanciái biztosítják, hogy a könyv minden olyan példája,
amely lefordul, az újabb Rust-verziókkal is le fog fordulni. A kimenet
verziónként kissé eltérhet, mert a Rust gyakran javít a hibaüzeneteken és a
figyelmeztetéseken. Más szóval a Rust bármely újabb, stabil verziója, amelyet
ezekkel a lépésekkel telepítesz, a várt módon működik majd a könyv tartalmával.

> ### Parancssori jelölés
>
> Ebben a fejezetben és a könyv további részében is mutatunk majd a
> terminálban használt parancsokat. Azok a sorok, amelyeket a terminálba be kell
> írnod, mind `$` jellel kezdődnek. A `$` karaktert nem kell begépelned; ez a
> parancssori prompt, amely az egyes parancsok kezdetét jelzi. Azok a sorok,
> amelyek nem `$` jellel kezdődnek, jellemzően az előző parancs kimenetét
> mutatják. Ezenkívül a kifejezetten PowerShellre vonatkozó példák `$` helyett
> `>` jelet használnak.

### A `rustup` telepítése Linuxon vagy macOS-en

Ha Linuxot vagy macOS-t használsz, nyiss meg egy terminált, és add ki a
következő parancsot:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

A parancs letölt egy szkriptet, és elindítja a `rustup` eszköz telepítését,
amely a Rust legutóbbi stabil verzióját telepíti. Előfordulhat, hogy a
jelszavadat kéri. Ha a telepítés sikeres, a következő sor jelenik meg:

```text
Rust is installed now. Great!
```

Szükséged lesz egy _linkerre_ is, vagyis arra a programra, amellyel a Rust
egyetlen fájlba fűzi össze a lefordított kimeneteit. Valószínű, hogy már van
ilyened. Ha linkerhibákat kapsz, telepíts egy C fordítót, amely jellemzően
tartalmaz linkert is. A C fordító azért is hasznos, mert néhány gyakori
Rust-csomag C kódtól függ, és C fordítóra lesz szüksége.

macOS-en így juthatsz C fordítóhoz:

```console
$ xcode-select --install
```

A Linux-felhasználók általában a GCC-t vagy a Clangot telepítsék a
disztribúciójuk dokumentációja szerint. Ha például Ubuntut használsz, a
`build-essential` csomagot telepítheted.

### A `rustup` telepítése Windowson

Windowson menj a [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> címre, és kövesd a Rust telepítésére vonatkozó utasításokat. A telepítés
egy pontján a rendszer felkér a Visual Studio telepítésére. Ez adja a linkert
és a programok fordításához szükséges natív könyvtárakat. Ha ehhez a lépéshez
több segítségre van szükséged, nézd meg a
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore --> oldalt.

A könyv további része olyan parancsokat használ, amelyek a _cmd.exe_-ben és a
PowerShellben egyaránt működnek. Ha konkrét eltérések vannak, elmagyarázzuk,
melyiket használd.

### Hibaelhárítás {#troubleshooting}

Annak ellenőrzéséhez, hogy helyesen telepítetted-e a Rustot, nyiss meg egy
shellt, és add ki ezt a sort:

```console
$ rustc --version
```

A legutóbb kiadott stabil verzió verziószámát, commit hash-ét és commitjának
dátumát kell látnod, a következő formátumban:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Ha látod ezt az információt, sikeresen telepítetted a Rustot! Ha nem látod,
ellenőrizd az alábbiak szerint, hogy a Rust szerepel-e a `%PATH%`
rendszerváltozóban.

Windows CMD-ben ezt használd:

```console
> echo %PATH%
```

PowerShellben ezt:

```powershell
> echo $env:Path
```

Linuxon és macOS-en pedig ezt:

```console
$ echo $PATH
```

Ha mindez rendben van, és a Rust mégsem működik, több helyen is kaphatsz
segítséget. A [közösségi oldalon][community] megtudhatod, hogyan léphetsz
kapcsolatba más rustaceanökkel (ezzel a bolondos becenévvel illetjük magunkat).

### Frissítés és eltávolítás

Ha a Rustot a `rustup` segítségével telepítetted, könnyen frissíthetsz egy
újonnan kiadott verzióra. A shellből futtasd a következő frissítőszkriptet:

```console
$ rustup update
```

A Rust és a `rustup` eltávolításához futtasd a következő eltávolító szkriptet a
shellből:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### A helyi dokumentáció olvasása

A Rust telepítése a dokumentáció helyi másolatát is tartalmazza, így offline is
olvashatod. Futtasd a `rustup doc` parancsot, hogy megnyisd a helyi
dokumentációt a böngésződben.

Valahányszor a standard könyvtár nyújt egy típust vagy függvényt, és nem vagy
biztos benne, mit csinál vagy hogyan kell használni, nézz utána az alkalmazások
programozási felületének (API) dokumentációjában!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Szövegszerkesztők és IDE-k használata

Ez a könyv semmit nem feltételez arról, hogy milyen eszközökkel írod a
Rust-kódot. Nagyjából bármelyik szövegszerkesztő megteszi! Sok szövegszerkesztő
és integrált fejlesztői környezet (IDE) azonban beépített Rust-támogatással
rendelkezik. A Rust weboldalán, [az eszközök oldalán][tools] mindig találsz egy
elég friss listát számos szerkesztőről és IDE-ről.

### Offline munka ezzel a könyvvel

Több példában is a standard könyvtáron túli Rust-csomagokat használunk. Ahhoz,
hogy végigdolgozd ezeket a példákat, vagy internetkapcsolatra lesz szükséged,
vagy arra, hogy előre letöltsd ezeket a függőségeket. A függőségek előzetes
letöltéséhez a következő parancsokat futtathatod. (Azt, hogy mi az a `cargo`, és
hogy ezek a parancsok pontosan mit csinálnak, később részletesen elmagyarázzuk.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Ezzel gyorsítótárba kerülnek e csomagok letöltött állományai, így később nem
kell újra letöltened őket. Miután lefuttattad ezt a parancsot, a
`get-dependencies` mappát nem kell megtartanod. Ha lefuttattad a parancsot, a
könyv további részében az összes `cargo` parancsnál használhatod az `--offline`
kapcsolót, hogy a hálózat helyett ezeket a gyorsítótárazott verziókat
használja.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
