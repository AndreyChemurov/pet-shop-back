from psycopg2 import (
    connect,
    sql
)
from src.config import postgres_info
from src.exceptions import HTTP_500_DATABASE_CONNECTION_ERROR


def drop_tables():
    connection = connect(
        dbname=postgres_info['dbname'],
        user=postgres_info['user'],
        password=postgres_info['password'],
        host=postgres_info['host']
    )

    if not connection:
        return False

    statement = "DROP TABLE IF EXISTS cart, wallet;"

    with connection.cursor() as cursor:
        s = sql.SQL(statement)
        cursor.execute(s)

        connection.commit()
        cursor.close()

    if connection:
        connection.close()  # Проверка закрытости

    return True


def create_database():
    connection = connect(
        dbname=postgres_info['dbname'],
        user=postgres_info['user'],
        password=postgres_info['password'],
        host=postgres_info['host']
    )

    if not connection:
        return False

    statement = """
    CREATE TABLE IF NOT EXISTS cart (
        identifier SERIAL PRIMARY KEY,
        cat SMALLINT NOT NULL,
        dog SMALLINT NOT NULL,
        feed SMALLINT NOT NULL,
        toy SMALLINT NOT NULL,
        collar SMALLINT NOT NULL,
        total INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS wallet (
        current INTEGER NOT NULL CHECK(current >= 0)
    );
    
    INSERT INTO wallet (current) VALUES(0);
    """

    with connection.cursor() as cursor:
        s = sql.SQL(statement)
        cursor.execute(s)

        connection.commit()
        cursor.close()

    if connection:
        connection.close()  # Проверка закрытости

    return True


def create_bill(cat: int, dog: int, feed: int, toy: int, collar: int, total: int):
    connection = connect(
        dbname=postgres_info['dbname'],
        user=postgres_info['user'],
        password=postgres_info['password'],
        host=postgres_info['host']
    )

    if not connection:
        return HTTP_500_DATABASE_CONNECTION_ERROR

    with connection.cursor() as cursor:
        statement = "UPDATE wallet SET current = current-{};" \
                    "INSERT INTO cart (cat, dog, feed, toy, collar, total) " \
                    "VALUES({}, {}, {}, {}, {}, {}) RETURNING identifier;"\
            .format(total, cat, dog, feed, toy, collar, total)

        cursor.execute(statement)

        identifier = cursor.fetchone()[0]   # Получить ID чека

        connection.commit()
        cursor.close()

    if connection is not None:
        connection.close()  # Закрыть соединение

    return {"identifier": identifier}


def assign_wallet(money: int):
    connection = connect(
        dbname=postgres_info['dbname'],
        user=postgres_info['user'],
        password=postgres_info['password'],
        host=postgres_info['host']
    )

    if not connection:
        return HTTP_500_DATABASE_CONNECTION_ERROR

    with connection.cursor() as cursor:
        statement = "UPDATE wallet SET current = current+{} RETURNING current;".format(money)

        cursor.execute(statement)

        current_wallet = cursor.fetchone()[0]   # Получить текущий баланс

        connection.commit()
        cursor.close()

    if connection is not None:
        connection.close()  # Закрыть соединение

    return {"current": current_wallet}
