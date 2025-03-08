import json





cpt=0

print("loading...")
with open('adresses_f.json', 'r', encoding='utf-8') as file:
    
        adresses = json.load(file)
        

        for key,value in adresses.items() :
                cpt+=1
                # if value==[0,0]:
                        # cpt+=1



        
print(cpt)

#15 k dans adresses1
#11,4 k dans adresses2
#15 k dans adresses3
#11,3 k dans adresses_f sur 103,3k


