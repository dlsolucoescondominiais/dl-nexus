import os
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

class LeadManager:
    """Manager for leads in Supabase based on MIGRATIONS_DL_NEXUS.sql"""

    def __init__(self, url: str = None, key: str = None):
        self.url = (url or SUPABASE_URL).rstrip("/")
        self.key = key or SUPABASE_KEY
        self.session = requests.Session()
        self.session.headers.update({
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        })

    def validate_lead(self, data: Dict[str, Any]) -> None:
        """20. Validar campos obrigatórios."""
        if not data.get("telefone") and not data.get("email"):
            raise ValueError("Telefone ou E-mail são obrigatórios.")
        if not data.get("nome_contato") and not data.get("nome_condominio"):
            raise ValueError("Nome do Contato ou Nome do Condomínio são obrigatórios.")

    def get_all_leads(self, limit: int = 100) -> List[Dict]:
        """2. Ler tabela leads."""
        url = f"{self.url}/rest/v1/leads?select=*&limit={limit}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_lead_by_telefone(self, telefone: str) -> Optional[Dict]:
        """6. Buscar lead por telefone."""
        url = f"{self.url}/rest/v1/leads?telefone=eq.{telefone}&select=*"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None

    def get_lead_by_email(self, email: str) -> Optional[Dict]:
        """7. Buscar lead por e-mail."""
        url = f"{self.url}/rest/v1/leads?email=eq.{email}&select=*"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if data else None

    def get_lead_by_nome(self, nome: str) -> List[Dict]:
        """8. Buscar lead por nome."""
        # Using ilike for case-insensitive search
        url = f"{self.url}/rest/v1/leads?nome_contato=ilike.*{nome}*&select=*"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def find_existing_lead(self, data: Dict[str, Any]) -> Optional[Dict]:
        """5. Evitar duplicidade."""
        if data.get("telefone"):
            lead = self.get_lead_by_telefone(data["telefone"])
            if lead:
                return lead
        if data.get("email"):
            lead = self.get_lead_by_email(data["email"])
            if lead:
                return lead
        return None

    def create_lead(self, data: Dict[str, Any]) -> Dict:
        """3. Criar novo lead."""
        self.validate_lead(data)

        # 5. Evitar duplicidade (se existir, atualiza)
        existing = self.find_existing_lead(data)
        if existing:
            return self.update_lead(existing["id"], data)

        # 15. Registrar data de criação
        # 16. Registrar data de atualização
        now = datetime.now().isoformat()
        data["created_at"] = now
        data["ultima_interacao"] = now  # Present on V6

        url = f"{self.url}/rest/v1/leads"
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()[0]

    def update_lead(self, lead_id: str, data: Dict[str, Any]) -> Dict:
        """4. Atualizar lead existente."""
        # 16. Registrar data de atualização
        data["ultima_interacao"] = datetime.now().isoformat()

        url = f"{self.url}/rest/v1/leads?id=eq.{lead_id}"
        resp = self.session.patch(url, json=data)
        resp.raise_for_status()
        return resp.json()[0]

    def update_status(self, lead_id: str, status: str) -> Dict:
        """9. Atualizar status do lead."""
        # Also map to pipeline_stage (V6)
        return self.update_lead(lead_id, {
            "status": status,
            "pipeline_stage": status if status in ['novo_lead', 'triagem_ia', 'avaliacao_agendada', 'proposta_enviada', 'negociacao', 'fechado_ganho', 'fechado_perdido'] else "novo_lead"
        })

    def update_origem(self, lead_id: str, origem: str) -> Dict:
        """10. Registrar origem do lead."""
        return self.update_lead(lead_id, {"origem": origem})

    def update_servico_interesse(self, lead_id: str, servico: str) -> Dict:
        """11. Registrar serviço de interesse."""
        # Maps to tipo_servico / servico_desejado
        return self.update_lead(lead_id, {
            "tipo_servico": servico,
            "servico_desejado": servico
        })

    def update_bairro_regiao(self, lead_id: str, regiao: str) -> Dict:
        """12. Registrar bairro (região)."""
        return self.update_lead(lead_id, {"regiao": regiao})

    def update_prioridade(self, lead_id: str, prioridade: str) -> Dict:
        """13. Registrar prioridade."""
        # e.g., 'baixa', 'urgencia'
        return self.update_lead(lead_id, {"prioridade": prioridade, "urgencia": prioridade})

    def update_observacoes(self, lead_id: str, observacoes: str) -> Dict:
        """14. Registrar observações."""
        return self.update_lead(lead_id, {"resumo_conversa": observacoes})

    def update_responsavel(self, lead_id: str, responsavel: str) -> Dict:
        """17. Registrar responsável."""
        return self.update_lead(lead_id, {"responsavel_interno": responsavel})

    def update_proximo_passo(self, lead_id: str, proximo_passo: str) -> Dict:
        """18. Registrar próximo passo."""
        # V6 has proximo_followup (timestamp), but could just use a text field if it existed, we map to observacoes or a follow up date
        # Assuming proximo_passo is a datetime string for proximo_followup
        return self.update_lead(lead_id, {"proximo_followup": proximo_passo})

    def add_historico_atendimento(self, lead_id: str, telefone: str, mensagem: str, direcao: str = 'entrada') -> Dict:
        """19. Registrar histórico de atendimento."""
        # Inserts into mensagens_whatsapp
        url = f"{self.url}/rest/v1/mensagens_whatsapp"
        data = {
            "lead_id": lead_id,
            "telefone": telefone,
            "mensagem": mensagem,
            "direcao": direcao,
            "created_at": datetime.now().isoformat()
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()[0]
