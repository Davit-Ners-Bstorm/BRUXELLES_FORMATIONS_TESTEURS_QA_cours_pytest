# PyTest — écrire des tests automatisés

---

## Où on en est

Depuis deux jours, vous interrogez EventFlow en Python avec `requests`, et vous
vérifiez les réponses **à la main** :

```python
response = requests.get("http://localhost:8000/api/events")
if response.status_code == 200:
    print("PASS")
else:
    print("FAIL")
```

Ça marche pour une vérification. Mais dès qu'une vraie campagne de test arrive,
cette approche craque :

- il faut **relancer** chaque script à la main ;
- il faut **lire soi-même** chaque `PASS`/`FAIL` à l'écran ;
- rien ne compte les réussites/échecs, rien ne signale **lequel** casse ;
- on **oublie** des cas, et on n'a aucun rapport exploitable ;
- ça ne **passe pas à l'échelle** : 200 vérifications à l'œil, c'est ingérable.

Un **framework de test** règle exactement ça. Avec PyTest, vous écrivez des
fonctions de test, vous lancez une commande, et l'outil : découvre vos tests,
les exécute tous, isole chaque échec, et produit un rapport clair.

### Ce que PyTest fait pour vous… et ce qu'il ne fait pas

PyTest prend en charge l'**exécution** : trouver les tests, les lancer, comparer,
rapporter. Il ne conçoit **pas** les bons cas de test à votre place. Choisir
quoi tester — le cas nominal, les cas d'erreur, les valeurs limites, les règles
métier — reste **votre travail de testeur**. C'est la compétence que vous avez
déjà ; PyTest ne fait que l'automatiser.

### Code métier vs code de test

Deux mondes séparés, à ne pas confondre :

- le **code métier** (`booking.py`) : la logique de l'application. Vous ne le
  modifiez pas pour le faire passer (sauf s'il a un vrai bug).
- le **code de test** (`test_*.py`) : vos vérifications. C'est ce que vous
  écrivez aujourd'hui.

Une **suite de tests**, c'est un ensemble de fichiers `test_*.py`, chacun
regroupant les tests d'un thème (le prix, les commandes…). On lance tout d'une
commande, et PyTest dit ce qui va et ce qui ne va pas.

Le reste du cours suit ce fil : chaque outil PyTest répond à un problème concret
que vous allez rencontrer.

---

## 1. Premiers tests : découverte, assert, lire un échec

### Le passage de « à la main » à « automatisé »

Reprenons la vérification manuelle, mais en la confiant à PyTest. Au lieu de :

```python
if ticket_price("vip") == 7500:
    print("PASS")
else:
    print("FAIL")
```

on écrit :

```python
def test_vip_price():
    assert ticket_price("vip") == 7500
```

La différence n'est pas cosmétique. Cette fonction, PyTest va la **trouver
tout seul**, l'**exécuter**, et — si l'assertion est fausse — vous dire
exactement quoi. Vous n'imprimez plus rien, vous n'inspectez plus l'écran.

### Comment PyTest trouve les tests (et pourquoi ces conventions)

PyTest n'a pas de liste de vos tests. Il les **découvre** par convention :

- il regarde les fichiers nommés `test_*.py` (ou `*_test.py`) ;
- dans ces fichiers, il exécute les fonctions dont le nom commence par `test_`.

C'est ce qui vous permet d'ajouter un test en écrivant simplement une fonction :
pas de fichier de configuration à mettre à jour. Le revers : une fonction de test
mal nommée (`verifie_prix`) ne sera **jamais lancée**, et vous croirez à tort que
tout va bien. La convention `test_` n'est pas décorative.

```bash
pytest              # découvre et lance tout
pytest -v           # une ligne par test (lisible)
pytest -k promo     # seulement les tests dont le nom contient "promo"
pytest -x           # s'arrête au premier échec
pytest test_pricing.py::test_vip_price   # un test précis
```

### Ce qu'est vraiment une assertion

`assert expression` dit : « à ce point, ceci **doit** être vrai ». Si c'est vrai,
le test continue (et se termine = réussi). Si c'est faux, Python lève une
`AssertionError` et PyTest marque le test échoué.

Ce qui rend PyTest précieux : quand un `assert` échoue, il **réintrospecte**
l'expression et vous montre les valeurs réelles de chaque côté du `==`. Vous ne
lisez pas « le test a échoué » : vous lisez *pourquoi*.

### Lire un échec — la compétence la plus utile de la journée

Rendez un test faux volontairement (`== 7000` au lieu de `7500`) et lancez :

```text
>       assert ticket_price("vip") == 7000
E       assert 7500 == 7000
E        +  where 7500 = ticket_price('vip')
```

Comment lire ça :

- la ligne qui commence par `>` est **l'assertion qui a cassé** ;
- les lignes `E` sont l'explication : `7500 == 7000` est faux ; et
  `where 7500 = ticket_price('vip')` vous dit **d'où vient** le 7500 (l'obtenu).
- donc : obtenu 7500, attendu 7000. Ici c'est le test qui a un mauvais attendu.

Réflexe à prendre : **on lit l'échec avant de toucher au code**. La moitié des
« bugs » sont en réalité des attentes de test fausses ; l'introspection vous le
dit tout de suite.

### Arrange / Act / Assert : une structure de lecture

La plupart des tests se lisent bien en trois temps :

```python
def test_order_total_two_vip():
    items = [{"category": "vip", "quantity": 2}]   # Arrange : on prépare
    total = order_total(items)                      # Act : on exécute l'action
    assert total == 15000                           # Assert : on vérifie
```

Ce n'est pas une règle rigide — un test trivial peut tout tenir sur une ligne —
mais c'est une bonne grille : *qu'est-ce que je prépare, qu'est-ce que
j'exécute, qu'est-ce que je vérifie ?* Un test où l'on ne distingue pas ces trois
temps est souvent un test qui vérifie trop de choses à la fois.

> ### 🧪 Mise en pratique — Exercice 1 : prise en main *(test_pricing.py)*
> Écrivez vos premiers tests sur `ticket_price` et `line_total`, lancez la suite,
> puis **provoquez un échec** et entraînez-vous à le lire. Énoncé complet dans
> `J3_exercices_eleves.md`.

---

## 2. Concevoir les cas : PyTest ne pense pas à votre place

C'est le point le plus important de la journée, et le plus proche de votre
métier. PyTest exécute ce que vous lui donnez. Si vous ne testez que le cas
« tout va bien », vous aurez une suite verte qui ne garantit presque rien.

La qualité d'une suite vient de la **conception des cas** — ce que vous savez
déjà faire :

- **cas nominal** : l'usage normal attendu (`line_total("vip", 2)` → 15000) ;
- **cas négatif** : les entrées qui doivent être refusées (quantité 0, catégorie
  inconnue) ;
- **classes d'équivalence** : regrouper les entrées qui se comportent pareil, et
  tester une par groupe plutôt que cent valeurs équivalentes ;
- **valeurs limites** : les bords entre deux comportements — c'est là que se
  cachent les bugs (« maximum 6 billets » se teste avec 5, 6 **et** 7) ;
- **règles métier** : les invariants du domaine (« on ne vend jamais plus que la
  capacité »).

Un exemple parlant : une règle « accès autorisé à partir de 18 ans » a une
frontière à 18. Tester 10 et 40 ne révèle presque rien ; ce sont les cas **17,
18 et 19** qui attrapent un éventuel `>` écrit à la place de `>=`. Les
frontières sont particulièrement propices aux erreurs de comparaison (`<`, `<=`,
`>`, `>=`) : c'est pourquoi on teste souvent juste avant la limite, à la limite,
et juste après.

> ### 🧪 Mise en pratique — Exercice 2 : tester du code hérité *(test_legacy.py)*
> On vous confie `legacy_pricing.py`, écrit par quelqu'un d'autre, avec sa
> spécification. À vous de **concevoir les cas** (classes d'équivalence + valeurs
> limites), d'écrire les tests, de lancer, et de **diagnostiquer** tout écart
> entre ce que vous observez et la spec. Objectif : une suite verte + une phrase
> expliquant ce que vous avez trouvé.

---

## 3. Quand l'erreur est le comportement attendu : `pytest.raises`

Jusqu'ici on vérifie une valeur de retour. Mais parfois, le comportement
**correct** d'une fonction est de **refuser** une entrée invalide en levant une
exception. `order_total` d'une commande de 7 billets ne doit pas « renvoyer un
nombre » : il doit **lever** une `ValueError`, parce que la règle métier
l'interdit.

Distinguez bien deux choses qui se ressemblent :

- le code **plante** (bug non prévu) ;
- le code **refuse volontairement** une entrée invalide, conformément à la spec.

Le second est un comportement **désiré**, et il se teste — on vérifie que
l'exception attendue est bien levée :

```python
import pytest

def test_too_many_tickets_is_rejected():
    with pytest.raises(ValueError):
        order_total([{"category": "standard", "quantity": 7}])
```

Le test **réussit** si le bloc lève bien `ValueError`, et **échoue** si aucune
exception n'est levée (donc si la règle n'est pas appliquée). On peut cibler le
message avec `match=` (une expression régulière) :

```python
def test_too_many_tickets_message():
    with pytest.raises(ValueError, match="Maximum"):
        order_total([{"category": "standard", "quantity": 7}])
```

**Piège important** : ne mettez dans le bloc `with` que **la ligne censée
lever**. Si vous en mettez plusieurs, dès que la première lève, les suivantes ne
s'exécutent jamais — et vous pourriez croire tester une chose que vous ne testez
pas. Un `raises` = une cause précise.

> ### 🧪 Mise en pratique — Exercice 3 : les cas interdits *(test_pricing.py)*
> Sur `apply_promo` et `order_total`, **décidez** quelles entrées doivent être
> refusées (promo inactive, épuisée, pourcentage hors bornes, commande vide, plus
> de 6 billets…) et écrivez les tests correspondants. Pas de checklist fournie :
> lisez les docstrings et choisissez.

---

## 4. Couvrir un espace de cas sans se répéter : `parametrize`

Vous allez vite rencontrer ce problème : trois, cinq, dix tests **quasi
identiques**, qui ne diffèrent que par les données.

```python
def test_line_total_early_bird():
    assert line_total("early_bird", 1) == 2495

def test_line_total_standard():
    assert line_total("standard", 2) == 7000

def test_line_total_vip():
    assert line_total("vip", 3) == 22500
```

C'est répétitif, pénible à maintenir, et le rapport devient bruyant. PyTest
propose de fournir une **table de cas** :

```python
import pytest

@pytest.mark.parametrize("category, quantity, expected", [
    ("early_bird", 1, 2495),
    ("standard", 2, 7000),
    ("vip", 3, 22500),
])
def test_line_total(category, quantity, expected):
    assert line_total(category, quantity) == expected
```

Chaque ligne de la table devient **un test indépendant** : si le cas `vip`
échoue, les deux autres passent quand même, et le rapport vous dit précisément
lequel a cassé. On nomme les cas avec `ids=` pour un rapport lisible :

```python
@pytest.mark.parametrize("qty", [5, 6], ids=["sous-limite", "limite"])
def test_within_max(qty):
    assert order_total([{"category": "standard", "quantity": qty}]) == 3500 * qty
```

`parametrize` est l'outil naturel des **valeurs limites** et des **classes
d'équivalence** : une ligne par cas représentatif. On peut même y mélanger des
cas valides et des cas qui doivent lever (via un petit drapeau) — mais réfléchissez
à la lisibilité.

**Ne paramétrez pas tout.** Si deux tests vérifient des choses conceptuellement
différentes, deux fonctions séparées sont plus claires qu'une table qui essaie de
tout faire. `parametrize` sert quand c'est **la même vérification** sur des
**données différentes**.

> ### 🧪 Mise en pratique — Exercice 4 : parametrize *(test_pricing.py)*
> Transformez vos vérifications de prix en tests paramétrés, et traitez la règle
> « maximum 6 billets » par les valeurs limites. Concevez votre table, ajoutez des
> `ids=`, et regardez le rapport avec `pytest -v`.

---

## 5. Préparer données et état : les fixtures

### Le problème : la préparation répétée

Regardez ces deux tests :

```python
def test_order_confirmed():
    user = {"email": "camille@eventflow.test", "active": True, "payment_token": "tok_123"}
    event = {"id": 1, "available": 50}
    ...

def test_order_receipt():
    user = {"email": "camille@eventflow.test", "active": True, "payment_token": "tok_123"}
    event = {"id": 1, "available": 50}
    ...
```

La préparation (`Arrange`) est dupliquée. Si le format du `user` change, il faut
le corriger partout. Une **fixture** règle ça.

### La fixture et l'injection par le nom

Une fixture est une fonction décorée `@pytest.fixture` qui prépare quelque chose.
Un test la « demande » simplement en la mettant **en paramètre** : PyTest voit le
nom du paramètre, exécute la fixture correspondante, et injecte son résultat.

```python
import pytest

@pytest.fixture
def active_user():
    return {"email": "camille@eventflow.test", "active": True, "payment_token": "tok_123"}

def test_user_is_active(active_user):     # PyTest injecte le résultat de la fixture
    assert active_user["active"] is True
```

Une fixture sert à deux choses : fournir des **données réutilisables** (un user,
un événement) et **préparer un état** (une base amorcée, un dossier temporaire…).

**Attention à la sur-utilisation.** Une donnée utilisée dans un seul test n'a pas
besoin d'une fixture — écrivez-la sur place, c'est plus lisible. Une fixture se
justifie par une **répétition réelle** ou une préparation non triviale. « Utilisée
partout » n'est pas un synonyme de « bonne fixture ».

### `yield` : préparer avant, nettoyer après

Parfois il faut **nettoyer** après un test (fermer une connexion, supprimer une
donnée créée). Une fixture peut utiliser `yield` : ce qui est avant le `yield`
s'exécute avant le test (setup), ce qui est après s'exécute **après** le test
(teardown), même si le test échoue.

```python
@pytest.fixture
def event_stock():
    event = {"id": 1, "available": 3}   # setup
    yield event                          # le test s'exécute ici, avec cet objet
    print("stock final :", event["available"])   # teardown : après le test
```

Aujourd'hui le teardown est discret ; il deviendra essentiel au J4, quand on
créera une donnée via l'API EventFlow et qu'il faudra la **supprimer** après le
test pour ne pas polluer la base.

### `conftest.py` : partager les fixtures

Quand **plusieurs fichiers** de test ont besoin des mêmes fixtures, on les place
dans un fichier `conftest.py`. PyTest le découvre automatiquement : les fixtures
qui y sont définies sont disponibles dans tous les tests du dossier, **sans
import**. C'est le pendant de la découverte des tests : une convention qui vous
évite la plomberie.

### Les scopes (pour information)

Par défaut, une fixture est recréée **pour chaque test** (scope `function`) —
c'est le comportement le plus sûr (chaque test repart propre). On peut élargir :
`module` (créée une fois par fichier), `session` (une fois pour toute la suite).
On s'en sert quand la préparation est coûteuse (démarrer un serveur, ouvrir une
connexion) et qu'on accepte de la partager. Vous n'en avez pas besoin
aujourd'hui — sachez seulement que ça existe.

> ### 🧪 Mise en pratique — Exercice 5 : fixtures & conftest *(test_orders.py)*
> `create_order` a besoin d'un user, d'un événement et de deux services externes
> (paiement, e-mail). **Ces deux faux services vous sont fournis dans le
> starter** — considérez-les comme des boîtes noires pour l'instant, on les
> comprendra au bloc suivant. Votre travail ici : repérer la répétition du setup,
> l'extraire en **fixtures**, en déplacer dans `conftest.py`, et écrire une
> fixture avec `yield`.

---

## 6. Isoler les dépendances externes : les mocks

### Le problème : on ne veut pas vraiment débiter ni envoyer d'e-mail

`create_order` fait deux choses qui sortent de notre code : elle appelle un
**service de paiement** et envoie un **e-mail**. Question simple : voulez-vous
qu'à *chaque* `pytest` on débite réellement une carte et qu'on envoie un vrai
mail ? Évidemment non. (Dans ce module, ces services lèvent même
`NotImplementedError` si on les appelle pour de vrai — impossible de les
utiliser tels quels en test.)

On veut tester **notre** logique (valider, calculer, orchestrer) **sans exécuter
la vraie dépendance**. C'est le rôle d'un **mock** : un faux objet qui prend la
place du vrai service, répond ce qu'on lui dit de répondre, et **enregistre
comment il a été appelé**.

### `Mock` et `return_value`

```python
from unittest.mock import Mock

payment = Mock()
payment.charge.return_value = {"success": True, "transaction_id": "tx_1"}
email = Mock()
```

Un `Mock()` accepte n'importe quel appel : `payment.charge(...)` existe sans
qu'on l'ait défini. `.return_value` fixe ce que l'appel renverra. On passe ensuite
ces faux services à la fonction (ils sont **injectés** en argument) :

```python
order = create_order(event, items, user, payment, email)
```

### Vérifier une interaction, pas seulement un résultat

Voici le point central du bloc. Un test peut vérifier deux natures de choses :

- un **résultat** : ce que la fonction renvoie (`order["status"] == "confirmed"`) ;
- une **interaction** : ce que la fonction a **fait à ses dépendances**.

```python
assert order["status"] == "confirmed"                       # résultat
payment.charge.assert_called_once_with(15000, "tok_123")    # interaction
email.send.assert_called_once()                             # interaction
```

Pourquoi c'est crucial : **une fonction peut renvoyer le bon résultat tout en
ayant appelé la dépendance avec de mauvais arguments.** Imaginez que `create_order`
renvoie bien `"confirmed"` mais appelle `charge` avec `1500` au lieu de `15000` :
en ne testant que le résultat, vous ne voyez rien ; le client est sous-facturé.
`assert_called_once_with(15000, "tok_123")` attrape ça.

Les vérifications d'appel utiles :

- `mock.methode.assert_called_once_with(args)` : appelé exactement une fois, avec
  ces arguments ;
- `mock.methode.assert_not_called()` : jamais appelé ;
- `mock.methode.call_count` : nombre d'appels.

Le test le plus « testeur » du lot est souvent un **négatif d'interaction** :
vérifier qu'on **n'a pas** envoyé l'e-mail de confirmation quand le paiement a
échoué. On garantit qu'on n'enverra jamais une fausse confirmation.

### `side_effect` : simuler une panne

`return_value` fait renvoyer une valeur. Pour simuler une **dépendance qui
tombe** (le service de paiement est injoignable), on utilise `side_effect` : le
mock **lève** au lieu de renvoyer.

```python
payment.charge.side_effect = ConnectionError("gateway timeout")
```

On vérifie alors que notre code réagit correctement à la panne (par exemple :
il ne prétend pas la commande confirmée, et il n'envoie pas d'e-mail).

> ### 🧪 Mise en pratique — Exercice 6 : isoler les dépendances *(test_orders.py)*
> À vous de garantir que `create_order` se comporte bien vis-à-vis de ses
> dépendances. **Vous décidez** quoi isoler et quelles interactions vérifier
> (montant du paiement, e-mail envoyé — ou justement pas), et quels scénarios
> comptent (succès, paiement refusé, utilisateur inactif, panne). Pas de
> checklist : concevez la suite comme un testeur.

### patch (secondaire)

L'injection de dépendance (passer le service en argument) est la façon la plus
simple de remplacer une dépendance. Mais certains codes créent leur dépendance
**eux-mêmes**, en interne — impossible alors d'injecter un mock. On utilise
`patch`, qui remplace temporairement un nom :

```python
from unittest.mock import patch

def test_register_sends_welcome():
    with patch("signup.EmailService") as FakeEmail:
        register_user("camille@eventflow.test")
        FakeEmail.return_value.send.assert_called_once()
```

La règle qui déroute : on patche le nom **là où il est utilisé**
(`signup.EmailService`), pas là où il est défini (`notifications.EmailService`).
Quand l'injection est possible, préférez-la à `patch` : c'est plus simple et plus
explicite.

---

## 7. `skip` et `xfail`

Deux marqueurs pour les tests qu'on ne veut pas voir échouer « pour de mauvaises
raisons » :

```python
@pytest.mark.skip(reason="liste d'attente pas encore livrée")
def test_waiting_list():
    ...

@pytest.mark.xfail(reason="bug connu EVENT-42, correction prévue")
def test_known_bug():
    ...
```

- `skip` : le test n'est **pas exécuté** (fonctionnalité pas encore disponible,
  test qui ne s'applique pas dans cet environnement) ;
- `xfail` : le test **est exécuté**, mais on sait qu'il échoue (bug connu et
  tracé) ; son échec ne fait pas passer la suite au rouge, et s'il se met à
  réussir, PyTest le signale (le bug est peut-être corrigé).

Règle de conduite : ils servent à documenter une situation connue, **jamais** à
faire taire un test qui dérange. Un `skip` sans raison sérieuse est une dette
qu'on oublie.

---

## Le challenge

> ### 🧪 Challenge final — `process_refund` *(test_challenge.py)*
> On vous donne une spécification métier et le code de `process_refund`. Écrivez
> une suite de tests pertinente. **Aucune consigne d'outil** : à vous de choisir
> assertions, `raises`, `parametrize`, fixtures, mocks — et de justifier vos
> choix. C'est là qu'on voit si vous savez *choisir* l'outil, pas seulement
> l'utiliser.

---

## En résumé

- Un test = une fonction `test_` qui **affirme** (`assert`) ; PyTest la découvre,
  l'exécute, et explique les échecs.
- PyTest automatise l'exécution ; **vous** concevez les cas (nominal, négatif,
  classes d'équivalence, valeurs limites, règles métier).
- `pytest.raises` teste qu'une entrée invalide est **refusée** comme prévu.
- `parametrize` couvre le même test sur plusieurs données — sans tout paramétrer.
- les **fixtures** préparent données et état sans répétition ; `yield` nettoie ;
  `conftest.py` partage.
- les **mocks** isolent les dépendances externes ; on vérifie le **résultat**
  *et* l'**interaction** (les bons arguments, l'e-mail envoyé ou non).
