from fastapi.security import HTTPBasic
from sqlalchemy import create_engine

"""Database settings"""
engine = create_engine("sqlite:///db.sqlite", echo=True, connect_args={"check_same_thread": False})


"""Security settings"""
security = HTTPBasic()


"""File settings"""
root = 'store'
