# ITCheck

ITCheck est un petit logiciel permettant de vérifier, à l'aide de tests, les différentes fonctions d'un étudiant lors d'un TP. Il permet à la fois à l'étudiant de s'assurer de la justesse de son code durant le TP et aussi de faciliter la correction d'un TP noté.

![Capture d'écran](/doc/screenshot.png "Capture d'écran")

**Fonctionnalités :**

 - Gestion du barème pour chaque question et chaque test
 - Affichage ou non du test effectué et/ou du résultat attendu
 - Limite de temps à l'exécution
 - Gestion stricte ou non des types
 - Importation de module
 - Ajout/modification de variables pour un test
 - Affichage de la sortie standard (stdout)
 - Compatible Windows et Linux

**Utilisation :**

Il faut télécharger le script [makebin.py](makebin.py) et le dossier [src](src/).

Pour générer le programme il faut d'abord configurer les tests avec le fichier [config.ini](config.ini) et ensuite exécuter le script [makebin.py](makebin.py) qui générera un fichier exécutable ITCheck (ou ITCheck.exe). Ce fichier constitue le programme de vérification qui pourra être distribué aux étudiants.

**Configuration :**

Voici un exemple de fichier de configuration [config.ini](example/config.ini)
et le fichier source d'un potentiel étudiant [TPex.py](example/TPex.py)

Le fichier commence par une section `[DEFAULT]` constituée des entrées :

 - `tp_name` : nom du TP (facultative / par défaut =TP)
 - `platform` : Linux ou Windows (facultative / par défaut =Linux)
 - `max_time_import` : temps maximal (en secondes) pour l'importation du fichier du TP (facultative / par défaut =1)
 - `module_import` : liste des modules (séparés par des virgules) nécessaires à l'importation d'un TP ou à l'exécution des tests (facultative / par défaut vide)

Chaque question nécessite une section `[Question]` ou n'importe quelle section commençant par un Q par exemple `[Q12]` ou `[Question 12 Exercice 2]`. Il n'est pas nécessaire que le nom de ces sections soient uniques. Cette section est constituée des entrées :

 - `exercice` : numéro de l'exercice (facultative)
 - `number` : numéro de la question (facultative)
 - `name` : nom de la question (facultative et remplace les deux précédentes entrée si non vide)
 - `func_name` : nom de la fonction ou variable à tester (obligatoire)
 - `scale` : barème de la question (facultative / par défaut vaut la somme des points des tests de la question)

A la suite d'une section `[Question]` on place une section `[Test]` (ou n'importe qu'elle section commençant par un T) pour chaque test à effectuer pour la question. Cette section est constituée des entrées :

 - `command` : instruction du test (obligatoire)
 - `result` : résultat attendu du test. Peut être une expression ou une instruction donnant le résultat (obligatoire sauf si level=info)
 - `max_time` : temps maximal (en secondes) que peut prendre l'exécution du test (facultative / par défaut =1)
 - `point` : nombre de point que rapporte le test en cas de succès (facultative / par défaut =1)
 - `level` :  détermine le mode de calcul des points de la question. Il y a 5 niveaux possibles :
    - `fatal` : en cas d'échec on arrête les tests, on met 0 à la question
    - `critic` : en cas d'échec le test ne rapporte aucun point et on continue les tests. Une pénalité de 25% du barème de la question est appliquée. En cas d'erreur d'execution (exception) on met 0 à la question et on arrète les tests
    - `error` : en cas d'échec le test ne rapporte aucun point et on continue les tests. En cas d'erreur d'execution on met 0 à la question et on arrète les tests
    - `warning` : en cas d'échec le test ne rapporte aucun point et on continue les tests
    - `info` : il n'y a pas de résultat attendu et pas de points. Utile pour voir le comportement d'une fonction sur des cas exotiques
    - Il est conseillé de respecter cet ordre dans une suite de test avec différents niveaux (facultative / par défaut =critic)
 - `hidden` : détermine si le test et/ou le résultat attendu doit être caché ou montré :
    - `0` : le test et le résultat attendu sont affichés
    - `1` : seul le résultat attendu est affiché
    - `2` : seul le résultat obtenu est affiché (par exemple utile pour tester les variables)
    - facultative / par défaut =0
 - `strict` : détermine si le test doit vérifier le type (facultative / par défaut =True)
 - `custom_var` : dictionnaire contenant des variables personalisées (par exemple des fonctions) pour effectuer le test. La clef est le nom de la variable et la valeur sa valeur. Utile par exemple pour redéfinir une fonction déjà existante, par exemple random pour avoir un test déterministe (facultative / par défaut ={})

**Dépendance :**

Pour générer un fichier binaire le script [makebin.py](makebin.py) a besoin du logiciel [PyInstaller](https://pyinstaller.org/en/stable/) qu'on peut installer via pip par la commande

    pip install pyinstaller

Pour se passer de ce module, il suffit de supprimer les dernière ligne du fichier [makebin.py](makebin.py) à partir de la ligne contenant

    PyInstaller.__main__.run

Il faudra ensuite lancer une fois le script [makebin.py](makebin.py) puis on pourra distribuer le dossier [src](src/) et lancer le programme avec le fichier [view.py](src/view.py)
