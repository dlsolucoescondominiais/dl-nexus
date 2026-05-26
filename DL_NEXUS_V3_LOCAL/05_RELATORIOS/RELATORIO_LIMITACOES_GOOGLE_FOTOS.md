# Limitações: Integração Google Fotos

A API do Google Fotos difere essencialmente da API do Google Drive em termos de governança de arquivos:
1. **Somente Leitura e Álbuns Isolados:** A API do Google Fotos não permite mover imagens nativamente da galeria primária para organizar de forma invisível. Arquivos criados fora do escopo da API só podem ser lidos se o usuário conceder a permissão máxima, e a organização se dá por álbuns lógicos, e não pastas físicas (hierárquicas).
2. **Perda de Contexto e Dados Sensíveis:** Muitas mídias no Google Fotos sofrem stripping de EXIF ou alteração estrutural dependendo do plano de armazenamento, o que prejudica a identificação de metadados críticos.
3. **Decisão Arquitetural DL Nexus:** Todo o fluxo do *Zelador* priorizará exclusivamente a API do Google Drive. Imagens do celular devem ser trafegadas para o ecossistema do Drive (ex: upload automático para pastas Inboxes no Drive) para que o Zelador as categorize com segurança e crie o inventário real de marketing B2B. Mídias exclusivas do Google Fotos poderão apenas ter inventário passivo (se houver permissão), mas não serão movidas nativamente pela automação.
