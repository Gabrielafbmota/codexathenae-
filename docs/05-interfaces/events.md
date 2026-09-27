# Eventos e auditoria interna

Eventos não são uma fila obrigatória no MVP 1; são fatos de domínio úteis para logs seguros, testes e projeções futuras.

| Evento | Etapa | Chave idempotente | Dados mínimos permitidos |
| --- | --- | --- | --- |
| `WorkImported` | M1 | `runId:row` | workId, resultado, source |
| `WorkRegistered` | M1 | `telegram:updateId:action` | workId, source, estado |
| `EditionOwned` | M1 | `telegram:updateId:action` | editionId, workId |
| `ReadStateChanged` | M1 | operação/version | workId, anterior, novo |
| `ReadingStarted/Completed` | M2 | operação/version | sessionId, workId, data |
| `ProgressRecorded` | M2 | operação/version | eventId, sessionId, unidade |
| `ImportCommitted` | M3 | runId | contagens e códigos |
| `RecommendationFeedbackRecorded` | R | operationId | identidade, ação |

Logs não incluem título, notas, resenhas ou sentimentos livres por padrão. Se surgir entrega assíncrona, persistir outbox e entrega idempotente; não afirmar sucesso no Telegram se commit falhou.
