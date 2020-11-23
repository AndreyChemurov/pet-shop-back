from src.objects import (
    Cart,
    Wallet,
    prices
)
from src.database import (
    create_bill,
    assign_wallet
)


def buy(c: Cart):
    """
    Функция принимает товары на вход, высчитывает общую стоимость, списывает средства и заносит чек в БД (атомарно),
    возвращает ID чека (serial в БД).
    """

    # Общая стоимость за все товары
    total = 0
    for k, v in c.dict().items():
        total += prices[k] * v

    # Работа с базой данных (создание записи)
    bill_identifier = create_bill(c.cat, c.dog, c.feed, c.toy, c.collar, total)

    return bill_identifier


def wallet(w: Wallet):
    """
    Функция принимает текущий кошелек на вход и обновляет данные в БД таблицы wallet.
    """

    new_wallet = assign_wallet(w.assign)

    return new_wallet
