import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('/home/royer/Desktop/movie_note/movies.db')
cursor = conn.cursor()

try:
    # Agregar columna is_favorite si no existe
    cursor.execute("ALTER TABLE movie ADD COLUMN is_favorite BOOLEAN DEFAULT 0")
    conn.commit()
    print("✓ Columna is_favorite agregada exitosamente")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("✓ La columna is_favorite ya existe")
    else:
        print(f"✗ Error: {e}")
finally:
    conn.close()
