# CHECKLIST KILLCRITIC — MOTOR SOLAR E BACKUP ECOVOLT (DL NEXUS)

Este checklist define os critérios de conformidade técnica, lógica e editorial obrigatórios para orçamentos de sistemas híbridos solares e backup com baterias. Nenhuma proposta comercial preliminar ou final pode ser emitida ao cliente se houver itens pendentes neste checklist.

---

## NÍVEL 1: Validação de Campos e Regex (Sintaxe Básica)

### Campos Obrigatórios de Entrada
- [ ] **Dados de Identificação:** Nome, tipo de cliente, responsável, WhatsApp, e-mail, endereço, bairro e cidade preenchidos.
- [ ] **Dados Elétricos Básicos:** Tensão de atendimento (V) e tipo de ligação (mono, bi, trifásico) informados.
- [ ] **Dados de Instalação e Padrão:** Tipo de telhado/laje, disjuntor geral (A) e padrão de entrada preenchidos.
- [ ] **Dados da Conta:** Consumo mensal em kWh, valor médio da conta e concessionária informados.
- [ ] **Dados de Backup:** Autonomia de backup solicitada (horas) e lista de cargas críticas preenchida.

### Padrão de Identificadores (RegEx)
- [ ] Protocolo segue o formato estrito: `^ECO-[0-9]{8}-[0-9]{4}$` (ex: `ECO-20260624-0001`).

---

## NÍVEL 2: Validação Técnica e Lógica dos Cálculos

### Dimensionamento do Banco de Baterias (Backup)
- [ ] **Energia Crítica Diária ($E_{critica}$):** Calculada deterministicamente via $kWh = \sum (kW \times horas \times qtd)$.
- [ ] **Bateria Nominal Mínima ($B_{nominal}$):** Calculada dividindo a energia crítica pela eficiência ($0.85$) e profundidade de descarga ($0.80$, DoD máximo para LFP).
- [ ] **Margem de Segurança:** Adicionada margem de segurança técnica entre 20% e 30% à capacidade nominal ($B_{nominal} \times (1 + margem)$).
- [ ] **Capacidade de Descarga:** Potência de pico e contínua do banco de baterias suporta a corrente máxima exigida pelo inversor na simultaneidade.

### Dimensionamento do Inversor Híbrido
- [ ] **Potência Simultânea:** Soma das cargas críticas que operam simultaneamente calculada.
- [ ] **Potência Mínima do Inversor:** Potência simultânea multiplicada pela margem técnica de segurança (mínimo 20%).
- [ ] **Bloqueio de Motores Sem Dados:** Se houver motores (elevador, bomba de recalque, bomba de incêndio, ar-condicionado > 18.000 BTUs, compressor, etc.), o sistema **BLOQUEIA** o dimensionamento automático. O status deve passar para `dados_insuficientes` até a realização de Avaliação Técnica presencial ou envio do manual técnico da partida do motor.
- [ ] **Restrição Absoluta de Elevadores:** Elevadores condominiais estão **bloqueados** de dimensionamento preliminar em backup comum. Requer estudo específico de partida, quadro dedicado e viabilidade de engenharia.

### Dimensionamento Fotovoltaico (Solar)
- [ ] **Arranjo Fotovoltaico Preliminar:** Potência em kWp calculada dividindo o consumo mensal (kWh) pela geração média regional (conforme tabela local).
- [ ] **Tabela de Geração Regional:** O dimensionamento fotovoltaico por kWp utiliza tabelas fixas de irradiação média (ex: Rio de Janeiro = 115 kWh/kWp/mês), e não chutes da IA.

### Equipamentos SolaXPower e Baterias Triple Power (Corsolar)
- [ ] **Custo e Preços no Banco:** Os equipamentos importados da tabela `dl_solar_equipamentos` possuem `custo = null` ou `estimado_validar`, `status = pendente_validacao` e `fornecedor = Corsolar`. Não são utilizados preços fictícios ou inventados.
- [ ] **Compatibilidade:** O inversor sugerido é compatível com a tensão de atendimento da rede (ex: inversores trifásicos SolaX X3 apenas para redes trifásicas).

---

## NÍVEL 3: Revisão Textual e Conformidade Comercial

### Terminologia Padrão
- [ ] **Termo Obrigatório:** Não usa a expressão "visita técnica"; substitui integralmente por **"Avaliação Técnica"**.
- [ ] **Nomes Internos Bloqueados:** Proposta do cliente não cita termos internos como "n8n", "DeepSeek", "Supabase", "B2B" ou "workflow".

### Restrições Editoriais e Comerciais (Bloqueio de Promessas)
- [ ] **Sem Promessas de Economia:** Não promete "economia garantida" ou "redução fixa de X%". Substitui por: *"estimativa de redução de consumo da rede, sujeita à análise da conta, irradiação, perfil de consumo, homologação, tarifas e condições locais."*
- [ ] **Sem Promessas de Backup Total:** Não usa termos como "backup total", "nunca ficará sem energia", "100% autônomo" ou "funciona qualquer carga".
- [ ] **Sem Preço Fechado Sem Avaliação:** O documento comercial deixa explícito que o valor é um pré-dimensionamento preliminar sujeito a alterações após Avaliação Técnica presencial.
- [ ] **Sem Termos Promocionais:** Bloqueia palavras como "grátis", "gratuito", "desconto", "promoção", "desconto especial".

### Observação Técnica Obrigatória
- [ ] A proposta do cliente exibe a seguinte observação de segurança em destaque:
  > **[!IMPORTANT]**
  > **Dimensionamento preliminar sujeito à Avaliação Técnica, análise da conta de energia, confirmação das cargas críticas, tensão de atendimento, local de instalação e compatibilidade dos equipamentos.**

---

## CONFORMIDADE DE INFRAESTRUTURA E SEGURANÇA (RLS & POLICIES)
- [ ] **Row Level Security (RLS):** Ativa em todas as tabelas (`dl_solar_*`).
- [ ] **Políticas n8n:** Criadas policies do tipo `service_full_access` para garantir que a chave `service_role` utilizada no n8n Cloud possua permissão total de INSERT/UPDATE/SELECT sem bloqueios inesperados.
- [ ] **Higienização de Código:** O arquivo `migration_dl_solar_backup_orcamentos.sql` é idempotente (`CREATE TABLE IF NOT EXISTS`), sem cláusulas destrutivas (`DROP`, `TRUNCATE`).
- [ ] **Nenhum Segredo:** O versionamento do código não contém tokens, credenciais ou strings `.env`.
