# Implantação e rede

## MVP 1 no computador

Compose executa bot/API Fastify e ferramentas de migração/importação. MongoDB é Atlas, fora do Compose. Fastify health em `127.0.0.1`, sem rota de dados pública. Bot inicia após conexão, índices e importação inicial verificados. Um único consumidor `getUpdates` por token. Deploy manual: atualizar código/imagem, executar migrações, iniciar, conferir log de autorização e smoke com conversa privada.

## Etapa 4 no Raspberry Pi

Criar backup, parar polling, configurar token e webhook secret, publicar somente POST `/telegram/webhook` via NGINX + Tailscale Funnel com TLS, registrar `setWebhook`, testar header e ID. UI/API pessoal futura via Tailscale Serve/rede privada e ACL; configuração de portas deve respeitar limitações de Serve/Funnel no mesmo host/porta. Teste externo deve ver somente webhook e nunca dashboard. Rollback: remover webhook, restaurar polling único após garantir que Pi não consome duplicado.

## Configuração 12-factor

Segredos e ID permitido por ambiente/secret file, logs stdout estruturados, processo stateless salvo contexto conversacional em Mongo, build imutável, saúde local. Não incluir `nginx`, Tailscale ou webhook no MVP 1.

## Arquivo de ambiente e documentação operacional

Preservar o `.env` local existente e manter `.env`/`..env` fora do Git e das imagens.
Um arquivo com nome personalizado exige carregamento explícito; no Compose,
`--env-file` seleciona o arquivo para interpolação, enquanto `environment` ou
`env_file` define o que chega ao container. Não presumir que todas as variáveis
sejam automaticamente exportadas ao processo.

O Compose ainda não foi implementado. Ao criá-lo, documentar e testar no README
os comandos reais de inicialização, importação, saúde, parada e recuperação,
sem imprimir configuração resolvida com valores sensíveis. Atualizar os runbooks
na mesma entrega de qualquer alteração operacional.

Fonte: [Docker Compose: interpolação e arquivo de ambiente](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).
