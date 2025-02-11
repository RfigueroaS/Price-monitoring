import requests
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
from io import StringIO
import pandas as pd
def scrape_amazon(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extraer nombre y precio
    product_name = soup.select_one("#productTitle").get_text().strip()
    product_price = soup.select_one(".a-price-whole").get_text().strip()
    
    return {"name": product_name, "price": product_price}

def transform_data(data):
    # Convertir precio a número (ej: "$1,000" → 1000.0)
    cleaned_price = float(data["price"].replace("$", "").replace(",", ""))
    return {
        "name": data["name"],
        "price": cleaned_price,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

#Subir los datos a AWS S3 usando boto3
def upload_to_s3(data, bucket_name, file_name):
    s3 = boto3.client("s3")
    csv_buffer = StringIO()
    df = pd.DataFrame([data])
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=f"{file_name}.csv", Body=csv_buffer.getvalue())