# SPEC-001 — Fundação do projeto

## Objetivo

Criar uma base técnica executável, testável e segura para o CodexAthenae.

## Escopo

- FastAPI com application factory e lifespan;
- configuração por variáveis de ambiente;
- PyMongo Async e MongoDB;
- health checks de liveness e readiness;
- logs estruturados;
- Docker e Docker Compose;
- lint, formatação, type checking e testes;
- GitHub Actions.

## Critérios de aceite

- `GET /health/live` retorna `200` sem depender de serviços externos;
- `GET /health/ready` verifica a disponibilidade do MongoDB;
- conexões são abertas e encerradas pelo lifespan;
- nenhuma credencial é versionada;
- testes não chamam serviços externos reais;
- um único comando executa lint, tipos e testes;
- a CI executa em pull requests;
- a aplicação pode ser iniciada localmente por Docker Compose.

## Fora do escopo

- domínio de livros;
- autenticação;
- frontend;
- Telegram;
- n8n.

## Testes mínimos

- health check de liveness;
- readiness com MongoDB disponível e indisponível;
- carregamento de configurações;
- inicialização e encerramento da aplicação.
