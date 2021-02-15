import requests
import sys
from bs4 import BeautifulSoup

keys=[]
with open (sys.argv[1], 'rt', encoding='utf-8') as fr:
    reading=fr.readlines()
    for line in reading:
        line=line.strip()
        keys.append(line)

list_present=["presfut_sg1","presfut_sg2","presfut_sg3","presfut_pl1","presfut_pl2","presfut_pl3"]

with open (sys.argv[2], 'wt', encoding="utf-8") as fw:
    head="russian_verb"+"\t"+"english_verb"+"\t"+"verb stress"+"\t"+"я"+"\t"+"ты"+"\t"+"он/она́/оно́"+"\t"+"мы"+"\t"+"вы"+"\t"+"они́"+"\n"
    fw.write(head)
    for key in keys:
        print (key, "start")
        url = 'https://en.openrussian.org/ru/'+key
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            soup=soup.decode('cp949','ignore')
            soup=soup.split("\n")
            count, with_mark_second, english=0,0,0
            list_word=[]
            for line in soup:
                count+=1
                if line.count('<meta content="Translation:')>0:
                    english=line.split('<meta content="Translation:')[1].split('.')[0]
                if line.count('<li class="version-2" data-version="2">')>0:
                    try:
                        with_mark_second=soup[count].split("Verb ")[1]
                    except:
                        continue
                if line.count('<div class="section basics">')>0:
                    with_mark=soup[count+5].strip()
                for present_one in list_present:
                    if line.count(present_one)>0:
                        list_word.append(soup[count])
                if len(list_word)==6:
                    string=key+"\t"+english+"\t"+with_mark+"\t"+"\t".join(list_word)+"\n"
                    fw.write(string)
                    list_word=[]
                    if with_mark_second!=0:
                        with_mark=with_mark_second
                        with_mark_second=0
                        continue
            if english==0:
                fw.write(key)
                fw.write("\n")
        else :
            error_message=key+"error"+response.status_code
            fw.write(error_message)
            print(response.status_code)
