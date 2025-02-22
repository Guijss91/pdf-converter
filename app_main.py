from flask import Flask, request, jsonify, send_from_directory
import os
from weasyprint import HTML
from datetime import datetime

app = Flask(__name__)

# Diretório onde os PDFs serão armazenados
PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    """Rota raiz que sinaliza que a API está rodando"""
    return "we're on boys"

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    """Recebe um JSON e gera um PDF com os dados"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido ou vazio"}), 400

    # Criando um template HTML simples a partir do JSON
    html_content = f"""
    <html>
    <head><title>Relatório</title></head>
    <body>
        <h1>Dados Recebidos</h1>
        <ul>
            {''.join(f'<li><b>{key}</b>: {value}</li>' for key, value in data.items())}
        </ul>
    </body>
    </html>
    """

    # Nome do arquivo com timestamp
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_path = os.path.join(PDF_FOLDER, filename)

    # Gerando o PDF
    HTML(string=html_content).write_pdf(pdf_path)

    return jsonify({"message": "PDF gerado com sucesso!", "pdf_url": f"/download_pdf/{filename}"}), 201

@app.route("/download_pdf/<filename>", methods=["GET"])
def download_pdf(filename):
    """Endpoint para baixar o PDF gerado"""
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
