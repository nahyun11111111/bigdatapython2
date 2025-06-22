from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os 


# 네이버 월요 웹툰 URL
url = 'https://comic.naver.com/webtoon?tab=mon'

# ChromeDriver 경로 설정
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver.exe')

try:
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless') # 브라우저를 백그라운드에서 실행 (선택 사항)
    chrome_options.add_argument('--disable-gpu') # GPU 사용 안함 (리눅스에서 필요할 수 있음)
    chrome_options.add_argument('--no-sandbox') # 샌드박스 비활성화 (리눅스에서 필요할 수 있음)

    # 서비스 객체 생성
    service = Service(CHROMEDRIVER_PATH)
    
    # 웹 드라이버 초기화
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("웹 드라이버가 성공적으로 초기화되었습니다.")

except Exception as e:
    print(f"웹 드라이버 초기화 오류가 발생했습니다: {e}")
    print("1. ChromeDriver가 설치되어 있고, 브라우저 버전과 일치하는지 확인하세요.")
    print(f"2. ChromeDriver 경로가 올바른지 확인하세요: {CHROMEDRIVER_PATH}")
    print("3. 필요한 권한이 있는지 확인하세요.")
    exit()

# 명시적 대기를 위한 WebDriverWait 객체 생성
wait = WebDriverWait(driver, 20) # 최대 20초까지 기다림

# --- 웹툰 정보 추출 함수 ---

def extract_webtoon_info(item_element):
    """
    개별 웹툰 요소에서 썸네일, 타이틀, 작가명, 평점 정보를 추출합니다.
    """
    try:
        # 썸네일 이미지 주소 추출
        # ContentPoster__image-- 또는 Poster__image-- 클래스 중 하나를 사용
        thumbnail_img = item_element.find_element(By.XPATH, ".//img[contains(@class, 'ContentPoster__image--') or contains(@class, 'Poster__image--')]")
        thumbnail_url = thumbnail_img.get_attribute('src') if thumbnail_img else 'N/A'
        
        # 타이틀 추출
        title_element = item_element.find_element(By.XPATH, ".//span[contains(@class, 'ContentTitle__title--')]")
        title = title_element.text if title_element else 'N/A'
        
        # 작가명 추출
        artist_elements = item_element.find_elements(By.XPATH, ".//a[contains(@class, 'ContentAuthor__author--')]")
        artists = [artist_el.text for artist_el in artist_elements if artist_el.text] # 빈 문자열 제외
        artist = ', '.join(artists) if artists else 'N/A'
        
        # 평점 추출
        try:
            # Rating__star_area-- 클래스 하위의 span (예: <span class="text">9.99</span>)
            rating_element = item_element.find_element(By.XPATH, ".//span[contains(@class, 'Rating__star_area--')]/span[contains(@class, 'text')]")
            rating = rating_element.text if rating_element else 'N/A'
        except:
            rating = 'N/A' # 평점 요소가 없는 경우
        
        return {
            '썸네일 이미지 주소': thumbnail_url,
            '타이틀': title,
            '작가명': artist,
            '평점': rating
        }
        
    except Exception as e:
        print(f"개별 웹툰 정보 추출 중 오류 발생 (해당 아이템): {e}")
        return None # 오류 발생 시 None 반환

# --- 메인 스크래핑 로직 ---

webtoons_data = []
processed_titles = set() # 중복 방지를 위해 이미 처리된 타이틀 저장

try:
    # 웹 페이지 열기
    print(f"페이지 로딩 중: {url}")
    driver.get(url)

    # 웹툰 리스트를 감싸는 컨테이너가 나타날 때까지 기다림
    # 네이버 웹툰 페이지 구조를 분석하여 적절한 XPath 사용
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'component_wrap')]")))
    print("페이지 로딩 완료. 웹툰 목록을 찾습니다.")

    # 스크롤을 통해 모든 웹툰 로드
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 현재 스크롤 위치의 모든 웹툰 아이템을 가져옵니다.
        # 기존에 찾았던 웹툰과 새롭게 로드된 웹툰을 모두 포함하기 위해 매번 다시 찾습니다.
        current_webtoon_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'ComponentRankingChart__item--') or contains(@class, 'ContentList__item--')]")
        
        # 새로 발견된 웹툰만 처리
        for item_element in current_webtoon_elements:
            try:
                # 미리 타이틀을 추출하여 이미 처리된 웹툰인지 빠르게 확인
                temp_title_element = item_element.find_element(By.XPATH, ".//span[contains(@class, 'ContentTitle__title--')]")
                temp_title = temp_title_element.text if temp_title_element else "TEMP_NO_TITLE"

                if temp_title not in processed_titles:
                    webtoon_info = extract_webtoon_info(item_element)
                    if webtoon_info and webtoon_info['타이틀'] != 'N/A': # 유효한 정보만 추가
                        webtoons_data.append(webtoon_info)
                        processed_titles.add(webtoon_info['타이틀'])
                        # print(f"새 웹툰 정보 추출: {webtoon_info['타이틀']}")
            except Exception as e:
                # print(f"새로운 웹툰 아이템 처리 중 오류 발생: {e}")
                pass # 특정 아이템에서 오류 발생 시 건너뛰기

        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) # 스크롤 후 콘텐츠 로드를 위한 대기 시간

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # 더 이상 스크롤할 내용이 없으면 반복 종료
            break
        last_height = new_height
    
    print(f"총 {len(processed_titles)}개의 고유한 웹툰 정보를 수집했습니다.")

except Exception as e:
    print(f"웹툰 목록 스크래핑 중 치명적인 오류 발생: {e}")

finally:
    # 웹 드라이버 종료
    driver.quit()
    print("웹 드라이버가 종료되었습니다.")

# --- 데이터 정리 및 저장 ---

# 스크롤 중 중복 추가될 수 있는 경우를 대비해 최종적으로 중복 제거
unique_webtoons = []
final_unique_titles = set()
for webtoon in webtoons_data:
    if webtoon['타이틀'] not in final_unique_titles:
        final_unique_titles.add(webtoon['타이틀'])
        unique_webtoons.append(webtoon)

print("\n--- 수집된 최종 웹툰 정보 ---")
if unique_webtoons:
    for i, webtoon in enumerate(unique_webtoons, 1):
        print(f"{i}. {webtoon['타이틀']} - {webtoon['작가명']} (평점: {webtoon['평점']})")
else:
    print("수집된 웹툰 정보가 없습니다.")

print(f"\n최종적으로 고유한 {len(unique_webtoons)}개의 웹툰 정보를 수집했습니다.")

# 데이터프레임으로 변환 및 CSV 저장
if unique_webtoons:
    df = pd.DataFrame(unique_webtoons)
    file_name = 'naver_monday_webtoons.csv'
    df.to_csv(file_name, index=False, encoding='utf-8-sig') # 엑셀에서 한글 깨짐 방지
    print(f"\n데이터를 '{file_name}' 파일로 성공적으로 저장했습니다.")
else:
    print("\n저장할 데이터가 없어 파일을 생성하지 않았습니다.")