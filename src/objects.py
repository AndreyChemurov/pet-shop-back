from pydantic import BaseModel
from typing import (
    Dict,
    Optional
)

"""
Иерархия вызовов

1. Cart: сформированная корзина товаров, готовая для покупки.
2. Wallet: списание средств после покупки.
3. Response: возвращаемые значения после покупки.

"""


prices: Dict[str, int] = {
    "cat": 100,
    "dog": 120,
    "feed": 7,
    "toy": 4,
    "collar": 17
}


class Cart(BaseModel):
    cat: int = 0        # купить кошку, количество
    dog: int = 0        # купить собаку, количество
    feed: int = 0       # купить корм, количество
    toy: int = 0        # купить игрушку, количество
    collar: int = 0     # купить кошку, количество


# После покупки
class Response:
    def __init__(self, identifier):
        self.identifier = identifier


class Wallet(BaseModel):
    current: Optional[int] = None    # текущий баланс, хранится в БД, не передается в request
    assign: int                      # передается в request для пополнения, не хранится в БД


# После пополнения кошелька
class WalletResponse:
    def __init__(self, current):
        self.current = current


class Shop:
    items: Dict[str, int]   # [название товара, сколько стоит за штуку]
