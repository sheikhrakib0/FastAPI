from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

# Pydantic Model
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='name of the patient')]
    city: Annotated[str, Field(..., description='City of the patient')]
    age: Annotated[int, Field(..., gt=0,lt=120,description='Age fo the patient')]
    gender: Annotated[Literal['Male', 'Female'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='height of the patient in cm'
    )]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient in kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/((self.height/100)**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <= 21:
            return "under weighted"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "over weighted"
        else:
            return "obese"

# Patient update class 
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(gt=0,lt=120,description='Age fo the patient', default=None)]
    gender: Annotated[Optional[Literal['Male', 'Female']], Field(description='Gender of the patient', default=None)]
    height: Annotated[Optional[float], Field(gt=0, description='height of the patient in cm', default=None
    )]
    weight: Annotated[Optional[float], Field(gt=0, description='weight of the patient in kg', default=None)]


# to laod the json file 
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

# save data
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient management system"}


@app.get('/about')
def about():
    return {"message": "A fully functional API to manage patients information"}

@app.get('/view')
def view():
    data = load_data()

    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id:str= Path(..., description='exact id of the patient in DB', example='P001')): #... defines it's compulsory
    #first loading all data 
    data = load_data()

    for patient in data:
        if patient_id in patient['id']:
            return patient
    raise HTTPException(status_code=404, detail="patient not found")

    
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort by height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid field from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order, select between asc and desc")
    
    data = load_data()
    
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # laod existing data
    data = load_data()

    # check if the patient id is available or not
    id_exists = any(item.get('id')== patient.id for item in data)
    if id_exists:
        raise HTTPException(status_code=400, detail="Patient is already exists")
    # new patient created
    data.append(patient.model_dump())

    # Save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

@app.put('/update/{patient_id}')
def patient_update(patient_id: str, patient: PatientUpdate):
    # laoding existing data
    data = load_data()

    id_exists = any(item.get('id') == patient_id for item in data)
    if not id_exists:
        raise HTTPException(status_code=400, detail='Patient not found')
    
    # extracting the targeted patients information for updating
    targeted_patient_in_db = {}
    for item in data:
        if item['id'] == patient_id:
            targeted_patient_in_db = item

    patient_updated_info = patient.model_dump(exclude_unset=True) #exclude_unset=true means it ignores empty fields
    for key, value in patient_updated_info.items():
        targeted_patient_in_db[key] = value

    # creating a new patient pydantic obj
    patient_pydantic_obj = Patient(**targeted_patient_in_db)
    # pydantic obj to dict
    updated_patien_info = patient_pydantic_obj.model_dump()

    #updating in db
    for item in data:
        if item['id'] == patient_id:
            for key, value in updated_patien_info.items():
                item[key] = value 
    #saving data 
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': 'patient updated successfully'})

# Creating a delete route
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    #loading data
    data = load_data()

    # checking if the data is available or not
    id_exists = any(item.get('id') == patient_id for item in data)
    if not id_exists:
        raise HTTPException(status_code=400, detail='Patient not found')

    # deleting that existing patient
    updated_data = [item for item in data if item.get('id') != patient_id]
    
    #putting back the new list to the file
    with open("patient.json", 'w') as f:
        json.dump(updated_data, f)
    # for item in data:
    #     if item['id'] == patient_id:
    #         print(item)
    #         del item
    #saving the data
    # save_data(data)

    return JSONResponse(status_code=201, content={"message": "patient deleted successfully"})