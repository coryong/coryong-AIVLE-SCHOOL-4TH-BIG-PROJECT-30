from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
# Chrome options to set preferences
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,  # Block notifications
    "profile.default_content_setting_values.cookies": 2,  # Block cookies
    # Add any other permissions you want to automate
})

# Initialize the webdriver with the options
driver = webdriver.Chrome(options=chrome_options)

# 스크래핑 데이터를 저장할 리스트
job_names = [] # 직업
titles = [] # 회사명
jobs = [] # 주요업무
requirements_list = [] # 자격요건
preferentials = [] # 우대사항
welfares = [] # 복지
technology_stacks = [] # 요구 기술스택 및 툴

# 스크래핑할 직업 목록
job_list = ['Data Analyst', 'Front-end Developer', 'Back-end Developer', 'AI Engineer', 'Data Scientist', 'Data Engineer', 'UI/UX Designer', 'App Developer']

for j in job_list:
    url = f'https://www.wanted.co.kr/search?query={j}&tab=position'
    driver.get(url)

    # 페이지의 맨 아래로 스크롤하는 루프
    last_count = 0
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        try:
            # 페이지가 로드될 때까지 대기
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'List_link__1jbJp')))
            current_count = len(driver.find_elements(By.CLASS_NAME, "List_link__1jbJp"))
            if current_count == last_count:
                break
            last_count = current_count
        except:
            break

    # 링크 수집 로직
    postings = driver.find_elements(By.CLASS_NAME, "List_link__1jbJp")
    url_list = [posting.get_attribute('href') for posting in postings]

    # 각 링크에 대해 세부 정보 스크래핑
    for url in url_list:
        try:
            driver.get(url)
            title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.job-title'))).text
            job_desc = driver.find_element(By.CSS_SELECTOR, "div.job-detail").text
            requirements = driver.find_element(By.CSS_SELECTOR, "div.requirements").text
            preferential = driver.find_element(By.CSS_SELECTOR, "div.preferentials").text
            welfare = driver.find_element(By.CSS_SELECTOR, "div.welfare").text
            tech_stack_elements = driver.find_elements(By.CSS_SELECTOR, '.SkillItem_SkillItem__E2WtM')
            tech_stack = [element.text for element in tech_stack_elements]

            job_names.append(j)
            titles.append(title)
            jobs.append(job_desc)
            requirements_list.append(requirements)
            preferentials.append(preferential)
            welfares.append(welfare)
            technology_stacks.append(', '.join(tech_stack))
        except Exception as e:
            print(f"An error occurred while scraping the URL: {url} - {e}")

# DataFrame 생성
df = pd.DataFrame({
    '직업': job_names,
    '회사명': titles,
    '주요업무': jobs,
    '자격요건': requirements_list,
    '우대사항': preferentials,
    '복지': welfares,
    '기술스택 및 기술': technology_stacks
})

# WebDriver 종료
driver.quit()

# 결과 출력
print(df)
