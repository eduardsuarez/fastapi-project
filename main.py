from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
import pydantic
from pydantic.main import BaseModel

app = FastAPI()

class Customer(BaseModel):
    name : str
    description : str | None
    age : int
    email : str

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
    "ES": "Europe/Madrid",
    "US": "America/New_York"
}

@app.get("/")
async def root():
    return {"message":"HOLA, BIENVENIDO, Eduard Suarez"}

@app.get("/time/{iso_code}")
async def time(iso_code:str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if timezone_str is None:
        raise ValueError(f"Invalid ISO code: {iso}")
    tz = ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.post("/customers")
async def customers(custom_data:Customer):
    return custom_data
