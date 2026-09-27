# Handoff para implementação — CodexAthenae

**Objetivo imediato:** implementar apenas o MVP 1. O restante deste pacote estabelece contratos e evolução futura, não funcionalidades antecipadas.

A [especificação ativa do MVP 1](../specs/001-biblioteca-mvp1/spec.md) detalha
histórias e critérios de aceite do PRD. Sua validação é documental; o próximo
passo é elaborar o plano, antes de gerar tarefas ou implementar.

## Ordem de leitura

1. `README.md`, `docs/00-governance/prd.md` e `open-decisions.md`.
2. `docs/01-architecture/`, `docs/02-adr/` e `docs/03-data/`.
3. `docs/04-security/`, `docs/05-interfaces/`, `docs/07-quality/`.
4. `docs/08-delivery/backlog.md` e `definition-of-done.md`.

## Instruções para o implementador

- Stack confirmada: TypeScript/Node.js, Fastify sem NestJS, MongoDB Atlas, Telegram polling local, Docker Compose. Não trocar por Python/FastAPI ou AWS porque outros projetos da proprietária usam essas tecnologias.
- Camadas `domain`, `application`, `infrastructure`, `presentation` (ou `interfaces`) com portas e adaptadores. Sem dependência de Telegram/Mongo no domínio.
- Primeiro criar índices e importador local. Depois bot privado, busca local, Open Library, Google Books, cadastro, deduplicação, edição possuída e alteração de estado.
- O CSV inicial possui 845 registros, dos quais 764 lidos sem data. Não criar sessões, ISBN, exemplares ou data fictícios. Importador é idempotente.
- Uma resposta do bot não prova gravação: confirmar sucesso somente após resultado do caso de uso. Seleção textual deve carregar ID/snapshot e expirar; nunca editar pelo número isolado.
- Verificar `from.id`, `chat.id` e tipo privado antes de ler banco. `username` não autoriza. Reentrega de `update_id` não duplica ação.
- Confirmar título e autor de resultado externo. Verificar duplicatas de obra e edição no commit. Se identidade incerta, perguntar.
- Guardar credenciais fora de Git; não utilizar CSV real em fixture, log ou CI. Testes automatizados em cada tarefa, incluindo caminhos adversariais.
- Conferir versões e contratos atuais nas docs oficiais antes de instalar bibliotecas. Registrar decisões de implementação divergentes em novo ADR.
- Manter toda a documentação afetada atualizada na mesma entrega, incluindo README completo na raiz; revisar PRD, ADRs, contratos, dados, segurança, operação, testes e backlog. Registrar áreas não afetadas e validar links/comandos.
- Reutilizar configuração local existente sem sobrescrever credenciais. `.env` e `..env` ficam fora do Git; exemplos não contêm valores reais.
- Ao concluir cada tarefa: código alterado, testes executados, evidência de aceite e próximo item. Não publicar ou implantar fora do computador no MVP 1.

## Definição de pronto para iniciar código

O repositório existe e a proprietária informou que as variáveis já estão no ambiente local. Foi verificada apenas a presença de `.env`, sem leitura dos valores; a validade e completude das credenciais e do ID autorizado serão verificadas pela aplicação. Valores não constam na documentação. Escolher biblioteca Telegram, versão de Node, validador de schema e convenção de IDs no primeiro PR, com justificativa curta. Quantidade de cópias idênticas permanece decisão posterior.
