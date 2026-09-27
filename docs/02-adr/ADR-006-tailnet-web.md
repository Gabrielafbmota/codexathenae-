# ADR-006 — Web privada pela tailnet

**Status:** aceito para Web 1. **Decisão:** UI e API privadas somente na Tailscale, sem login adicional no app; somente webhook público via Funnel.

**Alternativas:** login próprio adiciona custo e foi dispensado pela usuária; expor dashboard pelo Funnel contraria privacidade.

**Consequências:** ACL e verificação externa são controles obrigatórios; rever se houver acesso fora da tailnet ou outro usuário.
