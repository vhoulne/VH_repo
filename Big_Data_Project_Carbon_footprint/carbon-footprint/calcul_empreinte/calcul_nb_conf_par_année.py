import json
import math 
import matplotlib.pyplot as plt 

with open("par_année_classement.json", 'r', encoding='utf-8') as file:
        années=json.load(file)


n=len(années)
X=[0 for i in range(n)]
i=0
for year in années: 
    X[i]= year
    i+=1 
X.sort()


Y=[0 for i in range(n)]
for i in range(n):
    Y[i]=len (années[X[i]])


plt.figure(figsize=(10, 6))
plt.plot(X, Y, marker='o', linestyle='-', color='b')

# Add titles and labels
plt.title('Nombre de Conférences par année')
plt.xlabel('Année')
plt.ylabel('Nombre de conférences')

# Display the plot
plt.grid(True)
plt.xticks(rotation=80)
plt.show()


        
