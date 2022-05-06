from bs4 import BeautifulSoup
from jmespath import search
import requests
import json
import re
output=[]
for x in range(3):
    html_text=requests.get("https://www.olx.ro/locuri-de-munca/?page={x}").text
    soup=BeautifulSoup(html_text,'lxml')
    jobs=soup.find_all("tr",class_="wrap")
    for job in jobs:
        link=job.find("a").get("href")

        jobName=job.strong.text
        tipJob=job.find("small",class_="breadcrumb breadcrumb--job-type x-normal").text.replace(' ','')

        tipJob=tipJob.replace("\n","")
        locatieJob=job.find("small",class_="breadcrumb x-normal").text.replace("\n","")

        jobName=jobName.replace("\u00e2","a")
        jobName=jobName.replace("\u021b","t")
        jobName=jobName.replace("\u0219","s")
        jobName=jobName.replace("\u2019","'")
        jobName=jobName.replace("\u00ee","i")
        jobName=jobName.replace("\u2022\t","i")
        jobName=jobName.replace("\u0103","a")
        jobName=jobName.replace("\u0102"," ")
        jobName=jobName.replace("\u2013"," ")        
        html_text2=requests.get(link).text
        soup1=BeautifulSoup(html_text2,'lxml')
  
        programWeekend=False
        limbaEngleza=False
        ron=False
        euro=False
        limbaGermana=False
        isCuvCheie=False
        cuvCheie=""
        bonuriDeMasa=False
        aerLiber=False
    
        if(soup1.find("div",class_="css-2t3g1w-Text")):
            descriere=soup1.find("div",class_="css-2t3g1w-Text").text.replace("\u0103","a")
            descriere=descriere.replace("\u00e2","a")
            descriere=descriere.replace("\u021b","t")
            descriere=descriere.replace("\u0219","s")
            descriere=descriere.replace("\u2019","'")
            descriere=descriere.replace("\u00ee","i")
            descriere=descriere.replace("\u2022\t","i")
            descriere=descriere.replace("\u00a0"," ")
            descriere=descriere.replace("\u0102"," ")
            descriere=descriere.replace("\u2022"," ")    
            descriere=descriere.replace("\u00ce"," ")


            isEuro=re.search("euro|Euro|EURO",descriere)
            isRon=re.search("lei|Ron|ron|Lei|RON|LEI",descriere)
            isProgramWeekend=re.search("weekend|sambata|duminica",descriere)
            isEngleza=re.search("/([E]||[e]&&[n]||[N]&&[G]||[g]&&[L]||[l]&&[E]||[e]&&[Z]||[z]&&[A][a])\w",descriere)
            isGermana=re.search("germana|Germana|GERMANA",descriere)
            isCuvCheieDescriere=re.search(cuvCheie,descriere)
            isCuvCheieJobTitle=re.search(cuvCheie,jobName)
            isBonuriDeMasa=re.search("bonuri|tichete|Bonuri|Tichete",descriere)
            isAerLiber=re.search("aer liber|AER LIBER|Aer liber",descriere)
            if isProgramWeekend:
                programWeekend=True
            if isEngleza:
                limbaEngleza=True
            if isRon:
                ron=True
            if isEuro:
                euro=True
            if isGermana:
                limbaGermana=True
            if isCuvCheieDescriere or isCuvCheieJobTitle:
                isCuvCheie=True
            if isBonuriDeMasa:
                bonuriDeMasa=True
            if isAerLiber:
                aerLiber=True
        else:
            descriere=""
        d={}
        d["numeJob"]=jobName
        d["descriere"]=descriere
        d["tipJob"]=tipJob
        d["locatieJob"]=locatieJob
        d["programWeekend"]=programWeekend
        d["limbaEngleza"]=limbaEngleza
        d["limbaGermana"]=limbaGermana
        d["ron"]=ron
        d["euro"]=euro
        d["cuvCheie"]=cuvCheie
        d["bonuriDeMasa"]=bonuriDeMasa
        d["aerLiber"]=aerLiber
        if(limbaEngleza):
            output.append(d)
json_object = json.dumps(output, indent = 3)  
print(output) 
with open('file.json', 'w') as f:
    f.write(json_object)
