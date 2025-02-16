import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from unittest.mock import patch, Mock
from sqlalchemy.orm import Session

client = TestClient(app)

# Mock data to validate on scraper response (Search filter = Airline: D7, Flight Number: 506, Date: 15-Feb 2025)
MOCK_FLIGHT_DATA = [{
    'flightNo': 'D7 506',
    'flightAirline': 'AirAsia X',
    'flightStatus': 'Arrived',
    'flightStatusDesc': 'Delayed by 20m',
    'departureAirportCode': 'KUL',
    'departureAirportName': 'Kuala Lumpur International Airport',
    'departureCity': 'Kuala Lumpur, MY',
    'departureTerminal': '2',
    'departureGate': 'P10',
    'departureDate': '15-Feb-2025',
    'departureTimeScheduled': '10:00',
    'departureTimeActual': '10:28',
    'departureTimeZone': '+08',
    'arrivalAirportCode': 'ICN',
    'arrivalAirportName': 'Seoul Incheon International Airport',
    'arrivalCity': 'Seoul, KR',
    'arrivalTerminal': '1',
    'arrivalGate': '113',
    'arrivalBaggage': '8',
    'arrivalDate': '15-Feb-2025',
    'arrivalTimeScheduled': '17:30',
    'arrivalTimeActual': '17:50',
    'arrivalTimeZone': 'KST'
}]

@pytest.fixture
def mock_db():
    # Mock database session
    mock_session = Mock(spec=Session)
    
    # Override get_db dependency
    def mock_db_override():
        return mock_session
    app.dependency_overrides[get_db] = mock_db_override
    
    yield mock_session

    app.dependency_overrides.clear()

@pytest.fixture
def mock_scraper():
    with patch('main.scraper.scrapeData') as mock:
        yield mock

# Test get response with correct flight data
def test_get_flight_success(mock_scraper):
    mock_scraper.return_value = MOCK_FLIGHT_DATA
    
    response = client.get("/api/v1/flights?airline_code=D7&airline_no=506&date=2025-02-15")
    
    assert response.status_code == 200
    assert response.json() == MOCK_FLIGHT_DATA

# Test get response with incorrect flight data
def test_get_flight_not_found(mock_scraper):
    mock_scraper.return_value = [{'flightNo': ''}]
    
    response = client.get("/api/v1/flights?airline_code=XX&airline_no=999&date=2025-03-20")
    
    assert response.status_code == 400
    assert "Check typo or format in parameters" in response.json()["detail"]

# Test post response with correct flight data
def test_post_flight_success(mock_scraper, mock_db):
    mock_scraper.return_value = MOCK_FLIGHT_DATA
    
    response = client.post("/api/v1/flights?airline_code=D7&airline_no=506&date=2025-02-15")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"] == MOCK_FLIGHT_DATA
    
    # Verify DB operations were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# Test post response with incorrect flight data
def test_post_flight_invalid_data(mock_scraper, mock_db):
    mock_scraper.return_value = [{'flightNo': ''}]
    
    response = client.post("/api/v1/flights?airline_code=XX&airline_no=999&date=2025-03-20")
    
    assert response.status_code == 400
    assert "Check typo or format in parameters" in response.json()["detail"]
    
    # Verify no DB operations were performed
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called() 