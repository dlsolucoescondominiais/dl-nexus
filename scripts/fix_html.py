import sys

with open(r'd:\AntiGravity\projeto_01\LP_ORCAMENTO_INTERNO\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        { id: "gr_defeito", label: "Peças a Trocar (Selecione todas)", type: "checkbox-group", options: [
            "Contatora", "Resistência inferior", "Resistência superior",
            "Termostato", "Botão liga/desliga", "Botão Chave Gangorra (Paca Paca)",
            "Display", "Seletora", "Suspensão de chapa",
            "PVC de proteção (Cilipaque)", "Placa eletrônica",
            "Chicote interno", "Chicote de entrada 127/220", "Chicote de entrada 220/380",
            "Gaveta coletora", "Pé nivelador",
            "Não sei / Diagnóstico necessário"
        ], req: false }"""

replacement = """        { id: "gr_defeito_chapa", label: "Peças a Trocar — CHAPAS (Selecione todas)", type: "checkbox-group", options: [
            "Contatora", "Resistência inferior", "Resistência superior",
            "Termostato", "Botão liga/desliga", "Botão Chave Gangorra (Paca Paca)",
            "Display", "Seletora", "Suspensão de chapa",
            "PVC de proteção (Cilipaque)", "Placa eletrônica",
            "Chicote elétrico", "Não sei / Diagnóstico necessário"
        ], req: false },
        { id: "gr_defeito_frit", label: "Peças a Trocar — FRITADEIRAS (Selecione todas)", type: "checkbox-group", options: [
            "Contatora", "Resistência", "Termostato", "Termostato de Segurança",
            "Botão liga/desliga", "Cesta de Fritura", "Cuba de Óleo", "Lâmpada Piloto",
            "Placa eletrônica", "Chicote elétrico", "Não sei / Diagnóstico necessário"
        ], req: false }"""

new_content = content.replace(target, replacement)

with open(r'd:\AntiGravity\projeto_01\LP_ORCAMENTO_INTERNO\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
