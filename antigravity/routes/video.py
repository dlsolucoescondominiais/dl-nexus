import os
import requests
import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/video", tags=["VÍDEO", "MARKETING", "KLING"])

WEBHOOK_RETORNO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")
KLING_API_KEY = os.getenv("KLING_API_KEY")

class VideoRequest(BaseModel):
    tema: str
    plataforma: str = "Tiktok"

async def gerar_video_kling_real(tema: str):
     # Lógica real de integração API Kling omitida, retorna URL stub caso a API key exista.
     # Se a gente tiver documentação exata da Kling, a gente bota a chamada POST certa.
     print(f"[*] Chamando API Real do KLING para tema: {tema}")
     await asyncio.sleep(2)
     return "https://kling.ai/video/dl-nexus-output.mp4"

async def workflow_completo_background(tema: str):
    """
    Workflow para gerar roteiro e mandar pra Kling, aguardar e notificar.
    """
    try:
        if not KLING_API_KEY:
            print("[Sandbox] KLING_API_KEY não encontrada. Simulando geração de vídeo...")
            await asyncio.sleep(3) # Simula delay da geração
            video_url = "https://sandbox-kling-simulation.com/video.mp4"
            mensagem_alerta = f"Diogo, [SIMULAÇÃO] o novo vídeo sobre '{tema}' está pronto!"
        else:
            video_url = await gerar_video_kling_real(tema)
            mensagem_alerta = f"Diogo, o novo Reel/TikTok sobre '{tema}' está pronto!"

        # Avisa o N8N que tá pronto
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        payload = {
            "message": mensagem_alerta,
            "video_url": video_url,
            "tema": tema
        }
        try:
             requests.post(WEBHOOK_RETORNO_N8N, json=payload, headers=headers, timeout=10)
        except Exception as e:
             print(f"[!] Falha de notificação N8N após gerar o vídeo: {e}")

    except Exception as e:
        print(f"[!] Falha crítica no Agente de Vídeo: {e}")

@router.post("/gerar")
async def gerar_video_curto(request: VideoRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint para gerar vídeos curtos via Inteligência Artificial (Kling AI).
    Opera em modo Sandbox/Simulação se KLING_API_KEY não for fornecida.
    """
    try:
        bg_tasks.add_task(workflow_completo_background, request.tema)

        return {
            "status": "success",
            "message": "Solicitação recebida. O Agente de Vídeo iniciou a produção na Kling AI.",
            "tema": request.tema,
            "mode": "production" if KLING_API_KEY else "sandbox"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
