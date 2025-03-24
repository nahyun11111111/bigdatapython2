import requests
from bs4 import BeautifulSoup

# MBC 뉴스 URL (최신 뉴스 리스트 페이지)
url = "https://media.naver.com/press/214/ranking?type=popular/"

# HTML 요청 및 파싱
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 최신 뉴스 기사 목록 찾기
# MBC 뉴스는 <ul class="news_list"> 내부에 뉴스 목록이 있습니다.
news_list = soup.find_all('li', class_='list_item')

# 기사 제목 출력
for idx, news in enumerate(news_list[:20], start=1):  # 상위 20개 기사
    title = news.find('a').get_text(strip=True)  # 기사 제목 추출
    print(f"{idx}. {title}")
