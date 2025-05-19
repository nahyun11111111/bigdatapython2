# func.py
import requests
from bs4 import BeautifulSoup
import random

# 멜론 차트 크롤링 함수
def get_melon_chart():
    url = 'https://www.melon.com/chart/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    songs = []
    for entry in soup.select('tr.lst50, tr.lst100'):
        rank = entry.select_one('span.rank').get_text()
        title = entry.select_one('div.ellipsis.rank01 a').get_text()
        artist = entry.select_one('div.ellipsis.rank02 a').get_text()
        songs.append((rank, title, artist))
    return songs

# 멜론 100 출력
def m100(songs):
    print("[멜론 100]")
    for song in songs:
        print(f"{song[0]}. {song[1]} - {song[2]}")

# 멜론 50 출력
def m50(songs):
    print("[멜론 50]")
    for i in range(50):
        print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")

# 멜론 10 출력
def m10(songs):
    print("[멜론 10]")
    for i in range(10):
        print(f"{songs[i][0]}. {songs[i][1]} - {songs[i][2]}")

# AI 추천곡 출력
def m_random(songs):
    print("[AI 추천 노래]")
    song = random.choice(songs)
    print(f"추천곡은 바로바로 {song[1]} - {song[2]}!!!")

# 가수 이름으로 검색
def search_singer(songs, name):
    print(f"[가수 검색] {name}")
    found = False
    for song in songs:
        if name in song[2]:
            print(f"{song[0]}. {song[1]} - {song[2]}")
            found = True
    if not found:
        print("해당 가수의 노래가 없습니다.")

# 노래 제목으로 검색
def search_title(songs, keyword):
    print(f"[노래 제목 검색] '{keyword}'")
    found = False
    for song in songs:
        if keyword in song[1]:
            print(f"{song[0]}. {song[1]} - {song[2]}")
            found = True
    if not found:
        print("해당 키워드가 들어간 노래가 없습니다.")

# 멜론 100을 파일로 저장
def save_to_file(songs):
    with open("melon100.txt", "w", encoding="utf-8") as f:
        for song in songs:
            f.write(f"{song[0]}. {song[1]} - {song[2]}\n")
    print("멜론 100 목록이 'melon100.txt' 파일로 저장되었습니다.")