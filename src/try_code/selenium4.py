from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def firefox_get_title():
    print('firefox_get_page_title')    
    print( datetime.strftime(datetime.now(), '%H:%M:%S.%f') )    
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("http://google.com/")    
    print (driver.title)
    driver.quit()
    print( datetime.strftime(datetime.now(), '%H:%M:%S.%f') )


def firefox_get_heading():    
    print('firefox_get_heading')
    firefox_options = Options()    
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("http://todo.test:8000/")
    h1_titles = driver.find_elements(By.TAG_NAME, "h1")
    is_login_title = False
    page_title = ''
    for title in h1_titles:
        if title.text == 'Login':
            is_login_title = True
            page_title = title.text
            break
    driver.quit()
    assert( is_login_title )
    print(page_title)


def firefox_get_screenshot():
    print('firefox_get_screenshot')
    firefox_options = Options()    
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)    
    driver.get("http://todo.test:8000/")
    driver.get_full_page_screenshot_as_file('try_code/selenium_screen_shot.png')    
    driver.quit()


if __name__ == '__main__':
    firefox_get_screenshot()
    firefox_get_heading()
    firefox_get_title()


