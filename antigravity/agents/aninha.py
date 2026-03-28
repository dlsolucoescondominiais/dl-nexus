import re
import json
import os
import logging
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

class TipoServico(Enum):
    """Tipos de serviço baseados no portfólio DL Soluções"""
    ELETRICA = "eletrica"
    SOLAR = "solar"
    SEGURANCA = "seguranca"
    INCENDIO = "incendio"
    MOBILIDADE = "mobilidade"
    AUTOMACAO = "automacao"
    CONSULTORIA = "consultoria"

class Porte(Enum):
    """Porte do condomínio baseado no número de unidades"""
    PEQUENO = "PEQUENO"
    MEDIO = "MEDIO"
    GRANDE = "GRANDE"
    COMPLEXO = "COMPLEXO"

class AninhaAgent:
    """
    Agente ANINHA: Triagem Inteligente de Leads (Versão 2.0 - IA + Regras Híbridas)
    """
    
    def __init__(self):
        self.palavras_chave_bloqueio_b2b = [
            r"\bcasa\b", r"\bresidência\b", r"\bapartamento\b", r"\bmeu apartamento\b",
            r"\bminha casa\b", r"\bresidencial\b", r"\buso pessoal\b", r"\bparticular\b"
        ]
        
        self.palavras_chave_bloqueio_escopo = [
            r"\bbomba\b", r"\bhidrante\b", r"\bsprinkler\b", r"\bprumada\b", r"\bhidráulica\b",
            r"\bencanamento\b", r"\bmanutenção mecânica\b", r"\breparos gerais\b", r"\bcanaleta de plástico\b"
        ]

        if GEMINI_API_KEY:
            self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.gemini_client = None
            logger.warning("GEMINI_API_KEY não configurada. A triagem IA vai falhar.")
    
    def match_keywords(self, text: str, patterns: List[str]) -> bool:
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return True
        return False

    def validar_b2b(self, mensagem: str, tipo_imovel: Optional[str] = None) -> bool:
        """ Valida B2B mas PERMITE residencial se for MOBILIDADE (Carregador VE) """
        msg_lower = mensagem.lower()
        tipo_lower = (tipo_imovel or "").lower()
        
        is_mobilidade = "carregador" in msg_lower or "veículo elétrico" in msg_lower or "cve" in msg_lower
        
        has_block = self.match_keywords(msg_lower, self.palavras_chave_bloqueio_b2b) or \
                    self.match_keywords(tipo_lower, self.palavras_chave_bloqueio_b2b)
        
        if has_block:
            if is_mobilidade:
                return True # Exceção garantida!
            return False
        
        return True
    
    def validar_escopo(self, mensagem: str) -> tuple[bool, str]:
        """ Retorna (Valido, Motivo) """
        msg_lower = mensagem.lower()
        
        if re.search(r"canaleta.*pl[áa]stico", msg_lower):
            return False, "Fora de escopo/Qualidade: Não utilizamos canaletas de plástico."

        if self.match_keywords(msg_lower, self.palavras_chave_bloqueio_escopo):
            return False, "Fora de escopo: Foco exclusivo em elétrica e automação dry (sem hidráulica direta)."
        
        return True, "Escopo inicial aceito."

    def classificar_ia(self, mensagem: str) -> Dict[str, Any]:
        """ Classifica usando Gemini com Structured JSON Output """

        if not self.gemini_client:
            # Fallback seguro para não estourar se faltar API key (ex: testes)
            return {
                "urgencia": "media",
                "categoria_servico": "eletrica"
            }

        system_prompt = """Você é a Aninha, agente de IA de triagem da DL Soluções Condominiais.
Sua tarefa é analisar a mensagem do síndico e OBRIGATORIAMENTE devolver um JSON rigoroso com duas chaves:
1. "urgencia": Deve ser UM DOS SEGUINTES valores: "baixa", "media", "alta", "critica".
   (Ex: quadro desarmado/fogo/choque = critica; orçamento solar = media; reforma de PC = alta).
2. "categoria_servico": Deve ser UM DOS SEGUINTES valores: "eletrica", "solar", "incendio", "seguranca", "mobilidade", "automacao".

NÃO retorne formatação markdown, retorne APENAS o JSON.
"""

        try:
            response = self.gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=f"{system_prompt}\n\nMensagem do Síndico: '{mensagem}'",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            # Como usamos response_mime_type, o texto será um JSON string.
            resultado_json = json.loads(response.text)

            # Validação defensiva do payload gerado pela IA
            urgencia = resultado_json.get("urgencia", "media")
            if urgencia not in ["baixa", "media", "alta", "critica"]:
                urgencia = "media"
                
            categoria = resultado_json.get("categoria_servico", "eletrica")
            if categoria not in ["eletrica", "solar", "incendio", "seguranca", "mobilidade", "automacao"]:
                categoria = "eletrica"

            return {
                "urgencia": urgencia,
                "categoria_servico": categoria
            }
        except Exception as e:
            logger.error(f"Erro na IA Gemini Aninha: {e}")
            # Fallback seguro
            return {
                "urgencia": "media",
                "categoria_servico": "eletrica"
            }
    
    def calcular_porte(self, num_unidades: Optional[int]) -> Porte:
        if not num_unidades: return Porte.PEQUENO
        if num_unidades <= 30: return Porte.PEQUENO
        if num_unidades <= 100: return Porte.MEDIO
        if num_unidades <= 300: return Porte.GRANDE
        return Porte.COMPLEXO
    
    def calcular_valor_mensal(self, porte: Porte, categoria: str) -> float:
        valores_base = { Porte.PEQUENO: 400.0, Porte.MEDIO: 600.0, Porte.GRANDE: 1000.0, Porte.COMPLEXO: 1500.0 }
        multiplicadores = {
            "eletrica": 1.0, "solar": 1.5, "seguranca": 1.3,
            "incendio": 1.1, "mobilidade": 1.2, "automacao": 1.2,
            "consultoria": 0.8
        }
        return valores_base.get(porte, 400.0) * multiplicadores.get(categoria, 1.0)
    
    def definir_sla(self, urgencia: str) -> str:
        """ Nova regra dinâmica de SLAs baseada na Urgência Versão 2.0 """
        if urgencia == "critica":
            return "SLA 4 horas"
        elif urgencia == "alta":
            return "SLA 8 horas"
        elif urgencia == "media":
            return "SLA 24 horas"
        return "SLA 48 horas"
    
    def fazer_triagem(self, lead_data: Dict) -> Dict:
        resultado = {
            "status": "bloqueado",
            "motivo": None,
            "lead_id": lead_data.get("lead_id"),
            "timestamp": datetime.now().isoformat()
        }
        
        mensagem = lead_data.get("mensagem_original", "")

        if not self.validar_b2b(mensagem, lead_data.get("tipo_imovel")):
            resultado["motivo"] = "Lead residencial. Foco exclusivo em Condomínios e B2B Escolar."
            return resultado
        
        escopo_ok, escopo_motivo = self.validar_escopo(mensagem)
        if not escopo_ok:
            resultado["motivo"] = escopo_motivo
            return resultado
        
        # Etapa IA: Classificação Inteligente v2.0
        classificacao = self.classificar_ia(mensagem)
        urgencia = classificacao["urgencia"]
        categoria_servico = classificacao["categoria_servico"]

        porte = self.calcular_porte(lead_data.get("num_unidades"))
        valor_mensal = self.calcular_valor_mensal(porte, categoria_servico)
        sla = self.definir_sla(urgencia)
        
        resultado.update({
            "status": "triado",
            "categoria_servico": categoria_servico,
            "urgencia": urgencia,
            "porte": porte.value,
            "valor_mensal_estimado": valor_mensal,
            "sla_estimado": sla,
            "proxima_acao_obrigatoria": "Agendar Avaliação Técnica", # Diretriz: Nunca 'Visita Técnica'
            "nome_condominio": lead_data.get("nome_condominio"),
            "telefone": lead_data.get("telefone"),
            "email": lead_data.get("email"),
            "origem": lead_data.get("origem")
        })
        return resultado
