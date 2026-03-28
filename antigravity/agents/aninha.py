import re
import json
import os
import openai
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

class TipoServico(Enum):
    """Tipos de serviço baseados no portfólio DL Soluções"""
    ELETRICO = "eletrica"
    SOLAR = "solar"
    SEGURANCA = "seguranca"
    INCENDIO = "incendio"
    MOBILIDADE = "mobilidade"
    AUTOMACAO = "automacao"
    CONSULTORIA = "consultoria"
    INDEFINIDA = "indefinida"

class Urgencia(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class Porte(Enum):
    PEQUENO = "PEQUENO"
    MEDIO = "MEDIO"
    GRANDE = "GRANDE"
    COMPLEXO = "COMPLEXO"

class AninhaAgent:
    """
    Agente ANINHA V2: Triagem Integrada usando Inteligência Artificial (OpenAI)
    e Respostas em Formato JSON Rigoroso
    """
    def __init__(self):
        # API Key via variável de ambiente 
        api_key = os.getenv("OPENAI_API_KEY") 
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        self.system_prompt = """
        Você é a ANINHA - Arquiteta Escolar e Síndicos (Engenharia B2B).
        A sua função é conversar com o cliente, entender a dor dele e classificar a demanda para nossa equipe de engenharia.
        
        Sempre que processar um novo lead, você é OBRIGADA a devolver UM ÚNICO OUTPUT no formato JSON rigoroso.
        Não adicione saudações, não use markdown (```json), imprima puramente o objeto JSON.
        
        O JSON deve seguir esta estrutura exata:
        {
            "urgencia": "<valor>",
            "categoria_servico": "<valor>",
            "parecer": "<Breve resumo de até 2 linhas da dor do condomínio/escola>"
        }
        
        REGRAS DE VALORES:
        - urgencia: Deve ser EXATAMENTE "baixa", "media", "alta", ou "critica". (ex: quadro elétrico desarmando ou risco térmico = "critica"; orçamento de energia solar projeto verde = "media").
        - categoria_servico: Deve ser EXATAMENTE um destes: "eletrica", "solar", "incendio", "seguranca", "mobilidade", "automacao" ou "indefinida".
        - Regra: Sem canaletas plásticas. Terminologia: Avaliação Técnica. 
        """

    def calcular_porte(self, num_unidades: Optional[int]) -> Porte:
        if not num_unidades: return Porte.PEQUENO
        if num_unidades <= 30: return Porte.PEQUENO
        if num_unidades <= 100: return Porte.MEDIO
        if num_unidades <= 300: return Porte.GRANDE
        return Porte.COMPLEXO

    def analisar_mensagem_ia(self, mensagem_cliente: str) -> Dict[str, Any]:
        """A IA lê a mensagem e gera o Json rigoroso"""
        if not self.client:
            return {
                "urgencia": "alta", 
                "categoria_servico": "eletrica", 
                "parecer": "Falha - OPENAI_API_KEY não configurada."
            }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Mensagem do lead B2B: {mensagem_cliente}"}
                ],
                temperature=0.2
            )
            
            payload = json.loads(response.choices[0].message.content)
            
            valid_urgencia = ["baixa", "media", "alta", "critica"]
            valid_categoria = ["eletrica", "solar", "incendio", "seguranca", "mobilidade", "automacao"]
            
            if payload.get("urgencia") not in valid_urgencia:
                payload["urgencia"] = "media"
            if payload.get("categoria_servico") not in valid_categoria:
                payload["categoria_servico"] = "indefinida"
                
            return payload

        except Exception as e:
            return {
                "urgencia": "alta", 
                "categoria_servico": "indefinida", 
                "parecer": f"Falha na IA: {str(e)}"
            }

    def fazer_triagem(self, lead_data: Dict) -> Dict:
        """
        Substitui a lógica de Regras Antiga pela lógica de IA da V2.0
        """
        mensagem = lead_data.get("mensagem_original", "")
        # Processa com IA
        resultado_ia = self.analisar_mensagem_ia(mensagem)
        
        porte = self.calcular_porte(lead_data.get("num_unidades"))
        
        # Consolida payload para Supabase / Roteadores
        payload_final = {
            "status": "triado",
            "motivo": resultado_ia.get("parecer"),
            "lead_id": lead_data.get("lead_id"),
            "timestamp": datetime.now().isoformat(),
            "urgencia": resultado_ia.get("urgencia"),
            "categoria_servico": resultado_ia.get("categoria_servico"),
            "porte": porte.value,
            "proxima_acao_obrigatoria": "Agendar Avaliação Técnica",
            "nome_condominio": lead_data.get("nome_condominio"),
            "telefone": lead_data.get("telefone"),
            "email": lead_data.get("email"),
            "origem": lead_data.get("origem")
        }
        
        return payload_final
