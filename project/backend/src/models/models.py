from flask_login import UserMixin

from project.backend.src.db.db_app import db


class Tables:
    def __init__(self, tables):
        self.tables = tables

    def reserve_table(self, table_name):
        if self.tables[table_name]['is_reserve'] == 'N':
            self.tables[table_name]['is_reserve'] = 'Y'
            print(f"Стол {table_name} забронирован!")
        else:
            print(f"Стол {table_name} уже забронирован!")

    def free_table(self, table_name):
        if self.tables[table_name]['is_reserve'] == 'Y':
            self.tables[table_name]['is_reserve'] = 'N'
            print(f"Стол {table_name} освобожден.")
        else:
            print(f"Стол {table_name} уже свободен.")


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
        try:
            new_user = cls(
                user_name=user_name,
                tg_user_id=tg_user_id,
                tg_username=tg_username,
                user_phone=user_phone)
            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
