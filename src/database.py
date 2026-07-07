import sqlite3
import os


DB_PATH = os.path.join("database", "employee.db")


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_database():
    """初始化数据库"""

    os.makedirs("database", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        department TEXT,
        position TEXT,
        salary REAL
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("数据库初始化完成！")