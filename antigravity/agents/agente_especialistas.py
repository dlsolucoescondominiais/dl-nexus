import os
from openai import OpenAI
from typing import Dict, Any

class AgenteEspecialista:
    """
    Responsável por redigir a 'Proposta Bruta' (Draft Técnico) baseada nas dores do sistema de triagem.
    Atua focado puramente na sua área de expertise, antes de passar pelo JULES (QA).
    Motor: OpenAI (GPT-4o ou gpt-3.5-turbo)
    """
    
    def __init__(self):
        # A chave será pega do `.env` ou do ambiente operacional da VPS
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None

    def _obter_system_prompt(self, categoria: str) -> str:
        """Retorna a persona técnica correta baseada na classificação da Aninha"""
        
        base_prompt = (
            "Você é um Engenheiro Júnior/Pleno da DL Soluções Condominiais.\n"
            "Sua missão é rascunhar uma Proposta Comercial e Técnica baseada nos dados do lead.\n"
            "Formate sua saída em Markdown bem estruturado (Causa, Solução Proposta, Benefícios).\n"
            "NÃO envie JSON. Envie apenas o texto da proposta para ser lido e auditado pelo seu Diretor.\n\n"
        )

        categorias = {
            "eletrica": "ÁREA DE ATUAÇÃO: Engenharia Elétrica, Quadros de Força, Retrofit Elétrico e Preventiva de Relógios PC.",
            "solar": "ÁREA DE ATUAÇÃO: Energia Solar Fotovoltaica, Lei 14.300, Usinas em Telhados e Inversores.",
            "incendio": "ÁREA DE ATUAÇÃO: Prevenção e Combate a Incêndio (PPCI), Bombas de Pressurização e Sprinklers.",
            "seguranca": "ÁREA DE ATUAÇÃO: CFTV, Câmeras IP, Controle de Acesso Facial/Tag e Portaria Remota.",
            "automacao": "ÁREA DE ATUAÇÃO: Automação Predial, IoT, Sensores de Nível de Caixa d'água e Iluminação Inteligente."
        }
        
        # Garante fallback para um Técnico em Manutenção Geral se a categoria for desconhecida
        expertise = categorias.get(categoria.lower(), "ÁREA DE ATUAÇÃO: Manutenção e Facilities Predial Geral.")
        
        return base_prompt + expertise

    def gerar_draft_proposta(self, dor_do_cliente: str, categoria: str, urgencia: str) -> str:
        """ Gera o texto cru da proposta baseado no diagnóstico da Aninha """
        if not self.client:
            return "Erro: OPENAI_API_KEY ausente ou inválida. O Especialista não pôde ser instanciado."

        prompt_sistema = self._obter_system_prompt(categoria)
        
        prompt_usuario = (
            f"O lead relatou o seguinte problema/necessidade: '{dor_do_cliente}'.\n"
            f"O sistema classificou a urgência como: {urgencia.upper()}.\n\n"
            "Por favor, rascunhe a proposta técnica e os serviços recomendados para resolver este problema em nome da DL Soluções."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # O motor pode ser ajustado conforme custo (gpt-4o-mini é excelente para drafts)
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.3 # Mantemos baixo para não viajar na maionese técnica
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"[Erro Catastrófico no Agente Especialista]: Falha ao conectar ao cérebro OpenAi. {str(e)}"
