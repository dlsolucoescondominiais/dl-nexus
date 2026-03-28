import os
import time
from typing import Optional, Dict, Any
import google.generativeai as genai
from openai import OpenAI

class MultiLLMRouter:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # Anthropic could be added here

    def generate_response(self, system_prompt: str, user_message: str, fallback_chain: list = ['openai', 'gemini']) -> str:
        """
        Executes a Multi-LLM Fallback Strategy.
        If the primary provider fails, it seamlessly falls back to the next one.
        """
        for provider in fallback_chain:
            try:
                if provider == 'openai':
                    return self._call_openai(system_prompt, user_message)
                elif provider == 'gemini':
                    return self._call_gemini(system_prompt, user_message)
                # elif provider == 'anthropic': ...
            except Exception as e:
                print(f"[LLM_ROUTER] Provider {provider} falhou: {str(e)}. Tentando próximo...")
                time.sleep(1) # Backoff
                continue

        raise Exception("CRITICAL: Todos os provedores LLM falharam (Contingência esgotada).")

    def _call_openai(self, system: str, user: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            timeout=15
        )
        return response.choices[0].message.content

    def _call_gemini(self, system: str, user: str) -> str:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"System: {system}\n\nUser: {user}"
        response = model.generate_content(prompt)
        return response.text
