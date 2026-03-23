import re
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import json

class TipoServico(Enum):
    """Tipos de serviço baseados no portfólio DL Soluções"""
    ELETRICO = "ELETRICO"  # DL Volt™, DL Praxis Elétrica™, DL Energia™
    SOLAR = "SOLAR"  # DL EcoVolt Solar™
    SEGURANCA = "SEGURANCA"  # DL Guardião™, DL Observer™, DL Gatekeeper™
    INCENDIO = "INCENDIO"  # DL Alerta™
    MOBILIDADE = "MOBILIDADE"  # DL VoltCharge™
    AUTOMACAO = "AUTOMACAO"  # DL Commander™, DL Fortress™
    CONSULTORIA = "CONSULTORIA"  # DL Praxis™, DL Sustentia™

class Porte(Enum):
    """Porte do condomínio baseado no número de unidades"""
    PEQUENO = "PEQUENO"  # Até 30 unidades
    MEDIO = "MEDIO"  # 31 a 100 unidades
    GRANDE = "GRANDE"  # 101 a 300 unidades
    COMPLEXO = "COMPLEXO"  # 301+ unidades

class AninhaAgent:
    """
    Agente ANINHA: Triagem Inteligente de Leads (Híbrida: Regras + Contexto)
    """

    def __init__(self):
        self.palavras_chave_servicos = {
            TipoServico.ELETRICO: [
                r"\belétrico\b", r"\beletricidade\b", r"\bpainel\b", r"\bdisjuntor\b", r"\bfiação\b",
                r"\breforma elétrica\b", r"\binstalação elétrica\b", r"\bpc de luz\b",
                r"\bdl volt\b", r"\bpraxis elétrica\b", r"\bdl energia\b"
            ],
            TipoServico.SOLAR: [
                r"\bsolar\b", r"\benergia solar\b", r"\bfotovoltaico\b", r"\bpainel solar\b",
                r"\bbateria\b", r"\bhíbrido\b", r"\becovolt\b", r"\busina solar\b"
            ],
            TipoServico.SEGURANCA: [
                r"\bcâmera\b", r"\bcftv\b", r"\bsegurança\b", r"\bvigilância\b", r"\bportão\b",
                r"\bacesso\b", r"\bgatekeeper\b", r"\bguardião\b", r"\bobserver\b", r"\bcerca\b",
                r"\bcontrole de acesso\b", r"\bchave virtual\b"
            ],
            TipoServico.INCENDIO: [
                r"\bincêndio\b", r"\bdetector\b", r"\bfumaça\b", r"\balarme\b", r"\bsinalização\b",
                r"\bemergência\b", r"\balerta\b", r"\bprevenção incêndio\b"
            ],
            TipoServico.MOBILIDADE: [
                r"\bcarregador\b", r"\bcve\b", r"\bveículo elétrico\b", r"\bwallbox\b",
                r"\bvoltcharge\b", r"\bev charger\b", r"\bcarro elétrico\b"
            ],
            TipoServico.AUTOMACAO: [
                r"\bautomação\b", r"\bcomando\b", r"\btelemetria\b", r"\bsmart building\b",
                r"\bcommander\b", r"\bfortress\b", r"\bportaria digital\b"
            ],
            TipoServico.CONSULTORIA: [
                r"\bconsultoria\b", r"\bauditoria\b", r"\bsustentabilidade\b", r"\besg\b",
                r"\bpraxis\b", r"\bsustentia\b", r"\beficiência energética\b"
            ]
        }

        self.palavras_chave_bloqueio_b2b = [
            r"\bcasa\b", r"\bresidência\b", r"\bapartamento\b", r"\bmeu apartamento\b",
            r"\bminha casa\b", r"\bresidencial\b", r"\buso pessoal\b", r"\bparticular\b"
        ]

        self.palavras_chave_bloqueio_escopo = [
            r"\bbomba\b", r"\bhidrante\b", r"\bsprinkler\b", r"\bprumada\b", r"\bhidráulica\b",
            r"\bencanamento\b", r"\bmanutenção mecânica\b", r"\breparos gerais\b", r"\bcanaleta de plástico\b"
        ]

    def match_keywords(self, text: str, patterns: List[str]) -> bool:
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return True
        return False

    def validar_b2b(self, mensagem: str, tipo_imovel: Optional[str] = None) -> bool:
        """ Valida B2B mas PERMITE residencial se for MOBILIDADE (Carregador VE) """
        msg_lower = mensagem.lower()
        tipo_lower = (tipo_imovel or "").lower()

        # Exceção de regra rígida: Permite residencial SE for instalação de carregador veicular
        is_mobilidade = self.match_keywords(msg_lower, self.palavras_chave_servicos[TipoServico.MOBILIDADE])

        has_block = self.match_keywords(msg_lower, self.palavras_chave_bloqueio_b2b) or \
                    self.match_keywords(tipo_lower, self.palavras_chave_bloqueio_b2b)

        if has_block:
            if is_mobilidade:
                return True # Exceção garantida!
            return False

        return True

    def validar_escopo(self, mensagem: str) -> tuple[bool, str]:
        """ Retorna (Valido, Motivo) """
        msg_lower = mensagem.lower()

        if re.search(r"canaleta.*pl[áa]stico", msg_lower):
            return False, "Fora de escopo/Qualidade: Não utilizamos canaletas de plástico."

        if self.match_keywords(msg_lower, self.palavras_chave_bloqueio_escopo):
            return False, "Fora de escopo: Foco exclusivo em elétrica e automação dry (sem hidráulica direta)."

        for tipo, palavras in self.palavras_chave_servicos.items():
            if self.match_keywords(msg_lower, palavras):
                return True, "Escopo validado"

        return False, "Serviço não identificado no portfólio DL Soluções."

    def classificar_servico(self, mensagem: str) -> Optional[TipoServico]:
        """ Classifica com base no maior número de matches de regex """
        scores = {tipo: 0 for tipo in TipoServico}
        for tipo_servico, palavras in self.palavras_chave_servicos.items():
            for regex in palavras:
                if re.search(regex, mensagem, re.IGNORECASE):
                    scores[tipo_servico] += 1

        best_match = max(scores, key=scores.get)
        return best_match if scores[best_match] > 0 else None

    def calcular_porte(self, num_unidades: Optional[int]) -> Porte:
        if not num_unidades: return Porte.PEQUENO
        if num_unidades <= 30: return Porte.PEQUENO
        if num_unidades <= 100: return Porte.MEDIO
        if num_unidades <= 300: return Porte.GRANDE
        return Porte.COMPLEXO

    def calcular_valor_mensal(self, porte: Porte, tipo_servico: TipoServico) -> float:
        valores_base = { Porte.PEQUENO: 400.0, Porte.MEDIO: 600.0, Porte.GRANDE: 1000.0, Porte.COMPLEXO: 1500.0 }
        multiplicadores = {
            TipoServico.ELETRICO: 1.0, TipoServico.SOLAR: 1.5, TipoServico.SEGURANCA: 1.3,
            TipoServico.INCENDIO: 1.1, TipoServico.MOBILIDADE: 1.2, TipoServico.AUTOMACAO: 1.2,
            TipoServico.CONSULTORIA: 0.8
        }
        return valores_base.get(porte, 400.0) * multiplicadores.get(tipo_servico, 1.0)

    def definir_sla(self, tipo_servico: TipoServico, prioridade_texto: str) -> str:
        """ Regra rígida de SLAs de Atendimento DL """
        if "alta" in prioridade_texto.lower() or tipo_servico in [TipoServico.INCENDIO]:
            return "SLA 8 horas"
        elif tipo_servico in [TipoServico.ELETRICO, TipoServico.SEGURANCA]:
            return "SLA 24 horas"
        return "SLA 48 horas"

    def fazer_triagem(self, lead_data: Dict) -> Dict:
        resultado = {
            "status": "bloqueado",
            "motivo": None,
            "lead_id": lead_data.get("lead_id"),
            "timestamp": datetime.now().isoformat()
        }

        if not self.validar_b2b(lead_data.get("mensagem_original", ""), lead_data.get("tipo_imovel")):
            resultado["motivo"] = "Lead residencial. Foco exclusivo em Condomínios e B2B Escolar."
            return resultado

        escopo_ok, escopo_motivo = self.validar_escopo(lead_data.get("mensagem_original", ""))
        if not escopo_ok:
            resultado["motivo"] = escopo_motivo
            return resultado

        tipo_servico = self.classificar_servico(lead_data.get("mensagem_original", ""))
        porte = self.calcular_porte(lead_data.get("num_unidades"))
        valor_mensal = self.calcular_valor_mensal(porte, tipo_servico) if tipo_servico else 0
        sla = self.definir_sla(tipo_servico or TipoServico.ELETRICO, lead_data.get("prioridade", ""))

        resultado.update({
            "status": "triado",
            "tipo_servico": tipo_servico.value if tipo_servico else "NÃO_IDENTIFICADO",
            "porte": porte.value,
            "valor_mensal_estimado": valor_mensal,
            "sla_estimado": sla,
            "proxima_acao_obrigatoria": "Agendar Avaliação Técnica", # Nunca 'Visita Técnica'
            "nome_condominio": lead_data.get("nome_condominio"),
            "telefone": lead_data.get("telefone"),
            "email": lead_data.get("email"),
            "origem": lead_data.get("origem")
        })
        return resultado
