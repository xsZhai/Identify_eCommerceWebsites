import requests
import pandas as pd
import re
from lxml import html

with open('isvWebs.csv') as f:
    webs=f.read().split('\n')

def toDomain(link):
    import re
    return (re.sub(r'^(https?://)?(www\d?\.)?','', link).split('/')+[''])[0].strip()


def ecommerce(web):
    web=toDomain(web)
    try:
        res=requests.get('https://www.'+web)
        XurlText="//*[@href]//text()"
        urlTexts=html.fromstring(res.content).xpath(XurlText)
    except Exception as e:
        print(e)
        return
    for text in urlTexts:
        if len(text)<10:
            if re.findall(r'\bcart\b|\bshop\b|\bbuy\b|\bpurchase\b', text, re.I):
                result={}
                result['web']=web
                result['ecommerce']='1'
                df=pd.DataFrame([result])
                df.to_csv('ecommerceCheck1119.csv',mode='a',index=0,header=False)
                return
    
    Xurls="//@href"
    urls=html.fromstring(res.content).xpath(Xurls)

    for url in urls:
        
        if web in url:
            try:
                res2=requests.get(url)
                urlTexts2=html.fromstring(res2.content).xpath(XurlText)
            except Exception as e:
                print(e)
                continue
            for text2 in urlTexts2:
                if len(text2)<10:

                    if re.findall(r'\bcart\b|\bshop\b|\bbuy\b|\bpurchase\b', text2, re.I):
                        result={}
                        result['web']=web
                        result['ecommerce']='1'
                        df=pd.DataFrame([result])
                        df.to_csv('ecommerceCheck1119.csv',mode='a',index=0,header=False)
                        return
        if url:
            if url[0]=="/":
                try:
                    res2=requests.get('https://www.'+web+url)
                    urlTexts2=html.fromstring(res2.content).xpath(XurlText)
                except Exception as e:
                    print(e)
                    continue
                for text2 in urlTexts2:
                    if len(text2)<10:

                        if re.findall(r'\bcart\b|\bshop\b|\bbuy\b|\bpurchase\b', text2, re.I):
                            result={}
                            result['web']=web
                            result['ecommerce']='1'
                            df=pd.DataFrame([result])
                            df.to_csv('ecommerceCheck1119.csv',mode='a',index=0,header=False)
                            return
    return

for web in webs:
 
    try:
        ecommerce(web)
    except Exception as e:
        print(e)
        continue
  

print('---------done---------')
