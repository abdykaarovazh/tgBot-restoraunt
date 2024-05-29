import asyncio
from datetime import datetime, timedelta

from project.backend.src.telegram.bot import bot, logger
from project.backend.src.db.db_app import app
from project.backend.src.models.models import Tables, Users


async def check_reservations_alert(user_id):
    try:
        while True:
            with app.app_context():
                now = datetime.now()
                tomorrow = now + timedelta(days=1)
                user = Users.query.filter_by(tg_user_id=user_id).first()

                tables_reserved = Tables.get_all(user.tg_username, 'Y')

                if tables_reserved is not None:
                    for table in tables_reserved:
                        time_reserve = datetime.fromisoformat(table.time_reserve)

                        if tomorrow <= time_reserve < tomorrow + timedelta(days=1):
                            await bot.send_message(
                                user_id,
                                f'У вас есть <b>бронь!</b>\n'
                                f'<b>{time_reserve.strftime("%d.%m.%Y")}</b> в <b>{time_reserve.strftime("%H:%M")}</b> '
                                f'по адресу <b>{table.address}</b>.\n'
                                f'\n'
                                f'Не забудьте! Мы ждём Вас!')
            await asyncio.sleep(24*60*60)
    except Exception as e:
        logger.exception("alert", e)
