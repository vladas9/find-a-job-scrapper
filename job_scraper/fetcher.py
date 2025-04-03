import requests
import cloudscraper
import time

class JobFetcher:
    def __init__(self, timeout=10, use_proxy=False, proxy_url=None):
        """
        Initializes the JobFetcher with a specified timeout and optional proxy.

        Args:
            timeout (int): Maximum time (in seconds) to wait for a response.
            use_proxy (bool): Whether to use a proxy.
            proxy_url (str): The URL for the proxy server (e.g., "http://proxy.example.com:port").
        """
        self.timeout = timeout

        # Define custom headers to mimic a real browser.
        custom_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/105.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        # Create a cloudscraper instance with a custom browser profile.
        self.scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "mobile": False
            }
        )
        # Update the scraper's headers after creation.
        self.scraper.headers.update(custom_headers)

        self.proxies = None
        if use_proxy and proxy_url:
            self.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }

    def fetch(self, url):
        """
        Fetches the HTML content of a webpage.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the page, or None if fetching fails.
        """
        try:
            # Use cloudscraper for specific URLs, otherwise use requests.
            if url.startswith("https://www.cv-library.co.uk") or url.startswith("https://findajob.dwp.gov.uk"):
                print(f"Using cloudscraper for URL: {url}")
                response = self.scraper.get(url, timeout=self.timeout, proxies=self.proxies)
            else:
                print(f"Using requests for URL: {url}")
                response = requests.get(url, timeout=self.timeout, proxies=self.proxies)
            
            response.raise_for_status()
            return response.text

        except requests.exceptions.Timeout:
            print(f"Request timed out for URL: {url}")
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                print(f"Error: {e}. Status Code: {e.response.status_code}")
                print("Response Headers:", e.response.headers)
                print("Response snippet:", e.response.text[:200])
            else:
                print(f"An error occurred while fetching URL: {url}. Error: {e}")
        return None
