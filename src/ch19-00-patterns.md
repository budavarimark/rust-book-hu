# Minták és mintaillesztés

A minták a Rust olyan speciális szintaxisát alkotják, amellyel típusok
szerkezetére illeszthetünk – legyen az összetett vagy egyszerű. Ha a mintákat
`match` kifejezésekkel és más szerkezetekkel együtt használod, nagyobb
befolyásod lesz a program vezérlési folyamatára. Egy minta a következők
valamilyen kombinációjából áll:

- literálok
- destrukturált tömbök, enumok, structok vagy tuple-ök
- változók
- helyettesítő szimbólumok
- helykitöltők

Néhány példa mintára: `x`, `(a, 3)` és `Some(Color::Red)`. Azokban a
környezetekben, ahol a minták érvényesek, ezek az összetevők az adatok alakját
írják le. A program ezután értékeket illeszt a mintákhoz, hogy eldöntse, az
adatok alakja megfelelő-e ahhoz, hogy egy adott kódrészlet lefusson.

Egy minta használatához összehasonlítjuk azt valamilyen értékkel. Ha a minta
illeszkedik az értékre, felhasználhatjuk az érték részeit a kódunkban. Gondolj
vissza a 6. fejezet `match` kifejezéseire, amelyek mintákat használtak, például
a pénzérme-válogató gép példájára. Ha az érték illeszkedik a minta alakjára,
használhatjuk az elnevezett részeket. Ha nem illeszkedik, a mintához tartozó
kód nem fut le.

Ez a fejezet a mintákkal kapcsolatos összes tudnivaló referenciája. Végigvesszük
azokat a helyeket, ahol a minták érvényesek, a cáfolható és cáfolhatatlan minták
közötti különbséget, valamint a mintaszintaxis különféle fajtáit, amelyekkel
találkozhatsz. A fejezet végére tudni fogod, hogyan fejezz ki mintákkal sok
fogalmat világos módon.
