from utils.file_utils import convert_json_to_dict as cj
from utils.file_utils import add_to_json as aj
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
    if base_link == 'find-a-job':
        return f"{base_link}/search?adv=1&qwd={keyword}&cat=28&f=1&w={city}&d=25&pp=25&sb=date&sd=down"
    elif base_link == 'cv-library':
        return (f"{base_link}/{keyword.replace(' ', '-')}-jobs-in-{city}"
                f"?categories=construction&distance=25&order=date&posted=1&us=1")

def check_link(link):
    json_path = ""

    if link.startswith("https://www.cv-library.co.uk"):
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