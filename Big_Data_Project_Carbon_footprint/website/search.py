import json
import plotly.express as px
import numpy as np
import dash
from dash import dcc, html, Input, Output

# Fonction de recherche
def search_f(conf):
    with open('conf_per_year.json', 'r', encoding='utf-8') as file:
        dico = json.load(file)
        if conf in dico:
            conf_d = dico[conf]
            l1 = []
            l_ab = []
            l_ord = []
            for key, value in conf_d.items():
                try:
                    l1.append((int(key), value))
                except Exception as e:
                    pass
            l1_sorted = sorted(l1, key=lambda x: x[0])
            for elem in l1_sorted:
                l_ab.append(elem[0])
                l_ord.append(2 * elem[1])
            return (l_ab, l_ord)
        else:
            return ([], [])

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Définir la mise en page de l'application Dash
app.layout = html.Div(children=[
    html.H1(children='Empreinte carbone de votre conférence'),
    dcc.Input(id='input-conf', type='text', value='', placeholder='Entrez le code de la conférence'),
    html.Button(id='submit-button', n_clicks=0, children='Soumettre'),
    dcc.Graph(id='example-graph')
])

# Mettre à jour le graphique en fonction de la saisie de l'utilisateur
@app.callback(
    Output('example-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('input-conf', 'value')
)
def update_graph(n_clicks, query):
    if n_clicks > 0 and query:
        l_ab, l_ord = search_f(query)
        fig = px.line(x=l_ab, y=l_ord, markers=True)
        total = sum(l_ord)
        fig.update_layout(
            title=f"{query} : total émis = {total} tCO2eq",
            xaxis_title="Année",
            yaxis_title="tCO2eq"
        )
        return fig
    return {}

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
