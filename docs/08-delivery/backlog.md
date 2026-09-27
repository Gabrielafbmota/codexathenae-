# Backlog em tarefas pequenas

Cada item inclui teste automatizado e evidência de execução. IDs M1 são implementados primeiro.

| Ordem | Tarefa | Saída verificável |
| --- | --- | --- |
| F0-01 | Criar projeto TS/Fastify, lint/typecheck/test runner | comandos locais verdes |
| F0-02 | Configuração validada, `.env.example`, Compose e health loopback | boot seguro sem segredos no Git |
| F0-03 | Adaptador Atlas e migrações/índices | índices criados e teste de unicidade |
| M1-01 | Entidades obra/edição e normalização | testes de homônimos/acentos/autores |
| M1-02 | Importador/parser do CSV e relatório | AC-01/02; linhas inválidas rastreadas |
| M1-03 | Autorização Telegram e idempotência update | AC-08/11 |
| M1-04 | Parser textual, contexto e seleção paginada | AC-05, seleção expirada |
| M1-05 | Busca local | AC-03 |
| M1-06 | Adapter Open Library + timeout/429 | AC-04 parcial |
| M1-07 | Adapter Google Books + fallback | AC-04 completo |
| M1-08 | Resolução/deduplicação forte | AC-07/08 |
| M1-09 | Cadastro externo confirmado/manual | AC-06 |
| M1-10 | Edição possuída opcional | AC-09 |
| M1-11 | Estado e enriquecimento preservando dados pessoais | AC-10 |
| M1-12 | E2E, documentação de operação e smoke privado | todos AC-01..11 |

**Marcos posteriores:** M2 sessões/progressos/sentimentos; M3 estantes/importação Telegram; Pi webhook; W1 Web/dashboards/admin; W2 avaliações/textos/perfil; R recomendações; E exportação. Detalhes de aceite em `../07-quality/acceptance.md` e PRD.

## Detalhamento da feature MVP 1

A [especificação ativa](../../specs/001-biblioteca-mvp1/spec.md) detalha as nove
histórias do PRD, incluindo aceite de enriquecimento e caminhos adversariais.
A [rastreabilidade](../00-governance/traceability.md) relaciona os itens do PRD aos
requisitos e resultados esperados. Cenários posteriores ao MVP 1 continuam futuros.
Este documento não substitui o `tasks.md`, que será gerado após o planejamento.
