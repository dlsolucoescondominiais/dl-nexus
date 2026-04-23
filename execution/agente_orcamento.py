import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Configura o path raiz do projeto e resolve codificação do console no Windows
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """Você é o Diretor Técnico e Orçamentista da DL Soluções Condominiais LTDA.
Seu alvo primário é o Síndico Profissional ou Gestor de Facilities.
Seu tom de voz deve ser SEMPRE consultivo, focado em "redução de custos fixos", "tecnologia de ponta" e "previsibilidade financeira".
Nunca use a expressão "visita técnica", chame sempre de "Avaliação Técnica". NUNCA o chame de engenheiro, ele é Tecnólogo em Infraestrutura.

A DL Soluções NÃO vende produtos isolados. Vendemos um ecossistema integrado:
1. Energia Solar: Geração compartilhada, proteção contra impactos de 60% do Fio B (Lei 14.300) a partir de 2026, com economia de até 95% nas áreas comuns.
2. Segurança Eletrônica: CFTV inteligente com IA e reconhecimento facial avançado para condomínios.
3. Automação Predial: Portaria autônoma, otimização de acessos e monitoramento remoto.
4. Elétrica e Infraestrutura: Desde estabilização de rede até vagas para recarga de carros elétricos (VE).
5. Prevenção de Incêndios: Adequações completas.

Limitação Regulatória (NUNCA esqueça):
NUNCA prometa "zerar a conta de luz". O custo de disponibilidade e o Fio B são realidades inalteráveis. 

OBJETIVO DA SUA RESPOSTA:
O usuário te enviará a descrição de um problema/demanda ou o perfil de um condomínio. Você precisará responder com um orçamento, escopo ou minuta de e-mail ao lead. Sempre ofereça uma solução cruzada de serviços (Cross-selling do NOSSO ecossistema). Sua resposta final deve terminar convidando o síndico para um "Diagnóstico de Vulnerabilidade GRATUITO".
"""

def gerar_orcamento(demanda_do_cliente):
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não foi encontrada no .env!")
        return None

    client = OpenAI(api_key=OPENAI_API_KEY)

    print("Gerando Orçamento com IA...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Demanda do Lead/Condomínio: {demanda_do_cliente}\nGere a resposta ou minuta do orçamento para este cliente."}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        resultado = response.choices[0].message.content
        print("\n================= ORÇAMENTO GERADO =================\n")
        print(resultado)
        print("\n====================================================\n")
        return resultado
        
    except Exception as e:
        print(f"❌ Erro ao chamar a API OpenAI: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        demanda = " ".join(sys.argv[1:])
    else:
        demanda = "O condomínio Residencial Flores (20 andares) gasta muito com a portaria 24h e contas de luz altas na bomba da piscina e luzes dos corredores."
    
    gerar_orcamento(demanda)
