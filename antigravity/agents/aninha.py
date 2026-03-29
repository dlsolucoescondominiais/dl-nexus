import os
import json
import logging
import google.generativeai as genai
from typing import Dict, Any

class AninhaAgent:
    """
    Agente ANINHA: Triagem Inteligente de Leads (Camada 2 - Gemini Flash)
    Função: Classificação rápida, barata e bloqueio de LIXO residual.
    """

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # GEMINI 1.5 FLASH: Ideal para triagem ultrarrápida e barata ($0.35/1M tokens)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def fazer_triagem(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitui as antigas regex puras por IA Rápida.
        Retorna JSON com a classificação.
        """
        if not self.model:
            # Fallback para regras burras se não houver chave
            return {"status": "triado", "tipo_servico": "NÃO_IDENTIFICADO", "prioridade": "baixa", "requer_audio": False}

        prompt = f"""
        Você é a Aninha, recepcionista inteligente da DL Soluções Condominiais.
        Sua tarefa é ler a mensagem do cliente e extrair 4 informações vitais.

        MENSAGEM: "{lead_data.get('mensagem_original', '')}"

        REGRAS:
        1. status: Se a mensagem for sobre vender algo para nós, buscar emprego, ou spam óbvio, retorne "LIXO". Se for um possível cliente, retorne "LEAD".
        2. tipo_servico: Tente classificar em: ELETRICO, SOLAR, SEGURANCA, INCENDIO, AUTOMACAO, CONSULTORIA. Se não souber, "INDEFINIDO".
        3. prioridade: "ALTA" (emergência, incêndio, choque), "MEDIA" (orçamento normal), "BAIXA" (dúvida vaga).
        4. requer_audio: Retorne true APENAS se a prioridade for ALTA ou se o cliente parecer ser um lead Premium/Grande porte. Caso contrário, false.

        Responda APENAS com um objeto JSON válido (sem blocos markdown).
        Exemplo: {{"status": "LEAD", "tipo_servico": "SOLAR", "prioridade": "MEDIA", "requer_audio": false}}
        """

        try:
            response = self.model.generate_content(prompt)
            texto = response.text.strip().removeprefix('```json').removeprefix('```').removesuffix('```').strip()
            resultado = json.loads(texto)
            return resultado
        except Exception as e:
            logging.error(f"Erro no Gemini Flash (Aninha): {str(e)}")
            return {"status": "LEAD", "tipo_servico": "INDEFINIDO", "prioridade": "MEDIA", "requer_audio": False}
