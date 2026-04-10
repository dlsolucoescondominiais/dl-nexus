import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/nexus", tags=["PRICING", "BOM"])

class MaterialItem(BaseModel):
    nome: str
    quantidade: int

class ProposalRequest(BaseModel):
    cliente_id: str
    tipo_servico: str
    materiais: List[MaterialItem]

@router.post("/generate-bom")
async def generate_smart_bom(request: ProposalRequest):
    """
    Scrapes/Fetches updated prices for materials and generates a Bill of Materials (BOM).
    Also attaches relevant datasheets from the Drive.
    """
    try:
        # Mock logic for Smart Pricing
        print(f"[*] Gerando BOM Inteligente para cliente {request.cliente_id} (Serviço: {request.tipo_servico})")

        bom_items = []
        total_custo = 0.0

        for mat in request.materiais:
            # Mocking distributor prices (e.g., SD Maracanã)
            preco_unitario = 0.0
            link_datasheet = ""

            nome_lower = mat.nome.lower()
            if "cobre" in nome_lower:
                preco_unitario = 45.50
                link_datasheet = "https://drive.google.com/file/d/mock_cobre_datasheet/view"
            elif "disjuntor" in nome_lower:
                preco_unitario = 22.90
                link_datasheet = "https://drive.google.com/file/d/mock_disjuntor_weg/view"
            elif "galvanizado" in nome_lower:
                preco_unitario = 35.00
                link_datasheet = "https://drive.google.com/file/d/mock_eletroduto_datasheet/view"
            else:
                preco_unitario = 15.00

            subtotal = preco_unitario * mat.quantidade
            total_custo += subtotal

            bom_items.append({
                "material": mat.nome,
                "quantidade": mat.quantidade,
                "preco_unitario_atualizado": preco_unitario,
                "subtotal": subtotal,
                "distribuidor_sugerido": "SD Maracanã",
                "datasheet_link": link_datasheet
            })

        return {
            "status": "success",
            "orcamento_id": str(uuid.uuid4())[:8],
            "bom_items": bom_items,
            "custo_total_estimado": total_custo,
            "margem_sugerida": total_custo * 1.4, # 40% margin
            "message": "BOM gerada com sucesso e datasheets anexados."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
