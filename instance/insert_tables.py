import sqlite3
from project.backend.src.telegram.keyboard.reply.restoaddress import addresses

#def drop_table():
#    try:
#        connection = sqlite3.connect('diplom_sun_corner.db')
#        cursor = connection.cursor()
#        print("Подключились к БД")
#
#        sql_drop = """DROP TABLE tables"""
#        cursor.execute(sql_drop)
#        connection.commit()
#        print("Успешно удалили таблицу")
#        cursor.close()
#
#        connection.close()
#    except sqlite3.Error as e:
#        print("Ошибка : ", e)

def insert_tables():
    try:
        connection = sqlite3.connect('diplom_sun_corner.db')
        cursor = connection.cursor()
        print("Подключились к БД")

        for address in addresses:
            for i in range(1, 6):
                table_name = f"Столик №{i}"
                place_count = 2 if i == 1 or i == 4 else 4 if i == 2 or i == 3 else 6
                insert = f"""INSERT INTO tables(address, table_name, place_count, is_reserve, user_name, time_reserve)
                             VALUES (?, ?, ?, 'N', '', NULL);"""
                cursor.execute(insert, (address, table_name, place_count))

        connection.commit()
        print("Успешно внесли записи в БД")
        cursor.close()

        connection.close()
    except sqlite3.Error as e:
        print("Ошибка во время регистрации столов: ", e)


#drop_table()
insert_tables()
