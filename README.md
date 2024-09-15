# FastAPI Machine Learning Task

This repository contains a project to develop a machine learning model based on sustainable energy data and integrate it with a FastAPI-based REST API.

## Project Structure
```
FastAPI_ML_Task/

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fastapi_ml_task.git
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Jupyter notebook to train the model:
   - Navigate to `models/model_training.ipynb`.
   - Ensure the dataset is in the `data/` folder.
   - Run the notebook step by step.

# FastAPI Machine Learning Task

This repository contains a project to develop a machine learning model based on sustainable energy data and integrate it with a FastAPI-based REST API.

## Project Structure
```
FastAPI_ML_Task/
│
├── data/                          # Folder to store the dataset
│   └── global-data-on-sustainable-energy.csv
├── models/                        # Folder to store model files and notebooks
│   ├── model_training.ipynb       # Jupyter notebook for the ML workflow
│   ├── trained_model.pkl          # Initial trained model
│   ├── tuned_model.pkl            # Tuned XGBoost model
│   └── model_utils.py             # Utility functions for model training
├── app/                           # Folder for FastAPI application
│   ├── main.py                    # Main FastAPI application with endpoints
│   ├── database_setup.py          # Database setup and connection management
├── Dockerfile                     # Dockerfile for building the FastAPI container
├── docker-compose.yml             # Docker Compose file to orchestrate FastAPI and PostgreSQL services
├── requirements.txt               # List of Python dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore file to avoid committing sensitive files (like .env)

```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fastapi_ml_task.git
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Jupyter notebook to train the model:
   - Navigate to `models/model_training.ipynb`.
   - Ensure the dataset is in the `data/` folder.
   - Run the notebook step by step.

## Database Setup (PostgreSQL)

To set up the PostgreSQL database, follow these steps:

1. **Install PostgreSQL and pgAdmin4**: 
   Ensure that PostgreSQL and pgAdmin4 are installed and running on your machine.

2. **Configure the Database URL**:
   In the `app/database_setup.py` file, update the `DATABASE_URL` with your PostgreSQL credentials.

   Example:
   ```
   DATABASE_URL = "postgresql://your_username:your_password@localhost/your_dbname"
    ```

3. **Initialize the Database**:
   Run the following command to initialize the database and create the tables:

   ```
   python app/main.py
   ```

   This will create the following tables in your PostgreSQL database:
   - **energy_data**: For storing energy data records.
   - **predictions**: For storing prediction results.

5. **Verify the Database**:
   - You can open **pgAdmin4** and verify that the tables have been successfully created.
  
---

## Setting Up the Environment Variables

You will need to create a `.env` file in the root directory of this project.

### Steps to Set Up `.env`:

1. **Create a `.env` file**:
   - In the root of the project (where the `docker-compose.yml` file is located), create a new file named `.env`.

2. **Add the following content** to the `.env` file:
   ```
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_database_name
   ```

   - Replace `your_postgres_username`, `your_postgres_password`, and `your_database_name` with your actual PostgreSQL credentials. For example:

   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=ml_api
   ```

3. **Database URL**:
   - The environment variables in the `.env` file will be used to automatically configure the database connection inside the **`docker-compose.yml`** and **`app/database_setup.py`**.
   - The database connection string will look like this:
     ```
     postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
     ```

---


### Run the FastAPI Application
Start the FastAPI server by running:

```
uvicorn app.main:app --reload
```

You can access the API documentation and test the endpoints at **`http://127.0.0.1:8000/docs`**.

## API Endpoints

### 1. `/upload-data` (POST)
Uploads a CSV file containing energy data and stores it in the PostgreSQL database.

- **Request**: Upload a CSV file with columns `Entity`, `Year`, `Primary energy consumption per capita (kWh/person)`, and `Renewable energy share in the total final energy consumption (%)`.

### 2. `/get-data/{country}` (GET)
Retrieves energy data for a specific country from the PostgreSQL database.

- **Parameters**: `country` - The name of the country (e.g., "Afghanistan").

### 3. `/train-model` (POST)
Trains an XGBoost model using the uploaded energy data and saves the trained model.

- **Response**: Confirms that the model was successfully trained and saved.

### 4. `/predict` (POST)
Makes predictions using the trained model based on the energy production provided.

- **Parameters**: 
  - `energy_production`: The amount of energy production (numeric value e.g., "5000").
  
- **Response**: Returns the predicted value for the renewable energy share.

## Testing

You can test the API using the Swagger UI at **`http://127.0.0.1:8000/docs`**, or with tools like **Postman**.
=======


## Running the Project with Docker

To run the FastAPI application and PostgreSQL database using Docker, follow these steps:

### Prerequisites

- Ensure Docker and Docker Compose are installed on your machine.

### Steps:

1. **Build the Docker containers**:
   ```
   docker-compose build
   ```

2. **Start the services** (FastAPI and PostgreSQL):
   ```
   docker-compose up
   ```

   This will start both the FastAPI application and PostgreSQL database.

3. **Access the API**:
   - The FastAPI application will be available at **`http://localhost:8000`**.
   - The API documentation (Swagger UI) will be available at **`http://localhost:8000/docs`**.

4. **Interacting with the API**:
   - **Upload Data**: Use the `/upload-data` endpoint to upload the dataset (CSV file).
   - **Train the Model**: Call the `/train-model` endpoint to train the XGBoost model.
   - **Make Predictions**: Use the `/predict` endpoint to make predictions based on the trained model.
   - **Retrieve Data**: Fetch energy data for a specific country via the `/get-data/{country}` endpoint.

5. **Stopping the Docker services**:
   ```
   docker-compose down
   ```

   This will stop and remove the containers.

### Setting Up the Environment Variables

- The environment variables (like PostgreSQL credentials) are configured in the `.env` file. Each user should create a `.env` file in the root directory with the following content:

```
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=ml_api
```

- Replace `your_postgres_username` and `your_postgres_password` with your actual PostgreSQL credentials.



