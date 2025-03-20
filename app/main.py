from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
from models import Customer, Invoice, Transaction
from db import create_all_tables
from .routers import customers, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

db_customers: list[Customer] = []

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





@app.post("/invoices")
async def create_invoice(invoice_data:Invoice):
    return invoice_data
