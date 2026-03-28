from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from core.llm_router import MultiLLMRouter
from agents.aninha import AninhaAgent

app = FastAPI(title="DL Nexus API - Antigravity")

# CORS setup
origins = [
    "http://localhost:5173",
    "https://nexus.dlsolucoescondominiais.com.br",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = MultiLLMRouter()
aninha = AninhaAgent(router)

@app.get("/")
def read_root():
    return {"status": "online", "system": "DL Nexus Antigravity API"}

@app.post("/webhook/n8n/aninha")
async def webhook_aninha(request: Request):
    """
    Endpoint chamado pelo n8n quando uma mensagem chega no WhatsApp.
    O n8n já salvou no Supabase, aqui só processamos a IA e respondemos.
    """
    try:
        data = await request.json()
        telefone = data.get("telefone")
        mensagem = data.get("mensagem_original")

        if not telefone or not mensagem:
            raise HTTPException(status_code=400, detail="Missing telefone or mensagem")

        # Roda a inteligência da Aninha (que usa o router com fallback)
        resposta_ia = aninha.processar_mensagem(telefone, mensagem)

        # A Aninha já deve ter atualizado o Supabase e aqui retornamos a resposta
        # para o n8n pegar e engatilhar na API do Meta.
        return {"status": "success", "resposta": resposta_ia}

    except Exception as e:
        print(f"Erro no webhook: {e}")
        # Retorna o fallback hardcoded configurado no router
        fallback_msg = "Peço desculpas, mas nossos sistemas de atendimento estão passando por uma instabilidade momentânea. Por favor, deixe seu nome e a descrição do seu problema, e um técnico humano retornará em breve."
        return {"status": "error", "resposta": fallback_msg, "detail": str(e)}
