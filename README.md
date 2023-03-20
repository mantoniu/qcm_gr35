# qcm_gr35

## Lancement, installation
Pour lancer l'application, il faut préalablement installer différents modules :

    - le module Flask avec la commande "pip install Flask"
    - le module Flask-Markdown avec la commande "pip intall Flask-Markdown"
    - le module markdown avec la commande "pip install -r requirements.txt" car il faut une version antérieure à la 3.2 pour fonctionner avec md-mermaid
    - le module md-mermaid avec la commande "pip install md-mermaid"

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

CSS :

    - card-style.css
    - styles.css
    - header.css
    - list.css
    - my_qcm.css
    - style-tag.css

IMAGES :

    - site-background.jpg
    - background.jpg

### JAVASCRIPT:

    - chosen.jquery.js 
    - math-rendering.js
    - select-button.js

HTML :

    - add_students.html
    - create.html
    - edit.html
    - enonce.html
    - index.html
    - my_qcm.html
    - my_states.html
    - qcm_list.html
    - qcm.html
    

PYTHON :

    - app.py (serveur Flask)
    - globals.py (variables globales)
    - qcm.py (classe QCM et Statement)
    - saving.py 
    - user.py (classe User)
    - utilities.py 

TXT :

    - requirements.txt pour faire fonctionner le module md-mermaid
    - qcm.txt, statements.txt, user.txt pour les enregistrements


## Webographie :

    - Documentation Flask : https://flask.palletsprojects.com/en/2.2.x/
    - Projet md-mermaid : https://pypi.org/project/md-mermaid/
    - Ajout de tags : https://boundlessjourney.wordpress.com/2014/06/12/adding-new-values-to-chosen-plugin/
    - Jquery chosen : https://harvesthq.github.io/chosen/
    - Documentation Flask-SocketIO : https://flask-socketio.readthedocs.io/en/latest/

## Améliorations à faire :

    - Impression des QCM
    - Résultats après avoir fini un QCM
    - Éventuellement mieux sécuriser les enregistrements (interdire les chaînes séparatrices par exemple)