import sys
from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.database import session
from app.models import CarInfo


class CarsAnalytics:
    def __init__(self, input_cycle: str, input_cycle_period: int):
        """
        Initalize method. Here is defined some variables with specific data types.
        Realized mapping for relativedata lib.
        :param cycle: str
            Select field with period of analytics. Can be hours, days, weeks etc
            related on relativedelta lib.
        :param period: int
            Input field with number of for time period, must be number.
        """
        self.grouped_cars = defaultdict(list)
        self.sold_cars = defaultdict(int)
        self.sorted_sold_cars = []
        self.list_cars = []
        self.sorted_list_cars = []
        self.cycle = input_cycle.lower()
        self.cycle_input = input_cycle_period
        self.input_cycle_map = {
            'years': 'years',
            'months': 'months',
            'weeks': 'weeks',
            'days': 'days',
        }

    def cars_analyze(self):
        """
        Main script for analytics, here we run relativedelta with unpacked key-values of input_cycle_map(dict),
        executed DB query, for defined period and run loops which compare first and last day of period.
        As you can see at the end we get tuple of lists.
        """
        start_date = datetime.now() - relativedelta(**{self.input_cycle_map[self.cycle]: self.cycle_input})

        all_cars_from_db = session.query(CarInfo).filter(CarInfo.created_at >= start_date).all()

        for car in all_cars_from_db:
            sale_date = car.created_at.date()
            self.grouped_cars[sale_date].append(car)

        first_date = min(self.grouped_cars.keys())
        last_date = max(self.grouped_cars.keys())

        first_day_cars = set(car.link for car in self.grouped_cars[first_date])
        last_day_cars = set(car.link for car in self.grouped_cars[last_date])

        for car_link in first_day_cars:
            if car_link not in last_day_cars:
                sold_car = next(car for car in self.grouped_cars[first_date] if car.link == car_link)
                self.sold_cars[(sold_car.make, sold_car.model)] += 1
                self.list_cars.append((sold_car.make, sold_car.model, sold_car.price))

        self.sorted_sold_cars = sorted(self.sold_cars.items(), key=lambda x: x[1], reverse=True)
        self.sorted_list_cars = sorted(self.list_cars, key=lambda x: x[2], reverse=True)

    def get_stats(self) -> tuple:
        """
        Return method.
        :return: tuple
            Tuple of best sales and list of all saled vehicles.
        """
        return self.sorted_sold_cars, self.sorted_list_cars


if __name__ == "__main__":
    cycle = sys.argv[1]
    period = sys.argv[2]
    statistics = CarsAnalytics(cycle, int(period))
    statistics.cars_analyze()
    best_sales, list_cars = statistics.get_stats()
    print("Best sales:")
    for (make, model), count in best_sales:
        print(f"{make} {model}: {count} sales")
    print("List of cars:")
    for (make, model, price) in list_cars:
        print(f"{make} {model}: {price}€")

