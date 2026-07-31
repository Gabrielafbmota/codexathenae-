# Backlog inicial

## PR-001 — Bootstrap do backend

- [ ] Criar `pyproject.toml` e fixar versão suportada do Python.
- [ ] Configurar FastAPI, Pydantic Settings e servidor ASGI.
- [ ] Criar application factory e lifespan.
- [ ] Configurar logs estruturados e correlation ID.
- [ ] Criar health checks.
- [ ] Configurar Ruff, type checking, pytest e coverage.
- [ ] Criar Dockerfile e Docker Compose.
- [ ] Criar workflow de CI.
- [ ] Documentar execução local.

## PR-002 — Domínio de livros

- [ ] Criar `Book`, `BookId`, `ISBN`, `ReadingStatus` e `ReadingProgress`.
- [ ] Implementar invariantes e exceções de domínio.
- [ ] Usar datas timezone-aware.
- [ ] Criar testes unitários e arquiteturais.

## PR-003 — Persistência MongoDB

- [ ] Definir porta `BookRepository`.
- [ ] Implementar adaptador com PyMongo Async.
- [ ] Criar mapeadores domínio/documento.
- [ ] Criar índices idempotentes e índice único parcial para ISBN.
- [ ] Implementar paginação, filtros e soft delete.
- [ ] Criar testes de integração com MongoDB real em container.

## PR-004 — Casos de uso do catálogo

- [ ] Implementar criação, consulta, listagem, atualização e exclusão.
- [ ] Padronizar modelos de entrada e saída da aplicação.
- [ ] Traduzir erros de persistência para erros da aplicação.
- [ ] Criar testes unitários por caso de uso.

## PR-005 — API do catálogo

- [ ] Criar schemas e routers.
- [ ] Configurar injeção de dependências.
- [ ] Padronizar respostas de erro.
- [ ] Implementar paginação e filtros HTTP.
- [ ] Criar testes de contrato e integração.

## PR-006 — Provedores de metadados

- [ ] Definir porta `BookMetadataProvider`.
- [ ] Implementar Google Books e Open Library.
- [ ] Configurar timeout, retry seletivo e rate limit.
- [ ] Normalizar respostas externas.
- [ ] Criar testes com `httpx.MockTransport`.

## PR-007 — Enriquecimento

- [ ] Implementar busca por ISBN e título/autor.
- [ ] Combinar, pontuar e deduplicar candidatos.
- [ ] Implementar confirmação separada da busca.
- [ ] Registrar origem dos dados.
- [ ] Criar testes do fluxo completo.

## PR-008 — Jornada de leitura

- [ ] Implementar transições de status.
- [ ] Registrar início, conclusão, progresso, avaliação e comentários.
- [ ] Criar histórico básico.
- [ ] Criar testes de domínio, aplicação e API.

## PR-009 — n8n

- [ ] Adicionar serviço local do n8n.
- [ ] Criar webhooks autenticados e callbacks.
- [ ] Implementar idempotência, retry, fallback e workflow de erro.
- [ ] Exportar workflows sem segredos.
- [ ] Criar documentação operacional e testes de integração.

## PR-010 — Telegram

- [ ] Configurar bot e allowlist.
- [ ] Implementar comandos e estados de conversação.
- [ ] Adicionar confirmação, cancelamento e expiração.
- [ ] Integrar exclusivamente pela API.
- [ ] Criar testes automatizados.

## Definition of Ready

Uma tarefa está pronta quando possui objetivo, escopo, critérios de aceite, dependências, riscos e estratégia de testes claros.

## Definition of Done

Uma tarefa está concluída quando código e documentação foram atualizados, lint e tipos passam, testes automatizados passam, segurança foi revisada e não existem pendências ocultas fora do escopo declarado.
