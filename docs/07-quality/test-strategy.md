# Estratégia de testes

**Stack de teste:** runner TypeScript escolhido no primeiro PR (Vitest ou Node test runner), HTTP fake para provedores/Telegram e Mongo isolado para integração. Não usar o CSV pessoal em fixtures públicas.

1. **Domínio:** normalização, candidatos fortes, estados, estantes, progresso, média e sensibilidade.
2. **Contrato:** respostas Open Library/Google Books incompletas, 429 e timeout; updates Telegram privados/grupo, página expirada, reentrega.
3. **Integração:** índices únicos e corrida, reimportação idempotente, preservação de dados pessoais, migrações.
4. **E2E local:** update sintético → auth → busca → confirmação → commit → resposta; manual sem ISBN; edição possuída distinta.
5. **Operação/segurança:** token ausente, log redigido, backup isolado, ingress externo na fase Pi, CSV injection na exportação.

CI proposto: format/lint → typecheck → testes unitários → integração Mongo isolado → scan de segredos/dependências → build. Cobertura alta do domínio/aplicação é objetivo de engenharia, mas qualidade dos cenários prevalece sobre percentuais.
