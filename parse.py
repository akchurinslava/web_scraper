import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from app.database import session
from app.models import CarInfo
from makes import makes, types


class Auto24Parser:
    def __init__(self, input_car_make: str, input_page_amount: str):
        """
        Initialize method, here we define class attributes and set some ChromeDriver options.
        :param input_car_make: str
            Input field for vehicle make.
        :param input_page_amount: str
            Input field for number of pages, we redefine like int when script running.
        """
        load_dotenv()
        self.service = Service(
            executable_path=os.getenv("EXECUTABLE_PATH"), service_log_path=os.devnull
        )
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.getenv("BINARY_LOCATION")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.cars_links = []
        self.input_car_make = input_car_make.lower()
        self.input_page_amout = input_page_amount
        self.cars_list = []
        self.mapping = {
            'field-liik': 'type',
            'field-keretyyp': 'body_type',
            'field-month_and_year': 'reg',
            'field-mootorvoimsus': 'engine',
            'field-kytus': 'fuel',
            'field-labisoit': 'mileage',
            'field-vedavsild': 'drive',
            'field-seats': 'seats',
            'field-doors': 'doors',
            'field-kaigukast_kaikudega': 'transmission',
            'field-varvus': 'color',
            'field-reg_nr': 'reg_number',
            'field-tehasetahis': 'vin',
            'field-hind': 'price',
            'field-soodushind': 'bargain_price',
            'field-eksporthind': 'export_price',
        }

    def parse(self):
        """
        Our main method, here we work with auto24 pages and cars.
        Here we define and run Selenium for ChromeDriver work and run Chrome Browser.
        Here we define and run BeautifulSoup for parsing data from web pages.
        As you can see finally we store it in the list.
        """
        page_count = 0
        while True:
            base_url = f'https://eng.auto24.ee/kasutatud/nimekiri.php?bn=2&a={types.get('passenger_suv')}&b={makes.get(self.input_car_make)}&af=20&ak={page_count}'
            self.driver.get(base_url)
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            div = soup.find("div", id="usedVehiclesSearchResult-flex")
            if div:
                try:
                    listings = div.find_all("a", class_="row-link", href=lambda href: href and '/vehicles/' in href)
                    for listing in listings:
                        car_url = f'https://eng.auto24.ee{listing["href"]}'
                        self.cars_links.append(car_url)
                        self.driver.get(car_url)
                        soup_car = BeautifulSoup(self.driver.page_source, "lxml")
                        table = soup_car.find("table", class_="main-data")
                        self.car_info = {}
                        self.driver.get(car_url)
                        h1 = soup_car.find("h1", class_="commonSubtitle").text.split()
                        self.car_info['spec_name'] = ' '.join(h1)
                        breadcrumb_items = soup_car.find("div", class_="b-breadcrumbs").find_all("a", class_="b-breadcrumbs__item")
                        self.car_info['make'], self.car_info['model'] = breadcrumb_items[1].text.strip(), breadcrumb_items[2].text.strip()
                        for tr in table.find_all("tr"):
                            td_field = tr.find("td", class_="field")
                            span_value = td_field.find("span", class_="value")
                            tr_class = tr.attrs.get("class")[0]
                            if span_value == None:
                                self.car_info[self.mapping[tr_class]] = None
                            else:
                                if tr_class in ['field-labisoit']:
                                    clean_mileage = span_value.text
                                    clean_mileage = re.findall(r'\d+', clean_mileage)
                                    clean_mileage = int(''.join(clean_mileage))
                                    self.car_info[self.mapping[tr_class]] = clean_mileage
                                elif tr_class in ['field-hind', 'field-soodushind', 'field-eksporthind']:
                                    clean_price = span_value.text
                                    clean_price = int(re.sub(r'EUR\xa0|,', '', clean_price))
                                    self.car_info[self.mapping[tr_class]] = clean_price
                                    if tr_class in ['field-hind'] and td_field.find("span", class_="vat-value"):
                                        vat_value = td_field.find("span", class_="vat-value").text
                                        vat_value = re.findall(r'\d+', vat_value)
                                        vat_value = int(''.join(vat_value))
                                else:
                                    self.car_info[self.mapping[tr_class]] = span_value.text
                        self.car_info['vat'] = vat_value
                        self.car_info['link'] = car_url
                        self.cars_list.append(self.car_info)
                except Exception as e:
                    print(f'An exception occured during application was running:\n{e}')
            else:
                break
            page_count += 100
            try:
                next_page = self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-right")
                if next_page.get_attribute("class") == "btn btn-right disabled":
                    break
            except:
                if input_page_amount == page_count:
                    break

    def get_cars(self) -> list:
        """
        Return method.
        :return: list
            Each object in list is dict, in each dict we store information about each car key-value.
        """
        return self.cars_list

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    while True:
        input_car_make = input("Make of car: ")
        if input_car_make in makes:
            input_page_amount = input("Number of pages: ")
            try:
                input_page_amount = int(input_page_amount) * 100
                break
            except:
                input_page_amount = input_page_amount
                break
    parser = Auto24Parser(input_car_make, input_page_amount)
    parser.parse()
    # In the loop below we iterate through cycle, after loop will finshed
    # each car will commit and push to DB.
    for car in parser.get_cars():
        car_info = CarInfo(**car)
        session.add(car_info)
    session.commit()
    session.close()
    parser.close()