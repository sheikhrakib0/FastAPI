from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

    name: Annotated[str, Field(max_length=100, description='Give me your name', examples=['Rakib'])]
    email: EmailStr
    linkedIn: AnyUrl
    age: int = Field(gt=0)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['ific.com', 'mbstu.ac.bd']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domain:
            raise ValueError('not a valie Domain')
        return value
    
    @field_validator('name')
    @classmethod
    def name_transformation(cls, value):
        return value.upper()
    


def insert_patient_info(patient:Patient):

    print(patient.name)
    print(patient.email)
    print(patient.allergies)
    print('inserted')

patient_info = {
    'name': 'md. rakib',
    'email': 'abc@ific.com',
    'linkedIn':'https://logeachi.com',
    'age': 45,
    'weight': 65,
    'contact':{'location':'tangail','phone': '0158738759'}
}

patient1 = Patient(**patient_info)

insert_patient_info(patient1)