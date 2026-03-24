const https = require('https');

// A URL do seu webhook de teste (com -test no final) no n8n da DL Soluções
const webhookUrl = 'https://n8n.dlsolucoescondominiais.com.br/webhook-test/receber-lead';

const leadFalso = JSON.stringify({
  nome: "João Testador (Síndico)",
  nome_condominio: "Condomínio DL Nexus (Teste)",
  telefone: "21999999999",
  email: "joao@teste.com",
  tipo_imovel: "Condomínio Residencial",
  num_unidades: "150",
  tipo_servico: "Energia Solar",
  mensagem: "Teste de comunicação do sistema DL Nexus para o n8n. Está me ouvindo, Aninha?"
});

const options = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(leadFalso)
  }
};

console.log(`\n🚀 Enviando Lead Falso para o n8n em: ${webhookUrl}\n`);

const req = https.request(webhookUrl, options, (res) => {
  console.log(`📡 Status da Resposta do n8n: ${res.statusCode}`);

  res.on('data', (d) => {
    process.stdout.write(d);
    console.log('\n\n✅ Comunicação BEM-SUCEDIDA! O n8n recebeu a mensagem.');
  });
});

req.on('error', (e) => {
  console.error(`\n❌ ERRO NA COMUNICAÇÃO! O n8n não respondeu.`);
  console.error(`Motivo: ${e.message}`);
  console.error(`DICA: Verifique se o n8n está online, se a URL está certa e se você clicou em "Listen for Test Event" na tela do n8n.`);
});

req.write(leadFalso);
req.end();
