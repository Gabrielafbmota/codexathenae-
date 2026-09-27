# Backup e recuperação

Atlas: verificar política de backup do plano contratado e retenção efetiva, sem pressupor recurso pago. Antes de migração destrutiva ou importação em produção, criar backup/snapshot exportado seguro. Guardar cópia cifrada com acesso restrito e política definida pela proprietária.

**Ensaio:** restaurar em banco isolado; comparar quantidade de obras, edições, sessões, progressos, ratings e vínculos; verificar uma amostra com notas e releitura; documentar duração e falhas. Não usar base real como destino de teste.

**Etapa 8:** backup completo em CSVs relacionados com manifesto (versão, contagens, hashes, timezone, encoding e relações); restauração só em base vazia, pré-validada integralmente. CSV StoryGraph isolado não recupera sessões/posse.

**RPO/RTO:** ainda não acordados. Medir após primeiro ensaio e decidir frequência de backup compatível com uso pessoal.
