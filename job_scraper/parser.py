from bs4 import BeautifulSoup


def parse_job_details(job_element, base_link):
    """
    Extracts job details from a job listing element.
    """
    if base_link == "https://findajob.dwp.gov.uk":
        link = job_element.find("a")
        job_title = link.get_text(strip=True)
        job_link = link.get("href")

        job_components = job_element.find_all("ul")
        li_elements = job_components[0].find_all("li")
        name_and_location = li_elements[1].find_all()
        company_name = name_and_location[0].get_text(strip=True)
        location = name_and_location[1].get_text(strip=True)
        source = "findajob"

        salary = (
            li_elements[2].get_text(strip=True).strip()
            if "£" in li_elements[2].get_text(strip=True)
            else "Not Specified"
        )
    else:
        link = job_element.find("a")
        job_link = f'{base_link}/job/{link.get("data-job-id")}'
        article = job_element.find("article")
        job_title = article.get("data-job-title")
        company_name = article.get("data-company-name")
        location = article.get("data-job-location")
        salary = article.get("data-job-salary")
        source = "cv-library"

    return {
        "title": job_title,
        "company": company_name,
        "salary": salary,
        "location": location,
        "url": job_link,
        "source": source,
    }


def parse_job_listings(html, base_link):
    """
    Extracts job listings from the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    if base_link == "https://findajob.dwp.gov.uk":
        return soup.find_all("div", class_="search-result")
    ol = soup.find("ol", class_="results")
    li = ol.find_all("li", class_="results__item")
    return li

