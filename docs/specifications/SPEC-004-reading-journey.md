# SPEC-004 — Jornada de leitura

## Objetivo

Controlar status, progresso, datas, avaliações e comentários relacionados à leitura.

## Status

- `want_to_read`;
- `reading`;
- `read`;
- `abandoned`.

## Regras

- iniciar leitura registra `started_at` quando ainda não informado;
- concluir leitura registra `finished_at`;
- progresso pode ser informado por páginas ou percentual;
- páginas lidas não podem ser negativas nem superar o total conhecido;
- percentual deve permanecer entre 0 e 100;
- avaliação varia de 1 a 5 em incrementos de 0,5;
- várias leituras simultâneas são permitidas;
- alterações registram data e origem;
- transições inválidas geram erro de domínio.

## Operações iniciais

- alterar status;
- atualizar progresso;
- registrar avaliação;
- registrar comentário;
- consultar histórico básico.

## Critérios de aceite

- regras são aplicadas no domínio, não nos routers;
- progresso por páginas e percentual é normalizado;
- datas são armazenadas em UTC;
- conclusão e reabertura mantêm histórico coerente;
- erros de domínio são mapeados para respostas HTTP padronizadas.

## Testes mínimos

- todas as transições permitidas;
- transições inválidas;
- progresso válido e inválido;
- avaliação em incrementos de 0,5;
- início e conclusão automáticos;
- reabertura de livro concluído ou abandonado.
