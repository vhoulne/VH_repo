import json
import math 
import matplotlib.pyplot as plt 

with open("par_année_classement.json", 'r', encoding='utf-8') as file:
        années=json.load(file)
with open("empreinte_annuelle.json", 'r', encoding='utf-8') as file:
        empreinte_année=json.load(file)


n=len(années)
X=[0 for i in range(n)]
i=0
for year in années: 
    X[i]= year
    i+=1 
X.sort()


Y=[0 for i in range(n)]
for i in range(n):
    nb_conf=len (années[X[i]])
    empreinte= empreinte_année [X[i]]
    Y[i]= empreinte/nb_conf


plt.figure(figsize=(10, 6))
plt.plot(X, Y, marker='o', linestyle='-', color='b')

# Add titles and labels
plt.title('Empreinte Carbone Moyenne par conférence par année')
plt.xlabel('Année')
plt.ylabel('Empreinte Carbone Moyenne')

# Display the plot
plt.grid(True)
plt.xticks(rotation=80)
plt.show()


        
