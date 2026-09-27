# Runbooks rápidos

## Bot não responde

Checar container, conexão Telegram e Atlas, token sem imprimir, rede/IP Atlas e último `update_id`; confirmar único polling. Reiniciar preservando cursor/idempotência; enviar mensagem privada de smoke.

## Open Library/Google Books falha

Verificar reason code, timeout/429 e backoff; não repetir agressivamente. Oferecer cadastro manual; reconsultar sob demanda.

## Importação parcial

Ver `import_run`, totais e `import_row_errors`; corrigir somente linha/proveniência, repetir motor idempotente; não zerar biblioteca.

## Índice único falha na migração

Parar boot, executar auditoria read-only de duplicatas e identidade de obra/edição; backup antes de correção; não remover índice nem apagar registros para fazer boot passar.

## Webhook não recebe

Checar registro Telegram, NGINX/Funnel, TLS e segredo, sem expor Web; retomar polling apenas após desativar webhook.
