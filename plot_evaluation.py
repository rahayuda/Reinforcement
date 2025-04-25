import json
import matplotlib.pyplot as plt

with open("storage_log.json") as f:
    data = json.load(f)

episodes = list(range(len(data)))
db_A_sizes = [entry["db_A_total_size"] for entry in data]
db_B_sizes = [entry["db_B_total_size"] for entry in data]
difference = [abs(a - b) for a, b in zip(db_A_sizes, db_B_sizes)]
used_dbs = [entry["used_db"] for entry in data]

# Selisih kapasitas A dan B
plt.figure(figsize=(12, 6))
plt.plot(episodes, difference, label="|DB_A - DB_B|")
plt.xlabel("Episode")
plt.ylabel("Perbedaan Kapasitas (GB)")
plt.title("Perbedaan Kapasitas DB_A dan DB_B per Episode")
plt.legend()
plt.grid()
plt.show()

# Total data tersimpan sebelum semua DB penuh
full_index = next((i for i, d in enumerate(used_dbs) if d == "FULL"), len(used_dbs))
print(f"📦 Total data berhasil disimpan sebelum semua DB penuh: {full_index} entries")

# Rasio penggunaan
from collections import Counter
usage_count = Counter(used_dbs)
print("📊 Penggunaan DB:")
for db, count in usage_count.items():
    print(f" - {db}: {count} kali")
