HackNight20131114
=================

Afficher des tweets en live avec socket.io


Description
-----------
A l'aide de l'API JavaScript de Twitter, afficher en temps réel un feed de tweets poussé par un backend avec socket.io.

Technologies utilisées
----------------------
* back-end en gevent + socketio
* javaScript pur pour le front
* twython pour la partie streaming Twitter

Usage
-----
* Pour l'exemple simple affichant l'heure

`python geventhour.py`

* Pour l'exemple simple affichant un stream twitter parlant du mot clé 'python'.
* Ne pas oublier de mettre ses propres valeurs dans `APP_KEY`, `APP_SECRET`, `OAUTH_TOKEN`, `OAUTH_TOKEN_SECRET`

`python geventweet.py`

* Puis pointer son navigateur sur http://localhost:5000
