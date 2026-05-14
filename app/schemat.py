from pydantic import BaseModel
class Userlogin(BaseModel):
    email:str
    password:str
class UserRegister(BaseModel):
    name:str
    email:str
    password:str
