#this file is used to generate the tables using alchemy orm
from sqlalchemy import Column, Float, Integer, String, true
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()
class Product(Base):

    __tablename__="products"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True)
    description=Column(String)
    price=Column(Float)
    quantity=Column(Integer)