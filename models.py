#this models.py is used to connect with pydantic and work with api's
from pydantic import BaseModel


class Product(BaseModel):
    id:int
    name:str
    description:str
    price:float
    quantity:int