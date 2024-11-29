from http import HTTPStatus


def test_get_total_farms_count(client, farmer):
    response = client.get('/analytics/total-farms-count')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'total_farms': 1}


def test_get_total_farms_area(client, farmer):
    response = client.get('/analytics/total-farms-area')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'total_area': 100.0}


def test_get_state_distribution(client, farmer):
    response = client.get('/analytics/state-distribution')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'data': [{'label': 'SP', 'value': 1}]}


def test_get_crop_distribution(client, farmer):
    response = client.get('/analytics/crop-distribution')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'data': [{'label': 'Soja', 'value': 1}, {'label': 'Milho', 'value': 1}]
    }


def test_read_area_usage_distribution(client, farmer):
    response = client.get('/analytics/area-usage-distribution')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'data': [
            {'label': 'Arable Area', 'value': 50.0},
            {'label': 'Vegetation Area', 'value': 50.0},
        ]
    }
