import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['crawling']  # 사용할 데이터베이스 이름

# 다음 날 사용할 데이터 미리 저장
today = datetime.now()
one_day_later = today + timedelta(days=1)
formatted_date = one_day_later.strftime('%Y_%m_%d')
collection_name = f'products_{formatted_date}'
collection = db[collection_name]  # 사용할 컬렉션 이름

# CSV 파일 읽기
csv_file_path = f'./products_{formatted_date}.csv'  # CSV 파일 경로
data = pd.read_csv(csv_file_path)

# 필요하다면, 데이터를 정제하거나 변환하는 코드를 여기에 추가

# DataFrame을 MongoDB 문서로 변환 및 저장
records = data.to_dict('records')  # DataFrame을 딕셔너리 리스트로 변환
collection.insert_many(records)  # MongoDB에 일괄 삽입

print(f"Inserted {len(records)} documents into MongoDB")
