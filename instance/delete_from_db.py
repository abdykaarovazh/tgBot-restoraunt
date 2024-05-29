import sqlite3


def delete_from_db():
    try:
        connection = sqlite3.connect('diplom_sun_corner.db')
        cursor = connection.cursor()

        # sql_delete = """update tables
        #                    set user_name = 'airtooooour'
        #                   where user_name = '1068989629'"""
        sql_delete = """
            update 
        """
        cursor.execute(sql_delete)
        connection.commit()
        print("Успешно удалили записи из БД")
        cursor.close()

        connection.close()
    except sqlite3.Error as e:
        print("Ошибка во время удаления: ", e)


delete_from_db()
