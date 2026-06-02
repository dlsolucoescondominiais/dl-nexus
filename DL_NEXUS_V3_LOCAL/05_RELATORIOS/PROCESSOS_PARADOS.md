# Relatório de Processos Internos Parados

## 1. Aprovação Manual via Webhook (DL-APROVAR-POST)
**Motivo da Parada:** Transição estratégica para Autopublicação.
**Status:** Substituído pelo nó `Validar KILLCRITIC` automatizado no workflow `013_MAQUINA_DE_ATRACAO`. O fluxo manual só será usado como fallback explícito. O gargalo da aprovação manual foi eliminado para ganho de escala.

## 2. Publicação via TikTok
**Motivo da Parada:** Necessidade de credenciais específicas / API do TikTok restrita.
**Status:** O workflow `013_MAQUINA_DE_ATRACAO` foca nos canais liberados: Facebook, Instagram e Google Business Profile. O TikTok permanece configurado como falso ou aguardando credencial (via nó `084_PUBLICADOR_TIKTOK_ASSISTIDO`), devendo ser ativado posteriormente sem travar os outros canais.

## 3. Integrações Diretas de E-mail para Prospecção Fria
**Motivo da Parada:** Protocolo KILLCRITIC V3.
**Status:** As regras do KILLCRITIC (especificamente sobre a máquina do Manus Prospecção) desativaram mensagens de WhatsApp frias (cold outreach) automáticas. Prospecção agora direciona para webhooks específicos de `leads` em vez de mandar mensagens prontas sem aprovação de orçamento ou SLA.

## 4. Oferta de Garantia Vitalícia / Preço Final
**Motivo da Parada:** Ajuste Comercial.
**Status:** Aninha e Diego não podem enviar preços finais sem Avaliação Técnica, nem garantia sem SLA ativo (DL Partner). Nodes de formatação de preço foram refatorados para sempre indicar "a partir de".
