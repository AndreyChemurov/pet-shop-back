from src.config import app
from src.objects import (
    Cart,
    Response,
    Wallet,
    WalletResponse
)
from src.business import (
    buy as _buy,
    wallet as _wallet
)
from src.exceptions import (
    HTTP_400_WRONG_PARAMS,
    HTTP_400_WRONG_WALLET
)
from fastapi import HTTPException


@app.post("/buy")
def buy(cart: Cart):
    """
    Функция покупки всего, что находится в корзине.

    Товары в корзине (back-end) формируются через POST-запросы в JSON.
    """

    if (
            cart.cat < 0 or
            cart.dog < 0 or
            cart.feed < 0 or
            cart.toy < 0 or
            cart.collar < 0
    ):
        raise HTTPException(
            status_code=HTTP_400_WRONG_PARAMS['error']['status_code'],
            detail=HTTP_400_WRONG_PARAMS
        )

    bill = _buy(cart)  # Чек

    if "error" in bill:
        raise HTTPException(
            status_code=bill['error']['status_code'],
            detail=bill
        )

    return Response(identifier=bill['identifier'])


@app.post("/wallet")
def wallet(w: Wallet):
    """
    Функция пополнения баланса на кошельке.

    Сумма пополнения (back-end) формируется через POST-запрос в JSON.
    """

    if w.assign < 0:
        raise HTTPException(
            status_code=HTTP_400_WRONG_WALLET['error']['status_code'],
            detail=HTTP_400_WRONG_WALLET
        )

    new_wallet = _wallet(w)     # Новая текущая сумма на счете

    if "error" in new_wallet:
        raise HTTPException(
            status_code=new_wallet['error']['status_code'],
            detail=new_wallet
        )

    # возвращает current тоже, чтобы вывести на экране после пополнения
    return WalletResponse(current=new_wallet['current'])
