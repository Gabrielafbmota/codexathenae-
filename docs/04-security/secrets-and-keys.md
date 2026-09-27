# Segredos e chaves

| Segredo | Uso | Local e rotação |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | polling e envio | secret local/Compose, fora de Git, revogar pelo BotFather em suspeita |
| `MONGODB_URI` | Atlas | usuário dedicado com privilégio mínimo, IP restrito e TLS; rotacionar na Atlas |
| `TELEGRAM_WEBHOOK_SECRET` | validar header no Pi | gerar valor aleatório separado do bot token; trocar junto do `setWebhook` |
| Google Books API key se necessária | quota de consultas | escopo/restrições e secret local, não enviar ao cliente |

Não registrar valor nem fragmento em log, stack trace, URL compartilhada ou screenshot. `.env.example` só nomes e descrições; arquivos reais ignorados por Git, permissões restritas. Separar credenciais de dev/Pi; nunca usar token de produção em CI. Rotação: provisionar novo, testar, trocar serviço, revogar antigo, registrar evento sem valor.

## Configuração local existente

A proprietária informou variáveis locais em `..env`; na raiz foi constatado `.env`
(um ponto), sem leitura de conteúdo. Preservar esse arquivo e seus valores.
Ambas as grafias estão protegidas por `.gitignore`; se um caminho personalizado
for usado, o carregamento deve ser explícito. Não renomear nem sobrescrever
configuração sem necessidade. Documentar nomes, obrigatoriedade e validação quando
o contrato de configuração for implementado, sem copiar credenciais.

Na revisão inicial, `.env` estava rastreado pelo Git. Removê-lo do índice mantém a
cópia local, mas não elimina versões anteriores. Se continha credenciais reais,
rotacioná-las; ignorar o arquivo não revoga segredos presentes no histórico.
