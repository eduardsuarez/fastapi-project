from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
import pydantic
from sqlmodel import select

from models import Customer, CustomerCreate, Invoice, Transaction
from db import SessionDep, create_all_tables
app = FastAPI(lifespan=create_all_tables)

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

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data:CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.post("/transactions")
async def create_transaction(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data:Invoice):
    return invoice_data
