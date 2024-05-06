from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import gzip

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    residence_city: str
    socioeconomic_level: int
    civil_status: str
    age: int
    state: str
    province: str
    vulnerable_group: int
    desired_program: str
    family_income: int
    father_level: str
    mother_level: str
    dropout: str
    stem_subjects: float
    h_subjects: float
    avg_subject: float

@app.post("/predict/")
async def predict(item: Item):
    with gzip.open('models/scaler.gz', 'rb') as f:
        scaler = joblib.load(f)

    features = [[
        item.socioeconomic_level, item.age, item.vulnerable_group,
        item.family_income, item.stem_subjects, item.h_subjects, item.avg_subject
    ]]

    features_scaled = scaler.transform(features)

    model = joblib.load('models/random_forest_model.keras')

    prediction = model.predict(features_scaled)

    return {"prediction": prediction[0]}

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

# RUN in root -> uvicorn src.serve.main:app --reload --port 8000