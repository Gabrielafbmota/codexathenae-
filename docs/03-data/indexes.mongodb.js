// Esboço para revisão com driver/versão MongoDB escolhidos; executar por migração versionada.
db.works.createIndex({ 'externalIds.openLibraryWorkKey': 1 }, { unique: true, partialFilterExpression: { 'externalIds.openLibraryWorkKey': { $type: 'string' } } });
db.works.createIndex({ normalizedTitle: 1, normalizedAuthors: 1 });
db.editions.createIndex({ 'externalIds.openLibraryEditionKey': 1 }, { unique: true, partialFilterExpression: { 'externalIds.openLibraryEditionKey': { $type: 'string' } } });
db.editions.createIndex({ isbn13: 1 }, { unique: true, partialFilterExpression: { isbn13: { $type: 'string' } } });
db.editions.createIndex({ workId: 1, publisherNormalized: 1, publicationYear: 1, formatNormalized: 1 });
db.telegram_sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
db.processed_updates.createIndex({ updateId: 1 }, { unique: true });
db.processed_updates.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
// Criar somente no MVP 2; o predicado parcial permite várias sessões concluídas.
db.reading_sessions.createIndex({ workId: 1 }, { unique: true, partialFilterExpression: { status: 'open' } });
db.progress_events.createIndex({ sessionId: 1, occurredAt: 1, _id: 1 });
// Criar somente no MVP 3.
db.shelf_memberships.createIndex({ shelfId: 1, workId: 1 }, { unique: true });
db.personal_shelves.createIndex({ normalizedName: 1 }, { unique: true });
