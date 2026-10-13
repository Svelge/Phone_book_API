import requests

from config import TEST_USER_PASSWORD, TEST_USER_EMAIL, API_BASE_URL

payload = {
    "username": TEST_USER_EMAIL,
    "password": TEST_USER_PASSWORD
}

response = requests.post(f"{API_BASE_URL}v1/user/login/usernamepassword",json=payload)
print("status_code: ", response.status_code)
print("Content-Type header: ", response.headers["content-type"])
print("response.text is a raw string, length :", len(response.text))
body = response.json()
print("response.json() is a Python dict, keys: ", list(body.keys()))

