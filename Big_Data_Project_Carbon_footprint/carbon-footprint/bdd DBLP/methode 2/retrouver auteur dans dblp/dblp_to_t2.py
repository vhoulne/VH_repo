from lxml import etree
import json

element_data={}
print("starting")
def parse_xml_with_dtd(xml_file, dtd_file,save_path):
    # Créer un analyseur XML avec la résolution des entités et la validation DTD activées
    parser = etree.XMLParser(resolve_entities=True, dtd_validation=True)

    # Ouvrir le fichier XML
    with open(save_path, 'w', encoding='utf8') as file:
        with open(xml_file, 'rb') as f:
            # Ouvrir le fichier DTD
            dtd = etree.DTD(open(dtd_file))
            # Récupérer les éléments définis dans le DTD
            dtd_elements = [elt.name for elt in dtd.elements()]
            

 

            for event, element in etree.iterparse(f, events=('start', 'end'), load_dtd=True):
                # Vérifier si l'élément est une balise de fin
                if event == 'end':
                    if element.tag in dtd_elements:
                        element_data[element.tag] = []
                        # Vérifier si l'élément a des sous-éléments
                        has_children = len(element) > 0
                        if has_children:
                            # Si l'élément a des sous-éléments, vous pouvez traiter les données différemment
                            # par exemple, ajouter les sous-éléments à une liste distincte dans votre structure de données
                            sub_elements_data = []
                            for sub_element in element:     
                                sub_elements_data.append({str(sub_element.tag) : str(sub_element.text)})
                            # element_data[element.tag].append({'texte': element.text, 'sous_elements': sub_elements_data})
                            json.dump({str(element.tag): sub_elements_data}, file)
                            file.write('\n')
                # element.clear()
            f.close()
        file.close() 




parse_xml_with_dtd('dblp.xml', 'dblp.dtd','t2.json')


"""['dblp', 'article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www', 'data', 'person',
 'author', 'editor', 'address', 'title', 'booktitle', 'pages', 'year', 'journal', 'volume', 'number', 'month', 'url', 'ee', 'cite',
  'school', 'publisher', 'note', 'cdrom', 'crossref', 'isbn', 'chapter', 'rel', 'stream', 'series', 'publnr', 'ref', 'sup', 'sub',
    'i', 'tt']"""