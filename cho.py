from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('/Users/hyun/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get('https://comic.naver.com/')

input("크롬 창이 열렸으면 아무 키나 눌러서 종료하세요...")
driver.quit()