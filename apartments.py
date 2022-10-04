from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException   
from selenium.webdriver.common.by import By
from sheets import get_values

def get_apt_details(element):
    text = element.get_attribute('innerText').strip().split('\n')
    if len(text) < 2:
        text = element.get_attribute('innerText').strip().split(' ')
    return text[1]

def get_prices(url, range, sheet_id):
    options = Options()
    user_agent = str(os.environ.get('USER_AGENT'))
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(url)

    expand_btns = driver.find_elements(By.XPATH, '//button[@class="js-priceGridShowMoreLabel"]')

    for btn in expand_btns:
        if "Show More" in btn.get_attribute('innerText') and btn.is_enabled():
            try:
                btn.click()
            except WebDriverException:
                continue

    apts = []
    grids = driver.find_elements(By.CLASS_NAME, "hasUnitGrid")

    for grid in grids:

        # Get Grid Details
        details = grid.find_element(
            By.CLASS_NAME, "detailsTextWrapper")
        tags = details.find_elements(By.TAG_NAME, "span")

        beds = tags[0].get_attribute('innerText')

        grid_beds = ""
        grid_baths = ""

        if "Studio" in beds:
            grid_beds = '0.5'
        else:
            grid_beds = beds.split('bed')[0]

        grid_baths = tags[1].get_attribute(
            'innerText').split('bath')[0]

        containers = grid.find_elements(By.CSS_SELECTOR, "div.grid-container.js-unitExtension")
        for container in containers:

            try:
                elements = container.find_elements(By.XPATH, "./child::*")
                unit = {}

                for element in elements:
                    element_text = element.get_attribute('innerText')

                    if "Unit" in element_text and not "availibility" in element_text:
                        unit['name'] = get_apt_details(element)
                    if "price" in element_text:
                        unit['price'] = get_apt_details(element)
                    if "square feet" in element_text:
                        unit['size'] = get_apt_details(element)
                    if "availibility" in element_text:
                        unit['availability'] = get_apt_details(element)

                # Get Bed & Baths
                unit['beds'] = grid_beds
                unit['baths'] = grid_baths

                if "price" in unit:
                    converted_price = float(
                        unit['price'].split("$")[1].replace(",", ""))
                    converted_size = int(unit['size'].replace(",", ""))
                    unit['priceSqFt'] = "$" + \
                        str(round(converted_price / converted_size, 2))
                else:
                    unit['priceSqFt'] = '0'

                # Get Concessions
                concessions = driver.find_elements(
                    By.ID, 'rentSpecialsSection')

                if len(concessions) > 0:
                    unit['concessions'] = concessions[0].find_element(
                        By.TAG_NAME, 'p').get_attribute('innerText')

                if "name" in unit:
                    apts.append(unit)

            except Exception:
                continue
    try:
        rows = get_values(spreadsheet_id=sheet_id, range=range)

        apartments = []
        for apt in apts:
            vals = [''] * len(rows[0])
            vals[0] = datetime.today().strftime('%m/%d/%Y')
            vals[1] = apt['name']
            vals[2] = apt['beds']
            vals[3] = apt['baths']
            vals[4] = apt['size']
            vals[5] = apt['price']
            vals[6] = apt['priceSqFt']
            vals[7] = apt['availability']
            if 'concessions' in apt:
                vals[8] = apt['concessions']

            apartments.append(vals)
        rows += apartments

        return rows

    except BaseException as err:
        raise Exception(err)
