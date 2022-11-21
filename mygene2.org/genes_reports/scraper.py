import requests

import urllib.request

response = requests.get('https://mygene2.org/MyGene2/api/search/familycountbygenes').json()

for row in response:
    nameOfGene = row['nameOfGene']
    reportExists = row['reportExists']
    print(nameOfGene,reportExists)
    if reportExists:
        response = requests.get(f'https://mygene2.org/MyGene2/api/public/report/{nameOfGene}').json()
        familyInfo = response['familyInfo']
        for family in familyInfo:
            hasVcf = family['hasVcf']
            hasBam = family['hasBam']
            if hasVcf or hasBam:
                urllib.request.urlretrieve(f'https://mygene2.org/MyGene2/api/data/export/{nameOfGene}', f"{nameOfGene}.csv")


