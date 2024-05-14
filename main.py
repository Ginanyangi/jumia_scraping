import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def extract_jumia_products(url):
    jumia = requests.get(url)
    soup = BeautifulSoup(jumia.content, 'html.parser')
    products = soup.find_all('article', class_='prd')
    data = []
    for product in products:
        try:
            product_name = product.find('div', class_='name').text.strip()
        except AttributeError:
            product_name = None
        try:
            brand_name = product.find('a', class_='brand').text.strip()
        except AttributeError:
            brand_name = None
        try:
            price_text = product.find('div', class_='prc').text.strip()
            price = float(price_text.split()[1].replace(',', ''))  # Extracting numerical value
        except (AttributeError, ValueError):
            price = None
        try:
            discount = product.find('div', class_='bdg_dsct').text.strip()
        except AttributeError:
            discount = None
        try:
            rating_tag = product.find('div', class_='stars _s')
            if rating_tag:
                rating_stars = rating_tag.find_all('i', class_='star full')
                original_rating = len(rating_stars) / 2
            else:
                original_rating = 0
        except AttributeError:
            original_rating = 0
        adjusted_rating = round((original_rating + 2.5) / 2, 2)
        try:
            total_reviews_text = product.find('span', class_='total_reviews').text.strip()
            total_reviews = int(total_reviews_text.split()[0])
        except (AttributeError, ValueError):
            total_reviews = 0
        popularity = "High" if total_reviews >= 100 else "Low"
        product_data = {
            'Product Name': product_name,
            'Brand Name': brand_name,
            'Price (Ksh)': price,
            'Discount (%)': discount,
            'Total Reviews': total_reviews,
            'Original Rating': original_rating,
            'Adjusted Rating': adjusted_rating,
            'Popularity': popularity
        }
        data.append(product_data)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = f'jumiaproducts{timestamp}.csv'  
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Product Name', 'Brand Name', 'Price (Ksh)', 'Discount (%)', 'Total Reviews', 'Original Rating', 'Adjusted Rating', 'Popularity']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
    print(f"Jumia products data added to '{csv_file_path}'")

if __name__ == "__main__":
    jumia_url = 'https://www.jumia.co.ke/'
    extract_jumia_products(jumia_url)