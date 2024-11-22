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



