import datetime

admin_spam_dict = {}
class AdminSpam:
    def __init__(self, user_id):
        self.user_id = user_id
        self.date = []
        self.status = True
        self.ban_date = None


async def test(data, bot):
    try:
        admin_spam_dict[data.from_user.id]
    except KeyError:
        admin = AdminSpam(data.from_user.id)
        admin_spam_dict[data.from_user.id] = admin

    admin = admin_spam_dict[data.from_user.id]

    if admin.status is False:
        if datetime.datetime.now() - admin.ban_date > datetime.timedelta(seconds=10):
            admin.status = True
            return True
        else:
            return False

    admin.date.append(data.date)

    if len(admin.date) > 3:
        del admin.date[0]

    if len(admin.date) >= 3:
        if admin.date[2] - admin.date[0] < datetime.timedelta(seconds=1.5):
            admin.status = False
            admin.ban_date = datetime.datetime.now()

            try:
                await bot.send_message(data.from_user.id, text='❌ Отдохни секунд десять. Не спамь.\n❕ Причина: Спамер')
            except:
                pass

            return False
        return True
    else:
        return True


async def antibot(data, bot):
    try:
        admin = admin_spam_dict[data.from_user.id]
    except:
        return False
    admin.status = False
    admin.ban_date = datetime.datetime.now() + datetime.timedelta(minutes=1, seconds=10)

    try:
        await bot.send_message(data.from_user.id,
                               text='❌ Отдохни пожалуй пару минут и попробуй снова. Далее будь внимателен ❌\n❕ Причина: Сложная капча')
    except:
        pass
    return True
