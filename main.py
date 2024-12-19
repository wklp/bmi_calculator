from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# SQLite Database Configuration
DATABASE_URL = "sqlite:///bmi_history.db"  
engine = create_engine(DATABASE_URL, echo=True)

# Define the BMIRecord table using SQLModel
class BMIRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight: float
    height: float
    bmi: float
    category: str

# Create the database table on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

# Pydantic model for BMI calculation request
class BMICalculatorRequest(BaseModel):
    weight: float
    height: float

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the BMI Calculator!"}

# Route to calculate BMI
@app.post("/calculate-bmi/")
def calculate_bmi(request: BMICalculatorRequest, session: Session = Depends(get_session)):
    if not request.height:
        raise HTTPException(status_code=400, detail="enter the height please.")
    if not request.weight:
        raise HTTPException(status_code=400, detail="enter the weight please.")
    if request.height < 140 or request.height >= 210 or request.weight <= 30 or request.weight >= 200:
        raise HTTPException(status_code=400, detail="Weight and height must be a true value.")

    # Calculate BMI
    bmi = request.weight / ((request.height / 100) ** 2)
    category = (
        "Underweight" if bmi < 18.5 else
        "Normal weight" if bmi < 24.9 else
        "Overweight" if bmi < 29.9 else
        "Obesity"
    )

    # Save the record in the database
    record = BMIRecord(weight=request.weight, height=request.height, bmi=round(bmi, 2), category=category)
    session.add(record)
    session.commit()
    

    return {
        "id": record.id,
        "weight": record.weight,
        "height": record.height,
        "bmi": record.bmi,
        "category": record.category
    }

# Route to view BMI history
@app.get("/bmi-history/")
def bmi_history(session: Session = Depends(get_session)):
    records = session.exec(select(BMIRecord).order_by(BMIRecord.id)).all()
    if not records:
        return {"message": "No BMI records found."}

    # Calculate percentage change for each record
    history = []
    previous_bmi = None
    for record in records:
        change_percentage = (
            (record.bmi - previous_bmi) / previous_bmi * 100 if previous_bmi else None
        )
        history.append({
            "id": record.id,
            "weight": record.weight,
            "height": record.height,
            "bmi": record.bmi,
            "category": record.category,
            "change_percentage": round(change_percentage, 2) if change_percentage else None
        })
        previous_bmi = record.bmi

    return history
