import pathlib

import pytest


@pytest.fixture(scope="session")
def db_name():
    return "test.db.sqlite"


@pytest.fixture(scope="session")
def db_dsn(db_name):
    return f"sqlite:///{db_name}"


@pytest.fixture(autouse=True)
def _sqlite_marker(request):
    """
    Implement the sqlite marker.
    """
    marker = request.node.get_closest_marker("sqlite")
    if marker:
        request.getfixturevalue("sqlite_setup")


@pytest.fixture
def sqlite_setup(context, db_dsn, db_name):
    # Delete sqlite db file from previous run if something goes wrong
    p = pathlib.Path(__file__).parent.with_name(db_name)
    if p.exists():
        p.unlink()


@pytest.fixture
def config_yaml(db_dsn):
    return f"""
    db:
      cls: aioworkers_databases.database.Database
      dsn: {db_dsn}
    # Configure logger for debug
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
          level: DEBUG
          handlers: [console]
          propagate: true
    """
