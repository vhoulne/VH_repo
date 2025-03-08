from lxml import etree
import json

######################################## trouver les infos des conférences dans un ficheir xml à partir de leurs codes d'indentification##
def parse_xml_with_dtd(xml_file, save_path,conf_path):
        
        liste_conf=[]
        proceedings_data = {}

        with open(conf_path, 'r', encoding='utf-8') as fc:
            conferences_data = json.load(fc)

            for key_conf,value in conferences_data.items():      
                liste_conf.append(key_conf)

            print("fin etape 1")
            print(len(liste_conf))

            for elem in liste_conf:
                proceedings_data[elem]=[]

            print(len(proceedings_data))
            print("fin etape 2")


        with open(xml_file, 'rb') as f:
            ind=0
                # Itérer sur les éléments du fichier XML
            for event, element in etree.iterparse(f, events=('start', 'end'), load_dtd=True):
                # Vérifier si l'élément est une balise de fin et est de type inproceedings
                if event == 'end' and element.tag == 'proceedings':
                    ind+=1
                    print(ind)
                    # Récupérer la clé de l'élément

                    key = element.get('key', '')
                    if key.startswith("conf"):
                        print(key)
                        print(type(key))
                    # Vérifier si la clé commence par "conf"
                        if str(key) in liste_conf:
                            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                            # Récupérer les sous-balises <title>
                            titles1 = [title.text for title in element.findall('.//title')]

                            proceedings_data[key].append(titles1)
                                
                        # Nettoyer l'élément pour libérer la mémoire
                        element.clear()
                
            print("fin etape 3")

        with open(save_path, 'w', encoding='utf-8') as outfile:
            json.dump(proceedings_data, outfile, ensure_ascii=False, indent=4)    
        outfile.close()

########################################################### enlever le titre des infos ###############################################""

def offtitle (in_file,out_file):
    """Ce code supprime une partie des infos inutiles mais ne donne pas de lieu"""
    """il indique aussi si le contenu est problématique ou pas (il y en a 327 problématiques)"""
    dictionnaire={}
    ind=0
    indgalere=0
    with open(in_file, 'r', encoding='utf-8') as fin:
        conferences_data = json.load(fin)
        for conference_ref, titre in conferences_data.items():
            ind+=1
            if len(titre)>1:
                print("c'est la sauce")
                indgalere+=1
                new_title=[1,titre]
            
            elif titre==[] or len(titre[0])>1:
                print("c'est la grosse sauce")
                print(conference_ref,titre)
                indgalere+=1
                new_title=[1,titre]
            else: 
                pre_new_title= titre[0][0].split(',',1)
                if len(pre_new_title)==2 :
                    new_title= [0,pre_new_title[1].strip()]
                else:
                    print(pre_new_title)
                    print(ind)
                    indgalere+=1
                    new_title=[1,pre_new_title[0].strip()]

            dictionnaire[conference_ref]=new_title
        print('nombre conf',ind)
        print('nombre galere',indgalere)
        with open(out_file, 'w', encoding='utf-8') as fout:
            json.dump(dictionnaire,fout,ensure_ascii=False,indent=4)
        print("finished dumping")


#################################################### on essaye de ne récupérer que des phrases sans chiffres maintenant ######################################
def comporte_des_nombres(chaine):
    # Vérifie chaque caractère de la chaîne
    for char in chaine:
        # Si le caractère est un chiffre, retourne True
        if char.isdigit():
            return True
    # Si aucun caractère n'est un chiffre, retourne False
    return False

mots_usuels=[" and "," in ","Proceedings"," on ", "Part I","Modeling"]

def is_usual(chaine):
    for elem in mots_usuels:
        if elem in chaine:
            return True
    return False

def garder_lieu_sous_cond(in_file,out_file):
    dictionnaire={}
    ind=0
    indgalere=0
    
    with open(in_file, 'r', encoding='utf-8') as fin:
        conferences_data = json.load(fin)
        for conference_ref, listep in conferences_data.items():
            ind+=1
            if listep[0]==0:
                sentence1=listep[1].split(',')
                sentence2=[]
                for elem in sentence1:
                    if comporte_des_nombres(elem)==False and is_usual(elem)==False:
                        sentence2.append(elem)
                sentencef=""
                for mot in sentence2:
                    sentencef+=mot
                dictionnaire[conference_ref]=[0,sentencef]
                

            if listep[0]==1:
                try :
                    sentence1=listep[1].split()
                    sentence2=[]
                    for elem in sentence1:
                        if comporte_des_nombres(elem)==False and is_usual(elem)==False:
                            sentence2.append(elem)
                    sentencef=""
                    for mot in sentence2:
                        sentencef+=" "+ mot
                    dictionnaire[conference_ref]=[1,sentencef]  
                except Exception as e:
                    print(ind)
                    indgalere+=1
                    print("Une erreur s'est produite :", e)
                    dictionnaire[conference_ref]=listep
             
    print('nombre conf',ind)
    print('nombre galere',indgalere)
    with open(out_file, 'w', encoding='utf-8') as fout:
        json.dump(dictionnaire,fout,ensure_ascii=False,indent=4)


####################################################### main ############################################################""
garder_lieu_sous_cond('conf_no_name.json','conf_adress_max.json')
#offtitle('conf_info.json','conf_no_name.json')
#parse_xml_with_dtd('dblp.xml', 'conf_info.json','conferences.json')






