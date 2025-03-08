#Algorithme de Recherche Tabou avec Heuristiques:

- Utiliser une heuristique pour générer une solution initiale ( assigner chaque article à l'auteur avec la localisation la plus proche du lieu de la conférence).
- Maintenir une liste tabou pour éviter de revisiter les solutions récentes.
- Explorer les voisins de la solution courante en modifiant les affectations d'auteurs pour quelques articles.
- Accepter la meilleure solution parmi les voisins, même si elle est pire que la solution actuelle, pour éviter les minima locaux.
- Ajouter les mouvements récents à la liste tabou.
- Répéter jusqu'à ce qu'un critère d'arrêt soit atteint (par exemple, un nombre fixe d'itérations ou un temps d'exécution maximal).