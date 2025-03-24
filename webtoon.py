import requests
from bs4 import BeautifulSoup

# 네이버 웹툰 랭킹 페이지 URL
url = 'https://comic.naver.com/index'

# 페이지를 가져옵니다.
response = requests.get(url)

# 페이지가 정상적으로 로드되었는지 확인합니다.
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 웹툰 목록을 찾습니다.
    webtoon_list = soup.find_all('li', class_='rank01')  # 'rank01'은 웹툰 랭킹 1위를 포함한 항목
    
    # 상위 100위까지 데이터 추출
    rank = 1
    for webtoon in webtoon_list:
        title_tag = webtoon.find('a')  # 각 웹툰의 제목을 찾음
        title = title_tag.text.strip()  # 웹툰 제목
        link = 'https://comic.naver.com' + title_tag['href']  # 웹툰 링크
        
        print(f'{rank}위: {title} - {link}')
        rank += 1
        if rank > 100:
            break
else:
    print("웹 페이지를 가져오는 데 실패했습니다.")
