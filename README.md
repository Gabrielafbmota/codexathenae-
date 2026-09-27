# CodexAthenae

Biblioteca pessoal gerenciada por conversa privada no Telegram: encontrar livros,
registrar obras e edições possuídas e preservar o histórico sem inventar informações.
Projeto para uma única proprietária; não é um leitor de ebooks nem um serviço multiusuário.

## Estado atual

**27/09/2026 — especificação e preparação; produto ainda não implementado.**
O repositório contém documentação, constituição e ferramentas Spec Kit. Ainda não
há `package.json`, aplicação, suíte de testes do produto, Dockerfile ou Compose.
Credenciais locais já foram informadas pela proprietária; seu conteúdo não foi
inspecionado nem validado nesta etapa.

A [constituição 1.0.0](.specify/memory/constitution.md) rege engenharia e qualidade;
o [PRD](docs/00-governance/prd.md) define produto e etapas. Comece também pelo
[handoff](docs/CODEGEN_HANDOFF.md) e pelas [decisões abertas](docs/00-governance/open-decisions.md).

## Especificação ativa

O [MVP 1 está especificado](specs/001-biblioteca-mvp1/spec.md) na branch
`001-biblioteca-mvp1`, com nove histórias e critérios de aceite. O
[checklist de qualidade](specs/001-biblioteca-mvp1/checklists/requirements.md)
registra a validação documental. Próxima etapa: `/speckit-plan`.
Ainda não há plano de implementação ou tarefas geradas para essa feature.

## MVP 1

- Importação local repetível do CSV StoryGraph; corpus inicial descrito com 845
  registros: 764 lidos sem data e 81 por ler. Não criar datas, ISBN ou posse fictícios.
- Bot privado por polling, restrito aos IDs autorizados.
- Busca local, seguida de Open Library e Google Books quando a usuária continuar.
- Seleção textual, confirmação de título/autor, cadastro manual e deduplicação.
- Estado `quero ler` ou `lido`; zero ou várias edições possuídas por obra.
- Enriquecimento bibliográfico preservando tags, estado e demais dados pessoais.

Não inclui progresso, sessões de leitura, estantes, avaliações, recomendações,
web, capas, Raspberry Pi ou webhook. A evolução está no
[plano de entrega](docs/08-delivery/delivery-plan.md).

## Stack e arquitetura

| Área | Decisão |
| --- | --- |
| Runtime e linguagem | Node.js e TypeScript; versões a fixar no primeiro plano |
| Backend | Fastify, sem NestJS; saúde apenas local no MVP 1 |
| Banco | MongoDB Atlas; sem Mongo operacional no Compose |
| Interface MVP 1 | Telegram em conversa privada por polling |
| Execução | Docker Compose local, deploy manual |
| Testes | Runner TypeScript a selecionar; Mongo isolado e provedores simulados |
| Futuro | React, Vite e Tailwind; Raspberry Pi nas etapas definidas pelo PRD |

O monólito modular separa `domain`, `application`, `infrastructure` e
`presentation`/`interfaces`. SDKs e frameworks ficam nos adaptadores; casos de uso
concentram regras. Consulte [arquitetura](docs/01-architecture/architecture-and-decisions.md),
[portas](docs/01-architecture/ports-and-adapters.md) e [ADRs](docs/02-adr/).
Python/FastAPI, AWS, RDS e K3s não fazem parte da stack confirmada deste projeto.

## Estrutura existente

```text
.agents/skills/       workflows Spec Kit
.specify/memory/      constituição
.specify/templates/   templates de especificação, plano e tarefas
.specify/scripts/     ferramentas do processo de especificação
specs/               especificações de features e checklists
docs/                produto, arquitetura, dados, segurança, operação e qualidade
AGENTS.md            orientação aos agentes
README.md            entrada do projeto
```

O layout de código será definido no plano de implementação respeitando as camadas.

## Pré-requisitos e preparação

Para trabalhar na especificação: Git e leitura do PRD, constituição e handoff.
Os scripts Bash do Spec Kit dependem de Bash e das ferramentas descritas em seus workflows.
Para executar o produto futuramente: Node.js na versão selecionada, Docker com
Compose, acesso ao Atlas, bot Telegram e IDs autorizados configurados localmente.
Biblioteca Telegram, validador, convenção de IDs e runner ainda precisam de decisão.

Não há instalação de dependências nem comando de execução disponível nesta etapa.
O primeiro incremento de código deve adicionar manifesto, lockfile, scripts,
Compose e instruções verificadas nesta seção.

## Configuração e segredos

A proprietária informou variáveis em `..env`; a inspeção apenas de nomes constatou
`.env` na raiz e não encontrou `..env`. O arquivo existente foi preservado, sem
leitura dos valores. `.gitignore` protege as duas grafias e suas variantes locais.
Não sobrescrever a configuração para criar exemplos.

| Configuração conhecida na especificação | Uso |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Autenticação do bot |
| `MONGODB_URI` | Conexão Atlas com TLS e privilégio mínimo |
| IDs Telegram autorizados | Validação de remetente e conversa; nomes das variáveis a definir |
| Chave Google Books, se necessária | Quota de consultas; nome a definir |
| `TELEGRAM_WEBHOOK_SECRET` | Somente na etapa futura com webhook |

A presença desses valores não foi verificada. O contrato final deve validar campos
obrigatórios ao iniciar, sem imprimir valores. Exemplos versionados devem conter
somente nomes, descrições e valores fictícios, nunca dados copiados do arquivo real.

No futuro Compose, `--env-file` permite selecionar um arquivo de interpolação;
`environment`/`env_file` deve fornecer explicitamente a configuração ao container.
Consultar a [documentação oficial](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).
Não imprimir configuração resolvida nem incluir arquivos de ambiente na imagem Docker.

O `.env` estava rastreado e foi retirado do índice, mantendo a cópia local. Isso
não apaga o histórico: se havia credenciais reais, elas precisam de rotação.
Veja [segredos e chaves](docs/04-security/secrets-and-keys.md).

## Execução e importação

**Planejadas, ainda indisponíveis.** A ordem de implementação é: configuração e
índices, importador local, autorização do bot, busca, confirmação, cadastro e estados.
O importador deve produzir relatório por linha e permitir reexecução sem duplicar.
O CSV pessoal não deve entrar em Git, logs, fixtures ou CI.

Quando implementado, documentar aqui os comandos reais de instalação, build,
início/parada, importação e saúde, incluindo diretório de execução e pré-requisitos.
Não há comando `npm` ou `docker compose` de produto validado para copiar agora.
Consulte [importação inicial](docs/03-data/initial-import.md) e
[implantação](docs/06-operations/deployment-and-network.md).

## Testes e qualidade

Novas funcionalidades e correções exigem testes automatizados proporcionais ao
risco: domínio, contratos, integração e jornada local. Cobrir autorização negada,
reentrega, reimportação, concorrência, seleção expirada e APIs indisponíveis.
Usar dados sintéticos, nunca o CSV pessoal.

A suíte e o CI ainda não existem. O primeiro incremento deve documentar os scripts
reais de lint, typecheck, testes e build e configurar os controles de CI.
Mudanças apenas documentais validam links, coerência e comandos aplicáveis.
Veja [estratégia de testes](docs/07-quality/test-strategy.md),
[aceite](docs/07-quality/acceptance.md) e
[definição de pronto](docs/08-delivery/definition-of-done.md).

## Operação e solução de problemas

No MVP 1, apenas um consumidor polling por token; saúde local, logs estruturados
sem segredos e Atlas com acesso restrito. Backup, restauração e observabilidade
estão especificados, mas não implementados.

| Sintoma futuro | Verificação segura |
| --- | --- |
| Bot não responde | Processo ativo, conversa privada, IDs permitidos e consumidor único |
| Configuração ausente | Caminho e carregamento explícito, sem imprimir conteúdo |
| Atlas indisponível | Rede autorizada, TLS, credencial e privilégio mínimo |
| Catálogo falha | Timeout/quota e fluxo de recuperação ou cadastro manual |
| Seleção expirada | Repetir busca; nunca reaproveitar número isolado |

Detalhes: [runbooks](docs/06-operations/runbooks.md),
[backup](docs/06-operations/backup-and-recovery.md),
[observabilidade](docs/06-operations/observability-and-slo.md) e
[incidentes](docs/04-security/incident-response.md).

## Fluxo de contribuição e documentação

1. Relacionar a mudança à etapa e à história do PRD.
2. Ler a constituição e elaborar especificação, plano e tarefas quando aplicável.
3. Consultar documentação oficial atual para dependências e registrar decisões em ADR.
4. Implementar e executar verificações pertinentes com evidências.
5. Atualizar **toda documentação afetada na mesma entrega**, incluindo este README:
   PRD, ADRs, contratos, dados, segurança, operação, testes, backlog e artefatos Spec Kit.
6. Registrar áreas não afetadas com justificativa e revisar links/comandos.

Documentação desatualizada impede concluir a entrega. Mantenha o README completo,
com status verdadeiro e comandos reproduzíveis à medida que o projeto evoluir.
O [índice de documentação](docs/README.md) aponta para as fontes canônicas;
documentos legados em maiúsculas devem permanecer claramente identificados.

## Referências oficiais

- [Fastify](https://fastify.dev/docs/latest/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [MongoDB](https://www.mongodb.com/docs/manual/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Open Library Search](https://openlibrary.org/dev/docs/api/search)
- [Google Books](https://developers.google.com/books/docs/v1/reference/volumes)
