# Relatório de Teste: Aninha Telegram (Fase 2 - Refatorada)
## STATUS: Supabase Online

### Teste 1
**Entrada:** `Agendar uma Avaliação Técnica para o sistema de bombas do condomínio`
- **Status HTTP:** 200
- **Intenção Atual:** agendamento
- **Etapa do Funil:** coletando_dados_tecnicos
- **Lead Qualificado:** False
- **Bloquear:** False
**Resposta da Aninha:**
> Recebi sua mensagem. Para seguir com a Avaliação Técnica, me informe o nome do condomínio, bairro e o problema principal identificado.

- **Conclusão:** APROVADO

### Teste 2
**Entrada:** `São duas bombas. O painel está desarmando. Fica na Barra da Tijuca.`
- **Status HTTP:** 200
- **Intenção Atual:** agendamento
- **Etapa do Funil:** coletando_dados_condominio
- **Lead Qualificado:** False
- **Bloquear:** False
**Resposta da Aninha:**
> Perfeito. Entendi: são duas bombas, com painel desarmando, na Barra da Tijuca. Para avançar com a Avaliação Técnica, me informe o nome do condomínio, nome do responsável e melhor horário para atendimento.

- **Conclusão:** APROVADO

### Teste 3
**Entrada:** `Condomínio Solar da Barra, responsável Diogo, pode ser amanhã de manhã.`
- **Status HTTP:** 200
- **Intenção Atual:** agendamento
- **Etapa do Funil:** aguardando_agendamento
- **Lead Qualificado:** True
- **Bloquear:** False
**Resposta da Aninha:**
> Ótimo! Agendei a Avaliação Técnica para o Condomínio Solar da Barra com o responsável Diogo para amanhã de manhã. O nosso Tecnólogo entrará em contato em breve.

- **Conclusão:** APROVADO

### Teste 4
**Entrada:** `Quero trocar o disjuntor do meu apartamento.`
- **Status HTTP:** 200
- **Intenção Atual:** residencial_bloqueado
- **Etapa do Funil:** bloqueado_residencial
- **Lead Qualificado:** False
- **Bloquear:** True
**Resposta da Aninha:**
> No momento, a DL Soluções Condominiais atende demandas técnicas voltadas a condomínios, escolas, empresas e suporte a equipamentos profissionais. Para esse tipo de solicitação residencial avulsa, não conseguimos seguir com atendimento.

- **Conclusão:** APROVADO

### Teste 5
**Entrada:** `Quanto custa para arrumar uma bomba?`
- **Status HTTP:** 200
- **Intenção Atual:** orcamento
- **Etapa do Funil:** coletando_dados_condominio
- **Lead Qualificado:** False
- **Bloquear:** False
**Resposta da Aninha:**
> Não consigo informar um preço exato sem entender a infraestrutura atual. Para enviarmos um orçamento preciso, precisamos realizar uma Avaliação Técnica. Qual o nome do seu condomínio ou empresa?

- **Conclusão:** APROVADO
