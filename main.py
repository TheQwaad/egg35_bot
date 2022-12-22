import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time

from bot import Bot
from extra_commands import *
from json_commands import *

token = open("TOKEN.txt", "r").readline().strip()
group_id = open("GROUPID.txt", "r").readline().strip()

bot = Bot()
vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id)

#statistics_db = SQLiteDatabase("statistics")
#statistics_db.create_table("statistic", {"chat_id":"INT","user_id":"INT","messages":"INT"})

def get_rand():
    return random.randint(10 ** 5, 10 ** 6 - 1)


def write_message(user_id=-1, chat_id=-1, text="35", attachment="", disable_mentions = ""):
    args = {
        "message": text,
        "random_id": get_rand(),
        "attachment": attachment,
        "disable_mentions" : disable_mentions
    }
    if min(chat_id, user_id) != -1:
        raise "Can't be sent both to chat and to user"
    if chat_id != -1:
        args["chat_id"] = chat_id
    if user_id != -1:
        args["user_id"] = user_id
    vk.method("messages.send", args)


def bot_command(chat_id, message):
    attachment = ""
    text = ""
    disable_mentions = "false"
    for key in list(message.keys()):
        if key == "image":
            try:
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(message[key])
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            except:
                attachment = ""
        if key == "text":
            text = message[key]
        if key == "error":
            text = message[key]
            attachment = ""
            break
        if key == "mentions":
            disable_mentions = "true"
    write_message(chat_id=chat_id, text=text, attachment=attachment, disable_mentions=disable_mentions)

def main():
    print("Running!")
    while True:
        print("Reconnecting to longpoll...")
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_chat:
                        chance = random.randint(1, 15)
                        if len(event.message.text) > 0 and event.message.text[0] == '/':
                            if event.message.from_id < 0:
                                bot_command(event.chat_id, bot.get_command_res("bot", event.chat_id, event.message.from_id))
                            else:
                                json_update(json_change_statistics, "statistics", event.chat_id, event.message.from_id)
                                bot_command(event.chat_id, bot.get_command_res(event.message.text, event.chat_id, event.message.from_id))
                        if chance == 7:
                            bot_command(event.chat_id, bot.start_egg_game(event.chat_id))
                    if event.from_user:
                        write_message(text="Мой создатель клоун и не предусмотрел отправку сообщений в ЛС. Добавь меня в беседу", user_id=event.message.from_id)
        except:
            pass


if __name__ == '__main__':
    main()
