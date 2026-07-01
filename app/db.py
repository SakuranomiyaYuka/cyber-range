import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')

    users = [
        ('admin',   'admin_secure@2024',  'admin@range.local',  'admin'),
        ('alice',   'alice123',           'alice@test.com',     'user'),
        ('bob',     'b0b_p@ss',           'bob@test.com',       'user'),
        ('charlie', 'ch4rl!3',            'charlie@test.com',   'user'),
        ('dave',    'dave_secret!',       'dave@test.com',      'user'),
        ('eve',     'eve@test',           'eve@range.local',    'user'),
    ]
    c.executemany(
        'INSERT INTO users (username, password, email, role) VALUES (?,?,?,?)',
        users
    )

    c.execute('DROP TABLE IF EXISTS comments')
    c.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    sample_comments = [
        ('admin', 'Welcome to the XSS training range!'),
        ('alice', 'This is a sample comment.'),
        ('bob',   'Security is not a product, but a process.'),
    ]
    c.executemany(
        'INSERT INTO comments (name, content) VALUES (?,?)',
        sample_comments
    )

    c.execute('DROP TABLE IF EXISTS secrets')
    c.execute('''
        CREATE TABLE secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value TEXT
        )
    ''')
    c.execute(
        "INSERT INTO secrets (name, value) VALUES (?,?)",
        ('flag_sqli_level5', 'flag{f1rst_0rd3r_upd4t3_1nj3ct10n}')
    )
    c.execute(
        "INSERT INTO secrets (name, value) VALUES (?,?)",
        ('flag_xss_level5', 'flag{st0r3d_xss_w1th_csp_byp4ss}')
    )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('Database initialized.')
