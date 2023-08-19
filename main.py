from config import config
from src.utils import fill_db, get_data
from src.DBManager import DBManager


def main():

    companies_ids = [
        1122462,  # Skyeng
        15478,  # VK
        3529,  # Сбер
        1740,  # Яндекс
        4934,   # Билайн
        3127,   # Мегафон
        1942330,    # Пятёрочка
        592442,   # Деливери
        3530,   # Сдэк
        3776   # MTC
    ]

    database_name = 'hh_ru'
    params = config()

    fill_db(get_data(companies_ids), database_name, **params)

    db_manager = DBManager(database_name, params)


if __name__ == '__main__':
    main()