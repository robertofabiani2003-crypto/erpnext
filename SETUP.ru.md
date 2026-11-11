# Локальный репозиторий ERPNext

Проверено 11 ноября 2026 года. Это исходный код приложения ERPNext, которое
работает внутри Frappe Bench. Сам checkout не является запущенным ERP-сайтом.

## Fork и рабочая ветка

- GitHub: https://github.com/robertofabiani2003-crypto/erpnext
- GitHub API подтвердил `fork=true`, `parent=frappe/erpnext`, `source=frappe/erpnext`.
- `origin`: https://github.com/robertofabiani2003-crypto/erpnext.git
- `upstream`: https://github.com/frappe/erpnext.git
- Локальная ветка: `codex/erpnext-setup`.
- База: ERPNext `v16.54.0`, commit `495380b59c8701629f25089bd3807e6ddf7f26c6`.
- На момент подготовки `origin/version-16` совпадал с этим релизом.

Checkout содержит все 5641 файл релиза. История локально сокращена до одного
коммита: полный fetch прерывался на медленном соединении, поэтому загружен
фиксированный релиз с `--depth=1`. Для анализа старой истории при необходимости:

```powershell
git fetch --unshallow origin
```

Исходная папка содержала только пустой `.git`, без коммитов, remotes и рабочих
файлов. Чужие изменения не переносились. Ветка создана непосредственно от тега;
публикаций, push, merge и PR при подготовке не выполнялось.

## Зафиксированная совместимость

Выбран поддерживаемый major v16; планируемый конец поддержки — конец 2029 года.
Точные версии приложений:

| Компонент | Версия | Commit |
| --- | --- | --- |
| ERPNext | v16.54.0 | `495380b59c8701629f25089bd3807e6ddf7f26c6` |
| Frappe | v16.56.0 | `49789a1711d4dde2be9c6888efe35651465f4b64` |

В `pyproject.toml` ERPNext указан диапазон Frappe `>=16.55.0,<17.0.0`.
Выбранный Frappe удовлетворяет ему и требует Python `>=3.14,<3.15`;
его `package.json` требует Node.js `>=24`.

Официальная инструкция для v16 указывает Python 3.14, Node.js 24, MariaDB 11.8,
Redis/Valkey 6+, Yarn 1.22+ и pip 25.3+. Для PDF нужен Chromium.
Для установки из исходников рекомендуются Debian 13+ или Ubuntu 24.04+;
на Windows нужен Linux через WSL либо контейнеры. Версии приложений в собственном
Docker-образе необходимо фиксировать тегами выше: одинаковые номера patch/minor
для ERPNext и Frappe не требуются. Не использовать плавающий `develop`.

## Проверки и границы подготовки

- GitHub metadata подтвердили происхождение fork и стабильные, не предварительные релизы.
- GitHub API и `git ls-remote upstream` подтвердили commit тега ERPNext.
- HEAD, `origin/version-16` и `v16.54.0` совпали.
- После checkout рабочее дерево было чистым; `git fsck --full` завершился успешно.
- В эту задачу добавлен только данный документ. Прикладной код не менялся.
- Сайт, база данных и контейнеры локально не запускались; runtime-проверки
  выполняет отдельный чат деплоя. Сервер в этой задаче не менялся.
- Передача для деплоя: соседний файл `ERPNext-handoff/repository.md` вне Git.
  Он не должен содержать пароли, токены или ключи.

Обновления сначала проверять на отдельной рабочей ветке и тестовом сайте.
Перед сменой версий на рабочем сайте нужны резервная копия базы и файлов,
проверка миграций и возможность восстановить предыдущую версию.

## Официальные источники

Последующая синхронизация 11.11.2026: ветка публикуется в `origin`, файлы деплоя
и снимок несекретных передач включены в Git. Серверный checkout этой же ветки
размещается в `/opt/erpnext/source`. Основной runtime продолжает использовать
зафиксированный образ ERPNext 16.54.0 / Frappe 16.56.0. Секреты и данные остаются
в защищённом серверном хранилище. Подробности: `deploy/README.ru.md`.

- Поддержка версий: https://frappe.io/support-versions
- ERPNext release: https://github.com/frappe/erpnext/releases/tag/v16.54.0
- Frappe release: https://github.com/frappe/frappe/releases/tag/v16.56.0
- ERPNext dependencies: https://github.com/frappe/erpnext/blob/v16.54.0/pyproject.toml
- Frappe dependencies: https://github.com/frappe/frappe/blob/v16.56.0/pyproject.toml
- Node.js requirement: https://github.com/frappe/frappe/blob/v16.56.0/package.json
- Установка: https://docs.frappe.io/framework/user/en/installation
- Официальная контейнерная инфраструктура: https://github.com/frappe/frappe_docker
