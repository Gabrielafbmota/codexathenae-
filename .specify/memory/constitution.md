<!--
Sync Impact Report
Version change: template (sem versão ratificada) → 1.0.0
Modified principles: placeholders → I. Escopo e stack do projeto;
II. Arquitetura em camadas; III. Integridade e identidade dos dados;
IV. Segurança e configuração; V. Qualidade verificável;
VI. Documentação sempre atualizada.
Added sections: Restrições técnicas e operacionais; Fluxo de desenvolvimento;
Governança preenchida e fontes oficiais.
Removed sections: nenhuma seção substantiva; exemplos genéricos substituídos.
✅ updated: .specify/templates/plan-template.md
✅ updated: .specify/templates/spec-template.md
✅ updated: .specify/templates/tasks-template.md
✅ updated: AGENTS.md; README.md; docs/README.md; docs/CODEGEN_HANDOFF.md
✅ updated: docs/08-delivery/definition-of-done.md
✅ updated: docs/04-security/secrets-and-keys.md
✅ updated: docs/06-operations/deployment-and-network.md
✅ updated: docs/{PRD,ARQUITETURA_ADRS,IMPORTACAO_INICIAL,PLANO_ENTREGA,SEGURANCA,
QUESTOES_ABERTAS,FLUXOS,INTEGRACOES,MODELO_DADOS}.md (avisos de referência histórica)
✅ updated: .gitignore; .env retirado apenas do índice, preservado localmente
✅ reviewed: .specify/templates/checklist-template.md (sem alteração necessária)
Command templates: .specify/templates/commands/ não existe neste repositório.
As skills locais usam orientação genérica; AGENTS.md explicita a precedência
constitucional para testes e documentação sobre a opção genérica de testes.
Follow-up: escolher runtime, runner de testes e bibliotecas no primeiro plano;
publicar comandos executáveis no README quando houver implementação.
Nenhum placeholder constitucional adiado. Não existe plano de feature atual.
-->
# CodexAthenae Constitution

## Core Principles

### I. Escopo e stack do projeto

O PRD em `docs/00-governance/prd.md` DEVE definir o comportamento de produto e a
etapa entregue. O MVP 1 DEVE usar TypeScript/Node.js, Fastify sem NestJS, MongoDB
Atlas, Telegram privado por polling e Docker Compose no computador da proprietária.
Preferências de outros projetos NÃO DEVEM substituir essa stack por Python/FastAPI
ou AWS. Web, Raspberry Pi, webhook, leituras/progressos e recomendações DEVEM
permanecer nas etapas previstas pelo PRD. Antecipações exigem decisão explícita
da proprietária e atualização dos artefatos afetados.

### II. Arquitetura em camadas

A implementação DEVE separar `domain`, `application`, `infrastructure` e
`presentation` (ou `interfaces`, conforme o plano). Domínio e casos de uso NÃO
DEVEM depender de SDKs de Telegram, MongoDB ou de Fastify. Adaptadores DEVEM
implementar portas pequenas definidas pelas necessidades dos casos de uso.
Regras compartilhadas DEVEM existir nos casos de uso, com dependências apontando
para o interior. Clean Architecture, SOLID e 12-factor orientam a organização;
complexidade adicional DEVE ter necessidade concreta registrada em ADR.

### III. Integridade e identidade dos dados

Operações DEVEM identificar inequivocamente a obra e, quando aplicável, a edição.
Seleções DEVEM conservar ID/contexto e expirar; números de página isolados NÃO
DEVEM autorizar alterações. Resultados externos DEVEM confirmar título e autor.
Importação e reentrega Telegram DEVEM ser idempotentes; a persistência DEVE
tratar duplicatas e concorrência, distinguindo obra de edição.

Dados ausentes DEVEM permanecer ausentes: NÃO inventar ISBN, datas, sessões ou
posse. Enriquecimento DEVE preservar estado, tags e dados pessoais e registrar
origem bibliográfica. O corpus inicial descrito no PRD contém 845 registros,
764 lidos sem data e 81 por ler; esses números são aceite do corpus inicial,
não uma restrição para futuras importações. Sucesso só DEVE ser informado após
confirmação do resultado persistido pelo caso de uso.

### IV. Segurança e configuração

O bot DEVE validar `from.id`, `chat.id` e conversa privada antes de acessar dados
ou executar casos de uso; `username` NÃO autoriza. Entradas externas DEVEM ser
validadas, com limites, timeouts e tratamento de falhas. Atlas DEVE usar TLS,
privilégio mínimo e restrição de rede; saúde Fastify DEVE ficar local no MVP 1.

Segredos DEVEM vir do ambiente ou arquivo local ignorado pelo Git. Reutilizar a
configuração existente da proprietária sem sobrescrever valores. `.env` e `..env`
DEVEM ser protegidos; o caminho efetivo DEVE ser explícito na execução.
Credenciais, CSV pessoal e dados privados NÃO DEVEM aparecer em documentação,
fixtures, logs, imagens Docker ou CI. Exemplos DEVEM conter apenas nomes,
descrições e valores fictícios. Configuração obrigatória ausente DEVE impedir
inicialização com erro que não exponha segredos. Revisões DEVEM considerar as
ameaças OWASP aplicáveis ao fluxo alterado.

### V. Qualidade verificável

Novas funcionalidades e correções de comportamento DEVEM incluir testes
automatizados proporcionais ao risco, com runner TypeScript definido no plano.
Cobrir domínio/aplicação, contratos e integração quando essas fronteiras mudarem;
autorização negada, duplicação, concorrência, ausência de dados e falha externa
DEVEM ter cenários nos fluxos afetados. Usar dados sintéticos e Mongo isolado.
Mudanças apenas documentais DEVEM validar coerência, links e comandos aplicáveis,
sem exigir testes artificiais de implementação.

Lint, typecheck, testes pertinentes, build e verificações de segredos/dependências
DEVEM compor o CI quando o código for introduzido. A revisão DEVE registrar
comandos, resultados e limitações; não declarar testes executados sem evidência.
Versões e contratos DEVEM ser conferidos em documentação oficial atual antes de
adotar ou atualizar dependências, registrando links e data no plano ou ADR.

### VI. Documentação sempre atualizada

Toda mudança DEVE revisar a documentação afetada e atualizá-la na mesma entrega.
Isso inclui README, PRD, ADRs, contratos, modelo e migrações, segurança, operação,
testes, backlog e artefatos Spec Kit quando afetados. A revisão DEVE listar
arquivos atualizados ou justificar por que cada área relevante não foi afetada.
Documentação desatualizada impede considerar a mudança concluída.

O `README.md` da raiz DEVE ser completo e servir de entrada: objetivo, estado real,
stack, arquitetura, escopo, pré-requisitos, configuração sem segredos, instalação,
execução, testes, importação, operação, troubleshooting e links para documentos
canônicos. Comandos DEVEM corresponder a arquivos/scripts existentes e ser
validados quando executáveis; etapas ainda não implementadas DEVEM ser marcadas
como planejadas. Cópias antigas DEVEM ser sincronizadas ou claramente identificadas
como históricas, com link para a fonte vigente. Não apresentar propostas como entregas.

## Restrições técnicas e operacionais

- Busca do MVP 1: base local → Open Library → Google Books, conforme decisão da
  usuária de continuar; cadastro manual permanece disponível.
- MongoDB Atlas é o banco do MVP 1; NÃO introduzir Mongo local como banco operacional.
  Banco isolado de testes é permitido.
- Apenas um consumidor polling por token; falhas externas DEVEM permitir recuperação
  e logs estruturados sem conteúdo pessoal.
- Deploy é manual e local no MVP 1. React/Vite/Tailwind e migração para Raspberry Pi
  pertencem a etapas futuras; AWS, RDS e K3s não são requisitos deste projeto.
- Não impor metas arbitrárias de latência: medir e justificar metas conforme o PRD.
- Biblioteca Telegram, versões, validador e convenção de IDs DEVEM ser decididos no
  primeiro plano de implementação, com justificativa e fontes atuais.

Fontes oficiais de referência, consultadas em 2026-09-27:
[Fastify](https://fastify.dev/docs/latest/),
[Telegram Bot API](https://core.telegram.org/bots/api),
[MongoDB: índices únicos](https://www.mongodb.com/docs/manual/core/index-unique/),
[Docker Compose: variáveis de ambiente](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).

## Fluxo de desenvolvimento

1. Ler esta constituição, PRD, decisões abertas e plano atual, quando existir.
2. Relacionar a mudança a uma história e etapa. Perguntar diante de ambiguidade
   de produto; registrar decisões arquiteturais com alternativas e consequências.
3. No plano, verificar escopo/stack, camadas, integridade, segurança, testes e
   documentação antes da pesquisa e após o desenho. Exceções DEVEM ter justificativa,
   impacto e decisão da proprietária registrados antes da implementação dependente.
4. Gerar tarefas de implementação, testes e documentação por história. Configuração,
   índices e recuperação DEVEM ter tarefas quando afetados.
5. Executar verificações pertinentes, revisar o diff e atualizar os documentos
   afetados. O README DEVE refletir os comandos e o estado entregue.
6. Apresentar evidências e limitações da entrega conforme a definição de pronto.

## Governance

Esta constituição rege engenharia e qualidade; o PRD rege decisões de produto.
Templates e instruções genéricas NÃO DEVEM relaxar estes princípios. Divergências
DEVEM ser explicitadas e resolvidas com a proprietária, sem substituir decisões
específicas do projeto por preferências gerais.

Emendas DEVEM registrar motivo, princípios alterados, impacto e migração, atualizar
os templates/documentos dependentes e incluir Sync Impact Report. Mudanças de
princípio ou escopo exigem decisão explícita da proprietária. Toda revisão de
feature DEVE verificar conformidade e evidências de testes e documentação.

Versionamento semântico: MAJOR para remoção/redefinição incompatível de princípios;
MINOR para novo princípio ou ampliação normativa; PATCH para esclarecimento sem
mudança de obrigação. A ratificação original é preservada e a data de emenda
muda quando houver alteração. A versão 1.0.0 é a primeira constituição preenchida,
baseada na especificação e nas instruções confirmadas pela proprietária.

**Version**: 1.0.0 | **Ratified**: 2026-09-27 | **Last Amended**: 2026-09-27
