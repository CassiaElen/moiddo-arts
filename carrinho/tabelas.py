import sqlite3

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    artista TEXT NOT NULL,
    preco REAL NOT NULL
)
''')

cursor.executemany('''
INSERT INTO produtos (nome, artista, preco) VALUES (?, ?, ?)
''', [
    ('Pôr do Sol em Florença', 'Giovanni Bellini', 1200.00),
    ('Luz e Sombra', 'Helena Duarte', 800.50),
    ('Rostos do Vento', 'Carlos Menezes', 960.99)
])

conn.commit()
conn.close()
