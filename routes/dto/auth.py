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

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('phone_number')
    def phone_number_length(cls, v):
        if not re.match(r'^05\d{8}$', v):
            raise ValueError('Invalid phone number')
        return v

    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 8 characters')
        return v

    @validator('email')
    def email_valid(cls, v):
        if not re.match(r'^\S+@\S+\.\S+$', v):
            raise ValueError('Invalid email address')
        return v
