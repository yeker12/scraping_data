import requests
from bs4 import BeautifulSoup

LIMIT = 50;
SEARCH_WORD = "python"
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={SEARCH_WORD}&limit={LIMIT}&filter=0"


def change_num(to_change_num):
    for i in range(len(to_change_num)):
        changed_num = to_change_num.replace(",", "");
    return int(changed_num);


def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser");
    search_count_pages = soup.find("div", {"id": "searchCountPages"});

    total_jobs = search_count_pages.string.split()[-1];
    total_jobs = total_jobs.split()[-1][:-1];
    max_page = (change_num(total_jobs) // LIMIT) + 1;
    print(max_page);
    return max_page;


def extract_job(html):
    title = html.find("h2", {"class": "jobTitle"}).find("span", title=True).string;
    company = html.find("span", {"class": "companyName"}).string;
    location = html.find("div", {"class": "companyLocation"}).string;
    id = html["data-jk"]
    return {"title": title, "company": company, "location": location,
            "link": f"https://kr.indeed.com/jobs?q={SEARCH_WORD}&limit={LIMIT}&filter=0&vjk={id}&from=web&vjs=3"};


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page: ");
        result = requests.get(f"{URL}&start={12 * LIMIT}");
        soup = BeautifulSoup(result.text, "html.parser");
        results = soup.find_all("a", {"class": "fs-unmask"})
        for result in results:
            job = extract_job(result);
            jobs.append(job);
    return jobs;


def get_jobs():
    last_page = extract_pages();
    print(last_page);
    jobs = extract_indeed_jobs(last_page);
    print(jobs);
    return jobs;

