# Checklist de desenvolvimento seguro

- [ ] Configuração falha no boot se faltar ID permitido, token ou Atlas URI.
- [ ] Auth Telegram testada antes de parser/lookup; chat privado, ID usuário e chat permitidos.
- [ ] Schemas de entrada com limite e campos extras recusados; comandos Mongo não recebem objetos externos.
- [ ] Resultados de catálogo tratados como texto não confiável; URL/host permitido e escape de apresentação.
- [ ] Seleção expirada ou ambígua não grava. Commit revalida identidade e índice único.
- [ ] CSV limita recursos; saída neutraliza fórmula e caracteres de controle.
- [ ] Logs estruturados sem token, texto livre ou CSV bruto; `import_row_errors` redigidos.
- [ ] Dependências e imagem verificadas, build sem segredo, CI com lint/typecheck/testes/scans.
- [ ] Web/API não aparece fora da tailnet; único caminho público é webhook com segredo.
- [ ] Backup restaurado em base isolada antes de migração destrutiva.
