import mysql.connector

def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="portfolio_db"
    )
    return conn


def add_user(username, password, role):

    username = username.strip()
    password = password.strip()

    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (username,password,role) VALUES (%s,%s,%s)"
    values = (username,password,role)

    cursor.execute(query,values)

    conn.commit()
    conn.close()


def login_user(username,password):

    conn = create_connection()
    
    cursor = conn.cursor(buffered=True)

    username = username.strip()
    password = password.strip()

    query = "SELECT * FROM users WHERE TRIM(username)=%s AND TRIM(password)=%s"

    cursor.execute(query,(username,password))

    result = cursor.fetchone()

    conn.close()

    return result