-- =============================================
-- DL NEXUS - SEED DE DADOS PARA DESENVOLVIMENTO
-- =============================================

-- Inserindo um Lead de Teste (Condomínio Solar)
INSERT INTO leads (nome_contato, nome_condominio, telefone, email, tipo_imovel, num_unidades, mensagem, tipo_servico, status, porte, origem)
VALUES
('João Síndico', 'Condomínio Solar da Barra', '5521999999999', 'joao@solar.com', 'Condominio', 120, 'Gostaria de orçar painéis solares para as áreas comuns.', 'SOLAR', 'novo', 'grande', 'whatsapp'),
('Maria Zeladora', 'Edifício Central', '5521888888888', 'maria@central.com', 'Condominio', 40, 'As câmeras do elevador pifaram.', 'SEGURANCA', 'triado', 'pequeno', 'whatsapp'),
('Carlos Diretor', 'Colégio Aprender', '5521777777777', 'diretoria@aprender.com.br', 'Colegio', 500, 'Precisamos reformar o cabeamento de rede da escola toda.', 'ELETRICO', 'agendado', 'complexo', 'site');

-- Inserindo Histórico de Mensagens de Teste
INSERT INTO mensagens_whatsapp (telefone, nome_contato, mensagem, direcao, lida)
VALUES
('5521999999999', 'João Síndico', 'Olá, tudo bem? Quero orçar energia solar.', 'entrada', true),
('5521999999999', 'Aninha IA', 'Olá, João! Sou a Aninha, assistente da DL Soluções Condominiais. Como posso ajudar com a energia solar do seu condomínio?', 'saida', true),
('5521888888888', 'Maria Zeladora', 'As câmeras pararam. Socorro!', 'entrada', false);
