import re
import json
import os
import requests
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
        Você é a ANINHA - Especialista Arquiteta e Engenharia B2B da DL Soluções Condominiais.
        A sua função é conversar com o cliente, entender a dor dele e classificar a demanda pareando com os nossos Produtos Oficiais Premium.
        
        EIXO ENERGIA/ELÉTRICA (categoria: eletrica, solar, mobilidade):
        - "DL Volt™": Infraestrutura de potência e painéis QDC/PC de Luz.
        - "DL Praxis Elétrica™": Projetos, balanceamento e engenharia com ART.
        - "DL Energia™": Consultoria e saúde da rede elétrica.
        - "DL EcoVolt Solar™": Projetos fotovoltaicos.
        - "DL VoltCharge™": Carregadores de veículos elétricos.
        
        EIXO SEGURANÇA (categoria: seguranca):
        - "DL Guardião™": CFTV forense, proteção perimetral e facial.
        - "DL Fortress™": App gestor, controle de interfone virtual e avisos.
        - "DL Observer™": Integração proativa PMERJ/Guarda Municipal.
        - "DL Gatekeeper™": Chave virtual WiFi/Bluetooth.
        
        EIXO AUTOMAÇÃO E PREVENÇÃO (categoria: automacao, incendio):
        - "DL Commander™": Automação de cisterna, bombas e telemetria.
        - "DL Alerta™": Prevenção a incêndio, fumaça e gás.
        - "DL Insight™": Dashboard Plataforma Whiteboard.
        
        EIXO SUPORTE B2B (categoria: consultoria):
        - "DL Partner™": Seguro de Hardware (Locação vitálicia).
        - "DL Support™": SLAs agressivos de atendimento técnico.
        - "DL Sustentia™" e "DL Praxis™": Metodologias e sustentabilidade.

        Sempre que processar um novo lead, você é OBRIGADA a devolver UM ÚNICO OUTPUT no formato JSON rigoroso.
        
        {
            "urgencia": "<valor>",
            "categoria_servico": "<valor>",
            "parecer": "<Breve resumo da dor, apontando obrigatoriamente para qual Produto Oficial da DL resolve o problema>"
        }
        
        REGRAS DE VALORES:
        - urgencia: Deve ser EXATAMENTE "baixa", "media", "alta", ou "critica".
        - categoria_servico: Deve ser EXATAMENTE "eletrica", "solar", "incendio", "seguranca", "mobilidade", "automacao" ou "indefinida".
        - Exemplo de Parecer Ideal: "Síndico reclama de sobrecarga de carros. Lead qualificado para DL Praxis Elétrica™ e DL VoltCharge™."
        """

    def calcular_porte(self, num_unidades: Optional[int]) -> Porte:
        if not num_unidades: return Porte.PEQUENO
        if num_unidades <= 30: return Porte.PEQUENO
        if num_unidades <= 100: return Porte.MEDIO
        if num_unidades <= 300: return Porte.GRANDE
        return Porte.COMPLEXO

    def buscar_historico(self, telefone: str) -> List[Dict[str, str]]:
        """
        Busca o histórico de mensagens do cliente no banco de dados (Supabase)
        para prover memória persistente.
        """
        if not telefone:
            return []

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not supabase_url or not supabase_key:
            print("Aviso: Variáveis do Supabase ausentes. Memória persistente desativada.")
            return []

        try:
            url = f"{supabase_url.rstrip('/')}/rest/v1/mensagens_whatsapp?telefone=eq.{telefone}&order=created_at.desc&limit=10"
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            }
            resp = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()

            mensagens = resp.json()

            historico = []
            # Como a ordem foi desc, revertemos para cronológica
            for msg in reversed(mensagens):
                texto = msg.get("mensagem", "")
                if not texto:
                    continue

                direcao = msg.get("direcao", "entrada")
                # entrada = o lead enviou (user), saida = a Aninha enviou (assistant)
                role = "user" if direcao == "entrada" else "assistant"

                historico.append({"role": role, "content": texto})

            return historico
        except Exception as e:
            print(f"Erro ao buscar histórico para {telefone}: {e}")
            return []

    def analisar_mensagem_ia(self, mensagem_cliente: str, telefone: str = None) -> Dict[str, Any]:
        """A IA lê a mensagem e gera o Json rigoroso, agora com contexto histórico"""
        if not self.client:
            return {
                "urgencia": "alta", 
                "categoria_servico": "eletrica", 
                "parecer": "Falha - OPENAI_API_KEY não configurada."
            }

        try:
            # Recuperar o histórico de mensagens para injetar na IA
            historico = self.buscar_historico(telefone) if telefone else []

            messages = [
                {"role": "system", "content": self.system_prompt}
            ]

            # Adiciona o histórico antes da nova mensagem
            messages.extend(historico)

            # Adiciona a mensagem atual
            messages.append({"role": "user", "content": f"Mensagem do lead B2B: {mensagem_cliente}"})

            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=messages,
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
        telefone = lead_data.get("telefone", "")

        # Processa com IA passando o telefone para contexto de histórico
        resultado_ia = self.analisar_mensagem_ia(mensagem, telefone=telefone)
        
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
            "telefone": telefone,
            "email": lead_data.get("email"),
            "origem": lead_data.get("origem")
        }
        
        return payload_final
