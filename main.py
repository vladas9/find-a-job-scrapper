import time
from config.settings import BASE_LINK, SPREADSHEET_URL
from job_scraper.scraper import JobScraper

def main():
    while True:
        try:
            print("Starting job scraper...")
            scraper = JobScraper(BASE_LINK, SPREADSHEET_URL)
            scraper.scrape_jobs()
            print("Job scraper completed. Waiting for the next run...")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()
