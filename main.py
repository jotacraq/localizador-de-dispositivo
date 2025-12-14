import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

cursor.execute("""PRAGMA foreign_keys = ON;""")

cursor.execute("""CREATE TABLE IF NOT EXISTS dispositivos (
        id TEXT PRIMARY KEY,
        nome_host TEXT NOT NULL,
        usuario TEXT NOT NULL,
        criado_em TEXT NOT NULL,
        ultimo_sync_em TEXT,
        ativo INTEGER NOT NULL DEFAULT 1
        );
        """)

cursor.execute("""CREATE TABLE IF NOT EXISTS pings (
        id TEXT PRIMARY KEY,
        dispositivo_id TEXT NOT NULL,
        data_ping TEXT NOT NULL,
        ip_local TEXT,
        ip_publico TEXT,
        tem_internet INTEGER,
        ssid_wifi TEXT,
        latitude REAL,
        longitude REAL,
        sincronizado INTEGER NOT NULL DEFAULT 0,
        sincronizado_em TEXT,
    
        FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
        );
        """)

cursor.execute("""CREATE INDEX IF NOT EXISTS idx_pings_dispositivo_tempo 
                  ON pings(dispositivo_id, data_ping);""")

cursor.execute("""CREATE INDEX IF NOT EXISTS idx_pings_sincronizado 
                  ON pings(sincronizado);""")


conexao.commit()