from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from sheets import get_values

def get_prices(url, range, sheet_id):

    options = Options()
    user_agent = str(os.environ.get('USER_AGENT'))
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(url)

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

    rows = get_values(spreadsheet_id=sheet_id, range=range)

    apartments = []
    for apt in apts:
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

    return rows
