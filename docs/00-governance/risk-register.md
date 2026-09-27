# Registro de riscos

Escalas qualitativas: probabilidade P/B/A (pequena/baixa, moderada, alta) e impacto B/M/A. Revisar ao iniciar cada etapa.

| ID | Risco | Prob. | Impacto | Mitigação e gatilho |
| --- | --- | --- | --- | --- |
| R-01 | Obra duplicada ou fusão de homônimos | M | A | IDs, normalização, revisão humana e índices; medir colisões na importação |
| R-02 | APIs de catálogo limitam chamadas | A | M | Busca local, cache, timeout, backoff, cadastro manual; registrar 429 |
| R-03 | Estado lido sem data vira histórico fictício | M | A | `readEvidence`, testes com 764 importados, dashboard só datas reais |
| R-04 | Bot token/Atlas URI expostos | M | A | secrets, redaction, rotação e varredura Git; alerta de vazamento |
| R-05 | Web pessoal vaza pelo Funnel | M | A | configuração NGINX explícita, teste externo e tailnet ACL antes de Web 1 |
| R-06 | Descrições omitem temas sensíveis | A | A | classificar `unknown`, avisar, fonte/correção manual; nunca prometer cobertura total |
| R-07 | Corpus de recomendações ocupa recurso demais | M | M | medir dump/amostra, índice reduzido e importação offline incremental |
| R-08 | Falha/retentativa perde ou duplica importação | M | M | hash, linha, idempotência, logs estruturados, teste de interrupção |
| R-09 | Backup não restaura | M | A | ensaio em base isolada, contagem, hashes e runbook; antes de migração |
| R-10 | Escopo do MVP cresce | A | M | handoff/backlog com marcos, mudanças via PRD e ADR |
