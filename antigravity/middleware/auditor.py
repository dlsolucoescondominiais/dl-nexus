import os
import requests
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

WEBHOOK_ADMIN_N8N = os.getenv("N8N_ADMIN_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/admin-alerts")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")

def notificar_admin_bloqueio(motivo: str, payload_suspeito: str):
    try:
        headers = {"Content-Type": "application/json", "X-DL-API-KEY": API_KEY_N8N}
        payload = {
            "alert": "COMPLIANCE_BLOCK",
            "reason": motivo,
            "details": payload_suspeito
        }
        requests.post(WEBHOOK_ADMIN_N8N, json=payload, headers=headers, timeout=5)
    except:
        pass

class ComplianceAuditorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                body_text = body_bytes.decode('utf-8').lower()

                # Restaurar o body para as rotas poderem ler depois
                async def receive():
                    return {"type": "http.request", "body": body_bytes}
                request._receive = receive

                # RULE 1: BLOCK_PROPOSAL se usar canaleta plástica
                if "canaleta plástica" in body_text or "canaleta plastica" in body_text:
                    notificar_admin_bloqueio("Uso de termo proibido (Canaleta Plástica)", body_text[:200])
                    raise HTTPException(status_code=403, detail="Compliance Error: O uso de 'canaleta plástica' é estritamente proibido pelas normas da empresa. Utilize infraestrutura galvanizada.")

                # RULE 2: Avaliação Técnica
                if "visita técnica" in body_text or "visita tecnica" in body_text:
                     raise HTTPException(status_code=400, detail="Terminologia Incorreta: Use 'Avaliação Técnica' ao invés de 'visita técnica'.")

            except HTTPException as e:
                from fastapi.responses import JSONResponse
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
            except Exception:
                pass

        response = await call_next(request)
        return response
