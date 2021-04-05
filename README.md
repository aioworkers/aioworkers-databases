# aioworkers-databases

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-databases/CI)](https://github.com/aioworkers/aioworkers-databases/actions?query=workflow%3ACI)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-databases)](https://pypi.org/project/aioworkers-databases)
[![PyPI](https://img.shields.io/pypi/v/aioworkers-databases)](https://pypi.org/project/aioworkers-databases)

aioworkers plugin for [databases](https://github.com/encode/databases).

## Usage

Add your database config to aioworkers `config.yaml`:

```yaml
db:
  cls: aioworkers_databases.database.Database
  dsn: sqlite:///db.sqlite
logging:
  version: 1
  disable_existing_loggers: false
  root:
    level: ERROR
    handlers: [console]
  handlers:
    console:
      level: DEBUG
      class: logging.StreamHandler
  loggers:
    aioworkers_databases:
      level: ERROR
      handlers: [console]
      propagate: true
```

Run `aioworkers`:

```shell
aioworkers -c config.yaml -i        
```

Create `Context` for this config and use your db via context:

```python
await context.db.execute('CREATE TABLE some_table (id INT);')
```

## Development

Install requirements:

```shell
poetry install
```

Run tests:

```shell
pytest
```