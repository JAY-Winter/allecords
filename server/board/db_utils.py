from datetime import datetime
from pymongo import MongoClient

MONGO_DATABASE = 'crawling'


def get_database():
    return MongoClient()[MONGO_DATABASE]


def get_todays_collection():
    today = datetime.now().strftime('%Y_%m_%d')  # YYYY_MM_DD 형식
    todays_collection_name = f'products_{today}'  # 예: 'products_2023_11_03'
    db = get_database()
    return db[todays_collection_name]
