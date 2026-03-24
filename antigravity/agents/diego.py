from enum import Enum
from typing import Dict, Any

class DiegoTecnologo:
    """
    Agente DIEGO: Coordenação Técnica e Dimensionamento
    Responsável por aprovar estratégias técnicas (Redes, Solar, etc.)
    e definir variáveis complexas.
    """

    def __init__(self):
        # Aqui ficarão as regras de negócio técnicas
        pass

    def avaliar_viabilidade(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa os dados triados pela Aninha e define o plano de ação técnico.
        """
        # Exemplo de lógica inicial:
        tipo_servico = lead_data.get("tipo_servico")

        resultado = {
            "status_tecnico": "em_analise",
            "parecer": "",
            "requer_visita_in_loco": True,
            "materiais_estimados": []
        }

        if tipo_servico == "SOLAR":
            resultado["parecer"] = "Necessário analisar conta de luz e área de telhado."
            resultado["materiais_estimados"] = ["Painéis Fotovoltaicos", "Inversor"]
        elif tipo_servico == "ELETRICO":
            resultado["parecer"] = "Agendar vistoria do PC de Luz e prumadas."
            resultado["materiais_estimados"] = ["Cabeamento", "Disjuntores", "Quadro de Distribuição"]
        else:
            resultado["parecer"] = "Aguardando mais informações para dimensionamento."

        return resultado
