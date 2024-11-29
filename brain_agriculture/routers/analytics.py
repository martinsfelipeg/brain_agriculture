from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from brain_agriculture.database import get_session
from brain_agriculture.models import Farmer
from brain_agriculture.schemas import (
    TotalFarmsCount,
    TotalFarmsArea,
    PieChart,
    PieChartData,
)

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/total-farms-count', response_model=TotalFarmsCount)
def get_total_farms_count(session: Session = Depends(get_session)):
    total_farms_count = session.scalar(func.count(Farmer.ndoc))
    return TotalFarmsCount(total_farms=total_farms_count)


@router.get('/total-farms-area', response_model=TotalFarmsArea)
def get_total_farms_area(session: Session = Depends(get_session)):
    total_area = session.scalar(func.sum(Farmer.total_area)) or 0
    return TotalFarmsArea(total_area=total_area)


@router.get('/state-distribution', response_model=PieChart)
def get_state_distribution(session: Session = Depends(get_session)):
    state_data = (
        session.query(Farmer.state, func.count(Farmer.ndoc))
        .group_by(Farmer.state)
        .all()
    )
    distribution = [
        PieChartData(label=state, value=count) for state, count in state_data
    ]
    return PieChart(data=distribution)


@router.get('/crop-distribution', response_model=PieChart)
def get_crop_distribution(session: Session = Depends(get_session)):
    crop_data = {}
    farmers = session.query(Farmer.planted_crops).all()
    for farmer in farmers:
        if farmer.planted_crops:
            crops = farmer.planted_crops.split(', ')
            for crop in crops:
                crop_data[crop] = crop_data.get(crop, 0) + 1
    distribution = [
        PieChartData(label=crop, value=count)
        for crop, count in crop_data.items()
    ]
    return PieChart(data=distribution)


@router.get('/area-usage-distribution', response_model=PieChart)
def read_area_usage_distribution(session: Session = Depends(get_session)):
    total_arable_area = session.scalar(func.sum(Farmer.arable_area)) or 0
    total_vegetation_area = (
        session.scalar(func.sum(Farmer.vegetation_area)) or 0
    )
    distribution = [
        PieChartData(label='Arable Area', value=total_arable_area),
        PieChartData(label='Vegetation Area', value=total_vegetation_area),
    ]
    return PieChart(data=distribution)
