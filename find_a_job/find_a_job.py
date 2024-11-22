import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -----------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import utilities.link_builder as lb
import utilities.lyb_for_files as lf


BASE_LINK = "https://findajob.dwp.gov.uk"
for link in lb.build_link(BASE_LINK):
    print(link)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_list = soup.find_all('div', class_='search-result')

    for job in job_list:
        job_link = job.find('a', class_='govuk-link')['href']
        respone = requests.get(job_link)
        job_soup = BeautifulSoup(respone.text, 'html.parser')
        job_title = job_soup.find('h1', class_='govuk-heading-l govuk-!-margin-top-8').text.strip()
        print(job_title)
        
        
        print(salary_row)
