import json

with open('articles.json',"r",encoding='utf-8') as f_in:
    with open('articles_f.json',"w",encoding='utf-8') as f_out:
        dicf={}
        ind=0
        for line in f_in:
            # Charger la ligne JSON en un objet Python
            data = json.loads(line)
            dumpi=[]
            ind+=1
            titre=''
            interet=next(iter(data.values()))     #interter est une liste
            dic_l=[]
            for dic in interet:        
                for key,result in dic.items():
                    if key=="author":
                        dic_l.append(result)
                    elif key =="crossref":
                        dumpi.append(result) 
                    elif key=="title":
                        titre=result
            dumpi.append(dic_l)
            dicf[titre]=dumpi
            print(ind)
            
        json.dump(dicf,f_out,ensure_ascii=False,indent=4)