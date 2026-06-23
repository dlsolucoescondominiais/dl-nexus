const fs = require('fs');
let indexHtml = fs.readFileSync('index.html', 'utf8');

// Remove B2B from indexHtml
indexHtml = indexHtml.replace(/ B2B/g, '');
indexHtml = indexHtml.replace(/B2B /g, '');

// Apply WhatsApp buttons to index.html
indexHtml = indexHtml.replace('<h3>Atendimento via Meta/Redes</h3>', '<h3>Plantão Comercial Express</h3>');
indexHtml = indexHtml.replace('<p>Canal dedicado a solicitações originadas em campanhas do Instagram ou Facebook.</p>', '<p>Canal imediato para novas solicitações e avaliação técnica expressa para o seu condomínio.</p>');
indexHtml = indexHtml.replace('Atendimento Meta', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width:16px;height:16px;vertical-align:middle;margin-right:8px;fill:currentColor;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 413.4c-33 0-65.5-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg> Solicitar Orçamento via WhatsApp');

const waSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width:16px;height:16px;vertical-align:middle;margin-right:8px;fill:currentColor;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 413.4c-33 0-65.5-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>';
if (!indexHtml.includes(waSvg + ' Falar com o Suporte')) {
  indexHtml = indexHtml.replace('Falar com o Suporte', waSvg + ' Falar com o Suporte');
}
if (!indexHtml.includes(waSvg + ' Falar com Comercial')) {
  indexHtml = indexHtml.replace('Falar com Comercial', waSvg + ' Falar com Comercial');
}
if (!indexHtml.includes(waSvg + ' Solicitar avaliação elétrica')) {
  indexHtml = indexHtml.replace('Solicitar avaliação elétrica', waSvg + ' Solicitar avaliação elétrica');
}

fs.writeFileSync('index.html', indexHtml);

// Build Pages
const headerMatch = indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<main>/);
const footerMatch = indexHtml.match(/(<\/main>[\s\S]*?<\/html>)/);

if (headerMatch && footerMatch) {
  let header = headerMatch[1];
  let footer = footerMatch[1];
  
  header = header.replace(/<a class="skip-link"[^>]*>.*?<\/a>/, '');
  
  const createPage = (filename, title, content) => {
    let pageHeader = header.replace(/<title>.*?<\/title>/, '<title>' + title + '</title>');
    const fullPage = pageHeader + '\n<main style="padding: 100px 20px; max-width: 1000px; margin: auto;">\n' + content + '\n</main>\n' + footer;
    fs.writeFileSync(filename, fullPage);
  };

  const portifolioContent = 
    '<a href="index.html" class="btn btn-secondary" style="margin-bottom:20px">&larr; Voltar para Home</a>' +
    '<h1>Portfólio de Obras e Instalações</h1>' +
    '<p>Conheça nossos cases de sucesso em elétrica predial, montagem de quadros de comando, instalação de CFTV, controle de acesso e usinas solares.</p>' +
    '<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px;">' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center;">' +
        '<img src="assets/eletrica.png" alt="Elétrica Predial" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Elétrica Predial</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center;">' +
        '<img src="assets/cftv.png" alt="Sistema de CFTV" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Sistemas de CFTV IP</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center;">' +
        '<img src="assets/controle_acesso.png" alt="Controle de Acesso" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Controle de Acesso Facial</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center;">' +
        '<img src="assets/solar.png" alt="Energia Solar" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Usinas de Energia Solar</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center;">' +
        '<img src="assets/carros_eletricos.png" alt="Carregadores Veiculares" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Carregadores Veiculares</h3>' +
      '</div>' +
    '</div>';
  createPage('portifolio.html', 'Portfólio | DL Soluções Condominiais', portifolioContent);

  createPage('a-empresa.html', 'A Empresa | DL Soluções Condominiais', 
    '<h1>A Empresa</h1><p>A DL Soluções Condominiais busca ser a empresa referência no atendimento a condomínios no Rio de Janeiro.</p><p>Oferecemos soluções de excelência com registro no CREA-RJ, associação à ABESE-SP e equipe altamente qualificada, garantindo a sua tranquilidade jurídica e operacional em todos os projetos.</p>');

  createPage('o-fundador.html', 'O Fundador | DL Soluções Condominiais', 
    '<h1>O Fundador</h1><p>Diogo Lessa é Engenheiro de Integração com forte atuação no mercado corporativo e condominial. Ele fundou a DL Soluções Condominiais com o foco em entregar excelência operacional.</p><p>Sua especialidade abrange CFTV IP, Controle de Acesso Facial, Elétrica Predial e Usinas de Energia Solar, aliando sempre a tecnologia e a durabilidade exigidas pelos condomínios modernos do RJ.</p>');

  createPage('lgpd-gdpr.html', 'LGPD e GDPR | DL Soluções Condominiais', 
    '<h1>LGPD e GDPR</h1><p>Estamos 100% comprometidos com a segurança dos seus dados conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p><h2>Tratamento de Dados</h2><p>Coletamos dados apenas para fins de propostas comerciais e suporte técnico, não compartilhando informações com terceiros sem consentimento explícito.</p>');

  createPage('politica-privacidade.html', 'Política de Privacidade | DL Soluções Condominiais', 
    '<h1>Política de Privacidade e Proteção de Dados</h1><p>A DL Soluções Condominiais realiza o tratamento de dados com total transparência e segurança (Adequado à LGPD e políticas Meta).</p><h2>Como Utilizamos suas Informações</h2><p>Coletamos nome e WhatsApp apenas para responder suas solicitações de orçamento. Não enviamos spam. Seu contato no "Plantão Comercial Express" é privado e direto com nossos engenheiros.</p>');
}
