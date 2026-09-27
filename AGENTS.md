<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->

## Regras específicas do CodexAthenae

Leia [a constituição](.specify/memory/constitution.md), o
[PRD](docs/00-governance/prd.md) e o [README](README.md) antes de planejar mudanças.
Se ainda não existir plano, use essas fontes; não invente um plano atual.
Stack do MVP 1: TypeScript/Node.js, Fastify, MongoDB Atlas, Telegram polling e
Docker Compose local. Não substituir por Python/FastAPI ou AWS.
Testes automatizados para funcionalidades/correções e documentação atualizada na
mesma entrega são obrigatórios conforme a constituição; a opção genérica de testes
nas skills não dispensa essas regras. Revise todos os documentos afetados, incluindo
um README completo, e registre evidências ou justificativa de não aplicabilidade.
Preserve a configuração local existente; não leia/exponha segredos sem necessidade,
nem versione `.env` ou `..env`. Consulte fontes oficiais atuais ao escolher dependências.
