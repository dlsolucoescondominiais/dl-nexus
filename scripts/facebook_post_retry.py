import time
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env caso existam
load_dotenv()

def post_to_facebook(data):
    max_retries = 3
    retry_delay = 5  # segundos
    
    # Injeta o token oficial da DL Soluções Condominiais, se não foi passado no data
    if 'access_token' not in data:
        token = os.environ.get('META_PAGE_ACCESS_TOKEN_DL')
        if token:
            data['access_token'] = token
    
    # Substitui 'me' pelo ID real da página, caso configurado no .env
    page_id = os.environ.get('META_FACEBOOK_PAGE_ID', 'me')
    endpoint = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                endpoint,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Tentativa {attempt+1} falhou: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

if __name__ == "__main__":
    # Exemplo de uso
    post_data = {"message": "Teste de postagem via script Python com retry"}
    print(f"Iniciando postagem com {post_data}")
    try:
        result = post_to_facebook(post_data)
        print("Sucesso! Resposta da API:", result)
    except Exception as e:
        print("Falha definitiva após todas as tentativas:", e)
