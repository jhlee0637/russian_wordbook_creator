import requests
from bs4 import BeautifulSoup

keys=[]
with open ('keys.txt' 'r') as fr:
    reading=fr.readlines()
    for line in reading:
        line=line.strip()
        links.append(line)


for key in keys:
    url = 'https://en.openrussian.org/ru/'+key
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup=soup.decode('cp949','ignore')
        soup=soup.split("\n")
        count=0
        for line in soup:
            count+=1
            if line.count('<div class="section basics">')>0:
                with_mark=soup[count+5].strip()
            if line.count("Present")>0:
                print (key,"\t","\t",with_mark,"\t","\t".join((soup[count+8].split('/read/ru/')[1].split('" data-needs-pro')[0].split(","))))
                break
    else : 
        print(response.status_code)
