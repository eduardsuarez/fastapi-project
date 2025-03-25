from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)

customer = Customer(
    name="Eduard Suárez",
    description="Software Engineer",
    age=26,
    email="esuarez@unipamplona.edu.co"
)

session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
        customer_id = customer.id,
        description=f"Transaction {x}",
        ammount= 5 * x
    )
)
    
session.commit()