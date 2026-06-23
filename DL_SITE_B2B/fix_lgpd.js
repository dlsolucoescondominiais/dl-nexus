const fs = require('fs');

const lgpdContent = `
<h1 class="inner-heading" style="font-size: 2.5rem; margin-bottom: 30px; font-weight: 700;">Política de Privacidade e Proteção de Dados (LGPD / GDPR)</h1>
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Seção 1: Introdução e Compromisso com a Privacidade</strong></p>
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Preâmbulo</strong><br>A presente Política de Privacidade e Proteção de Dados ("Política") estabelece os termos e as condições sob os quais a DL SOLUÇÕES CONDOMINIAIS LTDA., pessoa jurídica de direito privado, inscrita no CNPJ/ME sob o nº 36.354.697/0001-46, com sede em território brasileiro ("DL Soluções Condominiais", "Empresa"), realiza o tratamento de dados pessoais. O objetivo primordial deste documento é conferir máxima transparência e estabelecer as regras aplicáveis a todas as operações de tratamento de dados pessoais executadas no contexto da prestação de seus serviços, em estrita conformidade com o ordenamento jurídico vigente, notadamente a Lei Geral de Proteção de Dados Pessoais (LGPD), Lei nº 13.709, de 14 de agosto de 2018, e as diretrizes de privacidade do Google e Meta.</p>
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Declaração de Compromisso</strong><br>A DL Soluções Condominiais reconhece a privacidade e a proteção de dados como pilares fundamentais de sua operação e como componentes essenciais para a construção de uma relação de confiança com seus clientes, parceiros e com os titulares de dados. A Empresa compromete-se a respeitar e a proteger os direitos fundamentais de liberdade e de privacidade, bem como o livre desenvolvimento da personalidade da pessoa natural, conforme preconiza o Artigo 1º da LGPD. Todas as atividades de tratamento de dados conduzidas pela Empresa são pautadas pelos mais elevados padrões éticos e legais.</p>
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Abrangência da Política</strong><br>Esta Política aplica-se a todas as operações de tratamento de dados pessoais realizadas pela DL Soluções Condominiais, independentemente do meio, seja ele digital ou físico. Seu escopo abrange os dados de todos os titulares com os quais a Empresa interage no exercício de suas atividades, incluindo clientes (síndicos, administradoras e condôminos), parceiros, fornecedores e visitantes do nosso site e redes sociais.</p>

<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Coleta e Tratamento de Dados (Requisitos Google e Meta)</strong><br>Para fornecer e melhorar nossos serviços, coletamos informações quando você interage com nosso site ou anúncios (Google Ads, Meta Ads). Isso pode incluir dados de contato (nome, telefone, e-mail) fornecidos voluntariamente para orçamentos, e dados de navegação (cookies, IP, comportamento no site) coletados automaticamente para otimização de campanhas e análises de tráfego. O tratamento desses dados possui bases legais claras, como o consentimento do titular e o legítimo interesse da empresa em melhorar sua comunicação e segurança.</p>

<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Compartilhamento e Segurança</strong><br>Os dados coletados não são comercializados ou compartilhados com terceiros não autorizados. Podem ser processados por plataformas parceiras (como Google Analytics, Meta Pixel, sistemas de CRM) estritamente para os fins descritos, sendo essas plataformas igualmente submetidas a rigorosos padrões de segurança da informação.</p>

<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;"><strong>Direitos do Titular</strong><br>Conforme a LGPD, o titular dos dados possui o direito de confirmar a existência de tratamento, acessar seus dados, corrigir informações incompletas, solicitar anonimização, bloqueio ou eliminação de dados desnecessários, bem como revogar o consentimento a qualquer momento. Para exercer esses direitos, entre em contato através de nossos canais oficiais de atendimento.</p>
`;

const indexHtml = fs.readFileSync('index.html', 'utf8');

const headerMatch = indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<section class="hero">/) || indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<main>/);
const header = headerMatch ? headerMatch[1] : '';

const footerMatch = indexHtml.match(/(<footer class="footer">[\s\S]*?<\/html>)/);
const footer = footerMatch ? footerMatch[1] : '';

const createPage = (filename, title, content) => {
  let pageHeader = header.replace(/<title>.*?<\/title>/, '<title>' + title + '</title>');
  
  const customStyles = `
    <style>
      .inner-heading {
        color: var(--dl-blue-dark);
      }
      [data-theme="dark"] .inner-heading {
        color: #f7f9fb;
      }
      .inner-content a {
        color: var(--dl-blue-light);
        text-decoration: underline;
      }
      [data-theme="dark"] .inner-content a {
        color: var(--dl-gold);
      }
    </style>
  `;
  
  pageHeader = pageHeader.replace('</head>', customStyles + '\n</head>');

  const fullPage = pageHeader + '\n<main class="inner-content" style="padding: 120px 20px 60px 20px; max-width: 1000px; margin: auto; min-height: 70vh;">\n' + content + '\n</main>\n' + footer;
  fs.writeFileSync(filename, fullPage, 'utf8');
};

createPage('lgpd-gdpr.html', 'LGPD / GDPR | DL Soluções Condominiais', lgpdContent);
createPage('politica-privacidade.html', 'Política de Privacidade | DL Soluções Condominiais', lgpdContent);

console.log('LGPD and Privacy Policy generated.');
