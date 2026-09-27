# Portas e adaptadores

| Porta de aplicação | Adaptador MVP 1 | Futuro | Erros discriminados |
| --- | --- | --- | --- |
| `WorkRepository` | MongoDB Atlas | Mesmo | duplicata, concorrência, indisponível |
| `EditionRepository` | MongoDB Atlas | Mesmo | edição existente, identidade incerta |
| `CatalogSearch` | Open Library e Google Books HTTP | catálogo offline de candidatos | timeout, 429, sem resultado, parse |
| `ConversationState` | Mongo com TTL/snapshot | Web não depende dela | expirada, versão divergente |
| `InboundMessage` | Telegram polling | webhook | remetente negado, update repetido |
| `MessagePresenter` | texto Telegram | Web React | entrega desconhecida |
| `Clock` | relógio UTC | mesmo | — |

Use cases recebem tipos e interfaces, não SDKs. O adaptador de catálogo mapeia dados externos em candidato tipado e guarda URL/fonte. Rotas Fastify futuras recebem IDs internos, nunca a posição visível da página do bot. Operações idempotentes revalidam estado e reportam resultado explícito.
