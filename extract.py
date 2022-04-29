import requests
import re
from bs4 import BeautifulSoup


def check_for_valid_url(url):

    #if url returns status code 200 return true
    try:        
        response=requests.get(url)        
        if response.status_code==200:
            return True
        else:
            print(response.status_code)
            return False
    except:
        print('wrong url')
        return False

def get_numbers(content):
    phones=[]
    clean_phones=[]
    return_phones=[]  
    #find all numbers on web page that could be phone numbers
    numbers=re.findall(r'[+]*[\s(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\)\(/0-9]*[0-9]{1}',content.text)

    for e in numbers:
        en=e.split("\n") 

        for e in en:
            #check for length of number and format
            if len(e.strip())>=8 and len(e.strip())<24:                
                phone=re.findall(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\)\(/0-9]*$', e.strip())
                if phone and phone not in phones:
                    phones.append(phone[0])                                   

    #check for dupicated phone numbers
    for phone in phones:
        if phone.replace(" ","") not in clean_phones:
            clean_phones.append(phone.replace(" ",""))
            return_phones.append(phone)

    return return_phones

def get_logo(content,url):
    regex = re.compile('.*logo.*',re.IGNORECASE)    
    logos=[]
    return_logo=''
    clean_url=url
    #find img element with class that contains "logo"
    for logo in content.find_all("img", {"class" : regex}):   
        if logo:    
            logos.append(logo)

    try:
        if not logos:
            for i in content.find(class_=regex):
                try:
                    if i["src"]:
                        logos.append(i)
                except:
                    pass
    except:
        pass
    
    try:
        if not logos:    
            for i in content.find(id=regex):
                try:
                    if i["src"]:
                        logos.append(i)
                except:
                    pass
    except:
        pass

    if not logos:
        for logo in content.find_all("img", {"src" : regex}):   
            if logo:    
                logos.append(logo)


    if url[0:5]=='https':
        clean_url=url[8:]
    elif url[0:4]=='http':
        clean_url=url[7:]   
    

    if len(logos)!=0:
        if logos[0]["src"][0:2]=='//':
            return_logo="https:"+logos[0]["src"]
        elif logos[0]["src"][0]=='/':
            return_logo=clean_url[0:clean_url.find('/')]+logos[0]["src"]
        else:
            return_logo=logos[0]["src"]



    return return_logo

def main():


    #ask for URL until url is valid
    valid_url=False
    while not valid_url:
        url = input("Enter url: ").lower()
        valid_url=check_for_valid_url(url)
            
    response=requests.get(url)
    content=BeautifulSoup(response.content,'html.parser')

    phone_numbers=get_numbers(content)

    if phone_numbers:
        for phone in phone_numbers:
            print(phone)
    else:
        print("none")

    logo=get_logo(content,url)
    if logo:
        print(logo)
    else:
        print("none")



main()