from django.core.management.base import BaseCommand
from job.models import Job  # modelni import qilasan
import requests
import bs4

REQUEST_HOST = "https://remoteok.com"
headers = {
    "accept": "*/*",
    # "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "uz-UZ,uz;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5",
    "cookie": "new_user=true; ref=https%3A%2F%2Fremoteok.com%2F; adShuffler=1; visit_count=6",
    "referer": "https://remoteok.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
session = requests.Session()


class Command(BaseCommand):
    help = "Ish o‘rinlarini scrap qiladi va DBga saqlaydi"

    def handle(self, *args, **kwargs):
        offset_page = 594
        print("Scraping ishga tushdi...")
        urinishlar = 0
        for i in range(1, offset_page , 50):
            url = f"https://remoteok.com/?&action=get_job&offset={i}"
            response = session.get(url,headers=headers)
            html_text = ''
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR("Xatolik yuz berdi! HTTP status code: {}".format(response.status_code)))
                urinishlar += 1
                if urinishlar < 2:
                    print("zahira nusxasini olish...")
                    with open("remoteok.html", "r", encoding="utf-8") as file:
                        html_text = file.read()
                else:
                    continue
            else:
                html_text = response.text
            print("Malumotlar muvaffaqiyatli olindi! Kuting...")
            soup = bs4.BeautifulSoup(html_text, "html.parser")
            jobs = soup.find_all("tr", class_="job")    
            del soup
            for job in jobs:
                job_data_offset = job['data-offset']
                job_name = job.find("td", class_="company").find("h2").text.strip()
                location = job.find("td", class_="company").find_all("div", class_="location")
                job_company_sity = location[0].text.strip() if len(location) > 0 else None
                job_company_salary = location[1].text.strip() if len(location) > 1 else None
                job_company_image = job.find("td", class_="image").find("img")['data-src'] if job.find("td", class_="image").find("img") else None
                job_link = REQUEST_HOST + job.find("td", class_="company").find("a")['href']

                Job(
                    name = job_name,
                    data_offset = job_data_offset,
                    company_sity = job_company_sity,
                    company_salary = job_company_salary,
                    company_image = job_company_image,
                    link = job_link
                ).save()
        self.stdout.write(self.style.SUCCESS("Scraping tugadi! 🚀"))
