from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup

def get_driver(url, chrome_driver_path, headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path=chrome_driver_path,
                              chrome_options=chrome_options
                             )
    driver.get(url)
    return driver


def web_loading(url, scroll_pause_time=0.2, load_round=500, headless=False, chrome_driver_path='chromedriver.exe'):
    driver = get_driver(url, chrome_driver_path, headless=headless)
    if 'news/tag' in url:
        click = driver.find_element(By.XPATH, "//div[@class=' css-b8dj8a-control']")
        click.click()
        click = driver.find_element(By.XPATH, "//div[@id='react-select-2-option-4']")
        click.click()

    elif 'archive' in url:
        click = driver.find_element(By.XPATH, """//*[@id="__next"]/div[1]/div[4]/section/div/div[2]/div[1]/div[1]/div[2]/div/div""")
        click.click()
        click = driver.find_element(By.XPATH, "//div[@id='react-select-3-option-4']")
        click.click()
        
    # t = driver.find_element(By.XPATH, """//*[@id="__next"]/div[1]/div[4]/section/div/div[2]/div[1]/div[1]/div[2]/div/div""")
    # print(t.get_attribute('innerHTML'))

    for i in range(load_round):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)
    return driver

def find_title_date_views_driver(driver, search_title, search_date, search_view):
    title_driver = driver.find_elements(By.XPATH, search_title)
    date_driver = driver.find_elements(By.XPATH, search_date)
    view_driver = driver.find_elements(By.XPATH, search_view)
    return title_driver, date_driver, view_driver
    
def dowload_web_to_text(url, file_path):
    '''
    url : link to news page (final link)
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        text_document = soup.find('div', id='EntryReader_0').text
    except Exception as e:
        text_document= ''
        print(f'error to scrape this page text {url} because', e)
        
    # return text_document
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(text_document)
        
if __name__ == '__main__':
    web_loading('https://www.sanook.com/game/archive/')# 'https://www.sanook.com/news/tag/อาชญากรรม/')
    
    # search_title = "//div[@class='jsx-3504035561 archive-post-col col-12 col-md-6']/article/div[2]/div/h3/span/a"
    # search_date = "//div[@class='jsx-3504035561 archive-post-col col-12 col-md-6']/article/div[2]/footer/time/span"
    # search_view = "//div[@class='jsx-3504035561 archive-post-col col-12 col-md-6']/article/div[2]/footer/small/span[2]"
    # driver_ = web_loading('https://www.sanook.com/game/archive/', load_round=10)
    # t, d, v = find_title_date_views_driver(driver_, search_title, search_date, search_view)
    # print(t, d, v)
    # while True:
    #     pass