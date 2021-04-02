import pytest


@pytest.mark.sqlite
async def test_database_basic(context):
    await context.db.execute('CREATE TABLE some_table (id INT);')

    query = "INSERT INTO some_table(id) VALUES (:id)"
    values = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]
    await context.db.execute_many(query, values)
    rows = await context.db.fetch_all("SELECT * FROM some_table")
    assert [(1,), (2,), (3,)] == rows

    await context.db.execute('DROP TABLE some_table;')
