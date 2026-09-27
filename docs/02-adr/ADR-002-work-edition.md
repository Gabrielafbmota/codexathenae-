# ADR-002 — Obra separada de edição possuída

**Status:** aceito. **Etapa:** MVP 1. **Contexto:** CSV sem ISBN e possibilidade de três edições da mesma obra.

**Decisão:** `works` representa identidade e estado de leitura; `editions` representa edições cadastradas como possuídas; zero ou muitas por obra. Sessões futuras referenciam edição opcionalmente.

**Alternativas:** um documento por ISBN falha sem ISBN e duplica obra; embutir todas as edições na obra complica índices e concorrência.

**Consequências:** resolver obra antes de edição, ISBN nunca é identidade universal da obra, posse não é inferida da busca externa.
