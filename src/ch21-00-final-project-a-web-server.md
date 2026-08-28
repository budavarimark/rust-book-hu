# Záróprojekt: többszálú webszerver építése

Hosszú út áll mögöttünk, de a könyv végéhez értünk. Ebben a fejezetben még egy
projektet készítünk el közösen, hogy bemutassunk néhányat az utolsó fejezetek
fogalmai közül, és felelevenítsünk néhány korábbi leckét is.

A záróprojektünkben olyan webszervert készítünk, amely „Hello!”-t mond, és a
böngészőben úgy néz ki, ahogy azt a 21-1. ábra mutatja.

Íme a tervünk a webszerver felépítéséhez:

1. Ismerkedjünk meg egy kicsit a TCP-vel és a HTTP-vel.
2. Figyeljük a TCP-kapcsolatokat egy socketen.
3. Elemezzünk néhány egyszerű HTTP-kérést.
4. Készítsünk szabályos HTTP-választ.
5. Javítsuk a szerverünk átbocsátóképességét egy thread pool segítségével.

<img alt="Képernyőkép egy böngészőről, amely a 127.0.0.1:8080 címet nyitotta meg, és egy weboldalt jelenít meg a „Hello! Hi from Rust” szöveges tartalommal" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">21-1. ábra: A záró közös projektünk</span>

Mielőtt belevágnánk, két dolgot érdemes megemlíteni. Először is: az általunk
használt módszer nem a legjobb mód arra, hogy Rusttal webszervert építsünk. A
közösség tagjai számos, éles használatra kész crate-et publikáltak a
[crates.io](https://crates.io/) oldalon, amelyek az itt megépítettnél jóval
teljesebb webszerver- és thread pool-implementációkat kínálnak. A célunk
ebben a fejezetben azonban az, hogy tanulj, nem az, hogy a könnyebbik utat
válasszuk. Mivel a Rust rendszerprogramozási nyelv, mi választhatjuk meg, hogy
milyen absztrakciós szinten szeretnénk dolgozni, és mélyebbre mehetünk, mint
ami más nyelvekben lehetséges vagy praktikus.

Másodszor: itt nem használunk asyncot és awaitet. Egy thread pool megépítése
önmagában is elég nagy kihívás, nem is beszélve arról, ha még egy async
runtime-ot is építenénk hozzá! Azt viszont jelezni fogjuk, hogy az async és az
await hogyan lenne alkalmazható néhány olyan problémára, amellyel ebben a
fejezetben találkozunk. Végső soron pedig, ahogy a 17. fejezetben már
megjegyeztük, sok async runtime maga is thread poolokkal kezeli a munkáját.

Az alap HTTP-szervert és a thread poolt tehát kézzel írjuk meg, hogy
megismerhesd azokat az általános elgondolásokat és technikákat, amelyek a
később használt crate-ek mögött állnak.
