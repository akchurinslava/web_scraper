import os
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from makes import makes

make_input = input("Please, enter car name: ")

load_dotenv()

service = Service(
    executable_path=os.getenv("EXECUTABLE_PATH"),
    service_log_path=os.devnull
)
options = webdriver.ChromeOptions()
options.binary_location = os.getenv("BINARY_LOCATION")
options.add_argument('headless') # Comment it out, if you want to see browser work
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

cars = []
page_count = 0 # ak

while True:
    url = f'https:/eng.auto24.ee/kasutatud/nimekiri.php?bn=2&a=100&b=4&af=100&ak={page_count}'
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")
    # Найти div с нужными ссылками
    div = soup.find("div", id="usedVehiclesSearchResult-flex")

    # Извлечь ссылки из div
    if div:
        listings = div.find_all("a", href=True)

        # Добавить href каждой ссылки в список cars
        for listing in listings:
            link = f'https://eng.auto24.ee{listing["href"]}'
            cars.append(link)
    next_page_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-right")
    if next_page_button.get_attribute("class") == "btn btn-right disabled":
        break
    page_count+=100
    time.sleep(7)
    break


# Вывести список ссылок
print(cars)

# ... (Дальнейшая работа с извлеченными ссылками)
    
driver.quit()
