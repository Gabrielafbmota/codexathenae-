# ADR-005 — Evidência de leitura e estantes derivadas

**Status:** aceito. **Etapa:** MVP 1 → 3. **Decisão:** lido importado/declaração e sessão concluída são evidências distintas; estantes automáticas derivadas delas e de sessão aberta.

**Alternativas:** criar sessão fictícia para CSV produziria datas erradas; persistir estantes automáticas exige sincronização em correções/deleções.

**Consequências:** `Lidos` e `Lendo` coexistem em releitura; exclusão da última evidência solicita estado desejado.
