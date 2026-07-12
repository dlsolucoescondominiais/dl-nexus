ORDEM TÉCNICA — CRIAÇÃO DOS AGENTES AUTÔNOMOS DL NEXUS

OBJETIVO

Criar dois agentes permanentes dentro do n8n para desenvolver, manter, revisar e melhorar continuamente o ecossistema DL Nexus.

Os agentes devem trabalhar sobre os workflows, integrações, APIs, portfólio e regras comerciais que já existem.

O objetivo não é reconstruir o projeto do zero.

O objetivo é aproveitar os mais de 60 workflows já existentes, corrigir gargalos, reutilizar estruturas válidas e manter o DL Nexus funcionando sem exigir que Diogo entre diariamente no n8n para ajustar manualmente cada problema.

---

1. AGENTES A CRIAR

Criar dois agentes complementares:

DL_NEXUS_GPT_ENGINEER
DL_NEXUS_GEMINI_AUDITOR

Os dois agentes devem operar dentro do n8n e compartilhar memória, logs, eventos, documentação e histórico de alterações.

---

2. AGENTE 1 — DL_NEXUS_GPT_ENGINEER

FUNÇÃO

O "DL_NEXUS_GPT_ENGINEER" será o agente principal de engenharia, manutenção e evolução do DL Nexus.

Ele utilizará a API da OpenAI.

Ele deverá possuir memória persistente no Supabase.

RESPONSABILIDADES

- analisar workflows existentes;
- identificar falhas;
- identificar nodes quebrados;
- identificar credenciais ausentes;
- identificar variáveis de ambiente ausentes;
- identificar webhooks incorretos;
- identificar workflows inativos;
- identificar erros de integração;
- identificar duplicidades;
- identificar referências quebradas;
- corrigir expressões n8n;
- corrigir IDs de subworkflows;
- corrigir estruturas JSON;
- propor e aplicar patches;
- reaproveitar workflows existentes;
- criar novos subworkflows apenas quando não existir estrutura reutilizável;
- documentar alterações;
- registrar histórico;
- acompanhar execuções;
- revisar logs;
- abrir incidentes;
- executar testes controlados;
- atualizar documentação técnica.

MEMÓRIA

Salvar em Supabase:

workflow analisado
problema encontrado
causa raiz
correção aplicada
resultado do teste
versão anterior
versão nova
dependências
decisão técnica
data da alteração

Tabela sugerida:

CREATE TABLE IF NOT EXISTS dl_nexus_agent_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_name TEXT NOT NULL,
  workflow_name TEXT,
  workflow_id TEXT,
  execution_id TEXT,
  action_type TEXT NOT NULL,
  problem_description TEXT,
  root_cause TEXT,
  solution_applied TEXT,
  previous_version JSONB,
  new_version JSONB,
  test_result JSONB,
  dependencies JSONB,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

---

3. AGENTE 2 — DL_NEXUS_GEMINI_AUDITOR

FUNÇÃO

O "DL_NEXUS_GEMINI_AUDITOR" será o agente de auditoria, validação, revisão e fiscalização do trabalho executado pelo agente GPT.

Ele utilizará a API do Gemini.

Ele não deverá duplicar o trabalho do agente GPT.

Sua responsabilidade será verificar se a correção aplicada realmente resolveu o problema e não criou outro.

RESPONSABILIDADES

- revisar patches;
- comparar versões;
- validar regras comerciais;
- validar escopo técnico da DL;
- validar coerência dos workflows;
- validar publicação;
- validar conteúdo;
- validar identidade visual e textual;
- identificar falso sucesso;
- identificar falha silenciosa;
- monitorar ausência de execexecuções;
- monitorar ausência de postagens;
- monitorar tokens expirados;
- monitorar APIs indisponíveis;
- monitorar filas paradas;
- monitorar workflows inativos;
- verificar dependências;
- aplicar KILLCRITIC;
- aprovar ou reprovar alterações;
- alertar via Telegram;
- enviar correção de volta ao agente GPT.

REGRA DE APROVAÇÃO

Nenhuma alteração deverá ser considerada concluída apenas porque o workflow executou sem erro.

O Gemini Auditor deverá validar o resultado funcional.

Exemplos:

Facebook

Somente aprovar quando existir:

post_id
objeto recuperável
permalink quando disponível
registro no Supabase

Instagram

Somente aprovar quando existir:

creation_id
status do container = FINISHED
media_id
permalink
registro no Supabase

Conteúdo

Somente aprovar quando:

- estiver alinhado ao portfólio;
- estiver dentro do escopo técnico;
- não inventar serviços;
- não mencionar Condify;
- não vender AVCB;
- não vender serviços hidráulicos;
- não vender manutenção mecânica de bombas;
- utilizar corretamente as linhas DL;
- possuir CTA;
- possuir público correto;
- possuir imagem coerente;
- não repetir conteúdo recente.

---

4. FLUXO DE TRABALHO DOS AGENTES

Problema detectado
↓
DL_NEXUS_GEMINI_AUDITOR identifica a anomalia
↓
Registra incidente no Supabase
↓
Envia tarefa para DL_NEXUS_GPT_ENGINEER
↓
GPT analisa workflow e dependências
↓
GPT gera patch ou correção
↓
Correção aplicada em ambiente controlado
↓
Teste executado
↓
Gemini revisa o resultado
↓
Aprovado?
├── SIM → versionar, registrar e liberar
└── NÃO → devolver para nova correção

---

5. MONITORAMENTO PERMANENTE

Os agentes devem monitorar continuamente:

- última postagem no Facebook;
- última postagem no Instagram;
- quantidade de postagens no dia;
- última execução da máquina de conteúdo;
- fila de conteúdo;
- fila de imagens;
- containers Instagram;
- tokens Meta;
- credenciais;
- Google Drive;
- Supabase;
- Gemini;
- OpenAI;
- Telegram;
- n8n;
- webhooks;
- subworkflows;
- erros consecutivos;
- workflows inativos;
- agendamentos parados.

ALERTAS OBRIGATÓRIOS

Alertar via Telegram quando:

- nenhuma postagem ocorrer por mais de 6 horas;
- menos de 3 postagens forem publicadas no dia;
- nenhuma execução da máquina de conteúdo ocorrer;
- Facebook falhar;
- Instagram falhar;
- imagem não estiver pública;
- token expirar;
- container ficar preso;
- fila ficar parada;
- workflow ficar inativo;
- credencial estiver ausente;
- API retornar 401, 403, 429 ou 5xx;
- Supabase estiver pausado;
- conteúdo for bloqueado três vezes seguidas;
- houver divergência entre conteúdo gerado e conteúdo publicado.

---

6. MISSÃO COMERCIAL DA MÁQUINA DE CONTEÚDO

A máquina de conteúdo deverá publicar diariamente sobre as linhas reais da DL.

Não publicar posts genéricos sobre “tecnologia”.

Cada postagem deverá estar vinculada a uma linha específica do portfólio.

LINHAS DL

DL Aqua

Escopo correto:

- automação elétrica de sistemas de bombeamento;
- painéis de comando;
- sensores de nível;
- boias elétricas;
- controle entre cisterna e reservatório superior;
- alternância automática entre bombas;
- proteção elétrica de motores;
- monitoramento de falhas;
- automação do sistema de recalque.

Nunca divulgar:

- manutenção mecânica de bomba;
- conserto de bomba;
- serviço hidráulico;
- tubulação;
- vazamento;
- encanamento;
- limpeza de cisterna.

DL Volt

- instalações elétricas;
- quadros elétricos;
- comandos;
- proteção elétrica;
- DR;
- DPS;
- aterramento;
- automação elétrica;
- modernização elétrica;
- eficiência energética.

DL VoltCharge

- carregadores para veículos elétricos;
- infraestrutura elétrica;
- proteção;
- balanceamento de carga;
- medição;
- controle de acesso ao carregador;
- gestão de consumo;
- condomínios e empresas.

DL EcoVolt

- energia solar;
- painéis fotovoltaicos;
- inversores;
- backup;
- baterias;
- redução da conta de energia;
- monitoramento;
- eficiência energética.

Não confundir DL EcoVolt com painéis elétricos comuns.

DL Alerta

Somente sistemas eletrônicos:

- detectores de fumaça;
- detectores de calor;
- acionadores manuais;
- sirenes;
- centrais de alarme;
- módulos;
- monitoramento;
- integração eletrônica.

Nunca divulgar:

- emissão de AVCB;
- licença do Corpo de Bombeiros;
- projeto legal;
- aprovação;
- consultoria de licenciamento.

DL Fortress

- controle de acesso;
- reconhecimento facial;
- biometria;
- QR Code;
- tags;
- fechaduras eletrônicas;
- intertravamento;
- portaria autônoma;
- integração de sistemas eletrônicos.

Nunca mencionar Condify.

DL Guardião

- CFTV;
- câmeras;
- gravação;
- monitoramento;
- visualização remota;
- análise de vídeo;
- proteção de áreas comuns;
- integração com controle de acesso.

DL Partner

- contrato de manutenção;
- acompanhamento preventivo;
- suporte;
- inspeções;
- redução de chamados emergenciais;
- continuidade operacional;
- manutenção dos sistemas atendidos pela DL.

Gatekeeper

- automação de portões;
- controle veicular;
- comandos;
- segurança de acesso;
- integração com sistemas eletrônicos.

Mult•Grill Express

- manutenção de chapas;
- manutenção de grills;
- manutenção de fritadeiras;
- equipamentos de cozinhas comerciais.

---

7. ESTRATÉGIA DIÁRIA DE POSTAGEM

A máquina não deverá publicar uma linha diferente a cada post de forma aleatória e confusa.

Cada dia deverá possuir um tema principal e um tema secundário.

EXEMPLO DE ROTAÇÃO

Dia 1

Tema principal: DL Aqua
Tema secundário: DL Volt

Publicações:

1. automação entre cisterna e reservatório;
2. painel de comando;
3. falha de sensor de nível;
4. proteção elétrica do sistema;
5. integração DL Aqua + DL Volt.

Dia 2

Tema principal: DL Volt
Tema secundário: DL VoltCharge

Publicações:

1. quadro elétrico antigo;
2. proteção por DR e DPS;
3. automação elétrica;
4. carregador veicular;
5. preparação do condomínio para veículos elétricos.

Dia 3

Tema principal: DL Alerta
Tema secundário: DL EcoVolt

Publicações:

1. detector de fumaça;
2. detector de calor;
3. central de alarme;
4. redução da conta de energia;
5. backup para áreas críticas.

Dia 4

Tema principal: DL Fortress
Tema secundário: DL Guardião

Publicações:

1. controle facial;
2. controle por tags;
3. intertravamento;
4. CFTV;
5. integração de câmeras com controle de acesso.

Dia 5

Tema principal: DL Partner
Tema secundário: linha com melhor desempenho da semana

---

8. QUANTIDADE DE PUBLICAÇÕES

Meta inicial:

4 a 6 publicações por dia

Distribuição:

- Facebook;
- Instagram Feed;
- Stories;
- Google Business, quando o publicador estiver homologado.

Os horários devem variar dentro das janelas configuradas.

Não publicar todas de uma vez.

Exemplo de janelas:

07:00–09:00
10:00–12:00
13:00–15:00
16:00–18:00
19:00–21:00

---

9. FORMATO DO CONTEÚDO

Cada postagem deve conter:

- linha DL;
- tema;
- público;
- dor;
- consequência;
- solução;
- benefício;
- CTA;
- hashtags;
- texto alternativo;
- imagem relacionada;
- identificador único;
- hash para evitar repetição.

PÚBLICO PRINCIPAL

- condomínios pequenos;
- condomínios médios;
- condomínios econômicos;
- condomínios tradicionais;
- condomínios antigos;
- síndicos moradores;
- síndicos profissionais;
- administradoras;
- empresas;
- escolas;
- comércios.

Nunca posicionar a DL como empresa exclusiva para alto padrão.

---

10. APRENDIZADO COM RESULTADOS

Registrar para cada postagem:

- linha DL;
- tema;
- formato;
- rede;
- horário;
- alcance;
- impressões;
- curtidas;
- comentários;
- compartilhamentos;
- salvamentos;
- cliques;
- mensagens;
- leads;
- solicitações de orçamento;
- contratos originados.

O agente Gemini deverá analisar semanalmente quais conteúdos tiveram melhor desempenho.

O agente GPT deverá utilizar os resultados para:

- gerar variações;
- reutilizar temas vencedores;
- trocar imagens;
- alterar ganchos;
- alterar CTAs;
- melhorar frequência;
- abandonar temas fracos;
- reforçar temas que geram mensagens.

Não copiar exatamente a mesma postagem.

Gerar novas versões do tema vencedor.

---

11. MANUTENÇÃO DOS WORKFLOWS

Os agentes devem utilizar como base os workflows existentes no n8n e no GitHub.

Antes de criar qualquer workflow novo:

1. procurar funcionalidade existente;
2. verificar se há workflow equivalente;
3. verificar se pode ser corrigido;
4. verificar se pode ser reutilizado;
5. verificar se pode virar subworkflow;
6. somente criar novo quando não existir alternativa válida.

Preservar:

- IDs reais;
- histórico;
- versões;
- logs;
- dependências.

---

12. GOVERNANÇA E SEGURANÇA

Os agentes não podem:

- apagar workflows;
- apagar tabelas;
- apagar arquivos;
- apagar credenciais;
- alterar produção sem backup;
- ativar todos os workflows em massa;
- publicar conteúdo fora do portfólio;
- inventar serviços;
- expor tokens;
- registrar segredos em logs.

Toda alteração deve possuir:

backup
diff
versão
teste
aprovação
rollback
registro no Supabase

---

13. WORKFLOWS MÍNIMOS A IMPLEMENTAR

DL_NEXUS_GPT_ENGINEER
DL_NEXUS_GEMINI_AUDITOR
DL_NEXUS_AGENT_MEMORY
DL_NEXUS_WORKFLOW_HEALTH_MONITOR
DL_NEXUS_SOCIAL_SENTINEL
DL_NEXUS_PATCH_MANAGER
DL_NEXUS_TEST_RUNNER
DL_NEXUS_CHANGELOG_MANAGER

Esses workflows podem reutilizar estruturas existentes do:

- 090 Guardião;
- 091 Sentinela;
- 004 Skill Router;
- 008 MCP Server;
- 150 Máquina de Conteúdo;
- 081 Instagram;
- 082 Facebook;
- 141 Revisor;
- 142 Classificador;
- 144 Revisor Duplo;
- 148 Log Social;
- 149 Relatório Social.

Não duplicar lógica existente.

---

14. RESULTADO FINAL ESPERADO

O DL Nexus deverá operar da seguinte forma:

Portfólio DL
↓
Planejamento diário
↓
Seleção da linha de serviço
↓
Criação de 4 a 6 conteúdos
↓
Geração de imagens
↓
Auditoria Gemini
↓
Fila de publicação
↓
Facebook e Instagram
↓
Validação real
↓
Registro de métricas
↓
Aprendizado
↓
Reutilização dos melhores temas

Paralelamente:

Monitoramento do n8n
↓
Detecção de falha
↓
Auditoria Gemini
↓
Correção GPT
↓
Teste
↓
Aprovação
↓
Versionamento
↓
Retorno à operação

O sistema deverá avisar automaticamente quando algo parar.

Diogo não deverá descobrir por acaso que nenhuma postagem foi publicada.

O DL Nexus deverá ser capaz de identificar a interrupção, explicar o motivo e iniciar o processo de correção.
