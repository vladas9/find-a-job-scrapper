from utils.file_utils import convert_json_to_dict as cj
from utils.file_utils import add_to_json as aj
import re
def build_link(base_link, keyword, city):
    """
    Builds a list of job search links based on keywords and cities.

    Args:
        base_link (str): The base URL for the job search site.
        keyword (str): The keyword to search for.
        city (str): The city to search in.
    Returns:
        str: a link to the job search
    """
    if base_link == 'https://findajob.dwp.gov.uk':
        return f"{base_link}/search?adv=1&qwd={keyword}&cat=28&f=3&w={city}&d=25&pp=25&sb=date&sd=down"
    elif base_link == 'https://www.cv-library.co.uk':
        return (f"{base_link}/{keyword.replace(' ', '-')}-jobs-in-{city}"
                f"?categories=construction&distance=25&order=date&posted=3&us=1")
    else:
        raise ValueError(f"Unsupported base_link: {base_link}")

def check_link(link):
    json_path = ""

    if link.startswith("/job/"):
        pattern = r"\/job\/(\d+)"

        # Search for the pattern in the URL
        match = re.search(pattern, link)
        job_id = match.group(1)
        link = f'https://www.cv-library.co.uk/job/{job_id}'
        json_path = "scraped_jobs/cv_library.json"
    elif link.startswith("https://findajob.dwp.gov.uk") :
        json_path = "scraped_jobs/find_a_job.json"

    job_list = cj(json_path)

    if link in job_list:
        checker = False
    else:
        checker = True
        job_list.append(link)
        aj(job_list, json_path)
    return checker