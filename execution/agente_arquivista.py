import os
import sys

# Garante que o console do Windows imprima emojis/unicode sem crash
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI

# 1. CARREGAMENTO DOS COFRES
load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive']
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INBOX_FOLDER_ID = os.getenv("INBOX_FOLDER_ID") 
ARCHIVE_FOLDER_ID = os.getenv("ARCHIVE_FOLDER_ID")

def autenticar_drive():
    """Valida o crachá do Agente para mexer nos ficheiros."""
    creds = None
    if os.path.exists(''):
        creds = Credentials.from_authorized_user_file('token_arquivista.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\Diogo\Documents\Arquivista_DL\credentials_drive.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_arquivista.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def classificar_arquivo_com_ia(nome_arquivo, tipo_arquivo):
    """O Cérebro do Agente: Lê o nome do ficheiro e escolhe a gaveta certa."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
    Você é o Arquivista-Chefe da DL Soluções Condominiais.
    A sua função é ler o nome de um arquivo recém-chegado e decidir em qual pasta ele deve ser guardado.
    
    Arquivo a ser analisado: {nome_arquivo}
    Formato do arquivo: {tipo_arquivo}
    
    Exemplos de gavetas corporativas: Contratos, Notas Fiscais, Projetos CFTV, Relatórios Solares, Fotos de Vistorias, Documentos Sindicos, Manuais Técnicos, Outros.
    
    REGRA INEGOCIÁVEL: Responda APENAS com o nome da pasta ideal. Nada mais. Sem aspas, sem pontos finais e sem explicações.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # Motor de Alta Precisão
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# Cache em memória para evitar N+1 queries na API do Google Drive
_folder_cache = {}

def obter_ou_criar_pasta(service, nome_pasta):
    """A Mão do Agente: Cria a gaveta caso ela ainda não exista."""
    if nome_pasta in _folder_cache:
        return _folder_cache[nome_pasta]

    query = f"name='{nome_pasta}' and mimeType='application/vnd.google-apps.folder' and '{ARCHIVE_FOLDER_ID}' in parents and trashed=false"
    resultados = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])
    
    if resultados:
        _folder_cache[nome_pasta] = resultados[0]['id']
        return _folder_cache[nome_pasta]
    else:
        # Cria a pasta nova dentro do Gabinete
        metadata = {
            'name': nome_pasta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [ARCHIVE_FOLDER_ID]
        }
        pasta = service.files().create(body=metadata, fields='id').execute()
        print(f"📂 Nova Gaveta Criada automaticamente: {nome_pasta}")
        _folder_cache[nome_pasta] = pasta.get('id')
        return _folder_cache[nome_pasta]

def rodar_triagem_corporativa():
    if not INBOX_FOLDER_ID or not ARCHIVE_FOLDER_ID:
        print("❌ ERRO: Faltam os IDs das pastas (Caixa de Entrada / Gabinete) no arquivo .env!")
        return

    service = autenticar_drive()
    print("🔍 Escaneando a Caixa de Entrada da DL Soluções...")
    
    # 1. Lista todos os ficheiros atirados na Caixa de Entrada
    query = f"'{INBOX_FOLDER_ID}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
    arquivos = service.files().list(q=query, fields="files(id, name, mimeType)").execute().get('files', [])
    
    if not arquivos:
        print("✅ Caixa de entrada impecável! Nenhum documento para arquivar agora.")
        return
        
    for arq in arquivos:
        nome = arq['name']
        tipo = arq['mimeType']
        print(f"\n📄 Analisando documento: {nome}...")
        
        # 2. A Inteligência Artificial decide o destino
        nome_pasta_destino = classificar_arquivo_com_ia(nome, tipo)
        print(f"🧠 IA categorizou como: [{nome_pasta_destino}]")
        
        # 3. Verifica ou cria a pasta no Gabinete
        id_pasta_destino = obter_ou_criar_pasta(service, nome_pasta_destino)
        
        # 4. Move o documento da Caixa de Entrada para a Gaveta Certa
        service.files().update(
            fileId=arq['id'],
            addParents=id_pasta_destino,
            removeParents=INBOX_FOLDER_ID,
            fields='id, parents'
        ).execute()
        print(f"✅ Documento guardado e organizado com sucesso!")

if __name__ == "__main__":
    print("==================================================")
    print("🤖 AGENTE ARQUIVISTA DL SOLUÇÕES INICIADO")
    print("==================================================")
    rodar_triagem_corporativa()