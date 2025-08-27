from fastapi import FastAPI
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
def view_patient(patient_id:str):
    #first loading all data 
    data = load_data()

    for patient in data:
        if patient_id in patient['id']:
            return patient
    return {'error': 'This patient information is not available to this database'}
