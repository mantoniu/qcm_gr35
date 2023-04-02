# qcm_gr35

## Lancement, installation
Pour lancer l'application, il faut préalablement installer les différents modules avec la commande "pip install -r requirements.txt" 

Ensuite il faut utiliser : "python3 app.py" pour lancer le serveur


## Description du format de sauvegarde :

Le système de sauvegarde est basé sur deux fichiers :

    - le fichier utilities.py pour la sauvegarde de façon générale, celui-ci pourra être réadapté et réutilisé par la suite car très général
    - le fichier saving.py qui vise précisément les besoins en terme de sauvegarde de notre projet en particulier, il exploite beaucoup les fonctions de utilities.py

Méthodes de sauvegarde :

    On a choisi d'enregistrer nos données dans des fichiers textes .txt.
    Au lieu d'utiliser des retours à la ligne, des espaces, ou des virgules comme classiquement pour séparer les données de notre fichier, nous avons utilisé les chaînes "@__///1S" pour séparer les lignes et "@__///2S" pour séparer les colonnes, ainsi il n'y que très peu de risque de problème lié à l'utilisation de séparateurs dans le texte des énoncés.
    Certaines propriétés sont séparées par des points virgules comme les tags et les numéros des bonnes réponses.


## Ensembles des fichiers sources :

### Partie générale

JAVASCRIPT :
    
    - chosen.jquery.js
    - math-rendering.js
    
HTML :

    - student_or_teacher.html

IMAGES :

    - background.jpg

CSS :
    
    - card-style.css
    - choosen.css
    - global.css
    - home.css
    - list_qcm.css
    - my_states.css
    - student_or_teacher.css
    - styles.css

TXT :

    - requirements.txt pour faire fonctionner le module md-mermaid
    - liveqcm.txt, livestatementsstats.txt, qcm.txt, statements.txt, teachers.txt, students.txt pour les enregistrements

### Partie étudiant

JAVASCRIPT :

    - home.js
    - statement.js

HTML :

    - home.html
    - login.html
    - myaccount.html
    - statement.html

### Partie professeur

JAVASCRIPT:

    - creation.js
    - tools.js
    - mystates.js
    - projection.js
    - qcm.js
    - stats.js
    
 HTML :

    - tools.html
    - create.html
    - edit.html
    - enonce.html
    - index.html
    - my_states.html
    - qcm_list.html
    - qcm.html
    - stats.html
    - exam.html
    

PYTHON :

    - app.py (serveur Flask)
    - globals.py (variables globales)
    - objects.py (classes QCM, Statement, LiveQCM)
    - saving.py 
    - user.py (classe User)
    - utilities.py 

## Webographie :

    - Documentation Flask : https://flask.palletsprojects.com/en/2.2.x/
    - Projet md-mermaid : https://pypi.org/project/md-mermaid/
    - Ajout de tags : https://boundlessjourney.wordpress.com/2014/06/12/adding-new-values-to-chosen-plugin/
    - Jquery chosen : https://harvesthq.github.io/chosen/
    - Documentation Flask-SocketIO : https://flask-socketio.readthedocs.io/en/latest/
    - Uploading files FLask : https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/


## Amélioration de la partie 1

    - Meilleur affichage des QCM
    - Résolution du bug lors de l'ajout puis de la suppresion de réponses


## Améliorations à faire :

    - Impression des QCM
    - Résultats après avoir fini un QCM
    - Éventuellement mieux sécuriser les enregistrements (interdire les chaînes séparatrices par exemple)
    - Mettre en place les statistiques
    - Résoudre bug de réponse