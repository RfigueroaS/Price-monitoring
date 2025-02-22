import os
import re
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'es-MX, es;q=0.9',
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    try:
        title = soup.find(id='productTitle').get_text(strip=True)
    except AttributeError:
        title = 'No se encontró el título del producto'

    try:
        image_url = soup.find('img', {'id': 'landingImage'})['src']
    except (AttributeError, ValueError):
        image_url = 'No se encontró la imagen del producto'

    try:
        price = soup.find(name='span', attrs={'class','a-offscreen'}).get_text()
    except (AttributeError, ValueError):
        price = 'No se encontró el precio del producto'

    return title, image_url, price

def save_image(image_url, product_name):
    folder = 'images'
    os.makedirs(folder, exist_ok=True)

    valid_file_name = re.sub(pattern=r'[<>"/\\|?*]', repl='', string=product_name)
    valid_file_name = valid_file_name[:10]
    filepath = os.path.join(folder, f'{valid_file_name}.jpg')

    base, ext = os.path.splitext(filepath)
    counter = 1
    while os.path.exists(filepath):
        filepath = f'{base}_{counter}{ext}'
        counter += 1

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    return None

def save_to_excel(data):
    df = pd.DataFrame(data)
    file_name= f"products.xlsx"

    if os.path.exists(file_name):
        existing_df = pd.read_excel(file_name)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(file_name, index=False)
    return file_name

def get_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'es-MX, es;q=0.9',
    }

    url = f"https://www.amazon.com/s?k={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    print(response.headers)

    product_links = []
    for link in soup.find_all(name='a', attrs={'class': 'a-link-normal s-line-clamp-2 s-link-style a-text-normal'}, href=True):
        product_links.append("https://www.amazon.com" + link['href'])

    return product_links


# Streamlit App
st.title('Amazon Scraper')

search_query = st.text_input("Ingresa el producto a buscar:")

if search_query:
    st.write(f"Buscando productos relacionados a '{search_query}'...")
    product_urls = get_search_results(search_query)

    if product_urls:
        all_data = []
        for url in product_urls[:10]:
            title, image_url, price = get_product_info(url)

            if title != 'No se encontró el título del producto':
                data = {
                    'fecha': datetime.now().strftime('%Y-%m-%d'),
                    'titulo': title,
                    'precio': price,
                    'URL Imagen': image_url,
                    'URL Producto': url,
                }
                all_data.append(data)

                if image_url:
                    save_image(image_url, title)
        if all_data:
            df = pd.DataFrame(all_data)
            st.write('### Resultados de la búsqueda:')
            st.dataframe(df.style.set_properties(**{'text-align': 'left'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}]
            ))

            ## Save to Excel
            file_name = save_to_excel(all_data)
            st.success(f'Los datos se guardaron en {file_name}')
        else:
            st.error('No se encontraron productos')
    else:
        st.error('No se encontraron resultados para la búsqueda')