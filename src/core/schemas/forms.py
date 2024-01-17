import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, validator


class Date(BaseModel):
    date: str

    @validator("date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY or YYYY-MM-DD.")


class Email(BaseModel):
    email: EmailStr


class Phone(BaseModel):
    phone: str

    @validator("phone")
    def validate_phone(cls, value):
        if re.match(r"^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$", value):
            return value
        else:
            raise ValueError("Invalid phone format. Use +7 XXX XXX XX XX")


class MatchingTemplate(BaseModel):
    template_name: str
