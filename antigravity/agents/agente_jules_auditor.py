import os
import json
from typing import Dict, Any
from anthropic import Anthropic

class JulesAuditorAgent:
    """
    Agente JULES: Auditor Técnico Sênior e Diretor de Qualidade (QA)
    Responsável por revisar propostas técnicas brutas antes da emissão final.
    """

    def __init__(self):
        # A chave de API deve ser configurada nas variáveis de ambiente (ex: Render)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            # Fallback seguro: Em ambiente de dev local sem chave, avisa no log,
            # mas o código não deve 'crashar' na importação. O erro será na chamada.
            pass

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229" # Usando Opus para raciocínio complexo de engenharia/auditoria

        self.system_prompt = """
        Você é JULES, Auditor Técnico Sênior e Diretor de Qualidade (QA) da DL Soluções Condominiais.

        Sua missão é atuar como a última barreira de qualidade antes que uma proposta técnica (Elétrica, Solar, Segurança, etc.)
        chegue ao cliente final. Você receberá uma "Proposta Bruta" gerada por outros agentes.

        Suas responsabilidades OBRIGATÓRIAS:
        1. REVISÃO TÉCNICA: Verifique rigorosamente a coerência de cálculos lógicos presentes na proposta.
           - Exemplo (Elétrica): Valide dimensionamento de cabos (bitolas), correntes de disjuntores, e balanceamento de fases.
           - Exemplo (Solar): Verifique estimativas de geração, ROI (Retorno sobre Investimento) e dimensionamento de inversores.
        2. CORREÇÃO DE JARGÕES: Corrija qualquer jargão técnico incorreto ou amador. A linguagem deve ser corporativa e precisa.
        3. REGRA DE NOMENCLATURA (CRÍTICA): Garanta que 'Diogo' seja tratado EXCLUSIVAMENTE pelo título de 'Tecnólogo'
           (ou 'Diogo Tecnólogo', 'nosso Tecnólogo Diogo'). É estritamente proibido referir-se a ele como 'Engenheiro'.
           Se encontrar o termo 'Engenheiro Diogo', altere imediatamente para 'Tecnólogo Diogo'.
        4. CLAREZA E PROFISSIONALISMO: Melhore a formatação do texto para que fique claro, persuasivo e profissional.

        SAÍDA ESPERADA:
        Você deve retornar EXCLUSIVAMENTE um objeto JSON válido (sem marcação Markdown em volta do JSON), com a seguinte estrutura:
        {
            "status_auditoria": "APROVADO_COM_CORRECOES" ou "REJEITADO_REVISAO_PROFUNDA",
            "proposta_corrigida": "O texto final revisado e formatado",
            "notas_do_auditor": "Seus comentários internos explicando o que você corrigiu (ex: 'Corrigido bitola de 2mm para 4mm por segurança; Alterado título de Diogo para Tecnólogo.')"
        }
        """

    def auditar_proposta(self, proposta_bruta: str, dados_contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Envia a proposta bruta para o Claude analisar e retorna o JSON estruturado.
        """
        try:
            prompt_user = f"Por favor, audite a seguinte proposta bruta gerada pela equipe técnica:\n\n{proposta_bruta}"

            if dados_contexto:
                prompt_user += f"\n\nContexto Adicional do Cliente:\n{json.dumps(dados_contexto, indent=2, ensure_ascii=False)}"

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.2, # Baixa temperatura para manter precisão técnica
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt_user}
                ]
            )

            conteudo_resposta = response.content[0].text

            # Tenta converter a resposta do Claude diretamente para um dicionário Python
            # Em cenários de produção, recomenda-se usar bibliotecas mais robustas
            # de extração de JSON (como Pydantic com o Claude) caso o LLM insira texto extra.
            resultado_json = json.loads(conteudo_resposta)
            return resultado_json

        except json.JSONDecodeError as e:
            # Fallback caso o LLM não retorne um JSON limpo
            return {
                "status_auditoria": "ERRO_FORMATACAO",
                "proposta_corrigida": proposta_bruta,
                "notas_do_auditor": f"Erro ao decodificar resposta JSON do auditor: {str(e)}",
                "resposta_bruta_auditor": conteudo_resposta if 'conteudo_resposta' in locals() else "N/A"
            }
        except Exception as e:
            # Fallback para erros de API (ex: sem chave, timeout)
            return {
                "status_auditoria": "ERRO_API",
                "proposta_corrigida": proposta_bruta,
                "notas_do_auditor": f"Falha ao comunicar com a API do Auditor (Claude): {str(e)}"
            }
