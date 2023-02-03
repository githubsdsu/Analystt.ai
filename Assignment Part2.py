import requests
from bs4 import BeautifulSoup
import csv 

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
csv_rows=[]
csv_header=['Description','ASIN','Product Description','Manufacturer']
query=list(range(1,21))
for n in range(len(query)):
    r = requests.get(f'https://www.amazon.in/s?k=bags&page={query[n]}', headers=headers)
    htmlcontent=r.content
    soup=BeautifulSoup(htmlcontent,'html.parser')
    producturls=soup.find_all('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    product_url_list=[]

    for z in producturls:
        ans=z.get('href')
        ans='https://www.amazon.in/'+ans
        #print(ans)
        product_url_list.append(ans)  

    
    asin_list=[]
    manufacture_list=[]
    description_list=[]
    productdescription_list=[]
    for z in range(len(product_url_list)):

            #print(product_url_list[z])
            r1 = requests.get(product_url_list[z], headers=headers)
            htmlcontent=r1.content
            soup1=BeautifulSoup(htmlcontent,'html.parser')

            data=soup1.find('div',{'id':'detailBullets_feature_div'})
            
            if data!=None:
                datalist=data.get_text().split()
                index1=datalist.index('ASIN')
               # print(datalist)
                #print(index1)
                asinnoindex=index1
                asinno=datalist[asinnoindex+4]
                asin_list.append(asinno)
                difflist=[]
                manufactureindexlist=[]
                manufacturevalue=0
                #print(asin_list)
                for y in range(len(datalist)):
                    if datalist[y]=='Manufacturer':
                        manufactureindexlist.append(y)
                if len(manufactureindexlist)==1:
                    manufacturevalue=manufactureindexlist[0]
                    value=datalist[manufacturevalue+4:asinnoindex]
                    value=''.join(value)
                    manufacture_list.append(value)    
                    
                elif len(manufactureindexlist)>1:
                    for a in manufactureindexlist:
                        if a<asinnoindex:
                            manufacturevalue=a 
                            value=datalist[manufacturevalue+4:asinnoindex]
                            value=''.join(value)
                            manufacture_list.append(value)    
                
                #print(asinno)
                else:
                    manufacture_list.append('None')
                   
               
            else:
                asin_list.append('None')
            newdatadescription=soup1.find('ul',{'class':'a-unordered-list a-vertical a-spacing-mini'})
            if newdatadescription==None:
                description_list.append('None')
        
            else: 
                newdatadescriptiontext=newdatadescription.get_text()
                description_list.append(newdatadescriptiontext)
            
            productdesription=soup1.find('div',{'id':'productDescription_feature_div'})
            if productdesription==None:
                productdescription_list.append('None')
            else: 
                productdesriptiontext=productdesription.get_text()
                
                
                
                productdescription_list.append(productdesriptiontext)
                # print(productdesriptiontext)
                
         
            #print(asin_list)
            #print(productdescription_list)
            #print(manufacture_list)
            #print(description_list)    
    with open('Assignment Part 2.csv','w',encoding='UTF8',newline='') as f: 
        csvwriter=csv.writer(f)
        csvwriter.writerow(csv_header)
        try:
            for x in range(len(asin_list)):
                csv_rows.append([description_list[x],asin_list[x],productdescription_list[x],manufacture_list[x]])
                        
                csvwriter.writerows(csv_rows)
        except Exception as e:
            print(e)