import os
import sys
import io
import datetime
import requests
from google import genai
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Garante que o console imprima emojis/unicode sem crash
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# =====================================================================
# 1. CARREGAMENTO DOS COFRES E VARIÁVEIS DE AMBIENTE
# =====================================================================
load_dotenv()
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
SCOPES_FOTOS = ['https://www.googleapis.com/auth/photoslibrary.readonly', 'https://www.googleapis.com/auth/photoslibrary.appendonly'] # Permissão total para criar álbuns
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
INBOX_FOLDER_ID = os.getenv("INBOX_FOLDER_ID")
ARCHIVE_FOLDER_ID = os.getenv("ARCHIVE_FOLDER_ID")

# Configura o Cérebro do Gemini (Novo SDK Oficial)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# =====================================================================
# 2. SISTEMA DE AUTENTICAÇÃO BLINDADO
# =====================================================================
def autenticar_api(nome_servico, versao, scopes, nome_token):
    """Fábrica de credenciais: Gerencia Drive e Fotos independentemente."""
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_token = os.path.join(pasta_atual, nome_token)
    
    caminho_cred = os.path.join(pasta_atual, 'credentials_arquivista.json')
    if not os.path.exists(caminho_cred):
        caminho_cred = os.path.join(pasta_atual, 'credentials_arquivista.json.json')

    creds = None
    if os.path.exists(caminho_token):
        creds = Credentials.from_authorized_user_file(caminho_token, scopes)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(f"[*] Solicitando permissao de acesso para: {nome_servico.upper()}...")
            flow = InstalledAppFlow.from_client_secrets_file(caminho_cred, scopes)
            creds = flow.run_local_server(port=0)
        with open(caminho_token, 'w') as token:
            token.write(creds.to_json())
            
    # O Fotos precisa do static_discovery=False
    static_disc = False if nome_servico == 'photoslibrary' else True
    return build(nome_servico, versao, credentials=creds, static_discovery=static_disc)


# =====================================================================
# 3. MÓDULOS DE ROTEAMENTO E INTELIGÊNCIA ARTIFICIAL
# =====================================================================
def extrair_local_com_ia(nome_arquivo):
    """Extrai uma palavra-chave de local do nome original via IA textual (Flash)."""
    prompt = f"""
    Extraia APENAS o nome do condomínio ou local deste arquivo: '{nome_arquivo}'.
    Se não houver, responda APENAS: 'VistoriaGeral'. Use CamelCase impecável e sem acentos.
    """
    try:
        res = gemini_client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        local = res.text.strip().replace(" ", "").replace("'", "").replace('"', "")
        return local if local else "VistoriaGeral"
    except:
        return "VistoriaGeral"

def analisar_midia_com_visao_computacional(dados_bytes, mime_type="image/jpeg") -> str:
    """
    O Olho do Arquiteto: Inspeciona a imagem/video em memória RAM e categoriza.
    """
    prompt_visao = """Você é o Diretor de Organização da DL Soluções Condominiais (especialista em redes, CFTV, elétrica e energia solar). Analise esta imagem/vídeo e responda APENAS com o nome de uma destas categorias:

SERVICO_DL: Quadros elétricos, cabeamento, câmeras, painéis solares, bombas, ferramentas, plantas ou manutenção.

PESSOAL: Lazer, família, cachorros, carros de passeio, casa.

ADMINISTRATIVO: Notas fiscais, recibos, planilhas, telas de sistemas.

LIXO_DIGITAL: Memes, prints irrelevantes, fotos borradas.

Caso a mídia não carregue ou o arquivo não seja compatível, retorne ERRO_LEITURA."""

    try:
        imagem_part = genai.types.Part.from_bytes(data=dados_bytes, mime_type=mime_type)
        resposta = gemini_client.models.generate_content(
            model='gemini-2.0-flash', # O modelo 2.0 tem visão imbatível
            contents=[imagem_part, prompt_visao]
        )
        resp_texto = resposta.text.strip().upper()
        
        # Validação do contrato da API
        categorias_validas = ["SERVICO_DL", "PESSOAL", "ADMINISTRATIVO", "LIXO_DIGITAL", "ERRO_LEITURA"]
        for cat in categorias_validas:
            if cat in resp_texto:
                return cat
        return "ERRO_LEITURA"
        
    except Exception as e:
        print(f"   [!] Erro de Visao Computacional (Falha no motor Gemini): {e}")
        return "ERRO_LEITURA"

_pasta_cache = {}

def obter_ou_criar_pasta(service_drive, nome_pasta, parent_id):
    """Cria ou recupera gaveta no Drive."""
    cache_key = f"{parent_id}_{nome_pasta}"
    if cache_key in _pasta_cache:
        return _pasta_cache[cache_key]

    query = f"name='{nome_pasta}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    resultados = service_drive.files().list(q=query, fields="files(id, name)").execute().get('files', [])
    if resultados:
        _pasta_cache[cache_key] = resultados[0]['id']
        return resultados[0]['id']
    else:
        metadata = {'name': nome_pasta, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
        pasta = service_drive.files().create(body=metadata, fields='id').execute()
        _pasta_cache[cache_key] = pasta.get('id')
        return pasta.get('id')

def obter_ou_criar_album_fotos(service_fotos, titulo_album):
    """Cria ou recupera Álbum Corporativo no Google Fotos."""
    try:
        # Busca álbuns da conta logada
        resposta = service_fotos.albums().list(pageSize=50).execute()
        albuns = resposta.get('albums', [])
        for alb in albuns:
            if alb.get('title') == titulo_album:
                return alb['id']
                
        # Se não achou, cria
        print(f"   [*] Criando o novo album '{titulo_album}' no Google Fotos...")
        novo_album = service_fotos.albums().create(body={'album': {'title': titulo_album}}).execute()
        return novo_album.get('id')
    except Exception as e:
        print(f"   [!] Erro ao operar albuns de foto: {e}")
        return None

# =====================================================================
# 4. ORQUESTRAÇÃO PRINCIPAL (O MOTOR DO AGENTE SIMULTÂNEO)
# =====================================================================
def orquestrar_limpeza_corporativa():
    if not INBOX_FOLDER_ID or not ARCHIVE_FOLDER_ID:
        print("❌ ERRO: Faltam 'INBOX_FOLDER_ID' ou 'ARCHIVE_FOLDER_ID' no .env!")
        return

    # START DOS SERVIÇOS
    service_drive = autenticar_api('drive', 'v3', SCOPES_DRIVE, 'token_arquivista.json')

    data_atual = datetime.datetime.now()
    ano_str, mes_str = data_atual.strftime("%Y"), data_atual.strftime("%m")

    # ==========================================================
    # CÉLULA 1: ESCANEAMENTO DO GOOGLE DRIVE
    # ==========================================================
    print("\n[*] INICIANDO VARREDURA: GOOGLE DRIVE (Raiz Geral) ...")
    # Agora procura na raiz do Drive inteiro em vez de apenas na Inbox
    query = f"'root' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
    arquivos_drive = service_drive.files().list(q=query, fields="files(id, name, mimeType, createdTime)").execute().get('files', [])

    if not arquivos_drive:
        print("   [OK] Gaveta de entrada impecavel. Nenhum lixo solto.")
    else:
        for idx, arq in enumerate(arquivos_drive):
            nome_original = arq['name']
            mime = arq.get('mimeType', '')
            print(f"\n[*] Processando [{idx+1}/{len(arquivos_drive)}]: {nome_original}")
            
            # Padroniza a data
            data_iso = arq.get('createdTime', '')
            dia_str = datetime.datetime.fromisoformat(data_iso.replace('Z', '+00:00')).strftime("%d") if data_iso else data_atual.strftime("%d")
            
            # Análise Visual com Gemini 
            classificacao = "SERVICO_DL" # Fallback (default) se não for mídia suportada
            if mime.startswith('image/'):
                print("   -> Fazendo download em memoria do Google Drive para Analise da Visao...")
                try:
                    request_dw = service_drive.files().get_media(fileId=arq['id'])
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request_dw)
                    while not downloader.next_chunk()[1]: pass
                    classificacao = analisar_midia_com_visao_computacional(fh.getvalue(), mime)
                    print(f"   [DECISAO IA]: -> {classificacao}")
                except Exception as e:
                    print(f"   [!] Falha na leitura visual: {e}")
            else:
                print("   [!] Arquivo de texto/pdf ou video gigante. Rotulado com fallback padrao.")

            if classificacao == "LIXO_DIGITAL":
                print("   [X] Detectado lixo digital. Este script apenas ignora. Ignorando...")
                continue # Pula arquivos classificados como lixo

            # Renomear e Rotear (Pasta Raiz Arquivo -> Categoria -> Ano -> Mês)
            pasta_categoria = obter_ou_criar_pasta(service_drive, classificacao, ARCHIVE_FOLDER_ID)
            pasta_ano = obter_ou_criar_pasta(service_drive, ano_str, pasta_categoria)
            pasta_mes = obter_ou_criar_pasta(service_drive, mes_str, pasta_ano)
            
            local_ia = extrair_local_com_ia(nome_original)
            extensao = os.path.splitext(nome_original)[1]
            novo_nome = f"DL_{classificacao}_{local_ia}_{dia_str}{mes_str}{ano_str}{extensao}"
            
            service_drive.files().update(
                fileId=arq['id'], addParents=pasta_mes, removeParents='root',
                body={'name': novo_nome}, fields='id, name').execute()
            print(f"   [OK] Movido e Renomeado para: {novo_nome} (Dentro de {classificacao}/{ano_str}/{mes_str})")
            
            # Rate limit protection (Gemini Free Tier: 15 RPM)
            print("   [zZz] Aguardando 8 segundos para evitar limite de requisições da IA...")
            import time
            time.sleep(8)

    # ==========================================================
    # CONCLUSÃO
    # A API oficial do Google Fotos desativou a capacidade de leitura
    # global para apps de terceiros (o escopo foi permanentemente removido
    # pelas políticas de privacidade). Portanto, toda a automação de 
    # mídia pessoal deve passar primeiro pelo Google Drive (InBox).
    # ==========================================================


if __name__ == "__main__":
    print("===============================================================")
    print("[*] ARQUITETURA DE AGENTE ZELADOR OMNICHANNEL (VISION) INICIADA")
    print("===============================================================")
    orquestrar_limpeza_corporativa()
