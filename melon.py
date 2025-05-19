import requests
from bs4 import BeautifulSoup

# 멜론 차트 페이지 URL
url = "https://www.melon.com/chart/index.htm"

# HTTP 요청 보내기
response = requests.get(url)

# 응답 코드가 200이면(성공) 웹페이지를 파싱
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 곡 정보를 담고 있는 HTML 요소 찾기
    songs = soup.find_all('tr', {'class': 'lst50'})  # lst50은 1위~50위까지, lst100은 51위~100위까지

    # 1~100위 데이터를 담을 리스트
    top_100_songs = []

    # 1~50위까지 수집
    for song in songs:
        title = song.find('div', {'class': 'ellipsis rank01'}).find('a').text.strip()
        artist = song.find('div', {'class': 'ellipsis rank02'}).find('a').text.strip()
        song_data = {
            "rank": song.find('span', {'class': 'rank'}).text.strip(),
            "title": title,
            "artist": artist
        }
        top_100_songs.append(song_data)

    # 51~100위까지 수집
    songs = soup.find_all('tr', {'class': 'lst100'})
    for song in songs:
        title = song.find('div', {'class': 'ellipsis rank01'}).find('a').text.strip()
        artist = song.find('div', {'class': 'ellipsis rank02'}).find('a').text.strip()
        song_data = {
            "rank": song.find('span', {'class': 'rank'}).text.strip(),
            "title": title,
            "artist": artist
        }
        top_100_songs.append(song_data)

    # 결과 출력
    for song in top_100_songs:
        print(f"Rank: {song['rank']}, Title: {song['title']}, Artist: {song['artist']}")

else:
    print("웹페이지를 가져오는 데 실패했습니다.")


