# pip install requests 필요
# URL 요청에 대한 응답을 받아주는 라이브러리
import requests
# pip install beautifulsoup4 필요
# 받아온 html을 각종 변수로 접근할 수 있도록 정리해주는 라이브러리
from bs4 import BeautifulSoup

LIMIT = 50
INDEED_URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def get_last_pn():
    result = requests.get(INDEED_URL)

    # html을 모두 가져와서 BeautifulSoup 적용
    soup = BeautifulSoup(result.text, "html.parser")


    # div 중 class가 pagination인 것을 찾기
    pagination = soup.find("div", {"class": "pagination"})


    # pagination의 anchoor을 찾기
    # links는 일종의 리스트
    links = pagination.find_all('a')


    # links를 돌며 각 페이지에 페이지 넘버가 있는 태그 불러서
    # 가장 큰 페이지 넘버 기억하기
    pages = []
    for link in links:
        pages.append(link.find("span").string)
        # pages.append(link.string) 과 동일
        # 왜? 그 내부 요소 중 string이 하나밖에 없으면 알아서 찾아줌
    pages = pages[:-1]
    pages = list(map(int, pages))
    max_pn = max(pages)
    return max_pn

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("div", {"class": "sjcl"}).find("span")
    company_anchor = company.find("a")
    company_location = html.find("span", {"class": "location"})
    # 해당 직무 id값, 이를 통해 지원 링크 연결 가능
    job_id = html["data-jk"]
    
    # span 속에 a 링크가 있는 경우가 있고, 없는 경우가 있으므로 분기 처리
    if company:
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None

    # 위치가 span 속에 있을 수도, div 속에 있을 수도 있어서
    if company_location is not None:
        location = str(company_location.string).strip()
    else:
        location = html.find("div", {"class": "location"}).string.strip()
    
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?cmp=%ED%98%84%EB%8C%80%EB%AA%A8%EB%B9%84%EC%8A%A4&t=%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%82%AC%EC%9D%B4%EC%96%B8%EC%8A%A4&jk={job_id}&sjdu=q7yxxeHj5IC7xEw8iiZPOn35LSTyHcaBQgEz7hsO_bzhy2TiENHxuoH_-fGoIhA72CWy-2vnIeFz7KBz_mv_ympJXnwj41C5w_3a2QGrBa6QlFuQT2OEqz3M_TdYQrtQoVEeTc3XqqzRqBU8LkzvUw&tk=1ebvcgilf0unm000&adid=349705345&vjs=3",
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{INDEED_URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_pn = get_last_pn()
    jobs = extract_jobs(last_pn)
    return jobs