> Referência histórica do pacote inicial. A fonte vigente é [03-data/initial-import.md](03-data/initial-import.md).
> Para estado e configuração atuais, consulte o [README principal](../README.md).

# Importação inicial do StoryGraph

Arquivo fornecido: `meus_livros_storygraph.csv` (não incluído neste pacote de documentação). Inspeção da amostra integral disponível: **845 registros**; `Read Status`: **764 `read`**, **81 `to-read`**. Cabeçalhos: `Title`, `Authors`, `ISBN/UID`, `Read Status`, `Star Rating`, `Review`, `Last Date Read`, `Tags`. ISBN/UID, avaliação, resenha e última data lida estão vazios nesta massa. Não houve duplicata exata por título+autor normalizados na inspeção; isso não garante ausência de edições/homônimos.

| Coluna | Destino MVP 1 | Regra |
| --- | --- | --- |
| `Title` | `works.title` | Obrigatório, preservar original e criar chave normalizada |
| `Authors` | `works.authors[]` | Obrigatório; preservar texto original e normalizar para busca |
| `ISBN/UID` | Proveniência/identificador somente se presente e classificado | Não inventar ISBN; distinguir ISBN de UID/edição |
| `Read Status` | `readEvidence` | `read` = lido sem sessão nem data; `to-read` = quero ler |
| `Star Rating`, `Review` | Preparar para etapa Web 2 se vierem preenchidos futuramente | Não criar nota/resenha vazia, nem descartar valor importado válido |
| `Last Date Read` | Data somente se explicitamente presente e válida | Não fabricar sessão histórica a partir do estado `read` |
| `Tags` | `works.rawTags[]` e proveniência | Preservar todos os valores; extrair gênero/editora/ano quando prefixo for reconhecido, sem apagar a tag original |

## Script local MVP 1

1. Ler CSV com parser que respeite aspas, quebra de linha e encoding; validar cabeçalho e contar registros.
2. Criar `import_run` com hash do arquivo e versão do mapeamento. Para cada linha: validar título/autor/estado, normalizar, procurar candidatos, inserir ou mesclar de modo idempotente. Suspeita de colisão sem prova é falha revisável, não fusão silenciosa.
3. Atualizar apenas campos permitidos; preservar metadados bibliográficos já enriquecidos, estado alterado manualmente, estantes e dados pessoais. Repetir arquivo idêntico não volta `lido` para `quero ler` nem cria outra obra.
4. Registrar totais `inserted`, `updated`, `unchanged`, `failed`, com código/motivo e número da linha para falhas; imprimir resumo claro no terminal. Falha em uma linha não oculta as demais.
5. Comparar contagem pós-importação com linhas únicas resolvidas, verificar amostra de títulos e estados. Uma segunda execução deve resultar em zero novas obras.

## MVP 3

O mesmo motor de mapeamento passa a receber arquivo do Telegram após autenticação. Acrescentar prévia com contagens antes de gravação, confirmação com expiração e execução registrada. O painel para resolver falhas aparece na Web 1. Não aceitar outros layouts até receber amostra e especificação; formato Maratona fica posterior.

**Nota sobre `Tags`:** tags de gênero, editora, ano e status são dados importados, não prova de exemplar possuído. Não convertê-las automaticamente em estantes pessoais editáveis sem regra explícita.
