# Modelo Google Sheets — Planilha Operacional de Orçamentos DL

**Data:** 2026-06-21
**Objetivo:** Definir a estrutura da planilha Google Sheets que Diogo e Nielton usarão no dia a dia para orçar, ajustar valores e acompanhar status.

---

## 1. Nome da Planilha

**`[DL Nexus] Orçamentos Operacionais`**

---

## 2. Abas da Planilha

### Aba 1: `Orçamentos`
Cada linha = 1 orçamento. Preenchida automaticamente pelo workflow `062` e editável manualmente.

| Coluna | Tipo | Preenchido por | Descrição |
|---|---|---|---|
| A — Protocolo | Texto | n8n (auto) | Ex: `ORC-V2-ABC123` |
| B — Data | Data | n8n (auto) | Data de entrada |
| C — Cliente | Texto | n8n (auto) | Nome do solicitante |
| D — Empresa/Condomínio | Texto | n8n (auto) | Nome do empreendimento |
| E — Perfil | Texto | n8n (auto) | condomínio, pessoa_fisica, restaurante... |
| F — Serviço | Texto | n8n (auto) | DL Guardião, Energia Solar, Mult•Grill... |
| G — Bairro | Texto | n8n (auto) | Bairro do cliente |
| H — Urgência | Texto | n8n (auto) | baixa, media, alta |
| I — Unidades | Número | n8n ou manual | Número de unidades (condomínio) |
| J — Material (R$) | Moeda | **Diogo/Nielton** | Custo total de materiais |
| K — Mão de Obra (R$) | Moeda | **Diogo/Nielton** | Custo total de mão de obra |
| L — Deslocamento (R$) | Moeda | **Diogo/Nielton** | Custo de deslocamento |
| M — Terceiros (R$) | Moeda | **Diogo/Nielton** | Custo de terceiros |
| N — Custo Total (R$) | Fórmula | Auto | `=J+K+L+M` |
| O — Margem (%) | Número | **Diogo/Nielton** | Ex: 35% |
| P — Preço Final (R$) | Fórmula | Auto | `=N*(1+O)` |
| Q — Rateio/Unidade (R$) | Fórmula | Auto | `=SE(I>0; P/I; "N/A")` |
| R — Status | Dropdown | **Diogo/Nielton** | rascunho, enviado, ganho, perdido, em negociação |
| S — Versão | Número | n8n (auto) | 1, 2, 3... |
| T — Observações | Texto | **Diogo/Nielton** | Notas livres |
| U — Link PDF | URL | n8n (auto) | Link do Google Drive |

### Aba 2: `Tabela de Preços`
Referência de custos unitários usada pelas fórmulas e pelo n8n.

| Coluna | Descrição |
|---|---|
| A — Item | Ex: "Câmera Bullet 2MP", "Disjuntor 32A" |
| B — Categoria | Ex: CFTV, Elétrica, Solar, Mult•Grill |
| C — Unidade | un, m, m², kit |
| D — Custo Unitário (R$) | Preço de compra |
| E — Preço Venda (R$) | Preço cobrado do cliente |
| F — Fornecedor | Nome do fornecedor |
| G — Última Atualização | Data |

### Aba 3: `Mão de Obra`
Tabela de custo homem/hora por tipo de serviço e região.

| Coluna | Descrição |
|---|---|
| A — Tipo de Serviço | Elétrica, CFTV, Solar, Grill |
| B — Região | Zona Sul, Zona Norte, Barra, Niterói |
| C — Custo/Hora (R$) | Valor base |
| D — Multiplicador Urgência | Normal=1.0, Urgência=1.5, Emergência=2.5 |

### Aba 4: `Deslocamento`
Custo de deslocamento por região.

| Coluna | Descrição |
|---|---|
| A — Região | Bairro ou zona |
| B — Distância (km) | Distância estimada da base DL |
| C — Custo Base (R$) | Valor de deslocamento |

---

## 3. Integração com n8n

O workflow `062_ORCAMENTO_PLANILHA_GOOGLE_SHEETS_DL` usará a API do Google Sheets para:
1. **Append Row**: Criar nova linha na aba `Orçamentos` com dados do lead.
2. **Read Range**: Consultar `Tabela de Preços` e `Mão de Obra` para pré-calcular custos.
3. **Update Cell**: Atualizar `Status`, `Link PDF` e `Versão` após envio.

Credencial necessária: Google Sheets API (já existente no n8n como `Google Sheets DL`).

---

## 4. Regras de Uso

- Diogo e Nielton **editam diretamente** as colunas J a Q (custos e margem).
- O n8n **nunca sobrescreve** valores já preenchidos por humanos.
- Ao enviar orçamento, a linha é marcada como `enviado` e a versão incrementa.
- Se Diogo quiser alterar um orçamento já enviado, deve duplicar a linha e incrementar a versão.
