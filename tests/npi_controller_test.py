from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from database.connection import get_db
from main import app
from models.calculation import Calculation

client = TestClient(app)

mock_db = MagicMock()


def override_get_db():
    yield mock_db


app.dependency_overrides[get_db] = override_get_db


def test_calculate_addition():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "3 4 +"})

    assert response.status_code == 200
    assert response.json() == {'operation': '3 4 +', 'result': 7.0}

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    added_calculation = mock_db.add.call_args[0][0]
    assert isinstance(added_calculation, Calculation)
    assert added_calculation.operation == "3 4 +"
    assert added_calculation.result == 7.0


def test_calculate_subtraction():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "10 3 -"})

    assert response.status_code == 200
    assert response.json() == {'operation': '10 3 -', 'result': 7.0}

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    added_calculation = mock_db.add.call_args[0][0]
    assert isinstance(added_calculation, Calculation)
    assert added_calculation.operation == "10 3 -"
    assert added_calculation.result == 7.0


def test_calculate_multiplication():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "5 6 *"})

    assert response.status_code == 200
    assert response.json() == {'operation': '5 6 *', 'result': 30.0}

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    added_calculation = mock_db.add.call_args[0][0]
    assert isinstance(added_calculation, Calculation)
    assert added_calculation.operation == "5 6 *"
    assert added_calculation.result == 30.0


def test_calculate_division():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "8 2 /"})

    assert response.status_code == 200
    assert response.json() == {'operation': '8 2 /', 'result': 4.0}

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    added_calculation = mock_db.add.call_args[0][0]
    assert isinstance(added_calculation, Calculation)
    assert added_calculation.operation == "8 2 /"
    assert added_calculation.result == 4.0


def test_calculate_division_by_zero():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "4 0 /"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Error: division by zero"}


def test_calculate_invalid_expression():
    mock_db.reset_mock()
    response = client.post("/api/calculate/", json={"operation": "3 +"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Error: invalid RPN expression"}
