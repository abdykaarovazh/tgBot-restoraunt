from flask_login import UserMixin
from project.backend.src.db.db_app import db
from project.backend.src.telegram.bot import logger
from datetime import datetime

class Tables(db.Model):
    table_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    address      = db.Column(db.String(128), nullable=False)
    table_name   = db.Column(db.String(128), nullable=False)
    place_count  = db.Column(db.Integer,     nullable=False)
    is_reserve   = db.Column(db.String(1),   nullable=True)
    user_name    = db.Column(db.String(128), nullable=True)
    time_reserve = db.Column(db.String(20),  nullable=True)

    @classmethod
    def get_all(cls, user_name: str, is_reserve: str):
        all_tables = cls.query.filter_by(user_name=user_name, is_reserve=is_reserve).all()
        return all_tables if all_tables else None

    @classmethod
    def reserve(cls, address, table_name, tg_username, time, date):
        table = cls.query.filter_by(address=address, table_name=table_name).first()
        if table:
            table.is_reserve = 'Y'
            table.user_name = tg_username
            table.time_reserve = datetime.strptime(f'{date} {time}', '%d.%m.%Y %H:%M')
            db.session.commit()
        logger.info("Столик забронирован")
        return table

    @classmethod
    def unreserve(cls, tg_username, table_name):
        table = cls.query.filter_by(table_name=table_name, user_name=tg_username).first()
        if table and table.is_reserve == 'Y':
            table.is_reserve = 'N'
            table.user_name = None
            table.time_reserve = None
            db.session.commit()
        logger.info("Столик освободился")
        return table

    @classmethod
    def change_date_time(cls, tg_username, table_name, date, time):
        table = cls.query.filter_by(table_name=table_name, user_name=tg_username).first()

        if table.is_reserve == 'Y':
            table.time_reserve = datetime.strptime(f'{date} {time}', '%d.%m.%Y %H:%M')
            db.session.commit()
            logger.info("Время обновлено")
        return table


class Users(db.Model, UserMixin):
    user_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_name   = db.Column(db.String(128), nullable=False)
    tg_user_id  = db.Column(db.Integer,     nullable=False, unique=True)
    tg_username = db.Column(db.String(128), nullable=False, unique=True)
    user_phone  = db.Column(db.String(12),  nullable=False, unique=True)

    @classmethod
    def get_current(cls, tg_username):
        """
        :param tg_username:
        :return: Текущий пользователь
        """
        is_user = cls.query.filter_by(tg_username=tg_username).first()
        return is_user if is_user else None

    @classmethod
    def create(cls,
               user_name:   str,
               tg_user_id:  int,
               tg_username: str,
               user_phone:  str):
        """
        Функция создания нового пользователя в базе данных.
        :param user_phone: str
        :param tg_user_id: int
        :param tg_username: str
        :param user_name: str
        """
        try:
            new_user = cls(
                user_name=user_name,
                tg_user_id=tg_user_id,
                tg_username=tg_username,
                user_phone=user_phone
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            logger.exception("create user", e)
            db.session.rollback()
        finally:
            db.session.close()
