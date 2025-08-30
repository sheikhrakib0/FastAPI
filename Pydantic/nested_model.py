from pydantic import BaseModel


class Address(BaseModel):

    house: str
    city: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {
    'house': '4b, D block',
    'city': 'faridpur',
    'pin':'3456'
}
address1 = Address(**address_dict)
patient_dict = {
    'name': 'nitish',
    'gender': 'male',
    'age': 40,
    'address': address1
}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address.city)