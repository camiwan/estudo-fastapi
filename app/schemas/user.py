from pydantic import BaseModel

class PassWordChange(BaseModel):
    old_password: str
    new_password: str

class UserSchema(BaseModel):
    email: str

class UserCreate(UserSchema):
    
    password: str

class User(UserSchema):
    id: int
   

    class Config:
        # orm_mode= True
        from_attributes = True