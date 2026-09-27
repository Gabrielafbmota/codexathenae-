# ADR-004 — Consulta local, catálogo e identidade

**Status:** aceito. **Etapa:** MVP 1. **Decisão:** MongoDB → Open Library → Google Books; confirmação de título/autor; identificação por IDs externos e título/autor normalizados; suspeita forte solicita confirmação; colisão fuzzy não funde automaticamente.

**Alternativas:** busca externa primeiro provoca chamadas desnecessárias; unicidade por título pode juntar homônimos; só ISBN falha com CSV atual.

**Consequências:** cache/backoff, snapshot de seleção, índice de candidatos e check atômico no commit; proveniência por campo.
