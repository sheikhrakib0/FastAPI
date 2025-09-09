from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse


# importing model
with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# pydantic class
class UserInput(BaseModel):
   
   age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
   weight: Annotated[float, Field(..., gt=0, description="Weight of the user")]
   height: Annotated[float, Field(..., gt=0, description="Height of the user in meter")]
   income_lpa: Annotated[float, Field(..., gt=0, description="Income of the user in LPA")]
   smoker: Annotated[bool, Field(..., description="Smoking habit of the user")]
   occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the user")]
   
   @computed_field
   @property
   def bmi(self) -> float:
       return self.weight/(self.height**2)
   
   @computed_field
   @property
   def lifestyle_risk(self) -> str:
       if self.smoker and self.bmi > 30:
            return "high"
       elif self.smoker or self.bmi > 27:
            return "medium"
       else:
            return "low"
       
    
# Building endpoint
@app.get('/')
def get():

    return "Welcome the Insurance API"

@app.post('/predict')
def predict(data: UserInput):

    input_df = pd.DataFrame([{
        "age": data.age,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
        "bmi": data.bmi,
        "lifestyle_risk":data.lifestyle_risk
    }])
    result = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"Predicted Category": result})
