# CodexAthenae · pacote de arranque

**Versão:** 2.0 · **Data:** 27/09/2026 · **Status:** especificação, sem código de produto implementado.
**Fonte:** entrevista com Gabi e CSV StoryGraph inicial.
**Stack confirmada:** TypeScript/Node.js, Fastify, MongoDB Atlas, Telegram, Docker Compose; React/Vite/Tailwind e Raspberry Pi em etapas futuras.

## Comece aqui

O [README principal](../README.md) descreve estado, configuração e fluxo do projeto.
A [constituição](../.specify/memory/constitution.md) exige documentação atualizada em cada entrega.

[CODEGEN_HANDOFF.md](CODEGEN_HANDOFF.md) instrui uma IA implementadora a construir **somente o MVP 1**. O [PRD](00-governance/prd.md) é a fonte normativa das decisões de produto. ADRs e demais documentos são propostas de engenharia coerentes com ele.

| Pasta | Conteúdo |
| --- | --- |
| `docs/00-governance/` | PRD, decisões abertas, glossário, riscos, rastreabilidade |
| `docs/01-architecture/` | arquitetura, portas/adaptadores, fluxos Mermaid |
| `docs/02-adr/` | template e oito decisões separadas |
| `docs/03-data/` | modelo, índices, migrações, exemplos, importação, governança |
| `docs/04-security/` | segurança, ameaças, segredos, checklist, incidentes |
| `docs/05-interfaces/` | Telegram, catálogos, eventos, HTTP futuro |
| `docs/06-operations/` | deploy/rede, observabilidade, backup, runbooks, capacidade |
| `docs/07-quality/` | testes e aceite |
| `docs/08-delivery/` | backlog e definição de pronto |

Arquivos em maiúsculas nesta pasta (`PRD.md`, `MODELO_DADOS.md` etc.) são cópias do pacote inicial, mantidas como referências históricas para compatibilidade de links; as versões organizadas nas subpastas são a base de trabalho vigente. Atualize toda documentação afetada, incluindo o README da raiz, na mesma entrega.

## Especificação ativa

[MVP 1 — biblioteca pessoal](../specs/001-biblioteca-mvp1/spec.md), com
[checklist validado](../specs/001-biblioteca-mvp1/checklists/requirements.md).
Pronta para planejamento; ainda sem código de produto ou plano de implementação.

## Limites do MVP 1

Importação local inicial, bot privado por polling, busca local → Open Library → Google Books, cadastro confirmado/manual, deduplicação, estado lido/quero ler e edições possuídas opcionais. Sem leituras/progressos, web, capa ou webhook. O CSV tem 845 obras (764 lidas sem data, 81 quero ler); não criar fatos inexistentes.

## Fontes oficiais

[Telegram Bot API](https://core.telegram.org/bots/api) · [Open Library Search](https://openlibrary.org/dev/docs/api/search) · [Google Books](https://developers.google.com/books/docs/v1/reference/volumes) · [Fastify](https://fastify.dev/docs/latest/) · [MongoDB](https://www.mongodb.com/docs/manual/) · [Docker Compose](https://docs.docker.com/compose/) · [Tailscale Funnel](https://tailscale.com/kb/1223/funnel).
