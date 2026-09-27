# Observabilidade e objetivos iniciais

**Logs:** JSON com timestamp UTC, request/update correlation, caso de uso, workId opaco, source, duração, outcome e reason code. CSV `runId`/linha; nunca token, nota, review ou texto de consulta por padrão.

**Métricas:** tempo de resposta Telegram, busca local/fonte, 429/timeout por provedor, taxa de cadastro duplicado, linhas importadas/falhas, conexão Atlas, lag de polling/webhook, erro de entrega. Na Web, taxa de falha de dashboard e filtros.

**Alertas operacionais locais:** bot não processa updates, Atlas indisponível, importação com falha, webhook com rejeição anômala; no MVP local pode ser verificação manual de logs, sem stack de métricas exigida.

**SLO:** não fixar número antes de medições. Meta qualitativa MVP 1: nenhuma edição incorreta ou duplicata por reentrega; falha de catálogo leva a cadastro manual; indisponibilidade é visível. Coletar baseline e definir limiares após uso real.
