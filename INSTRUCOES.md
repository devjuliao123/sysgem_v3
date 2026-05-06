# SysGEM Unified - Guia de Início Rápido

Este projeto unifica o sistema administrativo e operacional em uma única aplicação Flask multi-tenant.

## Pré-requisitos

- Python 3.10+
- PostgreSQL rodando localmente

## Instalação

1. Instale as dependências:
   ```bash
   pip install flask psycopg2-binary python-dotenv
   ```

2. Configure as variáveis de ambiente:
   - No diretório raiz do projeto, crie um arquivo chamado `.env` (você pode copiar o `.env.example`).
   - Edite o `.env` e preencha a sua senha do PostgreSQL:
     ```env
     DB_PASSWORD=sua_senha_aqui
     ```

## Como Rodar no Windows

1. Abra o Terminal ou PowerShell na pasta do projeto.
2. Execute o comando:
   ```bash
   python run.py
   ```

## Acesso ao Sistema

- **Admin (Gestão de Igrejas):** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
- **App (Operacional):** Após criar uma igreja no Admin, clique no botão **"Acessar"**.

## Solução de Problemas de Conexão

Se você vir o erro `psycopg2.OperationalError: ... fe_sendauth: no password supplied`:

1. **Arquivo .env:** Verifique se o arquivo se chama exatamente `.env` (sem .txt no final) e se está na mesma pasta que o `run.py`.
2. **Senha:** Certifique-se que a senha no `.env` é a mesma do seu usuário `postgres`.
3. **Variáveis de Sistema:** Alternativamente, você pode definir a senha diretamente no terminal antes de rodar (Windows PowerShell):
   ```powershell
   $env:DB_PASSWORD="sua_senha_aqui"
   python run.py
   ```
