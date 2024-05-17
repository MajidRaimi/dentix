from pydantic import BaseModel, validator
import re

class LoginDTO(BaseModel):
    email: str
    password: str


class SignupDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    confirm_password: str

