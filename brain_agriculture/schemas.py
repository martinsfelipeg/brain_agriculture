from typing import List, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    constr,
    field_validator,
)


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FarmerSchema(BaseModel):
    ndoc: str = constr(
        pattern=r'^\d{11}|\d{14}$'
    )  # CPF: 11 digits, CNPJ: 14 digits
    name: str
    farm_name: str
    city: str
    state: str
    total_area: float
    arable_area: float
    vegetation_area: float
    planted_crops: List[
        Literal['Soy', 'Corn', 'Cotton', 'Coffee', 'Sugar Cane']
    ]

    @field_validator('total_area', 'arable_area', 'vegetation_area')
    def validate_areas(cls, value):
        total = value.get('total_area', 0)
        agric = value.get('arable_area', 0)
        veget = value.get('vegetation_area', 0)
        if agric + veget > total:
            raise ValueError(
                'The sum of agricultural and vegetation areas cannot exceed the total area of the farm.'
            )
        return value


class FarmerList(BaseModel):
    farmers: list[FarmerSchema]
