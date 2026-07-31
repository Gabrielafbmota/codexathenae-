# SPEC-005 — Workflows n8n

## Objetivo

Orquestrar integrações assíncronas, retries, fallback, notificações e reprocessamentos sem transferir regras de negócio para o n8n.

## Responsabilidades do n8n

- receber eventos internos autenticados;
- consultar provedores externos;
- executar retry com backoff em falhas transitórias;
- acionar fallback;
- chamar callbacks internos;
- notificar sucesso ou falha;
- permitir reprocessamento controlado.

## Limites

O n8n não decide deduplicação, transições de leitura, persistência final nem sobrescrita de dados confirmados. Essas decisões pertencem à API.

## Segurança

- webhooks autenticados;
- segredos fora dos arquivos exportados;
- allowlist de destinos;
- limite de payload;
- timeout;
- idempotency key;
- logs sem tokens ou dados sensíveis;
- workflow de erro dedicado;
- princípio do menor privilégio.

## Critérios de aceite

- uma execução repetida não duplica efeitos;
- falhas transitórias são reprocessáveis;
- falhas definitivas terminam com estado explícito;
- workflows são exportados e versionados sem credenciais;
- callbacks rejeitam assinatura inválida;
- regras de negócio continuam testáveis sem n8n.

## Testes mínimos

- webhook autenticado e não autenticado;
- idempotência;
- retry e fallback;
- callback de sucesso e falha;
- indisponibilidade da API;
- reprocessamento manual seguro.
