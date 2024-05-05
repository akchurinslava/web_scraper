from fastapi import FastAPI
from sqladmin import Admin, ModelView

import app.models as models
from app.database import engine

app = FastAPI()
admin = Admin(app, engine)


class CarInfoView(ModelView, model=models.CarInfo):
    column_list = [
        'id',
        'make',
        'model',
        'spec_name',
        'type',
        'body_type',
        'reg',
        'engine',
        'fuel',
        'mileage',
        'drive',
        'seats',
        'doors',
        'transmission',
        'color',
        'reg_number',
        'vin',
        'price',
        'bargain_price'
        'export_price',
        'vat'
        'link',
        'created_at',
        ]
    

class CarMakeView(ModelView, model=models.CarMake):
    column_list = [
        'id',
        'make_name',
        'code',
    ]


class CarTypeView(ModelView, model=models.CarType):
    column_list = [
        'id',
        'type_name',
        'code',
    ]


admin.add_view(CarInfoView)
admin.add_view(CarMakeView)
admin.add_view(CarTypeView)
