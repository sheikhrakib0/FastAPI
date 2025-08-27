from pydantic import BaseModel
from typing import List, Dict, Optional


def insert_patient_data(name: str, age: int):
    if type(name)== str and type(age)== int:
        if age<0:
            raise ValueError("Age can not be negative")
        else:
            print(name)
            print(age)
            print('Inserted into the dataset')
    else:
        raise TypeError("Incorrect Data Type")
    

person1 = insert_patient_data('Rkb', 30)

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]


def insert_patient_data2(patient: Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('Inserted')

patient_info = {'name': 'Rakib', 'age': 40, 'weight': 60, 'married': False, 'contact_details':{'email':'rakib@gmail.com','phone':'123456'}}

patient1 = Patient(**patient_info)

insert_patient_data2(patient1)