# 🚀 Backend com FastAPI, Redis, PostgreSQL e LangChain (Completo)

Este projeto demonstra um backend escalável em **Python (FastAPI)** com:
- APIs RESTful
- Persistência em **PostgreSQL**
- Cache em **Redis**
- Integração com **LLMs (LangChain + OpenAI/Azure)**
- Containerização com **Docker Compose**
- **CI (GitHub Actions) rodando pytest**
- **Autenticação JWT** (rota /auth)

---

## 📌 Como Rodar Localmente (Docker)
1) Crie o arquivo `.env` a partir do `.env.example` e preencha sua `OPENAI_API_KEY` e `JWT_SECRET`:
```bash
cp .env.example .env
# edite .env e coloque OPENAI_API_KEY e JWT_SECRET
```

2) Para rodar com live-reload durante o desenvolvimento (usa docker-compose.override.yml):
```bash
docker-compose up --build
```
O `docker-compose.override.yml` monta o volume local e executa Uvicorn com `--reload`.

3) Acesse:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

---

## 🔐 Autenticação (JWT)
Endpoints em `/auth`:
- `POST /auth/register` → registra usuário (name, email, password)  
- `POST /auth/login` → faz login e retorna `access_token`

Exemplo de uso após obter token (substitua `<TOKEN>`):
```
Authorization: Bearer <TOKEN>
```

> Observação: por simplicidade e foco didático, as credenciais são armazenadas em um arquivo `.user_credentials` no container/local (não para produção). Em um projeto real, adicione coluna `password_hash` na tabela `users` e gerencie com migrações (Alembic) e secrets manager.

---

## 🚀 Passo a passo para subir no GitHub
... (mesma instrução do README anterior)
