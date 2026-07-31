# SPEC-006 — Integração com Telegram

## Objetivo

Oferecer uma interface complementar para consultar e atualizar a biblioteca sem acesso direto ao banco de dados.

## Comandos iniciais

- `/adicionar`;
- `/buscar`;
- `/lendo`;
- `/quero_ler`;
- `/progresso`;
- `/status`.

## Regras

- apenas usuários explicitamente autorizados podem operar o bot;
- toda operação passa pela API do CodexAthenae;
- ações de criação ou alteração exigem confirmação;
- comandos possuem rate limit;
- mensagens e operações usam correlation ID;
- tokens e conteúdos sensíveis não aparecem em logs;
- o bot não executa comandos arbitrários;
- estados de conversação possuem expiração.

## Critérios de aceite

- usuário não autorizado é rejeitado;
- cadastro apresenta candidatos antes de salvar;
- cancelamento não produz efeitos parciais;
- falhas da API geram mensagem clara e reprocessável;
- comandos são idempotentes quando aplicável;
- o bot não acessa o MongoDB diretamente.

## Testes mínimos

- autorização;
- cada comando principal;
- confirmação e cancelamento;
- expiração de estado;
- rate limit;
- timeout e erro da API;
- garantia de que dados sensíveis não sejam logados.
