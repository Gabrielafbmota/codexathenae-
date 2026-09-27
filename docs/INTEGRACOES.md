> Referência histórica do pacote inicial. A fonte vigente é [05-interfaces/integrations.md](05-interfaces/integrations.md).
> Para estado e configuração atuais, consulte o [README principal](../README.md).

# Integrações e contratos

## Telegram

- MVP 1–3: `getUpdates`, único consumidor e offset persistido/idempotência de `update_id`; mensagens privadas textuais e, no MVP 3, documento CSV. O texto livre é classificado por regras simples e esclarecimento, sem dependência de IA no MVP 1.
- Contexto de conversa tem seleção numerada, página, IDs das opções, intenção e prazo de expiração. Se expirar ou mudar lista, pedir escolha novamente. Antes de editar, repetir obra/edição/evento específicos.
- Etapa Pi: registrar `setWebhook`, desligar polling, `secret_token`, validar cabeçalho e emissor. Falha transitória responde sem confirmar processamento; reentrega é segura.
- Respostas minimizam dados pessoais e não mostram ficha a remetentes fora da allowlist.

## Open Library e Google Books

| Ordem | Uso | Dados confiáveis para identidade |
| --- | --- | --- |
| 1 Open Library | Search API por título para obras, detalhes/edições quando escolhidas; User-Agent identificável e respeito aos limites | Work key, edition key, ISBN da edição, título/autor e fonte da resposta |
| 2 Google Books | Alternativa se a opção desejada não aparecer; pesquisa de volumes por título e leitura da ficha escolhida | Volume ID e identificadores da edição, título/autores e link |

Adaptadores convertem cada resposta para `CatalogCandidate { source, sourceWorkId?, sourceEditionId?, title, authors[], isbn?, publisher?, year?, format?, pageCount?, language?, coverRef?, sourceUrl, fieldSources }`. Campos ausentes continuam opcionais. Pesquisas não são prova de posse nem leitura. Confirmar título/autor antes de persistir. Se a fonte muda metadado bibliográfico de obra importada, guardar proveniência anterior e manter estado/tags pessoais.

Definir timeout e limite por página; cache curto de consultas e detalhes, backoff em 429, limite de tentativas; não usar Search API para varredura de catálogo. Para catálogo amplo de recomendações futuras, avaliar dumps oficiais de Open Library com versão/licença/dimensões e processo offline, além de consultas pontuais de confirmação. Verificar qualidade e disponibilidade de tema/idioma antes de prometer classificação automática.

## Contratos internos de aplicação

`SearchBooks(query, page)` retorna locais primeiro, com opção de prosseguir à fonte; `ResolveCandidate(candidateId)` busca detalhes; `SaveWork(candidateOrManual, desiredState)` verifica duplicatas e confirma identidade; `AddOwnedEdition(workId, edition)` valida edição; `ChangeReadState(workId, state)` verifica contexto. Entradas usam IDs opacos de seleção, jamais apenas índice sem snapshot. Saídas discriminadas: sucesso, existente, suspeita de duplicata, seleção expirada, falha de fonte e validação.

Contratos futuros: `StartReading`, `AddProgress`, `EditProgress`, `CompleteReading`, `ManageShelf`, `PreviewImport`, `CommitImport`, `RateReading`, `Recommend`, `Export`. Transportes Telegram/Web traduzem entradas, casos de uso guardam regras.

**Fontes:** [Open Library Search](https://openlibrary.org/dev/docs/api/search), [Open Library dumps](https://openlibrary.org/developers/dumps), [Google Books volumes](https://developers.google.com/books/docs/v1/reference/volumes), [Telegram Bot API](https://core.telegram.org/bots/api).
