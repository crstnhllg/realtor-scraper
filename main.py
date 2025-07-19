from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import random
import logging
import pandas as pd
import sys


CHROME_OPTIONS = [
    '--no-first-run',
    '--no-service-autorun',
    '--disable-blink-features=AutomationControlled',
]


class RealtorScraper:
    """
    A web scraper that collects real estate listing data from Realtor.com
    for a specified U.S. ZIP code.
    """
    def __init__(self, zipcode):
        """
        Initializes the scraper with the given ZIP code and sets up the Chrome driver.

        Args:
            zipcode (int): The ZIP code to scrape listings for.
        """
        self.zipcode = zipcode
        self.page = 1
        self.data = []

        options = uc.ChromeOptions()
        for arg in CHROME_OPTIONS:
            options.add_argument(arg)

        self.driver = uc.Chrome(options=options)


    def run(self):
        """
        Runs the scraping process:
        - Loads search result pages (up to 5 by default).
        - Extracts listing data from each page.
        - Saves results to a CSV file if any listings are found.
        """
        logging.info(f'Starting scraper for ZIP code: {self.zipcode}')

        try:
            while self.page <= 5:
                if not self.load_page():
                    break
                self.scrape_data()
                self.page += 1
        finally:
            self.driver.quit()


        if self.data:
            pd.DataFrame(self.data).to_csv(f'output.csv', index=False)
            logging.info(f'Scraping complete. {len(self.data)} properties collected and saved to CSV.')
        else:
            logging.debug('No data was scraped.')


    def get_page_url(self) -> str:
        """
         Constructs the Realtor.com search URL for the current page.

         Returns:
             str: The URL for the current search results page.
         """
        return f'https://www.realtor.com/realestateandhomes-search/{self.zipcode}/pg-{self.page}'


    def load_page(self, retries=3) -> bool:
        """
        Attempts to load the current page in the browser, with optional retries.

        Args:
            retries (int): Number of retry attempts if the page fails to load.

        Returns:
            bool: True if the page loaded successfully; False otherwise.
        """
        url = self.get_page_url()
        for retry in range(1, retries + 1):
            try:
                time.sleep(random.uniform(1.5, 3.5))
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//section[contains(@class, "PropertiesList_propertiesContainer")]')))
                return True

            except Exception as e:
                logging.warning(f'Error: {e}')
                logging.warning(f'Attempt {retry}: Failed to load page. Retrying...')

        logging.error('Loading page failed.')
        return False


    def scrape_data(self):
        """
        Extracts data from each listing on the current search results page.

        Scraped fields include:
        - Property status
        - Price
        - Bed, Bath, Sqft
        - Lot Size
        - Address
        - Link

        Appends the extracted data to self.data.
        """
        try:
            properties = self.driver.find_elements(By.XPATH, f'.//div[@data-search-rank]')
            logging.info(f'Scraping data for {len(properties)} properties, page {self.page}')
            for prop in properties:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", prop)
                time.sleep(random.uniform(0.5, 1.5))
                try:
                    link = prop.find_element(
                        By.XPATH, './/div[contains(@class, "card-content")]//a').get_attribute('href')
                    status = prop.find_element(
                        By.XPATH, './/div[@data-testid="card-description"]/div').text
                    price = prop.find_element(
                        By.XPATH, './/div[@data-testid="card-price"]/span').text
                    bed = prop.find_element(
                        By.XPATH, './/ul/li[@data-testid="property-meta-beds"]/span').text
                    bath = prop.find_element(
                        By.XPATH, './/ul/li[@data-testid="property-meta-baths"]/span').text
                    sqft = prop.find_element(
                        By.XPATH, './/ul/li[@data-testid="property-meta-sqft"]/span').text
                    lot_size = prop.find_element(
                        By.XPATH, './/ul/li[@data-testid="property-meta-lot-size"]/span').text
                    address = ' '.join(prop.find_element(
                        By.XPATH, './/div[contains(@class, "card-address")]').text.split())

                    data = {
                        'Property Status': status,
                        'Price': price,
                        'Bed': bed or 'N/A',
                        'Bath': bath or 'N/A',
                        'Sqft': sqft or 'N/A',
                        'Lot Size': lot_size or 'N/A',
                        'Address': address,
                        'Link': link,
                    }
                    self.data.append(data)

                except Exception as e:
                    logging.debug(f'Error fetching data: {e}')
        except Exception as e:
            logging.debug(f'No properties found on page: {e}.')


def main(zipcode):
    """
    Entry point for the script. Sets up logging and runs the scraper.

    Args:
        zipcode (int): The ZIP code to scrape listings for.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    scraper = RealtorScraper(zipcode)
    scraper.run()



if __name__ == '__main__':
    zipcode = int(sys.argv[1]) if len(sys.argv) > 1 else 75034
    main(zipcode)