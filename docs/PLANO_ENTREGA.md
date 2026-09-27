> Referência histórica do pacote inicial. A fonte vigente é [08-delivery/delivery-plan.md](08-delivery/delivery-plan.md).
> Para estado e configuração atuais, consulte o [README principal](../README.md).

# Plano de entrega e qualidade

Os marcos abaixo são entregáveis, não estimativas de calendário. Cada etapa somente avança com demonstração da aceitação e migração/backup quando há mudança de dados.

## Backlog em ordem de execução

| Marco | Trabalho | Evidência de pronto |
| --- | --- | --- |
| M1-A | Repositório TS, Fastify, configuração/segredos, Compose, cliente Atlas, índices, CI local | Sobe em computador, saúde em loopback, conexão e índices verificados, nenhum segredo em Git |
| M1-B | Importador local CSV StoryGraph e relatório por linha | 845 linhas, 764 lidos, 81 quero ler na base vazia; segunda execução não duplica; campos vazios não são inventados |
| M1-C | Bot privado, contexto e parser natural determinístico | IDs/grupos negados; mensagem ambígua solicita esclarecimento; paginação textual consistente |
| M1-D | Busca local, Open Library, Google Books e cadastro | Prioridade correta, falhas recuperáveis, título/autor confirmados, manual funciona |
| M1-E | Deduplicação, edição possuída e mudança de estado | Mesmo livro não duplica em concorrência/reentrega; múltiplas edições distintas; CSV preservado/enriquecido |
| M2 | Sessões, progresso, notas/sentimentos e CRUD | Unidade fixa por sessão, releitura segura, histórico paginado, exclusão confirmada e estados recalculados |
| M3 | Estantes e CSV incremental no bot | Derivadas coexistem, pessoais preservadas; preview/commit idempotente e erros por linha |
| Pi | Webhook e Compose no Raspberry Pi | Apenas webhook público, segredo validado, polling desligado, rede tailnet testada |
| W1 | Web funcional e dashboards | Paridade bot, filtros corretos, datas ausentes fora de gráficos, painel de erros, fallback de capa |
| W2 | Notas, resenhas, anotações, perfil | Nota meia estrela, média e não avaliados corretos, paridade web/bot |
| R | Recomendações | Exclusões e temas sensíveis testados, livros e links verificáveis, feedback sem repetir rejeitados |
| E | Exportação/restauração | CSV compatível, backup completo íntegro, restore somente em banco vazio |

## Testes com valor de negócio

- **Unidade/domínio:** normalização de título/autor; regras de estantes; escolha de unidade e progresso final/regressivo; média de notas; classificação sensível e prioridade manual.
- **Integração:** concorrência de cadastro e índices Mongo; script CSV duas vezes; enriquecimento preservando campos pessoais; reentrega do mesmo `update_id`; timeout/429 de catálogos; webhook secreto e chat errado.
- **Jornadas:** livro já salvo abre ficha; busca externa confirmada; homônimo não fundido; três edições de uma obra; duas obras lendo ao mesmo tempo; releitura com sessão aberta; remoção de evento final e decisão de estado; CSV com uma linha inválida continua e registra falha; exportação/restore em base isolada.
- **Web:** filtros combinados não contam datas inexistentes; book list de não avaliados; capas ausentes/falhas usam genérica; acesso externo à tailnet falha.
- **Segurança:** operador Mongo em entrada rejeitado; CSV formula neutralizada na saída; logs sem segredos/texto livre; temas bloqueados nunca recomendados quando classificação explícita é conhecida.

## Definição de pronto por item

Caso de uso implementado com estados de erro legíveis; testes relevantes passando; índices/migração versionados; documentação de configuração atualizada; logs de sucesso/falha sem dado sensível; demonstração manual no Telegram quando aplicável. Não criar testes que apenas repetem a implementação sem verificar comportamento.

## Entregáveis de arranque do repositório

`README` de instalação, `.env.example`, `compose.yaml`, scripts `import:initial` e `db:indexes`, configuração validada, testes, licença/uso privado se desejado, documentação deste pacote em `docs/`. Segredos e o CSV real ficam fora do Git. Escolher biblioteca Telegram e versões de dependência ao começar a codificar, com revisão das APIs na versão instalada.
