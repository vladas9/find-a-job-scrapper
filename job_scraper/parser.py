from bs4 import BeautifulSoup

class JobParser:
    def parse_job_listings(self, html):
        """
        Extracts job listings from the HTML.
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("div", class_="search-result")

    def parse_job_details(self, job_element):
        """
        Extracts job details from a job listing element.
        """
        link = job_element.find("a")
        job_title = link.get_text(strip=True)
        job_link = link.get("href")

        job_components = job_element.find_all("ul")
        li_elements = job_components[0].find_all("li")
        date_posted = li_elements[0].get_text(strip=True)
        name_and_location = li_elements[1].find_all()
        company_name = name_and_location[0].get_text(strip=True)
        location = name_and_location[1].get_text(strip=True)

        salary = (
            li_elements[2].get_text(strip=True).strip()
            if "£" in li_elements[2].get_text(strip=True)
            else "Not Specified"
        )

        return {
            "title": job_title,
            "company": company_name,
            "salary": salary,
            "location": location,
            "url": job_link,
            "date_posted": date_posted,
        }
