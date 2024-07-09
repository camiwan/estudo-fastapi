from pydantic import BaseModel
from typing import List, Optional


class infoProfessionalSchema(BaseModel):
    training: str
    institution: str
    company_work: str

class InfoProfessionalCreate(infoProfessionalSchema):
    pass

class InfoProfessionalUpdate(infoProfessionalSchema):
    pass 

class InfoProfessional(infoProfessionalSchema):
    id: int

    class Config:
        orm_mode: True

class ClientSchema(BaseModel):
    name: str
    age: str

class ClientCreate(ClientSchema):
    info_professional: List[InfoProfessionalCreate] = []

class ClienteUpdate(ClientSchema):
    info_professional: Optional[List[InfoProfessionalUpdate]] = []

class Client(ClientSchema):
    id: int
    info_professional: List[InfoProfessional] = []    

    class Config:
        orm_mode = True


