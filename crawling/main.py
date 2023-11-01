import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time


def find_last_page_number(driver):
    try:
        # '끝'이라는 텍스트를 포함하는 요소를 찾음
        last_page_element = driver.find_element(By.XPATH, "//div[@class='numbox_last']/a[contains(text(), '끝')]")
        href_value = last_page_element.get_attribute('href')

        # 'Page_Set' 함수의 인자를 정규 표현식으로 추출
        match = re.search(r"Page_Set\('(\d+)'\)", href_value)
        if match:
            return int(match.group(1))
        else:
            return -1  # 매칭 실패
    except NoSuchElementException:
        print("마지막 페이지 링크를 찾을 수 없습니다.")
        return -1


def collect_data_and_write_to_csv(driver, writer):
    product_containers = driver.find_elements(By.CSS_SELECTOR, "form#Myform td[valign='top'][width='25%']")

    for container in product_containers:
        try:
            # 이미지 URL 추출
            image_element = container.find_element(By.CSS_SELECTOR, "img")
            image_url = image_element.get_attribute('src')
        except NoSuchElementException:
            image_url = "이미지 없음"  # 이미지가 없는 경우

        try:
            # 상품명과 링크 추출
            product_element = container.find_element(By.CSS_SELECTOR, "a.bo b")
            product_name = product_element.text
            product_link = container.find_element(By.CSS_SELECTOR, "a.bo").get_attribute('href')
        except NoSuchElementException:
            continue  # 상품명과 링크가 없는 경우 해당 상품은 건너뜁니다.

        # 가격 추출
        try:
            price_element = container.find_element(By.CSS_SELECTOR, "span.p1_n")
            price = int(re.sub(r'[^\d]', '', price_element.text.split('(')[0].strip()))
        except NoSuchElementException:
            price = "가격 정보 없음"  # 가격 정보가 없는 경우

        # 데이터 작성
        writer.writerow([product_name, product_link, image_url, price])


# 웹드라이버 설정
driver = webdriver.Chrome()

# CSV 파일 초기설정
csv_file = open('products_prices.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['상품이름', '가격'])  # 헤더 작성

try:
    # 최초 페이지 로드
    base_url = 'https://www.aladin.co.kr/shop/wbrowse.aspx?ItemType=101&ViewRowsCount=24&ViewType=Simple&PublishMonth=0&SortOrder=6&page=1&UsedShop=0&PublishDay=84&CID=0&SearchOption=&QualityType=&OrgStockStatus=&IsFlatPrice='
    driver.get(base_url)
    time.sleep(2)

    # 마지막 페이지 번호 찾기
    total_pages = find_last_page_number(driver)
    current_page = 1  # 첫 페이지로 시작

    # 페이지 순회 및 데이터 수집
    # 페이지 순회 및 데이터 수집
    while current_page <= total_pages:
        collect_data_and_write_to_csv(driver, csv_writer)

        # 다음 페이지로 이동
        current_page += 1
        if current_page <= total_pages:
            next_page_script = f"Page_Set('{current_page}')"
            driver.execute_script(next_page_script)
            time.sleep(2)  # 페이지 로딩 대기

except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
    csv_file.close()
