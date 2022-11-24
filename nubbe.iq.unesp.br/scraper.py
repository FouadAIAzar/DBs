# import time
# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup
# if __name__ == '__main__':
#     driver = uc.Chrome()
#     driver.get('https://nubbe.iq.unesp.br/portal/nubbe-search.html')
    
#     driver.find_element("xpath",'/html/body/div[4]/div[1]/div[5]/button').click()
#     driver.find_element("xpath",'/html/body/div[4]/div[1]/div[5]/button').click()
#     time.sleep(15)
#     soup = BeautifulSoup(driver.page_source,'lxml')
#     page_list = soup.select('div#pages_bottom a')
#     for page in page_list:
#         print(page)
#         page = page.string
#         driver.find_element("xpath",f'/html/body/div[4]/div[2]/div[3]/a[{page}]').click()

#         time.sleep(10)
#         soup = BeautifulSoup(driver.page_source,'lxml')
#         resultsTable = soup.select('div#resultsTable row')
        
#         for row in resultsTable:
#             a = row.select('a')[0]['id']
#             f_row = f'{a}\n'
#             file_id = open('id_list.txt','a',encoding='utf8')
#             file_id.write(f_row)
#             file_id.close()


import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib.request

base_data = {}
with open('output.csv','a',newline='') as f:
    writer=csv.writer(f)
    mystuff = ["Source(s)","species","Biological_properties","NuBBEID","Common_Name","IUPAC_Name","Inchi","Inchikey","Chemical_Class","Mol_Formula","SMILES","Molecular_Mass","Monoisotopic_Mass","cLogP","TPSA","Lipinski_Violations","H-bond_acceptors","H-bond_donors","Rotatable_Bonds","Molecular_Volume","image_link"]
    writer.writerow(mystuff)
response = requests.get('https://nubbe.iq.unesp.br/portal/do/Query?service=30')
soup = BeautifulSoup(response.text,'xml')
atividade_biologica = soup.select('atividade_biologica')
for atividade in atividade_biologica:
    codigo = atividade.select('codigo')[0].string
    nome = atividade.select('nome')[0].string
    base_data[codigo]  = nome

response = requests.post('https://nubbe.iq.unesp.br/portal/do/Query?service=17&tipo_1=')
soup = BeautifulSoup(response.text,'xml')
substancia_array = soup.select('substancia')

for substancia in substancia_array:
    id = substancia.select('id')[0].string
    NuBBEID = substancia.select('codigo_auto')[0].string
    print(id,' - ',NuBBEID, 'Processing!!!')

    response = requests.get(f'https://nubbe.iq.unesp.br/portal/do/Query?service=21&id={id}')
    soup = BeautifulSoup(response.text,'xml')
    substancia_1 = soup.select('substancia')[0]
    Common_Name = substancia_1.select('nome')[0].string
    try:
        nome_iupac = substancia_1.select('nome_iupac')[0].string
    except:
        nome_iupac = ''
    inchi = substancia_1.select('inchi')[0].string
    inchikey = substancia_1.select('inchikey')[0].string.replace('\n','')
    try:
        classe = substancia_1.select('classe')[0].string.replace('\n','')
    except:
        classe = ''
    formol = substancia_1.select('formol')[0].string.replace('\n','')
    smiles = substancia_1.select('smiles')[0].string.replace('\n','')
    massa_molar = substancia_1.select('massa_molar')[0].string.replace('\n','')
    massa_monoisotopica = substancia_1.select('massa_monoisotopica')[0].string.replace('\n','')
    logp = substancia_1.select('logp')[0].string.replace('\n','')
    tpsa = substancia_1.select('tpsa')[0].string.replace('\n','')
    nvlr = substancia_1.select('nvlr')[0].string.replace('\n','')
    non = substancia_1.select('non')[0].string.replace('\n','')
    nohnh = substancia_1.select('nohnh')[0].string.replace('\n','')
    nrotb = substancia_1.select('nrotb')[0].string.replace('\n','')
    mol_vol = substancia_1.select('mol_vol')[0].string.replace('\n','')
    ativ_bio = substancia_1.select('ativ_bio')
    Biological_properties = ''
    for bio in ativ_bio:
        which = bio.select('which')[0].string
        
        which1 = base_data[which]
        Biological_properties = f'{Biological_properties};{which1};'
    Biological_properties = Biological_properties[1:-1].replace(';;',';')
    tipo = substancia_1.select('tipo')[0].string
    file_list = substancia_1.select('nome_arq')
    for file in file_list:
        file = file.string
        
        urllib.request.urlretrieve(f'https://nubbe.iq.unesp.br/portal/do/Query?service=16&id={id}&name={file}', f"mol_files/{file}")
    image_link = f'https://nubbe.iq.unesp.br/portal/do/Query?service=24&id={id}&widthmax=700&heightmax=400'
    if tipo == '1':
        tipo = 'Synthetic'
    elif tipo == '2':
        tipo = 'Semisynthetic'
    elif tipo == '3':
        tipo = 'Biotransformation product'
    elif tipo == '4':
        tipo = 'Isolated from a plant'
    elif tipo == '5':
        tipo = 'Isolated from a microorganism'
    elif tipo == '6':
        tipo = 'Isolated from a marine organism'
    elif tipo == '7':
        tipo = 'Isolated from animalia'
    try:
        origem = substancia_1.select('especies origem')[0]
    except:
        origem = ''
    try:
        familia	 = origem.select('familia')[0].string
    except:
        famila = ''
    try:
        genero	 = origem.select('genero')[0].string
    except:
        genero = ''
    try:
        especie	 = origem.select('especie')[0].string
    except:
        especie = ''
    try:
        cidade	 = origem.select('cidade')[0].string
    except:
        cidade = ''
    species = f'{familia} {genero} {especie};{cidade}'
    with open('output.csv','a',newline='',encoding='utf8') as f:
        writer=csv.writer(f)
        mystuff = [tipo,species,Biological_properties,NuBBEID,Common_Name,nome_iupac,inchi,inchikey,classe,formol,smiles,massa_molar,massa_monoisotopica,logp,tpsa,nvlr,non,nohnh,nrotb,mol_vol,image_link]
        writer.writerow(mystuff)
