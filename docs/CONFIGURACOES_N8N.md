
---

## 3. Comandos de Deploy na HostGator (VPS)

1. Acesse via SSH a sua VPS:
   `ssh root@ip-da-vps`
2. Crie uma pasta para o n8n e entre nela:
   `mkdir -p /opt/dl-nexus-n8n && cd /opt/dl-nexus-n8n`
3. Crie o arquivo `.env` com todas as variáveis secretas mapeadas acima.
4. Jogue os arquivos `docker-compose.yml` e `Caddyfile` do repositório (`backend/n8n/`) nesta pasta.
5. Inicie o sistema de orquestração:
   `docker-compose up -d`
