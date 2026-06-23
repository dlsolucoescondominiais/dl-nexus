# Template Google Docs — Proposta Comercial DL

**Data:** 2026-06-21
**Objetivo:** Definir o modelo do Google Docs que será preenchido automaticamente pelo workflow `065` e exportado como PDF para envio ao cliente.

---

## 1. Nome do Template

**`[DL Nexus] Template Proposta Comercial v1`**

---

## 2. Estrutura do Documento

O template usa **placeholders** `{{campo}}` que o n8n substitui antes de exportar o PDF.

---

### CAPA

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║        DL SOLUÇÕES CONDOMINIAIS LTDA                ║
║        CNPJ: XX.XXX.XXX/0001-XX                     ║
║                                                      ║
║        PROPOSTA COMERCIAL                            ║
║        {{servico_interesse}}                         ║
║                                                      ║
║        Protocolo: {{protocolo}}                      ║
║        Data: {{data}}                                ║
║        Versão: {{versao}}                            ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

### SEÇÃO 1: IDENTIFICAÇÃO DO CLIENTE

```
Cliente: {{nome_empresa_ou_condominio}}
Responsável: {{nome}}
Contato: {{whatsapp}} | {{email}}
Endereço: {{endereco_completo}}, {{bairro}} — {{cidade}}
Perfil: {{tipo_cliente_extenso}}
```

Se `tipo_cliente = condominio`:
```
Unidades: {{numero_unidades}}
Blocos: {{numero_blocos}}
Síndico/Aprovador: {{responsavel_aprovacao}}
```

---

### SEÇÃO 2: ESCOPO TÉCNICO

```
Serviço: {{servico_interesse}}
Tipo de Orçamento: {{tipo_orcamento}}
Urgência: {{urgencia_extenso}}

Descrição da Necessidade:
{{descricao}}
```

Se houver mídia anexada:
```
⚠️ Evidências visuais foram recebidas e analisadas preliminarmente.
As imagens e vídeos são tratados como evidência visual, não como
confirmação técnica definitiva. Uma Avaliação Técnica presencial
poderá ser necessária para validação.
```

---

### SEÇÃO 3: COMPOSIÇÃO DE VALORES

```
┌─────────────────────────────┬────────────────┐
│ Item                        │ Valor (R$)     │
├─────────────────────────────┼────────────────┤
│ Materiais e Equipamentos    │ {{material}}   │
│ Mão de Obra                 │ {{mao_obra}}   │
│ Deslocamento                │ {{desloc}}     │
│ Serviços de Terceiros       │ {{terceiros}}  │
├─────────────────────────────┼────────────────┤
│ TOTAL                       │ {{total}}      │
└─────────────────────────────┴────────────────┘
```

Se `rateio_permitido = true`:
```
Valor por unidade (rateio): R$ {{rateio_unidade}}
(Baseado em {{numero_unidades}} unidades)
```

Se `rateio_permitido = false` e `tipo_cliente = condominio`:
```
⚠️ Dados insuficientes para confirmação definitiva do rateio por unidade.
O número de unidades não foi informado.
```

---

### SEÇÃO 4: CONDIÇÕES COMERCIAIS

```
Validade desta proposta: 15 dias corridos a partir da data de emissão.
Prazo estimado de execução: {{prazo_execucao}}
Forma de pagamento: A combinar.
Garantia: {{garantia}}
```

---

### SEÇÃO 5: CLÁUSULA DE CONFIDENCIALIDADE

```
As informações contidas neste documento, incluindo valores,
especificações técnicas, escopo e condições comerciais, são de uso
exclusivo do destinatário. É proibida a divulgação, reprodução ou
compartilhamento total ou parcial deste documento com terceiros,
sob pena de responsabilização civil nos termos da legislação vigente.

As soluções técnicas apresentadas são propriedade intelectual da
DL Soluções Condominiais LTDA e não podem ser replicadas ou
adaptadas sem autorização expressa.
```

---

### RODAPÉ

```
DL Soluções Condominiais LTDA
contato@dlsolucoescondominiais.com.br
(21) 96878-2196
dlsolucoescondominiais.com.br
```

---

## 3. Placeholders Completos

| Placeholder | Fonte |
|---|---|
| `{{protocolo}}` | Gerado pelo 060 |
| `{{data}}` | Data de geração |
| `{{versao}}` | Versão do orçamento (1, 2, 3...) |
| `{{nome}}` | Lead |
| `{{nome_empresa_ou_condominio}}` | Lead |
| `{{whatsapp}}` | Lead |
| `{{email}}` | Lead |
| `{{endereco_completo}}` | Localização |
| `{{bairro}}` | Localização |
| `{{cidade}}` | Localização |
| `{{tipo_cliente_extenso}}` | "Condomínio Residencial", "Pessoa Física", etc. |
| `{{numero_unidades}}` | Infraestrutura |
| `{{numero_blocos}}` | Infraestrutura |
| `{{responsavel_aprovacao}}` | Lead |
| `{{servico_interesse}}` | Demanda |
| `{{tipo_orcamento}}` | Demanda |
| `{{urgencia_extenso}}` | "Baixa (Planejamento)", "Média", "Alta (Emergência)" |
| `{{descricao}}` | Demanda |
| `{{material}}` | Google Sheets (coluna J) |
| `{{mao_obra}}` | Google Sheets (coluna K) |
| `{{desloc}}` | Google Sheets (coluna L) |
| `{{terceiros}}` | Google Sheets (coluna M) |
| `{{total}}` | Google Sheets (coluna N) |
| `{{rateio_unidade}}` | Google Sheets (coluna Q) |
| `{{prazo_execucao}}` | Manual ou estimado |
| `{{garantia}}` | Por tipo de serviço |

---

## 4. Fluxo de Geração

1. `065_ORCAMENTO_GOOGLE_DOCS_PDF_DL` duplica o template no Google Drive.
2. Substitui todos os `{{placeholders}}` pelos valores reais via Google Docs API.
3. Exporta como PDF.
4. Salva o PDF no Google Drive (pasta `Orçamentos/{{ano}}/{{mes}}/`).
5. Registra o link do PDF no Supabase e no Google Sheets.
6. A versão gerada é **congelada**: não editável. Qualquer alteração = nova versão.
