import requests
import cloudscraper


class JobFetcher:
    def __init__(self, timeout=10):
        """
        Initializes the JobFetcher with a specified timeout.

        Args:
            timeout (int): Maximum time (in seconds) to wait for a response.
        """
        self.timeout = timeout
        self.scraper = cloudscraper.create_scraper()

    def fetch(self, url):
        """
        Fetches the HTML content of a webpage using the appropriate method.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the page.

        Raises:
            requests.exceptions.RequestException: For connection or timeout errors.
        """
        try:
            if url.startswith("https://www.cv-library.co.uk"):
                print(f"Using cloudscraper for URL: {url}")
                response = self.scraper.get(url, timeout=self.timeout)
            else:
                print(f"Using requests for URL: {url}")
                response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            print(f"Request timed out for URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching URL: {url}. Error: {e}")
        return None


