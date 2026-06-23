import os
import psycopg2

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
SQL_FILE = r"d:\AntiGravity\projeto_01\backend\supabase\MIGRATIONS_DL_NEXUS_V8_ANINHA_MEMORIA.sql"

db_host = ""
db_password = ""
project_id = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("SUPABASE_DB_HOST="):
            db_host = line.split("=", 1)[1].strip()
        elif line.startswith("SUPABASE_DB_PASSWORD="):
            db_password = line.split("=", 1)[1].strip()
        elif line.startswith("SUPABASE_PROJECT_ID="):
            project_id = line.split("=", 1)[1].strip()

# User for Supabase direct connection is 'postgres'
db_user = "postgres"
db_name = "postgres"
db_port = 5432

print(f"[*] Connecting directly to Postgres at {db_host}:{db_port}...")
try:
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("[+] Connected to database.")
    
    # 1. Drop existing legacy tables
    print("[*] Dropping legacy tables...")
    drop_query = """
    DROP TABLE IF EXISTS mensagens_processadas_aninha CASCADE;
    DROP TABLE IF EXISTS eventos_aninha CASCADE;
    DROP TABLE IF EXISTS logs_aninha_erros CASCADE;
    DROP TABLE IF EXISTS conversas_aninha CASCADE;
    """
    cursor.execute(drop_query)
    print("[+] Legacy tables dropped successfully.")
    
    # 2. Read and run the V8 migration script
    print(f"[*] Reading SQL migration from {SQL_FILE}...")
    with open(SQL_FILE, 'r', encoding='utf-8') as sf:
        sql_query = sf.read()
        
    print("[*] Executing V8 migration queries...")
    cursor.execute(sql_query)
    print("[+] Migration executed successfully! All tables recreated with the correct schema.")
    
    cursor.close()
    conn.close()
    print("[+] Connection closed.")
except Exception as e:
    print(f"[-] Postgres migration error: {e}")
    exit(1)
