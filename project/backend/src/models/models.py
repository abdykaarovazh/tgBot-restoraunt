from flask_login import UserMixin
from project.backend.src.db.db_app import db


class Tables(db.Model):
    table_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    address      = db.Column(db.String(128), nullable=False)
    table_name   = db.Column(db.String(128), nullable=False)
    place_count  = db.Column(db.Integer,     nullable=False)
    is_reserve   = db.Column(db.String(1),   nullable=True)
    user_name    = db.Column(db.String(128), nullable=True)
    time_reserve = db.Column(db.DateTime,    nullable=True)

    @staticmethod
    def reserve(table_name, tg_username):
        table = Tables.query.filter_by(table_name=table_name).first()
        if table:
            table.is_reserve = 'Y'
            table.user_name = tg_username
            db.session.commit()
        print("Столик забронирован")
        return table

    @staticmethod
    def unreserve(tg_username):
        table = Tables.query.filter_by(user_name=tg_username).first()
        if table:
            table.is_reserve = 'N',
            table.user_name = None
            db.session.commit()

        return table


class Users(db.Model, UserMixin):
    user_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_name   = db.Column(db.String(128), nullable=False)
    tg_user_id  = db.Column(db.Integer,     nullable=False, unique=True)
    tg_username = db.Column(db.String(128), nullable=False, unique=True)
    user_phone  = db.Column(db.String(12),  nullable=False, unique=True)

    @staticmethod
    def get_current(tg_username):
        is_user = Users.query.filter_by(tg_username=tg_username).first()
        return is_user

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

            return new_user
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()







