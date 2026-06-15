// Auditoria Segura do Google Drive Zelador - NENHUMA DELEÇÃO PERMITIDA
// Este script apenas lista arquivos e sugere renomeação/organização (DRY RUN)
// PROIBIDO: files.delete, files.emptyTrash, files.update (name/parents), permissions.create/update/delete

const arquivos = [];
const arquivos_analisados = [];
const ignorados = [];
let duplicados_detectados = 0;

for (const item of $input.all()) {
  const f = item.json;

  if (f.trashed) {
    ignorados.push({ id: f.id, name: f.name, motivo: "Na lixeira" });
    continue;
  }

  const original_name = f.name || "";
  const ext = original_name.includes('.') ? original_name.split('.').pop().toLowerCase() : "";
  const mime = f.mimeType || "";

  let tipo_midia = "arquivo desconhecido";
  if (mime.includes("image")) tipo_midia = "imagem";
  else if (mime.includes("video")) tipo_midia = "vídeo";
  else if (mime.includes("audio")) tipo_midia = "áudio";
  else if (mime.includes("pdf")) tipo_midia = "PDF";
  else if (mime.includes("document") || mime.includes("text")) tipo_midia = "documento";

  let risco = "";
  let usa_nao = false;
  // Detecção de dados sensíveis
  const nomes_risco = ["placa", "cnh", "rg", "cpf", "boleto", "contrato", "rosto", "cliente", "email"];
  if (nomes_risco.some(r => original_name.toLowerCase().includes(r))) {
    risco = "POSSIVEL_DADO_SENSIVEL";
    usa_nao = true;
  }

  const tema = tipo_midia === "imagem" ? "foto_campo" : (tipo_midia === "vídeo" ? "video_campo" : "duvidoso");
  const produto = "DL_NEXUS";

  // LOGICA PARA DUPLICADOS
  let provavel_duplicado = false;
  let score_duplicidade = "baixo"; // baixo, médio, alto, idêntico_provável

  const checksum = f.md5Checksum || "unknown_hash";
  const tamanho = f.size || 0;

  // Verifica arquivos processados nesta execução (simulação simples)
  const copia_existente = arquivos_analisados.find(a => a.hash === checksum && a.tamanho === tamanho && checksum !== "unknown_hash");
  if (copia_existente) {
      provavel_duplicado = true;
      score_duplicidade = "idêntico_provável";
      duplicados_detectados++;
  } else {
      const nome_similar = arquivos_analisados.find(a =>
          a.nome_original === original_name && a.tamanho === tamanho
      );
      if (nome_similar) {
          provavel_duplicado = true;
          score_duplicidade = "alto";
          duplicados_detectados++;
      }
  }

  arquivos_analisados.push({
      id: f.id,
      hash: checksum,
      tamanho: tamanho,
      nome_original: original_name
  });

  const out = {
    "file_id": f.id,
    "link_drive": f.webViewLink || "",
    "file_name_original": original_name,
    "file_name_sugerido": `2026-06-02_${produto}_${tema}_CAMPO_NOVO_${original_name}`,
    "mime_type": mime,
    "extensao": ext,
    "pasta_origem": f.parents ? f.parents[0] : "",
    "pasta_destino_sugerida": "00_INVENTARIO_GERAL",
    "data_criacao": f.createdTime,
    "data_modificacao": f.modifiedTime,
    "tamanho_bytes": tamanho,
    "tema_detectado": tema,
    "produto_dl_relacionado": produto,
    "status_midia": "NOVO",
    "uso_recomendado": usa_nao ? "NAO_USAR" : "REVISAR",
    "risco_privacidade": risco,
    "precisa_revisao_humana": true,
    "descricao_tecnica_curta": "Arquivo coletado em varredura automática",
    "descricao_para_social": "",
    "cta_recomendado": "https://dlsolucoescondominiais.com",
    "modo_execucao": "DRY_RUN",
    "acao_real_executada": false,
    "provavel_duplicado": provavel_duplicado,
    "score_duplicidade": score_duplicidade,
    "observacoes": "Processado no modo DRY_RUN, arquivo não movido nem alterado."
  };

  arquivos.push({ json: out });
}

// Resumo / Relatório
if (arquivos.length > 0) {
    arquivos[0].json["__auditoria_resumo"] = {
        arquivos_analisados: arquivos_analisados.length,
        arquivos_ignorados: ignorados.length,
        possiveis_duplicados: duplicados_detectados,
        erros_encontrados: 0
    };
}

return arquivos;
