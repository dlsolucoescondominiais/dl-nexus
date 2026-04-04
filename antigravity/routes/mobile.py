import os
import uuid
from datetime import datetime
import requests
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

router = APIRouter(prefix="/api/nexus", tags=["MOBILE", "INGESTÃO"])

# Webhook do N8N para notificação
WEBHOOK_NOTIFICACAO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials_drive.json")
INBOX_FOLDER_ID = os.getenv("INBOX_FOLDER_ID")

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
         # Tentativa de fallback se as credenciais de service account nao existirem
         raise HTTPException(status_code=500, detail="Credenciais do Google Drive não encontradas no servidor.")

    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def disparar_notificacao_background(mensagem: str):
    try:
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        payload = {"message": mensagem}
        resp = requests.post(WEBHOOK_NOTIFICACAO_N8N, json=payload, headers=headers, timeout=10)
        print(f"Callback n8n disparado com sucesso: HTTP {resp.status_code}")
    except Exception as e:
        print(f"Falha ao notificar o webhook do n8n: {e}")

def obter_ou_criar_pasta(service, nome_pasta, parent_id):
    query = f"name='{nome_pasta}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    resultados = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])
    if resultados:
        return resultados[0]['id']
    else:
        metadata = {'name': nome_pasta, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
        pasta = service.files().create(body=metadata, fields='id').execute()
        return pasta.get('id')

@router.post("/organizar-mobile")
async def organizar_mobile(bg_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not INBOX_FOLDER_ID:
        raise HTTPException(status_code=500, detail="INBOX_FOLDER_ID não configurado.")

    content = await file.read()
    mime_type = file.content_type
    extensao = os.path.splitext(file.filename)[1].lower()

    # Lógica de processamento
    is_image = mime_type.startswith('image/')
    is_doc = mime_type.startswith('application/') or mime_type.startswith('text/')
    is_music = mime_type.startswith('audio/')

    data_atual = datetime.now().strftime("%Y%m%d")
    file_id = str(uuid.uuid4())[:8]

    if is_image:
        novo_nome = f"dl_avaliacao_tecnica_{data_atual}_{file_id}{extensao}"
        pasta_destino_nome = "02_Avaliacoes_Tecnicas_Campo"
    elif is_doc:
        novo_nome = f"dl_doc_administrativo_{file.filename}"
        pasta_destino_nome = "01_Administrativo_e_Legal"
    else:
        novo_nome = file.filename
        pasta_destino_nome = "03_Outros"

    try:
        service = get_drive_service()

        # Encontra ou cria a pasta de destino dentro do INBOX_FOLDER_ID
        pasta_destino_id = obter_ou_criar_pasta(service, pasta_destino_nome, INBOX_FOLDER_ID)

        # Upload do arquivo
        file_metadata = {
            'name': novo_nome,
            'parents': [pasta_destino_id]
        }

        from io import BytesIO
        media = MediaIoBaseUpload(BytesIO(content), mimetype=mime_type, resumable=True)

        arquivo_drive = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        mensagem = "Diogo, 1 novo arquivo do smartphone foi processado e organizado no Drive!"
        bg_tasks.add_task(disparar_notificacao_background, mensagem)

        return {"status": "success", "file_id": arquivo_drive.get('id'), "nome_salvo": novo_nome}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
