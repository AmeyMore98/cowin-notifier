from fastapi import status

def test_ping(test_app):
    response = test_app.get("/ping")
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data.get("detail") == "pong"
