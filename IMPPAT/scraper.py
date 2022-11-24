import requests
from bs4 import BeautifulSoup
import concurrent.futures,time
from tqdm import tqdm
import threading

file_write_lock = threading.Lock()

def pagination_creator(last_page): #017968
    page_list = []
    last_page = last_page
    
    for page in range(1,last_page):
        url = f'https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY{page}'
        page_list.append(url)
    return page_list

def page_parser(url):
    while True:
        try:
            response = requests.get(url)
            if 'This website is under heavy load (queue full)' in response.text:
                time.sleep(3)
                continue
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            continue

    soup = BeautifulSoup(response.text,'lxml')

    table = soup.select('table#no_snp_overview tr')
    header_check = 0
    for tr in table:
        if header_check == 0:
            header_check+=1
            continue

        td = tr.select('td')
        snp_id = td[0].string
        name = td[1].string
        position = td[2].string
        chromosome = td[3].string
        your_genotype = td[4].string
        ranking = td[5].string
        with file_write_lock:
            result_row = u'{}|{}|{}|{}|{}|{}\n'.format(snp_id,name,position,chromosome,your_genotype,ranking)
            result_row = result_row.replace('\n','')
            result_row = f'{result_row}\n'
            with open('first_data.csv','a',encoding='utf8') as file:
                file.write(result_row)

def run(download, line_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        results = list(tqdm(executor.map(download, line_list), total=len(line_list)))
    return results