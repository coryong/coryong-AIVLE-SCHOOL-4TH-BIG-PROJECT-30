from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import numpy as np
import re
import nltk  # pip install nltk
import os
import csv
import glob
import datetime
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from stackapi import StackAPI

# 링크 추출 함수
def ex_tag(sid, page):
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}#&date=%2000:00:00&page={page}"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")
    tag_lst = [a["href"] for a in a_tag if "href" in a.attrs and f"sid={sid}" in a["href"] and "article" in a["href"]]
    return tag_lst

# 링크 수집 및 중복 제거 함수
def re_tag(sid):
    re_lst = []
    for i in tqdm(range(100)):  # 수정된 부분
        lst = ex_tag(sid, i+1)
        re_lst.extend(lst)
    return list(set(re_lst))

all_hrefs = {}
sids = [105]  # 분야 리스트

# 각 분야별로 링크 수집해서 딕셔너리에 저장
for sid in sids:
    sid_data = re_tag(sid)
    all_hrefs[sid] = sid_data

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from summa.summarizer import summarize

def art_crawl(all_hrefs, sid, index, driver):
    art_dic = {}
    url = all_hrefs[sid][index]
    driver.get(url)

    wait = WebDriverWait(driver, 10)  # 최대 10초간 대기

    try:
        # CSS 선택자로 요소를 찾고, 텍스트를 추출합니다.
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#title_area > span"))).text.strip()
        date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span"))).text.strip()
        main = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dic_area"))).text.strip()
        img_url = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img#img1"))).get_attribute('src')

        # main 텍스트를 요약합니다.
        summarized_main = summarize(main, ratio=0.3)  # 요약 비율을 30%로 설정

    except Exception as e:
        print(f"Error while extracting data: {e}")
        title = date = main = img_url = summarized_main = None

    # 요약된 내용을 딕셔너리에 추가합니다.
    art_dic["title"] = title
    art_dic["date"] = date
    art_dic["body"] = summarized_main if summarized_main else main  # 요약된 내용이 없으면 원본을 사용
    art_dic["image"] = img_url

    return art_dic

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저가 보이지 않는 모드
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# WebDriver 서비스
service = Service(ChromeDriverManager().install())

# 드라이버 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# 모든 섹션의 데이터 수집 (제목, 날짜, 본문, section, url)
section_lst = [105]
artdic_lst = []

for section in tqdm(section_lst):
    for i in tqdm(range(len(all_hrefs[section]))):
        art_dic = art_crawl(all_hrefs, section, i, driver)
        art_dic["section"] = section
        art_dic["url"] = all_hrefs[section][i]
        artdic_lst.append(art_dic)

# 드라이버 종료
driver.quit()

art_df = pd.DataFrame(artdic_lst)

art_df = art_df[['title', 'body', 'image', 'url']]

# CSV 파일을 'utf-8-sig' 인코딩으로 저장
art_df.to_csv("naver_title_main_img_url_url_1.csv", encoding='utf-8-sig')
