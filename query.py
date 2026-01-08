import sqlite3
import os


def conexao_bd():
    """Cria ou retorna conexão com banco de dados"""
    return sqlite3.connect("banco.db")


def inicializar_banco():
    """Cria a tabela de pings se não existir"""
    conexao = conexao_bd()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid_hardware TEXT NOT NULL,
        data_ping TEXT NOT NULL,
        nome_host TEXT,
        ip_local TEXT,
        ip_publico TEXT,
        ssid TEXT,
        tem_internet INTEGER NOT NULL CHECK (tem_internet IN (0,1)),
        latitude TEXT,
        longitude TEXT
    );
    """)
    
    conexao.commit()
    conexao.close()


def inserir_ping(dados_ping):
    """Insere um novo ping no banco de dados"""
    try:
        conexao = conexao_bd()
        cursor = conexao.cursor()
        
        cursor.execute("""
        INSERT INTO pings (
            uuid_hardware, data_ping, nome_host, ip_local, ip_publico,
            ssid, tem_internet, latitude, longitude
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados_ping["uuid_hardware"],
            dados_ping["data_hora"],
            dados_ping["nome_host"],
            dados_ping["ip_local"],
            dados_ping["ip_publico"],
            dados_ping["ssid"],
            dados_ping["tem_internet"],
            str(dados_ping["latitude"]),
            str(dados_ping["longitude"])
        ))

        conexao.commit()
        conexao.close()
        return True, "Ping inserido com sucesso!"
    except Exception as e:
        return False, f"Erro ao inserir ping: {str(e)}"


def obter_todos_pings():
    """Retorna todos os pings registrados"""
    try:
        conexao = conexao_bd()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM pings ORDER BY id DESC")
        pings = cursor.fetchall()
        
        conexao.close()
        return pings
    except Exception as e:
        print(f"Erro ao obter pings: {str(e)}")
        return []


def obter_pings_por_uuid(uuid_hardware):
    """Retorna todos os pings de um UUID específico"""
    try:
        conexao = conexao_bd()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM pings WHERE uuid_hardware = ? ORDER BY id DESC", (uuid_hardware,))
        pings = cursor.fetchall()
        
        conexao.close()
        return pings
    except Exception as e:
        print(f"Erro ao obter pings por UUID: {str(e)}")
        return []


def limpar_banco():
    """Limpa todos os dados do banco"""
    try:
        conexao = conexao_bd()
        cursor = conexao.cursor()
        
        cursor.execute("DELETE FROM pings")
        
        conexao.commit()
        conexao.close()
        return True, "Banco de dados limpo!"
    except Exception as e:
        return False, f"Erro ao limpar banco: {str(e)}"
