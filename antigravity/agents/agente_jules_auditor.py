import os
import json
import anthropic
from typing import Dict, Any

class JulesAuditorAgent:
    """
    Agente JULES: Diretor de Qualidade (QA) e Auditor Técnico Sênior
    Motor: Anthropic (Claude 3.5 Sonnet ou Claude 3 Haiku)
    """
    def __init__(self):
        # API Key da Anthropic configurada no .env ou injetada no ambiente
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
        
        self.system_prompt = """
        Você é JULES, o Diretor de Qualidade (QA) e Auditor Técnico Sênior da DL Soluções Condominiais.
        
        Sua função primária é auditar e revisar todas as "Propostas Brutas" (geradas por agentes técnicos júniores de Elétrica, Solar, Segurança, etc.) antes da emissão do Laudo/PDF oficial para os condomínios.
        
        DIRETRIZES FUNDAMENTAIS (LEI CUMPRIDA À RISCA):
        1. REVISÃO LÓGICA: Confira se cálculos óbvios fazem sentido (bitolas de cabos coerentes com disjuntores, ROI de energia solar faz sentido, dimensionamento lógico).
        2. JARGÃO TÉCNICO: Remova ou corrija jargões informais ou gramaticalmente incorretos. A linguagem deve ser técnica, culta e afiada para leitura de Síndicos (Engenharia B2B).
        3. REGRA DO NOME: Ao se referir ao seu superior, o Arquiteto de Sistemas corporativo e fundador, trate Diogo EXCLUSIVAMENTE como "Tecnólogo" ou "Arquiteto de Sistemas". VOCÊ JAMAIS DEVE CHAMÁ-LO DE ENGENHEIRO.
        
        FORMATO DE SAÍDA (OBRIGATÓRIO):
        Você NUNCA deve retornar textos soltos. Devolva única e estritamente UM OBJETO JSON VÁLIDO contendo as seguintes chaves:
        {
            "status_auditoria": "APROVADO" ou "REPROVADO",
            "erros_encontrados": ["lista de erros encontrados, se houver"],
            "proposta_corrigida": "O texto final limpo, estruturado, mantendo todo detalhamento técnico, pronto para pdf.",
            "observacoes_qa": "Seu parecer breve como QA Sênior"
        }
        """

    def auditar_proposta(self, proposta_bruta: str) -> Dict[str, Any]:
        """ Recebe a proposta técnica gerada e devolve auditada em JSON """
        if not self.client:
            return {
                "status_auditoria": "REPROVADO",
                "erros_encontrados": ["A ANTHROPIC_API_KEY falhou ou não existe no ambiente."],
                "proposta_corrigida": proposta_bruta,
                "observacoes_qa": "Falha no motor do Diretor (Sem chave API)."
            }

        try:
            # Integração correta e nativa para chamada JSON na Anthropic Messages API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620", 
                max_tokens=4096,
                temperature=0.1, # Temperatura baixa para QA cirúrgico
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Por favor, audite rigorosamente a seguinte proposta bruta gerada pela equipe:\n\n{proposta_bruta}\n\nLembre-se: Responda SOMENTE com o JSON válido."
                    }
                ]
            )
            
            # A API do Claude devolve uma lista de ContentBlocks
            conteudo_json = response.content[0].text
            payload = json.loads(conteudo_json)
            
            return payload
            
        except Exception as e:
            return {
                "status_auditoria": "REPROVADO",
                "erros_encontrados": [f"Erro crítico do Motor Claude: {str(e)}"],
                "proposta_corrigida": proposta_bruta,
                "observacoes_qa": "O agente não conseguiu analisar. Necessita intervenção humana."
            }
