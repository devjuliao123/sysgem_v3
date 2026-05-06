# SysGEM Unified - Guia de Início Rápido

Este projeto unifica o sistema administrativo e operacional em uma única aplicação Flask multi-tenant.

## Pré-requisitos

- Python 3.10+
- PostgreSQL rodando localmente

## Instalação

1. Instale as dependências:
   ```bash
   pip install flask psycopg2-binary
   ```

2. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o `.env` com suas credenciais do PostgreSQL (principalmente `DB_PASSWORD`)

## Como Rodar

Execute o arquivo principal:
```bash
python run.py
```

- **Admin (Gestão de Igrejas/Schemas):** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
- **App (Operacional):** Após criar uma organização no Admin, clique em "Acessar" para entrar no sistema do usuário.

## Solução de Problemas

### Erro: `fe_sendauth: no password supplied` ou `Connection refused`
Isso significa que o Flask não conseguiu conectar ao seu PostgreSQL.
1. Certifique-se que o PostgreSQL está ativo.
2. Certifique-se que você definiu a senha correta no arquivo `.env` ou como variável de ambiente `DB_PASSWORD`.
