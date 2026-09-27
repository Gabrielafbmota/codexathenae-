# Rastreabilidade PRD → componente → teste

| Requisito | Etapa | Componente | Aceite/teste |
| --- | --- | --- | --- |
| M1-01 importação inicial | MVP 1 | ImportStoryGraph + WorkRepository | AC-01, AC-02: 845/764/81; repetição sem novos registros |
| M1-02 busca local | MVP 1 | SearchWorks | AC-03: registro abre antes de API externa |
| M1-03 fontes e paginação | MVP 1 | CatalogGateway + Conversation | AC-04, AC-05: ordem OL→Google, 3–4 opções e seleção estável |
| M1-04/05 cadastro | MVP 1 | RegisterWork | AC-06: confirmação de título/autor, manual sem ISBN |
| M1-06 enriquecimento | MVP 1 | EnrichWork + CatalogGateway | US6 da spec MVP 1: bibliografia atualizada, dados pessoais preservados e origem rastreável |
| Deduplicação transversal (M1-04/05/07) | MVP 1 | IdentityResolver + índices | AC-07, AC-08: colisão e concorrência sem fusão indevida |
| M1-07 edição/posse | MVP 1 | AddOwnedEdition | AC-09: zero, uma e várias edições, sem posse inferida |
| M1-08 estado | MVP 1 | ChangeReadState | AC-10: dois sentidos e preservação do CSV |
| M1-09 autorização | MVP 1 | TelegramIngress | AC-11: ID/chat/grupo negados |
| Sessões/progresso | MVP 2 | ReadingSession + ProgressEvent | AC-20..24: unidade fixa, releitura, CRUD e sentimentos |
| Estantes/importação | MVP 3 | Shelves + ImportRun | AC-30..33: derivadas, prévia, idempotência, falha por linha |
| Web/dashboards | Web 1 | Fastify routes + React | AC-40..43: tailnet, filtros, datas conhecidas, painel erros |
| Notas/perfil | Web 2 | Rating/Review/Profile | AC-50..53: meia estrela, média, não avaliados, paridade |
| Recomendações | Etapa 7 | CandidateIndex + Policy + Ranker | AC-60..64: exclusão, fontes, sensibilidade e feedback |
| Exportação | Etapa 8 | Export/Restore | AC-70..72: formatos e restore em base vazia |

Mudança de requisito deve atualizar componente, aceite e backlog no mesmo PR de documentação.

## Especificação ativa do MVP 1

[Spec](../../specs/001-biblioteca-mvp1/spec.md) e
[checklist de qualidade](../../specs/001-biblioteca-mvp1/checklists/requirements.md).
Os IDs M1 do PRD e do backlog pertencem a listas distintas; a tabela abaixo usa os do PRD.

| PRD | História | Requisitos da spec | Resultado |
| --- | --- | --- | --- |
| M1-01 | US1 | FR-001 a FR-005 | SC-001, SC-002, SC-009 |
| M1-02 | US2 | FR-006, FR-007, FR-023 | SC-003, SC-008 |
| M1-03 | US3 | FR-007 a FR-010, FR-023 | SC-003, SC-008, SC-009 |
| M1-04 | US4 | FR-011, FR-012, FR-014 a FR-016 | SC-004, SC-005 |
| M1-05 | US5 | FR-012 a FR-014 | SC-004 |
| M1-06 | US6 | FR-017 a FR-019 | SC-006 |
| M1-07 | US7 | FR-015, FR-020, FR-021 | SC-005, SC-007 |
| M1-08 | US8 | FR-004, FR-015, FR-022, FR-023 | SC-002, SC-005, SC-007, SC-008 |
| M1-09 | US9 | FR-023 a FR-027 | SC-008 |
| Constituição | Todas | CR-001 a CR-004 | SC-010 e evidências de entrega |

A cobertura acima é de requisitos, não evidência de implementação ou testes executados.
