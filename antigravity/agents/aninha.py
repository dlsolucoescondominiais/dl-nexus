from core.llm_router import MultiLLMRouter
# import supabase_client...

class AninhaAgent:
    def __init__(self, router: MultiLLMRouter):
        self.router = router
        self.system_prompt = """
        Você é a Aninha, assistente virtual inteligente da DL Soluções Condominiais.
        Seu objetivo é fazer uma triagem rápida com síndicos e zeladores.
        Identifique se eles precisam de serviços de Infraestrutura de Redes, CFTV, Energia Solar, Elétrica ou Prevenção de Incêndio.
        NUNCA use o termo 'visita técnica'. Use 'Avaliação Técnica'.
        Mantenha as respostas curtas e objetivas.
        """

    def processar_mensagem(self, telefone: str, mensagem: str) -> str:
        try:
            # Chama o roteador multi-llm (OpenAI -> Gemini -> Fallback)
            resposta = self.router.generate_response(self.system_prompt, mensagem)

            # TODO: Aqui entraria o código para atualizar a tabela 'leads' no Supabase
            # se a IA determinar que é uma qualificação positiva.
            # e.g., supabase.table('leads').update({...}).eq('telefone', telefone).execute()

            return resposta
        except Exception as e:
            # Erro crítico pego no nível do agente
            print(f"[Aninha] Erro crítico ao processar: {e}")
            raise e
