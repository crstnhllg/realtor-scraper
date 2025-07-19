# Realtor.com Scraper

This is a simple Python script that scrapes real estate listings from Realtor.com based on a given U.S. ZIP code. It collects basic property information such as price, number of beds and baths, square footage, lot size, address, and the listing link.

## Features

* Scrapes listings for a given ZIP code
* Collects essential property data
* Saves results to a CSV file (`output.csv`)
* Uses undetected ChromeDriver to help avoid bot detection

## Requirements

* Python 3.7+
* Google Chrome installed

## Installation

1. Clone this repository or download the script.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with a ZIP code:

```bash
python script.py 75034
```

If no ZIP code is provided, it defaults to `75034`.

## Output

A file named `output.csv` will be created in the same directory with the scraped results.

## Disclaimer

This project is for educational and personal use only. Do not use it for commercial purposes or excessive scraping that may violate Realtor.com's terms of service.
