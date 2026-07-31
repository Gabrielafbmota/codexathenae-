# SPEC-002 — Catálogo de livros

## Objetivo

Permitir cadastrar, consultar, listar, atualizar e excluir logicamente livros da biblioteca pessoal.

## Regras de domínio

- ISBN-10 e ISBN-13 devem ser normalizados e validados por checksum;
- um ISBN normalizado pertence a apenas um livro ativo;
- livros sem ISBN são permitidos;
- vários livros podem estar com status `reading`;
- dados confirmados pela usuária não são sobrescritos automaticamente;
- exclusão é lógica e auditável.

## Endpoints iniciais

- `POST /api/v1/books`;
- `GET /api/v1/books`;
- `GET /api/v1/books/{book_id}`;
- `PATCH /api/v1/books/{book_id}`;
- `DELETE /api/v1/books/{book_id}`.

## Critérios de aceite

- criação retorna `201` e header `Location`;
- ISBN inválido retorna `422`;
- ISBN duplicado retorna `409`;
- recurso inexistente retorna `404`;
- listagem suporta paginação e filtro por status;
- livros excluídos não aparecem por padrão;
- schemas de entrada e saída são separados;
- domínio não importa FastAPI, Pydantic ou PyMongo;
- índice único parcial protege a deduplicação também em concorrência.

## Testes mínimos

- criação com e sem ISBN;
- ISBN inválido e duplicado;
- consulta e listagem paginada;
- atualização;
- soft delete;
- concorrência para ISBN duplicado;
- testes arquiteturais de dependência entre camadas.
