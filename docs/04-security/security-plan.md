# Plano de segurança e operação

Escopo: uma proprietária, bot privado e MongoDB Atlas; Web futura restrita à tailnet. A ausência de login web é decisão de produto e pressupõe acesso à tailnet controlado.

## Ameaças e controles

| Risco | Controle e verificação |
| --- | --- |
| Terceiro envia mensagem ao bot ou em grupo | Checar `from.id`, `chat.id` configurados e `chat.type=private` **antes** de interpretar, buscar ou responder com dados. Teste de ID errado, grupo, encaminhamento e payload sem usuário |
| Token do bot, URI Atlas ou segredo webhook vazam | Segredos fora de Git/imagens/logs; arquivo local ignorado pelo Git com permissões restritas ou Compose secrets; rotação documentada, exemplo `.env.example` sem valores; checar logs de inicialização |
| Dados pessoais em Atlas | TLS, usuário Atlas dedicado com privilégios mínimos na base, IP access list restrita, backups e política de retenção; não exibir URI em exceções |
| Injeção em entrada Telegram/CSV/Web | Validação de esquema e tamanho, campos Mongo construídos por código (nunca operador `$` de usuário), escape de saída HTML/Markdown, limites de upload e paginação, normalização controlada |
| APIs externas lentas ou indisponíveis | Hosts permitidos fixos, HTTPS, timeout, limite de respostas, retry limitado com backoff para 429/5xx; nenhuma URL arbitrária de usuário; falha legível e cadastro manual |
| Atualização repetida ou corrida | Índices únicos, escrita idempotente por `updateId`, revalidação de seleção no commit, versão/estado antes de alteração; teste de mensagens repetidas e inserção concorrente |
| CSV malicioso e exportação | Validar encoding, cabeçalho, extensão/tamanho/linhas e campos; limitar recursos; ao exportar neutralizar células iniciadas por `=`, `+`, `-`, `@` e caracteres de controle conforme consumidor; teste em planilha |
| Acesso indevido à Web/API futura | NGINX/Funnel expõe somente webhook; Web/API vinculados ao Serve/tailnet e ACL de dispositivo/usuária; testar de fora da tailnet; CORS e proteção de mutações adequados ao modo de acesso escolhido |
| Webhook falso | Validar `X-Telegram-Bot-Api-Secret-Token` com comparação segura; método/path e corpo limitados; depois verificar ID privado; não depender apenas de URL secreta |
| Logs revelam notas/sentimentos | Logar IDs opacos, ação, resultado, duração e código de falha; redigir texto livre, IDs de Telegram quando possível, segredos e CSV bruto; restringir acesso e retenção |
| Perda ou corrupção de dados | Backups Atlas testados periodicamente por restauração isolada; script de exportação completa na etapa 8; migração versionada com backup prévio |

## Controles por etapa

**MVP 1:** allowlist privada, configuração validada na inicialização, segredos fora do repositório, Atlas TLS/usuário mínimo/IP restrito, validação de entrada, limites e logs sem conteúdo sensível. Endpoint Fastify de saúde em loopback e sem dados. Uma única instância do polling.

**MVP 3:** arquivo CSV recebido só na conversa privada permitida; limitar bytes/linhas, reconhecer layout, preview, confirmação, logs estruturados de sucesso e falha por linha. `safeRowExcerpt` deve evitar campos livres extensos.

**Pi/Web:** desligar polling antes de habilitar webhook; configurar segredo Telegram, proxy HTTPS, limitador e somente rota de webhook via Funnel. Testar exposição com cliente fora da tailnet; UI e APIs pessoais somente via tailnet, regras de ACL de acesso restritas. Não confiar apenas em CORS. Caso seja necessária sessão de navegador, aplicar cookies seguros e proteção CSRF; determinar no desenho Web 1 sem criar login novo.

**Recomendações:** descrições externas e conteúdo produzido por IA são dados não confiáveis; não executar instruções contidas neles. Classificação sensível registra evidência e correção manual prioritária. Não afirmar ausência de tema quando informação é insuficiente.

## Procedimentos operacionais mínimos

1. Provisionar bot token e Atlas fora do repositório; revogar/rotacionar ao suspeitar exposição.
2. Verificar IP de saída autorizado no Atlas, conexão TLS, coleção/índices e saúde antes da importação.
3. Registrar deploy manual, versão, resultado de migração e backup; falha interrompe inicialização, sem pular migração.
4. Monitorar falhas de polling/webhook, 429 de provedores, timeout Atlas e erros de importação por código; não gravar mensagens completas.
5. Restaurar somente em ambiente isolado para ensaio; validar contagens, amostra de obras e histórico, depois documentar procedimento de produção.

**Fontes oficiais:** [Telegram webhook secret token](https://core.telegram.org/bots/api#setwebhook), [Atlas network security](https://www.mongodb.com/docs/atlas/security/), [Docker Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/), [Tailscale Funnel](https://tailscale.com/kb/1223/funnel), [Tailscale Serve](https://tailscale.com/kb/1312/serve), [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), [OWASP CSV injection](https://owasp.org/www-community/attacks/CSV_Injection).
