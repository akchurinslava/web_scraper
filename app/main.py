import os
import subprocess

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates") 
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> None:
    """
    Home page.
    :param request: Request
        type of HTTP-request param
    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
async def home_post(request: Request) -> None:
    """
    Defined post form on the home page.
    With post form we run run_analytics().
    :param request: Request
        Type of HTTP-request param
    """
    form_data = await request.form()
    cycle = form_data.get("cycle")
    period = form_data.get("period")
    best_sales, car_list = run_analytics(cycle, period)
    return templates.TemplateResponse("results.html", {"request": request, "best_sales": best_sales, "car_list": car_list})


def run_analytics(cycle: str, period: int) -> list:
    """
    Function that with subprocces run the ./analytics.py script, which send us
    analytic results in response.
    :param cycle: str
        Select field with period of analytic, can be hours, days, weeks etc
        related on relativedelta lib.
    :param period: int
        Input field with number of for time period, must be number.
    :return car_list: list
        List of all saled vehicles.
    :return best_sales: list
        List of best sales of vehicles.
    """
    result = subprocess.run(["python", os.getenv("ANALYTICS_LOCATION"), cycle, str(period)], capture_output=True, text=True)
    best_sales = []
    car_list = []
    current_list = None
    for line in result.stdout.split('\n'):
        if line.startswith("Best sales:"):
            current_list = best_sales
        elif line.startswith("List of cars:"):
            current_list = car_list
        elif current_list is not None:
            current_list.append(line.strip())
    return best_sales, car_list[:-1]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

