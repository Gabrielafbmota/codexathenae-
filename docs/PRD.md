> Referência histórica do pacote inicial. A fonte vigente é [00-governance/prd.md](00-governance/prd.md).
> Para estado e configuração atuais, consulte o [README principal](../README.md).

# PRD — CodexAthenae

Versão 1.0 · 27/09/2026 · proprietária única.

## Problema e objetivo

Manter uma biblioteca pessoal rápida, com livros lidos e por ler, registrar leituras e recuperar o histórico. Etapas posteriores acrescentam organização, análise e recomendações. Não é um leitor de livros. Não existe plano de multiusuário.

**Princípios:** conversa natural e objetiva; nunca editar o livro errado; não inventar ISBN, datas, posse ou conteúdo; preservar informação pessoal durante enriquecimento; deduplicar obra e edição separadamente.

## MVP 1 — resultado exigido

Bot Telegram em conversa privada, rodando no computador da proprietária por polling; TypeScript/Node.js, Fastify e MongoDB Atlas, com Docker Compose. Sem interface, capa ou imagem. Script local importa o CSV StoryGraph uma vez, de modo repetível. Fluxo principal: buscar título na base local, depois Open Library e, se a opção desejada não for encontrada, Google Books; resultados textuais em páginas de 3–4; escolha textual; confirmar título e autor; salvar com estado `quero ler` por padrão, podendo escolher `lido`. Cadastro manual sempre disponível. Edições/formato possuídos opcionais: zero ou várias edições por obra.

### Histórias e aceite

| ID | História | Critério observável |
| --- | --- | --- |
| M1-01 | Importar a biblioteca inicial no computador | 845 linhas processadas (764 `read`, 81 `to-read`), relatório de inseridos/atualizados/falhas; repetir não duplica; dados ausentes continuam ausentes |
| M1-02 | Buscar um título já salvo | O bot apresenta primeiro o registro local e permite abri-lo; pesquisa externa só se a usuária quiser continuar |
| M1-03 | Buscar fora da base | Open Library antecede Google Books; se não houver opção adequada, continuar no Google; páginas com 3–4 opções numeradas, `próximos` e `voltar` |
| M1-04 | Salvar um resultado | Confirmar título e autor da opção exata; demais metadados da fonte são aceitos; deduplicar antes de inserir; padrão `quero ler` alterável |
| M1-05 | Cadastrar manualmente | Exigir título e autor, permitir ausência de ISBN, gênero, editora, data e edição; confirmar seleção se houver colisão forte |
| M1-06 | Atualizar livro existente | Abrir o registro encontrado; enriquecimento sob demanda atualiza bibliografia, preservando estado, tags e dados pessoais |
| M1-07 | Registrar posse opcional | Uma obra comporta múltiplas edições/formatos possuídos; pesquisar edição, ou cadastrar por editora/ano/formato sem ISBN; não criar edição implícita para CSV |
| M1-08 | Alterar estado | Trocar `quero ler` e `lido` em ambos os sentidos, após identificar o livro; leitura histórica não é fabricada |
| M1-09 | Restringir acesso | Mensagens de grupos e IDs não autorizados não executam casos de uso, nem exibem dados |

**Fora do MVP 1:** progresso, sessões, datas de conclusão presumidas, listagem de estantes, exclusão, avaliações, resenhas, recomendações, upload CSV no bot, web, capas, Raspberry Pi, webhook. Fastify pode expor somente saúde local para operação.

## Etapas seguintes e critérios principais

| Etapa | Escopo | Aceite distintivo |
| --- | --- | --- |
| MVP 2 | Sessões, releituras e progresso CRUD via Telegram | Muitos livros diferentes abertos; uma sessão aberta por obra; unidade escolhida por sessão no primeiro progresso e mantida; eventos históricos preservados; correções/exclusões confirmadas; notas e múltiplos sentimentos |
| MVP 3 | Estantes e importação CSV pelo bot | Estantes automáticas derivadas coexistem (`Lendo` e `Lidos`); manuais persistem; importação idempotente com prévia, confirmação, log de execução e falha por linha |
| Etapa 4 | Migrar bot para Raspberry Pi | Compose manual, NGINX e Tailscale Funnel; polling desligado, webhook autenticado; apenas webhook público |
| Web 1 | React/Vite/Tailwind, paridade funcional acumulada, painéis | Web/API pessoal só na tailnet; filtros para métricas e sentimentos; importações sem data só em totais; painel de erros; capas reais com fallback genérico |
| Web 2 | Avaliações, textos, perfil, paridade Telegram/web | Notas 1–5 por 0,5, média exata armazenada e exibida arredondada a 0,5; avaliação só após leitura; resenha opcional por sessão; anotações simples por obra; lista de não avaliados |
| Recomendações | Sob demanda, cinco por vez e mais | `Da sua estante` + `Novas descobertas`; excluir lidos/lendo e conteúdos bloqueados; justificativa verificável, tom honesto, sem spoilers, fonte e feedback |
| Exportação | CSV StoryGraph e backup completo separados ou ZIP | Escolha independente dos formatos; restauração integral apenas em banco vazio, sem mesclagem |

### Regras de leituras (MVP 2)

Sessão de leitura tem início automático corrigível, finalização automática corrigível e estado aberta/concluída/interrompida. Ao começar releitura da mesma obra com sessão aberta, perguntar se quer continuar, concluir ou interromper a sessão anterior. Livros diferentes não têm limite simultâneo. Primeira atualização escolhe páginas (página atual e total) ou porcentagem; a unidade vale até o fim da sessão, mas outra leitura escolhe de novo. Progresso regressivo exige confirmação. Última página ou 100% conclui automaticamente, mas é permitido concluir sem progresso. Evento inclui data/hora, nota curta e zero ou mais sentimentos de lista com emoji ou personalizados; pode conter apenas nota/sentimento. Editar e apagar sessão/evento depois de seleção inequívoca; exclusão definitiva requer confirmação. Ao desfazer conclusão, perguntar o estado resultante quando não puder ser inferido com segurança.

### Estantes (MVP 3)

`Quero ler`: nunca lido e sem sessão aberta. `Lendo`: sessão aberta. `Lidos`: já lido/importado como lido, mesmo em releitura. `Favoritos`, `Detestados` e personalizadas são manuais e coexistentes. Excluir estante pessoal não exclui seus livros. Tags originais do CSV permanecem mesmo após importações e enriquecimento.

### Análises e recomendações

Painel: totais, andamento, progresso, lidos por mês/ano, gêneros, estantes, frequência/evolução dos sentimentos e comparação por gênero; filtros de período, livro, gênero, estante e sentimento. O CSV lido sem data não alimenta série temporal. Perfil com pesos 0–10 de autor, gênero e tema; manuais prevalecem, 0 impede novas descobertas daquela preferência, 1 reduz peso. Avaliações e sentimentos alimentam estimativas editáveis.

Recomendar cinco livros por solicitação, com distribuição flexível entre duas seções; pedido pode restringir origem, autor, gênero ou clima. Candidatos são identificados no catálogo e confrontados por IDs e obra canônica com a biblioteca; nenhuma IA inventa um título ou decide sozinha se já foi lido. `Quero ler` pode aparecer; `Lidos` e `Lendo` não. Preferência por português, outros idiomas sinalizados e rebaixados. `Não tenho interesse` evita repetição; `já li` pede confirmação e atualiza. Títulos de estante manual não são removidos por mudança de preferências.

Temas sensíveis: representação explícita/detalhada de tema bloqueado exclui sugestão, inclusive da estante; mera menção contextual pode aparecer com aviso; ausência de evidência pode aparecer como não verificada. A ficha permite ver fonte/origem da classificação e corrigir, com prioridade manual. Uma classificação automática nunca é tratada como certeza. Não remover livro nem vínculo de estante ao filtrar uma recomendação.

## Identidade visual futura

Dark mode permanente. Fundo `#100C17`, painel `#1C1426`, roxo principal `#3B0366`, superfície `#25152F`, prata envelhecida `#AEA7B2`, texto `#F2ECEE`; medir contraste na implementação. Tipografia editorial antiga, interface simples. Logo aprovado: coruja em contorno prateado, de perfil lendo livro, detalhes roxos, sem óculos nem coluna; nome serifado. Capa genérica aprovada no mesmo estilo, usada se não houver capa real ou ela falhar.

## Medidas de sucesso e limites

- MVP 1: fluxo completo de importar, encontrar, confirmar, deduplicar e alterar estado sem edições incorretas; reiniciar o bot sem duplicar processamentos.
- Etapas futuras: taxa de importação resolvida, completude de datas declarada, distribuição de sugestões aceitas/rejeitadas e falsos positivos de deduplicação/sensibilidade revistos manualmente.
- Evitar metas arbitrárias de desempenho no MVP; instrumentar latências e falhas das APIs e definir limiares após uso real.
