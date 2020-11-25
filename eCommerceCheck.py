import requests
import pandas as pd
import re
from lxml import html

with open('isvWebsAll.csv') as f:
    webs=f.read().split('\n')

def toDomain(link):
    import re
    return (re.sub(r'^(https?://)?(www\d?\.)?','', link).split('/')+[''])[0].strip()



def ecommerce(web):
    web=toDomain(web)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    try:
        res=requests.get('https://www.'+web,timeout=60,headers=headers)
        XurlText="//*[@href]//text()"
        urlTexts=html.fromstring(res.content).xpath(XurlText)
    except Exception as e:
        print(e)
        return
    for text in urlTexts:
        if len(text)<10:
            if re.findall(r'\bcart\b|\bshop\b|\bbuy\b|\bpurchase\b|\btrial\b|\bpricing\b|\bsupport\b|\bget started\b|\bproduct\b', text, re.I):
                result={}
                result['web']=web
                result['ecommerce']='1'
                df=pd.DataFrame([result])
                df.to_csv('ecommerceCheck1125.csv',mode='a',index=0,header=False)
                return

for web in webs:
 
    try:
        ecommerce(web)
    except Exception as e:
        print(e)
        continue
  

print('---------done---------')
