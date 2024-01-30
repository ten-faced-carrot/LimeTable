from core.cryptography import hash_password
import requests
from datetime import date

API_INSTANCE = "http://127.0.0.1:5000"
username = "user"
password = hash_password("123123")
print(password)
r = requests.get(f'{API_INSTANCE}/api/day/000000/{date.today().isoformat()}', headers={'X-User': username, 'X-Access-Hash': password})
print(r.text)