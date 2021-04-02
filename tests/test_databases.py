import pytest


@pytest.mark.sqlite
async def test_database_basic(context):
    await context.db.execute('CREATE TABLE some_table (id INT);')
    await context.db.execute_many("INSERT INTO some_table(id) VALUES (:id)", [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ])

    rows = await context.db.fetch_all("SELECT * FROM some_table")
    assert [(1,), (2,), (3,)] == rows

    row = await context.db.fetch_one("SELECT id FROM some_table WHERE id = :id;", values={"id": 3})
    assert (3,) == row

    val = await context.db.fetch_val("SELECT id FROM some_table WHERE id = :id;", values={"id": 2})
    assert 2 == val

    transaction = await context.db.transaction()
    await context.db.execute("DELETE FROM some_table WHERE id = :id", values={"id": 2})
    await transaction.rollback()

    rows = [(1,), (2,), (3,)]
    index = 0
    async for row in context.db.iterate("SELECT * FROM some_table"):
        assert rows[index] == row
        index += 1

    await context.db.execute('DROP TABLE some_table;')
