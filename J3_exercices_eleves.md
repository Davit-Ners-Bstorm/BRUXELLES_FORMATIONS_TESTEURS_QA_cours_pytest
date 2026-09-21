# J3 — Exercices PyTest

On teste un module métier `booking.py` (billets, prix, promos, commandes,
remboursements) et un module `legacy_pricing.py`. **Lisez les docstrings** des
fonctions : elles contiennent la spécification à tester.

Fichiers fournis : `booking.py`, `payment.py`, `notifications.py`,
`legacy_pricing.py`, `signup.py`, et des fichiers de test à compléter
(`test_pricing.py`, `test_legacy.py`, `test_orders.py`, `test_challenge.py`),
plus `conftest.py` (vide au départ).

Installer : `pip install pytest`. Lancer : `pytest -v`.

---

## Exercice 1 — Prendre en main PyTest *(fichier `test_pricing.py`)*

Objectif : retrouver les mécanismes de base sur des fonctions simples.

Écrivez des tests pour `ticket_price(category)` et `line_total(category, quantity)`,
en vérifiant des **valeurs de retour** :

- le prix de quelques catégories connues ;
- le total d'une ligne pour quelques quantités.

Les cas « catégorie inconnue » ou « quantité invalide » doivent produire une
**erreur** : on ne sait pas encore tester ça proprement, on les garde pour
l'exercice 3. Ici, uniquement des `assert` sur des valeurs.

Lancez `pytest test_pricing.py -v`. Provoquez volontairement un échec (mettez
une valeur attendue fausse) et **lisez** ce que PyTest affiche : obtenu vs
attendu. Remettez ensuite le bon attendu.

---

## Exercice 2 — Tester du code hérité et diagnostiquer *(fichier `test_legacy.py`)*

On vous confie un module `legacy_pricing.py` écrit par quelqu'un d'autre. Vous
devez le **tester**, sans le modifier au départ.

1. Lisez la spécification de `loyalty_discount_percent` (dans sa docstring).
2. **Concevez vos cas** : quelles valeurs de `previous_orders` couvrent
   correctement la règle ? Pensez aux classes d'équivalence et aux **valeurs
   limites**. Écrivez ces tests.
3. Testez aussi `price_with_loyalty` (le prix après remise).
4. Lancez la suite. Si un test échoue : **lisez l'échec**, déterminez si l'erreur
   vient de votre test ou du code, et expliquez précisément le problème.
5. Une fois le diagnostic posé, corrigez `legacy_pricing.py` et relancez.

Livrable : une suite verte + une phrase expliquant le défaut trouvé et pourquoi
vos cas l'ont révélé.

---

## Exercice 3 — Les cas interdits *(fichier `test_pricing.py`)*

Vous disposez maintenant de `pytest.raises`. **Reprenez d'abord** les deux cas
laissés de côté à l'exercice 1 : `ticket_price` avec une catégorie inconnue, et
`line_total` avec une quantité invalide — leur comportement correct est de
**lever une erreur**.

Ensuite, plusieurs règles de `booking.py` doivent **refuser** certaines entrées.
À vous de décider lesquelles tester. Fonctions concernées : `apply_promo`,
`order_total`. Lisez leurs docstrings et couvrez les situations où elles doivent
lever une erreur. Utilisez `match=` au moins une fois pour cibler un message.

Question à vous poser (pas un piège, une vraie décision de testeur) : parmi ces
règles, lesquelles méritent aussi un test du cas **autorisé** juste à côté de la
limite ?

---

## Exercice 4 — Couvrir un espace de cas avec parametrize *(fichier `test_pricing.py`)*

Objectif : couvrir beaucoup de cas sans dupliquer.

1. Transformez vos vérifications de prix (`line_total` / `order_total`) en tests
   `@pytest.mark.parametrize` avec une table de cas que **vous** concevez.
2. Traitez la règle « maximum 6 billets par commande » par les valeurs limites.
   Un même test paramétré peut contenir des cas autorisés **et** des cas refusés
   (réfléchissez à comment exprimer les deux proprement).
3. Ajoutez des `ids=` lisibles et vérifiez le rendu avec `pytest -v`.

---

## Exercice 5 — Fixtures & conftest *(fichier `test_orders.py`)*

`create_order(event, items, user, payment_gateway, email_service, promo=None)`
a besoin d'un utilisateur, d'un événement, et de deux dépendances (paiement,
e-mail). Lisez sa docstring.

1. Écrivez un test du **cas nominal** (paiement OK → commande confirmée). Pour
   les dépendances, utilisez des `Mock()` (voir le cours ; on approfondit au
   prochain exercice).
2. Vous répétez la préparation de l'utilisateur / de l'événement dans plusieurs
   tests ? Extrayez des **fixtures**.
3. Déplacez les fixtures utiles à plusieurs fichiers dans `conftest.py` et
   vérifiez qu'elles fonctionnent sans import.
4. Écrivez une fixture avec `yield` qui prépare un état et affiche/observe
   quelque chose après le test.

---

## Exercice 6 — Isoler les dépendances *(fichier `test_orders.py`)*

`create_order` dépend d'un service de paiement et d'un service d'e-mail. Ces
services **ne peuvent pas être appelés pour de vrai** (ils lèvent
`NotImplementedError`). C'est à vous de les remplacer par des mocks.

Votre mission : écrire les tests qui garantissent que `create_order` se comporte
correctement vis-à-vis de ses dépendances. **À vous de déterminer** :

- quelles dépendances isoler ;
- quelles **interactions** vérifier (a-t-on appelé le paiement ? avec quel
  montant ? l'e-mail a-t-il été envoyé — ou justement PAS envoyé ?) ;
- quels scénarios comptent (succès, paiement refusé, utilisateur inactif, panne
  du service…) ;
- ce qui relève d'un **résultat** à vérifier et ce qui relève d'une
  **interaction** à vérifier.

Il n'y a pas de checklist fournie : concevez la suite comme un testeur qui doit
garantir que cette fonction est fiable, y compris quand une dépendance échoue.

*Indice outillage (pas de solution)* : `Mock()`, `.return_value`, `.side_effect`,
`.assert_called_once_with(...)`, `.assert_not_called()`.

---

## Challenge final — `process_refund` *(fichier `test_challenge.py`)*

Spécification (voir aussi la docstring de `process_refund`) :

> On peut rembourser une commande **confirmée**. Le remboursement passe par la
> passerelle de paiement (`payment_gateway.refund(montant, transaction_id)`) et,
> en cas de succès, un e-mail de confirmation est envoyé au client. Le
> remboursement est **interdit à moins de 48h** de l'événement (48h pile =
> autorisé). Une commande non confirmée ne peut pas être remboursée. Si la
> passerelle refuse, aucun e-mail n'est envoyé.

Écrivez une **suite de tests pertinente et complète** pour `process_refund`.

Aucune consigne d'outil : à vous de choisir ce qui convient (assertions,
`pytest.raises`, `parametrize`, fixtures, mocks). Préparez-vous à justifier vos
choix :

- pourquoi une fixture ici (ou pas) ?
- pourquoi paramétrer ces cas précis ?
- pourquoi mocker cette dépendance, et qu'est-ce que vous vérifiez sur elle ?
- qu'est-ce que votre suite **garantit réellement** sur `process_refund` ?

---

## Bonus (si vous avez fini)

- `skip` / `xfail` : marquez un test d'une fonctionnalité imaginaire « pas encore
  livrée », et un test d'un « bug connu ». Vérifiez le rendu dans le rapport.
- `patch` : `signup.register_user` crée son service d'e-mail lui-même (pas
  d'injection possible). Testez qu'un e-mail de bienvenue est envoyé, sans
  appeler le vrai service. (Indice : on patche là où l'objet est utilisé.)
- Ajoutez un test qui vérifie qu'une commande avec promo expirée est refusée
  **et** que l'e-mail n'est jamais envoyé dans ce cas.
