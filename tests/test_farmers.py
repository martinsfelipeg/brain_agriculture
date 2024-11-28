from http import HTTPStatus

from brain_agriculture.schemas import FarmerSchema


def test_create_farmer(client):
    response = client.post(
        '/farmers/',
        json={
            'ndoc': '22244433366',
            'name': 'José da Silva',
            'farm_name': 'Fazenda da Silva',
            'city': 'Sao Paulo',
            'state': 'SP',
            'total_area': 100,
            'arable_area': 50,
            'vegetation_area': 50,
            'planted_crops': 'Soja, Milho',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
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


def test_read_farmers(client):
    response = client.get('/farmers/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'farmers': []}


def test_read_farmers_with_farmers(client, farmer):
    farmer_dict = {
        'ndoc': farmer.ndoc,
        'name': farmer.name,
        'farm_name': farmer.farm_name,
        'city': farmer.city,
        'state': farmer.state,
        'total_area': farmer.total_area,
        'arable_area': farmer.arable_area,
        'vegetation_area': farmer.vegetation_area,
        'planted_crops': farmer.planted_crops,
    }

    farmer_schema = FarmerSchema.model_validate(farmer_dict).model_dump()

    response = client.get('/farmers/')
    assert response.status_code == 200
    assert response.json() == {'farmers': [farmer_schema]}


def test_update_farmer(client, farmer):
    updated_data = {
        'ndoc': '12345678910',
        'name': 'José da Silva',
        'farm_name': 'Fazenda José',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'total_area': 200.0,
        'arable_area': 120.0,
        'vegetation_area': 80.0,
        'planted_crops': 'Cana, Café',
    }

    response = client.put(f'/farmers/{farmer.ndoc}', json=updated_data)
    assert response.status_code == HTTPStatus.OK
    updated_farmer = response.json()

    assert updated_farmer['ndoc'] == updated_data['ndoc']
    assert updated_farmer['name'] == updated_data['name']
    assert updated_farmer['farm_name'] == updated_data['farm_name']
    assert updated_farmer['city'] == updated_data['city']
    assert updated_farmer['state'] == updated_data['state']
    assert updated_farmer['total_area'] == updated_data['total_area']
    assert updated_farmer['arable_area'] == updated_data['arable_area']
    assert updated_farmer['vegetation_area'] == updated_data['vegetation_area']
    assert updated_farmer['planted_crops'] == updated_data['planted_crops']


def test_delete_farmer_success(client, farmer):
    response = client.delete(f'/farmers/{farmer.ndoc}')
    assert response.status_code == HTTPStatus.OK
