# SPEC-003 — Enriquecimento de metadados

## Objetivo

Buscar candidatos de livros por ISBN, título e autor usando provedores externos, sem persistir alterações antes da confirmação da usuária.

## Provedores

1. Google Books como fonte primária;
2. Open Library como fallback e fonte complementar.

## Modelo canônico

Cada candidato pode conter título, subtítulo, autores, ISBNs, editora, ano da edição, ano original quando confiável, descrição, páginas, gêneros, idioma, capa, fonte e nível de confiança.

## Regras

- chamadas externas possuem timeout explícito;
- `429`, timeouts e `5xx` são tratados como falhas transitórias;
- erros `4xx` não transitórios não recebem retry automático;
- resultados são normalizados antes de chegar à aplicação;
- candidatos duplicados são consolidados;
- no máximo 10 candidatos são retornados;
- nenhum resultado é uma resposta válida, não um erro interno;
- falha de um provedor não impede o uso do outro;
- dados externos só são aplicados após confirmação;
- a origem dos dados é registrada.

## Critérios de aceite

- busca por ISBN e por título/autor;
- fallback para Open Library quando necessário;
- retorno consistente independentemente do provedor;
- confirmação separada da pesquisa;
- ausência de chamadas externas reais nos testes;
- nenhuma chave ou credencial aparece em logs.

## Testes mínimos

- sucesso em cada provedor;
- nenhum resultado;
- fallback;
- combinação e deduplicação;
- payload incompleto ou inválido;
- timeout, `429` e `5xx`;
- indisponibilidade de todos os provedores.
