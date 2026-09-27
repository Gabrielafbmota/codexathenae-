# Pontos a decidir durante a implementação

As respostas abaixo não bloqueiam o início do MVP 1; adotar a regra conservadora indicada até decisão da proprietária.

| Tema | Ponto aberto | Regra provisória |
| --- | --- | --- |
| Exemplares idênticos | Quantidade de cópias físicas da **mesma edição** ainda não foi definida | Registrar edição possuída uma vez; não inferir contagem; discutir antes de suportar quantidade |
| Livro homônimo | Quão forte é a similaridade necessária para perguntar? | IDs exatos resolvem; título+autor exatos normalizados como candidato forte; fuzzy exige título e autor muito próximos e confirmação; não fundir automaticamente |
| Catálogo/idioma | Cobertura e qualidade de tema/idioma no corpus de recomendações | Medir amostra de dados antes de escolher tamanho do dump, índices e classificadores; manter `unknown` |
| Telegram parser | Vocabulário natural inicial de mensagens | Implementar frases representativas e confirmação de ambiguidades; ampliar com observações reais, sem IA obrigatória |
| Preferências de segurança web | Política de sessão/CSRF em app sem login | Definir junto da Web 1 e testar tailnet-only; nunca inferir que CORS autentica |
| Exportação | Mapeamento exato do CSV StoryGraph quando campos evoluírem | Manter cabeçalhos recebidos e documentar perdas inevitáveis em formato de uma linha por obra; backup completo é a opção sem perda |

Qualquer nova decisão deve atualizar PRD, ADR pertinente, modelo/fluxo e teste de aceite correspondente.
