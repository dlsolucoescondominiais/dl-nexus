import os
import requests
import logging

logger = logging.getLogger(__name__)

class N8nMCPClient:
    """
    Cliente Python para interagir com o endpoint MCP no n8n.
    """
    def __init__(self, n8n_host=None):
        # Prefer the internal Docker URL by default based on architecture guidelines
        # to prevent DNS resolution or proxy failures.
        self.n8n_host = n8n_host or os.getenv("N8N_INTERNAL_URL", "http://n8n:5678")
        self.mcp_endpoint = f"{self.n8n_host}/webhook/mcp-server/http"

    def send_instruction(self, action: str, data: dict, agent: str = "jules") -> dict:
        """
        Envia uma instrução (payload) para o webhook MCP no n8n.

        Args:
            action (str): A ação que o n8n deve realizar (ex: 'sync_github', 'process_lead').
            data (dict): Os dados da instrução.
            agent (str): O agente que está enviando a instrução.

        Returns:
            dict: A resposta do n8n.
        """
        payload = {
            "agent": agent,
            "action": action,
            "data": data,
            "source": "antigravity"
        }

        try:
            logger.info(f"Enviando instrução MCP '{action}' para n8n: {self.mcp_endpoint}")
            # In a real environment, you might need to add headers for authentication (e.g. HeaderAuth)
            headers = {"Content-Type": "application/json"}

            response = requests.post(self.mcp_endpoint, json=payload, headers=headers, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao comunicar com n8n MCP Server: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "action": action
            }

# Example Usage:
# if __name__ == "__main__":
#     client = N8nMCPClient()
#     res = client.send_instruction(action="test_connection", data={"key": "value"})
#     print(res)
