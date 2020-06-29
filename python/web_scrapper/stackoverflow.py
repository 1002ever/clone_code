import requests
from bs4 import BeautifulSoup


SO_URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
    result = requests.get(SO_URL)
    soup = BeautifulSoup(result.text, "html.parser")
    links = soup.find("div", {"class": "s-pagination"}).find_all("a")
    
    last_pn = int(links[-2].find("span").string)
    return last_pn

def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    # span 속 span을 찾는 것을 방지, 한 층까지만 들어가서 찾음. ( recurusive = False)
    company, location = html.find("h3").find_all("span", recursive=False)
    
    # innerText를 가져와서 strip 해주는 BeautifulSoup 메소드
    company = company.get_text(strip=True).strip("-").strip("\n").strip(" \r")
    location = location.get_text(strip=True).strip("-").strip("\n").strip(" \r")
    link = html.find("a", {"class": "s-link"})["href"]
    link = f"https://stackoverflow.com{link}"
    
    return {'title': title, 'company': company, 'location': location, 'link': link,}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: page: {page}")
        result = requests.get(f"{SO_URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

    
def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs