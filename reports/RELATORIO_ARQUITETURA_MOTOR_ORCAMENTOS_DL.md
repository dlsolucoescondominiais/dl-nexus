# Relatório de Arquitetura: Motor de Orçamentos DL

## Falhas encontradas na arquitetura atual
- Ausência de validação humana obrigatória antes do envio de orçamentos finais (risco de precificação incorreta).
- Falta de registro claro sobre a fonte de informações (ex: dados vindos do cliente vs. dados enriquecidos).
- Uso de estimativas não baseadas em evidências sólidas, como calcular rateios sem saber o número real de unidades.
- Risco de violação da LGPD devido à captura ou uso indevido de dados pessoais sem fluxo de consentimento explícito.
- Termos proibidos sendo gerados na comunicação pública (ex: "B2B", "visita técnica", "Condfy", "preço final").

## Campos obrigatórios
- `nome`
- `telefone`
- `e-mail`
- `tipo_cliente`
- `numero_unidades` (obrigatório exclusivamente quando houver rateio)
- `aceite_lgpd`
- `custo_total`, `margem`, `impostos`, `deslocamento`, `material`, `mao_de_obra` (para cálculo)

## Campos que não podem ser estimados
- **Número de unidades:** Deve ser fornecido pelo cliente ou por documentação oficial; a IA jamais deve estimar este valor para fins de cálculo financeiro.
- **Valores e custos diretos sem evidência:** O cálculo deve sempre derivar dos dados inseridos no módulo de cálculo.

## Riscos LGPD
- Uso do CPF para buscas públicas (o CPF deve ser usado estritamente para cadastro/contrato com consentimento explícito).
- Armazenamento de reclamações/opiniões de moradores que podem ser classificadas como dados sensíveis (estas devem ir apenas para o relatório interno, de forma restrita).
- Coleta de dados de imagem/vídeo sem o consentimento claro de que serão usados para avaliação técnica (necessidade do aceite explícito - `aceite_lgpd`).

## Arquitetura n8n sugerida
A arquitetura baseia-se em 7 módulos sequenciais e assíncronos:
1. **Módulo 1:** Entrada pelo site via Webhook, coletando todos os campos iniciais.
2. **Módulo 2:** Enriquecimento de dados de CNPJ, validação e geolocalização de CEP (preservando o dado original e marcando as divergências).
3. **Módulo 3:** Análise de Mídia, avaliando vídeos e imagens para classificar o nível de evidência (confirmado, provável, não confirmado, insuficiente).
4. **Módulo 4:** Classificação do Serviço, roteando para as linhas DL adequadas.
5. **Módulo 5:** Motor de Cálculo Comercial, processando custos para gerar preço sugerido, e rateio apenas se o número de unidades for válido.
6. **Módulo 6:** Protocolo KILLCRITIC, rodando verificações finais no payload textual para bloquear emissão de orçamentos automáticos ou o uso de termos proibidos.
7. **Módulo 7 & 8:** Geração de Documentos, acionando o Gotenberg para a emissão de PDF com design A4 padrão.
8. **Módulo 9:** Logs gerais via integração com Supabase.

## Tabelas Supabase
As seguintes tabelas deverão ser criadas/ajustadas para registro integral do ciclo de vida:
- `dl_orcamentos` (dados principais do lead e status do orçamento)
- `dl_orcamento_enriquecimento` (dados de terceiros e divergências vs input)
- `dl_orcamento_arquivos` (metadados de vídeos/imagens recebidos e analisados)
- `dl_orcamento_riscos` (reclamações internas e grau de confiança das evidências)
- `dl_orcamento_versoes` (histórico de pré-propostas e aprovações do documento Gotenberg)
- `dl_orcamento_envios` (logs de comunicação final e follow-up)

## Workflows necessários
Serão criados/alocados os seguintes workflows n8n para a esteira:
- `060_ORCAMENTO_RECEPCAO_SITE_DL`
- `061_ORCAMENTO_ENRIQUECIMENTO_DADOS_DL`
- `062_ORCAMENTO_ANALISE_VIDEO_IMAGEM_DL`
- `063_ORCAMENTO_CALCULO_COMERCIAL_DL`
- `064_ORCAMENTO_KILLCRITIC_DL`
- `065_ORCAMENTO_GERADOR_PDF_GOTENBERG_DL`
- `066_ORCAMENTO_ENVIO_E_FOLLOWUP_DL`

## Pontos que exigem aprovação humana
- **Validação Comercial:** Nenhuma proposta técnica/comercial pode ser convertida em "PDF Final" ou "Preço Final" enviado ao cliente sem a aprovação explícita de um operador/responsável.
- **Evidências Insuficientes:** Orçamentos que caírem na regra de "dados insuficientes para confirmação definitiva" precisam de auditoria humana antes de prosseguir com sugestões de preços.

## Próximos passos de implementação
1. **Modelagem de Dados:** Provisionar as 6 tabelas no Supabase com suas respectivas políticas (RLS) para proteger dados sob a LGPD.
2. **Desenvolvimento dos Workflows Iniciais:** Construir e testar os workflows `060` e `061` em ambiente isolado (`active=false`), acionando mocks de formulário do site.
3. **Integração de Mídia e IA:** Implementar a lógica no `062` para classificar arquivos, validando prompts de IA contra o protocolo KILLCRITIC.
4. **Templates HTML/Gotenberg:** Desenvolver os layouts A4 para relatórios internos e propostas externas do workflow `065`.
5. **Auditoria Geral:** Rodar simulações completas garantindo que o fluxo trava (Módulo 6) se as diretrizes humanas não forem aprovadas ou se termos proibidos aparecerem.
