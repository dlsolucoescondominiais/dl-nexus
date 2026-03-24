---
name: Agente de Orçamentos
description: Gera minutas e propostas comerciais complexas integrando energia solar, CFTV, automação e elétrica para síndicos.
---

# Agente de Orçamentos (DL Consultor Técnico)

O Agente de Orçamento serve para transformar as dores e dúvidas simples de um síndico ou gestor predial em um **escopo de serviços integrado e de alto valor** da DL Soluções Condominiais LTDA.
Ele não é um simples gerador de preços. Ele estrutura a proposta focando na Redução de Custos Fixos e segurança usando IA e a Lei 14.300 de energia solar.

## Pré-requisitos
- O arquivo `.env` configurado com a `OPENAI_API_KEY`.
- Custo de infraestrutura rodando Python 3.10 ou superior.
- Acesso à API da OpenAI garantido (recomendado \`gpt-4o\`).

## Instruções Passo a Passo

O Agente de Orçamento é uma ferramenta cli que recebe uma string como argumento e retorna um markdown gerado no console.

### Como Executar:

Pelo terminal, chame o interpretador Python apontando pelo caminho correto e defina a demanda:

```powershell
python execution/agente_orcamento.py "Gostaria de colocar um sistema solar porque a luz das áreas comuns está alta."
```

## Diretrizes de Tom e Regras Frias (Internas)

1. **Nunca use "Visita Técnica".** É sempre "Avaliação Técnica" ou "Diagnóstico de Vulnerabilidade GRATUITO".
2. **Nunca minta vendendo ilusões.** Não prometa conta zerada. O Fio B e custos de disponibilidade são inegociáveis.
3. **Ofereça o Ecossistema.** Alguém pediu energia solar? Mande também o CFTV facial dizendo que a placa solar barateou o custo a longo prazo e a portaria autônoma é o próximo passo inteligente.

## Notas e Cuidados
- Caso o agente trave por "Quota Exceeded", significa que a chave da OpenAI atingiu o limite de gastos diário/mensal e os fundos precisam ser renovados.
- Se nenhuma "demanda" for enviada, o script processará uma string de fallback hardcoded apenas para teste se a API está funcionando.
