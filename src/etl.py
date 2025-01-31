import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def request_to_api():
    API_KEY = os.getenv('API_KEY')
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY     
    }
    params = {
        "start": "1",     
        "limit": "50",    
        "convert": "GBP"  
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

def connect_to_db():
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

def extract(data):
    extracted_data = []
    for crypto in data['data']:
        el = {"name": crypto['name'],
              "symbol": crypto['symbol'],
              "max_supply": crypto['max_supply'],
              "circulating_supply": crypto['circulating_supply'],
              "price": crypto['quote']['GBP']['price'],
              "market_cap": crypto['quote']['GBP']['market_cap'],
              "market_cap_dominance": crypto['quote']['GBP']['market_cap_dominance'],
              "percentage_change_24h": crypto['quote']['GBP']['percent_change_24h'],
              "percentage_change_30d": crypto['quote']['GBP']['percent_change_30d']}
        extracted_data.append(el)
    return extracted_data

def transform(extracted_data):
    transformed_data = []
    for crypto in extracted_data:
        crypto['circulating_supply'] = round(crypto['circulating_supply'], 2)
        crypto['price'] = round(crypto['price'], 2)
        crypto['market_cap'] = round(crypto['market_cap'], 2)
        crypto['market_cap_dominance'] = round(crypto['market_cap_dominance'], 2)
        crypto['percentage_change_24h'] = round(crypto['percentage_change_24h'], 2)
        crypto['percentage_change_30d'] = round(crypto['percentage_change_30d'], 2)
        if crypto['max_supply'] is None:
            crypto['max_supply'] = 'Infinite'
        transformed_data.append(crypto)
    return transformed_data

def load(transformed_data):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS student.sn_crypto_data (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    symbol VARCHAR(10) NOT NULL,
                    max_supply VARCHAR(100),
                    circulating_supply DECIMAL(500,8),
                    price DECIMAL(30,8) NOT NULL,
                    market_cap DECIMAL(30,8),
                    market_cap_dominance DECIMAL(5,2),
                    percentage_change_24h DECIMAL(5,2),
                    percentage_change_30d DECIMAL(5,2),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   );""")
    
    insert_query = """INSERT INTO sn_crypto_data
    (name, symbol, max_supply, circulating_supply, price, market_cap, market_cap_dominance, percentage_change_24h, percentage_change_30d) 
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    transformed_data_tuples = [(data['name'], data['symbol'], data['max_supply'], data['circulating_supply'],
                    data['price'], data['market_cap'], data['market_cap_dominance'],
                    data['percentage_change_24h'], data['percentage_change_30d']) for data in transformed_data]
    
    cursor.executemany(insert_query, transformed_data_tuples)
    conn.commit()
    cursor.close()
    conn.close()
    return "Crypto data inserted successfully!"

def etl():
    data = request_to_api()
    extracted_data = extract(data)
    transformed_data = transform(extracted_data)
    load(transformed_data)
    return "ETL pipeline was successful!"

etl()