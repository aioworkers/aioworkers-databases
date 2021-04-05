import pathlib

import pytest


def pytest_configure(config):
    # FIXME: Pass custom markers here instead of pyproject.toml because pytest ignore it there.
    config.addinivalue_line(
        "markers", "sqlite"
    )


@pytest.fixture(scope='session')
def db_name():
    return 'test.db.sqlite'


@pytest.fixture(scope='session')
def db_url(db_name):
    return f"sqlite:///{db_name}"


@pytest.fixture(autouse=True)
def _sqlite_marker(request):
    """
    Implement the sqlite marker.
    """
    marker = request.node.get_closest_marker('sqlite')
    if marker:
        request.getfixturevalue('sqlite_setup')


@pytest.fixture
def sqlite_setup(context, db_url, db_name):
    # Delete sqlite db file from previous run if something goes wrong
    p = pathlib.Path(__file__).parent.with_name(db_name)
    if p.exists():
        p.unlink()


@pytest.fixture
def config_yaml(db_url):
    return f"""
    db:
      cls: aioworkers_databases.database.Database
      url: {db_url}
    # Configure logging for debug purposes
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
        aioworkers:
          level: DEBUG
          handlers: [console]
          propagate: true
    """
