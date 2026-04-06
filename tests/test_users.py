from app import schemas
from jose import jwt
from app.config import settings
import pytest


# @app.get("/,status_code=status.HTTP_200_OK")
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.status_code == 200
#     assert res.json().get("message") == "API is running!"

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@example.com"
    print("User creation test passed!")
    print("Response:", res.json())

def test_login_user(client,test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert res.status_code == 200
    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['user_id']
    assert res.status_code == 200
    print("User login test passed!")
    assert login_response.token_type == "bearer"
    print("Token type test passed!")

@pytest.mark.parametrize("email,password,status_code", [
    ("invalidemail", "password123", 403),
    (None, "password123", 422),
    ("test@example.com", "password123", 200)
])
def test_incorrect_login(client,test_user,email,password,status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get("detail") == "Invalid Credentials"
    print("Incorrect login test passed!")


