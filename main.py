from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


options = Options()
# options.add_experimental_option("detach", True)


def main():
    load_dotenv()
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

            if "name" in unit:
                apts.append(unit)

    print(apts)


main()
