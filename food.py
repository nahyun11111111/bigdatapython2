import requests
from bs4 import BeautifulSoup

# 부산 맛집 검색 URL
url = 'https://map.naver.com/p?c=10.00,0,0,0,dh'

# 페이지 요청
response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 맛집 목록 추출 (HTML 구조에 맞게 필요한 부분을 파싱)
    restaurant_list = soup.find_all('div', class_='lst_resto')  # 맛집 리스트 부분 (HTML 구조에 맞게 수정 필요)

    restaurants = []
    for restaurant in restaurant_list:
        title = restaurant.find('span', class_='name').text if restaurant.find('span', class_='name') else 'No name'
        address = restaurant.find('span', class_='addr').text if restaurant.find('span', class_='addr') else 'No address'
        rating = restaurant.find('span', class_='rating').text if restaurant.find('span', class_='rating') else 'No rating'

        # 별점 정보를 가져와서 float로 변환
        try:
            rating = float(rating)
        except ValueError:
            rating = 0  # 별점이 없으면 0으로 설정

        restaurants.append({'title': title, 'address': address, 'rating': rating})

    # 별점 순으로 정렬 (내림차순)
    sorted_restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)

    # 정렬된 맛집 정보 출력
    for idx, restaurant in enumerate(sorted_restaurants, start=1):
        print(f'{idx}위: {restaurant["title"]}')
        print(f'주소: {restaurant["address"]}')
        print(f'별점: {restaurant["rating"]}')
        print('---')
else:
    print("페이지 요청 실패")

    
