# Resposta a incidentes

## Token Telegram vazou

Desabilitar ou rotacionar token no BotFather; interromper bot; trocar segredo de webhook se existir; revisar updates e logs de acesso sem reproduzir conteúdo pessoal; testar allowlist e reativar com novo token.

## Credencial Atlas vazou

Revogar usuário/URI, restringir IP access list, criar usuário mínimo novo, revisar Atlas logs e alterações, restaurar de backup isolado se integridade estiver comprometida; registrar período e ações.

## Duplicata/fusão incorreta

Suspender importação ou caso de uso afetado; preservar snapshot/backup e `import_run`; identificar IDs, edições, sessões e referências; preparar correção auditável e teste de regressão. Não apagar ficha equivocada antes de mapear referências.

## Web exposta fora da tailnet

Desabilitar ingress do Funnel/NGINX para rota pessoal; verificar configuração e logs, invalidar segredos expostos, testar de rede externa antes de reabrir.

## Recuperação

Registrar linha do tempo, causa, alcance, dados afetados, correção e teste. A proprietária decide comunicação externa se necessária. Não guardar segredos ou texto livre no relatório.
