import os
import sys
import urllib.request
import json

client_id = "7oq3k0Y3vFVKJRpftsIJ"
client_secret = "fgUT2OsHuM"

def naver_search_api(search_query: str, api_type: str) -> list:

    if api_type not in ["blog", "news"]:
        print("오류: 'api_type'은 'blog' 또는 'news'여야 합니다.")
        return []

    encText = urllib.parse.quote(search_query)
    
    if api_type == "blog":
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    else: # api_type == "news"
        url = "https://openapi.naver.com/v1/search/news?query=" + encText
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    json_data = ""
    try:
        with urllib.request.urlopen(request) as response:
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                json_data = response_body.decode('utf-8')
            else:
                print(f"Error Code: {rescode}")
                return []
    except urllib.error.URLError as e:
        print(f"URL 오류 발생: {e.reason}")
        return []
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return []

    # JSON 데이터 파싱 및 에러 처리
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        print("오류: JSON 데이터를 디코딩할 수 없습니다.")
        return []

    extracted_list = []
    if 'items' in data:
        for item in data['items']:
            extracted_item = {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "description": item.get("description", ""),
                "bloggername": item.get("bloggername", "") if api_type == "blog" else item.get("publisher", ""), # 블로그는 bloggername, 뉴스는 publisher
                "postdate": item.get("postdate", "") 
            }
            if api_type == "news":
                extracted_item["postdate"] = item.get("pubDate", "")
            
            extracted_list.append(extracted_item)
    
    return extracted_list


if __name__ == "__main__":
    print("--- 네이버 블로그 검색 ---")
    blog_results = naver_search_api("파이썬 프로그래밍", "blog")
    if blog_results:
        for i, item in enumerate(blog_results):
            print(f"[{i+1}]")
            print("제목:", item['title'])
            print("링크:", item['link'])
            print("블로거:", item['bloggername'])
            print("작성일:", item['postdate'])
            print("-" * 30)
    else:
        print("블로그 검색 결과를 찾을 수 없거나 오류가 발생했습니다.")

    print("\n--- 네이버 뉴스 검색 ---")
    news_results = naver_search_api("AI 기술 동향", "news")
    if news_results:
        for i, item in enumerate(news_results):
            print(f"[{i+1}]")
            print("제목:", item['title'])
            print("링크:", item['link'])
            print("언론사:", item.get('publisher', 'N/A')) 
            print("게시일:", item.get('pubDate', 'N/A')) 
            print("-" * 30)
    else:
        print("뉴스 검색 결과를 찾을 수 없거나 오류가 발생했습니다.")