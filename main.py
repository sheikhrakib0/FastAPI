from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

# to laod the json file 
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

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