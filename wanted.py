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

job_names = []  # 직업
titles = []  # 회사명
jobs = []  # 주요업무
requirements_list = []  # 자격요건
preferentials = []  # 우대사항
welfares = []  # 복지
technology_stacks = []  # 요구 기술스택 및 툴

job_list = ['데이터 분석가', '프론트엔드 개발자', '백엔드 개발자', 'AI 엔지니어', '데이터 사이언티스트', '데이터 엔지니어', 'UI/UX 디자이너', '앱 개발자']
for j in job_list:
    url_list = []
    url = f'https://www.wanted.co.kr/search?query={j}&tab=position'
    driver.get(url)

    last_count = 0
    while True:
        # Scroll to the end of the page
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        
        # Wait for the page to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "class-of-job-posting-elements")))
        
        # Get current count of job postings
        current_count = len(driver.find_elements(By.CLASS_NAME, "class-of-job-posting-elements"))

        # Break if no new postings are loaded
        if current_count == last_count:
            break
        last_count = current_count
        
        except :
            pass
    # # You need to replace 'job-link-selector' with the actual selector
    # job_links = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, "job-link-selector")]

    for k in range(len(url_list)):
        try:
            a = url_list[k]
            driver.get(a)
            # You need to add code here to handle any potential popups or dialogs
            title = driver.find_element(By.CSS_SELECTOR, 'span.JobHeader_companyNameText__uuJyu > a')
            job = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[2]/span')
            requirements = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[3]/span')
            preferential = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[4]/span')
            welfare = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[5]/span')
            # Scrape the technology stack and tools
            tech_stack_elements = driver.find_elements(By.CSS_SELECTOR, '.JobDescription_JobDescription_skill_wrapper__9EdFE .SkillItem_SkillItem__E2WtM')
            tech_stack = [element.text for element in tech_stack_elements]
            technology_stacks.append(', '.join(tech_stack))  # Combine into a single string
            
            job_names.append(j)
            titles.append(title.text)
            jobs.append(job.text)
            requirements_list.append(requirements.text)
            preferentials.append(preferential.text)
            welfares.append(welfare.text)

        except : 
            pass

df = pd.DataFrame({
    '직업': job_names,
    '회사명': titles,
    '주요업무': jobs,
    '자격요건': requirements_list,
    '우대사항': preferentials,
    '복지': welfares,
    '기술스택 및 기술': technology_stacks
})

# Close the driver
driver.quit()

# Print the DataFrame to console (or you can export it to CSV or another format)
print(df)
