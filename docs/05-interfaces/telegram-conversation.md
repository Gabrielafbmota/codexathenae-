# Contrato conversacional Telegram

| Intenção | Exemplo em português | Resposta esperada |
| --- | --- | --- |
| Buscar | `procure orgulho e preconceito` | locais primeiro, opção de prosseguir à fonte |
| Paginar | `próximos`, `voltar` | nova página de 3–4 com snapshot atualizado |
| Escolher | `o 2` | repetir título/autor e ação exata antes da gravação |
| Cadastrar manual | `quero cadastrar um livro` | perguntar título, autor e estado opcional |
| Mudar estado | `marque X como lido` | resolver X inequivocamente, mostrar efeito |
| Edição possuída | `tenho outra edição de X` | mostrar obra, pesquisar edição ou coletar editora/ano/formato |

`pendingIntent` registra fase (`search_results`, `confirm_work`, `duplicate_review`, `edition_review`, `change_state`), candidate IDs, page e expiry. Alteração de contexto invalida opções antigas. `sim` sem intenção pendente não executa nada. Mensagem ambígua provoca pergunta curta. Toda mensagem recusada por identidade/grupo para antes de qualquer consulta privada.

Etapas futuras: frases para progresso, nota, sentimentos e estantes seguem o mesmo padrão de identificação exata, confirmação em exclusões e feedback de sucesso/falha. Não exigir comandos slash ou botões.
