import json
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


def text(links):
    for elem in links:
        result = elem.text.strip()
        break

    return result


url = 'https://www.biblio-globus.ru/catalog/categories'
catalog = requests.get(url)
catalog_soup = BeautifulSoup(catalog.text, 'lxml')
list_categories = catalog_soup.find_all('li', class_='list-group-item')

df = []
columns = ['product_url', 'image', 'author', 'title', 'annotation', 'genre']


for link in tqdm(list_categories):

    category_url = 'https://www.biblio-globus.ru' + link.find('a')['href']
    category_page = requests.get(category_url)
    category_soup = BeautifulSoup(category_page.text, 'lxml')    
    list_subcategories = category_soup.find_all('a', class_='product-preview-title')

    n = 1
    for sub in tqdm(list_subcategories):
        
        subcategory_id = sub['href'].split('/')[-1]

        page = 1
        while True:
            
            subcategiry_url = f'https://www.biblio-globus.ru/catalog/category?id={subcategory_id}&page={page}&sort=0'
            subcategiry_page = requests.get(subcategiry_url)
            subcategiry_soup = BeautifulSoup(subcategiry_page.text, 'lxml')
            subcategiry_links = subcategiry_soup.find_all('div', class_='text')
            if not subcategiry_links:
                break

            for product in subcategiry_links:
                product_url = 'https://www.biblio-globus.ru' + product.find('a')['href']
                product_page = requests.get(product_url)
                product_soup = BeautifulSoup(product_page.text, 'lxml')
                product_annotation = product_soup.find('div', id='collapseExample')
                if product_annotation:
                    annotation = ''.join([symbol for symbol in product_annotation.text if symbol not in ['\n', '\r', '\t', 'm', '\xa0']])
                    annotation = annotation.split('Характеристики', 1)[0]
                    annotation = annotation.strip()
                else:
                    annotation = None

                try:
                    product_json = product_soup.find('script', type='application/ld+json')
                    dict_json = json.loads(product_json.text)
                except (AttributeError, json.JSONDecodeError):
                    continue

                author = dict_json['author']['name']
                title = dict_json['name']
                image = dict_json['image']
                genre = dict_json['genre']
                df.append([product_url, image, author, title, annotation, genre])
            page += 1

        data = pd.DataFrame(df, columns=columns)
        data.to_csv(f'data{n}.csv', index=False)
        n += 1