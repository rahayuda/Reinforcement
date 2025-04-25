import pickle
import random
from utils import get_total_size

Q_TABLE_FILE = "q_table.pkl"

# Parameter Q-Learning
alpha = 0.1
gamma = 0.9
epsilon = 0.3  # eksplorasi di awal

# Load Q-Table jika ada
try:
    with open(Q_TABLE_FILE, "rb") as f:
        Q = pickle.load(f)
except FileNotFoundError:
    Q = {}

def state_to_key(size_a, size_b):
    return f"{int(size_a) // 10}-{int(size_b) // 10}"

def choose_action(state_key):
    if random.random() < epsilon or state_key not in Q:
        action = random.choice(["db_A", "db_B"])
        print(f"[ACTION] Eksplorasi: {action} untuk state {state_key}")
        return action
    action = max(Q[state_key], key=Q[state_key].get)
    print(f"[ACTION] Eksploitasi: {action} untuk state {state_key}")
    return action

def reward_function(new_size_a, new_size_b):
    total = new_size_a + new_size_b
    balance = abs(new_size_a - new_size_b)
    penalty = 100 if new_size_a > 100 or new_size_b > 100 else 0
    reward = -(balance + 0.1 * total + penalty)
    print(f"[REWARD] new_size_a={new_size_a}, new_size_b={new_size_b}, reward={reward}")
    return reward

def update_q(state_key, action, reward, next_state_key):
    Q.setdefault(state_key, {"db_A": 0.0, "db_B": 0.0})
    Q.setdefault(next_state_key, {"db_A": 0.0, "db_B": 0.0})

    current_q = Q[state_key][action]
    max_next_q = max(Q[next_state_key].values())
    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q)
    Q[state_key][action] = new_q

    print(f"[Q-UPDATE] {state_key} --{action}--> {next_state_key} | reward: {reward:.2f} | Q: {Q[state_key]}")

    with open(Q_TABLE_FILE, "wb") as f:
        pickle.dump(Q, f)

def get_db_choice_and_learn():
    size_a = float(get_total_size("db_A"))
    size_b = float(get_total_size("db_B"))

    # ✅ Jika kedua DB sudah penuh
    if size_a >= 100 and size_b >= 100:
        print("[INFO] Kedua DB sudah penuh, tidak bisa menyimpan data.")
        return "FULL"

    # ✅ Jika salah satu DB penuh, paksa simpan ke yang lain
    if size_a >= 100:
        print("[INFO] db_A penuh, pakai db_B")
        size_b += 1  # Ubah penambahan dari 10 ke 1
        reward = reward_function(size_a, size_b)
        update_q(state_to_key(size_a, size_b - 1), "db_B", reward, state_to_key(size_a, size_b))
        return "db_B"

    if size_b >= 100:
        print("[INFO] db_B penuh, pakai db_A")
        size_a += 1  # Ubah penambahan dari 10 ke 1
        reward = reward_function(size_a, size_b)
        update_q(state_to_key(size_a - 1, size_b), "db_A", reward, state_to_key(size_a, size_b))
        return "db_A"

    # ✅ Q-Learning decision jika keduanya belum penuh
    state_key = state_to_key(size_a, size_b)
    action = choose_action(state_key)

    # Prediksi ukuran setelah aksi
    new_size_a = size_a + 1 if action == "db_A" else size_a  # Ubah penambahan dari 10 ke 1
    new_size_b = size_b + 1 if action == "db_B" else size_b  # Ubah penambahan dari 10 ke 1

    # Final check (harusnya tidak sampai sini karena sudah dicek di atas, tapi tetap aman)
    if new_size_a > 100 or new_size_b > 100:
        print(f"[INFO] Aksi {action} menyebabkan overload. Tidak diproses.")
        return "FULL"

    next_state_key = state_to_key(new_size_a, new_size_b)
    reward = reward_function(new_size_a, new_size_b)
    update_q(state_key, action, reward, next_state_key)

    return action