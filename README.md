# Cambridge Picture Portal

Portal, login, logout, and admin UI for the Cambridge Picture app suite.

This app depends on the shared auth package:

```bash
python -m pip install -e ../shared
```

The portal stores users in SQLite. Configure `USER_DB_PATH` to choose the
database location, or use the default `data/.user_store.sqlite3` path used by
the current deployment.
