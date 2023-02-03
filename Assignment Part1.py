import requests
from bs4 import BeautifulSoup
import csv 
import re 
order='r[0-9]'
query=list(range(1,21))

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

csv_header=['Product URL','Product Name','Product Price','Rating','Number of reviews']



csv_rows=[]
for n in range(len(query)):
    
    r = requests.get(f'https://www.amazon.in/s?k=bags&page={query[n]}', headers=headers)
    htmlcontent=r.content
    #url=f'https://www.amazon.in/s?k=bags&page={2}'
    #print(url)
    soup=BeautifulSoup(htmlcontent,'html.parser')

   # names=soup.find_all('span',class_='a-size-medium a-color-base a-text-normal')
   
    producturls=soup.find_all('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    prices=soup.find_all('a',class_='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    rating_list=[]
    number_review=[]
    product_name_list=[]
    product_price_list=[]
    product_url_list=[]
    newnameslist=[]


        
    for z in producturls:
        ans=z.get('href')
        ans='https://www.amazon.in/'+ans
       # print(ans)
        product_url_list.append(ans)  


    for z in range(len(product_url_list)):

        try:
            r1 = requests.get(product_url_list[z], headers=headers)
            htmlcontent=r1.content
            soup1=BeautifulSoup(htmlcontent,'html.parser')
            
            cost=soup1.find('div',{'class':'a-section a-spacing-none aok-align-center'})
            if cost==None: 
                product_url_list.remove(product_url_list[z])
            else:    
                value=cost.get_text()
                splitvalue=value.split('₹')
            # print(splitvalue[1])
                product_price_list.append(splitvalue[1])
         # rating=soup.find('span',class_='a-size-medium a-color-base a-text-beside-button a-text-bold')
                reviews=soup1.find('div',{"id": "averageCustomerReviews"})
            # print(rating)
                if reviews==None:
                    rating_list.append('None')
                    number_review.append('None')
                else:    
                    ans=reviews.get_text()
                    anslist=ans.split()
                    rating_list.append(anslist[0])
                    number_review.append(anslist[-2])
                    #print(anslist) 
                names=soup1.find('div',{'id':'titleSection'})
                name=names.get_text()
                newnameslist.append(name)
                
             
                
        except Exception as e:
            print(e)
         

    with open('Assignment Part 1.csv','w',encoding='UTF8',newline='') as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(csv_header)
            for x in range(len(newnameslist)):
                
                
                if (x<len(product_url_list) and x<len(newnameslist) and x<len(product_price_list) and x<len(rating_list) and x<len(number_review)):
                    csv_rows.append([product_url_list[x],newnameslist[x],product_price_list[x],rating_list[x],number_review[x]])
                    
                    csvwriter.writerows(csv_rows)
        #product_price_list.append(splitvalue[1])  


       # print(ans)
       
 
    #print(len(product_name_list))

    
   # print(len(rating_list))    
    #print(len(rating_list))
    #print(len(number_review))
   
 


 
    
    

    


