# qcm_gr35

Pour lancer l'application, il faut préalablement installer différents modules :

    - le module Flask avec la commande pip install Flask
    - le module Flask-Markdown avec la commande pip intall Flask-Markdown
    - le module markdown avec la commande pip install -r requirements.txt
    car il faut une version antérieure à la 3.2 pour fonctionner avec md-mermaid
    - le module md-mermaid avec la commande pip install md-mermaid

Ensuite il faut utiliser : python3 app.py pour lancer le serveur


Description du format de sauvegarde des énoncés :




Ensembles des fichiers sources :

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

JAVASCRIPT:
    - chosen.jquery.js 
    - math-rendering.js
    - select-button.js

HTML :
    - create.html
    - edit.html
    - enonce.html
    - home.html
    - index.html
    - my_qcm.html
    - my_states.html
    - qcm_list.html
    - qcm.html
    - tag.html

PYTHON :
    - app.py (serveur Flask)
    - globals.py (variables globales)
    - qcm.py (classe QCM et Statement)
    - saving.py 
    - user.py (classe User)
    - utilities.py 

TXT :
    - requirements.txt pour faire fonctionner le module md-mermaid


Webographie :

    - Documentation Flask : https://flask.palletsprojects.com/en/2.2.x/
    - Projet md-mermaid : https://pypi.org/project/md-mermaid/
    - Ajout de tags : https://boundlessjourney.wordpress.com/2014/06/12/adding-new-values-to-chosen-plugin/
    - Jquery chosen : https://harvesthq.github.io/chosen/

Bugs connus :
    - 