import sys
from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.database import session
from app.models import CarInfo


class CarsAnalytics:
    def __init__(self, input_cycle, input_cycle_period):
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
                first_day_car = next(car for car in self.grouped_cars[first_date] if car.link == car_link)
                self.sold_cars[(first_day_car.make, first_day_car.model)] += 1
                self.list_cars.append((first_day_car.make, first_day_car.model, first_day_car.price))

        self.sorted_sold_cars = sorted(self.sold_cars.items(), key=lambda x: x[1], reverse=True)
        self.sorted_list_cars = sorted(self.list_cars, key=lambda x: x[2], reverse=True)

    def get_stats(self):
        return self.sorted_sold_cars


if __name__ == "__main__":
    cycle = sys.argv[1]
    period = sys.argv[2]
    statistics = CarsAnalytics(cycle, int(period))
    statistics.cars_analyze()
    print("Best sales:")
    for (make, model), count in statistics.get_stats():
        print(f"{make} {model}: {count} sales")
    print("List of cars:")
    for (make, model, price) in statistics.sorted_list_cars:
        print(f"{make} {model}: {price}€")
