# Contratos de aplicação e HTTP futuro

MVP 1 não publica API pessoal. Fastify pode ter `GET /health/live` em loopback sem informações de biblioteca. Rotas abaixo são **propostas para Web 1**, não escopo de MVP 1.

| Método | Rota futura | Caso de uso | Respostas |
| --- | --- | --- | --- |
| GET | `/api/v1/books?query=&cursor=` | Busca local | `200`, `400` |
| POST | `/api/v1/books` | Cadastro confirmado | `201`, `409` duplicata/suspeita |
| GET | `/api/v1/books/{id}` | Ficha | `200`, `404` |
| PATCH | `/api/v1/books/{id}/read-state` | Estado | `200`, `409` conflito |
| POST | `/api/v1/books/{id}/editions` | Posse | `201`, `409` edição existente |
| GET/POST/PATCH/DELETE | `/api/v1/books/{id}/readings` | MVP 2 via Web 1 | seleção e versão obrigatórias |
| GET/POST/PATCH/DELETE | `/api/v1/readings/{id}/progress` | MVP 2 via Web 1 | unidade e versão obrigatórias |
| GET | `/api/v1/dashboard` | Métricas | filtros explícitos, datas ausentes fora da série |
| GET | `/api/v1/imports/{id}/errors` | Resolução de falhas | paginação e código seguro |

Erros padronizados `{ code, message, requestId, details? }`, sem payload cru nem segredo. `409 DUPLICATE_CANDIDATE` inclui IDs/título/autor mínimos para confirmação, nunca grava sem consentimento. Nas mutações Web, considerar versão `If-Match`/campo versionado. Autorização de rede/ingress precede HTTP; CORS sozinho não autentica.
