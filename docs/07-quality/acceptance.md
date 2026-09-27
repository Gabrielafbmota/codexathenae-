# Cenários de aceitação

| ID | Dado | Quando | Então |
| --- | --- | --- | --- |
| AC-01 | CSV inicial íntegro | importo em base vazia | 845 obras; 764 lidas, 81 quero ler; zero sessões/edições inventadas |
| AC-02 | CSV já aplicado | importo outra vez | zero novas obras e estados manuais preservados |
| AC-03 | obra existente | busco pelo título | ficha local vem primeiro e abre sem duplicar |
| AC-04 | título não encontrado localmente | busco | Open Library antes de Google Books, com fallback |
| AC-05 | >4 resultados | digo `próximos` e `o 2` | escolha corresponde à página corrente, não à anterior |
| AC-06 | resultado externo | confirmo título/autor | obra salva com `quero ler` padrão alterável |
| AC-07 | título/autor similares mas distintos | salvo | pergunta diante de suspeita forte, sem fusão automática |
| AC-08 | mesmo update concorrente | recebo duas vezes | apenas uma obra/edição persistida |
| AC-09 | obra com três edições distintas | cadastro | uma obra e três edições possuídas; CSV por si não cria edição |
| AC-10 | livro importado lido | altero quero ler e depois lido | estados corretos sem data ou sessão fictícia |
| AC-11 | outro ID/grupo | envia busca | nenhum dado pessoal retorna e nenhuma escrita ocorre |
| AC-20 | duas obras em leitura | inicio ambas | ambas abertas; segunda sessão da mesma obra exige escolha |
| AC-21 | sessão percentual | tento lançar página | rejeita troca de unidade; releitura nova pode escolher página |
| AC-22 | progresso 100% | lanço | conclui automaticamente, data corrigível |
| AC-23 | evento final apagado | confirmo exclusão | estado reavaliado e pergunta se ambíguo |
| AC-30 | releitura de obra lida | abro sessão | aparece em `Lidos` e `Lendo` |
| AC-31 | CSV com linha inválida | confirmo importação | demais linhas entram, falha rastreada por linha |
| AC-40 | 764 lidos sem datas | vejo gráfico mensal | entram no total, não no mês |
| AC-50 | notas 3,5 e 4 | avalio | média exata 3,75; apresentação arredondada a 4,0 |
| AC-60 | lido/lendo/rejeitado | peço sugestões | nenhum aparece; `quero ler` pode aparecer |
| AC-61 | tema explícito bloqueado | peço sugestões | livro excluído inclusive da seção da estante; vínculo preservado |
| AC-62 | tema contextual/desconhecido | peço sugestões | aviso apropriado, sem afirmar segurança |
| AC-70 | base não vazia | tento restaurar | restauração bloqueada sem alteração |

## Detalhamento da feature MVP 1

A [especificação ativa](../../specs/001-biblioteca-mvp1/spec.md) detalha as nove
histórias do PRD, incluindo aceite de enriquecimento e caminhos adversariais.
A [rastreabilidade](../00-governance/traceability.md) relaciona os itens do PRD aos
requisitos e resultados esperados. Cenários posteriores ao MVP 1 continuam futuros.
Este documento não substitui o `tasks.md`, que será gerado após o planejamento.
