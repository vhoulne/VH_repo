⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⡿⣞⣷⣻⢿⣿⣿⣿⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⡿⣞⣷⣻⢿⣿⣿⣿

                                            PROJ104|ARTISHOW : Carbon Footprint

Notre dépot est constitué essentiellement de 3 dossiers : **bdd**, **calcul_empreinte** et **conf_by_code** ainsi que quelques fichiers.

--------------------------------------------------
Le dossier **bdd** contient le code qui permet de récupérer les données du dump du site web :

• **méthode 1** : contient les fichiers afterparsing.py, bddclass.py et bddparsing.py qui permettent de récupérer les données en utilisant etree.iterparse .La méthode a été abandonné car elle ne fonctionnait pas.
• **méthode 2** : méthode abondonnée, ce dossier contient :  
    - Un programme Java donné directement sur le site de DBLP( dossier methode 1 : on n'a pas gardé le fichier associé )
    - Un programme Python trouvé sur github et référencé à beaucoup d'endroit sur le web permettant de parser la bdd avec beaucoup de fonction. Ce programme utilise la fonction etree.parse.( dossier methode 2: parsing_dblp_parsing.py )
    - Un programme Python trouvé sur stackoverflow utilisant la méthode etree.iterparse ( scrap.py ) ce dossier contient aussi : 5 fichiers .json qui contiennent des echantillons de données scrapées
• **nv_base_de_données** :
    - Deux fichiers python **test.py** et **total.py** qui permettent, dans un 1er temps, de récuperer les ID des chercheurs, leurs noms, leurs adresses et de les regrouper en une base de données SQLlite 
    - **Données_chercheurs.bdd** qui contient la nouvelle base de données SQLlite 
    - **Decodage_GPS.py** qui permet de transformer les adresses en des coordonnées GPS 
• **parsing ORCID** :
    - **ORCID_3.py** : code python qui permet d'extraire les données sur les chercheurs des fichiers .xml et de les enregistrer dans un fichier .db : une base de données à 3 colonnes (id_chercheur, nom_source, ville)
**5 fichiers python** : différentes méthodes pour transformer les bases de données .json en des fichier .bd

--------------------------------------------------
Le dossier **adresse_parsing** contient : 

- **parsing_cities.py** : un code python qui permet de parcourir toutes les villes du monde à plus de 500 habitants (à partir d'une base de données réparties en 4 fichiers .json ) et de récupérer leurs coordonnées GPS et puis tout stocker dans un fichier .json sous forme de dictionnaire dont keys = villes 
- **parsing_countries.py** : la meme chose mais pour des pays + codes des pays (les codes à 2 lettres majus ) 
- **parsing_avec_api_geocode.py** : code python pour récupérer les coordonnées GPS des adresses précises à partir de l'api geocode de google map(la clé de l'api a été supprimé du fichier pour des raisons de confidentialité ) 

--------------------------------------------------
Le dossier **auteursORCID1** contient :

• **partie summaries** : contient les fichier python qui permettent de parser ORCID_SUMMARIES et de récupérer les localisations des chercheurs
• **adresse3 and google** : ensemble de fichiers python qui permettent de regrouper toutes les données sur les localisations à partir des bases de données et de l'API Geocode.

--------------------------------------------------
Le dossier **calcul_empreinte** contient :

- **calcul_empreinte_carbone.py** : code python final qui permet de calculer l'empreinte carbone des différentes conférences à partir des différentes bases de données .json et .db puis afficher le total de cette empreinte et de renvoyer un dictionnaire avec les conf en clé et leur empreinte en attribut.
- **calcul_empreinte_moyenne_par_année.py** : code python qui permet de calculer puis visualiser la moyenne de l'empreinte carbone par conférence par année.
|-> **moyenne_empreinte_parconf_parannée.png** : le graphe illustre la moyenne annuelle de l'empreinte carbone par conférence.
- **calcul_empreinte_par_année.py** : code python final qui permet de calculer l'empreinte carbone des différentes conférences regroupées par année + renvoyer un dictionnaire avec les années en key et les empreines annuelles en valeur.
|-> **empreinte_annuelle.png** : le graphe en question, qui montre l'évolution annuelle de l'empreinte carbone des conférences.
- **calcul_nb_conf_par_année.py** : code python qui permet de calculer et de visualiser le nombre de conférence par année.
|-> **nb_conf_par_année.png** : le graphe des nommbres de conférences par année.
- **convert_db_to_json.py** : un code python qui permet de transformer la bdd .db des locations des auteurs en un dict .json
- **db_to_json_articles.py** : code python qui permet de transformer la bdd .db des articles en un dict .json avec les conférences en key 
- **vers_json_conf_par_année.py** : code python qui permet de tranformer la bdd.json des conférences en un dict dont les clés sont les années 
- **organisation_données.py** : un code python qui permet de lister les infos: années/ empreintes et les visualiser en un graphe qui montre l'évolution de l'empreinte carbone des confs à travers les années. 

--------------------------------------------------
Le dossier **documents informatifs** contient :

- Le planning et le .pdf sur les enjeux sociaux et économiques de notre projet.

--------------------------------------------------
Le dossier **elements_algorithme** contient :

- Les fichiers python des premières réflexions sur l'algorithme de calcul de l'empreinte, finalisé dans le dossier calcul_empreinte

--------------------------------------------------
Le dossier **finaliser la bdd des auteurs** contient :

- **modif auteurs_2.py** : effectue des modifications sur la base de données des auteurs en un fichier .db

--------------------------------------------------
Le dossier **page_article** contient :

- fichiers python pour scraper DBLP

--------------------------------------------------
Le dossier **retrouver auteur dans dblp** contient :

- fichiers python qui permettent de parser DBLP et récuperer puis trier les données sur les auteurs

--------------------------------------------------
Le dossier **conf_by_code** contient :

- **index.html** & **page2.html** : site web page principale & page de recherche par conférence
- fichiers pour python : pour la partie traitement des .json et affichage des courbes, graphiques...

--------------------------------------------------
**ORCID.PY** : un code python qui permet de regrouper les fichier XML issus de la base de données orcid en une unique base de données globale  
- le fichier convert_json_to_db_conferences.py : code python qui permet d'obtenir la bdd de conferences sous forme d'un fichier .db à partir d'un dictionnaire .json 
- le dossier retrouver auteur dans dblp qui contient: 
**2_articlestodb.py** , article_nv_version.py  : code python qui permet d'obtenir la bdd des articles sous forme d'un fichier .db à partir d'un dict .json, les colonnes sont nom_article, conf_nom et les colonnes des auteurs 
**dblp_to_t2.py** : code python qui permet de parser un fichier XML et récupoérer des données sur les articles sous forme d'un dict json 
**modifauteur.py** : code python qui permet de faire qq modifs sur le dict .json obtenu notamment au niveau des noms des auteurs 
**tri.py** : code python qui permet de faire le tri sur les données récupérées dans un fichier .json et les stocker dans un autre fichier .json  

⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⡿⣞⣷⣻⢿⣿⣿⣿⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⣿⣿⡽⣯⢿⣽⣳⢯⣟⣷⣻⢷⣯⢿⣽⣿⣿⣿⣿⣿⣷⣟⣾⣳⢯⣟⣾⣳⢯⡷⣯⢷⣻⣞⡿⣞⣷⣻⢿⣿⣿⣿⡿⣞⣷⣻⢿⣿⣿⣿

Projet supervisé par _Antoine Amarilli_,
par _Rahma Loukil_, _Vincent Houlné_ et _Paul Gonzalez_
fait le 27/06/2024.