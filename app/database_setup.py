from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Retrieve the DATABASE_URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create the PostgreSQL engine
engine = create_engine(DATABASE_URL)

# Define the EnergyData table
class EnergyData(Base):
    __tablename__ = 'energy_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    energy_production = Column(Float, nullable=True)
    renewables_percentage = Column(Float, nullable=True)

# Define the Predictions table
class Predictions(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    prediction_date = Column(DateTime, nullable=False)
    predicted_value = Column(Float, nullable=False)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
