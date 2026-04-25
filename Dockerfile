# Base image otimizada
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte (Antigravity e Execution)
COPY antigravity/ antigravity/
COPY execution/ execution/
# Cria arquivo __init__.py na raiz do execution caso não exista (para imports funcionarem)
RUN touch execution/__init__.py

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando de inicialização
CMD ["uvicorn", "antigravity.main:app", "--host", "0.0.0.0", "--port", "8000"]
