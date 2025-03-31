

songs = ["a노래","b노래","c노래","d노래"]
print(songs)
print(songs[2])

for song in songs:
    print(song)

print("AI야 노래 한곡만 추천해줘")
print("""알겠습니다.
제가 열심히 분석해서
고객님께 노래 한곡 추천합니다""")

#여기서 AI가 돌아야죠
AI_song = random.choice(songs)
print(f"두두두두ㅜ둥 제가 추천한 곡은 {AI_song}입니다.")

#리스트를 쓰는 이유python list.py
song1 = "a노래"
song2 = "b노래"
song3 = "c노래"
song4 = "d노래"
