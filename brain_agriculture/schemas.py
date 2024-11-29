from typing import List

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    constr,
    model_validator,
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
    planted_crops: str

    @model_validator(mode='after')
    def validate_areas(cls, model):
        if model.arable_area + model.vegetation_area > model.total_area:
            raise ValueError(
                'The sum of agricultural and vegetation areas cannot exceed the total area of the farm.'
            )
        return model


class FarmerList(BaseModel):
    farmers: list[FarmerSchema]


class TotalFarmsCount(BaseModel):
    total_farms: int


class TotalFarmsArea(BaseModel):
    total_area: float


class PieChartData(BaseModel):
    label: str
    value: float


class PieChart(BaseModel):
    data: List[PieChartData]
