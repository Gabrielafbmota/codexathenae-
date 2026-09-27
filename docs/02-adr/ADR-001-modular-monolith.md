# ADR-001 — Monólito modular TypeScript/Fastify

**Status:** aceito. **Etapa:** MVP 1. **Contexto:** bot pessoal único, casos de uso reaproveitados pela futura Web.

**Decisão:** processo Node/TypeScript com Fastify, domínio e aplicação separados de adaptadores Telegram, MongoDB e catálogos. Compose local e Atlas externo.

**Alternativas:** microserviços aumentam operação/consistência sem necessidade; NestJS não foi escolhido; Python/FastAPI é preferência geral da proprietária, mas esta entrevista confirmou expressamente TypeScript/Fastify.

**Consequências:** uma unidade de deploy, testes de domínio isolados, adaptadores substituíveis e migrações versionadas. Rever se houver carga real que justifique workers separados.
