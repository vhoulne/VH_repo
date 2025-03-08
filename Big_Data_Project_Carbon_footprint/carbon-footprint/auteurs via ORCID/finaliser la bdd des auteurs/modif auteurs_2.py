import sqlite3

# Chemins vers les bases de données existante et nouvelle
existing_db_path = 'auteurs_2.db'
new_db_path = 'auteurs_f.db'

# Connexion à la base de données existante
conn_existing = sqlite3.connect(existing_db_path)
cursor_existing = conn_existing.cursor()

# Connexion à la nouvelle base de données
conn_new = sqlite3.connect(new_db_path)
cursor_new = conn_new.cursor()

# Création de la table auteurs dans la nouvelle base de données
cursor_new.execute('''
    CREATE TABLE auteurs (
        author_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        author_name TEXT NOT NULL,
        author_location TEXT,
        nom2 TEXT
    )
''')

# Sélection de toutes les lignes de la table auteurs dans la base de données existante
cursor_existing.execute('SELECT author_ID, author_name, author_location, nom2 FROM auteurs')
rows = cursor_existing.fetchall()

# Insertion des lignes dans la nouvelle base de données
for row in rows:
    author_ID, author_name, author_location, nom2 = row
    
    # Insérer la ligne originale
    cursor_new.execute('''
        INSERT INTO auteurs (author_name, author_location, nom2)
        VALUES (?, ?, ?)
    ''', (author_name, author_location, nom2))
    
    # Si nom2 n'est pas null, insérer une nouvelle ligne
    if nom2:
        cursor_new.execute('''
            INSERT INTO auteurs (author_name, author_location, nom2)
            VALUES (?, ?, ?)
        ''', (nom2, author_location, None))

# Sauvegarder les changements et fermer les connexions
conn_new.commit()
conn_existing.close()
conn_new.close()

print("La nouvelle base de données a été créée avec succès.")
