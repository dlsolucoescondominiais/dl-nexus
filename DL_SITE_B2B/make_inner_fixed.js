/**
 * make_inner_fixed.js — Fortress v1
 * Gerador de páginas internas para o site DL Soluções Condominiais.
 * Extrai header/footer do index.html e injeta conteúdo nas páginas internas.
 * Todas as referências KILLCRITIC são respeitadas.
 */
const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');

// Extract header (everything before <section class="hero">)
const heroIdx = indexHtml.indexOf('<section class="hero"');
const header = heroIdx !== -1 ? indexHtml.substring(0, heroIdx) : '';

// Extract footer (from <footer> to end of file)
const footerIdx = indexHtml.indexOf('<footer class="footer"');
const footer = footerIdx !== -1 ? indexHtml.substring(footerIdx) : '';

// Extract cookie banner + WA float + scripts (between </footer> closing and </html>)
// These are already included in the footer match above since it goes to </html>

const createPage = (filename, title, metaDesc, content) => {
  let pageHeader = header.replace(/<title[^>]*>.*?<\/title>/, `<title id="dl-seo-title">${title}</title>`);
  
  // Replace meta description
  pageHeader = pageHeader.replace(
    /<meta id="dl-seo-description"[^>]*>/,
    `<meta id="dl-seo-description" name="description" content="${metaDesc}">`
  );

  // Replace canonical
  pageHeader = pageHeader.replace(
    /<link rel="canonical"[^>]*>/,
    `<link rel="canonical" href="https://dlsolucoescondominiais.com.br/${filename}">`
  );

  // Update dataLayer page type
  pageHeader = pageHeader.replace(
    "'dl_page_type': 'home'",
    `'dl_page_type': '${filename.replace('.html', '')}'`
  );

  const customStyles = `
    <style>
      .inner-page-content {
        padding: 120px 20px 60px 20px;
        max-width: 1000px;
        margin: 0 auto;
        min-height: 70vh;
      }
      .inner-page-content h1 {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 700;
        color: var(--dl-heading);
        margin-bottom: 24px;
        line-height: 1.2;
      }
      .inner-page-content h2 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--dl-heading);
        margin-top: 36px;
        margin-bottom: 16px;
      }
      .inner-page-content h3 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dl-heading);
        margin-top: 28px;
        margin-bottom: 12px;
      }
      .inner-page-content p,
      .inner-page-content li {
        font-size: 1rem;
        line-height: 1.8;
        color: var(--dl-text);
        margin-bottom: 16px;
      }
      .inner-page-content ul {
        padding-left: 24px;
        margin-bottom: 20px;
      }
      .inner-page-content a {
        color: var(--dl-blue-light);
        text-decoration: underline;
      }
      [data-theme="dark"] .inner-page-content a {
        color: var(--dl-gold-light);
      }
      .inner-page-content strong {
        color: var(--dl-heading);
      }
    </style>
  `;
  
  pageHeader = pageHeader.replace('</head>', customStyles + '\n</head>');

  // Ajusta todas as âncoras para apontarem de volta para a index.html (Evita links que não funcionam nas inner pages)
  pageHeader = pageHeader.replace(/href="#/g, 'href="index.html#');
  let pageFooter = footer.replace(/href="#/g, 'href="index.html#');

  const fullPage = pageHeader + 
    '\n<main class="inner-page-content">\n' + 
    content + 
    '\n</main>\n' + 
    pageFooter;
  
  fs.writeFileSync(filename, fullPage, 'utf8');
  console.log(`  ✅ ${filename}`);
};

console.log('🔨 Gerando páginas internas (Fortress v1)...\n');

// ============================================================
// A EMPRESA
// ============================================================
createPage(
  'a-empresa.html',
  'A Empresa | DL Soluções Condominiais',
  'Conheça a DL Soluções Condominiais: proteção patrimonial, segurança eletrônica, elétrica predial e automação para condomínios no Rio de Janeiro.',
  `
<h1>A Jornada da DL Soluções Condominiais: Da Expertise à Excelência</h1>

<p>Toda grande solução nasce de um problema. A história da DL Soluções Condominiais não é diferente. Ela começa com a jornada de seu fundador, Diogo Luiz de Oliveira, e a sua busca incansável por conhecimento técnico em um mercado que nem sempre valoriza a experiência. Nossa trajetória é a prova de que a segurança eletrônica no Rio de Janeiro e as soluções condominiais podem e devem ser sinônimo de confiança e tranquilidade.</p>

<h2>A Fundação: Uma Base Sólida em Tecnologia</h2>
<p>A trajetória começou em 2010, com a formatura em Tecnologia em Infraestrutura de Redes de Computadores pelo SENAC Rio. Antes mesmo do diploma, a paixão por sistemas complexos já era evidente, com estudos aprofundados em Linux (LPI 1 e 2) e Cisco (CCNA). Esta base em redes é o que hoje nos permite criar sistemas de CFTV para condomínios e automação verdadeiramente integrados, onde cada componente "conversa" com o outro de forma estável e segura.</p>
<p>No entanto, o mercado de TI da época apresentava um desafio inesperado: uma preferência por profissionais mais jovens. Para um especialista de 32 anos, com uma bagagem de conhecimento robusta, as portas pareciam mais difíceis de abrir. Foi essa barreira que, em vez de um fim, se tornou um novo começo.</p>

<h2>A Reinvenção: Da Elétrica à Especialização em Soluções Condominiais</h2>
<p>A necessidade de adaptação levou a uma mudança de rumo: a área elétrica. Com cursos na Firjan SENAI e muita dedicação prática — inicialmente através de estágios não remunerados — o conhecimento em redes se uniu à expertise em instalações elétricas. A atuação começou na construção civil, gerenciando equipes em grandes obras para empresas de engenharia.</p>
<p>Mas foi na manutenção de condomínios que a verdadeira vocação se revelou. A experiência prática evidenciou uma carência alarmante no mercado: prestadores de serviço sem qualificação técnica adequada, colocando em risco a segurança e o patrimônio dos moradores.</p>

<h2>A Criação da DL Soluções Condominiais</h2>
<p>Movido pela indignação com a baixa qualidade dos serviços prestados e pela vontade de fazer a diferença, o fundador decidiu formalizar sua expertise. Assim nasceu a DL Soluções Condominiais, com um propósito claro: elevar o padrão dos serviços de elétrica, segurança eletrônica e automação para condomínios no Rio de Janeiro.</p>
<p>A atuação em grandes condomínios do Rio de Janeiro, com foco na Barra da Tijuca, Recreio dos Bandeirantes e Tijuca, incluindo complexos com mais de 500 unidades, revelou uma necessidade latente no mercado: a falta de um parceiro que oferecesse uma solução completa, com responsabilidade técnica. Síndicos e administradores estavam cansados de lidar com múltiplos fornecedores e com a incerteza de serviços executados sem a devida garantia.</p>
<p>Foi nesse cenário que, no início de 2025, a DL Soluções Condominiais nasceu oficialmente, consolidando anos de experiência em um novo modelo de negócio. A mudança foi solidificada com a conclusão da Pós-Graduação em Energia Solar pela Uninter, trazendo a última peça para o nosso portfólio, permitindo-nos oferecer projetos de energia solar RJ com a máxima eficiência e ajudando na redução de custos de energia em condomínio.</p>

<h2>Nossa Missão: A Sua Tranquilidade</h2>
<p>A missão da DL Soluções Condominiais é simples e poderosa: ser a parceira de tecnologia que elimina a complexidade da gestão de infraestrutura, entregando tranquilidade, segurança e valorização para síndicos, administradores e condôminos. Nós entendemos que o seu foco é na gestão, não na procura de dezenas de orçamentos.</p>
<p>Oferecemos um ecossistema completo, desde a segurança perimetral e controle de acesso na Barra da Tijuca e outras regiões, até a eficiência energética com energia solar e a prevenção de incêndio. Não trabalhamos com vigilância 24h, mas com sistemas de prevenção inteligentes e parcerias com as melhores empresas de monitoramento.</p>
<p>Com registro no CREA-RJ 2022346653, associação à ABESE-SP e seguro de obra para todos os nossos serviços, garantimos não apenas a execução, mas a sua total tranquilidade jurídica e operacional. A DL Soluções Condominiais busca ser a empresa referência no atendimento a condomínios de todos os portes no Rio de Janeiro, transformando tecnologia em paz de espírito.</p>
`
);

// ============================================================
// O FUNDADOR
// ============================================================
createPage(
  'o-fundador.html',
  'O Fundador | DL Soluções Condominiais',
  'Conheça Diogo Luiz de Oliveira, fundador da DL Soluções Condominiais. Tecnólogo em Redes, especialista em elétrica predial e Pós-Graduado em Energia Solar.',
  `
<h1>O Fundador — Diogo Luiz de Oliveira</h1>

<p>Diogo Luiz de Oliveira é o fundador e responsável técnico da DL Soluções Condominiais. Tecnólogo em Infraestrutura de Redes de Computadores pelo SENAC Rio (2010), com certificações em Linux (LPI) e Cisco (CCNA), e Pós-Graduado em Energia Solar pela Uninter.</p>

<h2>Da Tecnologia à Elétrica: Uma Jornada de Reinvenção</h2>
<p>Após uma carreira sólida em infraestrutura de TI, Diogo trouxe sua expertise em redes para o mundo da elétrica predial e segurança eletrônica. Com formações complementares na Firjan SENAI, construiu uma bagagem técnica rara no mercado condominial: a capacidade de projetar sistemas verdadeiramente integrados, onde CFTV, controle de acesso, automação e elétrica conversam entre si de forma inteligente.</p>

<h2>A Experiência no Campo</h2>
<p>Com anos de atuação em grandes condomínios do Rio de Janeiro — incluindo complexos residenciais na Barra da Tijuca, Recreio dos Bandeirantes, Tijuca e Zona Norte com mais de 500 unidades — Diogo identificou uma lacuna crítica no mercado: a falta de um parceiro técnico completo, com responsabilidade civil e registro profissional adequado.</p>
<p>Essa percepção foi o combustível para a criação da DL Soluções Condominiais em 2025.</p>

<h2>Credenciais e Registros</h2>
<ul>
  <li><strong>Tecnólogo em Infraestrutura de Redes</strong> — SENAC Rio</li>
  <li><strong>Pós-Graduação em Energia Solar</strong> — Uninter</li>
  <li><strong>CREA-RJ</strong> — Registro nº 2022346653</li>
  <li><strong>ABESE-SP</strong> — Associação Brasileira de Sistemas Eletrônicos de Segurança</li>
  <li><strong>Certificações:</strong> Linux LPI 1 e 2, Cisco CCNA</li>
  <li><strong>Formações complementares:</strong> Firjan SENAI (Elétrica Predial e NR-10)</li>
</ul>

<h2>Visão</h2>
<p>A visão de Diogo para a DL é clara: ser a empresa referência em soluções técnicas para condomínios no Rio de Janeiro, unindo tecnologia de ponta com responsabilidade técnica inquestionável. Cada projeto carrega ART emitida, seguro de obra e a garantia de conformidade com todas as normas vigentes.</p>
`
);

// ============================================================
// POLÍTICA DE PRIVACIDADE
// ============================================================
createPage(
  'politica-privacidade.html',
  'Política de Privacidade | DL Soluções Condominiais',
  'Política de Privacidade e Proteção de Dados da DL Soluções Condominiais, em conformidade com a LGPD e requisitos do Google e Meta.',
  `
<h1>Política de Privacidade e Proteção de Dados</h1>

<h2>Seção 1: Introdução e Compromisso com a Privacidade</h2>
<h3>Preâmbulo</h3>
<p>A presente Política de Privacidade e Proteção de Dados ("Política") estabelece os termos e as condições sob os quais a <strong>DL SOLUÇÕES CONDOMINIAIS LTDA.</strong>, pessoa jurídica de direito privado, inscrita no CNPJ/ME sob o nº 36.354.697/0001-46, com sede em território brasileiro ("DL Soluções Condominiais", "Empresa"), realiza o tratamento de dados pessoais. O objetivo primordial deste documento é conferir máxima transparência e estabelecer as regras aplicáveis a todas as operações de tratamento de dados pessoais executadas no contexto da prestação de seus serviços, em estrita conformidade com o ordenamento jurídico vigente, notadamente a Lei Geral de Proteção de Dados Pessoais (LGPD), Lei nº 13.709, de 14 de agosto de 2018.</p>

<h3>Declaração de Compromisso</h3>
<p>A DL Soluções Condominiais reconhece a privacidade e a proteção de dados como pilares fundamentais de sua operação e como componentes essenciais para a construção de uma relação de confiança com seus clientes, parceiros e com os titulares de dados. A Empresa compromete-se a respeitar e a proteger os direitos fundamentais de liberdade e de privacidade, bem como o livre desenvolvimento da personalidade da pessoa natural, conforme preconiza o Artigo 1º da LGPD. Todas as atividades de tratamento de dados conduzidas pela Empresa são pautadas pelos mais elevados padrões éticos e legais.</p>

<h3>Abrangência da Política</h3>
<p>Esta Política aplica-se a todas as operações de tratamento de dados pessoais realizadas pela DL Soluções Condominiais, independentemente do meio, seja ele digital ou físico. Seu escopo abrange os dados de todos os titulares com os quais a Empresa interage no exercício de suas atividades de administração condominial, incluindo, mas não se limitando a: condôminos, moradores, locatários, funcionários dos condomínios, visitantes, prestadores de serviços, síndicos e membros do corpo diretivo dos condomínios clientes.</p>

<h3>Referência a Padrões Globais</h3>
<p>Embora a atuação da DL Soluções Condominiais esteja juridicamente vinculada à legislação brasileira, suas práticas e políticas internas são informadas pelas melhores práticas globais em matéria de proteção de dados. A Empresa monitora e incorpora, quando aplicável, os princípios e diretrizes estabelecidos em regulamentações internacionais de referência, como o Regulamento Geral sobre a Proteção de Dados (GDPR) (UE) 2016/679. Esta abordagem não apenas reforça a robustez de seu programa de conformidade, mas também posiciona a DL Soluções Condominiais como uma empresa que valoriza a proteção de dados como um diferencial competitivo e um pilar de confiança no mercado.</p>

<h2>Seção 2: Definições Essenciais (Glossário LGPD)</h2>
<p>Para os fins desta Política, e em alinhamento com o Artigo 5º da LGPD, os seguintes termos terão as definições abaixo especificadas:</p>
<ul>
  <li><strong>Dado Pessoal:</strong> Qualquer informação relacionada a uma pessoa natural identificada ou identificável.</li>
  <li><strong>Dado Pessoal Sensível:</strong> Dado pessoal sobre origem racial ou étnica, convicção religiosa, opinião política, filiação a sindicato ou a organização de caráter religioso, filosófico ou político, dado referente à saúde ou à vida sexual, dado genético ou biométrico, quando vinculado a uma pessoa natural.</li>
  <li><strong>Titular:</strong> Pessoa natural a quem se referem os dados pessoais que são objeto de tratamento.</li>
  <li><strong>Tratamento:</strong> Toda e qualquer operação realizada com dados pessoais.</li>
  <li><strong>Controlador:</strong> Pessoa natural ou jurídica a quem competem as decisões referentes ao tratamento de dados pessoais. No contexto dos nossos serviços, o Controlador é, na maioria dos casos, o próprio Condomínio cliente.</li>
  <li><strong>Operador:</strong> Pessoa natural ou jurídica que realiza o tratamento de dados pessoais em nome do Controlador. Este é o papel preponderante da DL Soluções Condominiais.</li>
  <li><strong>Encarregado (DPO):</strong> Pessoa indicada para atuar como canal de comunicação entre o Controlador, os titulares dos dados e a ANPD.</li>
  <li><strong>Autoridade Nacional de Proteção de Dados (ANPD):</strong> Órgão responsável por zelar, implementar e fiscalizar o cumprimento da LGPD.</li>
</ul>

<h2>Seção 3: O Papel da DL Soluções Condominiais no Tratamento de Dados</h2>
<h3>Esclarecimento Fundamental: DL Soluções como Operadora</h3>
<p>Na esmagadora maioria das atividades desempenhadas, a DL Soluções Condominiais atua na qualidade de Operadora de dados pessoais. Neste modelo, o Controlador dos dados é o Condomínio cliente, representado pelo síndico.</p>

<h3>Implicações Legais e Práticas</h3>
<p>Como Operadora, realizamos o tratamento de dados estritamente de acordo com as finalidades e instruções lícitas fornecidas pelo Condomínio. Compete ao Condomínio a responsabilidade primária por definir os propósitos do tratamento e por assegurar que existe uma base legal válida para cada operação.</p>

<h3>Cenários de Atuação como Controladora</h3>
<p>A DL Soluções Condominiais atua como Controladora em cenários específicos e limitados, como:</p>
<ul>
  <li><strong>Recursos Humanos:</strong> Tratamento dos dados de seus próprios colaboradores.</li>
  <li><strong>Atividades Comerciais e de Marketing:</strong> Tratamento de dados de contato de potenciais clientes.</li>
  <li><strong>Gestão de Fornecedores:</strong> Tratamento de dados de seus próprios fornecedores e parceiros.</li>
</ul>

<h2>Seção 4: Dados Pessoais Tratados</h2>
<p>No exercício de suas atividades como Operadora, a DL Soluções Condominiais trata diversas categorias de dados pessoais, estritamente necessários para as finalidades da gestão condominial.</p>
<ul>
  <li><strong>Condôminos, Moradores e Locatários:</strong> Dados Cadastrais, da Unidade Condominial e Financeiros.</li>
  <li><strong>Visitantes e Prestadores de Serviço Terceirizados:</strong> Dados de Identificação e de Segurança (imagens de CFTV).</li>
  <li><strong>Funcionários do Condomínio:</strong> Dados Cadastrais, Contratuais, de Saúde (sensível) e Biométricos (sensível).</li>
  <li><strong>Membros do Corpo Diretivo (Síndico, Subsíndico, Conselheiros):</strong> Dados de Identificação e Contato.</li>
</ul>

<h2>Seção 5: Finalidades e Bases Legais para o Tratamento de Dados</h2>
<p>Todo tratamento de dados está vinculado a finalidades legítimas, específicas e explícitas, conforme determinado pelo Condomínio Controlador. A tabela a seguir detalha as principais atividades:</p>
<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse: collapse; margin-bottom: 30px; margin-top: 15px; font-size: 0.95rem;">
    <thead>
      <tr style="border-bottom: 2px solid var(--dl-border); text-align: left;">
        <th style="padding: 12px;">Categoria de Titulares</th>
        <th style="padding: 12px;">Exemplos de Dados Pessoais Tratados</th>
        <th style="padding: 12px;">Finalidade Principal do Tratamento</th>
        <th style="padding: 12px;">Base Legal (LGPD - Art. 7º)</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid var(--dl-border);">
        <td style="padding: 12px;">Condôminos/Moradores</td>
        <td style="padding: 12px;">Nome, CPF, e-mail, telefone, dados da unidade, dados financeiros.</td>
        <td style="padding: 12px;">Gestão administrativa e financeira; emissão de boletos; envio de comunicados; gestão de inadimplência.</td>
        <td style="padding: 12px;">V - Execução de contrato; II - Cumprimento de obrigação legal; X - Proteção do crédito.</td>
      </tr>
      <tr style="border-bottom: 1px solid var(--dl-border);">
        <td style="padding: 12px;">Visitantes/Prestadores</td>
        <td style="padding: 12px;">Nome, documento, placa do veículo, imagem (CFTV).</td>
        <td style="padding: 12px;">Controle de acesso para garantir a segurança física.</td>
        <td style="padding: 12px;">IX - Legítimo interesse do controlador; VII - Proteção da vida ou da incolumidade física.</td>
      </tr>
      <tr style="border-bottom: 1px solid var(--dl-border);">
        <td style="padding: 12px;">Funcionários do Condomínio</td>
        <td style="padding: 12px;">Dados cadastrais, de saúde, de ponto, bancários.</td>
        <td style="padding: 12px;">Gestão de RH: folha de pagamento, encargos, obrigações trabalhistas.</td>
        <td style="padding: 12px;">V - Execução de contrato; II - Cumprimento de obrigação legal.</td>
      </tr>
      <tr style="border-bottom: 1px solid var(--dl-border);">
        <td style="padding: 12px;">Prestadores de Serviço (Pessoa Física)</td>
        <td style="padding: 12px;">Nome, CPF, contato, dados bancários.</td>
        <td style="padding: 12px;">Cadastro para controle de acesso; gestão de contratos e pagamentos.</td>
        <td style="padding: 12px;">V - Execução de contrato.</td>
      </tr>
      <tr style="border-bottom: 1px solid var(--dl-border);">
        <td style="padding: 12px;">Todos os Titulares</td>
        <td style="padding: 12px;">Dados pessoais pertinentes a cada caso.</td>
        <td style="padding: 12px;">Atendimento a requisições de autoridades competentes.</td>
        <td style="padding: 12px;">VI - Exercício regular de direitos em processo.</td>
      </tr>
    </tbody>
  </table>
</div>

<h2>Seção 6: Compartilhamento de Dados Pessoais</h2>
<p>A DL Soluções Condominiais somente compartilha dados pessoais com terceiros quando estritamente necessário para a execução dos serviços e para o cumprimento das finalidades legítimas. As categorias de destinatários incluem:</p>
<ul>
  <li>Instituições Financeiras e Meios de Pagamento</li>
  <li>Provedores de Tecnologia e Software (SaaS)</li>
  <li>Escritórios de Advocacia e Empresas de Cobrança</li>
  <li>Autoridades Públicas</li>
  <li>Empresas de Contabilidade</li>
  <li>Seguradoras</li>
</ul>

<h2>Seção 7: Direitos dos Titulares de Dados</h2>
<p>A DL Soluções Condominiais respeita e garante aos titulares o exercício de todos os direitos previstos no Artigo 18 da LGPD, como confirmação, acesso, correção, eliminação, portabilidade, entre outros.</p>
<h3>Procedimento para Exercício dos Direitos</h3>
<p>Uma vez que atuamos como Operadora, o titular deve direcionar sua requisição diretamente ao Controlador (o Condomínio). Prestaremos todo o suporte técnico e operacional necessário ao Controlador para que a resposta seja fornecida de forma célere e segura. Nos casos em que atuamos como Controladora, a requisição pode ser feita diretamente à Empresa através do canal do DPO.</p>

<h2>Seção 8: Medidas de Segurança da Informação</h2>
<p>Adotamos um conjunto robusto de medidas de segurança, técnicas e administrativas, para proteger os dados pessoais, incluindo:</p>
<ul>
  <li><strong>Medidas Técnicas:</strong> Controle de Acesso Lógico, Criptografia, Segurança de Rede e Gestão de Backups.</li>
  <li><strong>Medidas Administrativas e Organizacionais:</strong> Políticas Internas, Acordos de Confidencialidade e Treinamento contínuo.</li>
</ul>

<h2>Seção 9: Período de Retenção e Descarte de Dados</h2>
<p>Os dados pessoais são retidos apenas pelo período necessário para o cumprimento das finalidades, obrigações contratuais e requisitos legais. Findo o prazo, os dados são eliminados de forma definitiva e segura.</p>

<h2>Seção 10: Encarregado pela Proteção de Dados (DPO)</h2>
<p>Para exercer seus direitos, esclarecer dúvidas ou enviar qualquer comunicação relacionada a esta Política, o titular deve entrar em contato através do seguinte canal oficial:</p>
<ul>
  <li><strong>Canal de Comunicação:</strong> Encarregado pela Proteção de Dados - DL Soluções Condominiais</li>
  <li><strong>Endereço de E-mail:</strong> sac@dlsolucoescondominiais.com.br</li>
</ul>

<h2>Seção 11: Disposições Gerais e Atualizações da Política</h2>
<p>Esta Política poderá ser atualizada periodicamente. A versão mais recente estará sempre disponível em nosso website. Esta Política é regida pelas leis da República Federativa do Brasil.</p>

<p><em>Última Atualização: 16 de agosto de 2024 | Versão: 1.0</em></p>
`
);

// ============================================================
// POLÍTICA DE COOKIES
// ============================================================
createPage(
  'politica-cookies.html',
  'Política de Cookies | DL Soluções Condominiais',
  'Saiba como a DL Soluções Condominiais utiliza cookies no seu site.',
  `
<h1>Política de Cookies</h1>

<h2>O que são Cookies?</h2>
<p>Cookies são pequenos arquivos de texto armazenados no seu dispositivo quando você visita nosso site. Eles nos ajudam a oferecer uma experiência melhor, lembrar suas preferências e analisar como o site é utilizado.</p>

<h2>Tipos de Cookies Utilizados</h2>

<h3>Cookies Essenciais</h3>
<p>Necessários para o funcionamento básico do site, como o armazenamento da preferência de tema (claro/escuro) e a aceitação de cookies. Não podem ser desativados.</p>

<h3>Cookies de Análise</h3>
<p>Utilizamos o Google Analytics para entender como os visitantes interagem com o site, permitindo melhorias contínuas na experiência de navegação.</p>

<h3>Cookies de Publicidade</h3>
<p>O Google Ads e o Meta Pixel utilizam cookies para medir a eficácia das campanhas publicitárias e exibir anúncios relevantes. Estes cookies só são ativados após o seu consentimento.</p>

<h2>Como Gerenciar Cookies</h2>
<p>Você pode aceitar ou rejeitar cookies não essenciais através do banner exibido na sua primeira visita. Também pode configurar seu navegador para bloquear ou excluir cookies a qualquer momento.</p>

<h2>Cookies de Terceiros</h2>
<p>Google Analytics, Google Ads, Meta Pixel e plataformas de atendimento integradas podem definir seus próprios cookies conforme suas respectivas políticas de privacidade.</p>

<p><em>Última atualização: Junho de 2026.</em></p>
`
);

// ============================================================
// TERMOS DE USO
// ============================================================
createPage(
  'termos-de-uso.html',
  'Termos de Uso | DL Soluções Condominiais',
  'Termos de Uso do site da DL Soluções Condominiais.',
  `
<h1>Termos de Uso</h1>

<h2>1. Aceitação dos Termos</h2>
<p>Ao acessar e utilizar o site da DL Soluções Condominiais (dlsolucoescondominiais.com.br), você concorda com os presentes Termos de Uso. Caso não concorde, solicitamos que interrompa a utilização do site.</p>

<h2>2. Descrição dos Serviços</h2>
<p>O site tem como objetivo apresentar os serviços da DL Soluções Condominiais LTDA (CNPJ 36.354.697/0001-46), facilitar o contato comercial e a solicitação de Avaliação Técnica para condomínios, colégios e empresas no Rio de Janeiro.</p>

<h2>3. Propriedade Intelectual</h2>
<p>Todo o conteúdo do site — textos, imagens, logotipos, design e código-fonte — é de propriedade da DL Soluções Condominiais e está protegido pela legislação brasileira de direitos autorais. A reprodução não autorizada é proibida.</p>

<h2>4. Uso Adequado</h2>
<p>O usuário compromete-se a utilizar o site de forma ética e legal, sendo proibido: utilizar o site para fins ilícitos; tentar acessar áreas restritas; enviar conteúdo malicioso ou spam através dos formulários.</p>

<h2>5. Limitação de Responsabilidade</h2>
<p>A DL Soluções Condominiais envidará esforços para manter o site disponível e atualizado, mas não garante a ininterruptibilidade do serviço. Orçamentos e avaliações técnicas apresentados no site são estimativas e estão sujeitos a confirmação após análise presencial.</p>

<h2>6. Legislação Aplicável</h2>
<p>Estes Termos são regidos pelas leis da República Federativa do Brasil, com foro da Comarca do Rio de Janeiro, RJ.</p>

<p><em>Última atualização: Junho de 2026.</em></p>
`
);

// ============================================================
// LGPD / GDPR — DIREITOS DO TITULAR
// ============================================================
createPage(
  'lgpd-gdpr.html',
  'Direitos do Titular LGPD | DL Soluções Condominiais',
  'Conheça seus direitos como titular de dados pessoais conforme a LGPD na DL Soluções Condominiais.',
  `
<h1>Direitos do Titular — LGPD</h1>

<h2>Seus Direitos</h2>
<p>A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) garante a você, titular dos dados, os seguintes direitos:</p>

<ul>
  <li><strong>Confirmação de tratamento:</strong> Confirmar se a DL trata seus dados pessoais.</li>
  <li><strong>Acesso aos dados:</strong> Solicitar uma cópia dos dados pessoais que mantemos sobre você.</li>
  <li><strong>Correção:</strong> Solicitar a correção de dados incompletos, inexatos ou desatualizados.</li>
  <li><strong>Anonimização, bloqueio ou eliminação:</strong> Solicitar a anonimização ou eliminação de dados desnecessários.</li>
  <li><strong>Portabilidade:</strong> Solicitar a transferência dos seus dados a outro fornecedor.</li>
  <li><strong>Eliminação:</strong> Solicitar a eliminação dos dados tratados com seu consentimento.</li>
  <li><strong>Informação sobre compartilhamento:</strong> Saber com quais entidades seus dados são compartilhados.</li>
  <li><strong>Revogação do consentimento:</strong> Revogar seu consentimento a qualquer momento.</li>
</ul>

<h2>Como Exercer seus Direitos</h2>
<p>Para exercer qualquer dos direitos acima, entre em contato através dos canais oficiais de atendimento da DL Soluções Condominiais. Responderemos sua solicitação no prazo legal de 15 dias.</p>

<h2>Encarregado de Dados (DPO)</h2>
<p>A DL Soluções Condominiais designou um responsável pelo tratamento de dados pessoais, acessível através dos canais de atendimento da empresa.</p>

<p><em>Última atualização: Junho de 2026.</em></p>
`
);

// ============================================================
// POLÍTICA DE ATENDIMENTO DIGITAL
// ============================================================
createPage(
  'politica-atendimento.html',
  'Política de Atendimento Digital | DL Soluções Condominiais',
  'Política de Atendimento Digital da DL Soluções Condominiais. Saiba como funciona nosso atendimento via WhatsApp, Telegram e canais digitais.',
  `
<h1>Política de Atendimento Digital</h1>

<h2>Canais de Atendimento</h2>
<p>A DL Soluções Condominiais disponibiliza atendimento digital através dos seguintes canais oficiais:</p>
<ul>
  <li><strong>WhatsApp Comercial:</strong> Acessível exclusivamente através dos botões de atendimento do nosso site.</li>
  <li><strong>Telegram:</strong> Acessível exclusivamente através do ícone de Telegram do nosso site.</li>
  <li><strong>E-mail:</strong> Através do formulário de contato do site.</li>
</ul>

<h2>Horário de Atendimento</h2>
<p>O atendimento comercial funciona de segunda a sexta-feira, das 08h às 18h, e aos sábados das 08h às 13h. Solicitações fora deste horário serão respondidas no próximo dia útil.</p>

<h2>Assistente Virtual (Aninha)</h2>
<p>Utilizamos uma assistente virtual inteligente para realizar a triagem inicial das solicitações, garantindo que você seja direcionado ao departamento correto de forma rápida e eficiente. A assistente pode solicitar informações básicas como nome, tipo de imóvel e região para agilizar o atendimento.</p>

<h2>Avaliação Técnica</h2>
<p>A solicitação de Avaliação Técnica é gratuita e pode ser feita através de qualquer canal de atendimento. Após a triagem, um especialista entrará em contato para agendar a avaliação presencial no local.</p>

<h2>SLA de Resposta</h2>
<p>Nos comprometemos a responder todas as solicitações em até 4 horas dentro do horário comercial. Solicitações urgentes serão priorizadas conforme a criticidade.</p>

<p><em>Última atualização: Junho de 2026.</em></p>
`
);

// ============================================================
// PORTFÓLIO COMPLETO
// ============================================================
createPage(
  'portifolio.html',
  'Portfólio de Obras | DL Soluções Condominiais',
  'Portfólio de obras e instalações da DL Soluções Condominiais: CFTV, elétrica predial, energia solar, controle de acesso e automação para condomínios no RJ.',
  `
<h1>Portfólio de Obras e Instalações</h1>
<p>Conheça nossos cases de sucesso em elétrica predial, montagem de quadros de comando, instalação de CFTV, controle de acesso e usinas solares para condomínios no Rio de Janeiro.</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 28px; margin-top: 40px;">
  <div style="background: var(--dl-surface); border: 1px solid var(--dl-border); border-radius: var(--radius-md); overflow: hidden;">
    <div style="height: 200px; background: url('assets/cftv.png') center/cover;"></div>
    <div style="padding: 24px;">
      <h3 style="margin-top: 0;">Instalação de CFTV Intelbras — 64 Câmeras IP</h3>
      <p style="color: var(--dl-text-muted);">Condomínio de grande porte na Barra da Tijuca. Sistema completo com NVR dedicado e acesso remoto para síndico e administradora.</p>
    </div>
  </div>
  
  <div style="background: var(--dl-surface); border: 1px solid var(--dl-border); border-radius: var(--radius-md); overflow: hidden;">
    <div style="height: 200px; background: url('assets/solar.png') center/cover;"></div>
    <div style="padding: 24px;">
      <h3 style="margin-top: 0;">Usina Solar Fotovoltaica — 24 Painéis</h3>
      <p style="color: var(--dl-text-muted);">Instalação de usina solar para área comum de condomínio no Recreio dos Bandeirantes. Redução de 90% na conta de energia.</p>
    </div>
  </div>
  
  <div style="background: var(--dl-surface); border: 1px solid var(--dl-border); border-radius: var(--radius-md); overflow: hidden;">
    <div style="height: 200px; background: url('assets/controle_acesso.png') center/cover;"></div>
    <div style="padding: 24px;">
      <h3 style="margin-top: 0;">Controle de Acesso Biométrico Facial</h3>
      <p style="color: var(--dl-text-muted);">Sistema de acesso facial e biometria para 200 moradores em condomínio na Tijuca, com integração de portaria remota.</p>
    </div>
  </div>

  <div style="background: var(--dl-surface); border: 1px solid var(--dl-border); border-radius: var(--radius-md); overflow: hidden;">
    <div style="height: 200px; background: url('assets/eletrica.png') center/cover;"></div>
    <div style="padding: 24px;">
      <h3 style="margin-top: 0;">Retrofit Elétrico Completo — Edifício dos Anos 80</h3>
      <p style="color: var(--dl-text-muted);">Substituição integral da infraestrutura elétrica, novos quadros QGBT e obtenção do AVCB junto ao CBMERJ.</p>
    </div>
  </div>
</div>
`
);

// ============================================================
// QUEM SOMOS (Redirect para A Empresa)
// ============================================================
createPage(
  'quem-somos.html',
  'Quem Somos | DL Soluções Condominiais',
  'Conheça a DL Soluções Condominiais e sua missão de oferecer proteção patrimonial e tecnologia para condomínios no RJ.',
  `
<h1>Quem Somos</h1>
<p>A DL Soluções Condominiais é uma empresa especializada em proteção patrimonial, segurança eletrônica, elétrica predial, automação e energia solar para condomínios, colégios e empresas no Rio de Janeiro.</p>
<p>Para conhecer nossa história completa, <a href="a-empresa.html">visite a página A Empresa</a> ou conheça <a href="o-fundador.html">O Fundador</a>.</p>
`
);

console.log('\n✅ Todas as páginas internas foram geradas com sucesso (Fortress v1).');
console.log('📋 Páginas criadas: a-empresa, o-fundador, politica-privacidade, politica-cookies, termos-de-uso, lgpd-gdpr, politica-atendimento, portifolio, quem-somos');
