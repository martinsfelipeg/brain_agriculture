from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from brain_agriculture.database import get_session
from brain_agriculture.models import Farmer
from brain_agriculture.schemas import (
    FarmerSchema,
    FarmerList,
    FilterPage,
    Message,
)

router = APIRouter(prefix='/farmers', tags=['farmers'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=FarmerSchema)
def create_farmer(farmer: FarmerSchema, session: Session):
    db_farmer = session.scalar(
        select(Farmer).where(Farmer.ndoc == farmer.ndoc)
    )

    if db_farmer:
        if db_farmer.ndoc == farmer.ndoc:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='CNPJ or CPF already exists',
            )

    db_farmer = Farmer(
        ndoc=farmer.ndoc,
        name=farmer.name,
        farm_name=farmer.farm_name,
        city=farmer.city,
        state=farmer.state,
        total_area=farmer.total_area,
        arable_area=farmer.arable_area,
        vegetation_area=farmer.vegetation_area,
        planted_crops=farmer.planted_crops,
    )

    session.add(db_farmer)
    session.commit()
    session.refresh(db_farmer)

    return db_farmer


@router.get('/', response_model=FarmerList)
def read_farmers(
    session: Session, filter_farmers: Annotated[FilterPage, Query()]
):
    farmers = session.scalars(
        select(Farmer)
        .offset(filter_farmers.offset)
        .limit(filter_farmers.limit)
    ).all()

    return {'farmers': farmers}


@router.put('/{ndoc}', response_model=FarmerSchema)
def update_farmer(ndoc: str, farmer: FarmerSchema, session: Session):
    db_farmer = session.scalar(select(Farmer).where(Farmer.ndoc == ndoc))
    if not db_farmer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Farmer not found',
        )

    db_farmer.name = farmer.name
    db_farmer.farm_name = farmer.farm_name
    db_farmer.city = farmer.city
    db_farmer.state = farmer.state
    db_farmer.total_area = farmer.total_area
    db_farmer.arable_area = farmer.arable_area
    db_farmer.vegetation_area = farmer.vegetation_area
    db_farmer.planted_crops = farmer.planted_crops

    session.commit()
    session.refresh(db_farmer)

    return db_farmer


@router.delete('/{ndoc}', response_model=Message)
def delete_farmer(ndoc: str, session: Session):
    db_farmer = session.scalar(select(Farmer).where(Farmer.ndoc == ndoc))

    if not db_farmer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Farmer not found',
        )

    session.delete(db_farmer)
    session.commit()

    return {'message': 'Farmer deleted'}
