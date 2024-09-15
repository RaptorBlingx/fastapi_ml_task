from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database_setup import engine, EnergyData, Predictions, SessionLocal, init_db
import pandas as pd
import pickle
from models.model_utils import train_model  # Import your custom train_model function

# Initialize FastAPI
app = FastAPI()

# Initialize the database (create tables if they don't exist)
init_db()
print("Database initialized and tables created.")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Upload data and store in PostgreSQL
@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = pd.read_csv(file.file)

    # Strip whitespace and clean numeric values
    data['Primary energy consumption per capita (kWh/person)'] = pd.to_numeric(
        data['Primary energy consumption per capita (kWh/person)'], errors='coerce')
    data['Renewable energy share in the total final energy consumption (%)'] = pd.to_numeric(
        data['Renewable energy share in the total final energy consumption (%)'], errors='coerce')

    for _, row in data.iterrows():
        energy_data = EnergyData(
            country=row['Entity'],
            year=row['Year'],
            energy_production=row['Primary energy consumption per capita (kWh/person)'],
            renewables_percentage=row['Renewable energy share in the total final energy consumption (%)']
        )
        db.add(energy_data)
    db.commit()
    return {"message": "Data uploaded successfully"}

# Endpoint: Retrieve energy data for a specific country
@app.get("/get-data/{country}")
async def get_data(country: str, db: Session = Depends(get_db)):
    data = db.query(EnergyData).filter(EnergyData.country == country).all()
    if not data:
        return {"message": "No data found for this country"}
    return data

# Endpoint: Train the model using the uploaded data
@app.post("/train-model")
async def train_model_endpoint(db: Session = Depends(get_db)):
    # Fetch all the data from the database
    data = db.query(EnergyData).filter(EnergyData.energy_production.isnot(None),
                                       EnergyData.renewables_percentage.isnot(None)).all()

    # Convert the data into a DataFrame
    df = pd.DataFrame([{
        'country': d.country,
        'year': d.year,
        'energy_production': d.energy_production,
        'renewables_percentage': d.renewables_percentage
    } for d in data])

    # Clean the DataFrame if necessary
    df = df.dropna()  # Ensure no null values in the DataFrame

    # Call the training function from your notebook or utility file
    model = train_model(df)  # This should return the trained model
    
    # Save the trained model
    with open("models/trained_model.pkl", "wb") as f:
        pickle.dump(model, f)

    return {"message": "Model trained and saved successfully"}


# Endpoint: Make predictions based on user input
@app.post("/predict")
async def predict(energy_production: float):
    # Load the trained model
    with open("models/trained_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Prepare input data for prediction
    input_data = {'energy_production': energy_production}

    # Make the prediction
    prediction = model.predict(pd.DataFrame([input_data]))[0]

    # Convert numpy.float32 to a native Python float
    return {"predicted_value": float(prediction)}


