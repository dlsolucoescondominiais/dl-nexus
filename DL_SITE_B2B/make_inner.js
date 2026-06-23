const fs = require('fs');
let indexHtml = fs.readFileSync('index.html', 'utf8');

const headerMatch = indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<main>/) || indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<section class="hero">/);
const footerMatch = indexHtml.match(/(<\/footer>[\s\S]*?<\/html>)/);

if (headerMatch && footerMatch) {
  let header = headerMatch[1];
  let footer = footerMatch[1];

  const createPage = (filename, title, content) => {
    let pageHeader = header.replace(/<title>.*?<\/title>/, '<title>' + title + '</title>');
    const fullPage = pageHeader + '\n<main style="padding: 100px 20px; max-width: 1000px; margin: auto;">\n' + content + '\n</main>\n<footer class="footer">' + footer;
    fs.writeFileSync(filename, fullPage);
  };

  const portifolioContent = 
    '<a href="index.html" class="btn btn-secondary" style="margin-bottom:20px">&larr; Voltar para Home</a>' +
    '<h1 style="color:var(--dl-blue-dark);">Portfólio de Obras e Instalações</h1>' +
    '<p>Conheça nossos cases de sucesso em elétrica predial, montagem de quadros de comando, instalação de CFTV, controle de acesso e usinas solares.</p>' +
    '<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px;">' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center; box-shadow: var(--shadow-soft);">' +
        '<img src="assets/eletrica.png" alt="Elétrica Predial" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Elétrica Predial</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center; box-shadow: var(--shadow-soft);">' +
        '<img src="assets/cftv.png" alt="Sistema de CFTV" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Sistemas de CFTV IP</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center; box-shadow: var(--shadow-soft);">' +
        '<img src="assets/controle_acesso.png" alt="Controle de Acesso" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Controle de Acesso Facial</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center; box-shadow: var(--shadow-soft);">' +
        '<img src="assets/solar.png" alt="Energia Solar" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Usinas de Energia Solar</h3>' +
      '</div>' +
      '<div style="border: 1px solid var(--dl-border); border-radius: 12px; overflow: hidden; background: var(--dl-surface); text-align: center; box-shadow: var(--shadow-soft);">' +
        '<img src="assets/carros_eletricos.png" alt="Carregadores Veiculares" style="width: 100%; height: 200px; object-fit: cover;">' +
        '<h3 style="margin: 15px; color: var(--dl-blue-dark);">Carregadores Veiculares</h3>' +
      '</div>' +
    '</div>';
  createPage('portifolio.html', 'Portfólio | DL Soluções Condominiais', portifolioContent);

  createPage('a-empresa.html', 'A Empresa | DL Soluções Condominiais', 
    '<h1 style="color:var(--dl-blue-dark);">A Empresa</h1><p>A DL Soluções Condominiais busca ser a empresa referência no atendimento a condomínios no Rio de Janeiro.</p><p>Oferecemos soluções de excelência com registro no CREA-RJ, associação à ABESE-SP e equipe altamente qualificada, garantindo a sua tranquilidade jurídica e operacional em todos os projetos.</p>');

  createPage('o-fundador.html', 'O Fundador | DL Soluções Condominiais', 
    '<h1 style="color:var(--dl-blue-dark);">O Fundador</h1><p>Diogo Lessa é Engenheiro de Integração com forte atuação no mercado corporativo e condominial. Ele fundou a DL Soluções Condominiais com o foco em entregar excelência operacional.</p><p>Sua especialidade abrange CFTV IP, Controle de Acesso Facial, Elétrica Predial e Usinas de Energia Solar, aliando sempre a tecnologia e a durabilidade exigidas pelos condomínios modernos do RJ.</p>');

  createPage('lgpd-gdpr.html', 'LGPD e GDPR | DL Soluções Condominiais', 
    '<h1 style="color:var(--dl-blue-dark);">LGPD e GDPR</h1><p>Estamos 100% comprometidos com a segurança dos seus dados conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p><h2 style="color:var(--dl-blue-dark);">Tratamento de Dados</h2><p>Coletamos dados apenas para fins de propostas comerciais e suporte técnico, não compartilhando informações com terceiros sem consentimento explícito.</p>');

  createPage('politica-privacidade.html', 'Política de Privacidade | DL Soluções Condominiais', 
    '<h1 style="color:var(--dl-blue-dark);">Política de Privacidade e Proteção de Dados</h1><p>A DL Soluções Condominiais realiza o tratamento de dados com total transparência e segurança (Adequado à LGPD e políticas Meta).</p><h2 style="color:var(--dl-blue-dark);">Como Utilizamos suas Informações</h2><p>Coletamos nome e WhatsApp apenas para responder suas solicitações de orçamento. Não enviamos spam. Seu contato no "Plantão Comercial Express" é privado e direto com nossos engenheiros.</p>');
}
