import uvicorn
from src.transport import *
from src.database import create_database, drop_tables


"""
Стек технологий для бэкенда:

    - python 3
    - fastapi
    - uvicorn
    - pydantic
    - postgres

"""


if __name__ == '__main__':
    # drop_tables()

    if create_database():
        uvicorn.run(app=app, host="0.0.0.0", port=8000)
