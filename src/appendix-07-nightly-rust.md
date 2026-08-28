## G függelék – Hogyan készül a Rust, és mi a „nightly Rust”

Ez a függelék arról szól, hogyan készül a Rust, és ez hogyan érint téged Rust
fejlesztőként.

### Stabilitás megrekedés nélkül

A Rust mint nyelv _nagyon_ sokat törődik a kódod stabilitásával. Azt szeretnénk,
ha a Rust sziklaszilárd alap lenne, amelyre építhetsz, és ez lehetetlen lenne,
ha folyton változnának a dolgok. Ugyanakkor, ha nem kísérletezhetünk új nyelvi
elemekkel, előfordulhat, hogy csak a kiadásuk után derülnek ki a fontos
hiányosságok, amikor már nem tudunk változtatni.

Erre a problémára a megoldásunk az, amit „stabilitás megrekedés nélkül”-nek
hívunk, a vezérelvünk pedig a következő: soha ne kelljen félned attól, hogy a
stabil Rust új verziójára frissítesz. Minden frissítés legyen fájdalommentes, de
hozzon új képességeket, kevesebb hibát és gyorsabb fordítási időt is.

### Sínen vagyunk! Kiadási csatornák és a vonatozás

A Rust fejlesztése _vonatmenetrend_ szerint működik. Vagyis minden fejlesztés a
Rust repository fő ágán történik. A kiadások egy szoftverkiadási vonatmodellt
követnek, amelyet a Cisco IOS és más szoftverprojektek is használtak. A Rustnak
három _kiadási csatornája_ van:

- Nightly
- Beta
- Stable

A legtöbb Rust fejlesztő elsősorban a stable csatornát használja, de aki ki
akarja próbálni a kísérleti újdonságokat, használhatja a nightlyt vagy a betát.

Íme egy példa arra, hogyan működik a fejlesztési és kiadási folyamat: tegyük
fel, hogy a Rust csapata a Rust 1.5 kiadásán dolgozik. Ez a kiadás 2015
decemberében történt, de valósághű verziószámokkal fog szolgálni nekünk. Egy új
nyelvi elem kerül a Rustba: egy új commit érkezik a fő ágra. Minden éjjel
elkészül a Rust új nightly verziója. Minden nap kiadási nap, és ezeket a
kiadásokat automatikusan hozza létre a kiadási infrastruktúránk. Ahogy telik az
idő, a kiadásaink így néznek ki, éjszakánként egyszer:

```text
nightly: * - - * - - *
```

Hathetente eljön az idő egy új kiadás előkészítésére! A Rust repository `beta`
ága leágazik a nightly által használt fő ágról. Innentől két kiadás létezik:

```text
nightly: * - - * - - *
                     |
beta:                *
```

A legtöbb Rust-felhasználó nem használja aktívan a beta kiadásokat, de a CI
rendszerében a beta ellen is tesztel, hogy segítsen a Rustnak felfedezni az
esetleges regressziókat. Közben minden éjjel születik egy nightly kiadás is:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Tegyük fel, hogy találunk egy regressziót. Szerencsére volt időnk tesztelni a
beta kiadást, mielőtt a regresszió bekerült volna egy stabil kiadásba! A javítás
a fő ágra kerül, így a nightly rendbe jön, majd a javítást visszaportoljuk a
`beta` ágra, és elkészül a beta új kiadása:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Hat héttel az első beta létrehozása után eljön a stabil kiadás ideje! A `stable`
ág a `beta` ágból készül el:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hurrá! A Rust 1.5 kész! Egy dologról azonban megfeledkeztünk: mivel eltelt a hat
hét, a Rust _következő_, 1.6-os verziójából is szükségünk van egy új betára.
Így miután a `stable` leágazott a `beta`-ról, a `beta` következő verziója újra
leágazik a `nightly`-ról:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Ezt hívjuk „vonatmodellnek”, mert hathetente egy kiadás „elhagyja az
állomást”, de még végig kell utaznia a beta csatornán, mielőtt stabil
kiadásként megérkezik.

A Rust hathetente jelenik meg, óramű pontossággal. Ha ismered az egyik Rust
kiadás dátumát, tudhatod a következőét is: hat héttel később lesz. A hathetente
ütemezett kiadások egyik kellemes vonása, hogy a következő vonat már úton van.
Ha egy újdonság véletlenül lemarad egy adott kiadásról, nem kell aggódni:
rövidesen jön a következő! Ez segít csökkenteni azt a nyomást, hogy még a
kiadási határidő közelében becsúsztassanak esetleg kiforratlan újdonságokat.

Ennek a folyamatnak köszönhetően bármikor kipróbálhatod a Rust következő
buildjét, és magad ellenőrizheted, hogy könnyű lesz-e ráfrissíteni: ha egy beta
kiadás nem a várt módon működik, jelentheted a csapatnak, és még a következő
stabil kiadás előtt kijavíttathatod! A beta kiadásokban viszonylag ritka a
törés, de a `rustc` is csak egy szoftver, és hibák igenis léteznek.

### Karbantartási idő

A Rust projekt a legutóbbi stabil verziót támogatja. Amikor megjelenik egy új
stabil verzió, a régi verzió eléri az életciklusa végét (EOL). Ez azt jelenti,
hogy minden verzió hat hétig támogatott.

### Instabil nyelvi elemek {#unstable-features}

Van még egy csavar ebben a kiadási modellben: az instabil nyelvi elemek. A Rust
a „feature flag”-eknek nevezett technikát használja annak meghatározására, hogy
egy adott kiadásban mely képességek engedélyezettek. Ha egy új képesség aktív
fejlesztés alatt áll, bekerül a fő ágra, és így a nightlyba is, de egy _feature
flag_ mögé rejtve. Ha felhasználóként ki szeretnéd próbálni a fejlesztés alatt
álló képességet, megteheted, de ehhez a Rust nightly kiadását kell használnod,
és a forráskódodat a megfelelő flaggel kell annotálnod, hogy bekapcsold.

Ha a Rust beta vagy stable kiadását használod, nem használhatsz feature
flageket. Ez az a kulcs, amely lehetővé teszi, hogy gyakorlati tapasztalatot
szerezzünk az új képességekkel, mielőtt örökre stabilnak nyilvánítanánk őket.
Aki a legújabb, kiforratlan dolgokat akarja, megteheti, aki pedig sziklaszilárd
élményre vágyik, maradhat a stable-nél annak tudatában, hogy a kódja nem törik
el. Stabilitás megrekedés nélkül.

Ez a könyv csak a stabil képességekről tartalmaz információt, mivel a fejlesztés
alatt álló képességek még változnak, és biztosan mások lesznek a könyv írásának
ideje és aközött, hogy a stabil buildekben bekapcsolják őket. A csak nightlyban
elérhető képességek dokumentációját megtalálod az interneten.

### A rustup és a Rust nightly szerepe

A rustuppal könnyű váltani a Rust különböző kiadási csatornái között, globálisan
vagy projektenként. Alapértelmezés szerint a stabil Rust lesz telepítve. A
nightly telepítése például így néz ki:

```console
$ rustup toolchain install nightly
```

A `rustup`-pal megnézheted az összes telepített _toolchain_-edet (a Rust
kiadásait és a hozzájuk tartozó komponenseket) is. Íme egy példa az egyik
szerzőnk Windows-os gépéről:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Ahogy látod, a stable toolchain az alapértelmezett. A legtöbb Rust-felhasználó
az idő nagy részében a stable-t használja. Lehet, hogy te is többnyire a
stable-t szeretnéd használni, egy konkrét projektben viszont a nightlyt, mert
fontos számodra valamilyen legfrissebb képesség. Ehhez az adott projekt
könyvtárában használhatod a `rustup override` parancsot, hogy a nightly
toolchaint állítsd be annak, amit a `rustup` használjon, amikor abban a
könyvtárban vagy:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Mostantól, valahányszor a `rustc`-t vagy a `cargo`-t hívod a
_~/projects/needs-nightly_ könyvtárban, a `rustup` gondoskodik róla, hogy a
nightly Rustot használd az alapértelmezett stabil Rust helyett. Ez nagyon jól
jön, ha sok Rust projekted van!

### Az RFC-folyamat és a csapatok

Hogyan szerezhetsz tudomást ezekről az új képességekről? A Rust fejlesztési
modellje a _Request For Comments (RFC) folyamatot_ követi. Ha szeretnél egy
fejlesztést a Rustban, megírhatsz egy javaslatot, amelyet RFC-nek hívunk.

Bárki írhat RFC-t a Rust fejlesztésére, a javaslatokat pedig a Rust csapata
véleményezi és vitatja meg; ez a csapat sok tematikus alcsapatból áll. A
csapatok teljes listája megtalálható [a Rust weboldalán](https://www.rust-lang.org/governance),
és a projekt minden területéhez tartozik csapat: nyelvtervezés,
fordítóimplementáció, infrastruktúra, dokumentáció és így tovább. Az illetékes
csapat elolvassa a javaslatot és a hozzászólásokat, megírja a saját
megjegyzéseit, végül pedig konszenzus születik a képesség elfogadásáról vagy
elutasításáról.

Ha a képességet elfogadják, megnyílik egy issue a Rust repositoryban, és valaki
implementálhatja. Aki implementálja, könnyen lehet, hogy nem az, aki eredetileg
javasolta! Amikor az implementáció kész, egy feature gate mögött bekerül a fő
ágra, ahogy azt az [„Instabil nyelvi elemek”](#unstable-features)<!-- ignore -->
szakaszban tárgyaltuk.

Egy idő után, amikor a nightly kiadásokat használó Rust fejlesztőknek már volt
alkalmuk kipróbálni az új képességet, a csapat tagjai megbeszélik a képességet,
azt, hogyan vált be a nightlyban, és eldöntik, bekerüljön-e a stabil Rustba. Ha
a döntés a továbblépés, a feature gate megszűnik, és a képesség immár stabilnak
számít! Felszáll a vonatra, és megérkezik a Rust egy új stabil kiadásába.
