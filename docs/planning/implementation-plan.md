# Plano de implementação

## Estratégia

A implementação será incremental, com uma responsabilidade principal por pull request. Cada etapa deve preservar a aplicação executável e incluir testes, documentação e validação automatizada.

## Versões

### v0.1.0 — Fundação e catálogo

- bootstrap FastAPI;
- configuração e observabilidade básica;
- MongoDB;
- domínio de livros;
- CRUD do catálogo;
- deduplicação por ISBN;
- Docker e CI.

### v0.2.0 — Enriquecimento

- Google Books;
- Open Library;
- modelo canônico de metadados;
- busca por título, autor ou ISBN;
- fallback, timeout e retry;
- confirmação antes de salvar.

### v0.3.0 — Jornada de leitura

- status;
- progresso;
- datas de início e conclusão;
- avaliação;
- comentários.

### v0.4.0 — Automação com n8n

- execução assíncrona de enriquecimento;
- callbacks autenticados;
- idempotência;
- tratamento de erro e reprocessamento;
- notificações.

### v0.5.0 — Telegram

- cadastro;
- busca;
- consulta da biblioteca;
- status e progresso;
- confirmação de operações.

### v0.6.0 — Frontend

- biblioteca;
- filtros;
- cadastro;
- confirmação de metadados;
- detalhes e progresso.

### v1.0.0 — MVP estável

- fluxo completo integrado;
- segurança revisada;
- observabilidade;
- backup;
- deploy;
- testes end-to-end;
- documentação operacional.

## Sequência de pull requests

1. `PR-001` — bootstrap do backend;
2. `PR-002` — domínio de livros;
3. `PR-003` — persistência MongoDB;
4. `PR-004` — casos de uso do catálogo;
5. `PR-005` — API do catálogo;
6. `PR-006` — provedores de metadados;
7. `PR-007` — enriquecimento e confirmação;
8. `PR-008` — jornada de leitura;
9. `PR-009` — workflows n8n;
10. `PR-010` — integração Telegram;
11. `PR-011` — frontend inicial;
12. `PR-012` — hardening e entrega do MVP.

## Definition of Ready

Uma tarefa está pronta para implementação quando possui:

- objetivo claro;
- escopo e itens fora do escopo;
- critérios de aceite verificáveis;
- dependências identificadas;
- riscos conhecidos;
- contrato ou comportamento esperado;
- estratégia de testes.

## Definition of Done

Uma tarefa está concluída quando:

- critérios de aceite foram atendidos;
- testes unitários e de integração necessários foram adicionados;
- lint, typecheck, testes e build passam;
- documentação foi atualizada;
- não há segredos ou dados sensíveis versionados;
- logs e erros seguem o padrão do projeto;
- revisão de segurança foi realizada quando aplicável;
- pull request está pequeno e revisável.
