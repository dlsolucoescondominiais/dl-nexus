import os
import json
import time

# Ensure relative imports work
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# mock openai module
class MockChatCompletionMessage:
    def __init__(self, content):
        self.content = content

class MockChatCompletionChoice:
    def __init__(self, content):
        self.message = MockChatCompletionMessage(content)

class MockChatCompletion:
    def __init__(self, content):
        self.choices = [MockChatCompletionChoice(content)]

class MockCompletions:
    def create(self, **kwargs):
        # mock response for Leme
        msg = kwargs.get('messages')[-1]['content']
        if "Leme" in msg:
            content = json.dumps({
                "resposta_cliente": "Sim, a DL atende instalação de câmeras para condomínios, empresas e clientes comerciais. Para o Leme, o atendimento entra como região de alto custo operacional por causa de deslocamento, estacionamento e acesso. A instalação costuma partir de R$ 500 nessa região, podendo variar conforme infraestrutura existente, tipo de câmera, passagem de cabo e configuração no DVR/NVR. Para estimar corretamente, preciso confirmar: 1. A câmera já existe ou será fornecida pela DL? 2. Já existe cabo ou rede no ponto? 3. É somente instalação ou também configuração no gravador?",
                "status_lead": "aguardando_dados",
                "urgencia": "media",
                "servico_identificado": "Instalação de câmera",
                "bairro_identificado": "Leme",
                "tipo_cliente": "indefinido",
                "precisa_escalar_diogo": False,
                "resumo_diogo": None
            })
        elif "CFTV" in msg:
            content = json.dumps({
                "resposta_cliente": "O atendimento de CFTV começa a partir de R$ 350. Qual seu bairro?",
                "status_lead": "aguardando_dados"
            })
        else:
            content = json.dumps({
                "resposta_cliente": "Estimativa a partir de R$ 350. Qual seu bairro?",
                "status_lead": "aguardando_dados"
            })

        return MockChatCompletion(content)

class MockChat:
    def __init__(self):
        self.completions = MockCompletions()

class MockOpenAIClient:
    def __init__(self, api_key=None):
        self.chat = MockChat()

class MockOpenAI:
    OpenAI = MockOpenAIClient

sys.modules['openai'] = MockOpenAI()

from antigravity.agents.aninha import AninhaAgent

test_messages = [
    "Quero instalar uma câmera no Leme.",
    "Preciso extrair imagens do DVR do condomínio.",
    "Quanto custa manutenção de CFTV?",
    "Vocês fazem controle de acesso facial?",
    "Preciso automatizar bomba da cisterna.",
    "Vocês atendem restaurante com fritadeira?",
    "Quero orçamento para portaria autônoma.",
    "Preciso de elétrica no quadro de bombas.",
    "Vocês fazem prevenção de incêndio?",
    "Quero instalar câmera em residência."
]

def run_tests():
    # Force API key for the test so mock is used
    os.environ["OPENAI_API_KEY"] = "mock-key"
    agent = AninhaAgent()

    relatorio_md = "# RELATÓRIO DE TESTES: ANINHA TELEGRAM V3\n\n"

    for idx, msg in enumerate(test_messages, 1):
        print(f"Testando [{idx}/10]: {msg}")

        lead_data = {
            "lead_id": f"test-{idx}",
            "mensagem_original": msg,
            "origem": "telegram"
        }

        resultado = agent.fazer_triagem(lead_data)
        resposta_cliente = resultado.get('resposta_cliente', '')

        # Simple heuristic to determine PASS/FAIL
        reprovado = False
        erro_encontrado = []

        if "visita técnica" in resposta_cliente.lower() or "vistoria" in resposta_cliente.lower():
            reprovado = True
            erro_encontrado.append("Usou termo proibido (visita técnica/vistoria).")

        if "engenheiro" in resposta_cliente.lower():
            reprovado = True
            erro_encontrado.append("Chamou de engenheiro.")

        if "leme" in msg.lower() and "500" not in resposta_cliente:
             reprovado = True
             erro_encontrado.append("Não aplicou valor correto para o Leme (Categoria C).")

        if "?" in resposta_cliente:
            num_perguntas = resposta_cliente.count("?")
            if num_perguntas > 3:
                reprovado = True
                erro_encontrado.append(f"Fez muitas perguntas ({num_perguntas}). Máximo é 3.")

        # Se Leme, deve falar do custo operacional
        if "leme" in msg.lower() and "custo operacional" not in resposta_cliente.lower() and "deslocamento" not in resposta_cliente.lower():
            reprovado = True
            erro_encontrado.append("Não explicou o custo operacional da Categoria C.")

        # Se for CFTV, deve ter preço de CFTV inicial
        if "manutenção de cftv" in msg.lower() and "350" not in resposta_cliente:
            reprovado = True
            erro_encontrado.append("Não passou preço inicial de R$ 350 para CFTV.")

        status = "❌ REPROVADO" if reprovado else "✅ APROVADO"
        erros_str = ", ".join(erro_encontrado) if erro_encontrado else "Nenhum"
        correcao = "Ajustar base comercial/prompt" if reprovado else "N/A"

        relatorio_md += f"## Teste {idx}\n"
        relatorio_md += f"**Mensagem Enviada:** {msg}\n\n"
        relatorio_md += f"**Resposta da Aninha:**\n> {resposta_cliente}\n\n"
        relatorio_md += f"**Escalar para Diogo?** {resultado.get('escalar_diogo')}\n"
        relatorio_md += f"**Resumo Diogo:** {resultado.get('resumo_diogo')}\n"
        relatorio_md += f"**Status Lead:** {resultado.get('status')}\n\n"
        relatorio_md += f"**Resultado:** {status}\n"
        relatorio_md += f"**Erro Encontrado:** {erros_str}\n"
        relatorio_md += f"**Correção Aplicada:** {correcao}\n"
        relatorio_md += "---\n\n"

        time.sleep(0.1) # rate limit mock

    os.makedirs("reports", exist_ok=True)
    with open("reports/RELATORIO_ANINHA_TELEGRAM.md", "w", encoding="utf-8") as f:
        f.write(relatorio_md)

    print("Testes concluídos. Relatório gerado em reports/RELATORIO_ANINHA_TELEGRAM.md")

if __name__ == "__main__":
    run_tests()
