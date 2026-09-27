# ADR-003 — Polling local e webhook futuro

**Status:** aceito. **Etapa:** MVP 1 → Pi. **Decisão:** polling `getUpdates` por um consumidor no computador até MVP 3; webhook com segredo, NGINX e Funnel no Pi, sem polling concorrente.

**Alternativas:** webhook já no MVP 1 exigiria ingress público local sem benefício; polling permanente no Pi contraria decisão de produto.

**Consequências:** adaptador comum de update, idempotência por ID, transição operacional explícita e testes do segredo antes de expor webhook.
