# -*- coding: utf-8 -*-
"""네이버 기사 웹 크롤링_ITnews

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lZZMX64Ux14dlmTXLVZpgqRYFrR8TesP
"""

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

# import requests
# from bs4 import BeautifulSoup

# query="it"

# url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + query
# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")

# titles = soup.find_all("a", class_="api_txt_lines total_tit _cross_trigger")

# for title in titles:
#     print(title.text)

"""경제는 101, 사회는 102, 생활/문화는 103, 세계는 104, IT/과학은 105

"""

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

"""기사 제목, 날짜, 본문, 카테고리, 링크 수집


```
# 코드로 형식 지정됨
```


"""

# 기사 크롤링 함수
def art_crawl(all_hrefs, sid, index):
    art_dic = {}
    title_selector = "#title_area > span"
    date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span"
    main_selector = "#dic_area"

    url = all_hrefs[sid][index]
    html = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")

    title = soup.select(title_selector)
    date = soup.select(date_selector)
    main = soup.select(main_selector)

    art_dic["title"] = "".join(t.text for t in title)
    art_dic["date"] = "".join(d.text for d in date)
    art_dic["main"] = "".join(m.text.strip() for m in main)
    return art_dic

# 모든 섹션의 데이터 수집 (제목, 날짜, 본문, section, url)
section_lst = [105] 

all_hrefs = {105: re_tag(105)}  # IT/과학 분야의 링크 수집
artdic_lst = []

for section in tqdm(section_lst):
    for i in tqdm(range(len(all_hrefs[section]))):
        art_dic = art_crawl(all_hrefs, section, i)
        art_dic["section"] = section
        art_dic["url"] = all_hrefs[section][i]
        artdic_lst.append(art_dic)

"""csv로 변환"""

import pandas as pd

art_df = pd.DataFrame(artdic_lst)

art_df = art_df[['title', 'main']]

art_df.to_csv("naver_title_main.csv")
