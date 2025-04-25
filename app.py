from flask import Flask, jsonify
import mysql.connector
from db_config import get_conn
from utils import get_total_size
from rl_agent import get_db_choice_and_learn
import pickle
import os
import json
from datetime import datetime

app = Flask(__name__)

def log_request(page, used_db, total_A, total_B):
    # Pastikan konversi Decimal ke float
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "page": page,
        "used_db": used_db,
        "db_A_total_size": float(total_A),
        "db_B_total_size": float(total_B)
    }

    if os.path.exists("storage_log.json"):
        with open("storage_log.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open("storage_log.json", "w") as f:
        json.dump(data, f, indent=2)

@app.route("/page/<page_name>", methods=["GET"])
def view_page(page_name):
    CURRENT_DB = get_db_choice_and_learn()
    print(f"[INFO] Page '{page_name}' diakses, digunakan DB: {CURRENT_DB}")

    if CURRENT_DB == "FULL":
        return jsonify({
            "page": page_name,
            "message": "Semua DB sudah penuh. Data tidak dapat disimpan.",
            "used_db": CURRENT_DB
        }), 400

    try:
        conn = get_conn(CURRENT_DB)
        cursor = conn.cursor()

        cursor.execute("SELECT view FROM data_storage WHERE page = %s", (page_name,))
        row = cursor.fetchone()

        if row:
            view = row[0] + 1
            size = view * 1
            cursor.execute("UPDATE data_storage SET view=%s, size=%s WHERE page=%s", (view, size, page_name))
        else:
            cursor.execute("INSERT INTO data_storage (page, view, size) VALUES (%s, %s, %s)", (page_name, 1, 1))

        conn.commit()
        conn.close()

        total_A = get_total_size("db_A")
        total_B = get_total_size("db_B")

        # Logging untuk evaluasi
        log_request(page_name, CURRENT_DB, total_A, total_B)

        return jsonify({
            "page": page_name,
            "used_db": CURRENT_DB,
            "db_A_total_size": total_A,
            "db_B_total_size": total_B
        })

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/status", methods=["GET"])
def status():
    total_A = get_total_size("db_A")
    total_B = get_total_size("db_B")
    return jsonify({
        "db_A_total_size": total_A,
        "db_B_total_size": total_B
    })

@app.route("/q-table", methods=["GET"])
def q_table():
    try:
        if not os.path.exists("q_table.pkl"):
            return jsonify({"message": "Q-table belum dibuat"}), 404

        with open("q_table.pkl", "rb") as f:
            q_table_data = pickle.load(f)
        return jsonify(q_table_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
