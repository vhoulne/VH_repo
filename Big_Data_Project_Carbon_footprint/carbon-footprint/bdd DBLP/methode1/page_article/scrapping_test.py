#test
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import extraction
import re

# A=soup.find(id="LayoutWrapper")
# B=A.find("div",class_="row")
# C=B.find("div",class_="col")
# R1=C.find("div", class_="ng2-app")


# R2=R1.find("div", class_="global-content-wrapper")
# M=R2.find("xpl-root")
# print(M)
# R4=M.find("div", class_="global-ng-wrapper")
# print(R4)



# script_tags = soup.find_all('script')
# for script_tag in script_tags:
#     if 'var my_variable' in script_tag.text:
#         # Utiliser une expression régulière pour extraire la valeur de la variable
#         match = re.search(r'var my_variable = "(.*?)";', script_tag.text)
#         if match:
#             my_variable_value = match.group(1)
#             print("La valeur de la variable JavaScript est :", my_variable_value)
#             break

"""
ext = extraction.Extractor()

x = ext.extract(requests.get(URL,headers=headers).text, source_url=URL)
print(x)
"""
#page = requests.get(URL, headers=headers)
#soup = BeautifulSoup(page.content, "html.parser")
#print(soup)
# R1=soup.find(id="LayoutWrapper")
# R2=R1.find("div",class_="row")
# R3=R2.find("div",class_="col")
# R4=R3.find("div",class_="ng2-app")   #ok
# R5=R4.find("div",class_="global-content-wrapper")
# R6=R5.find('xpl-root')
# R7=R6.find(id="xplMainContentLandmark")
# print(R1)
#à priori il y 23 div à faire
# =R18.find_all('xpl-accordian-section')
#R2 = R1.find_all("div",class_="document-accordion-section-container hide-mobile")
#R3=R2.find_all('xpl-document-section')
#results = soup.find(id="authors")
#adresse = results.find_all("div", class_="col-24-24")
#print(adresse)