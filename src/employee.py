from src.database import get_connection


def add_employee(name, age, department, position, salary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        (name, age, department, position, salary)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, department, position, salary))

    conn.commit()
    conn.close()


def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees ORDER BY id ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def search_employees(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    keyword_like = f"%{keyword}%"

    cursor.execute("""
        SELECT * FROM employees
        WHERE name LIKE ?
           OR department LIKE ?
           OR position LIKE ?
           OR CAST(age AS TEXT) LIKE ?
           OR CAST(salary AS TEXT) LIKE ?
        ORDER BY id ASC
    """, (keyword_like, keyword_like, keyword_like, keyword_like, keyword_like))

    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    conn.commit()
    conn.close()


def update_employee(emp_id, name, age, department, position, salary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET name=?, age=?, department=?, position=?, salary=?
        WHERE id=?
    """, (name, age, department, position, salary, emp_id))

    conn.commit()
    conn.close()