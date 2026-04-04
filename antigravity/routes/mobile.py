import os
import uuid
from datetime import datetime
import requests
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google import genai

router = APIRouter(prefix="/api/nexus", tags=["MOBILE", "INGESTÃO"])

# Variáveis do Drive e Notificação
WEBHOOK_NOTIFICACAO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials_drive.json")
INBOX_FOLDER_ID = os.getenv("INBOX_FOLDER_ID")

# Integração Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nejdtvkpiclagsnfljsz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_JWT_SECRET"))

# Integração Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
         raise HTTPException(status_code=500, detail="Credenciais do Google Drive não encontradas no servidor.")
    creds = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def disparar_notificacao_background(mensagem: str):
    try:
        headers = {"Content-Type": "application/json", "X-DL-API-KEY": API_KEY_N8N}
        requests.post(WEBHOOK_NOTIFICACAO_N8N, json={"message": mensagem}, headers=headers, timeout=10)
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

def analisar_tipo_documento(nome_arquivo: str) -> str:
    """Usa IA para classificar o documento em: Nota Fiscal, Contrato ou Manual"""
    if not GEMINI_API_KEY:
        return "01_Administrativo"

    prompt = f"O arquivo se chama '{nome_arquivo}'. Ele se parece mais com uma 'Nota Fiscal', 'Contrato' ou 'Manual'? Responda apenas com uma dessas 3 opções, ou 'Outro'."
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        res = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        resposta = res.text.strip().lower()

        if "nota" in resposta or "fiscal" in resposta or "contrato" in resposta:
            return "01_Administrativo"
        elif "manual" in resposta:
            return "03_Engenharia"
        else:
            return "01_Administrativo" # Fallback corporativo
    except:
        return "01_Administrativo"

def registrar_no_supabase(nome_salvo: str, link_drive: str):
    """Registra o arquivo processado na tabela documentacao_tecnica"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return

    url = f"{SUPABASE_URL}/rest/v1/documentacao_tecnica"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    payload = {
        "nome_arquivo": nome_salvo,
        "link_drive": link_drive,
        "data_upload": datetime.now().isoformat()
    }
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao registrar no Supabase: {e}")

@router.post("/organizar-mobile")
async def organizar_mobile(bg_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not INBOX_FOLDER_ID:
        raise HTTPException(status_code=500, detail="INBOX_FOLDER_ID não configurado.")

    content = await file.read()
    mime_type = file.content_type
    extensao = os.path.splitext(file.filename)[1].lower()

    is_image = mime_type.startswith('image/')
    is_doc = mime_type.startswith('application/') or mime_type.startswith('text/')
    is_music = mime_type.startswith('audio/')

    data_atual = datetime.now().strftime("%Y%m%d")
    file_id = str(uuid.uuid4())[:8]

    if is_image:
        # Padroniza como JPG e usa terminologia "Avaliação Técnica" ao invés de visita técnica
        novo_nome = f"dl_avaliacao_tecnica_{data_atual}_{file_id}.jpg"
        pasta_destino_nome = "02_Avaliacoes_Tecnicas_Campo"
    elif is_doc:
        novo_nome = f"dl_doc_administrativo_{file.filename}"
        pasta_destino_nome = analisar_tipo_documento(file.filename)
    elif is_music:
        novo_nome = file.filename
        pasta_destino_nome = "07_Midia_e_Pessoal/Musicas" # Pode precisar lidar com subpastas
    else:
        novo_nome = file.filename
        pasta_destino_nome = "03_Outros"

    try:
        service = get_drive_service()

        # Tratamento especial para pasta aninhada (Musicas)
        if "/" in pasta_destino_nome:
            partes = pasta_destino_nome.split("/")
            parent = INBOX_FOLDER_ID
            for parte in partes:
                parent = obter_ou_criar_pasta(service, parte, parent)
            pasta_destino_id = parent
        else:
            pasta_destino_id = obter_ou_criar_pasta(service, pasta_destino_nome, INBOX_FOLDER_ID)

        # Upload
        file_metadata = {
            'name': novo_nome,
            'parents': [pasta_destino_id]
        }

        from io import BytesIO
        media = MediaIoBaseUpload(BytesIO(content), mimetype=mime_type, resumable=True)

        arquivo_drive = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        link_drive = arquivo_drive.get('webViewLink', '')

        # Registra no banco e notifica
        bg_tasks.add_task(registrar_no_supabase, novo_nome, link_drive)

        mensagem = "Diogo, infraestrutura/arquivo processado com sucesso!"
        bg_tasks.add_task(disparar_notificacao_background, mensagem)

        return {"status": "success", "file_id": arquivo_drive.get('id'), "nome_salvo": novo_nome}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
