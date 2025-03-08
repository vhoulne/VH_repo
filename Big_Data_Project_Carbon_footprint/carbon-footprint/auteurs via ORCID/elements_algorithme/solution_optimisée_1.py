# solution 2: #Algorithme de Recherche Tabou avec Heuristiques:

 ## Utiliser une heuristique : cf solution 1 (reflexionx_algo.py ) 
 ## Maintenir une liste tabou pour éviter de revisiter les solutions récentes.
 ## Explorer les voisins de la solution courante en modifiant les affectations d'auteurs pour quelques articles.
 ##Accepter la meilleure solution parmi les voisins, même si elle est pire que la solution actuelle, pour éviter les minima locaux.
 ##Ajouter les mouvements récents à la liste tabou.
 ##Répéter jusqu'à ce qu'un critère d'arrêt soit atteint (par exemple, un nombre fixe d'itérations ou un temps d'exécution maximal).
import random
import math
import sqlite3
import reflexion_algo as ra 
def get_neighbors(solution, articles, conferences, author_locations):
    neighbors = []
    
    for article_id, current_author in solution.items():
        conference_id = articles[article_id]['conference_id']
        conf_lat, conf_lon = conferences[conference_id]
        
        for author_id in articles[article_id]['authors']:
            if author_id != current_author:
                new_solution = solution.copy()
                new_solution[article_id] = author_id
                neighbors.append(new_solution)
    
    return neighbors

def evaluate_solution(solution, articles, conferences, author_locations):
    total_distance = 0
    
    for article_id, author_id in solution.items():
        conference_id = articles[article_id]['conference_id']
        conf_lat, conf_lon = conferences[conference_id]
        author_lat, author_lon = author_locations.get(author_id, (0, 0))
        distance = haversine_distance(conf_lat, conf_lon, author_lat, author_lon)
        total_distance += distance
    
    return total_distance

def tabu_search(conferences, articles, author_locations, max_iterations, tabu_list_size):
    solution, total_distance = initial_solution(conferences, articles, author_locations)
    best_solution = solution
    best_distance = total_distance
    tabu_list = []
    
    for iteration in range(max_iterations):
        neighbors = get_neighbors(solution, articles, conferences, author_locations)
        neighbors = [n for n in neighbors if n not in tabu_list]
        
        if not neighbors:
            break
        
        solution = min(neighbors, key=lambda n: evaluate_solution(n, articles, conferences, author_locations))
        total_distance = evaluate_solution(solution, articles, conferences, author_locations)
        
        if total_distance < best_distance:
            best_solution = solution
            best_distance = total_distance
        
        tabu_list.append(solution)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)
    
    return best_solution, best_distance