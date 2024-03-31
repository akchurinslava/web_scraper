import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from makes import makes, types


class Auto24Parser:
    def __init__(self, input_car_make: str, input_page_amount: str):
        """
        Our initialize method, here we define class attributes and set some ChromeDriver options
        """
        load_dotenv()
        self.service = Service(
            executable_path=os.getenv("EXECUTABLE_PATH"),
            service_log_path=os.devnull
        )
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.getenv("BINARY_LOCATION")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.cars = []
        self.input_car_make = input_car_make.lower()
        self.input_page_amout = input_page_amount
        self.cars_list = []

    def parse(self) -> list:
        """
        Our main method, here we work with auto24 pages and cars.
        Here we define and ran Selenium for ChromeDriver work and ran Chrome Browser.
        Here we define and ran BeautifulSoup for parsing data from web pages.
        As you can see finally we store it in list.
        """
        page_count = 0
        if self.input_car_make == 'all':
            base_url = f'https://eng.auto24.ee/kasutatud/nimekiri.php?bn=2&a={types.get('all_types')}'
        while True:
            base_url = f'https://eng.auto24.ee/kasutatud/nimekiri.php?bn=2&a={types.get('all_types')}&b={makes.get(self.input_car_make)}&af=100&ak={page_count}'
            self.driver.get(base_url)
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            div = soup.find("div", id="usedVehiclesSearchResult-flex")
            if div:
                listings = div.find_all("a", class_='row-link', href=True)
                for listing in listings:
                    car_url = f'https://eng.auto24.ee{listing["href"]}'
                    self.cars.append(car_url)
                for car in (self.cars):
                    self.driver.get(car)
                    self.cars_list.append(car)
            else:
                break
            try:
                next_page = self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-right")
                if next_page.get_attribute("class") == "btn btn-right disabled":
                    break
            except:
                if input_page_amount == page_count:
                    break
            page_count += 100
            print(self.cars_list)

    def get_cars(self):
        return self.cars

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    input_car_make = input('Введите марку машины: ')
    input_page_amount = input('Сколько страниц сканировать: ')
    try:
        input_page_amount = int(input_page_amount) * 100
    except:
        input_page_amount = input_page_amount
    parser = Auto24Parser(input_car_make, input_page_amount)
    parser.parse()
    car_links = parser.get_cars()
    # print(car_links)
    parser.close()
