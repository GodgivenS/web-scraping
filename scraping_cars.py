from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd  
import time
import xlsxwriter

website = 'http://www.autotrader.co.uk'
make = "Audi"
records = []

for i in range(1, 49):
	url = 'http://www.autotrader.co.uk/car-search?sort=sponsored&postcode=w1a0ax&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&make=AUDI&year-from=2013&maximum-mileage=40000&seller-type=private&page={}'.format(i)
	r = uReq(url)
	page_html = r.read()
	r.close()
	page_soup = soup(page_html, 'html.parser')
	containers = page_soup.find_all('li', attrs={'class':'search-page__result'})

	for container in containers:
		time.sleep(2)
		item_adress = container.find('a', attrs={'class':'listing-fpa-link'})["href"]

		item_r = uReq(website + item_adress)
		item_page_html = item_r.read()
		item_r.close()
		item_page_soup = soup(item_page_html, 'html.parser')
		model = item_page_soup.find('span', attrs={'class':'pricetitle__advertTitle'}).text[5:]
		price = item_page_soup.find('section', attrs={'class':'priceTitle__price gui-advert-price'}).text[1:]
		mileage = item_page_soup.find_all('li', attrs={'class':'keyFacts__item'})[2].text[:-6]
		phone = item_page_soup.find('div', attrs={'itemprop':'telephone'}).text
		records.append((make, model, price, mileage, phone))

	print("page " + str(i) + " from 48 done")

df = pd.DataFrame(records, columns=['Make', 'Model', 'Price', 'Mileage', 'Telephone Number'])  
writer = pd.ExcelWriter('Audi.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False, sheet_name='Sheet1') 
writer.save()

print("Done")