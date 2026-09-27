# Migrações e integridade

## Bootstrap MVP 1

1. Validar configuração, TLS/Atlas e versão de schema esperada.
2. Criar índices de obra, edição e inbox com migração versionada.
3. Importar CSV local via `import_run`, usando parser com aspas e encoding explícito.
4. Verificar contagens 845/764/81 e repetir para demonstrar idempotência.
5. Liberar polling somente após índices e importação concluídos.

## Alterações posteriores

- Migrações `up` pequenas, registradas em `schema_migrations` com ID e checksum; falha interrompe boot.
- Índice único em coleção com dados existentes exige auditoria de duplicatas antes de criar; nunca remover registros automaticamente.
- Campos novos são opcionais até backfill concluído. Backup antes de exclusão/renomeação de campo.
- M2 introduz sessões/eventos e índice parcial de sessão aberta; M3 estantes/import errors; Web 2 ratings/profile; rec filtros/candidatos; export sem alterar identidades.
- Reconciliar `readEvidence` com sessões concluídas após alteração, sem apagar evidência importada.

## Checks de integridade

Edição aponta a obra existente; sessão aponta a obra e edição opcional da mesma obra; evento aponta sessão; rating de sessão aponta mesma obra; vínculo de estante aponta a obra; falha aponta `import_run`. Executar script read-only de contagens e órfãos antes/depois de cada migração.
