import json 
import math 
import matplotlib.pyplot as plt 


json_path="empreinte_annuelle.json"
with open(json_path, 'r', encoding='utf-8') as file:
    dict_empreinte= json.load(file)
n=len(dict_empreinte)
X=[0 for i in range(n)]
i=0
for year in dict_empreinte: 
    X[i]= year
    i+=1 
X.sort()


Y=[0 for i in range(n)]
for i in range(n):
    Y[i]=dict_empreinte[X[i]]


plt.figure(figsize=(10, 6))
plt.plot(X, Y, marker='o', linestyle='-', color='b')

# Add titles and labels
plt.title('Empreinte Carbone Annuelle à travers les années')
plt.xlabel('Année')
plt.ylabel('Empreinte Carbone (tonnes CO2e)')

# Display the plot
plt.grid(True)
plt.xticks(rotation=80)
plt.show()

