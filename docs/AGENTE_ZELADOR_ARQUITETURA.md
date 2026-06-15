# Agente Zelador do Google Drive - Arquitetura de Organização Segura

## 1. Objetivo e Arquitetura

O sistema implementa uma organização baseada em três camadas para garantir segurança e rastreabilidade total:

1. **INVENTÁRIO** (`SCRIPT_INVENTARIO_DRIVE_V1`): Lê o Drive passivamente e mapeia todos os arquivos no Supabase. O Code Node nativo resolve óbvios (MIME type e extensões).
2. **CLASSIFICAÇÃO** (`AGENTE_ZELADOR_CLASSIFICADOR_V1`): Lê arquivos pendentes/ambíguos via Supabase e consulta a IA (Prompt configurado com o perfil DL/Mult•Grill). Nenhuma ação de movimentação ocorre aqui.
3. **EXECUÇÃO CONTROLADA** (`ZELADOR_DRIVE_EXECUTOR_SEGURO_V1`): Módulo isolado que apenas movimenta os arquivos previamente definidos como `status = 'aprovado_para_mover'`. Valida rigidamente as pastas pela "allowlist" (tabela `drive_zelador_allowed_folders`).

## 2. Regras e Ações Permitidas/Proibidas

**Ações Permitidas:** classificar, revisar, ignorar, mover.
**Ações Proibidas (Bloqueadas em Código):** delete, trash, remove, erase, destroy, rename, overwrite, permanently_delete.

*Regra Máxima:* Se houver dúvida, enviar para a pasta "04. TRIAGEM_REVISAO_HUMANA".

## 3. Política de Status

A tabela `drive_zelador_inventory` utiliza o seguinte lifecycle:
- `novo`
- `inventariado`
- `classificacao_pendente`
- `classificado`
- `revisao_humana`
- `aprovado_para_mover`
- `movido`
- `bloqueado`
- `erro`
- `ignorado`

## 4. Pastas Base da Allowlist (ID Real a inserir no SQL/Supabase)

A área de "Computadores" ou sincronizados está fora do escopo primário e é vetada até liberação formal manual. Todo workflow começará apenas mapeando `TESTE_ZELADOR_NAO_EXCLUIR`.

| Folder Key | Name | Categoria |
| :--- | :--- | :--- |
| INBOX_SMARTPHONE | 00_INBOX_SMARTPHONE | inbox |
| AUDIOS | 01. ÁUDIOS | audio |
| CONTRATOS_DOCUMENTOS | 02. CONTRATOS E DOCUMENTOS | documentos |
| FOTOS_VIDEOS | 03. FOTOS E VÍDEOS | midia |
| TRIAGEM_HUMANA | 04. TRIAGEM_REVISAO_HUMANA | triagem |
| CENTRAL_MEMORIA | 05. CENTRAL DE MEMÓRIA | memoria |
| FOOD_SERVICE_MULTGRILL | FOOD_SERVICE_MULTGRILL | food_service |
| CONDOMINIOS_COLEGIOS | CONDOMINIOS_COLEGIOS | condominios_colegios |
| FINANCEIRO | FINANCEIRO | financeiro |
| FORNECEDORES | FORNECEDORES | fornecedores |

## 5. Códigos Nodais (Para Conferência Rápida)

### 5.1 Code Node - Extração Metadados e Classificador Objetivo
Usado no final de `SCRIPT_INVENTARIO_DRIVE_V1`
```javascript
return items.map(item => {
  const f = item.json;
  const name = String(f.name || '').toLowerCase();
  const mime = String(f.mimeType || '').toLowerCase();
  const ext = name.includes('.') ? name.split('.').pop().toLowerCase() : '';

  let categoria = null;
  let pasta = null;
  let confianca = 0;
  let motivo = '';

  if (mime.startsWith('audio/') || ['mp3', 'm4a', 'ogg', 'wav', 'opus'].includes(ext)) {
    categoria = 'AUDIOS';
    pasta = 'AUDIOS';
    confianca = 0.95;
    motivo = 'Arquivo identificado como áudio por MIME ou extensão.';
  } else if (mime.startsWith('image/') || mime.startsWith('video/') || ['jpg', 'jpeg', 'png', 'webp', 'mp4', 'mov', 'avi'].includes(ext)) {
    categoria = 'FOTOS_VIDEOS';
    pasta = 'FOTOS_VIDEOS';
    confianca = 0.9;
    motivo = 'Arquivo identificado como foto ou vídeo por MIME ou extensão.';
  } else if (name.includes('contrato') || name.includes('proposta') || name.includes('orçamento') || name.includes('orcamento') || name.includes('termo') || name.includes('recibo') || name.includes('nota fiscal') || name.includes('nf') || name.includes('boleto') || name.includes('pix')) {
    categoria = 'CONTRATOS_DOCUMENTOS';
    pasta = 'CONTRATOS_DOCUMENTOS';
    confianca = 0.85;
    motivo = 'Nome indica documento comercial, financeiro ou contratual.';
  } else if (name.includes('fritadeira') || name.includes('chapa') || name.includes('multgrill') || name.includes('mult•grill') || name.includes('hamburgueria') || name.includes('lanchonete') || name.includes('restaurante')) {
    categoria = 'FOOD_SERVICE_MULTGRILL';
    pasta = 'FOOD_SERVICE_MULTGRILL';
    confianca = 0.88;
    motivo = 'Nome indica atendimento Food Service / Mult•Grill.';
  } else if (name.includes('condominio') || name.includes('condomínio') || name.includes('sindico') || name.includes('síndico') || name.includes('colegio') || name.includes('colégio') || name.includes('escola')) {
    categoria = 'CONDOMINIOS_COLEGIOS';
    pasta = 'CONDOMINIOS_COLEGIOS';
    confianca = 0.88;
    motivo = 'Nome indica atendimento de condomínio, síndico, colégio ou escola.';
  } else {
    categoria = 'TRIAGEM_HUMANA';
    pasta = 'TRIAGEM_HUMANA';
    confianca = 0.3;
    motivo = 'Classificação incerta. Encaminhar para revisão humana.';
  }

  return {
    json: {
      file_id: f.id,
      file_name: f.name || '',
      file_extension: ext,
      mime_type: f.mimeType || null,
      file_size: f.size ? Number(f.size) : null,
      current_folder_id: f.parents?.[0] || null,
      web_view_link: f.webViewLink || null,
      md5_checksum: f.md5Checksum || null,
      created_time: f.createdTime || null,
      modified_time: f.modifiedTime || null,
      status: confianca >= 0.75 ? 'classificado' : 'revisao_humana',
      acao_sugerida: 'classificar',
      categoria_detectada: categoria,
      categoria_sugerida: categoria,
      pasta_destino_sugerida: pasta,
      confianca: confianca,
      motivo_classificacao: motivo,
      precisa_revisao_humana: confianca < 0.75
    }
  };
});
```

### 5.2 Code Node - Bloqueio Final de Ações Proibidas
Usado no workflow executor (`ZELADOR_DRIVE_EXECUTOR_SEGURO_V1`):
```javascript
const forbidden = ['delete', 'trash', 'remove', 'erase', 'destroy', 'rename', 'overwrite', 'permanently_delete'];

return items.map(item => {
  const action = String(item.json.acao_aprovada || '').toLowerCase();
  const status = String(item.json.status || '').toLowerCase();

  if (forbidden.includes(action)) {
    throw new Error(`Ação proibida bloqueada: ${action}`);
  }
  if (action !== 'mover') {
    throw new Error(`Ação não autorizada para executor: ${action}`);
  }
  if (status !== 'aprovado_para_mover') {
    throw new Error(`Status não autorizado para mover: ${status}`);
  }
  if (!item.json.pasta_destino_id) {
    throw new Error('Sem pasta_destino_id. Movimento bloqueado.');
  }
  if (item.json.precisa_revisao_humana === true) {
    throw new Error('Arquivo marcado para revisão humana. Movimento bloqueado.');
  }

  return item;
});
```

## 6. Checklists de Operação e Segurança

### Checklist de Deploy e Configuração (Administrador)
- [ ] Rodar SQL de criação das tabelas no Supabase (`backend/supabase/MIGRATIONS_DL_NEXUS_ZELADOR.sql`).
- [ ] Obter os `ID`s reais do Google Drive para cada pasta autorizada.
- [ ] Atualizar os `folder_id`s na tabela `drive_zelador_allowed_folders` (Update via SQL ou Painel).
- [ ] Workflow 1 (Inventário) configurado com Folder ID restrito apenas à pasta `TESTE_ZELADOR_NAO_EXCLUIR`.
- [ ] Workflow 2 (Classificador) configurado com credencial Gemini ou OpenAI.
- [ ] Workflow 3 (Executor) configurado, verificado nó Google Drive com Action `Update/Parents` (ou `Move`). O nó NUNCA pode ser `Delete` ou `Trash`.
- [ ] Validação dos Logs: Garantir que Upserts no Supabase estejam mapeando `file_id`.
- [ ] Schedule configurado apenas na madrugada para lotes limitados (ex: 10 a 100 arquivos/lote).
- [ ] Confirmada a proibição de uso em "Computadores" sincronizados antes da homologação.

### Checklist do Teste Inicial Obrigado (TDD Zelador)
A execução de homologação deve apontar o workflow de Inventário para a pasta `TESTE_ZELADOR_NAO_EXCLUIR` com os seguintes dummies:
1. `IMG_001.jpg`
2. `WhatsApp Audio.ogg`
3. `Contrato Cliente.pdf`
4. `Orcamento CFTV.docx`
5. `fritadeira_multgrill_resistencia.jpg`
6. `chapa_nao_aquece.mp4`
7. `arquivo_sem_nome.bin`
8. `comprovante_pix.pdf`
9. `nota_fiscal.pdf`
10. `foto_condominio_portaria.jpg`

*Critérios Passa/Não Passa (P/NP)*
- [ ] 0 arquivos excluídos/movidos para lixeira
- [ ] 0 arquivos renomeados ou editados no conteúdo
- [ ] 100% inventariados na tabela com status inicial
- [ ] 100% classificados ou marcados como "revisão_humana"
- [ ] Workflow Executor moveu os itens de teste APENAS para os ID de teste temporários, alterando os Paths de forma transparente e gravando status `movido` (sem alterar File ID).

## 7. Relatório de Riscos (Security Risk Registry)

1. **Risco de Deleção Categórica:** O n8n Cloud / Desktop possui nodes nativos de Drive. Se por erro humano o nó executor for alterado de "Move" para "Delete/Trash", a base será destruída.
   *Mitigação:* O Code Node `Bloqueio Final de Ações Proibidas` lê as variáveis ativas. Para proteção adicional, as chaves de permissão da Conta de Serviço / Oauth do Drive usadas no n8n devem ter o scope de `delete` ou `trash` revogado sempre que possível na nuvem do Google GCP (usar o escopo mais restrito de leitura e escrita, `drive.file` / `drive` restrito a subpastas, sem `drive.appdata` ou trash rights caso a API permita).
2. **Risco de Limites de API (Rate Limits):** Leituras pesadas em diretórios com milhares de arquivos gerarão erro 429 do Google e quebrarão a extração do inventário.
   *Mitigação:* `Split In Batches` parametrizado com delay agressivo (ex: 2 a 5 segundos por lote de 10) e cap inicial máximo de 100 arquivos por execução.
3. **Falsa Confiança da IA (Alucinação de Path):** A IA pode inventar ou misturar IDs.
   *Mitigação:* A arquitetura não usa IDs vindos da IA. A IA sugere a "Key" da pasta (`FOOD_SERVICE_MULTGRILL`), que é cruzada em SQL via JOIN na tabela `drive_zelador_allowed_folders` para extrair o ID real blindado do sistema.
