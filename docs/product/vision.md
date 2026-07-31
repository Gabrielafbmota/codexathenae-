# Visão do produto

## Produto

O CodexAthenae é uma plataforma pessoal para organização de biblioteca, acompanhamento de leituras e automação de tarefas relacionadas a livros.

## Problema

Informações sobre livros, progresso, avaliações, listas de leitura e metadados ficam dispersas entre planilhas, anotações e serviços externos. O CodexAthenae centraliza esses dados e cria uma base confiável para consultas, automações e futuras recomendações.

## Objetivo da primeira versão

Permitir que uma única usuária:

1. cadastre um livro por título ou ISBN;
2. consulte metadados em fontes externas;
3. revise os candidatos encontrados antes de salvar;
4. evite duplicidades por ISBN;
5. consulte sua biblioteca;
6. altere status e progresso de leitura.

## Capacidades futuras

- cadastro por fotografia;
- bot do Telegram;
- sessões de leitura;
- lembretes de 2, 7, 15 e 30 dias;
- metas e dashboard;
- importação em massa;
- recomendações assistidas por IA.

## Fora do escopo inicial

- múltiplos usuários;
- aplicativo móvel nativo;
- marketplace;
- rede social;
- agente autônomo com execução arbitrária;
- recomendações por IA;
- OCR de capas;
- processamento em massa.

## Regras de produto já definidas

- MongoDB é a fonte oficial dos dados da aplicação.
- Um ISBN normalizado identifica no máximo um livro.
- Pode haver vários livros com status `reading`.
- Dados externos não sobrescrevem dados confirmados sem autorização.
- O sistema trabalha prioritariamente com edições em português do Brasil.
- Status suportados inicialmente: `want_to_read`, `reading`, `read` e `abandoned`.
- Avaliações usam escala de 1 a 5, com intervalos de 0,5.
