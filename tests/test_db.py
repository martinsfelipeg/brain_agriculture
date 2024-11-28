from dataclasses import asdict

from sqlalchemy import select

from brain_agriculture.models import User, Farmer


def test_create_user(session):
    new_user = User(
        username='felipe', password='123456', email='felipe@test.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'felipe'))

    assert asdict(user) == {
        'id': 1,
        'username': 'felipe',
        'password': '123456',
        'email': 'felipe@test.com',
    }


def test_create_farmer(session):
    new_farmer = Farmer(
        ndoc='22244433366',
        name='José da Silva',
        farm_name='Fazenda da Silva',
        city='Sao Paulo',
        state='SP',
        total_area=100,
        arable_area=50,
        vegetation_area=50,
        planted_crops='Soja, Milho',
    )
    session.add(new_farmer)
    session.commit()

    farmer = session.scalar(select(Farmer).where(Farmer.ndoc == '22244433366'))

    assert asdict(farmer) == {
        'ndoc': '22244433366',
        'name': 'José da Silva',
        'farm_name': 'Fazenda da Silva',
        'city': 'Sao Paulo',
        'state': 'SP',
        'total_area': 100.0,
        'arable_area': 50.0,
        'vegetation_area': 50.0,
        'planted_crops': 'Soja, Milho',
    }
