from datetime import timedelta

from telebot.types import Message

from modules.loader import load_json, load_text
from modules.pset import PendingSet
from modules.quota import TimeQuota
from project.bot import bot


admins: frozenset[int] = load_json('configs/admins.json')
quotas: dict[str, int] = load_json('configs/quotas.json')
pending_set: PendingSet = PendingSet(
    on_error=lambda message: bot.send_message(
        chat_id=message.chat.id,
        text=load_text('texts/errors/not-pending.txt'),
    )
)
minutely_quota: TimeQuota[int] = TimeQuota(
    delta=timedelta(minutes=1),
    quota=quotas.get('minutely-per-member', 3),
)
daily_quota: TimeQuota[int] = TimeQuota(
    delta=timedelta(days=1),
    quota=quotas.get('daily-per-member', 10),
)
total_quota: TimeQuota[str] = TimeQuota(
    delta=timedelta(hours=1),
    quota=quotas.get('hourly-total', 20),
)


@bot.message_handler(commands=['start'])  # type: ignore[misc]
def on_start(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text=load_text('texts/start.txt'))


@bot.message_handler(commands=['new'])  # type: ignore[misc]
def on_new(message: Message) -> None:
    pending_set.add(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=load_text('texts/new.txt'))


@bot.message_handler(content_types=['text', 'photo'])  # type: ignore[misc]
@pending_set.assert_pending
def on_report(message: Message) -> None:
    match message.chat.id:
        case member if minutely_quota.exceeds(member):
            bot.send_message(
                chat_id=member,
                text=load_text('texts/errors/minutely-quota-exceeded.txt'),
            )
        case member if daily_quota.exceeds(member):
            bot.send_message(
                chat_id=member,
                text=load_text('texts/errors/daily-quota-exceeded.txt'),
            )
        case member if total_quota.exceeds('total'):
            bot.send_message(
                chat_id=member,
                text=load_text('texts/errors/total-quota-exceeded.txt'),
            )
        case _:
            for receiver in admins:
                bot.forward_message(
                    chat_id=receiver,
                    from_chat_id=member,
                    message_id=message.id,
                )
            bot.send_message(
                chat_id=message.chat.id,
                text=load_text('texts/success.txt'),
            )


if __name__ == '__main__':
    bot.infinity_polling()
