import sqlite3
import bcrypt


def create_connection():
    conn = sqlite3.connect(
        "varg_medi.db",
        check_same_thread=False
    )
    return conn


conn = create_connection()
cursor = conn.cursor()


def create_users_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()


def hash_password(password):
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    )

    return hashed_password.decode(
        "utf-8"
    )


def verify_password(
    plain_password,
    hashed_password
):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def register_user(
    full_name,
    email,
    username,
    password
):
    try:
        hashed_password = hash_password(
            password
        )

        cursor.execute("""
        INSERT INTO users
        (
            full_name,
            email,
            username,
            password
        )
        VALUES (?, ?, ?, ?)
        """, (
            full_name,
            email,
            username,
            hashed_password
        ))

        conn.commit()
        return True

    except:
        return False


def login_user(
    username,
    password
):
    cursor.execute("""
    SELECT * FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user:
        stored_password = user[4]

        if verify_password(
            password,
            stored_password
        ):
            return user

    return None