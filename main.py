import func

# 데이터 가져오기
songs = func.get_melon_chart()

print("===================")
print("1. 멜론 100")
print("2. 멜론 50")
print("3. 멜론 10")
print("4. AI 추천 노래")
print("5. 가수 이름 검색")
print("6. 노래 제목 검색")
print("7. 파일에 저장(멜론100)")
print("===================")

n = input("메뉴선택(숫자입력): ")

if n == "1":
    func.m100(songs)
elif n == "2":
    func.m50(songs)
elif n == "3":
    func.m10(songs)
elif n == "4":
    func.m_random(songs)
elif n == "5":
    name = input("가수 이름을 입력하세요: ")
    func.search_singer(songs, name)
elif n == "6":
    keyword = input("노래 제목 키워드를 입력하세요: ")
    func.search_title(songs, keyword)
elif n == "7":
    func.save_to_file(songs)
else:
    print("1~7 중에서 입력해주세요.")
