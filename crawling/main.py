from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv

import time
import os
import re

# 현재 스크립트의 디렉토리 경로를 구함
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상대 경로를 사용하여 ChromeDriver 경로를 구성
chrome_driver_path = os.path.join(current_dir, 'chromedriver-mac-arm64/chromedriver')

# Service 객체를 사용하여 웹드라이버 초기화
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # 웹페이지 로드
    driver.get(
        'https://www.aladin.co.kr/shop/wbrowse.aspx?ItemType=101&ViewRowsCount=24&ViewType=Simple&PublishMonth=0&SortOrder=6&page=1&UsedShop=0&PublishDay=84&CID=0&SearchOption=&QualityType=&OrgStockStatus=&IsFlatPrice=')
    time.sleep(2)  # 페이지가 완전히 로드될 때까지 기다림

    # 상품명 추출
    products = driver.find_elements(By.CSS_SELECTOR, "a.bo b")
    product_names = [product.text for product in products]

    # 가격 추출
    price_elements = driver.find_elements(By.CSS_SELECTOR, "td[valign='top'] span.p1_n")
    prices = [int(re.sub(r'[^\d]', '', element.text.split('(')[0].strip())) for element in price_elements]

    # 상품명과 가격을 튜플로 묶기
    items = list(zip(product_names, prices))

    # CSV 파일 저장
    with open('products_prices.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['상품이름', '가격'])  # 헤더 작성
        for item in items:
            writer.writerow(item)

except Exception as e:
    print("Error:", e)

finally:
    # 드라이버 종료
    driver.quit()
