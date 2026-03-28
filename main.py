import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from antigravity.routes.aninha import router as aninha_router
from antigravity.routes.propostas import router as propostas_router

app = FastAPI(
    title="DL Nexus API",
    description="API do Ecossistema DL Soluções Condominiais - Motor de IA Antigravity",
    version="1.0.0"
)

# Configuração de CORS para permitir que o Frontend (React/Next.js) e o n8n conversem com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, substitua pelo domínio da Vercel e IP do n8n
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando as rotas criadas pelo Antigravity
app.include_router(aninha_router)
app.include_router(propostas_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "DL Nexus - Antigravity Engine",
        "modules_active": ["Aninha Especialista DL", "Jules Auditor de Qualidade"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
