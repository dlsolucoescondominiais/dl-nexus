import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
ARCHIVE_FOLDER_ID = os.getenv("ARCHIVE_FOLDER_ID")
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']

def autenticar_drive():
    creds = Credentials.from_authorized_user_file('token_arquivista.json', SCOPES_DRIVE)
    return build('drive', 'v3', credentials=creds)

def main():
    service = autenticar_drive()
    # Encontrar pasta ERRO_LEITURA
    query = f"name='ERRO_LEITURA' and '{ARCHIVE_FOLDER_ID}' in parents and trashed=false"
    resultados = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])
    if not resultados:
        print("Nenhuma pasta ERRO_LEITURA encontrada.")
        return
        
    erro_pasta_id = resultados[0]['id']
    query_2026 = f"name='2026' and '{erro_pasta_id}' in parents and trashed=false"
    ano_folders = service.files().list(q=query_2026, fields="files(id, name)").execute().get('files', [])
    if not ano_folders: return
    
    query_mes = f"'{ano_folders[0]['id']}' in parents and trashed=false"
    mes_folders = service.files().list(q=query_mes, fields="files(id, name)").execute().get('files', [])
    
    if mes_folders:
        # Optimization: Fetch all files across all month folders in a single API call
        # avoiding an N+1 query problem where we'd list files for each month individually.
        parent_queries = [f"'{mf['id']}' in parents" for mf in mes_folders]
        query_files = f"({' or '.join(parent_queries)}) and trashed=false"

        # Include 'parents' in fields to know which folder the file came from
        arquivos = service.files().list(q=query_files, fields="files(id, name, parents)").execute().get('files', [])

        mf_ids = {mf['id'] for mf in mes_folders}
        for a in arquivos:
            print(f"Voltando para root: {a['name']}")
            parents_to_remove = [p for p in a.get('parents', []) if p in mf_ids]
            if parents_to_remove:
                service.files().update(fileId=a['id'], addParents='root', removeParents=','.join(parents_to_remove)).execute()

if __name__ == '__main__':
    main()
