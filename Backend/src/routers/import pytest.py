import pytest
from unittest.mock import patch
from Backend.app import app

# filepath: Backend/src/routers/test_performance_metrics_routes.py


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch('src.handlers.controllers.performance_metrics_controller.get_deliveries_per_driver')
def test_get_deliveries_per_driver(mock_get_deliveries_per_driver, client):
    mock_get_deliveries_per_driver.return_value = ('{"data": "mocked response"}', 200)
    response = client.get('/performance/deliveries-per-driver')
    assert response.status_code == 200
    assert response.json == {"data": "mocked response"}

@patch('src.handlers.controllers.performance_metrics_controller.get_average_delivery_time')
def test_get_average_delivery_time(mock_get_average_delivery_time, client):
    mock_get_average_delivery_time.return_value = ('{"data": "mocked response"}', 200)
    response = client.get('/performance/average-delivery-time')
    assert response.status_code == 200
    assert response.json == {"data": "mocked response"}

@patch('src.handlers.controllers.performance_metrics_controller.get_order_acceptance_rejection')
def test_get_order_acceptance_rejection(mock_get_order_acceptance_rejection, client):
    mock_get_order_acceptance_rejection.return_value = ('{"data": "mocked response"}', 200)
    response = client.get('/performance/order-acceptance-rejection')
    assert response.status_code == 200
    assert response.json == {"data": "mocked response"}

@patch('src.handlers.controllers.performance_metrics_controller.get_customer_ratings')
def test_get_customer_ratings(mock_get_customer_ratings, client):
    mock_get_customer_ratings.return_value = ('{"data": "mocked response"}', 200)
    response = client.get('/performance/customer-ratings')
    assert response.status_code == 200
    assert response.json == {"data": "mocked response"}