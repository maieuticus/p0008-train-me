import os

import pytest


@pytest.mark.skipif(os.environ.get("RUN_DATABASE_TESTS") != "1", reason="RUN_DATABASE_TESTS=1 benötigt PostgreSQL")
def test_postgres_connection():
    import psycopg

    with psycopg.connect(
        host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"], user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"], connect_timeout=5,
    ) as connection:
        assert connection.execute("SELECT 1").fetchone() == (1,)
