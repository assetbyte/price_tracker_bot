# Details

Date : 2026-11-05 09:37:00

Directory /Users/setbdirahman/Desktop/road_to_1st_offer/price_tracker_bot_project

Total : 80 files,  3285 codes, 193 comments, 846 blanks, all 4324 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [Dockerfile](/Dockerfile) | Docker | 8 | 0 | 6 | 14 |
| [alembic.ini](/alembic.ini) | Ini | 123 | 0 | 27 | 150 |
| [alembic/env.py](/alembic/env.py) | Python | 46 | 28 | 29 | 103 |
| [alembic/versions/0b02ae8f12cd\_initial\_tables\_users\_trackings\_price\_.py](/alembic/versions/0b02ae8f12cd_initial_tables_users_trackings_price_.py) | Python | 60 | 14 | 7 | 81 |
| [alembic/versions/1bfe4536d1b9\_update\_price\_history\_schema.py](/alembic/versions/1bfe4536d1b9_update_price_history_schema.py) | Python | 13 | 14 | 8 | 35 |
| [alembic/versions/356c321e2170\_add\_stations\_table.py](/alembic/versions/356c321e2170_add_stations_table.py) | Python | 23 | 14 | 8 | 45 |
| [alembic/versions/4cc7c9c128f1\_add\_last\_notified\_price\_to\_trackings.py](/alembic/versions/4cc7c9c128f1_add_last_notified_price_to_trackings.py) | Python | 11 | 14 | 8 | 33 |
| [alembic/versions/5b79e389bd1c\_drop\_route\_column\_and\_refresh\_price\_.py](/alembic/versions/5b79e389bd1c_drop_route_column_and_refresh_price_.py) | Python | 17 | 14 | 8 | 39 |
| [alembic/versions/e694e0d902cd\_remove\_unique\_constraint\_from\_station\_.py](/alembic/versions/e694e0d902cd_remove_unique_constraint_from_station_.py) | Python | 11 | 14 | 8 | 33 |
| [app/bot/handlers/common.py](/app/bot/handlers/common.py) | Python | 27 | 0 | 6 | 33 |
| [app/bot/handlers/delete.py](/app/bot/handlers/delete.py) | Python | 54 | 0 | 15 | 69 |
| [app/bot/handlers/start.py](/app/bot/handlers/start.py) | Python | 21 | 0 | 10 | 31 |
| [app/bot/handlers/tracking.py](/app/bot/handlers/tracking.py) | Python | 435 | 4 | 92 | 531 |
| [app/bot/handlers/view.py](/app/bot/handlers/view.py) | Python | 32 | 0 | 8 | 40 |
| [app/bot/keyboards/tracking\_kb.py](/app/bot/keyboards/tracking_kb.py) | Python | 52 | 0 | 6 | 58 |
| [app/bot/main.py](/app/bot/main.py) | Python | 33 | 0 | 7 | 40 |
| [app/core/celery.py](/app/core/celery.py) | Python | 26 | 0 | 4 | 30 |
| [app/crud/add\_price\_record.py](/app/crud/add_price_record.py) | Python | 27 | 0 | 3 | 30 |
| [app/crud/price\_history.py](/app/crud/price_history.py) | Python | 24 | 0 | 8 | 32 |
| [app/crud/tracking.py](/app/crud/tracking.py) | Python | 105 | 0 | 19 | 124 |
| [app/crud/users.py](/app/crud/users.py) | Python | 23 | 0 | 3 | 26 |
| [app/db/base.py](/app/db/base.py) | Python | 95 | 0 | 22 | 117 |
| [app/db/redis.py](/app/db/redis.py) | Python | 6 | 0 | 1 | 7 |
| [app/db/session.py](/app/db/session.py) | Python | 18 | 0 | 9 | 27 |
| [app/scrapers/ktzh\_client.py](/app/scrapers/ktzh_client.py) | Python | 42 | 1 | 22 | 65 |
| [app/scrapers/ktzh\_parser.py](/app/scrapers/ktzh_parser.py) | Python | 61 | 2 | 22 | 85 |
| [app/services/cache\_service.py](/app/services/cache_service.py) | Python | 35 | 0 | 14 | 49 |
| [app/services/checker.py](/app/services/checker.py) | Python | 106 | 1 | 41 | 148 |
| [app/services/notifier.py](/app/services/notifier.py) | Python | 15 | 0 | 4 | 19 |
| [app/services/station\_repository.py](/app/services/station_repository.py) | Python | 15 | 0 | 2 | 17 |
| [app/services/stations.py](/app/services/stations.py) | Python | 15 | 0 | 2 | 17 |
| [app/tasks/checker\_tasks.py](/app/tasks/checker_tasks.py) | Python | 20 | 0 | 9 | 29 |
| [debounce.js](/debounce.js) | JavaScript | 18 | 0 | 5 | 23 |
| [docker-compose.yml](/docker-compose.yml) | YAML | 61 | 0 | 4 | 65 |
| [docs/db\_schema.md](/docs/db_schema.md) | Markdown | 59 | 0 | 14 | 73 |
| [requirements.txt](/requirements.txt) | pip requirements | 66 | 0 | 1 | 67 |
| [web/backend/api/\_\_init\_\_.py](/web/backend/api/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [web/backend/api/admin.py](/web/backend/api/admin.py) | Python | 1 | 1 | 2 | 4 |
| [web/backend/api/apps.py](/web/backend/api/apps.py) | Python | 3 | 0 | 3 | 6 |
| [web/backend/api/authentication.py](/web/backend/api/authentication.py) | Python | 49 | 0 | 17 | 66 |
| [web/backend/api/migrations/\_\_init\_\_.py](/web/backend/api/migrations/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [web/backend/api/models.py](/web/backend/api/models.py) | Python | 1 | 1 | 2 | 4 |
| [web/backend/api/serializers.py](/web/backend/api/serializers.py) | Python | 33 | 0 | 4 | 37 |
| [web/backend/api/tests.py](/web/backend/api/tests.py) | Python | 1 | 1 | 2 | 4 |
| [web/backend/api/urls.py](/web/backend/api/urls.py) | Python | 12 | 0 | 2 | 14 |
| [web/backend/api/views.py](/web/backend/api/views.py) | Python | 141 | 1 | 31 | 173 |
| [web/backend/config/\_\_init\_\_.py](/web/backend/config/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [web/backend/config/asgi.py](/web/backend/config/asgi.py) | Python | 4 | 8 | 5 | 17 |
| [web/backend/config/settings.py](/web/backend/config/settings.py) | Python | 105 | 25 | 38 | 168 |
| [web/backend/config/urls.py](/web/backend/config/urls.py) | Python | 6 | 16 | 3 | 25 |
| [web/backend/config/wsgi.py](/web/backend/config/wsgi.py) | Python | 4 | 8 | 5 | 17 |
| [web/backend/manage.py](/web/backend/manage.py) | Python | 15 | 3 | 5 | 23 |
| [web/frontend/README.md](/web/frontend/README.md) | Markdown | 36 | 0 | 24 | 60 |
| [web/frontend/src/app/app.config.ts](/web/frontend/src/app/app.config.ts) | TypeScript | 14 | 0 | 2 | 16 |
| [web/frontend/src/app/app.css](/web/frontend/src/app/app.css) | PostCSS | 0 | 0 | 1 | 1 |
| [web/frontend/src/app/app.routes.ts](/web/frontend/src/app/app.routes.ts) | TypeScript | 10 | 0 | 5 | 15 |
| [web/frontend/src/app/app.spec.ts](/web/frontend/src/app/app.spec.ts) | TypeScript | 20 | 0 | 4 | 24 |
| [web/frontend/src/app/app.ts](/web/frontend/src/app/app.ts) | TypeScript | 11 | 0 | 2 | 13 |
| [web/frontend/src/app/components/dashboard/dashboard.css](/web/frontend/src/app/components/dashboard/dashboard.css) | PostCSS | 101 | 1 | 24 | 126 |
| [web/frontend/src/app/components/dashboard/dashboard.spec.ts](/web/frontend/src/app/components/dashboard/dashboard.spec.ts) | TypeScript | 18 | 0 | 6 | 24 |
| [web/frontend/src/app/components/dashboard/dashboard.ts](/web/frontend/src/app/components/dashboard/dashboard.ts) | TypeScript | 104 | 0 | 20 | 124 |
| [web/frontend/src/app/components/tracking-create/tracking-create.css](/web/frontend/src/app/components/tracking-create/tracking-create.css) | PostCSS | 98 | 0 | 19 | 117 |
| [web/frontend/src/app/components/tracking-create/tracking-create.spec.ts](/web/frontend/src/app/components/tracking-create/tracking-create.spec.ts) | TypeScript | 18 | 0 | 6 | 24 |
| [web/frontend/src/app/components/tracking-create/tracking-create.ts](/web/frontend/src/app/components/tracking-create/tracking-create.ts) | TypeScript | 72 | 0 | 10 | 82 |
| [web/frontend/src/app/components/tracking-list/tracking-list.css](/web/frontend/src/app/components/tracking-list/tracking-list.css) | PostCSS | 296 | 7 | 62 | 365 |
| [web/frontend/src/app/components/tracking-list/tracking-list.spec.ts](/web/frontend/src/app/components/tracking-list/tracking-list.spec.ts) | TypeScript | 18 | 0 | 6 | 24 |
| [web/frontend/src/app/components/tracking-list/tracking-list.ts](/web/frontend/src/app/components/tracking-list/tracking-list.ts) | TypeScript | 52 | 0 | 12 | 64 |
| [web/frontend/src/app/interceptors/telegram-auth.interceptor.ts](/web/frontend/src/app/interceptors/telegram-auth.interceptor.ts) | TypeScript | 13 | 0 | 4 | 17 |
| [web/frontend/src/app/interceptors/tunnel-bypass.interceptor.ts](/web/frontend/src/app/interceptors/tunnel-bypass.interceptor.ts) | TypeScript | 13 | 0 | 2 | 15 |
| [web/frontend/src/app/services/stations.spec.ts](/web/frontend/src/app/services/stations.spec.ts) | TypeScript | 12 | 0 | 5 | 17 |
| [web/frontend/src/app/services/stations.ts](/web/frontend/src/app/services/stations.ts) | TypeScript | 22 | 0 | 6 | 28 |
| [web/frontend/src/app/services/telegram.spec.ts](/web/frontend/src/app/services/telegram.spec.ts) | TypeScript | 12 | 0 | 5 | 17 |
| [web/frontend/src/app/services/telegram.ts](/web/frontend/src/app/services/telegram.ts) | TypeScript | 36 | 0 | 9 | 45 |
| [web/frontend/src/app/services/tracking.spec.ts](/web/frontend/src/app/services/tracking.spec.ts) | TypeScript | 12 | 0 | 5 | 17 |
| [web/frontend/src/app/services/tracking.ts](/web/frontend/src/app/services/tracking.ts) | TypeScript | 57 | 0 | 18 | 75 |
| [web/frontend/src/environments/environment.prod.ts](/web/frontend/src/environments/environment.prod.ts) | TypeScript | 4 | 0 | 0 | 4 |
| [web/frontend/src/environments/environment.ts](/web/frontend/src/environments/environment.ts) | TypeScript | 4 | 0 | 0 | 4 |
| [web/frontend/src/main.ts](/web/frontend/src/main.ts) | TypeScript | 5 | 0 | 2 | 7 |
| [web/frontend/src/styles.css](/web/frontend/src/styles.css) | PostCSS | 24 | 1 | 2 | 27 |
| [web/frontend/src/types/telegram.d.ts](/web/frontend/src/types/telegram.d.ts) | TypeScript | 25 | 0 | 1 | 26 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)