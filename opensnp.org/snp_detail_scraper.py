import requests
from bs4 import BeautifulSoup
import concurrent.futures,time
from tqdm import tqdm
import threading
import json

result_lck = threading.Lock()

def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele + ';'
 
    # return string
    return str1


def download(row):
        ids = row.split('|')[1]
        try:
            while True:
                try:
                    response = requests.get(f'https://opensnp.org/snps/{ids}')

                    if 'This website is under heavy load (queue full)' in response.text:
                        time.sleep(3)
                        continue
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue
            r = response.text
            start_freq_data = 'freq_data=['
            end_freq_data = "var plot1 = jQuery.jqplot ('freq_chart', [freq_data],"
            freq_data = r[r.find(start_freq_data)+len(start_freq_data):r.rfind(end_freq_data)].replace('   ','').replace('\r','').replace('\t','').replace('\n','').replace('];','').strip()
            freq_data = '['+str(freq_data)+']'
            freq_data = freq_data.replace("'",'"')
            freq_data = json.loads(freq_data)
            freq_list = []
            for freq in freq_data:
                freq_name = freq[0]
                freq_value = freq[1]
                freq = f'{freq_name} : {freq_value}'
                freq_list.append(freq)

            start_allele = 'var allele_data=['
            end_allele = "var plot2 = jQuery.jqplot ('allele_chart', [allele_data],"
            allele_data = r[r.find(start_allele)+len(start_allele):r.rfind(end_allele)].replace('   ','').replace('\r','').replace('\t','').replace('\n','').replace('];','').strip()
            allele_data = '['+str(allele_data)+']'
            allele_data = allele_data.replace("'",'"')
            allele_data = json.loads(allele_data)
            allele_list = []
            for allele in allele_data:
                allele_name = allele[0]
                allele_value = allele[1]
                allele = f'{allele_name} : {allele_value}'
                allele_list.append(allele)

            allele_list = listToString(allele_list)[0:-1]
            freq_list = listToString(freq_list)[0:-1]
            result_row = f'{row}|{allele_list}|{freq_list}\n'
            with result_lck:
                with open('result_data.csv','a',encoding='utf8') as file:
                    file.write(result_row)
        except:
            result_row = f'{row}\n'
            with result_lck:
                with open('error.csv','a',encoding='utf8') as file:
                    file.write(result_row)

def run(download, line_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        results = list(tqdm(executor.map(download, line_list), total=len(line_list)))
    return results
if __name__ == "__main__":
    with open('first_data.csv','r',encoding='utf8') as fp:
        fp = fp.read().split('\n')
    start = 0
    end = 1000
    for i in range(1,3300):
        print(start,end)
        run(download,fp[start:end])

        start+=1000
        end+=1000