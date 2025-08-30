from pydantic import BaseModel, EmailStr, model_validator
from typing import Dict, List

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('Patient older than 60 should have an emergency contact')
        return model
    
def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.contact)
    print('inserted')

patient_info = {
    'name': 'rakib',
    'email': 'rakib@gmail.com',
    'age': 65,
    'weight': 65,
    'married': True,
    'allergies': ['dust'],
    'contact': {'phone': '0167889', 'location': 'Tangail', 'emergency':'123456789'}
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)
    