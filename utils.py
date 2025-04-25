from db_config import get_conn

def get_total_size(db_name):
    conn = get_conn(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(size) FROM data_storage")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0
