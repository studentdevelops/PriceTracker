import requests
from bs4 import BeautifulSoup
from os import path
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55"}

global filename, urlfile

def urls():
    """gets the url in url file provided by user

    Returns:
        list: list of urls
    """
    with open(urlfile,'r') as f:
        urls = [str(i.replace('\n','')) for i in f.readlines()]
    return urls

def file(url,name,price):
    """processes the file, updates new prices shows old prices,
    if link doesnt exists then adds the link to the file with
    product name and price

    Args:
        url (String): Url link to the product
        name (String): Name of the product
        price (String): price of the product, kept string so that could be processed
    """
    
    if(path.exists(filename)==False or path.getsize(filename) == 0):
        with open(filename, 'w') as f:
            f.write('url,name,prices \n')

    if(path.exists(filename) and path,path.getsize(filename) >= 18):
        with open(filename,'r') as f:
            lines = f.readlines()
            flag = False
            for line in lines:
                if(url in line):
                    if(price not in line):
                        lines[lines.index(line)] = line.replace('\n' , '') + ',' + str(price) + '\n'
                    flag = True
            if(flag==False):
                lines.append(f'{url},{name},{price} \n')

        with open(filename, 'w') as f:
            f.writelines(lines)


# flipkart
def flipkart(soup):
    """process web pages from flipkart

    Args:
        soup (object): soup object that contains the page content
    """
    # title class "B_NuCI"
    titleClass = "B_NuCI"
    title = str(soup.find(class_=titleClass).getText()).strip().replace(',','')

    # current price class "_30jeq3 _16Jk6d"
    currentPriceClass = "_30jeq3 _16Jk6d"
    cprice = str(soup.find(class_=currentPriceClass).getText()).strip()
    # removing everything except number, flipkart doesnt include digits post decimals
    cprice = re.sub('\D','',cprice)
    file(urls[i],title,cprice)


# amazon
def amazon(soup):
    """processes web pages from amazon

    Args:
        soup (object): soup object that contains the page content
    """
    titletag = 'productTitle'
    title = str(soup.find(id=titletag).getText()).strip().replace(',','')

    cpricetag = 'priceblock_ourprice'
    cprice = str(soup.find(id=cpricetag).getText()).strip()
    # removing everything except number till the decimal in the string,
    #  amazons keeps degits post decimals
    cprice = re.sub('\D','',cprice[:cprice.find(".")])

    file(urls[i],title,cprice)


# main driver code

    """main Driver code
    uses request package to sent reqests to server using the url
    and stores the returned page in a object
    the object is then given to bs4 for further processing with just page content as just html
    """

print("ex. filename.csv")
# filename = input("Enter Output Filename: ")
filename = 'prices.csv'
# urlfile = input("Enter URL Filename: ")
urlfile = 'urls.txt'

urls = urls()
for i in range(len(urls)):
    page = requests.get(urls[i], headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    if('flipkart' in urls[i]):
        flipkart(soup)
    elif('amazon' in urls[i]):
        amazon(soup)