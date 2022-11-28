import requests
from bs4 import BeautifulSoup
import concurrent.futures,time
from tqdm import tqdm
import urllib.request

import threading
import csv
file_write_lock = threading.Lock()
with open('output.csv','a',newline='') as f:
    writer=csv.writer(f)
    mystuff = ["impat_type","phytochmecial","Synonymous_chemical_names","External_chemical_identifiers","smiles","InChI","InChIKey","DeepSMILES","Functional_groups","ClassyFire_Kingdom","ClassyFire_Superclass","ClassyFire_Class","ClassyFire_Subclass","NP_Classifier_Biosynthetic_pathway","NP_Classifier_Superclass","NP_Classifier_Class","NP_Likeness_score"]
    writer.writerow(mystuff)
def pagination_creator(last_page): #017968
    page_list = []
    last_page = last_page
    
    for page in range(1,last_page):
        ID = str(page).zfill(6)
        url = f'https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY{ID}'
        page_list.append(url)
    return page_list



def run(download, line_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        results = list(tqdm(executor.map(download, line_list), total=len(line_list)))
    return results

def download(page):
    while True:
        try:
            response = requests.get(page)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            continue
    soup = BeautifulSoup(response.text,'lxml')
    div = soup.select('div.col-8.pt-0.mt-0.ml-2.pl-2')[0].text
    try:
        impat_type = div.split('IMPPAT Phytochemical identifier:  ')[1].split('Phytochemical name:  ')[0]
    except:
        impat_type = 'NA'
    try:
        phytochmecial = div.split('Phytochemical name:  ')[1].split('Synonymous chemical names:')[0]
    except:
        phytochmecial = 'NA'
    try:
        Synonymous_chemical_names = div.split('Synonymous chemical names:')[1].split('External chemical identifiers:')[0]
    except:
        Synonymous_chemical_names = 'NA'
    try:
        External_chemical_identifiers= div.split('External chemical identifiers:')[1].split('Chemical structure information')[0]
    except:
        External_chemical_identifiers    = 'NA'
    try:
        smiles = div.split('SMILES:')[1].split('InChI:')[0]
    except:
        smiles = 'NA'
    try:
        InChI = div.split('InChI:')[1].split('InChIKey')[0]
    except:
        InChI = 'NA'
    try:
        InChIKey = div.split('InChIKey:')[1].split('DeepSMILES:')[0]
    except:
        InChIKey = 'NA'
    try:
        DeepSMILES = div.split('DeepSMILES:')[1].split('Functional groups:')[0]
    except:
        DeepSMILES = 'NA'
    try:
        Functional_groups= div.split('Functional groups:')[1].split('Molecular scaffolds')[0]
    except:
        Functional_groups = 'NA'
    try:
        ClassyFire_Kingdom = div.split('ClassyFire Kingdom:')[1].split('ClassyFire Superclass:')[0].strip()
    except:
        ClassyFire_Kingdom = 'NA'
    try:
        # ClassyFire_Superclass = div.split('ClassyFire Superclass:')[1].split('ClassyFire Class:')[0].strip()
        ClassyFire_Superclass = div.split('ClassyFire Superclass:')[1].split('ClassyFire Class:')[0].strip()
    except Exception as e:
        print(e)
        ClassyFire_Superclass = 'NA'
    try:
        ClassyFire_Class = div.split('ClassyFire Class:')[1].split('ClassyFire Subclass:')[0].strip()
    except:
        ClassyFire_Class = 'NA'
    try:
        ClassyFire_Subclass = div.split('ClassyFire Subclass:')[1].split('NP Classifier Biosynthetic pathway: ')[0].strip()
    except:
        ClassyFire_Subclass = 'NA'

    try:
        NP_Classifier_Biosynthetic_pathway = div.split('NP Classifier Biosynthetic pathway:')[1].split('NP Classifier Superclass: ')[0].strip()
    except:
        NP_Classifier_Biosynthetic_pathway = 'NA'
    try:
        NP_Classifier_Superclass = div.split('NP Classifier Superclass:')[1].split('NP Classifier Class:')[0].strip()
    except:
        NP_Classifier_Superclass = 'NA'
    try:
        NP_Classifier_Class = div.split('NP Classifier Class:')[1].split('NP-Likeness score:')[0].strip()
    except:
        NP_Classifier_Class = 'NA' 
    try:
        NP_Likeness_score = div.split('NP-Likeness score:')[1].split('Chemical structure download')[0].strip()
    except:
        NP_Likeness_score = 'NA'
    mol_list = soup.select('div.buttonlink.ml-2 a')
    for mol in mol_list:
        mol_name = mol.string
        if '2D' in mol_name:
            mol_url = mol['href']
            mol_url2 = f'https://cb.imsc.res.in{mol_url}'
            mol_file_name = mol_url.split('/')[-1]
            while True:
                try:
                    urllib.request.urlretrieve(mol_url2, f'mol_files\\{mol_file_name}')
                    break
                except:
                    time.sleep(1)
                    continue
    
    with file_write_lock:
        with open('output.csv','a',newline='',encoding='utf8') as f:
            writer=csv.writer(f)
            mystuff = [impat_type,phytochmecial,Synonymous_chemical_names,External_chemical_identifiers,smiles,InChI,InChIKey,DeepSMILES,Functional_groups,ClassyFire_Kingdom,ClassyFire_Superclass,ClassyFire_Class,ClassyFire_Subclass,NP_Classifier_Biosynthetic_pathway,NP_Classifier_Superclass,NP_Classifier_Class,NP_Likeness_score]
            writer.writerow(mystuff)
page_list = pagination_creator(17968)

for page in page_list:
    print(page)
    download(page)