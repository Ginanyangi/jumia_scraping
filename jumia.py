import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.jumia.co.ke/'

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'html.parser')
        return soup
    else:
        print(f"Failed to retrive content from {url}")
        return None
    
def get_product_links(soup):
    links = []
    product_link_elements = soup.select('a.core')

    for link_element in product_link_elements:
        link = link_element.get('href')
        

    #if link.startswith('/'):
        #link (f'{url}{link}')
        
    links.append(link)
    return links

def get_product_name(soup):
    name = soup.select_one('div.name').text
    return name

def get_product_brand(soup):
    brand = soup.select_one('data-ga4-item_brand').text
    return brand

def get_product_price(soup):
    price = soup.select_one('data-oprc').text
    return price

def get_product_discount(soup):
    discount = soup.select_one('data-ga4-discount').text
    return discount
    
#def get_product_reviews(soup):
    #discount = soup.select_one('CSS_SELECTOR_FOR_PRODUCT_DISCOUNT').text
    #return discount

#def get_product_rating(soup):
   # rating = soup.select_one('CSS_SELECTOR_FOR_PRODUCT_RATING').text
    #return rating

def scrape_and_save_data(url, filename='jumia.csv'):
    homepage_soup = get_page_content(url)

    product_links = get_product_links(homepage_soup)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name','brand','price','discount','rating'])

        for link in product_links:
            product_soup = get_page_content(link)
            name = get_product_name(product_soup)
            brand = get_product_brand(product_soup)
            price = get_product_price(product_soup)
            discount = get_product_discount(product_soup)
           # rating = get_product_rating(product_soup)

            writer.writerow([name,brand,price,discount])

        print('Data scraping and saving complete')
       
jumia_url = 'https://www.jumia.co.ke/'


scrape_and_save_data(jumia_url)