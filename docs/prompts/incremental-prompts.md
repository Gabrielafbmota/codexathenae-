# Prompts incrementais de implementação

## Regras gerais

Cada prompt deve ser executado isoladamente. O agente deve inspecionar o repositório antes de alterar arquivos, respeitar o escopo, executar validações e relatar arquivos modificados, decisões, comandos, resultados e pendências.

---

## Prompt 00 — Inspeção inicial

```text
Analise o repositório CodexAthenae antes de realizar qualquer alteração.

Objetivos:
1. identificar estrutura, versões, gerenciador de dependências e ferramentas;
2. mapear arquivos, responsabilidades, testes e decisões já existentes;
3. comparar o estado atual com docs/specifications e docs/planning;
4. identificar inconsistências, riscos de regressão e dúvidas bloqueantes;
5. propor a menor sequência segura de implementação.

Não altere arquivos e não suponha que algo não existe sem verificar.
```

## Prompt 01 — Bootstrap FastAPI

```text
Implemente somente a fundação FastAPI descrita na SPEC-001.

Inclua estrutura de camadas, application factory, lifespan, Pydantic Settings, GET /health/live e testes.
Não integre MongoDB, domínio de livros, autenticação, Telegram ou n8n.
Use tipagem estrita e as convenções existentes.
Execute lint, typecheck e testes.
```

## Prompt 02 — MongoDB e readiness

```text
Implemente apenas a conexão MongoDB com PyMongo Async e o endpoint GET /health/ready.

A conexão deve ser criada e encerrada no lifespan, nunca por requisição. Adicione configurações por ambiente, tratamento de indisponibilidade e testes. Não crie repositórios de domínio ainda.
Execute lint, typecheck e testes.
```

## Prompt 03 — Domínio de livros

```text
Implemente somente Book, BookId, ISBN, ReadingStatus, ReadingProgress e exceções de domínio conforme a SPEC-002.

ISBN deve normalizar espaços e hífens e validar checksums ISBN-10 e ISBN-13. O domínio não pode importar FastAPI, Pydantic ou PyMongo. Use datas timezone-aware e proteja invariantes.
Adicione testes unitários completos. Não implemente persistência ou endpoints.
```

## Prompt 04 — Porta de persistência

```text
Implemente apenas a abstração BookRepository na camada application.

Inclua create, get_by_id, get_by_isbn, list, update e soft_delete, além dos critérios de consulta estritamente necessários. Não importe PyMongo nem exponha documentos de banco.
Adicione testes arquiteturais impedindo domain e application de importar infrastructure.
```

## Prompt 05 — Adaptador MongoDB

```text
Implemente somente o adaptador MongoDB de BookRepository usando PyMongo Async.

Inclua mapeadores, índices idempotentes, índice único parcial para ISBN, paginação, filtros e soft delete. Traduza DuplicateKeyError para erro da aplicação e não exponha objetos PyMongo.
Crie testes de integração com MongoDB real em container, incluindo concorrência de ISBN duplicado.
```

## Prompt 06 — Caso de uso CreateBook

```text
Implemente somente CreateBook.

Entrada: título, autores, ISBN opcional e status opcional. Normalize e valide, verifique duplicidade, crie a entidade, persista e retorne modelo independente do banco.
Cubra criação com e sem ISBN, duplicidade, dados inválidos e falha de persistência. Não crie endpoint.
```

## Prompt 07 — Endpoint POST /books

```text
Implemente apenas POST /api/v1/books.

Crie schemas separados, injete CreateBook, retorne 201 e Location, mapeie duplicidade para 409 e entrada inválida para 422. Nenhuma regra de negócio deve ficar no router.
Adicione testes de contrato, payload inválido, headers e campos internos não expostos.
```

## Prompt 08 — Demais operações do catálogo

```text
Implemente get, list, update e soft delete do catálogo, primeiro na aplicação e depois na API.

Inclua paginação com limite máximo, filtros por status, 404 consistente e exclusão lógica. Não implemente enriquecimento ou jornada de leitura.
Adicione testes unitários, integração e contrato.
```

## Prompt 09 — Google Books

```text
Implemente somente o adaptador Google Books para BookMetadataProvider.

Use httpx.AsyncClient injetado, timeout explícito, limite de resultados, busca por ISBN e título/autor, e modelo canônico. Não persista resultados. Trate 429 e 5xx como transitórios e não repita 4xx definitivos.
Teste com httpx.MockTransport: sucesso, vazio, 429, 500, timeout, JSON inválido e payload incompleto.
```

## Prompt 10 — Open Library

```text
Implemente o adaptador Open Library usando o mesmo contrato canônico.

Mantenha comportamento consistente com Google Books. Cubra ISBN, título, nenhum resultado, timeout, payload incompleto e normalização. Não implemente ainda a orquestração de fallback.
```

## Prompt 11 — Pesquisa e fallback

```text
Implemente somente SearchBookMetadata conforme a SPEC-003.

Consulte Google Books, use Open Library como fallback ou complemento, normalize, deduplique, ordene por relevância e retorne no máximo 10 candidatos. Não salve ou altere livros.
Teste resultado primário, fallback, combinação, duplicidade, vazio, um provedor indisponível e todos indisponíveis.
```

## Prompt 12 — Confirmação do enriquecimento

```text
Implemente apenas a confirmação de um candidato de metadados.

A operação deve receber book_id, candidato e campos aprovados, preservar dados confirmados não selecionados, registrar origem e data e ser idempotente. Não aceite payload bruto de provedor como documento de banco.
Adicione testes de precedência, confirmação parcial, concorrência e repetição.
```

## Prompt 13 — Jornada de leitura

```text
Implemente a SPEC-004 em etapas: primeiro regras de domínio, depois casos de uso e por último endpoints.

Inclua status, progresso por páginas ou percentual, datas de início e conclusão, rating de 1 a 5 em incrementos de 0,5, comentários e histórico básico.
Cubra transições permitidas e inválidas. Não implemente lembretes ainda.
```

## Prompt 14 — n8n local

```text
Implemente somente a base local do n8n conforme a SPEC-005.

Adicione serviço no Docker Compose, variáveis documentadas, persistência local e acesso protegido. Não crie workflows de produção nem versione segredos.
Valide inicialização, health check e isolamento da rede.
```

## Prompt 15 — Workflow de enriquecimento

```text
Crie e versione o workflow n8n de enriquecimento.

Inclua webhook autenticado, idempotency key, Google Books, fallback Open Library, callback para FastAPI, retry com backoff e workflow de erro. Regras de persistência e domínio permanecem na API.
Exporte o JSON sem credenciais e documente importação, configuração e reprocessamento.
```

## Prompt 16 — Telegram

```text
Implemente a integração Telegram conforme a SPEC-006, começando por autorização e um único comando /buscar.

Use allowlist, rate limit, correlation ID e acesso exclusivo pela API. Adicione testes para usuário autorizado, não autorizado, sucesso, vazio, timeout e erro da API. Não implemente os demais comandos nesta tarefa.
```

## Prompt 17 — Revisão final da entrega

```text
Revise a implementação concluída contra a especificação e o planejamento correspondentes.

Não altere arquivos inicialmente. Verifique escopo, arquitetura, segurança OWASP, tratamento de erros, observabilidade, testes, documentação, dependências, segredos e regressões.
Classifique achados por severidade, cite arquivos e linhas, indique critérios de aceite atendidos ou não e proponha correções mínimas. Só implemente correções após aprovação explícita.
```
