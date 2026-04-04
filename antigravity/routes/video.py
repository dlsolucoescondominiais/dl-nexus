import os
import requests
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from antigravity.agents.agente_video import KlingVideoAgent

router = APIRouter(prefix="/api/video", tags=["VÍDEO", "MARKETING", "KLING"])
agente = KlingVideoAgent()

WEBHOOK_RETORNO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")

class VideoRequest(BaseModel):
    tema: str
    plataforma: str = "Tiktok"

async def workflow_completo_background(tema: str):
    """
    Simula o workflow longo: Gerar roteiro, mandar pra Kling, esperar e notificar.
    """
    try:
        # Pede pra Kling
        prompt = agente.gerar_prompt_otimizado(tema)
        task_id = await agente.solicitar_geracao_kling(prompt)

        # Simula o polling rápido
        video_url = await agente.verificar_status_kling(task_id)

        # Avisa o N8N que tá pronto
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        payload = {
            "message": "Diogo, o novo Reel/TikTok está pronto!",
            "video_url": video_url,
            "tema": tema
        }
        requests.post(WEBHOOK_RETORNO_N8N, json=payload, headers=headers, timeout=10)

    except Exception as e:
        print(f"[!] Falha crítica no Agente de Vídeo: {e}")

@router.post("/gerar")
async def gerar_video_curto(request: VideoRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint para gerar vídeos curtos via Inteligência Artificial (Kling AI).
    Otimizado para rodar em background tasks sem derrubar a API.
    """
    try:
        # 1. Dispara o processamento pesado pro Background
        bg_tasks.add_task(workflow_completo_background, request.tema)

        return {
            "status": "success",
            "message": "Solicitação recebida. O Agente de Vídeo iniciou a produção na Kling AI.",
            "tema": request.tema
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
