import os
import jwt
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from antigravity.routes import aninha
from antigravity.routes import marketing

# Carrega variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

app = FastAPI(
    title="Antigravity IA Engine - DL Nexus",
    description="Motor de Inteligência Artificial Especializada B2B",
    version="2.0.0"
)

# 1. SEGURANÇA: Configuração rigorosa de CORS
ALLOWED_ORIGINS = [
    "https://nexus.dlsolucoescondominiais.com.br",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-DL-API-KEY"],
)

# 2. SEGURANÇA: Validação de Tokens JWT Supabase (Fail-Closed)
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

async def verify_supabase_jwt(request: Request):
    """
    Dependência FastAPI que intercepta o header 'Authorization'
    e valida a assinatura usando o JWT Secret do Supabase.
    SEMPRE bloqueia se a chave não estiver configurada no servidor.
    """
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Configuração de segurança crítica ausente no servidor (SUPABASE_JWT_SECRET)."
        )

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autorização ausente ou formato inválido.")

    token = auth_header.split(" ")[1]

    try:
        # Supabase usa HS256
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token JWT expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token JWT inválido ou adulterado.")

# Anexando as rotas da Aninha protegidas
app.include_router(aninha.router, dependencies=[Depends(verify_supabase_jwt)])
app.include_router(marketing.router, dependencies=[Depends(verify_supabase_jwt)])

@app.get("/health")
def health_check():
    return {"status": "online", "motor": "Antigravity", "versao": "2.0"}
