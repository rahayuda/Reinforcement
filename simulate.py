import requests
import time

for i in range(200):
    page = f"page_{i % 10}"  # 10 halaman yang diakses berulang
    r = requests.get(f"http://localhost:5000/page/{page}")
    print(f"[{i}] {r.json()}")
    time.sleep(0.05)  # sedikit delay biar stabil
