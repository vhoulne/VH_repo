import json

def search_f(conf):
    #conf est un str
    with open('conf_per_year.json', 'r', encoding='utf-8') as file:
        dico = json.load(file)
        if conf in dico:
            conf_d=dico[conf]
            l1=[]
            l_ab=[]
            l_ord=[]
            for key,value in conf_d.items():
                try:
                    l1.append((int(key),value))
                except Exception as e:
                    pass
            l1_sorted = sorted(l1, key=lambda x: x[0])
            for elem in l1_sorted:
                l_ab.append(elem[0])
                l_ord.append(elem[1])
            return(l_ab,l_ord)
                
        else:
            return ([],[])
        


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Rechercher une conférence et trier les résultats")
#     parser.add_argument('conf', type=str, help='Nom de la conférence à rechercher')
#     args = parser.parse_args()

#     l_ab, l_ord = search(args.conf)
#     plt.plot(l_ab,l_ord)
#     plt.show()
#     #print("l_ab:", l_ab)
#     #print("l_ord:", l_ord)


import matplotlib.pyplot as plt

def plot_graph(x, y):
    plt.plot(x,y)
    plt.show()


from flask import Flask, request, jsonify

app = Flask(__name__)

# Route pour la gestion de la requête OPTIONS
@app.route('/', methods=['OPTIONS'])
def handle_options_request():
    # Autorise les méthodes que vous utilisez (POST dans ce cas)
    response = jsonify({'allow': 'POST'})
    response.headers.add('Access-Control-Allow-Origin', '*')  # autorise toutes les origines
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

# Route pour la gestion de la requête POST
@app.route('/', methods=['POST'])
def handle_search_request():
    if request.method == 'POST':
        data = request.get_json()
        query = data['query']
        print(f'Requête de recherche reçue : {query}')
        l=search_f(query)
        plot_graph(l[0],l[1])
        # Ici, vous pouvez exécuter votre fonction Python avec la variable query
        
        # Répond avec un message JSON
        return jsonify({'message': 'Requête reçue avec succès'})

if __name__ == '__main__':
    app.run(port=8000)

