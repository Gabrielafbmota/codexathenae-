# Riscos iniciais

| ID | Risco | Impacto | Probabilidade | Mitigação |
|---|---|---:|---:|---|
| R-001 | Escopo crescer antes do catálogo básico estar estável | Alto | Alta | Entregas por versão, critérios de aceite e fora de escopo explícito |
| R-002 | Regras de negócio migrarem para routers ou n8n | Alto | Média | Testes arquiteturais, portas e revisão de dependências |
| R-003 | Duplicidade causada por concorrência ou ISBN inconsistente | Alto | Média | Value object, normalização e índice único parcial |
| R-004 | Bloqueio por rate limit dos provedores | Médio | Alta | Cache, rate limit local, backoff, fallback e fila de reprocessamento |
| R-005 | Metadados externos incorretos sobrescreverem dados confirmados | Alto | Média | Confirmação humana, origem por campo e política de precedência |
| R-006 | Dependência excessiva do n8n | Médio | Média | Casos de uso continuam executáveis e testáveis sem n8n |
| R-007 | Segredos expostos em repositório, logs ou workflows | Alto | Média | Secret store, redaction, `.env.example` e revisão automatizada |
| R-008 | Telegram permitir operação não autorizada | Alto | Baixa | Allowlist, rate limit, confirmação e tokens rotacionáveis |
| R-009 | Baixa observabilidade dificultar diagnóstico | Médio | Média | Logs estruturados, correlation ID, métricas e estados explícitos |
| R-010 | Testes frágeis por dependerem de APIs reais | Médio | Alta | MockTransport, fixtures determinísticas e testes de contrato isolados |
| R-011 | Incompatibilidade com mudanças no PyMongo Async ou provedores | Médio | Média | Versões fixadas, adaptadores isolados e atualização controlada |
| R-012 | Documentação divergir do código | Médio | Média | Atualização documental no DoD e revisão em cada PR |

## Política de revisão

Os riscos devem ser revistos no início de cada versão e sempre que uma decisão arquitetural, integração externa ou regra de domínio for alterada.
