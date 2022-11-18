import requests
from bs4 import BeautifulSoup
import concurrent.futures,time
from tqdm import tqdm
import threading

file_write_lock = threading.Lock()

def pagination_creator(last_page):
    page_list = []
    last_page = last_page+1
    for page in range(1,last_page):
        url = f'https://opensnp.org/snps?page={page}'
        page_list.append(url)
    return page_list


def page_parser(url):
    while True:
        try:
            response = requests.get(url)
            break
        except:
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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(download, line_list), total=len(line_list)))
    return results

if __name__ == "__main__":
    page_list = pagination_creator(320000)
    run(page_parser,page_list)