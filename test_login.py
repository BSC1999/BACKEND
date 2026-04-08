import requests

session = requests.Session()
response = session.get("http://127.0.0.1:8000/admin/login/")

# Extract CSRF token
csrf_token = session.cookies.get("csrftoken")
if not csrf_token:
    print("Could not retrieve CSRF token.")
    exit(1)

login_data = {
    "username": "boss",
    "password": "boss123",
    "csrfmiddlewaretoken": csrf_token,
    "next": "/admin/"
}

login_response = session.post("http://127.0.0.1:8000/admin/login/", data=login_data, headers={"Referer": "http://127.0.0.1:8000/admin/login/"})

if login_response.url == "http://127.0.0.1:8000/admin/" or "Log in | Django site admin" not in login_response.text:
    print("SUCCESS: Logged in successfully via HTTP.")
else:
    print("FAILED: Login failed via HTTP.")
    print("Response text contains 'correct username and password': ", "Please enter the correct username and password" in login_response.text)
