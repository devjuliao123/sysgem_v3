import os
from dotenv import load_dotenv
from app import create_app

# Carrega variáveis de ambiente do arquivo .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print(f"Carregando configurações de: {env_path}")
    load_dotenv(env_path)
else:
    print("Aviso: Arquivo .env não encontrado. Usando variáveis de ambiente do sistema.")

app = create_app()

if __name__ == '__main__':
    print("="*50)
    print("SYSGEM Unified Iniciando...")
    print(f"Banco de Dados: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}")
    print(f"Usuário: {os.getenv('DB_USER', 'postgres')}")
    print(f"Senha definida: {'SIM' if os.getenv('DB_PASSWORD') else 'NÃO'}")
    print("Admin: http://127.0.0.1:5000/admin")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)
