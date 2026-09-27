# Feature Specification: Biblioteca pessoal — MVP 1

**Feature Branch**: `001-biblioteca-mvp1`

**Created**: 2026-09-27

**Status**: Draft — validada para planejamento; produto não implementado

**Input**: User description: "docs/". Fonte normativa: [PRD](../../docs/00-governance/prd.md),
com escopo imediato definido no [handoff](../../docs/CODEGEN_HANDOFF.md) e princípios
na [constituição 1.0.0](../../.specify/memory/constitution.md).

## User Scenarios & Testing *(mandatory)*

A proprietária única quer importar e manter sua biblioteca pessoal por conversa
privada no Telegram, usando texto em português. Esta feature cobre os nove itens
M1-01 a M1-09 do PRD. P2 indica ordem de construção, não exclusão do MVP completo.
Cada história pode ser validada com dados preparados, sem exigir a execução prévia
das demais jornadas. Controle de acesso e integridade valem para todas elas.

### User Story 1 - Importar a biblioteca inicial (Priority: P1)

**Origem**: PRD M1-01.

Trazer a biblioteca existente sem perder informações nem criar fatos ausentes.

**Why this priority**: Trazer a biblioteca existente sem perder informações nem criar fatos ausentes.

**Independent Test**: Com uma biblioteca vazia e arquivo de teste equivalente ao corpus descrito, importar e repetir a operação; não depende do bot.

**Acceptance Scenarios**:

1. **US1-AS1** — **Given** o corpus inicial íntegro e biblioteca vazia, **When** a proprietária executa a importação local, **Then** 845 obras ficam disponíveis, 764 lidas sem data e 81 por ler, sem sessões nem edições possuídas inventadas.
2. **US1-AS2** — **Given** uma importação concluída e um estado posteriormente alterado pela proprietária, **When** o mesmo arquivo é reaplicado, **Then** nenhuma nova obra é criada e a alteração pessoal é preservada.
3. **US1-AS3** — **Given** um arquivo com linhas válidas, uma linha inválida e uma colisão de identidade, **When** a importação termina, **Then** linhas válidas são processadas; inválida e colisão ficam identificadas por linha e motivo, sem fusão silenciosa, com totais de inseridas, atualizadas, inalteradas e falhas.
4. **US1-AS4** — **Given** um arquivo sem título, autor ou estado válido em uma linha, ou cabeçalho incompatível, **When** a proprietária tenta importá-lo, **Then** a linha inválida não é salva; cabeçalho incompatível impede a importação e explica o problema sem expor dados pessoais.
5. **US1-AS5** — **Given** tags originais e valores opcionais ausentes ou explicitamente preenchidos, **When** a linha válida é importada, **Then** tags e valores válidos são preservados, ausências não são preenchidas por suposição e tags de editora/ano não viram prova de posse.

### User Story 2 - Consultar um livro já salvo (Priority: P1)

**Origem**: PRD M1-02.

Encontrar a própria informação antes de pesquisar fora da biblioteca.

**Why this priority**: Encontrar a própria informação antes de pesquisar fora da biblioteca.

**Independent Test**: Preparar obras conhecidas na biblioteca e buscar pelo título, sem depender da importação ou dos catálogos.

**Acceptance Scenarios**:

1. **US2-AS1** — **Given** uma obra existente, **When** a proprietária busca seu título, **Then** a ficha local é apresentada primeiro e pode ser aberta sem duplicar a obra nem consultar catálogo externo.
2. **US2-AS2** — **Given** resultados locais que não correspondem ao livro desejado, **When** a proprietária decide continuar a busca, **Then** a busca externa é oferecida sem modificar os registros locais.
3. **US2-AS3** — **Given** obras homônimas, **When** a proprietária pede para abrir uma delas de forma ambígua, **Then** o bot pede uma escolha que distinga as obras, sem selecionar silenciosamente.

### User Story 3 - Pesquisar catálogos e escolher a opção correta (Priority: P1)

**Origem**: PRD M1-03.

Encontrar títulos fora da biblioteca com escolha estável e compreensível.

**Why this priority**: Encontrar títulos fora da biblioteca com escolha estável e compreensível.

**Independent Test**: Preparar respostas de catálogo controladas e verificar a sequência de fontes e a navegação, sem salvar obras.

**Acceptance Scenarios**:

1. **US3-AS1** — **Given** nenhum resultado local adequado, **When** a proprietária prossegue para fontes externas, **Then** Open Library é consultada antes de Google Books; se a opção desejada não aparecer, é possível continuar no Google Books.
2. **US3-AS2** — **Given** mais de quatro resultados, **When** a proprietária pede próximos, voltar e escolhe o 2, **Then** cada página completa tem três ou quatro opções textuais numeradas e a seleção corresponde exatamente à página corrente.
3. **US3-AS3** — **Given** uma seleção antiga, expirada, fora da página ou um sim sem ação pendente, **When** a proprietária responde, **Then** nenhuma gravação acontece e o bot solicita nova escolha válida.
4. **US3-AS4** — **Given** catálogo indisponível, sem resultados ou com resposta incompleta, **When** a proprietária pesquisa, **Then** recebe uma explicação sem falso resultado, podendo tentar novamente, continuar na próxima fonte disponível ou cadastrar manualmente; campos ausentes não são inventados.

### User Story 4 - Salvar um resultado externo (Priority: P1)

**Origem**: PRD M1-04.

Adicionar o livro que foi efetivamente escolhido, sem duplicar registros.

**Why this priority**: Adicionar o livro que foi efetivamente escolhido, sem duplicar registros.

**Independent Test**: Com candidatos controlados e biblioteca preparada, confirmar ou recusar o cadastro e verificar o resultado.

**Acceptance Scenarios**:

1. **US4-AS1** — **Given** um candidato externo selecionado, **When** a proprietária confirma título e autor, **Then** a obra é salva como quero ler por padrão, ou lido se escolhido, aceitando os demais metadados disponíveis da fonte.
2. **US4-AS2** — **Given** uma opção ainda não confirmada, **When** a proprietária recusa ou muda o contexto da conversa, **Then** a opção anterior não é salva.
3. **US4-AS3** — **Given** uma obra já existente ou outra gravação da mesma identidade em andamento, **When** a proprietária confirma o cadastro, **Then** existe uma só obra ao final; duplicata certa aponta ao registro existente e identidade conflitante exige revisão, sem fundir obras apenas semelhantes.
4. **US4-AS4** — **Given** falha ao salvar ou perda de resposta após salvar, **When** a operação é repetida, **Then** não é anunciado sucesso sem gravação confirmada e a repetição não cria outra obra.

### User Story 5 - Cadastrar uma obra manualmente (Priority: P1)

**Origem**: PRD M1-05.

Registrar livros ausentes dos catálogos sem depender de ISBN.

**Why this priority**: Registrar livros ausentes dos catálogos sem depender de ISBN.

**Independent Test**: Sem catálogos disponíveis, informar título/autor e concluir o cadastro manual.

**Acceptance Scenarios**:

1. **US5-AS1** — **Given** um livro sem ISBN, edição, gênero, editora ou data, **When** a proprietária informa título e autor, **Then** o cadastro é permitido com os demais campos ausentes e estado quero ler por padrão, alterável para lido.
2. **US5-AS2** — **Given** título ou autor ausente, **When** a proprietária tenta concluir, **Then** o bot pede o dado obrigatório e não grava uma obra incompleta.
3. **US5-AS3** — **Given** um candidato forte a duplicata por título e autor, **When** a proprietária tenta salvar, **Then** o bot apresenta a possível correspondência e pede confirmação da identidade; não funde por semelhança nem modifica livro diferente.

### User Story 6 - Enriquecer uma obra preservando dados pessoais (Priority: P2)

**Origem**: PRD M1-06.

Melhorar a ficha bibliográfica sem perder o que foi registrado pela proprietária.

**Why this priority**: Melhorar a ficha bibliográfica sem perder o que foi registrado pela proprietária.

**Independent Test**: Preparar uma obra com estado e tags pessoais; aplicar enriquecimento solicitado e comparar os dados anteriores.

**Acceptance Scenarios**:

1. **US6-AS1** — **Given** uma obra identificada e uma fonte bibliográfica escolhida, **When** a proprietária solicita enriquecimento e confirma a correspondência de título/autor, **Then** somente a bibliografia permitida é atualizada, mantendo estado, tags, posse e demais dados pessoais, com origem e valores anteriores rastreáveis.
2. **US6-AS2** — **Given** correção bibliográfica manual explícita, **When** um catálogo apresenta valor diferente, **Then** a correção manual tem prioridade e o catálogo não a substitui silenciosamente.
3. **US6-AS3** — **Given** identificadores conflitantes ou uma fonte indisponível, **When** o enriquecimento é solicitado, **Then** o conflito exige revisão ou a falha é informada, preservando a ficha existente.

### User Story 7 - Registrar edições possuídas (Priority: P2)

**Origem**: PRD M1-07.

Distinguir conhecer uma obra de possuir uma edição ou formato.

**Why this priority**: Distinguir conhecer uma obra de possuir uma edição ou formato.

**Independent Test**: Preparar uma obra e registrar três edições distintas, inclusive uma sem ISBN.

**Acceptance Scenarios**:

1. **US7-AS1** — **Given** uma obra sem posse registrada, **When** a proprietária pesquisa uma edição ou informa editora, ano e formato sem ISBN, **Then** a edição escolhida é vinculada à obra correta, sem exigir ISBN.
2. **US7-AS2** — **Given** uma obra com uma edição possuída, **When** a proprietária registra duas edições distintas adicionais, **Then** permanece uma obra com três edições possuídas distintas.
3. **US7-AS3** — **Given** a mesma edição já vinculada ou pedido entregue duas vezes, **When** a proprietária repete o registro, **Then** a edição não é duplicada e nenhuma quantidade de cópias físicas é presumida.
4. **US7-AS4** — **Given** apenas uma obra importada ou encontrada em catálogo, **When** a proprietária ainda não declarou posse, **Then** não há edição possuída inferida; vínculo ambíguo requer nova identificação.

### User Story 8 - Alterar o estado de leitura da obra (Priority: P1)

**Origem**: PRD M1-08.

Manter lido e quero ler coerentes com a declaração atual da proprietária.

**Why this priority**: Manter lido e quero ler coerentes com a declaração atual da proprietária.

**Independent Test**: Preparar uma obra importada lida sem data e alterar seu estado nos dois sentidos.

**Acceptance Scenarios**:

1. **US8-AS1** — **Given** uma obra identificada como lida, **When** a proprietária pede para marcar quero ler, **Then** o estado muda e o bot mostra o livro e o efeito, sem criar data ou sessão.
2. **US8-AS2** — **Given** a mesma obra marcada quero ler, **When** a proprietária pede para marcar lido e depois reimporta o arquivo inicial, **Then** o estado declarado é preservado, sem inventar histórico de leitura.
3. **US8-AS3** — **Given** um título ambíguo ou contexto alterado antes da gravação, **When** a proprietária tenta mudar o estado, **Then** o bot pede identificação atual, sem modificar outra obra.
4. **US8-AS4** — **Given** uma alteração já concluída, **When** a mesma mensagem chega novamente ou o bot reinicia e a recebe, **Then** não há efeito adicional nem reversão de estado.

### User Story 9 - Usar a biblioteca somente em conversa privada autorizada (Priority: P1)

**Origem**: PRD M1-09.

Impedir que terceiros consultem ou alterem a biblioteca pessoal.

**Why this priority**: Impedir que terceiros consultem ou alterem a biblioteca pessoal.

**Independent Test**: Com identidade e conversa autorizadas configuradas e dados sintéticos preparados, comparar mensagens permitidas e negadas.

**Acceptance Scenarios**:

1. **US9-AS1** — **Given** a proprietária na conversa privada permitida, **When** ela envia uma solicitação textual, **Then** pode usar os fluxos do MVP sem comandos slash ou botões obrigatórios.
2. **US9-AS2** — **Given** outro remetente, conversa não permitida ou grupo, mesmo com nome de usuário igual, **When** chega uma solicitação, **Then** nenhum dado pessoal é consultado ou exibido e nenhuma ação da biblioteca é executada.
3. **US9-AS3** — **Given** configuração obrigatória ausente ou inválida, **When** o serviço é iniciado, **Then** o uso da biblioteca é bloqueado e o diagnóstico não revela credenciais.
4. **US9-AS4** — **Given** mensagem ambígua ou intenção fora do MVP 1, **When** a proprietária conversa com o bot, **Then** recebe esclarecimento ou indicação de limite, sem alteração indevida.

### Edge Cases

- Arquivo vazio, cabeçalho incompatível, aspas/quebras de linha em campos e linha inválida:
  respeitar a estrutura do arquivo, não inventar conteúdo, explicar falhas e contabilizar linhas.
  Arquivo vazio compatível produz relatório com zero processamentos, sem alterar a biblioteca.
- UID não é automaticamente ISBN; dado inválido não vira identificador confiável.
- Título igual com autores distintos ou identificadores conflitantes não prova mesma obra.
- Repetição da importação após enriquecimento/alteração pessoal não desfaz esses valores.
- Última página pode ter menos de três opções; não preencher com resultados inventados.
- Seleção de página anterior, expiração, mudança de intenção, índice inexistente ou resposta
  ambígua exigem nova escolha e nunca autorizam gravação por número isolado.
- Falha, lentidão ou limitação temporária de catálogo deve terminar com orientação de
  recuperação; não deixar espera indefinida nem impedir cadastro manual.
- Reentrega simultânea, reinício após salvar e resposta ao usuário perdida não duplicam efeitos.
- Conflito entre leitura da ficha e gravação exige revalidar a identidade/estado; não sobrescrever
  silenciosamente a decisão mais recente usando uma seleção obsoleta.
- Uma edição repetida não implica segunda cópia física. Tags de editora não implicam posse.
- Configuração incompleta, grupo ou identidade não permitida nunca expõem a biblioteca.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE permitir à proprietária importar localmente o CSV StoryGraph com validação de cabeçalho, título, autor e estado; respeitar aspas, quebras de linha e caracteres do arquivo. **Aceite:** US1-AS1, US1-AS4; Edge Cases.
- **FR-002**: O sistema DEVE mapear read para lido e to-read para quero ler, preservando ausências de ISBN, data, avaliação, resenha e edição; não criar sessão histórica. **Aceite:** US1-AS1, US1-AS5.
- **FR-003**: O sistema DEVE preservar tags originais e valores válidos explicitamente fornecidos; distinguir UID de ISBN e não inferir posse a partir de tags. **Aceite:** US1-AS5; Edge Cases.
- **FR-004**: O sistema DEVE reimportar de forma repetível sem criar novas obras já resolvidas nem sobrescrever estado manual, dados pessoais ou bibliografia já enriquecida. **Aceite:** US1-AS2, US8-AS2.
- **FR-005**: O sistema DEVE gerar relatório com totais inseridos, atualizados, inalterados e falhos e identificação por linha/motivo das falhas; a soma deve explicar todas as linhas processadas. Falha isolada não impede processar as demais; identidade incerta fica pendente de revisão sem fusão. **Aceite:** US1-AS3, US1-AS4.
- **FR-006**: O sistema DEVE apresentar resultados da biblioteca antes de qualquer catálogo e permitir abrir a ficha existente sem duplicação. **Aceite:** US2-AS1.
- **FR-007**: O sistema DEVE prosseguir para catálogo externo quando a proprietária decidir continuar; pesquisar primeiro Open Library e permitir Google Books quando não houver opção adequada. **Aceite:** US2-AS2, US3-AS1.
- **FR-008**: O sistema DEVE exibir resultados textuais numerados em páginas de três ou quatro opções quando houver quantidade suficiente, com próximos e voltar; a última página pode ser menor. **Aceite:** US3-AS2; Edge Cases.
- **FR-009**: O sistema DEVE associar a escolha à lista e ao livro efetivamente apresentados; invalidar escolhas expiradas ou de contexto anterior e pedir nova seleção, sem gravar. **Aceite:** US3-AS2, US3-AS3.
- **FR-010**: O sistema DEVE diante de falha ou ausência de resultado externo, informar o ocorrido e oferecer recuperação, continuação na próxima fonte disponível ou cadastro manual, sem inventar resultados. **Aceite:** US3-AS4.
- **FR-011**: O sistema DEVE exigir confirmação do título e autor do resultado externo selecionado antes de salvar, aceitando os demais metadados disponíveis da fonte sem transformar ausência em fato. **Aceite:** US4-AS1, US4-AS2.
- **FR-012**: O sistema DEVE usar quero ler como estado padrão do cadastro e permitir escolher lido. **Aceite:** US4-AS1, US5-AS1.
- **FR-013**: O sistema DEVE disponibilizar cadastro manual com título e autor obrigatórios e sem exigir ISBN, gênero, editora, data ou edição. **Aceite:** US5-AS1, US5-AS2.
- **FR-014**: O sistema DEVE verificar a identidade antes de concluir cadastro; reutilizar obra seguramente existente, pedir confirmação diante de candidato forte e nunca fundir automaticamente por semelhança. **Aceite:** US4-AS3, US5-AS3.
- **FR-015**: O sistema DEVE evitar duplicação de obra e de edição em gravações concorrentes e mensagens repetidas, inclusive após reinício. **Aceite:** US4-AS3, US4-AS4, US7-AS3, US8-AS4.
- **FR-016**: O sistema DEVE informar sucesso somente quando a gravação estiver confirmada; em falha ou resultado incerto, não afirmar que o livro foi salvo, e permitir repetição segura. **Aceite:** US4-AS4.
- **FR-017**: O sistema DEVE permitir enriquecimento bibliográfico sob demanda para obra inequivocamente identificada, confirmando a correspondência de título/autor. **Aceite:** US6-AS1, US6-AS3.
- **FR-018**: O sistema DEVE preservar estado, tags, posse e demais dados pessoais no enriquecimento e dar prioridade a correção manual explícita. **Aceite:** US6-AS1, US6-AS2.
- **FR-019**: O sistema DEVE manter origem e valores anteriores rastreáveis para a bibliografia enriquecida; identidade conflitante exige revisão, e falha de fonte preserva a ficha. **Aceite:** US6-AS1, US6-AS3.
- **FR-020**: O sistema DEVE permitir zero, uma ou várias edições possuídas por obra, escolhidas em catálogo ou informadas por editora/ano/formato sem ISBN. **Aceite:** US7-AS1, US7-AS2, US7-AS4.
- **FR-021**: O sistema DEVE vincular cada edição à obra correta, distinguir edições diferentes e registrar a mesma edição uma vez, sem inferir quantidade de cópias físicas. **Aceite:** US7-AS2, US7-AS3, US7-AS4.
- **FR-022**: O sistema DEVE alterar lido e quero ler em ambos os sentidos após identificar a obra, mostrando livro e efeito, sem fabricar data, sessão ou progresso. **Aceite:** US8-AS1, US8-AS2.
- **FR-023**: O sistema DEVE pedir esclarecimento quando livro ou ação forem ambíguos; revalidar escolhas obsoletas antes de alterar e não tratar sim isolado como autorização. **Aceite:** US2-AS3, US3-AS3, US8-AS3, US9-AS4.
- **FR-024**: O sistema DEVE autorizar somente a proprietária e a conversa privada configuradas antes de consultar ou modificar dados; nomes de usuário não autorizam, e grupos ou outros IDs não recebem dados pessoais. **Aceite:** US9-AS1, US9-AS2.
- **FR-025**: O sistema DEVE permitir os fluxos por texto em português sem exigir comandos slash, botões ou uma interpretação ilimitada de linguagem natural. **Aceite:** US9-AS1, US9-AS4.
- **FR-026**: O sistema DEVE impedir o uso sem configuração obrigatória válida, preservar a configuração local existente e não revelar segredos ou conteúdo pessoal nos diagnósticos. **Aceite:** US9-AS3; CR-003.
- **FR-027**: O sistema DEVE limitar esta entrega ao MVP 1 e informar que intenções de etapas posteriores não estão disponíveis, sem executar ações substitutas. **Aceite:** US9-AS4; Assumptions.

### Constitution Requirements *(mandatory)*

- **CR-001 — Escopo e precedência:** aplicar a constituição e os nove itens MVP 1 do PRD.
  Decisões de arquitetura, stack, versões e integração serão detalhadas no plano sem
  substituir as escolhas já ratificadas. Aceite: revisão de escopo e ausência dos recursos
  excluídos em Assumptions.
- **CR-002 — Evidência:** automatizar cenários de comportamento e falha das histórias,
  incluindo acesso negado, reimportação, concorrência, seleção expirada e ausência de dados.
  Usar dados sintéticos; registrar resultado das verificações e limitações reais.
  Aceite: cenários desta especificação associados a testes e evidências na entrega.
- **CR-003 — Privacidade e operação:** preservar configuração local já existente, sem
  copiar valores para documentação, repositório, testes ou diagnósticos. Expor somente
  a saúde local prevista para operação, nunca dados pessoais publicamente. Aceite:
  configuração ausente bloqueia uso sem revelar valores; verificação de ausência de
  segredos nos artefatos e de acesso pessoal externo negado.
- **CR-004 — Documentação:** atualizar README completo e todos os documentos afetados
  na mesma entrega: PRD, ADRs, contratos, dados, segurança, operação, testes, backlog e
  artefatos Spec Kit. Registrar áreas não afetadas com justificativa. Aceite: README
  descreve estado real, configuração sanitizada e comandos existentes/verificados;
  links e documentos refletem o comportamento entregue, sem pendência documental.

### Key Entities *(include if feature involves data)*

- **Proprietária autorizada**: única pessoa com acesso, vinculada à conversa privada permitida.
- **Obra**: título, autores e identidade bibliográfica, com estado lido/quero ler e tags originais;
  não se confunde com edição, exemplar possuído ou sessão de leitura.
- **Edição possuída**: edição/formato declarado pela proprietária e associado a uma obra;
  pode ter editora, ano e ISBN; uma obra admite nenhuma ou várias edições distintas.
- **Candidato de catálogo**: opção bibliográfica externa com título, autores, identificadores
  disponíveis e origem; não prova que a proprietária possui ou leu o livro.
- **Seleção pendente**: livro e ação apresentados no contexto de uma página/conversa;
  perde validade após expiração ou mudança de contexto.
- **Execução de importação**: origem do arquivo e resultado de processamento, totais e
  falhas por linha; permite explicar o resultado e repetir sem duplicar.
- **Proveniência bibliográfica**: origem de dados importados/enriquecidos e valores
  anteriores necessários para rastrear mudanças sem apagar declarações pessoais.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: No corpus inicial íntegro descrito e biblioteca vazia, 845 obras ficam
  disponíveis, com 764 lidas e 81 por ler; zero sessões, datas ou posses são inventadas.
- **SC-002**: Reaplicar o arquivo inicial produz zero novas obras e preserva 100% das
  alterações pessoais e dos campos bibliográficos enriquecidos nos cenários de aceite.
- **SC-003**: Em 100% das buscas de aceite com correspondência local, a ficha local vem
  primeiro; toda busca que prossegue usa a ordem de fontes e a opção da página escolhida.
- **SC-004**: Todas as jornadas de cadastro externo confirmado e manual válido terminam
  com o livro correto disponível no estado escolhido, sem exigir ISBN no fluxo manual.
- **SC-005**: Nos cenários de reentrega, concorrência, reinício e resposta perdida, há zero
  obras/edições duplicadas e zero alterações no livro errado.
- **SC-006**: Nos cenários de enriquecimento, 100% dos dados pessoais e correções manuais
  permanecem preservados, e a origem das mudanças bibliográficas pode ser identificada.
- **SC-007**: A proprietária consegue manter uma obra com três edições distintas, incluindo
  edição sem ISBN, e mudar lido/quero ler nos dois sentidos sem criar histórico fictício.
- **SC-008**: Em todos os cenários de acesso negado, expiração ou ambiguidade não resolvida,
  ocorrem zero gravações indevidas; acesso negado também revela zero dados pessoais.
- **SC-009**: Toda linha processada tem resultado explicável nos totais da importação;
  todas as falhas externas exercitadas oferecem orientação de recuperação sem falso sucesso.
- **SC-010**: A revisão de entrega encontra zero documento afetado desatualizado, zero link
  local quebrado nos documentos alterados e zero comando de produto apresentado como pronto
  sem implementação e validação correspondentes.

## Assumptions

- O [handoff](../../docs/CODEGEN_HANDOFF.md) determina implementar somente MVP 1;
  `docs/` inclui evolução futura e referências históricas, que não ampliam esta feature.
- Fora do escopo: sessões/progresso, datas presumidas, listagem/gestão de estantes,
  exclusão, avaliações/resenhas, recomendações, upload CSV no bot, web, capas/imagens,
  migração para Raspberry Pi e webhook. Preservar valor importado válido não cria
  funcionalidade de avaliação/resenha nesta etapa.
- Os números 845/764/81 vêm da documentação do corpus inicial; o CSV privado não foi
  aberto nem validado neste trabalho. Importações futuras não ficam limitadas a esses números.
- Os dados para testes serão sintéticos e equivalentes às regras de aceite. A conferência
  do corpus real pertence à validação local autorizada da implementação.
- Dependências externas são o canal Telegram, Open Library, Google Books e o arquivo
  StoryGraph fornecido localmente; indisponibilidade não autoriza inventar dados.
- A proprietária informou variáveis existentes; o README registra `.env` na raiz.
  Valores não foram lidos/validados. A implementação verificará completude sem sobrescrevê-los.
- As regras conservadoras em [decisões abertas](../../docs/00-governance/open-decisions.md)
  se aplicam: não contar cópias idênticas; não fundir por similaridade; esclarecer vocabulário
  não reconhecido. Nenhuma dessas decisões bloqueia esta especificação.
- Duração de contexto, limites de entrada, espera/tentativas e retenção operacional serão
  definidos com justificativa no plano. Não se assume espera ilimitada nem se inventam
  metas de desempenho sem medição, conforme o PRD.
- Os percentuais e contagens de sucesso são critérios para cenários de aceite controlados,
  não garantias estatísticas sobre comportamento futuro dos catálogos.
