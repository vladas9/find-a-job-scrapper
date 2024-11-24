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
    return f"{base_link}/search?adv=1&qwd={keyword}&cat=28&f=1&w={city}&d=25&pp=25&sb=date&sd=down"

def check_link(link):
    job_list = cj("scraped_jobs/find_a_job.json")
    if link in job_list:
        checker = False
    else:
        checker = True
        job_list.append(link)
        aj(job_list, "scraped_jobs/find_a_job.json")
    return checker