import os
import requests

output_dir = r"d:\AntiGravity\projeto_01\Manuais_Equipamentos"
os.makedirs(output_dir, exist_ok=True)

manuals = [
    {
        "brand": "Tedesco",
        "name": "Manual Forno Turbo FTT",
        "url": "https://tedesco.ind.br/uploads/produtos/manuais/manual_forno_turbo_2022.pdf",
        "filename": "Tedesco_Manual_Forno_Turbo.pdf",
        "description": "Manual de instruções e segurança para Forno Turbo FTT."
    },
    {
        "brand": "Venâncio",
        "name": "Manual Forno Convector",
        "url": "https://venanciometal.com.br/arquivos/manuais/FORNO-CONVECTOR.pdf", 
        "filename": "Venancio_Forno_Convector.pdf",
        "description": "Manual do Forno Convector Venâncio."
    },
    {
        "brand": "Croydon",
        "name": "Manual Fritadeira FAM5",
        "url": "https://croydon.com.br/wp-content/uploads/2021/05/FAM5-manual.pdf",
        "filename": "Croydon_Fritadeira_FAM5.pdf",
        "description": "Manual de instruções da Fritadeira Croydon FAM5."
    },
    {
        "brand": "Metvisa",
        "name": "Manual Liquidificador de Baixa Rotação",
        "url": "https://metvisa.com.br/wp-content/uploads/2021/06/manual-liquidificador-baixa-rotacao.pdf",
        "filename": "Metvisa_Liquidificador.pdf",
        "description": "Manual do Liquidificador Metvisa (Baixa Rotação)."
    },
    {
        "brand": "MultGrill",
        "name": "Catálogo Geral / Manuais (Busca genérica)",
        "url": "https://multgrill.com.br/wp-content/uploads/2021/01/Catalogo-Mult-Grill-2021.pdf",
        "filename": "MultGrill_Catalogo_Manuais.pdf",
        "description": "Catálogo com especificações técnicas dos equipamentos MultGrill."
    }
]

index_lines = ["# Índice de Manuais de Equipamentos\n\n"]
index_lines.append("Este diretório contém os manuais, esquemas elétricos e catálogos dos equipamentos das marcas MultGrill, Croydon, Venâncio, Metvisa e Tedesco.\n\n")

print(f"Iniciando downloads na pasta: {output_dir}")

for m in manuals:
    try:
        print(f"Baixando {m['name']} ({m['brand']})...")
        response = requests.get(m['url'], timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code == 200:
            filepath = os.path.join(output_dir, m['filename'])
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            index_lines.append(f"### {m['brand']}\n")
            index_lines.append(f"- **Documento:** [{m['name']}]({m['filename']})\n")
            index_lines.append(f"- **Descrição:** {m['description']}\n")
            index_lines.append(f"- **Fonte Original:** [Link]({m['url']})\n\n")
            print(f"Sucesso: {m['filename']}")
        else:
            print(f"Erro HTTP {response.status_code} ao baixar {m['name']}")
            index_lines.append(f"### {m['brand']}\n- **{m['name']}**: Falha ao baixar (HTTP {response.status_code}) - [Tente baixar manualmente]({m['url']})\n\n")
    except Exception as e:
        print(f"Erro interno ao baixar {m['name']}: {e}")
        index_lines.append(f"### {m['brand']}\n- **{m['name']}**: Erro na conexão - [Tente baixar manualmente]({m['url']})\n\n")

index_path = os.path.join(output_dir, "INDEX.md")
with open(index_path, "w", encoding="utf-8") as f:
    f.writelines(index_lines)

print(f"Processo concluído. Índice gerado em: {index_path}")
