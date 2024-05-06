# Создание и реализация Телеграм-бота на Aiogram в области рестораноого бизнеса.


### Обзор, выбор модулей для реализации и автоматизации основных бизнес-процессов ресторана
Ресторан называется "Sun Corner". Для него потребовалась разработка и реализация 
Телеграм-бота для автоматизации основных бизнес-процессов.

![Create new topic options](start_description_bot.png){ width=640 }{border-effect=line}

### Модули, использованные для программной реализации бота
При поставке задачи и выполнения, были выбраны модули, на основе которых реализован бот.
<procedure>
    <tabs>
        <tab title="Библиотека для бота">
            При выборе библиотеки для бота, был сделан выбор в пользу 
                <a href="https://aiogram.readthedocs.io/_/downloads/en/latest/pdf/">Aiogram 3</a>.
            Эта более новая версия (3.5.0) получила возможность встроить Web-приложение в бота,
            с которыми мы и будем работать далее.<br></br>
            Регистрация бота по правилам Телеграма происходит в боте <a href="https://t.me/BotFather">@BotFather</a>.
            <img src="created_bot.png" alt="create_bot" width="640" border-effect="rounded"/><br></br>
            Для того, чтобы Бот работал, нужно его определить в пространстве Python:<br></br>
            <code-block lang="plain text">
                bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
                dp = Dispatcher()
            </code-block><br></br>
            <shortcut>config.tg_bot.token</shortcut> - это специальная настройка проекта в файле <shortcut>config.py</shortcut>
            через файл переменных окружения <shortcut>.env</shortcut> для сокрытия личных данных.
            Эти данные также не косматятся в системе контроля версий GitHub.<br></br>
            Для того, чтобы начать работать с ботом, нужно сделать для него обработчик сообщений (<shortcut>handler</shortcut>)
            для команды <shortcut>/start</shortcut>:<br></br>
            <code-block>
                async def start(message: Message, state: FSMContext):
                    try:
                        with app.app_context():
                            tg_username = message.from_user.username
                            is_user = Users.get_current(tg_username=tg_username)
                            if is_user:
                                await message.answer("Salami! Рады, что ты снова решил обратиться к нам!\n"
                                                     "Хочешь забронировать столик? "
                                                     "Ты сможешь это сделать по команде /reserve")
                            else:
                                await message.answer("Salami! Рады, что ты решил(а) мной воспользоваться!\n"
                                                     "Давай зарегистрируем тебя у нас, чтобы ты мог без "
                                                     "повторной регистрации пользоваться"
                                                     "моими возможностями!")
                                await message.answer("Напиши, пожалуйста, своё имя?")
                                await state.set_state(UserStates.set_name)
                    except Exception as e:
                        print("START: ", e)
                        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, "
                                             "мы решаем эти проблемы....")
            </code-block><br></br>
            Здесь асинхронная функция start выступает в роли начальной команды для начала работы с Ботом.
            В ней мы проверяем пользователя зарегистрирован он или нет. Далее отталкиваемся от этого.<br></br>
            Если пользователь не зарегистрирован,
            то через метод <shortcut> Users.create()</shortcut> создаем пользователя в базе данных.<br></br>
            Для запуска бота и его <shortcut>хэндлеров</shortcut> используем следующй скрипт в файле <shortcut>run_bot.py</shortcut>:
            <br></br>
            <code-block>
                if __name__ == '__main__':
                    # Инициализируем таблицы в базе данных
                    with app.app_context():
                        db.create_all()
                    # Запускаем бота на локальном сервере
                    dp.run_polling(bot)
            </code-block><br></br>
            Далее уже создаем отдельные файлы для отдельных команд и регистрируем
            их в блоке запуска <code>if __name__ == '__main__'</code> методом <shortcut>Dispatcher</shortcut> следующим образом:<br></br>
            <code-block>
                # Регистрация команды /start
                dp.message.register(start, CommandStart())
                dp.message.register(set_name, UserStates.set_name)
                dp.message.register(set_phone, UserStates.set_phone)
            </code-block><br></br>
            Таким образом, мы реализуем backend Бота для работы основных бизнес-процессов.
        </tab>
        <tab title="Вендор базы данных">
            Мы знаем, что для реализации основных бизнес-процессов нам нужна база данных.<br></br>
            Основные задачи нашего Бота это бронь столиков.
            Для того, чтобы забронировать столик, нужно знать, кто его бронирует.<br></br>
            Таким образом, мы знаем, что у нас будет всего 2 таблицы:
            <procedure title="Таблицы Базы данных" id="tables-database">
                <step>
                    <p>Метаструктура таблицы <b>Users</b>:</p>
                    <code-block>
                        create table users(
                            user_id     serial primary key,
                            user_name   varchar(128) not null,
                            tg_user_id  integer not null unique,
                            tg_username varchar(128) not null unique,
                            user_phone  varchar(12) not null
                        );
                    </code-block>
                </step>
                <step>
                    <p>Метаструктура таблицы <b>Tables</b>:</p>
                    <code-block>
                        create table tables(
                            table_id     serial primary key,
                            address      varchar(128) not null,
                            table_name   varchar(128) not null,
                            place_count  integer not null,
                            is_reserve   varchar(1) not null,
                            user_name    varchar(128),
                            time_reserve date
                        );
                    </code-block>
                </step>
            </procedure>
            Т.к. мы не будем хранить большое количество информации,
            а наш бот является всего-лишь микросервисом нашей системы,
            сделаем выбор <b>Вендера базы данных</b> в пользу 
            <a href="https://docs.python.org/3/library/sqlite3.html">SQLite 3</a>
            и будем хранить данные в файле <shortcut>diplom_sun_corner.db</shortcut><br></br>
            Расширение для Pycharm SQLite Browser позволяет работать с данными в намного удобном формате.<br></br>
            Далее манипуляции с этой базой данных будет описаны в разделе <shortcut>ORM</shortcut>.
        </tab>
        <tab title="ORM">
            Самым популярным модулем для работы с базой данных в Python это <shortcut>SQLAlchemy</shortcut>.<br></br>
            Конкретно в данном проекте используется модуль
            <a href="https://flask-sqlalchemy.palletsprojects.com/en/latest/">Flask_SQLAlchemy</a>.
            Эта библиотека позволяет создавать образы таблиц и работать с ними на backend`e проекта.
            Используя эту библиотеку создаем файл <shortcut>models.py</shortcut>
            и в нём создаем классы <b>Users</b> и <b>Tables</b>:<br></br>
            <code-block>
                class Users(db.Model, UserMixin):
                    user_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
                    user_name   = db.Column(db.String(128), nullable=False)
                    tg_user_id  = db.Column(db.Integer,     nullable=False, unique=True)
                    tg_username = db.Column(db.String(128), nullable=False, unique=True)
                    user_phone  = db.Column(db.String(12),  nullable=False, unique=True)
            </code-block><br></br>
            <code-block>
                class Tables(db.Model):
                    table_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
                    address      = db.Column(db.String(128), nullable=False)
                    table_name   = db.Column(db.String(128), nullable=False)
                    place_count  = db.Column(db.Integer,     nullable=False)
                    is_reserve   = db.Column(db.String(1),   nullable=True)
                    user_name    = db.Column(db.String(128), nullable=True)
                    time_reserve = db.Column(db.DateTime,    nullable=True)
            </code-block><br></br>
            Эти классы и созданные методы этих классов позволяет манипулировать данными при работе Бота.
            Методы, созданные в этих классах будут описаны далее.
        </tab>
    </tabs>
</procedure>

### Описание работы методов таблицы Users
В классе `Users` для создания пользователя в Базе данных мы создаем `@classmethod Users.create`.
#### Метод create {collapsible="true"}
<code-block>
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
</code-block>
Таким образом, мы создаем пользователя. С помощью <shortcut>db.session.add(new_user)</shortcut> добавляем в БД запись
и с помощью <shortcut>db.session.commit()</shortcut> сохраняем изменение в базе данных. Обработка транзакции завершена.

#### Методы обработки данных таблицы Tables:
Для брони столиков используем 2 метода - `reserve` и `unreserve`:

#### Метод reserve {collapsible="true"}
<code-block>
    @staticmethod
    def reserve(table_name, tg_username):
        table = Tables.query.filter_by(table_name=table_name).first()
        if table:
            table.is_reserve = 'Y'
            table.user_name = tg_username
            db.session.commit()
        return table
</code-block>
Пользователь выбирает адрес и столик по адресу ресторана и с помощью этого метода
мы обновляем поля <shortcut>is_reserve</shortcut> на метку "Y"
и <shortcut>user_name</shortcut> на логин Телеграма пользователя (<shortcut>message.from_user.username</shortcut>).

#### Метод unreserve {collapsible="true"}
<code-block>
    @staticmethod
    def unreserve(tg_username):
        table = Tables.query.filter_by(user_name=tg_username).first()
        if table:
            table.is_reserve = 'N',
            table.user_name = None
            db.session.commit()
        return table
</code-block>
Здесь по Телегам-логину пользователя мы находим в базе данных столик,
забронированный на него и снимаем бронь действиями,
обратными методу <shortcut>Tables.reserve()</shortcut>

### Меню бота
Для лёгкой навигации пользователя в боте мы создадим меню.
Определяем команды и описание команд с помощью словаря `LEXICON`:
<procedure>
    <step>
        Словарь команд:
        <code-block>
            LEXICON_MENU_COMMANDS: dict[str, str] = {
                '/menu':        'Посмотреть меню ресторана',
                '/reserve':     'Бронь столика',
                '/description': 'Описание ресторана',
                '/feedback':    'Оставить отзыв',
                '/social':      'Другие социальные сети',
                '/support':     'Поддержка'
            }
        </code-block>
    </step>
    <step>
        Создание команд в меню бота:
        <code-block>
            # Кнопка меню, которая упаравляет основным функционалом
            async def set_main_menu(bot: Bot):
                main_menu_commands = [
                    BotCommand(
                        command=command,
                        description=description) for command, description in LEXICON_MENU_COMMANDS.items()
                ]
                await bot.set_my_commands(main_menu_commands)
        </code-block>
    </step>
    <step>
        Инициализация меню при запуске бота:
        <code-block>
            # Регистрация списка кнопок меню
            dp.startup.register(set_main_menu)
        </code-block>
    </step>
</procedure>


### Итог
Таким образом, мы реализовали основные бизнес-процессы бота-помощника ресторана "Sun Corner".
Реализованы основные команды бота, создана база данных на основе SQLite 3, backend бота связан с базой данных с помощью
flask_sqlalchemy.
Ознакомиться подробнее с проектом можно по ссылке ниже в подвале страницы.

<seealso>
    <category ref="wrs">
        Таким образом, мы реализуем основные бизнес-процессы бота-помощника ресторана "Sun Corner"
        <a href="https://t.me/zhazgulita">Телеграм автора</a>
        <a href="https://github.com/abdykaarovazh/tgBot-restoraunt">Репозиторий GitHub</a>
    </category>
</seealso>