from bs4 import BeautifulSoup
from utils.file_utils import read_txt
from utils.link_utils import check_link
from job_scraper.fetcher import JobFetcher
from job_scraper.parser import JobParser
from job_scraper.poster import JobPoster
from utils.link_utils import build_link
from utils.phone_number_utils import extract_phone_numbers
from utils.date_utils import check_by_date

class JobScraper:
    def __init__(self, base_link, spreadsheet_url):
        self.base_link = base_link
        self.fetcher = JobFetcher()
        self.parser = JobParser()
        self.poster = JobPoster(spreadsheet_url)

    def scrape_jobs(self):
        """
        Scrapes jobs and posts the details to the spreadsheet.
        """
        keyword_list = read_txt("keywords.txt")
        city_list = read_txt("cities.txt")
        for keyword in keyword_list:
            for city in city_list:
                search_link = build_link(self.base_link, keyword, city)

                html = self.fetcher.fetch(search_link)
                if not html:
                    print(f"Failed to fetch URL: {search_link}")
                    continue

                job_listings = self.parser.parse_job_listings(html)
                if not job_listings:
                    print(f"No job listings found for URL: {search_link}")
                    continue

                for job_element in job_listings:
                    link = job_element.find("a").get("href")

                    if not check_link(link):
                        continue
                    
                    

                    job_details = self.parser.parse_job_details(job_element)
                    if not job_details:
                        print("Failed to parse job details. Skipping element.")
                        continue
                    #date_posted = job_details["date_posted"]
                    #if not check_by_date(date_posted):
                    #    continue
                        
                    job_html = self.fetcher.fetch(job_details["url"])
                    if not job_html:
                        print(f"Failed to fetch job details page: {job_details['url']}")
                        continue

                    soup = BeautifulSoup(job_html, "html.parser")
                    description = soup.find(itemprop="description")
                    description_text = description.get_text(strip=True) if description else ""
                    phone_numbers = extract_phone_numbers(description_text)
                    job_details.pop("date_posted", None)
                    job_details["phone_numbers"] = phone_numbers
                    job_details["source"] = "find-a-job"
                    job_details["keyword"] = keyword
                    job_details["city"] = city
                    self.poster.post_job(job_details)
            print("Job scraping completed.")
