import datetime
import time
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver

url = 'https://www.tokopedia.com/p/handphone-tablet/handphone?page='
links = {}
dictMerchant = {}
dictStar = {}
dictProdName = {}
dictDescription = {}
dictPrice = {}
dictImage = {}

headers ={
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                   '(KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
}


driver = webdriver.Chrome(r'your chrome driver full path')
count = 0
for page in range(1,21):
    # print("Scraping link of the products in page: " + str(page))
    req = requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    product = soup.findAll('div', class_='css-bk6tzz e1nlzfl3')

    for i in product:
        link = i.find('a', class_='css-89jnbj')['href']
        if 'ta.tokopedia.com' in link:
            pass
        else:
            count += 1
            driver.maximize_window()
            driver.get(link)
            time.sleep(2)
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, "html.parser")
            name = soup.find('h1', {'data-testid': 'lblPDPDetailProductName'}).text
            dictProdName[count] = name
            try:
                description = soup.find('div', {'data-testid': 'lblPDPDescriptionProduk'}).text
                dictDescription[count] = description
            except:
                dictDescription[count] = "No Description"
            img = soup.find('img', class_='success fade')['src']
            dictImage[count] = img
            price = soup.find('div', class_='price').text
            dictPrice[count] = price
            rating = soup.find('span', {'data-testid': 'lblPDPDetailProductRatingNumber'}).text
            dictStar[count] = rating
            merchant = soup.find('a', class_='css-1n8curp').find('h2').text
            dictMerchant[count] = merchant
            print(f"Success to scrape product #{count}")

driver.quit()

data = []

print("Please wait while I'm writing the data into CSV")
for i in range(1, 101):
    data.append([dictProdName[i], dictDescription[i], dictImage[i], dictPrice[i],dictStar[i],dictMerchant[i]])

now = datetime.date.today()
headerCSV = ['Name of Product', 'Description', 'Image Link', 'Price', 'Rating', 'Name of Merchant']
writer = csv.writer(open(f'Result/Result of Web Scrape from Tokopedia {now}.csv', 'w', newline = '', encoding="utf-8"), lineterminator='\n')
writer.writerow(headerCSV)
for d in data:
    writer.writerow(d)
print("Success to scrape the List of Handphone from Tokopedia Website")
