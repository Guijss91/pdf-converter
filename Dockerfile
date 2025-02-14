FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação
COPY . .

# Expõe a porta 5000
EXPOSE 5000

# Comando para rodar a API
CMD ["python", "app.py"]
