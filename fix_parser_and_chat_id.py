import json

with open(r'C:\Users\Diogo\.gemini\antigravity\brain\1017fe4f-5b63-4113-beda-7a5d4b01035b\020_PUBLICADOR_SOCIAL_DL_NEXUS_FIXED.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

for n in wf['nodes']:
    if n['type'] == 'n8n-nodes-base.telegram':
        n['parameters']['chatId'] = '762863956'
    
    if n['name'] == 'NORMALIZAR_SAIDA_IA_SOCIAL':
        n['parameters']['jsCode'] = '''const entrada = $('Entrada do Post').item.json || {};
let conteudo = "";
if ($json.message && $json.message.content) {
  conteudo = $json.message.content;
} else if ($json.choices && $json.choices[0] && $json.choices[0].message) {
  conteudo = $json.choices[0].message.content;
} else {
  conteudo = typeof $json === 'string' ? $json : JSON.stringify($json);
}

let parsed = {};
let status_parse = 'SUCESSO';
let observacao = 'JSON parseado com sucesso.';

try {
  const jsonMatch = conteudo.match(/```(?:json)?\\n([\\s\\S]*?)\\n```/) || conteudo.match(/{[\\s\\S]*}/);
  if (jsonMatch && jsonMatch[1]) {
    parsed = JSON.parse(jsonMatch[1]);
  } else if (jsonMatch && jsonMatch[0]) {
    parsed = JSON.parse(jsonMatch[0]);
  } else {
    parsed = JSON.parse(conteudo);
  }
} catch (e) {
  status_parse = 'FALHOU_USANDO_FALLBACK';
  observacao = 'IA não retornou JSON válido; fallback aplicado: ' + e.message;
  parsed = {
    legenda_facebook: conteudo,
    legenda_instagram: conteudo,
    texto_telegram: conteudo,
    hashtags: []
  };
}

return {
  json: {
    post_id: Date.now().toString(),
    tema: entrada.tema || 'N/A',
    produto: entrada.produto || 'N/A',
    legenda_facebook: parsed.legenda_facebook || parsed.facebook_legenda || parsed.facebook || conteudo,
    legenda_instagram: parsed.legenda_instagram || parsed.instagram_legenda || parsed.instagram || conteudo,
    texto_telegram: parsed.texto_telegram || parsed.telegram_texto || parsed.telegram || conteudo,
    hashtags: parsed.hashtags || [],
    image_url: entrada.image_url || '',
    observacoes: [observacao],
    status_parse_ia: status_parse
  }
};'''

with open(r'C:\Users\Diogo\.gemini\antigravity\brain\1017fe4f-5b63-4113-beda-7a5d4b01035b\020_PUBLICADOR_SOCIAL_DL_NEXUS_V4_FINAL.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)
print("File Generated!")
