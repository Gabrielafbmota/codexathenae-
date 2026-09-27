# Fluxos funcionais

Diagramas são especificação de comportamento; textos de mensagem são exemplos, não comandos obrigatórios.

## Busca e cadastro — MVP 1

```mermaid
flowchart TD
  A[Mensagem com título] --> B{Remetente privado autorizado?}
  B -- Não --> X[Ignorar sem dados]
  B -- Sim --> C[Buscar obras locais]
  C --> D{Encontrou a desejada?}
  D -- Sim --> E[Abrir ficha existente]
  D -- Não --> F[Buscar Open Library]
  F --> G{Escolheu resultado?}
  G -- Não --> H[Buscar Google Books]
  H --> I{Escolheu resultado?}
  I -- Não --> J[Cadastro manual]
  G -- Sim --> K[Confirmar título e autor]
  I -- Sim --> K
  J --> L[Validar título e autor]
  K --> L
  L --> M{Duplicata forte?}
  M -- Sim --> N[Confirmar obra existente]
  M -- Não --> O[Salvar obra]
  N --> E
  N --> O
```

Cada pesquisa retorna páginas de 3–4 opções textuais. A opção digitada se vincula ao snapshot da página e expira; antes da escrita o bot mostra exatamente título e autor. Se já existe, oferece abrir ou registrar edição possuída. A ação de cadastro sempre reconsulta chaves no banco antes de gravar, inclusive após confirmação.

## Edições possuídas — MVP 1

```mermaid
flowchart TD
  A[Obra inequívoca] --> B[Solicitar nova edição]
  B --> C[Buscar edição na fonte]
  C --> D{Metadados encontrados?}
  D -- Sim --> E[Confirmar edição e formato]
  D -- Não --> F[Informar editora ano formato]
  E --> G[Checar identidade da edição]
  F --> G
  G --> H{Já cadastrada?}
  H -- Sim --> I[Exibir edição existente]
  H -- Não --> J[Registrar posse]
```

## Sessões e progresso — MVP 2

```mermaid
flowchart TD
  A[Iniciar leitura da obra] --> B{Sessão aberta desta obra?}
  B -- Sim --> C[Continuar concluir ou interromper]
  B -- Não --> D[Criar sessão]
  C --> D
  D --> E[Primeiro progresso escolhe unidade]
  E --> F[Salvar evento com data nota sentimentos]
  F --> G{100% ou última página?}
  G -- Sim --> H[Concluir sessão e convidar nota futura]
  G -- Não --> I[Manter aberta]
```

Se escolher continuar, não cria outra sessão. Páginas e porcentagem não se misturam na sessão. Marcar como lido sem progresso também conclui. Edição/exclusão de evento recalcula a condição de conclusão e solicita confirmação quando houver conflito.

## Importação incremental — MVP 3

```mermaid
flowchart TD
  A[Receber CSV] --> B[Validar layout e limites]
  B --> C[Preparar correspondências por linha]
  C --> D[Mostrar prévia e contagens]
  D --> E{Confirmou?}
  E -- Não --> F[Descartar prévia]
  E -- Sim --> G[Aplicar por linha idempotente]
  G --> H[Guardar execução e falhas]
  H --> I[Resumo de novos atualizados ignorados falhas]
```

Não criar data de leitura nem edição por inferência; estados e estantes manuais presentes têm prioridade. Cada falha conserva número da linha, código, motivo seguro e campos mínimos para revisão na Web 1.

## Recomendações — etapa 7

```mermaid
flowchart TD
  A[Pedido sob demanda] --> B[Estante ou candidatos verificáveis]
  B --> C[Resolver identidade de obra]
  C --> D[Excluir lidos lendo rejeitados]
  D --> E[Aplicar bloqueio sensível]
  E --> F[Ordenar por perfil idioma diversidade]
  F --> G[Exibir duas seções e fontes]
  G --> H[Registrar feedback ou pedir mais]
```

Conhecimento insuficiente sobre tema sensível rende aviso; representação explícita de tema bloqueado é excluída. Filtragem não altera estantes. Pedidos por autor/gênero/clima modificam ordenação e diversidade, sem remover regras de exclusão.
