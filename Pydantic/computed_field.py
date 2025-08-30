from pydantic import BaseModel, EmailStr, computed_field
from typing import Dict, List

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    height: float
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @computed_field
    @property
    def bmi(self) ->  float:
        bmi = round(self.weight/(self.height **2), 2)
        return bmi
    
def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.contact)
    print(patient.bmi)
    print('inserted')

patient_info = {
    'name': 'rakib',
    'email': 'rakib@gmail.com',
    'age': 65,
    'height':1.7,
    'weight': 65,
    'married': True,
    'allergies': ['dust'],
    'contact': {'phone': '0167889', 'location': 'Tangail', 'emergency':'123456789'}
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)
    