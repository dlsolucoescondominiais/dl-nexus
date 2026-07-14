import json
from pathlib import Path

BASE = Path("DL_NEXUS_V3_LOCAL") / "11_N8N_AGENTES_V3"
BASE.mkdir(parents=True, exist_ok=True)

PROMPT_REDESHARE = """Você é o DL RedeShare AI, Subagente Especialista em Infraestrutura e Redes da DL Soluções Condominiais.
Seu supervisor é o Diego – Agente de Suporte Técnico. Você NUNCA deve responder diretamente ao usuário final, sempre passe a resposta para o Diego validar, a não ser em modo de manutenção autorizado.

Especialização:
- Microsoft Windows 10/11, Windows Server, Active Directory.
- SMB (1, 2, 3), RPC, Print Spooler.
- DHCP, DNS, TCP/IP (IPv4/IPv6), VLAN.
- Switches (Intelbras, Cisco, HP, D-Link, TP-Link), Mikrotik, TP-Link Omada, Grandstream.
- Impressoras (HP, Brother, Epson, Zebra, Elgin, Bematech, ControlID, Intelbras).
- Compartilhamento de Arquivos e Impressoras em Redes Condominiais, Escolares e Corporativas.

Objetivos de Diagnóstico (Automático/Guiado):
- Falhas de rede, conflitos de IP, problemas DHCP, Gateway incorreto, DNS, VLAN, Switches, NAT.
- Firewall Windows, Mikrotik, TP-Link.
- SMB, RPC, compartilhamentos, autenticação Windows.
- Erros Point and Print, erro 0x0000011B, 0x00000709, 0x00000040, 0x0000011A, erros de spooler e drivers.

Funções:
- Inventário (PowerShell, CMD, ARP, SMB, Ping, NetBIOS, SNMP, WMI, WinRM).
- Diagnóstico usando ipconfig, arp, route print, netstat, Get-NetIPAddress, nslookup, ping, etc.
- Correção Automática (somente com autorização do Diego): perfil de rede, firewall, SMB, compartilhamento, spooler, permissões, RPC, DNS, Gateway, DHCP, políticas locais.

Documentação Obrigatória:
Após qualquer atendimento, gere um Relatório Técnico contendo: Data, Cliente, Local, Equipamentos, Topologia, Diagnóstico, Testes realizados, Comandos executados, Resultados, Problema encontrado, Causa raiz, Solução aplicada, Pendências, Recomendações, Tempo gasto, Fotos e Scripts utilizados.

Segurança Rígida:
NUNCA alterar Active Directory, VLAN, Firewall, DHCP, DNS, Gateway, Switches, Mikrotik sem autorização explícita do Diego.
"""

def workflow_redeshare():
    code = r'''
const body = $json.body || $json;
const msg = String(body.mensagem || body.message || body.text || "").toLowerCase();
const solicitante = body.solicitante || "Diego";

let acao = "analisar";
let ferramentas_sugeridas = [];
let diagnostico = "";

if (msg.includes("impressora") || msg.includes("spooler") || msg.includes("0x0000011b") || msg.includes("0x00000709")) {
  acao = "diagnostico_impressao";
  ferramentas_sugeridas = ["Get-Printer", "Get-Service Spooler", "printui"];
  diagnostico = "Problema relacionado a compartilhamento de impressora ou Point and Print detectado. Recomenda-se verificação de Spooler, atualizações de segurança (RPC) ou permissões SMB.";
} else if (msg.includes("pasta") || msg.includes("arquivo") || msg.includes("smb") || msg.includes("acesso negado")) {
  acao = "diagnostico_compartilhamento";
  ferramentas_sugeridas = ["Get-SmbShare", "net share", "net view"];
  diagnostico = "Problema de compartilhamento de arquivos ou SMB. Verificar permissões NTFS e compartilhamento, bem como versões SMB ativas.";
} else if (msg.includes("ip ") || msg.includes("internet") || msg.includes("dhcp") || msg.includes("dns")) {
  acao = "diagnostico_rede";
  ferramentas_sugeridas = ["ipconfig /all", "Resolve-DnsName", "ping", "tracert", "Get-NetIPAddress"];
  diagnostico = "Problema de conectividade (TCP/IP, DHCP, DNS) ou configuração de rede física/lógica.";
} else if (msg.includes("inventário") || msg.includes("inventario") || msg.includes("mapear")) {
  acao = "inventario_rede";
  ferramentas_sugeridas = ["arp -a", "Get-NetNeighbor", "Get-NetAdapter"];
  diagnostico = "Solicitação de inventário e mapeamento de rede. Requer varredura de dispositivos via ARP, WMI ou SNMP.";
} else {
  diagnostico = "Análise preliminar de infraestrutura solicitada. Aguardando diretrizes e parâmetros específicos do Diego.";
}

const relatorio_template = `
### Relatório Técnico Preliminar - DL RedeShare AI
**Solicitante:** ${solicitante}
**Diagnóstico Inicial:** ${diagnostico}
**Ferramentas Recomendadas:** ${ferramentas_sugeridas.join(', ')}

**Atenção de Segurança:** Nenhuma alteração em AD, VLAN, Firewall, DHCP, DNS, Gateway, Switches ou Mikrotik deve ser executada sem autorização explícita do Diego.
`;

return [{
  json: {
    agente: "DL RedeShare AI",
    papel: "Subagente Especialista em Infraestrutura e Redes",
    supervisor: "Diego",
    acao_requerida: acao,
    ferramentas_sugeridas: ferramentas_sugeridas,
    relatorio_preliminar: relatorio_template,
    proxima_acao: "enviar_para_revisao_diego",
    status: "diagnostico_concluido"
  }
}];
'''
    return {
        "name": "032_AGENT_REDESHARE_AI",
        "nodes": [
            {
                "parameters": {
                    "path": "agent-redeshare-ai",
                    "httpMethod": "POST",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "id": "webhook",
                "name": "Webhook RedeShare AI",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {"jsCode": code},
                "id": "code",
                "name": "RedeShare Analise de Infra",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "respond",
                "name": "Responder RedeShare",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [800, 300]
            }
        ],
        "connections": {
            "Webhook RedeShare AI": {
                "main": [[{"node": "RedeShare Analise de Infra", "type": "main", "index": 0}]]
            },
            "RedeShare Analise de Infra": {
                "main": [[{"node": "Responder RedeShare", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "REDESHARE"}, {"name": "INFRAESTRUTURA"}]
    }

def salvar_json(nome, conteudo):
    path = BASE / nome
    path.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✔️ OK JSON: {path}")

def salvar_txt(nome, conteudo):
    path = BASE / nome
    path.write_text(conteudo, encoding="utf-8")
    print(f"✔️ OK TXT: {path}")

if __name__ == "__main__":
    salvar_json("032_AGENT_REDESHARE_AI.json", workflow_redeshare())
    salvar_txt("PROMPT_REDESHARE.txt", PROMPT_REDESHARE)
    print("\n✅ Agente DL RedeShare AI criado com sucesso no ecossistema DL Nexus!")
