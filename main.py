from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

from sheets import get_values, write_values


options = Options()
# options.add_experimental_option("detach", True)


def main():
    load_dotenv()

    SHEET_ID = str(os.environ.get('SPREADSHEET'))

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(
        "https://www.apartments.com/district-west-gables-west-miami-fl/3f1qyse/")

    apts = []
    grids = driver.find_elements(By.CLASS_NAME, "pricingGridItem")
    for grid in grids:
        containers = grid.find_elements(By.CLASS_NAME, "grid-container")
        for container in containers:
            unit = {}

            # Get Unit Name
            unit_selector = container.find_element(By.CLASS_NAME, "unitColumn").get_attribute('innerHTML').split('\n')[2]
            splitter = '<span class="screenReaderOnly">Unit</span>'
            if splitter in unit_selector:
                unit['name'] = unit_selector.split(splitter)[1].strip()

            # Get Unit Price
            price_selector = container.find_element(By.CLASS_NAME, "pricingColumn")
            tags = price_selector.find_elements(By.TAG_NAME, "span")
            if len(tags) > 0:
                unit['price'] = tags[1].get_attribute('innerHTML').strip()

            # Get Sqt. Ft
            size_selector = container.find_element(By.CLASS_NAME, "sqftColumn")
            tags = size_selector.find_elements(By.TAG_NAME, "span")
            if len(tags) > 0:
                unit['size'] = tags[1].get_attribute('innerHTML').strip()

            # Get Availability
            availability_selector = container.find_element(By.CLASS_NAME, "availableColumn")
            tags = availability_selector.find_elements(By.TAG_NAME, "span")
            if len(tags) > 0:
                unit['availability'] = tags[0].get_attribute('innerHTML').split('<span class="screenReaderOnly">availibility </span>')[1].strip().strip()

            # Get Apt Details
            details = grid.find_element(By.CLASS_NAME, "detailsTextWrapper")
            tags = details.find_elements(By.TAG_NAME, "span")
            beds = tags[0].get_attribute('innerHTML')
            if "Studio" in beds:
                unit['beds'] = "Studio"
            else:
                unit['beds'] = tags[0].get_attribute('innerHTML').split('bed')[0].strip()
            unit['baths'] = tags[1].get_attribute('innerHTML').split('bath')[0].strip()

            if "price" in unit:
                converted_price = float(unit['price'].split("$")[1].replace(",", ""))
                converted_size = int(unit['size'].replace(",", ""))
                unit['priceSqFt'] = "$" + str(round(converted_price / converted_size, 2))
            else:
                unit['priceSqFt'] = '0'

            if "name" in unit:
                apts.append(unit)

    rows = get_values(spreadsheet_id=SHEET_ID, range='District West Gables!C:J')

    apartments = []
    for apt in apts:
        print('beds: ', apt['beds'])
        vals = [''] * len(rows[0])
        vals[0] = datetime.today().strftime('%d/%m/%Y')
        vals[1] = apt['name']
        vals[2] = apt['beds']
        vals[3] = apt['baths']
        vals[4] = apt['size']
        vals[5] = apt['price']
        vals[6] = apt['priceSqFt']
        vals[7] = apt['availability']

        apartments.append(vals)

    rows += apartments

    write_values(spreadsheet_id=SHEET_ID, range='District West Gables!C:J', values=rows)

main()
