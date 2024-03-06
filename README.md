Rendu du projet de compilation. Pour chaque partie du projet (pretty-printer, interprète, compilateur), décrivez ce qui
fonctionne et ce qui ne fonctionne pas, ainsi que les choix techniques que vous avez pris.

# Projet Compil

## Membres :

- Jeanne Lauwers
- Alexandre Ledun

## Depuis la soutenance

- Création d'un allocateur de registre : allocation_registres.py:
    - permet de générer un code assembleur valide pour l'exemple 01 et 03.
    - ces codes sont respectivement dans test.py et test2.py , il compile et donne le bon résultat

## Utiliser l'interface

- Dans un terminal : `python3 user_interface.py`
- sélectionner un exécutable et un fichier d'exemple
- cliquer sur le bouton bleu en dessous des listes
- vous obtenez en bas à gauche : l'arbre de syntaxe abstraite, en base à droite : le résultat de l'exécution et en haut
  à droite : le code js correspondant à l'exemple sélectionné.

## Partie 1 : pretty-printer (`A_pp.py`)

Le pretty-printer part de l'arbre de syntaxe abstraite pour réécrire le code JS équivalent. Le projet fonctionne sur
tous les exemples sauf une petit erreur qui a été vu dans l'exemple 2. L'indentation est correcte.

## Partie 2 : Interprète (`B_interp.py`)

L'interprète est presque intégralement implémenté. Il ne prend pas encore en compte les paramètres chaîne de caractère
pour les fonctions et les opérateurs logiques.

## Partie 3 : Compilateur (`C_gen3adresses.py` et `D_allocation_registres.py`)

Le projet génère un code assembleur 3 adresses, alloue les registres et marche correctement jusqu'à l'exemple 03. Nous
avons tenté le While et le If en vain.


