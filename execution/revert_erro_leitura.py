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
    
    def batch_callback(request_id, response, exception):
        if exception:
            print(f"Erro ao mover arquivo: {exception}")

    for mf in mes_folders:
        query_files = f"'{mf['id']}' in parents and trashed=false"
        arquivos = service.files().list(q=query_files, fields="files(id, name)").execute().get('files', [])

        batch = service.new_batch_http_request(callback=batch_callback)
        count = 0
        for a in arquivos:
            print(f"Preparando para voltar para root: {a['name']}")
            req = service.files().update(fileId=a['id'], addParents='root', removeParents=mf['id'])
            batch.add(req)
            count += 1
            if count >= 100:
                batch.execute()
                batch = service.new_batch_http_request(callback=batch_callback)
                count = 0

        if count > 0:
            batch.execute()

if __name__ == '__main__':
    main()
