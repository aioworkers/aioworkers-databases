import pytest

import sqlalchemy


metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(length=100)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


@pytest.mark.sqlite
async def test_database_sqlalchemy(context):
    await context.db.execute('CREATE TABLE notes (id int, text TEXT, completed boolean)')

    query = notes.insert()
    values = {"text": "example1", "completed": True}
    await context.db.execute(query=query, values=values)

    await context.db.execute('DROP TABLE notes;')
