import re
import json
import os
import openai
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

class Urgencia(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class AninhaAgent:
    """
    Agente ANINHA V3: Triagem Integrada usando Inteligência Artificial (OpenAI)
    Responde com texto natural para o cliente e JSON rigoroso para o sistema.
    """
    def __init__(self):
        # API Key via variável de ambiente 
        api_key = os.getenv("OPENAI_API_KEY") 
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        # Carrega a base comercial
        base_path = os.path.join(os.path.dirname(__file__), '../../docs/BASE_COMERCIAL_ANINHA_DL.md')
        try:
            with open(base_path, 'r', encoding='utf-8') as f:
                self.base_comercial = f.read()
        except FileNotFoundError:
            self.base_comercial = "BASE COMERCIAL NÃO ENCONTRADA."
        
        self.system_prompt = """
Você é a ANINHA - Especialista Comercial e de Triagem Técnica da DL Soluções Condominiais.
Sua função é atender o cliente, entender o problema, conduzir a venda (com preços mínimos),
coletar dados e classificar o lead.

Abaixo está a sua base de conhecimento OBRIGATÓRIA. Siga TODAS as regras descritas nela:
" + self.base_comercial + "

Quando você responder, você DEVE retornar um JSON estrito, sem formatação markdown (sem ```json), com a seguinte estrutura:

{
  "resposta_cliente": "A mensagem natural que será enviada de volta ao cliente. Lembre-se: use 'a partir de', seja comercial, ajuste por região se o bairro for informado, max 3 perguntas.",
  "status_lead": "novo | aguardando_dados | qualificado | orçamento_preliminar | encaminhado_diogo",
  "urgencia": "baixa | media | alta | critica",
  "servico_identificado": "Descrição curta do serviço que o cliente quer, ex: 'Instalação CFTV' ou 'indefinido'",
  "bairro_identificado": "Bairro se o cliente informou, senão null",
  "tipo_cliente": "condominio | escola | administradora | empresa | restaurante | residencial | indefinido",
  "valor_inicial_informado": "Valor informado ao cliente (ex: R$ 350) ou null",
  "dados_faltantes": "Quais dados faltam para o orçamento fechado",
  "resumo_conversa": "Resumo do que foi falado até agora",
  "proxima_acao": "Qual o próximo passo com o lead",
  "precisa_escalar_diogo": true/false (true se atender às regras de escalonamento),
  "resumo_diogo": "Se precisa_escalar_diogo for true, coloque aqui a mensagem formatada para o Diogo conforme a regra de escalonamento. Se false, pode ser null."
}
"""

    def analisar_mensagem_ia(self, mensagem_cliente: str, historico: List[Dict] = None) -> Dict[str, Any]:
        """A IA lê a mensagem e gera o Json rigoroso"""
        if not self.client:
            return {
                "resposta_cliente": "Erro: OPENAI_API_KEY não configurada.",
                "status_lead": "erro",
                "urgencia": "media",
                "servico_identificado": "indefinido",
                "bairro_identificado": None,
                "tipo_cliente": "indefinido",
                "precisa_escalar_diogo": False,
                "resumo_diogo": None
            }

        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        if historico:
            messages.extend(historico)

        messages.append({"role": "user", "content": f"Mensagem do lead: {mensagem_cliente}"})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=messages,
                temperature=0.2
            )
            
            payload = json.loads(response.choices[0].message.content)
            return payload

        except Exception as e:
            return {
                "resposta_cliente": "Desculpe, ocorreu um erro interno ao processar sua mensagem.",
                "status_lead": "erro",
                "urgencia": "media",
                "servico_identificado": "indefinido",
                "bairro_identificado": None,
                "tipo_cliente": "indefinido",
                "precisa_escalar_diogo": False,
                "resumo_diogo": f"Falha na IA: {str(e)}"
            }

    def fazer_triagem(self, lead_data: Dict) -> Dict:
        """
        Processa o lead e retorna o payload completo para Supabase e Telegram.
        """
        mensagem = lead_data.get("mensagem_original", "")
        # Processa com IA
        resultado_ia = self.analisar_mensagem_ia(mensagem)
        
        # Consolida payload para Supabase / Roteadores
        payload_final = {
            "lead_id": lead_data.get("lead_id"),
            "timestamp": datetime.now().isoformat(),
            "origem": lead_data.get("origem", "indefinida"),
            "nome_cliente": lead_data.get("nome_cliente", "Não informado"),
            "telefone_id": lead_data.get("telefone", ""),
            "mensagem_original": mensagem,

            "resposta_cliente": resultado_ia.get("resposta_cliente", ""),
            "status": resultado_ia.get("status_lead", "novo"),
            "urgencia": resultado_ia.get("urgencia", "media"),
            "servico": resultado_ia.get("servico_identificado", ""),
            "bairro": resultado_ia.get("bairro_identificado", ""),
            "tipo_cliente": resultado_ia.get("tipo_cliente", "indefinido"),
            "valor_inicial_informado": resultado_ia.get("valor_inicial_informado", ""),
            "dados_faltantes": resultado_ia.get("dados_faltantes", ""),
            "resumo_conversa": resultado_ia.get("resumo_conversa", ""),
            "proxima_acao": resultado_ia.get("proxima_acao", ""),
            "escalar_diogo": resultado_ia.get("precisa_escalar_diogo", False),
            "resumo_diogo": resultado_ia.get("resumo_diogo", "")
        }
        
        return payload_final
