songs = ["a노래","b노래","c노래","d노래"]
print(songs)
print(songs[2])

for song in songs:
    print(song)

print("AI야 노래 한곡만 추천해줘")
print("""넵!!!
지금 즉시 맛깔나는
노래 한곡 추천드리겠습니다!!!""")

AI_song = random.choice(songs)
print(f"두두두두ㅜ둥 저의 추천곡은 {AI_song}!!!")

#리스트를 쓰는 이유
song1 = "a노래"
song2 = "b노래"
song3 = "c노래"
song4 = "d노래"


import requests
from bs4 import BeautifulSoup
import random

# 멜론 차트 페이지 URL
url = 'https://www.melon.com/chart/index.htm'  # 멜론의 최신 차트 URL로 확인 필요

# 헤더 설정 (멜론은 User-Agent 확인을 통해 봇 접근을 차단할 수 있으므로 설정이 필요할 수 있음)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# 웹페이지 요청
response = requests.get(url, headers=headers)

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 노래 제목과 아티스트를 담을 리스트.
songs = []

# 멜론 차트의 노래 제목과 아티스트를 찾습니다.
#lst50 #frm > div > table > tbody #lst50
for entry in soup.select('tr.lst50, tr.lst100'):  # 상위 50위 및 100위 목록
    rank = entry.select_one('span.rank').get_text()
    title = entry.select_one('div.ellipsis.rank01 a').get_text()
    artist = entry.select_one('div.ellipsis.rank02 a').get_text()
    songs.append((rank, title, artist))


# 메뉴
print("===================")
print("1. 멜론 100")
print("2. 멜론 50")
print("3. 멜론 10")
print("4. AI 추천 노래")
print("5. 가수 이름 검색")
print("===================")
# 메뉴선택(숫자입력): 1
n = input("메뉴선택(숫자입력): ")
print(f"당신이 입력한 값은? {n}") 
# 여기까지는 n 이 문자열
# n = int(n) # 숫자로 변경(연산을 해야 된다면)
# 여기서 부터는 n은 숫자(정수)

# 만약에 1을 입력하면
# 멜론 100 출력

#songs = [(순위, 제목, 가수)]
if n == "1":
    print("멜론 100")
    for i in range(len(songs)):
        print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")


elif n == "2":
    print("멜론 50")

elif n == "3":
    print("멜론 10")

elif n == "4":
    print("AI 추천곡")
 

elif n == "5":
    print("가수 이름 검색")

else:
    print("1~5까지 입력하세요")
