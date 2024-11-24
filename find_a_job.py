import re
import requests
from bs4 import BeautifulSoup
import utils.link_utils as lb


class JobScraper:
    def __init__(self, base_link, spreadsheet_url):
        self.base_link = base_link
        self.spreadsheet_url = spreadsheet_url

    def post_to_spreadsheet(self, job_details):
        job_title, company_name, salary, location, phone_numbers, job_link, source, keyword, city = job_details
        data = {"title": job_title, "url": job_link, "company": company_name, "rate": salary, "location": location,
                "phoneNumbers": phone_numbers, "source": source, "keyword": keyword, "city": city}
        response = requests.post(self.spreadsheet_url, json=data)
        print(response.text)

    def get_phone_numbers(self, description_text):
        """
        This function extracts phone numbers from the provided text.
        will use my own pattern, assuming that the phone number is 9 to 11 digits.

        Args:
            description_text: The text from which to extract phone numbers.

        Returns:
            list: A list containing the extracted phone numbers.
        """
        # Remove all special characters from the text
        clean_text = re.sub(r'[^a-zA-Z0-9]+', '', description_text)
        # Define the phone number pattern, after removing all special characters,
        # the phone number should be 9 to 11 digits
        phone_pattern = r'\d{9,}'
        phone_numbers = re.findall(phone_pattern, clean_text)
        # Save them in a list, to handle cases where there are multiple phone numbers
        selected_phone_numbers = [num for num in phone_numbers if len(num) <= 11]
        return selected_phone_numbers

    def scrape_jobs(self):
        for link in lb.build_link(self.base_link):
            response = requests.get(link)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            search_results = soup.find_all('div', class_='search-result')

            for result in search_results:
                job_id = result.get('data-aid')
                link = result.find('a')
                job_title = link.get_text(strip=True)
                job_link = link.get('href')

                job_components = result.find_all('ul')
                for component in job_components:
                    li_elements = component.find_all('li')
                    date_posted = li_elements[0].get_text(strip=True)
                    name_and_location = li_elements[1].find_all()
                    company_name = name_and_location[0].get_text(strip=True)
                    location = name_and_location[1].get_text(strip=True)

                    if "£" not in li_elements[2].get_text(strip=True):
                        salary = "Not Specified"
                    else:
                        salary = li_elements[2].get_text(strip=True).strip()

                    description = requests.get(job_link)
                    html_job = description.text
                    soup_job = BeautifulSoup(html_job, 'html.parser')
                    description_text = soup_job.find(itemprop="description").get_text(strip=True)
                    phone_numbers = self.get_phone_numbers(description_text)
                    job_details = [job_title, company_name, salary, location, phone_numbers, job_link, 'find-a-job',
                                   'job', 'London']
                    print(job_details)
                    self.post_to_spreadsheet(job_details)


if __name__ == "__main__":
    BASE_LINK = "https://findajob.dwp.gov.uk"
    SPREADSHEET_URL = "https://script.google.com/macros/s/AKfycbzJ8ePGlm1RqvIGbSWtYEaRbdEW6rqI0WsyOvaOSyRvwz7YqRbmSxrsoVwI0yDNbtTT/exec"
    scraper = JobScraper(BASE_LINK, SPREADSHEET_URL)
    scraper.scrape_jobs()
