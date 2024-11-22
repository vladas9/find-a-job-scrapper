from utilities.lyb_for_files import read_keywords_and_cities



def build_link(base_link):

    keywords = read_keywords_and_cities("keywords.txt")
    cities = read_keywords_and_cities("cities.txt")
    link_list = []
    for keyword in keywords:
        for city in cities:
            if base_link == "https://findajob.dwp.gov.uk":
                link_list.append(f"{base_link}/search?adv=1&qwd={keyword}&cat=28&f=1&w={city},%20UK&d=25&pp=25&sb=date&sd=down")
    return link_list